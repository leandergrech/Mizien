#!/usr/bin/env python3
"""Archive every claim source and record a content hash.

For each URL in data/sources.csv this script:
  1. checks robots.txt and skips automated fetching where it is disallowed,
  2. fetches the page and records its SHA-256 and retrieval time,
  3. looks for an existing Wayback Machine snapshot, and asks the Wayback Machine to save one if none exists.

Results go to archive/manifest.csv. Run from the repository root:
    python scripts/archive_sources.py [--limit N] [--no-save]

It needs network access and is deliberately slow (one request every few seconds). Sources that block
automation are marked 'robots_disallowed' (a robots.txt rule) or 'robots_refused' (robots.txt itself refused the
archiver: a bot wall): archive those by hand in a browser and paste the snapshot URL into archive/manifest.csv. Never commit paywalled PDFs; the manifest stores links and hashes only.
"""
import argparse
import csv
import datetime as dt
import hashlib
import json
import pathlib
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser

ROOT = pathlib.Path(__file__).resolve().parent.parent
UA = "Mizien-archiver/1.0 (public claim-checking project)"
FIELDS = ["claim_ids", "title", "url", "status", "http_status", "sha256", "retrieved_utc", "archived_url", "notes"]


def robots_check(url: str) -> str:
    """'allowed', 'disallowed' (robots.txt has a rule against this page) or 'refused' (robots.txt itself answered
    401/403 to the archiver: a bot wall, not a rule; skipped all the same, and archived by hand).

    robots.txt is fetched with the archiver's own User-Agent. RobotFileParser.read() would send Python's default
    one, which some sites refuse even where their robots.txt allows the page (amphora.media did, 5 Oct 2026).
    """
    p = urllib.parse.urlparse(url)
    rp = urllib.robotparser.RobotFileParser()
    req = urllib.request.Request(f"{p.scheme}://{p.netloc}/robots.txt", headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            rp.parse(r.read().decode("utf-8", "surrogateescape").splitlines())
    except urllib.error.HTTPError as e:
        if e.code in (401, 403):
            return "refused"
        return "disallowed" if e.code >= 500 else "allowed"   # RFC 9309: 4xx allows all, 5xx disallows all
    except Exception:
        return "allowed"  # robots.txt unreachable: proceed politely
    return "allowed" if rp.can_fetch(UA, url) else "disallowed"


def fetch(url: str, timeout: int = 40):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read()


def wayback_lookup(url: str) -> str:
    api = "https://archive.org/wayback/available?url=" + urllib.parse.quote(url, safe="")
    try:
        _, body = fetch(api, timeout=30)
        snap = json.loads(body).get("archived_snapshots", {}).get("closest")
        return snap["url"] if snap and snap.get("available") else ""
    except Exception:
        return ""


def wayback_save(url: str) -> str:
    try:
        req = urllib.request.Request("https://web.archive.org/save/" + url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=120) as r:
            loc = r.headers.get("Content-Location") or ""
            return ("https://web.archive.org" + loc) if loc.startswith("/web/") else r.geturl()
    except Exception:
        return ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--no-save", action="store_true", help="only look up existing snapshots")
    ap.add_argument("--claim-id", action="append", default=[], help="archive sources for this claim only (repeatable)")
    args = ap.parse_args()

    with open(ROOT / "data" / "sources.csv", newline="", encoding="utf-8") as f:
        sources = [r for r in csv.DictReader(f) if str(r.get("URL", "")).startswith("http")]
    if args.claim_id:
        wanted = set(args.claim_id)
        sources = [r for r in sources if wanted.intersection(x.strip() for x in r.get("Claim IDs", "").split(","))]
    manifest_path = ROOT / "archive" / "manifest.csv"
    def ids(text):
        return {x.strip() for x in str(text or "").split(",") if x.strip()}

    # Rows recorded by hand (maintainer copies, browser reads, transcriptions) and rows already fetched and archived
    # are kept as they are; only automated failures and gaps are tried again. A URL cited by several sources is
    # fetched once, and rows whose URL has left data/sources.csv stay in the manifest.
    retry = {"", "error", "http_error", "robots_disallowed", "robots_refused"}
    out, extra = {}, []    # extra: a second hand-made row for the same URL (two copies), kept as it is
    if manifest_path.exists():
        with open(manifest_path, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                prev = out.get(r["url"])
                if prev is None:
                    out[r["url"]] = r
                    continue
                keep, drop = (prev, r) if r["status"] in retry else (r, prev)
                if drop["status"] not in retry:      # both made by hand: keep both
                    extra.append(r)
                    continue
                keep["archived_url"] = keep.get("archived_url") or drop.get("archived_url", "")
                keep["claim_ids"] = ", ".join(sorted(ids(keep.get("claim_ids")) | ids(drop.get("claim_ids"))))
                out[r["url"]] = keep
    todo = []
    for s in sources:
        url = s["URL"]
        prev = out.get(url)
        if prev is not None:
            prev["claim_ids"] = ", ".join(sorted(ids(prev.get("claim_ids")) | ids(s.get("Claim IDs"))))
            if prev.get("status") not in retry and not (prev.get("status") == "fetched" and not prev.get("archived_url")):
                continue
        if url not in todo:
            todo.append(url)
    titles = {s["URL"]: s for s in reversed(sources)}
    for i, url in enumerate(todo):
        if args.limit and i >= args.limit:
            break
        prev, s = out.get(url), titles[url]
        if prev and prev.get("status") == "fetched":      # hashed before; only the snapshot is missing
            prev["archived_url"] = wayback_lookup(url) or ("" if args.no_save else wayback_save(url))
            print(f"[{i + 1}/{len(todo)}] {'snapshot' if prev['archived_url'] else 'no snapshot':>18}  {url[:80]}")
            time.sleep(2)
            continue
        row = {"claim_ids": (prev or {}).get("claim_ids") or s["Claim IDs"], "title": s["Source"], "url": url,
               "status": "", "http_status": "", "sha256": "", "retrieved_utc": "", "archived_url": "", "notes": ""}
        robots = robots_check(url)
        if robots == "disallowed":
            row["status"] = "robots_disallowed"
            row["notes"] = "Automated access disallowed. Archive manually in a browser."
        elif robots == "refused":
            row["status"] = "robots_refused"
            row["notes"] = "robots.txt refused the archiver (HTTP 401/403; a bot wall, not a rule). Archive manually in a browser."
        else:
            try:
                code, body = fetch(url)
                row.update(status="fetched", http_status=str(code), sha256=hashlib.sha256(body).hexdigest(),
                           retrieved_utc=dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
            except urllib.error.HTTPError as e:
                row.update(status="http_error", http_status=str(e.code))
            except Exception as e:  # network error, timeout, bad TLS
                row.update(status="error", notes=str(e)[:150])
        row["archived_url"] = wayback_lookup(url) or (prev or {}).get("archived_url", "")
        if not row["archived_url"] and not args.no_save:
            row["archived_url"] = wayback_save(url)
        out[url] = row
        print(f"[{i + 1}/{len(todo)}] {row['status']:>18}  {url[:80]}")
        time.sleep(4)

    rows = list(out.values()) + extra
    manifest_path.parent.mkdir(exist_ok=True)
    with open(manifest_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {len(rows)} rows to {manifest_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
