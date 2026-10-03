#!/usr/bin/env python3
"""Check which source hosts this machine can reach, before a claim check starts.

Scheduled cloud runs sit behind an egress allowlist. A host that the allowlist refuses cannot be read
at all, so a check that depends on it must wait for a human or for a wider allowlist, not be marked
"In progress" and abandoned. Run from the repository root:

    python scripts/net_check.py            # core research hosts only
    python scripts/net_check.py CC-013     # core hosts plus every host in data/sources.csv for CC-013

Each host is reported as one of:
  ok             the site answered (2xx or 3xx)
  site-refused   the site answered with an error (often a bot wall: 403, 429, 503); try a browser or an archive
  proxy-refused  the network proxy refused the connection: the host is not on the allowlist
  error          timeout, DNS or TLS failure

Exit code: 0 if every core host and at least one of the claim's hosts were reached,
3 if a core host was refused by the proxy (the environment is locked down), 4 if every one of the
claim's own hosts was refused by the proxy.
"""
import csv
import pathlib
import sys
import urllib.error
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
UA = "Mozilla/5.0 (Mizien source check)"
CORE = {
    "api.crossref.org": "https://api.crossref.org/works?rows=0",
    "ec.europa.eu": "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/nrg_ind_ren?geo=MT&lastTimePeriod=1",
    "web.archive.org": "https://web.archive.org/",
    "www.eea.europa.eu": "https://www.eea.europa.eu/",
}


def probe(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA}, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return "ok" if r.status < 400 else f"site-refused {r.status}"
    except urllib.error.HTTPError as e:
        return f"site-refused {e.code}"
    except urllib.error.URLError as e:
        reason = str(e.reason)
        if "Tunnel connection failed" in reason or "403" in reason:
            return "proxy-refused"
        return f"error {reason[:60]}"
    except Exception as e:  # noqa: BLE001 - report anything else as an error
        return f"error {type(e).__name__}"


def claim_hosts(cid: str) -> dict:
    hosts = {}
    with open(ROOT / "data" / "sources.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if cid not in (row.get("Claim IDs") or ""):
                continue
            url = (row.get("URL") or "").strip()
            p = urllib.parse.urlparse(url)
            if p.scheme in ("http", "https") and p.netloc and p.netloc not in hosts:
                hosts[p.netloc] = f"{p.scheme}://{p.netloc}/"
    return hosts


def main() -> int:
    cid = sys.argv[1] if len(sys.argv) > 1 else None
    core = {h: probe(u) for h, u in CORE.items()}
    own = {h: probe(u) for h, u in claim_hosts(cid).items()} if cid else {}
    for label, res in (("core", core), (cid or "", own)):
        for h, s in res.items():
            print(f"{label:7} {h:40} {s}")
    if any(s == "proxy-refused" for s in core.values()):
        print("RESULT locked: core research hosts are refused by the network proxy.")
        return 3
    if own and all(s == "proxy-refused" for s in own.values()):
        print(f"RESULT blocked: every source host for {cid} is refused by the network proxy.")
        return 4
    print("RESULT ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
