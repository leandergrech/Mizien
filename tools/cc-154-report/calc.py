#!/usr/bin/env python3
"""CC-154: date arithmetic for the timeline and the checks sheet. Writes data/cc-154/checks.csv.
Dates come from the sources in the report: CJEU judgment C-23/23 (19 Sep 2024); Commission letter Ares(2025)8980114,
e-signed 24 Oct 2025 (the date Italpress gives is 27 Oct 2025); new derogation 17 Oct 2025 (as stated in the letter);
BirdLife Malta posts of 1 Nov and 21 Nov 2025; Italpress 2 Nov 2025."""
import csv, pathlib, datetime
ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "cc-154"; OUT.mkdir(parents=True, exist_ok=True)
SRC = "Commission letter Ares(2025)8980114 (BirdLife Malta copy, retrieved 9 Nov 2026); CJEU C-23/23 (EUR-Lex); Italpress 2 Nov 2025; BirdLife Malta 1 and 21 Nov 2025"
D = datetime.date.fromisoformat
d = lambda a, b: (D(b) - D(a)).days
rows = [
 ("Days from the CJEU judgment (19 Sep 2024) to the new derogation (17 Oct 2025)", d("2024-09-19", "2025-10-17"), "days", "judgment date from EUR-Lex; derogation date as stated in the Commission letter"),
 ("Days from the new derogation (17 Oct 2025) to the letter's electronic signature (24 Oct 2025)", d("2025-10-17", "2025-10-24"), "days", "signature date printed on the letter"),
 ("Days between the letter's signature date (24 Oct) and the date Italpress gives (27 Oct)", d("2025-10-24", "2025-10-27"), "days", "unexplained difference; the PDF's file name carries a different Ares number from the Ref. printed in the letter"),
 ("Days from the letter's signature to BirdLife Malta's post (1 Nov 2025)", d("2025-10-24", "2025-11-01"), "days", "BirdLife post date"),
 ("Days from the new derogation (17 Oct 2025) to BirdLife's report of a new formal notice (21 Nov 2025)", d("2025-10-17", "2025-11-21"), "days", "second-hand: Commission notice INFR(2025)2128 not read"),
]
with open(OUT / "checks.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["check", "value", "unit", "source", "note"])
    for c, v, u, n in rows: w.writerow([c, v, u, SRC, n])
for c, v, u, n in rows: print(c, "=", v, u)
