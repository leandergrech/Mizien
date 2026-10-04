#!/usr/bin/env python3
"""CC-018: test 'the IMF's assessment confirms what the MDA has been saying' with formulas, not by eye.

Reads data/cc-018/ and data/cc-013/eurostat_housing.csv; writes data/cc-018/checks.csv.
"""
import csv, pathlib
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-018"
P = defaultdict(dict)
for r in csv.DictReader(open(D / "eurostat_tipsho60.csv")):
    P[(r["unit"], r["geo"])][int(r["year"])] = float(r["value"])
E = defaultdict(dict)
for r in csv.DictReader(open(ROOT / "data" / "cc-013" / "eurostat_housing.csv")):
    if r["dataset"] != "#":
        E[(r["dataset"], r["geo"])][int(r["year"])] = float(r["value"])
I = {r["item"]: r["value"] for r in csv.DictReader(open(D / "imf_extracts.csv"))}
rows = []


def add(check, value, unit, source, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": source, "note": note})


for geo, lab in (("MT", "Malta"), ("EU27_2020", "EU-27")):
    i15, lt = P[("PTIR_I15", geo)], P[("PTIR_LT_AVG", geo)]
    last = max(i15)
    add(f"{lab}: price-to-income ratio, 2015 -> {last}", round(i15[last] - 100, 1), "% change", "Eurostat tipsho60")
    add(f"{lab}: price-to-income ratio vs long-term average, {last}", lt[last], "index (100 = average)",
        "Eurostat tipsho60")
    yrs = [y for y in range(2020, last + 1) if y in i15]
    add(f"{lab}: years 2020-{last} with a rising ratio", sum(i15[y] > i15[y - 1] for y in yrs), f"of {len(yrs)}",
        "Eurostat tipsho60")
mt = P[("PTIR_I15", "MT")]
add("Malta: peak of price-to-income ratio since 2010", max((v, y) for y, v in mt.items() if y >= 2010)[1], "year",
    "Eurostat tipsho60")
add("Banks: real estate and construction share of private loans",
    f"{I['Real estate and construction share of private loans a decade earlier']} -> "
    f"{I['Real estate and construction share of private loans mid-2025']}", "%", "IMF CR 26/29 p.19")
add("Banks: residential mortgages share of private lending",
    f"{I['Residential mortgages share a decade earlier']} -> {I['Residential mortgages share of private lending']}", "%",
    "IMF CR 26/29 p.19")
o = E[("ilc_lvho07a", "MT")]
add("Malta: housing-cost overburden 2015 -> 2025", f"{o[2015]} -> {o[2025]}", "% of people", "Eurostat ilc_lvho07a",
    "affordability, not covered by the IMF assessment")
r = E[("tipsho10", "MT")]
add("Malta: real house prices 2015 -> 2025", round(100 * (r[2025] / r[2015] - 1)), "%", "Eurostat tipsho10")
add("MDA-commissioned study: price-to-income 2024 -> 2025", "14.0 -> 14.5", "ratio",
    "MaltaToday, 8 Feb 2026 (second-hand)", "different measure from Eurostat's; method not seen")

with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\r\n")
    w.writeheader()
    w.writerows(rows)
for x in rows:
    print(f"{x['check']:66s} {str(x['value']):>14} {x['unit']:22s} {x['note']}")
