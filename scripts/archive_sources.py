#!/usr/bin/env python3
"""Archive every claim source and record a content hash.

For each URL in data/sources.csv this script:
  1. checks robots.txt and skips automated fetching where it is disallowed,
  2. fetches the page and records its SHA-256 and retrieval time,
  3. looks for an existing Wayback Machine snapshot, and asks the Wayback Machine to save one if none exists.

Results go to archive/manifest.csv. Run from the repository root:
    python scripts/archive_sources.py [--limit N] [--no-save]

It needs network access and is deliberately slow (one request every few seconds). Sources that block
automation are marked 'robots_disallowed': archive those by hand in a browser and paste the snapshot URL
into archive/manifest.csv. Never commit paywalled PDFs; the manifest stores links and hashes only.
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


def robots_ok(url: str) -> bool:
    p = urllib.parse.urlparse(url)
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(f"{p.scheme}://{p.netloc}/robots.txt")
    try:
        rp.read()
    except Exception:
        return True  # robots.txt unreachable: proceed politely
    return rp.can_fetch(UA, url)


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
    args = ap.parse_args()

    with open(ROOT / "data" / "sources.csv", newline="", encoding="utf-8") as f:
        sources = [r for r in csv.DictReader(f) if str(r.get("URL", "")).startswith("http")]
    manifest_path = ROOT / "archive" / "manifest.csv"
    done = {}
    if manifest_path.exists():
        with open(manifest_path, newline="", encoding="utf-8") as f:
            done = {r["url"]: r for r in csv.DictReader(f)}

    rows = []
    for i, s in enumerate(sources):
        if args.limit and i >= args.limit:
            break
        url = s["URL"]
        prev = done.get(url)
        if prev and prev.get("sha256") and prev.get("archived_url"):
            rows.append(prev)
            continue
        row = {"claim_ids": s["Claim IDs"], "title": s["Source"], "url": url, "status": "", "http_status": "",
               "sha256": "", "retrieved_utc": "", "archived_url": "", "notes": ""}
        if not robots_ok(url):
            row["status"] = "robots_disallowed"
            row["notes"] = "Automated access disallowed. Archive manually in a browser."
        else:
            try:
                code, body = fetch(url)
                row.update(status="fetched", http_status=str(code), sha256=hashlib.sha256(body).hexdigest(),
                           retrieved_utc=dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
            except urllib.error.HTTPError as e:
                row.update(status="http_error", http_status=str(e.code))
            except Exception as e:  # network error, timeout, bad TLS
                row.update(status="error", notes=str(e)[:150])
        row["archived_url"] = wayback_lookup(url)
        if not row["archived_url"] and not args.no_save:
            row["archived_url"] = wayback_save(url)
        rows.append(row)
        print(f"[{i + 1}/{len(sources)}] {row['status']:>18}  {url[:80]}")
        time.sleep(4)

    manifest_path.parent.mkdir(exist_ok=True)
    with open(manifest_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {len(rows)} rows to {manifest_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
