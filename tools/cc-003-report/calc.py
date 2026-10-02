#!/usr/bin/env python3
"""CC-003: test the per-capita claim and the 2030 projection with formulas, not by eye.

Reads data/cc-003/eurostat_ghg_population.csv (Eurostat env_air_gge and nama_10_pe, retrieved 2 Oct 2026)
and writes data/cc-003/checks.csv. ESR figures are typed from the Commission's Climate Action Progress
Report 2025 staff working document (capr2025_swd_en.pdf), pages cited per row.
"""
import csv, pathlib
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-003"
v = defaultdict(dict)
for r in csv.DictReader(open(D / "eurostat_ghg_population.csv")):
    v[(r["geo"], r["item"])][int(r["year"])] = float(r["value"])

rows = []


def add(check, value, unit, source, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": source, "note": note})


ES = "Eurostat env_air_gge (2026 inventory) and nama_10_pe, retrieved 2 Oct 2026"
for geo, lab in (("MT", "Malta"), ("EU27_2020", "EU-27")):
    pop = v[(geo, "POP_NC")]
    tot = v[(geo, "TOTX4_MEMO")]  # total excl. LULUCF and international bunkers
    for y in (2023, 2024):
        pc0, pc = tot[2005] / pop[2005] * 1000, tot[y] / pop[y] * 1000
        add(f"{lab}: per-capita GHG change 2005-{y}", round(100 * (pc / pc0 - 1), 1), "%", ES,
            f"{pc0:.2f} t -> {pc:.2f} t per person (excl. LULUCF and international transport)")
        add(f"{lab}: absolute GHG change 2005-{y}", round(100 * (tot[y] / tot[2005] - 1), 1), "%", ES,
            f"{tot[2005]:.3f} -> {tot[y]:.3f} Mt CO2e")
    add(f"{lab}: population change 2005-2024", round(100 * (pop[2024] / pop[2005] - 1), 1), "%", ES,
        f"{pop[2005]:.1f} -> {pop[2024]:.1f} thousand")

# Decomposition of Malta's per-capita change into the emissions and population parts (log shares)
import math
pop, tot = v[("MT", "POP_NC")], v[("MT", "TOTX4_MEMO")]
lt, lp = math.log(tot[2024] / tot[2005]), math.log(pop[2024] / pop[2005])
lpc = lt - lp
add("Malta: share of per-capita fall 2005-2024 due to population growth", round(100 * (-lp) / lpc, 0), "%", ES,
    "log decomposition: ln(pc ratio) = ln(emissions ratio) - ln(population ratio)")
add("Malta: per-capita change if population had stayed at 2005 level", round(100 * (tot[2024] / tot[2005] - 1), 1),
    "%", ES, "equals the absolute change")

for item, lab in (("CRF1A1", "energy industries (power)"), ("CRF1A3", "domestic transport"),
                  ("CRF2F", "F-gases (refrigeration, air conditioning)"), ("CRF1A4", "buildings and other combustion"),
                  ("CRF5", "waste"), ("CRF1D1", "international bunkers (memo, outside targets)")):
    s = v[("MT", item)]
    add(f"Malta: {lab} change 2005-2024", round(100 * (s[2024] / s[2005] - 1), 1), "%", ES,
        f"{s[2005]:.3f} -> {s[2024]:.3f} Mt CO2e")

SWD = "European Commission, Climate Action Progress Report 2025, SWD (capr2025_swd_en.pdf)"
add("Malta: ESR target 2030 vs 2005", -19, "%", SWD + " p.115", "Effort Sharing Regulation")
add("Malta: ESR emissions 2024 vs 2005", 41, "%", SWD + " p.115")
add("Malta: ESR projection 2030, existing measures (WEM)", 42, "%", SWD + " p.115", "gap -61 pp")
add("Malta: ESR projection 2030, additional measures (WAM)", 30, "%", SWD + " p.115", "gap -49 pp")
add("Malta: ESR gap WAM, percentage points", 30 - (-19), "pp", "calculated", "projection minus target")
add("Next largest WAM gap among EU-27 (Ireland)", -20, "pp", SWD + " p.115", "Malta -49 pp is the largest in pp terms")
add("Malta: cumulative AEA balance 2030", -2.1, "Mt CO2e", SWD + " p.126", "negative = shortfall before flexibilities")

ren = {(r["geo"], r["item"], r["year"]): float(r["value"]) for r in csv.DictReader(open(D / "eurostat_renewables_share.csv"))}
for item, lab in (("REN", "renewables, gross final energy"), ("REN_ELC", "renewables, electricity")):
    add(f"Malta: {lab} 2024", ren[("MT", item, "2024")], "%", "Eurostat nrg_ind_ren, retrieved 2 Oct 2026",
        f"EU-27: {ren[('EU27_2020', item, '2024')]}%")

with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
for r in rows:
    print(f"{r['check']:70s} {r['value']:>8} {r['unit']}  {r['note']}")
