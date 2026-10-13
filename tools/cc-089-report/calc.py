#!/usr/bin/env python3
"""CC-089: test the figures in PwC Malta's press release (posted by the Malta Chamber, 22 Jul 2026) with formulas.

Reads data/cc-089/ (Eurostat and World Bank, retrieved by fetch.py) and writes data/cc-089/checks.csv.
PwC figures are typed in below exactly as printed in the release (paragraph numbers in the comments).
"""
import csv, pathlib
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-089"
EU = "AT BE BG CY CZ DE DK EE EL ES FI FR HR HU IE IT LT LU LV MT NL PL PT RO SE SI SK".split()

# PwC release, as printed (Malta Chamber copy, 22 Jul 2026)
PW = dict(pop_end2025=588254, rise=14000, rise_pct=2.4,           # para 1
          pop2030=636000, density_now=1862, density_2030=2013,     # paras 2, 3
          beds100k=397, beds_eu=511, rank=17, add_keep=329, add_keep_pct=15, add_par=1054, add_par_pct=48,  # para 4
          local_mwh=2138, import_mwh=970, import_2030=1304, import_pct=25)                                 # para 5


def load(name):
    return list(csv.DictReader(open(D / f"{name}.csv")))


flag = {}
POP = defaultdict(dict)
for r in load("eurostat_pop"):
    POP[r["geo"]][int(r["time"])] = float(r["value"])
    flag[("pop", r["geo"], int(r["time"]))] = r["flag"]
PROJ = defaultdict(dict)
for r in load("eurostat_proj"):
    PROJ[r["projection"]][int(r["time"])] = float(r["value"])
BEDS = defaultdict(dict)
for r in load("eurostat_beds_100k"):
    BEDS[r["geo"]][int(r["time"])] = float(r["value"])
BEDNR = {int(r["time"]): float(r["value"]) for r in load("eurostat_beds_nr")}
BEDFLAG = {int(r["time"]): r["flag"] for r in load("eurostat_beds_nr")}
EL = defaultdict(dict)
for r in load("eurostat_elec"):
    EL[r["nrg_bal"]][int(r["time"])] = float(r["value"])
ELF = {(r["nrg_bal"], int(r["time"])): r["flag"] for r in load("eurostat_elec")}
AREA = {int(r["time"]): float(r["value"]) for r in load("eurostat_area")}
MED = {(r["geo"], int(r["time"])): float(r["value"]) for r in load("eurostat_medage")}
WB = [r for r in load("worldbank_density_2023") if r["people_per_km2_land"]]

rows = []


def add(check, value, unit, source, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": source, "note": note})


rank = lambda d, k, rev=True: sorted(d, key=lambda g: -d[g] if rev else d[g]).index(k) + 1

# ---- A. population ----------------------------------------------------------------------------------------------
mt = POP["MT"]
ch = mt[2026] - mt[2025]
add("Population 1 Jan 2026 (end-2025)", int(mt[2026]), "persons", "Eurostat demo_gind", f"PwC: {PW['pop_end2025']}; equal")
add("Change in 2025", int(ch), "persons", "Eurostat demo_gind", f"PwC: 'approximately {PW['rise']}'")
add("Change in 2025", round(100 * ch / mt[2025], 2), "%", "Eurostat demo_gind", f"PwC: {PW['rise_pct']}%")
g26 = {g: 100 * (POP[g][2026] / POP[g][2025] - 1) for g in EU}
add("Population growth 2025, Malta", round(g26["MT"], 2), "%", "Eurostat demo_gind",
    f"rank {rank(g26, 'MT')} of 27; next {sorted(g26, key=lambda g: -g26[g])[1]} {sorted(g26.values())[-2]:.2f}%")
add("Population growth 2025, EU-27", round(100 * (POP["EU27_2020"][2026] / POP["EU27_2020"][2025] - 1), 2), "%",
    "Eurostat demo_gind", "EU-27 values flagged provisional (ep)")
g1526 = {g: 100 * (POP[g][2026] / POP[g][2015] - 1) for g in EU}
add("Population growth 1 Jan 2015 to 1 Jan 2026, Malta", round(g1526["MT"], 1), "%", "Eurostat demo_gind",
    f"rank {rank(g1526, 'MT')} of 27; next {sorted(g1526, key=lambda g: -g1526[g])[1]} "
    f"{sorted(g1526.values())[-2]:.1f}%")
add("Population growth 1 Jan 2015 to 1 Jan 2026, EU-27", round(100 * (POP["EU27_2020"][2026] / POP["EU27_2020"][2015] - 1), 1),
    "%", "Eurostat demo_gind")

# ---- B. projection ----------------------------------------------------------------------------------------------
b = PROJ["BSL"]
for v in ("BSL", "LMIGR", "HMIGR", "NMIGR"):
    add(f"EUROPOP2025 {v}: 1 Jan 2030", int(PROJ[v][2030]), "persons", "Eurostat proj_25np",
        f"1 Jan 2031: {int(PROJ[v][2031])}")
add("EUROPOP2025 baseline: 1 Jan 2026 projected vs actual", f"{int(b[2026])} vs {int(mt[2026])}", "persons",
    "Eurostat proj_25np, demo_gind", f"actual is {100 * (mt[2026] / b[2026] - 1):+.2f}% above the projection")
for y in (2030, 2031):
    need = 100 * (PW["pop2030"] / mt[2026] - 1)
    base = 100 * (b[y] / b[2026] - 1)
    rebased = mt[2026] * b[y] / b[2026]
    add(f"Growth from 1 Jan 2026 to 1 Jan {y}: PwC {PW['pop2030']} vs EUROPOP2025 baseline",
        f"{need:.1f}% vs {base:.1f}%", "%", "Eurostat; PwC release",
        f"baseline rebased on actual 2026 = {rebased:,.0f}; PwC is {100 * (PW['pop2030'] / rebased - 1):+.1f}% against it")
hm = mt[2026] * PROJ["HMIGR"][2030] / PROJ["HMIGR"][2026]
add("EUROPOP2025 higher-migration variant rebased on actual 1 Jan 2026, for 1 Jan 2030", round(hm), "persons",
    "Eurostat proj_25np", "PwC's 636,000 lies between the rebased baseline and this variant")
add("Annual growth needed for PwC's 636,000 by 1 Jan 2030 / 1 Jan 2031", f"{100 * ((PW['pop2030'] / mt[2026]) ** (1 / 4) - 1):.2f} / {100 * ((PW['pop2030'] / mt[2026]) ** (1 / 5) - 1):.2f}",
    "% a year", "calculation", "compare 2.44% in 2025")

# ---- C. density -------------------------------------------------------------------------------------------------
a = AREA[max(AREA)]
add("Land area, Malta", a, "km2", "Eurostat demo_r_d3area", f"latest year in the series is {max(AREA)} (316.0 km2 in 2008-2014, as PwC; 315.6 before)")
add("Density, end-2025 (PwC 1,862)", round(PW["pop_end2025"] / a), "per km2", "calculation", "588,254 / area")
add("Density, 2030 (PwC 2,013)", round(PW["pop2030"] / a), "per km2", "calculation", "636,000 / area")
add("Area implied by PwC's 1,862 and 2,013", f"{PW['pop_end2025'] / PW['density_now']:.1f} / {PW['pop2030'] / PW['density_2030']:.1f}",
    "km2", "calculation", "both round to 316 km2")
wb = sorted(WB, key=lambda r: -float(r["people_per_km2_land"]))
mi = [r["iso3"] for r in wb].index("MLT") + 1
add("World Bank density 2023, Malta", round(float(wb[mi - 1]["people_per_km2_land"])), "per km2",
    "World Bank EN.POP.DNST", f"rank {mi} of {len(wb)} entries (incl. territories)")
add("World Bank density 2023, top entries", "; ".join(f"{r['name']} {float(r['people_per_km2_land']):.0f}" for r in wb[:9]),
    "per km2", "World Bank EN.POP.DNST", "Macao, Hong Kong and Gibraltar are not sovereign states (general context)")

# ---- D. hospital beds -------------------------------------------------------------------------------------------
for y in (2022, 2023, 2024):
    v = {g: BEDS[g][y] for g in EU if y in BEDS[g]}
    add(f"Hospital beds per 100,000, {y}: Malta", v["MT"], "per 100k", "Eurostat hlth_rs_bds1",
        f"rank {rank(v, 'MT')} of {len(v)}; EU-27 {BEDS['EU27_2020'][y]:.1f}" + ("; flag b (break) for Malta" if y == 2023 else ""))
n24, r24, e24 = BEDNR[2024], BEDS["MT"][2024], BEDS["EU27_2020"][2024]
add("Hospital beds, Malta 2024 (number)", int(n24), "beds", "Eurostat hlth_rs_bds1", f"2023: {int(BEDNR[2023])} (flag b); 2022: {int(BEDNR[2022])}")
P30 = PW["pop2030"]
sc = {
    "Hold Eurostat's own 2024 rate (390.6) at 636,000": P30 * r24 / 1e5,
    "Hold PwC's 397 at 636,000": P30 * PW["beds100k"] / 1e5,
    "Hold 2024 beds per resident of 1 Jan 2026 (588,254)": n24 * P30 / mt[2026],
}
for k, v in sc.items():
    add(f"Beds needed: {k}", round(v), "beds", "calculation", f"+{v - n24:.0f} on {int(n24)} (+{100 * (v / n24 - 1):.1f}%); PwC +{PW['add_keep']} (+{PW['add_keep_pct']}%)")
add("Beds for the EU-27 average (2024: 507.35) at 636,000", round(P30 * e24 / 1e5), "beds", "calculation",
    f"+{P30 * e24 / 1e5 - n24:.0f} (+{100 * (P30 * e24 / 1e5 / n24 - 1):.0f}%)")
add("Beds for PwC's EU average 511 at 636,000", round(P30 * PW["beds_eu"] / 1e5), "beds", "calculation",
    f"+{P30 * PW['beds_eu'] / 1e5 - n24:.0f} (+{100 * (P30 * PW['beds_eu'] / 1e5 / n24 - 1):.0f}%); PwC +{PW['add_par']} (+{PW['add_par_pct']}%)")
add("Population base implied by PwC's +329 beds (15%) at 397 per 100,000", round((P30 * 397 / 1e5 - PW["add_keep"]) / 397 * 1e5),
    "persons", "calculation", "i.e. beds before = 636,000 x 397 / 100,000 - 329; this base is below the release's 588,254")
add("Median age 2025, Malta / EU-27", f"{MED[('MT', 2025)]} / {MED[('EU27_2020', 2025)]}", "years", "Eurostat demo_pjanind",
    "a younger population needs fewer beds per head (context, not a bed target)")

# ---- E. electricity ---------------------------------------------------------------------------------------------
y = 2024
loc, imp, gep, afc, dl = PW["local_mwh"], PW["import_mwh"], EL["GEP"][y], EL["AFC"][y], EL["DL"][y]
add("Electricity 2024: Eurostat gross production vs PwC 'locally generated'", f"{gep:.0f} vs {loc}", "GWh", "Eurostat nrg_cb_e",
    f"PwC is {100 * (loc / gep - 1):+.1f}%; PwC's wording 'k MWh' = GWh")
add("Electricity 2024: Eurostat imports vs PwC 'net imported'", f"{EL['IMP'][y]:.0f} vs {imp}", "GWh", "Eurostat nrg_cb_e",
    f"exports {EL['EXP'][y]:.1f} GWh; equal")
add("Electricity 2024: available for final consumption + distribution losses", round(afc + dl), "GWh", "Eurostat nrg_cb_e",
    f"PwC total = {loc} + {imp} = {loc + imp}")
base_pop = mt[2025]
tot = loc + imp
scaled = tot * P30 / base_pop
add("PwC's 1,304: reproduced with 574,250 residents (1 Jan 2025) as the base", round(scaled - loc), "GWh", "calculation",
    f"({loc}+{imp}) x 636,000 / 574,250 - {loc}; PwC {PW['import_2030']}; scaling 2024 demand by population")
with_2026 = tot * P30 / mt[2026] - loc
add("The same with 588,254 residents (1 Jan 2026) as the base", round(with_2026), "GWh", "calculation", "")
add("Rise in imports 970 -> 1,304: relative to 970", round(100 * (PW["import_2030"] / imp - 1), 1), "%", "calculation",
    f"PwC prints 'circa {PW['import_pct']}%'")
add("Rise in imports 970 -> 1,304: relative to 1,304", round(100 * (PW["import_2030"] - imp) / PW["import_2030"], 1), "%", "calculation",
    "the only reading that gives about 25%")
add("Rise in total demand implied (population ratio)", round(100 * (P30 / base_pop - 1), 1), "%", "calculation", "636,000 / 574,250")
for yy in (2023, 2024, 2025):
    pop_mid = (POP["MT"][yy] + POP["MT"][yy + 1]) / 2
    add(f"Electricity per resident {yy} (AFC+losses / mean of 1 Jan populations)", round((EL["AFC"][yy] + EL["DL"][yy]) * 1e6 / pop_mid),
        "kWh", "Eurostat nrg_cb_e, demo_gind", ("2025 provisional (flag p)" if yy == 2025 else ""))
add("Imports 2023 / 2024 / 2025", f"{EL['IMP'][2023]:.0f} / {EL['IMP'][2024]:.0f} / {EL['IMP'][2025]:.0f}", "GWh", "Eurostat nrg_cb_e",
    "2025 provisional (flag p); production 2,344 / 2,186 / 2,222: local generation is not constant")

with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, ["check", "value", "unit", "source", "note"], lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
for r in rows:
    print(f"{r['check']}: {r['value']} {r['unit']}  [{r['note']}]")
