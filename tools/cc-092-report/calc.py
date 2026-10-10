#!/usr/bin/env python3
"""CC-092: could afforestation make Gozo net zero? Offline; run fetch.py first (and search_programme.py for the
search log). Reads only data/cc-092/:

- gozo_energy_baseline_table16.csv: Gozo's energy-related CO2, 2016-2020 (2023 Energy Baseline Scenario for Gozo).
- eurostat_extract.csv: Malta's inventory total and LULUCF / forest land; population of Malta and MT002; area of
  MT002; Malta's forest area (FAO definitions); water exploitation index plus (WEI+).
- clc2018_gozo_polygons.csv: CORINE Land Cover 2018 polygons around Gozo; a polygon is on Malta if it lies wholly
  south of 36.0 N, on Comino if it reaches south of 36.025 N east of 14.31 E, otherwise on Gozo (checked by eye
  against the extents; sea, class 523, is left out).
- sequestration_rates.csv: low / central / high rates from the literature (Renna et al. 2024; Grünzweig et al.
  2007; Bernal et al. 2018), plus sensitivity rates.
- planting_inputs.csv: planting density and survival from the literature; Malta's recent planting count.
- natura2000_overlap.csv: Gozo's CORINE land inside Natura 2000 sites (natura.py).
- nasa_power_gozo.json, nasa_power_yatir.json: 1991-2020 rainfall (MERRA-2), Gozo and the Yatir forest.

Writes data/cc-092/afforestation_offset.csv (every emissions x rate case) and data/cc-092/checks.csv.
"""
import csv, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-092"
C_TO_CO2 = 44 / 12
GOZO_HA_EC = 6700        # Gozo 67 km2: European Commission, Clean energy for EU islands, Malta page (as in CC-107)

# ------------------------------------------------------------------ inputs
t16 = {int(r["year"]): float(r["co2_t"]) for r in csv.DictReader(open(D / "gozo_energy_baseline_table16.csv"))
       if r["sector"] == "Total"}
es = {}
for r in csv.DictReader(open(D / "eurostat_extract.csv")):
    es[(r["dataset"], r["geo"], r["item"], r["year"])] = (float(r["value"]), r["flag"])


def esv(ds, geo, item, year):
    return es[(ds, geo, item, str(year))][0]


GGE = "unit=THS_T|airpol=GHG|src_crf="
POP = "sex=T|unit=NR|age=TOTAL"
rates = {r["key"]: r for r in csv.DictReader(open(D / "sequestration_rates.csv"))}


def t_co2(r):
    v = float(r["value"])
    return v / 100 * C_TO_CO2 if r["unit"].startswith("g C") else v   # g C m-2 yr-1 -> t C ha-1 yr-1 -> t CO2


RATE = {"low": t_co2(rates["renna2024_low"]), "central": t_co2(rates["grunzweig2007"]),
        "high": t_co2(rates["bernal2018_pine_tdry"])}
RATE_SRC = {"low": "Renna et al. 2024 (native oaks, biomass, lower end)",
            "central": "Grünzweig et al. 2007 (Yatir, ecosystem, 35-year mean)",
            "high": "Bernal et al. 2018 (planted pine, temperate dry, biomass, 0-20 years)"}
SENS = {k: t_co2(r) for k, r in rates.items() if r["case"] == "sensitivity"}
plant = {r["input"]: float(r["value"]) for r in csv.DictReader(open(D / "planting_inputs.csv"))}
power = {n: json.load(open(D / f"nasa_power_{n}.json")) for n in ("gozo", "yatir")}

# Gozo emissions cases (t CO2 or t CO2e a year)
share24 = esv("demo_r_pjangrp3", "MT002", POP, 2024) / esv("demo_r_pjangrp3", "MT", POP, 2024)
EMIS = {"EU islands baseline 2020 (lowest year)": t16[2020],
        "EU islands baseline 2019 (highest year)": t16[2019],
        "EU islands baseline, mean 2016-2020": sum(t16.values()) / len(t16),
        "Population share of Malta's 2024 inventory (all GHG)": esv("env_air_gge", "MT", GGE + "TOTX4_MEMO", 2024)
        * 1000 * share24}

# CORINE 2018: Gozo land by class
clc = list(csv.DictReader(open(D / "clc2018_gozo_polygons.csv")))


def island(r):
    if float(r["lat_max"]) < 36.0:
        return "Malta"
    if float(r["lat_min"]) < 36.025 and float(r["lon_min"]) > 14.31:
        return "Comino"
    return "Gozo"


CLC_NAMES = {"112": "Discontinuous urban fabric", "131": "Mineral extraction sites", "142": "Sport and leisure facilities",
             "211": "Non-irrigated arable land", "242": "Complex cultivation patterns",
             "243": "Agriculture with significant natural vegetation", "323": "Sclerophyllous vegetation (incl. garrigue)",
             "333": "Sparsely vegetated areas", "313": "Mixed forest"}
gozo = {}
for r in clc:
    if r["code_18"] == "523":
        continue
    if island(r) == "Gozo":
        gozo[r["code_18"]] = gozo.get(r["code_18"], 0) + float(r["area_ha"])
gozo_clc_ha = sum(gozo.values())
semi_nat = gozo.get("323", 0) + gozo.get("333", 0)
agri = gozo.get("211", 0) + gozo.get("242", 0) + gozo.get("243", 0)
built = gozo.get("112", 0) + gozo.get("131", 0) + gozo.get("142", 0)
LAND = {"Semi-natural land (CORINE 323 + 333)": semi_nat,
        "All farmland and semi-natural land (CORINE 2xx + 3xx)": semi_nat + agri,
        "All of Gozo (67 km2)": GOZO_HA_EC}

# ------------------------------------------------------------------ scenario table
rows = []
for en, e in EMIS.items():
    for rk, rate in RATE.items():
        ha = e / rate
        row = {"emissions_case": en, "emissions_t": round(e), "rate_case": rk, "rate_source": RATE_SRC[rk],
               "t_co2_per_ha_yr": round(rate, 2), "forest_needed_ha": round(ha), "forest_needed_km2": round(ha / 100, 1),
               "multiple_of_gozo_area": round(ha / GOZO_HA_EC, 1),
               "multiple_of_malta_forest_2025": round(ha / (esv("for_area", "MT", "unit=THS_HA|indic_fo=FOR", 2025) * 1000), 1)}
        for ln, la in LAND.items():
            row[f"offset_pct_if_{ln}"] = round(100 * la * rate / e, 1)
        rows.append(row)
with open(D / "afforestation_offset.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)

# ------------------------------------------------------------------ checks
SRC_T16 = "Energy Baseline Scenario for Gozo (2023), Table 16, PDF p. 25"
SRC_ES = "Eurostat (env_air_gge, demo_r_pjangrp3, reg_area3, for_area, sdg_06_60), retrieved 10 Oct 2026"
SRC_CLC = "EEA CORINE Land Cover 2018 (map service), retrieved 10 Oct 2026; island by polygon extent"
SRC_LIT = "data/cc-092/sequestration_rates.csv (Crossref-verified sources)"
checks = []


def add(check, value, unit, source, note=""):
    checks.append({"check": check, "value": value, "unit": unit, "source": source, "note": note})


add("Gozo energy-related CO2, lowest year (2020)", round(t16[2020]), "t CO2", SRC_T16, "energy only; not official statistics")
add("Gozo energy-related CO2, highest year (2019)", round(t16[2019]), "t CO2", SRC_T16,
    "the study flags the 2019 land-transport peak for a possible change of method")
add("Gozo energy-related CO2, mean 2016-2020", round(EMIS["EU islands baseline, mean 2016-2020"]), "t CO2", SRC_T16, "")
add("Gozo and Comino share of Malta's population, 1 Jan 2024", round(100 * share24, 2), "%", SRC_ES,
    f"{esv('demo_r_pjangrp3', 'MT002', POP, 2024):.0f} of {esv('demo_r_pjangrp3', 'MT', POP, 2024):.0f}")
add("Gozo emissions 2024, population share of Malta's inventory total", round(EMIS["Population share of Malta's 2024 inventory (all GHG)"]),
    "t CO2e", SRC_ES, "NOT Gozo data: Malta's 2024 total excl. LULUCF (2,170.21 kt) x population share; as in Claim Check 031")
for rk, rate in RATE.items():
    add(f"Sequestration rate, {rk} case", round(rate, 2), "t CO2 per ha per year", SRC_LIT, RATE_SRC[rk])
for k, v in SENS.items():
    add(f"Sequestration rate, sensitivity: {k}", round(v, 2), "t CO2 per ha per year", SRC_LIT, "")
for rk, rate in RATE.items():
    lo, hi = t16[2020] / rate, t16[2019] / rate
    add(f"New forest needed to offset Gozo's 2016-2020 energy CO2, {rk} rate", f"{lo / 100:.0f}-{hi / 100:.0f}", "km2",
        SRC_T16 + "; " + SRC_LIT, f"{lo / GOZO_HA_EC:.1f}-{hi / GOZO_HA_EC:.1f} times Gozo's 67 km2")
add("Gozo area used", 67, "km2", "European Commission, Clean energy for EU islands: Malta (page read 10 Oct 2026)",
    "Malta 246, Gozo 67, Comino 3.5 km2 on the same page")
add("Gozo and Comino land area (NUTS 3 MT002), 2026", esv("reg_area3", "MT002", "landuse=L0008|unit=KM2", 2026), "km2", SRC_ES,
    "total area incl. inland water 69 km2")
add("Gozo land mapped by CORINE 2018 (all classes)", round(gozo_clc_ha), "ha", SRC_CLC, "25 ha minimum mapping unit")
for code in sorted(gozo):
    add(f"Gozo, CORINE {code} {CLC_NAMES.get(code, '')}", round(gozo[code]), "ha", SRC_CLC,
        f"{100 * gozo[code] / gozo_clc_ha:.1f}% of Gozo's mapped land")
add("Gozo semi-natural land (CORINE 323 + 333)", round(semi_nat), "ha", SRC_CLC,
    f"{100 * semi_nat / gozo_clc_ha:.1f}% of mapped land; 323 includes maquis and garrigue (CLC nomenclature)")
add("Gozo farmland (CORINE 211 + 242 + 243)", round(agri), "ha", SRC_CLC, f"{100 * agri / gozo_clc_ha:.1f}% of mapped land")
add("Gozo built-up and other artificial land (CORINE 112 + 131 + 142)", round(built), "ha", SRC_CLC,
    f"{100 * built / gozo_clc_ha:.1f}% of mapped land")
add("Forest classes (CORINE 31x) mapped on Gozo", sum(v for k, v in gozo.items() if k.startswith("31")), "ha", SRC_CLC,
    "none at the 25 ha mapping unit")
for ln, la in LAND.items():
    for rk, rate in RATE.items():
        add(f"Share of Gozo's 2016-2020 energy CO2 offset if {ln} were forest, {rk} rate",
            f"{100 * la * rate / t16[2019]:.1f}-{100 * la * rate / t16[2020]:.1f}", "%",
            SRC_CLC + "; " + SRC_LIT + "; " + SRC_T16,
            f"{la:.0f} ha x {rate:.2f} t, against {t16[2019]:.0f} t (2019) and {t16[2020]:.0f} t (2020); a ceiling, not a plan")
n2k = {r["land_group"]: r for r in csv.DictReader(open(D / "natura2000_overlap.csv"))}
SRC_N2K = "EEA CORINE Land Cover 2018 and Natura 2000 sites (MS='MT'), EPSG:3035, retrieved 10 Oct 2026 (natura.py)"
for g, lab in (("semi-natural", "Gozo semi-natural land"), ("farmland", "Gozo farmland"),
               ("all Gozo land (CORINE)", "All Gozo land mapped by CORINE")):
    r = n2k[g]
    add(f"{lab} inside Natura 2000 sites (Habitats or Birds Directive)", round(float(r["in_either_ha"])), "ha", SRC_N2K,
        f"{r['in_either_pct']}% of {float(r['area_ha']):.0f} ha; Habitats Directive sites alone {r['in_Habitats Directive (SAC/SCI)_pct']}%")
fa = esv("for_area", "MT", "unit=THS_HA|indic_fo=FOR", 2025) * 1000
add("Malta's forest area (FAO definition), 2025", round(fa), "ha", SRC_ES, "whole country; other wooded land 70 ha")
add("Forest needed at the central rate (2019 energy CO2) as a multiple of Malta's forest area",
    round(t16[2019] / RATE["central"] / fa), "times", SRC_ES + "; " + SRC_LIT, "")
fl = esv("env_air_gge", "MT", GGE + "CRF4A", 2024)
add("Malta inventory, forest land (CRF 4.A), 2024", fl, "kt CO2e", SRC_ES, "negative = net removal; whole country")
add("Malta inventory, LULUCF total (CRF 4), 2024", esv("env_air_gge", "MT", GGE + "CRF4", 2024), "kt CO2e", SRC_ES,
    "positive = net emission")
add("Malta's forest-land removals in 2024 as a share of Gozo's 2019 energy CO2", round(100 * -fl * 1000 / t16[2019], 2),
    "%", SRC_ES + "; " + SRC_T16, "national sink, as reported")
for y in (2022, 2023):
    add(f"Water exploitation index plus (WEI+), Malta, {y}", esv("sdg_06_60", "MT", "statinfo=VAL_A|unit=PC", y), "%", SRC_ES,
        f"four-year average {esv('sdg_06_60', 'MT', 'statinfo=AVG_4Y|unit=PC', y)}%; EU {esv('sdg_06_60', 'EU27_2020', 'statinfo=VAL_A|unit=PC', y)}%; "
        "Eurostat: above 20% a sign of water scarcity, 40% or more severe")
for n in ("gozo", "yatir"):
    p = power[n]["properties"]["parameter"]["PRECTOTCORR"]["ANN"]
    add(f"Mean annual rainfall 1991-2020, {n.title()} (NASA POWER, MERRA-2)", round(p * 365.25), "mm a year",
        "NASA POWER climatology API (MERRA-2), retrieved 10 Oct 2026", "reanalysis grid cell (about 50 km); approximate")
dens = plant["Tree density of the measured Yatir plantation"]
surv = plant["Survival of planted Aleppo pine after 20 years, no shelter"] / 100
pace = plant["Trees planted by government entities in Malta and Gozo, 2022 legislature to 31 Dec 2025"] / \
    plant["Length of that period, 26 Mar 2022 to 31 Dec 2025"]
trees_semi = semi_nat * dens / surv
add("Trees to plant to stock Gozo's semi-natural land at Yatir density, allowing for 20-year survival", round(trees_semi, -3),
    "trees", "planting_inputs.csv; " + SRC_CLC, f"{semi_nat:.0f} ha x {dens:.0f} per ha / {surv:.2f}")
add("Malta's recent government planting pace", round(pace, -2), "trees a year", "planting_inputs.csv (PQ 34270 via Claim Check 010)",
    "national, all purposes")
add("Years at that pace to plant that many trees", round(trees_semi / pace), "years", "derived", "order of magnitude only")
with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["check", "value", "unit", "source", "note"])
    w.writeheader()
    w.writerows(checks)
for c in checks:
    print(f"{c['check'][:96]:96s} {c['value']!s:>12} {c['unit']}")
