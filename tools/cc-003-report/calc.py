#!/usr/bin/env python3
"""CC-003: test the per-capita claim and the 2030 projection with formulas, not by eye.

Reads data/cc-003/eurostat_ghg_population.csv (Eurostat env_air_gge and nama_10_pe, retrieved 2 Oct 2026)
and writes data/cc-003/checks.csv. ESR figures are typed from the Commission's Climate Action Progress
Report 2025 staff working document (capr2025_swd_en.pdf), printed page numbers cited per row.
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

for item, lab in (("CRF1A1", "energy industries (power)"), ("CRF1A3", "domestic transport")):
    s = v[("EU27_2020", item)]
    add(f"EU-27: {lab} change 2005-2024", round(100 * (s[2024] / s[2005] - 1), 1), "%", ES,
        f"{s[2005]:.3f} -> {s[2024]:.3f} Mt CO2e")

# Page numbers are the printed page numbers of the SWD (the PDF page number is one higher).
SWD = "European Commission, Climate Action Progress Report 2025, SWD (capr2025_swd_en.pdf)"
add("Malta: industrial emissions change 2005-2023", 293, "%", SWD + " p.44",
    "mainly refrigeration and air-conditioning gases")
add("EU-27: industrial emissions change 2005-2023", -36, "%", SWD + " p.44", "total industrial emissions")
add("Malta: buildings emissions change since 2005", 12, "%", SWD + " p.59",
    "all other Member States fell except Romania (+6%)")
add("Malta: ESR target 2030 vs 2005", -19, "%", SWD + " p.114 (Table 25)", "Effort Sharing Regulation")
add("Malta: ESR emissions 2024 vs 2005", 41, "%", SWD + " p.114 (Table 25)")
add("Malta: ESR projection 2030, existing measures (WEM)", 42, "%", SWD + " p.114 (Table 25)", "gap -61 pp")
add("Malta: ESR projection 2030, additional measures (WAM)", 30, "%", SWD + " p.114 (Table 25)", "gap -49 pp")
add("Malta: ESR gap WAM, percentage points", 30 - (-19), "pp", "calculated", "projection minus target")
add("Next largest WAM gap among EU-27 (Ireland)", -20, "pp", SWD + " p.113 (Table 25)",
    "Malta -49 pp is the largest in pp terms; Ireland WEM gap -33 pp")
add("EU-27: ESR target 2030 vs 2005", -40, "%", SWD + " p.115 (Table 25)")
add("EU-27: ESR emissions 2024 vs 2005", -20, "%", SWD + " p.115 (Table 25)")
add("EU-27: ESR projection 2030, existing measures (WEM)", -31, "%", SWD + " p.115 (Table 25)", "gap -8 pp")
add("EU-27: ESR projection 2030, additional measures (WAM)", -38, "%", SWD + " p.115 (Table 25)", "gap -2 pp")
add("Malta: cumulative AEA balance 2030", -2.1, "Mt CO2e", SWD + " p.125", "negative = shortfall before flexibilities")
add("Malta: ESR distance to target 2030", -0.5, "Mt CO2e", SWD + " p.125 (Table 26)", "baseline 2005: 1.0 Mt")
add("Germany: ESR distance to target 2030", -64.0, "Mt CO2e", SWD + " p.118 (Table 26)",
    "baseline 2005: 484.7 Mt; gap -14 pp (WEM) / -13 pp (WAM): smaller than Malta's in pp, larger in tonnes")

# ---- v1.2: Malta's rank among the EU-27 on the per-person and the total cut (eurostat_ghg_pop_eu27.csv, fetch_eu27.py)
EU = "AT BE BG CY CZ DE DK EE EL ES FI FR HR HU IE IT LT LU LV MT NL PL PT RO SE SI SK".split()
g27 = defaultdict(dict)
fl27 = {}
for r in csv.DictReader(open(D / "eurostat_ghg_pop_eu27.csv")):
    g27[(r["geo"], r["dataset"])][int(r["year"])] = float(r["value"])
    if r["flag"]:
        fl27[(r["geo"], r["dataset"], int(r["year"]))] = r["flag"]
ES27 = "Eurostat env_air_gge (TOTX4_MEMO) and nama_10_pe (POP_NC), all EU-27, retrieved 5 Oct 2026"
cut = {}
for g in EU:
    e, p = g27[(g, "env_air_gge")], g27[(g, "nama_10_pe")]
    cut[g] = (100 * (e[2024] / e[2005] - 1), 100 * ((e[2024] / p[2024]) / (e[2005] / p[2005]) - 1),
              100 * (p[2024] / p[2005] - 1))
rank_pc = sorted(EU, key=lambda g: cut[g][1])
rank_tot = sorted(EU, key=lambda g: cut[g][0])
rank_pop = sorted(EU, key=lambda g: -cut[g][2])
pflags = sorted(g for g in EU if (g, "nama_10_pe", 2024) in fl27)
add("Malta: EU-27 rank on per-person GHG cut 2005-2024 (1 = largest cut)", rank_pc.index("MT") + 1, "of 27", ES27,
    f"Malta {cut['MT'][1]:.1f}%; ahead: " + ", ".join(f"{g} {cut[g][1]:.1f}%" for g in rank_pc[:2]))
add("Malta: EU-27 rank on total GHG cut 2005-2024 (1 = largest cut)", rank_tot.index("MT") + 1, "of 27", ES27,
    f"Malta {cut['MT'][0]:.1f}%; largest: " + ", ".join(f"{g} {cut[g][0]:.1f}%" for g in rank_tot[:3]))
add("Malta: EU-27 rank on population growth 2005-2024", rank_pop.index("MT") + 1, "of 27", ES27,
    f"Malta +{cut['MT'][2]:.1f}%; first: {rank_pop[0]} +{cut[rank_pop[0]][2]:.1f}%; "
    f"2024 population provisional (flag p) for {', '.join(pflags)}")
drop = sorted(EU, key=lambda g: -(rank_tot.index(g) - rank_pc.index(g)))
add("Largest falls in EU-27 rank from per-person cut to total cut, 2005-2024", ", ".join(
    f"{g} {rank_tot.index(g) - rank_pc.index(g)}" for g in drop[:3]), "places", ES27)
for g in ("LU", "IE", "CY"):
    add(f"{g}: per-person and total GHG change 2005-2024, rank", f"{cut[g][1]:.1f} / {cut[g][0]:.1f}", "%", ES27,
        f"ranks {rank_pc.index(g) + 1} and {rank_tot.index(g) + 1} of 27; population +{cut[g][2]:.1f}%")

# ---- v1.2: Malta's effort-sharing path, Commission SWD Table 25 (p. 114) and Table 26 (p. 125)
esr = defaultdict(dict)
for r in csv.DictReader(open(D / "capr2025_esr_malta.csv")):
    if r["table"].startswith("#") or not r["value"]:
        continue
    esr[r["series"]][r["year"]] = float(r["value"])
tgt, emi = esr["Malta ESR target vs 2005"], esr["Malta ESR emissions vs 2005"]
for y in ("2021", "2022", "2023", "2024"):
    dist = esr["Malta distance to target (pp)"][y]  # the Commission's own (rounded) distance, not emissions minus target
    add(f"Malta: ESR emissions vs yearly limit {y}", f"{emi[y]:+.0f} vs {tgt[y]:+.0f}", "% vs 2005",
        SWD + " p.114 (Table 25)", f"{abs(dist):.0f} points {'over' if dist < 0 else 'under'} the limit (Table 25)")
cb = esr["Malta cumulative balance of AEAs"]
add("Malta: cumulative AEA balance 2021 -> 2024", f"{cb['2021']} -> {cb['2024']}", "Mt CO2e", SWD + " p.125 (Table 26)",
    "2021 surplus (allocation 2.1 Mt vs emissions 1.3 Mt) carried forward; cancellations and transfers not counted")
add("Malta: cumulative AEA balance 2025 (projected)", cb["2025"], "Mt CO2e", SWD + " p.125 (Table 26)",
    "first compliance check in 2027 for 2021-2025 (p.111); ETS flexibility 0.5 Mt for 2021-2030")

# ---- v1.2: effort-sharing emissions per person, proxy = national total (TOTX4_MEMO) minus power generation (CRF1A1).
# A proxy, not the official ESR series: it is tested against the Commission's 2005 base (Table 26) and its
# 2021-2024 changes (Table 25) below, and reproduces them within about 3 points.
prox = {y: tot[y] - v[("MT", "CRF1A1")][y] for y in (2005, 2021, 2022, 2023, 2024)}
EP = "Eurostat env_air_gge (TOTX4_MEMO minus CRF1A1) and nama_10_pe, retrieved 2 Oct 2026; proxy for ESR scope"
add("Malta: ESR proxy 2005 (total minus power generation)", round(prox[2005], 3), "Mt CO2e", EP,
    f"Commission 2005 ESR base: {esr['Malta baseline emissions']['2005']} Mt (Table 26, rounded)")
for y in (2021, 2022, 2023, 2024):
    add(f"Malta: ESR proxy change 2005-{y}", round(100 * (prox[y] / prox[2005] - 1), 1), "%", EP,
        f"Commission Table 25: {emi[str(y)]:+.0f}%")
for y in (2005, 2024):
    add(f"Malta: ESR proxy per person {y}", f"{prox[y] / pop[y] * 1000:.2f}", "t CO2e", EP,
        f"{prox[y]:.3f} Mt / {pop[y]:.1f} thousand people")
add("EU-27: ESR emissions per person, change 2005-2024", round(100 * ((1 + (-20) / 100) / (v[("EU27_2020", "POP_NC")][2024]
    / v[("EU27_2020", "POP_NC")][2005]) - 1), 0), "%", SWD + " p.115 (Table 25) and Eurostat nama_10_pe",
    "Commission EU-27 ESR -20% divided by population growth")

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
