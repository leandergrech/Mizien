"""Claim Check 086: date arithmetic and counts from data/cc-086/statements.csv. Output: data/cc-086/checks.csv"""
import csv
import datetime as dt
import pathlib

D = pathlib.Path(__file__).resolve().parents[2] / "data" / "cc-086"
rows = list(csv.DictReader(open(D / "statements.csv", encoding="utf-8", newline="")))
by = {r["id"]: r for r in rows}
d = lambda s: dt.date.fromisoformat(s)
pledge, mta, shift = d(by["S3"]["date"]), d(by["S5"]["date"]), d(by["S8"]["date"])
today = dt.date(2026, 10, 12)
met_summer_end = dt.date(2026, 8, 31)       # meteorological summer (Northern Hemisphere)
late_summer_end = dt.date(2026, 9, 30)      # most generous reading: tourist season to the end of September
checks = [
    ("Days from Borg's words to the MTA's statement", (mta - pledge).days, "days", "S3, S5", "14 Apr 2025 to 8 Feb 2026"),
    ("Days from the MTA's statement to 1 Jun 2026", (dt.date(2026, 6, 1) - mta).days, "days", "S5", "the season the pledge named had not begun"),
    ("Days since 31 Aug 2026 (meteorological summer ends)", (today - met_summer_end).days, "days", "calendar", "to 12 Oct 2026"),
    ("Days since 30 Sep 2026 (most generous reading of summer)", (today - late_summer_end).days, "days", "calendar", "to 12 Oct 2026"),
    ("Days from 1 Jun 2026 to The Shift's report", (shift - dt.date(2026, 6, 1)).days, "days", "S8", "24 Jun 2026: still no tender reported"),
    ("Kiosk concessions stated by the Minister", 11, "kiosks", "S1", "'around 11 kiosks' (3 Mar 2025); no later count found, so a reduction cannot be tested"),
    ("Kiosk tender notices found", 0, "notices", "literature/CC-086/notes.md", "none found in the places searched (not a count of all notices)"),
]
with open(D / "checks.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, lineterminator="\r\n")
    w.writerow(["check", "value", "unit", "source", "note"])
    w.writerows(checks)
for c in checks:
    print(*c, sep=" | ")
