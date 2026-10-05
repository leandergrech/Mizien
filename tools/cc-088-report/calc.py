#!/usr/bin/env python3
"""CC-088: test the NSO World Population Day release (NR 120/2026, 9 July 2026) against Eurostat demo_gind.

Reads data/cc-088/eurostat_demo_gind.csv (fetch.py; Eurostat updated 30 Sep 2026, retrieved 5 Oct 2026) and writes
data/cc-088/checks.csv. NSO's figures are typed in from the release (NSO_* below). Population is on 1 January of the
following year in Eurostat's tables: end 2025 = 1 Jan 2026.

Caveat: Eurostat's Maltese demographic data are supplied by the NSO, so agreement shows consistent transmission and
internal arithmetic, not an independent measurement.
"""
import csv, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-088"
v = {}
for r in csv.DictReader(open(D / "eurostat_demo_gind.csv")):
    v[(r["indic_de"], int(r["year"]))] = float(r["value"])
SRC = "Eurostat demo_gind (updated 30 Sep 2026), retrieved 5 Oct 2026"
NSO = dict(pop_end2025=588254, growth_pct=2.4, net_migration=13906, nat_2024=193, nat_2025=98, nat_change_pct=-49.2,
           mig_change_pct=31.0, births_pct=-0.8, deaths_pct=1.4, deaths_2025=4240)
rows = []


def add(check, nso, calc, unit, ok, note=""):
    rows.append({"check": check, "nso_release": nso, "recomputed": calc, "unit": unit, "reproduces": ok, "source": SRC, "note": note})


pop25, pop26 = v[("JAN", 2025)], v[("JAN", 2026)]
g = 100 * (pop26 / pop25 - 1)
add("Population end 2025 (1 Jan 2026)", NSO["pop_end2025"], int(pop26), "people", pop26 == NSO["pop_end2025"])
add("Growth over 2025", NSO["growth_pct"], round(g, 2), "%", round(g, 1) == NSO["growth_pct"], f"{pop25:,.0f} -> {pop26:,.0f}")
mig25, mig24 = v[("CNMIGRAT", 2025)], v[("CNMIGRAT", 2024)]
add("Net migration 2025", NSO["net_migration"], int(mig25), "people", mig25 == NSO["net_migration"])
add("Net migration, change on 2024", NSO["mig_change_pct"], round(100 * (mig25 / mig24 - 1), 2), "%",
    round(100 * (mig25 / mig24 - 1), 1) == NSO["mig_change_pct"], f"2024: {mig24:,.0f}")
n25, n24 = v[("NATGROW", 2025)], v[("NATGROW", 2024)]
add("Natural increase 2024 and 2025", f"{NSO['nat_2024']} and {NSO['nat_2025']}", f"{int(n24)} and {int(n25)}", "people",
    (n24, n25) == (NSO["nat_2024"], NSO["nat_2025"]))
add("Natural increase, change", NSO["nat_change_pct"], round(100 * (n25 / n24 - 1), 2), "%", round(100 * (n25 / n24 - 1), 1) == NSO["nat_change_pct"])
b25, b24, d25, d24 = v[("LBIRTH", 2025)], v[("LBIRTH", 2024)], v[("DEATH", 2025)], v[("DEATH", 2024)]
add("Live births, change", NSO["births_pct"], round(100 * (b25 / b24 - 1), 2), "%", round(100 * (b25 / b24 - 1), 1) == NSO["births_pct"], f"{b24:,.0f} -> {b25:,.0f}")
add("Deaths, change", NSO["deaths_pct"], round(100 * (d25 / d24 - 1), 2), "%", round(100 * (d25 / d24 - 1), 1) == NSO["deaths_pct"], f"{d24:,.0f} -> {d25:,.0f}")
add("Deaths 2025", NSO["deaths_2025"], int(d25), "people", d25 == NSO["deaths_2025"])
tot = pop26 - pop25
add("Components add up: natural + net migration vs change in stock", int(tot), int(n25 + mig25), "people", tot == n25 + mig25,
    "no statistical adjustment in 2025: Eurostat's net migration equals NSO's")
add("Net migration as share of 2025 growth", "main contributor", round(100 * mig25 / tot, 1), "%", mig25 / tot > 0.5)
for y in (2022, 2023, 2024, 2025):
    add(f"Net migration share of growth, {y}", "", round(100 * v[("CNMIGRAT", y)] / v[("GROW", y)], 1), "%", True)
add("Annual growth 2024 (1 Jan 2024 to 1 Jan 2025)", "", round(100 * (pop25 / v[("JAN", 2024)] - 1), 2), "%", True,
    f"{v[('JAN', 2024)]:,.0f} -> {pop25:,.0f}")
with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for r in rows:
    print(f"{r['check'][:62]:62s} NSO {str(r['nso_release']):>18} calc {str(r['recomputed']):>10} {r['unit']:7s} {r['reproduces']}")
