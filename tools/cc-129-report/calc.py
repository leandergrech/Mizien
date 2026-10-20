#!/usr/bin/env python3
"""CC-129: how late was Malta's NAPCP update when the Commission acted? Date arithmetic only, from
data/cc-129/timeline.csv. Writes data/cc-129/checks.csv. Directive 2016/2284 Art. 6(3) requires an update 'at least every
four years' without naming the start date, so two readings are shown: four years from the first due date (1 Apr 2019) and
four years from the March 2020 version (second-hand)."""
import csv, datetime as dt, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-129"
SRC = "data/cc-129/timeline.csv; Directive 2016/2284 Art. 6(3), 10(1); retrieved 20 Oct 2026"
lfn = dt.date(2025, 7, 17)
due_a = dt.date(2023, 4, 1)   # first due date + 4 years
due_b = dt.date(2024, 3, 1)   # March 2020 + 4 years (second-hand start)
today = dt.date(2026, 10, 20)
rows = []
def add(check, value, unit, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": SRC, "note": note})
add("Update due, reading A (first due date 1 Apr 2019 + 4 years)", due_a.isoformat(), "date")
add("Months from reading-A due date to letter of formal notice", round((lfn - due_a).days / 30.44, 1), "months", f"{(lfn - due_a).days} days")
add("Update due, reading B (March 2020 version + 4 years, second-hand start)", due_b.isoformat(), "date", "month only; 1 March assumed")
add("Months from reading-B due date to letter of formal notice", round((lfn - due_b).days / 30.44, 1), "months", f"{(lfn - due_b).days} days (about)")
add("Months from letter of formal notice to the 2026 draft consultation (June 2026, month only)", round((dt.date(2026, 6, 1) - lfn).days / 30.44, 1), "months", "approximate")
add("Months from letter of formal notice to today", round((today - lfn).days / 30.44, 1), "months")
add("Member States in the same letters of formal notice (July 2025 package)", 6, "states", "Croatia, Latvia, Hungary, Malta, Portugal, Slovakia")
with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for r in rows: print(f"{r['check'][:80]:80s} {r['value']:>12} {r['unit']} {r['note']}")
