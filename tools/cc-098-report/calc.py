#!/usr/bin/env python3
"""CC-098: date arithmetic for the timeline and the checks sheet. Writes data/cc-098/checks.csv.
All dates are from sources in the report: Graffitti release (24 Jun 2026), TVM News (24 Jun 2026), Newsbook (25 Jun 2026)."""
import csv, pathlib, datetime
ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "cc-098"; OUT.mkdir(parents=True, exist_ok=True)
SRC = "Moviment Graffitti release 24 Jun 2026; TVM News 24 Jun 2026; Newsbook 25 Jun 2026"
d = lambda a, b: (datetime.date.fromisoformat(b) - datetime.date.fromisoformat(a)).days
rows = [
    {"check": "Days from the incident (14 Jun 2026) to the NGO's release", "value": d("2026-06-14", "2026-06-24"), "unit": "days", "source": SRC, "note": "incident date as stated by the NGO"},
    {"check": "Days from the release to the Prime Minister's reported response (Newsbook)", "value": d("2026-06-24", "2026-06-25"), "unit": "days", "source": SRC, "note": "response date taken as the article date; the remarks may predate it"},
]
with open(OUT / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, ["check", "value", "unit", "source", "note"]); w.writeheader(); w.writerows(rows)
for r in rows: print(r["check"], "=", r["value"], r["unit"])
