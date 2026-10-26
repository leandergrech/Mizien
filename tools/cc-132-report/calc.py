#!/usr/bin/env python3
"""CC-132: test the Commission's sentence on public-transport non-use with formulas, not by eye.

Reads data/cc-132/ (Eurostat ilc_atst01, ilc_atst02; retrieved 26 Oct 2026) and writes data/cc-132/checks.csv.
"""
import csv, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-132"
A1 = {(r["geo"], r["frequenc"]): float(r["value"]) for r in csv.DictReader(open(D / "eurostat_ilc_atst01_2024.csv"))}
FL = {(r["geo"], r["frequenc"]): r["flag"] for r in csv.DictReader(open(D / "eurostat_ilc_atst01_2024.csv"))}
A2 = {(r["geo"], r["reason"], r["frequenc"]): float(r["value"])
      for r in csv.DictReader(open(D / "eurostat_ilc_atst02_2024_MT_EU.csv"))}
MS = ["BE", "BG", "CZ", "DK", "DE", "EE", "IE", "EL", "ES", "FR", "HR", "IT", "CY", "LV", "LT", "LU", "HU", "MT", "NL",
      "AT", "PL", "PT", "RO", "SI", "SK", "FI", "SE"]
assert len(MS) == 27 and all((g, "NVR") in A1 for g in MS)
rows = []


def add(check, value, unit, source, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": source, "note": note})


mt, eu = A1[("MT", "NVR")], A1[("EU27_2020", "NVR")]
S1, S2 = "Eurostat ilc_atst01", "Eurostat ilc_atst02"
add("Malta: persons 16+ never using public transport, 2024", mt, "%", S1,
    "Commission wrote 58%; 58.6 rounds to 59. Eurostat flags on the value: " + (FL[("MT", "NVR")] or "none"))
add("EU-27: persons 16+ never using public transport, 2024", eu, "%", S1, "Commission wrote 50.6%; Eurostat news item: 50.6%")
add("Malta minus EU-27", round(mt - eu, 1), "percentage points", S1, "positive = Malta above the EU average")
add("Malta / EU-27", round(mt / eu, 2), "ratio", S1)
add("Is Malta below the EU-27 average?", "no" if mt > eu else "yes", "", S1, "the Commission's sentence says 'below'")
rank = sorted(MS, key=lambda g: -A1[(g, "NVR")])
above = sum(A1[(g, "NVR")] > mt for g in MS)
tied = [g for g in MS if g != "MT" and A1[(g, "NVR")] == mt]
add("Member States with a higher never-use share than Malta", above, "of 26", S1,
    "tied with Malta: " + (", ".join(tied) or "none"))
add("Rank of Malta (1 = highest never-use share)", f"{above + 1} (tied with {', '.join(tied)})" if tied else above + 1,
    "of 27", S1, "")
add("Median Member State never-use share", sorted(A1[(g, 'NVR')] for g in MS)[13], "%", S1)
add("Member States above the EU-27 aggregate", sum(A1[(g, "NVR")] > eu for g in MS), "of 27", S1,
    "the aggregate is population-weighted")
for f, lab in (("DAY", "every day"), ("WEEK", "every week"), ("MTH", "every month"), ("LT1M", "less than once a month")):
    add(f"Malta vs EU-27: uses public transport {lab}", f"{A1[('MT', f)]} vs {A1[('EU27_2020', f)]}", "%", S1)
tm = round(sum(A1[("MT", f)] for f in ("DAY", "WEEK", "MTH", "LT1M", "NVR")), 1)
te = round(sum(A1[("EU27_2020", f)] for f in ("DAY", "WEEK", "MTH", "LT1M", "NVR")), 1)
add("Frequency categories sum to 100 (Malta; EU-27)", f"{tm}; {te}", "%", S1, "consistency check")
for rc, lab in (("FIN", "financial reasons"), ("SERV_NAVL", "service not available"), ("COM_LG", "long commute"),
                ("SKD", "schedule"), ("OTH", "other reason")):
    add(f"Never-users: reason '{lab}', Malta vs EU-27", f"{A2[('MT', rc, 'NVR')]} vs {A2[('EU27_2020', rc, 'NVR')]}", "%",
        S2, "share of never-users giving this reason (Eurostat's denominator: see report)")
add("Rounding check: 58.6 rounded to whole %", round(mt), "%", "calculation", "Commission's 58% does not match a whole-number rounding of 58.6")
with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["check", "value", "unit", "source", "note"])
    w.writeheader()
    w.writerows(rows)
for r in rows:
    print(r["check"], "=", r["value"], r["unit"])
