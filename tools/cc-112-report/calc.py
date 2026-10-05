#!/usr/bin/env python3
"""CC-112: test "Malta's population rose by 25 percent over a decade, largely due to immigration" (IMF Selected
Issues, Feb 2026). The paper gives no years, so every ten-year window to 1 January 2026 is tested.

Reads data/cc-112/eurostat_demo_gind.csv (fetch.py; Eurostat demo_gind, updated 30 Sep 2026, retrieved 5 Oct 2026)
and writes data/cc-112/checks.csv. Population is on 1 January; natural change and net migration (including the
statistical adjustment, CNMIGRAT) are for the calendar year, so the change from 1 Jan of year a to 1 Jan of year a+10
is the sum of the components over years a .. a+9.
"""
import csv, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-112"
v = {}
for r in csv.DictReader(open(D / "eurostat_demo_gind.csv")):
    v[(r["geo"], r["indic_de"], int(r["year"]))] = float(r["value"])
SRC = "Eurostat demo_gind (updated 30 Sep 2026), retrieved 5 Oct 2026"
rows = []


def add(check, value, unit, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": SRC, "note": note})


P = lambda g, y: v[(g, "JAN", y)]
for a in range(2005, 2017):
    b = a + 10
    nat = sum(v[("MT", "NATGROW", y)] for y in range(a, b))
    mig = sum(v[("MT", "CNMIGRAT", y)] for y in range(a, b))
    ch = P("MT", b) - P("MT", a)
    add(f"Malta: population change 1 Jan {a} to 1 Jan {b}", round(100 * (ch / P("MT", a)), 1), "%",
        f"{P('MT', a):,.0f} -> {P('MT', b):,.0f}; net migration {mig:,.0f} ({100 * mig / (nat + mig):.1f}% of the components), natural change "
        f"{nat:,.0f}; components sum to {nat + mig:,.0f} vs change in stock {ch:,.0f} (the gap reflects census revisions)")
add("EU-27: population change 1 Jan 2015 to 1 Jan 2025", round(100 * (P("EU27_2020", 2025) / P("EU27_2020", 2015) - 1), 1), "%")
latest = max(y for y in range(2005, 2027) if ("MT", "JAN", y) in v)
add("Latest population on 1 January in the dataset", f"{P('MT', latest):,.0f} ({latest})", "people")
win = [a for a in range(2005, 2017) if abs(100 * (P("MT", a + 10) / P("MT", a) - 1) - 25) < 1.5]
add("Ten-year windows within 1.5 points of 25%", ", ".join(f"{a}-{a + 10}" for a in win), "windows")
with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for r in rows:
    print(f"{r['check'][:58]:58s} {r['value']:>12} {r['unit']}  {r['note'][:110]}")
