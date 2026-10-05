#!/usr/bin/env python3
"""CC-110: test the Commission's 2026 Country Report figures on zero-emission new cars in Malta.

Reads data/cc-110/eurostat_road_eqr_carpda.csv and eurostat_road_eqs_carpda.csv (fetch.py; Eurostat, updated 1 Sep
2026, retrieved 5 Oct 2026) and writes data/cc-110/checks.csv. Zero-emission (ZEV) = battery electric (ELC) plus
hydrogen and fuel cell (HYD_FCELL); plug-in hybrids are not zero-emission.
"""
import csv, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-110"
n, s = {}, {}
for r in csv.DictReader(open(D / "eurostat_road_eqr_carpda.csv")):
    n[(r["geo"], r["mot_nrg"], int(r["year"]))] = float(r["value"])
for r in csv.DictReader(open(D / "eurostat_road_eqs_carpda.csv")):
    s[(r["geo"], r["mot_nrg"], int(r["year"]))] = float(r["value"])
SRC = "Eurostat road_eqr_carpda / road_eqs_carpda (updated 1 Sep 2026), retrieved 5 Oct 2026"
rows = []


def add(check, value, unit, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": SRC, "note": note})


def zev(d, g, y):
    return d.get((g, "ELC", y), 0) + d.get((g, "HYD_FCELL", y), 0)


def share(d, g, y):
    return 100 * zev(d, g, y) / d[(g, "TOTAL", y)]


for y in (2022, 2023, 2024, 2025):
    add(f"Malta: new passenger cars registered, {y}", int(n[("MT", "TOTAL", y)]), "cars")
    add(f"Malta: ZEV share of new passenger cars, {y}", round(share(n, "MT", y), 2), "%")
    add(f"EU-27: ZEV share of new passenger cars, {y}", round(share(n, "EU27_2020", y), 2), "%")
add("Malta: change in ZEV share 2023-2024", round(share(n, "MT", 2024) - share(n, "MT", 2023), 2), "percentage points",
    "from unrounded shares; the report's 17.4 comes from its rounded annex values (37.66 - 20.31 = 17.35)")
add("Malta: plug-in hybrid share of new cars, 2024", round(100 * (n.get(("MT", "ELC_PET_PI", 2024), 0) + n.get(("MT", "ELC_DIE_PI", 2024), 0)) / n[("MT", "TOTAL", 2024)], 2), "%", "not counted as ZEV")
geos = [g for g in {k[0] for k in n} if g != "EU27_2020" and (g, "TOTAL", 2024) in n]
rank = sorted(geos, key=lambda g: -share(n, g, 2024))
add("Malta's rank among member states, ZEV share of new cars 2024", f"{rank.index('MT') + 1} of {len(rank)}", "rank",
    "higher: " + ", ".join(f"{g} {share(n, g, 2024):.1f}%" for g in rank[:rank.index('MT')]))
add("Unweighted mean of member states' ZEV shares, 2024", round(sum(share(n, g, 2024) for g in geos) / len(geos), 2), "%",
    "for comparison with the report's 13.6%; the EU-27 aggregate is the weighted figure")
for y in (2023, 2024):
    add(f"Malta: ZEV share of the passenger-car stock, end {y}", round(share(s, "MT", y), 2), "%")
    add(f"EU-27: ZEV share of the passenger-car stock, end {y}", round(share(s, "EU27_2020", y), 2), "%")
add("Malta: net growth of the passenger-car stock in 2024", int(s[("MT", "TOTAL", 2024)] - s[("MT", "TOTAL", 2023)]), "cars",
    f"{(s[('MT', 'TOTAL', 2024)] - s[('MT', 'TOTAL', 2023)]) / 366:.1f} cars a day (2024 is a leap year)")
add("Malta: net growth of ZEVs in the stock in 2024", int(zev(s, "MT", 2024) - zev(s, "MT", 2023)), "cars")
with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for r in rows:
    print(f"{r['check'][:78]:78s} {r['value']:>10} {r['unit']}  {r['note'][:70]}")
