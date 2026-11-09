#!/usr/bin/env python3
"""CC-159: test the IMF staff's "population density fifteen times greater than the EU average" (Country Report 26/29).
Reads data/cc-159 (fetch.py). Writes data/cc-159/checks.csv. Every ratio is Malta / comparator on a stated basis."""
import csv, pathlib, statistics as st
ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-159"
rows = []
def add(check, value, unit, source, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": source, "note": note})

ES = "Eurostat demo_r_d3dens (updated 25 Feb 2026), retrieved 9 Nov 2026"
dens = {(r["geo"], int(r["year"])): float(r["value_per_km2"]) for r in csv.DictReader(open(D / "eurostat_demo_r_d3dens.csv"))}
flag = {(r["geo"], int(r["year"])): r["flag"] for r in csv.DictReader(open(D / "eurostat_demo_r_d3dens.csv"))}
yrs = sorted({y for g, y in dens if g == "MT"})
for y in yrs:
    add(f"Eurostat {y}: Malta / EU-27 aggregate density", round(dens[("MT", y)] / dens[("EU27_2020", y)], 1), "x", ES,
        f"{dens[('MT', y)]} vs {dens[('EU27_2020', y)]} per km2 (EU flag '{flag[('EU27_2020', y)]}')")
Y = max(yrs)
states = {g: dens[(g, Y)] for g in {g for g, y in dens if y == Y} if g not in ("EU27_2020", "MT")}
add(f"Eurostat {Y}: median of the 26 other states' densities", round(st.median(states.values()), 1), "per km2", ES)
add(f"Eurostat {Y}: Malta / median other state", round(dens[("MT", Y)] / st.median(states.values()), 1), "x", ES)
add(f"Eurostat {Y}: Malta / unweighted mean of the 26 other states", round(dens[("MT", Y)] / st.mean(states.values()), 1), "x", ES,
    f"mean {st.mean(states.values()):.1f}")
add(f"Eurostat {Y}: Malta / EU-27 excluding Malta (population-weighted)", None, "x", ES, "see below")
# EU excluding Malta, from population and area
AR = "Eurostat reg_area3 (updated 22 Jan 2026), retrieved 9 Nov 2026"
area = {(r["geo"], int(r["year"])): float(r["area_km2"]) for r in csv.DictReader(open(D / "eurostat_reg_area3.csv"))}
DG = "Eurostat demo_gind (updated 27 Oct 2026), retrieved 9 Nov 2026"
pop = {(r["geo"], int(r["year"])): float(r["population_1_jan"]) for r in csv.DictReader(open(D / "eurostat_demo_gind_jan.csv"))}
rows.pop()
for y in (2024, 2025):
    ex = (pop[("EU27_2020", y)] - pop[("MT", y)]) / (area[("EU27_2020", y)] - area[("MT", y)])
    add(f"EU-27 excluding Malta, 1 Jan {y}: population / total area", round(ex, 1), "per km2", f"{DG}; {AR}")
    add(f"Malta 1 Jan {y} / EU-27 excluding Malta", round((pop[("MT", y)] / area[("MT", y)]) / ex, 1), "x", f"{DG}; {AR}",
        f"Malta {pop[('MT', y)]:,.0f} / {area[('MT', y)]:.0f} km2 = {pop[('MT', y)] / area[('MT', y)]:.0f}")
# the IMF's own populations
for y, imf in ((2024, 553000), (2025, 563000), (2026, 573000), (2027, 584000)):
    pass
for y, imf in ((2022, 520000), (2023, 542000)):
    add(f"IMF Table 1 {y} ({imf:,}) vs Eurostat 1 Jan {y}", round(100 * (imf / pop[("MT", y)] - 1), 1), "%", DG, f"Eurostat {pop[('MT', y)]:,.0f}")
add("IMF Table 1 2026 (573,000) vs Eurostat 1 Jan 2026", round(100 * (573000 / pop[("MT", 2026)] - 1), 1), "%", DG, f"Eurostat {pop[('MT', 2026)]:,.0f}")
for y, imf in ((2024, 553000), (2025, 563000)):
    for yy in (y,):
        add(f"IMF table {y} ({imf:,}) vs Eurostat 1 Jan {yy}", round(100 * (imf / pop[("MT", yy)] - 1), 1), "%", DG,
            f"Eurostat {pop[('MT', yy)]:,.0f}")
add("Density ratio if Malta's population is the IMF's 2025 value (563,000), EU-27 2024 aggregate", round(563000 / 316 / dens[("EU27_2020", 2024)], 1), "x",
    f"IMF Country Report 26/29 population table; {AR}; {ES}", "Eurostat area 316 km2")
# World Bank basis (land area)
WB = "World Bank EN.POP.DNST (land area), lastupdated 8 Oct 2026, retrieved 9 Nov 2026"
wb = {}
for r in csv.DictReader(open(D / "worldbank_density_eu27.csv")):
    wb.setdefault(r["iso3"], {})[int(r["year"])] = float(r["people_per_km2_land"])
w24 = {k: v[2024] for k, v in wb.items() if 2024 in v}
oth = [v for k, v in w24.items() if k != "MLT"]
add("World Bank 2024: Malta density (land area)", round(w24["MLT"]), "per km2", WB, f"{len(w24)} EU states with data")
add("World Bank 2024: Malta / median other EU state", round(w24["MLT"] / st.median(oth), 1), "x", WB, f"median {st.median(oth):.0f}")
add("World Bank 2024: Malta / unweighted mean of other EU states", round(w24["MLT"] / st.mean(oth), 1), "x", WB, f"mean {st.mean(oth):.0f}")
add("World Bank 2024: Malta / next densest EU state (Netherlands)", round(w24["MLT"] / w24["NLD"], 1), "x", WB, f"NL {w24['NLD']:.0f}")
# what EU average gives exactly fifteen
add("EU density that would give a ratio of exactly 15 (Malta 1,817.4)", round(1817.4 / 15, 1), "per km2", ES, "versus Eurostat EU-27 109.7")
with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for r in rows:
    print(f"{r['check'][:80]:80s} {str(r['value']):>9} {r['unit']:8s} {r['note'][:70]}")
