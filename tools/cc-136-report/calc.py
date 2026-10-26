#!/usr/bin/env python3
"""CC-136: test AFP's (6 Jun 2026) statements that Malta is "the most densely populated country in Europe", that
"approvals for new buildings are soaring" and that "the country's population has grown nearly 30 percent over a decade".

Reads data/cc-136/ (fetch.py: World Bank EN.POP.DNST, Eurostat demo_r_d3dens, Eurostat demo_gind; retrieved on the
date in each file) and data/cc-013/pa_approved_dwellings.csv (Planning Authority, Approved Dwelling Units 2007-2025).
Writes data/cc-136/checks.csv."""
import csv, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-136"
rows = []


def add(check, value, unit, source, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": source, "note": note})


# --- A. density -------------------------------------------------------------------------------------------------
WB = "World Bank EN.POP.DNST (people per sq. km of land area), lastupdated 8 Oct 2026, retrieved 26 Oct 2026"
latest = {}
for r in csv.DictReader(open(D / "worldbank_density.csv")):
    if r["iso3"] not in latest or r["year"] > latest[r["iso3"]][0]:
        latest[r["iso3"]] = (r["year"], float(r["people_per_km2_land"]), r["country"])
rank = sorted(latest.items(), key=lambda kv: -kv[1][1])
for i, (k, (y, v, name)) in enumerate(rank[:5], 1):
    add(f"Europe (World Bank list of {len(latest)} states), density rank {i}: {name}", round(v), "people/km2", WB, f"year {y}")
mt = latest["MLT"][1]
add("Monaco density as a multiple of Malta's", round(latest["MCO"][1] / mt, 1), "x", WB, "2024 values")
EU = set("AUT BEL BGR HRV CYP CZE DNK EST FIN FRA DEU GRC HUN IRL ITA LVA LTU LUX MLT NLD POL PRT ROU SVK SVN ESP SWE".split())
eu = sorted(((v[1], v[2]) for k, v in latest.items() if k in EU), reverse=True)
add("EU Member States in the World Bank data", len(eu), "states", WB)
add("Malta density as a multiple of the next EU state (Netherlands)", round(eu[0][0] / eu[1][0], 1), "x", WB, f"{eu[0][1]} vs {eu[1][1]}")
ES = "Eurostat demo_r_d3dens (updated 25 Feb 2026), retrieved 26 Oct 2026"
es = {(r["geo"], r["year"]): float(r["value_per_km2"]) for r in csv.DictReader(open(D / "eurostat_demo_r_d3dens.csv"))}
yr = max(y for g, y in es if g == "MT")
nat = sorted(((v, g) for (g, y), v in es.items() if y == yr and g != "EU27_2020"), reverse=True)
add(f"Eurostat {yr}: Malta density", es[("MT", yr)], "people/km2", ES, "total area basis; flag none")
add(f"Eurostat {yr}: next densest country", f"{nat[1][1]} {nat[1][0]}", "people/km2", ES, "countries in the dataset: EU, EFTA, candidates")
add(f"Eurostat {yr}: EU-27 density", es[("EU27_2020", yr)], "people/km2", ES, "Eurostat flag ep (provisional)")
add("Eurostat: Malta rank among countries in the dataset", 1 + sum(1 for v, g in nat if v > es[("MT", yr)]), "rank", ES)

# --- B. approvals -----------------------------------------------------------------------------------------------
PA = "Planning Authority, Approved Dwelling Units 2007-2025 (transcribed in data/cc-013/pa_approved_dwellings.csv, read 3 Oct 2026)"
pa = {int(r["year"]): int(r["approved_units_total"]) for r in csv.DictReader(open(ROOT / "data/cc-013/pa_approved_dwellings.csv"))}
add("Approved dwelling units 2025", pa[2025], "units", PA)
add("Approved dwelling units 2024", pa[2024], "units", PA)
add("Change 2024 to 2025", round(100 * (pa[2025] / pa[2024] - 1), 1), "%", PA)
add("Approved dwelling units 2013 (low)", pa[2013], "units", PA)
add("Approved dwelling units 2018 (peak before 2025)", pa[2018], "units", PA)
add("Approved 2025 as a multiple of 2013", round(pa[2025] / pa[2013], 1), "x", PA)
add("2025 vs 2018 peak", round(100 * (pa[2025] / pa[2018] - 1), 1), "%", PA, "2025 is below the 2018 and 2019 peaks")
add("Years in 2007-2025 with more approved units than 2025", ", ".join(str(y) for y in pa if pa[y] > pa[2025]) or "none", "years", PA)
add("Change 2022 to 2025 (three years)", round(100 * (pa[2025] / pa[2022] - 1), 1), "%", PA)
add("Approved units 2015-2025 (eleven years) per year", round(sum(pa[y] for y in range(2015, 2026)) / 11), "units/yr", PA)
add("Approved units 2007-2014 per year", round(sum(pa[y] for y in range(2007, 2015)) / 8), "units/yr", PA)

# --- C. population ----------------------------------------------------------------------------------------------
DG = "Eurostat demo_gind (updated 30 Sep 2026), retrieved 26 Oct 2026"
pop = {(r["geo"], int(r["year"])): float(r["population_1_jan"]) for r in csv.DictReader(open(D / "eurostat_demo_gind_jan.csv"))}
for a in range(2012, 2017):
    b = a + 10
    add(f"Malta: population change 1 Jan {a} to 1 Jan {b}", round(100 * (pop[("MT", b)] / pop[("MT", a)] - 1), 1), "%", DG,
        f"{pop[('MT', a)]:,.0f} -> {pop[('MT', b)]:,.0f}")
add("EU-27: population change 1 Jan 2015 to 1 Jan 2025", round(100 * (pop[("EU27_2020", 2025)] / pop[("EU27_2020", 2015)] - 1), 1), "%", DG)
add("Ten-year windows 2012-2022 .. 2016-2026 with growth below 30%", ", ".join(
    f"{a}-{a+10}" for a in range(2012, 2017) if 100 * (pop[("MT", a + 10)] / pop[("MT", a)] - 1) < 30) or "none", "windows", DG)

with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for r in rows:
    print(f"{r['check'][:75]:75s} {str(r['value']):>14} {r['unit']}  {r['note'][:60]}")
