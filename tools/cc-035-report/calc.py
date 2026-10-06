#!/usr/bin/env python3
"""CC-035: test the EEA's Malta PM2.5 statement against the EEA's own data and against measurements.

Statement (EEA, Air pollution country fact sheets 2025: quick country facts, modified 1 Dec 2025): the rate of
all-cause natural deaths attributable to long-term exposure to PM2.5 above 5 ug/m3 (per 100 000 inhabitants aged 30 or
over) "is estimated to have been reduced by 67.7% between 2005 and 2023 (from 143.5 to 46.3, respectively), resulting
in 172 (95% CI: 131-192) attributable deaths in 2023".

Inputs (all in data/cc-035/, retrieved 6 Oct 2026 by fetch.py): the EEA burden-of-disease table (Malta, every scenario;
all countries, WHO 2021 baseline), Eurostat sdg_11_52, demo_pjan, demo_magec, hlth_cd_aro, env_air_emis, and EEA
station files for Malta (AirBase and E1a). Output: data/cc-035/checks.csv and data/cc-035/station_vs_model.csv.
"""
import csv, math, pathlib
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-035"
EBD = "EEA burden-of-disease table (Countries & NUTS), retrieved 6 Oct 2026"
ETC = "ETC HE Report 2025/8 (Soares et al. 2025), Annex 3-4"
S_SDG = "Eurostat sdg_11_52, updated 9 Dec 2025, retrieved 6 Oct 2026"
S_ST = "EEA station files (AirBase, E1a), retrieved 6 Oct 2026"
BASE = "Baseline from WHO 2021 AQG"
BETA = math.log(1.08) / 10          # WHO 2021 AQG all-cause CRF: RR 1.08 per 10 ug/m3 (Chen and Hoek 2020)
CF = 5.0                            # counterfactual: WHO 2021 annual guideline level
EU27 = ("Austria Belgium Bulgaria Croatia Cyprus Czechia Denmark Estonia Finland France Germany Greece Hungary Ireland "
        "Italy Latvia Lithuania Luxembourg Malta Netherlands Poland Portugal Romania Slovakia Slovenia Spain Sweden").split()
rows = []


def add(check, value, unit, source, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": source, "note": note})


def f(x):
    return float(x) if x not in ("", None) else None


# ------------------------------------------------------------------ EEA table: Malta
mt = defaultdict(dict)      # scenario -> year -> row (attributable deaths)
for r in csv.DictReader(open(D / "eea_ebd_malta_pm25.csv", encoding="utf-8")):
    if r["Health Indicator"] == "Attributable deaths (AD)":
        mt[r["Scenario"]][int(r["Year"])] = r
B = mt[BASE]
y0, y1 = 2005, 2023
R = lambda y, sc=BASE: f(mt[sc][y]["Value for 100k Of Affected Population"])
AD = lambda y, sc=BASE: f(mt[sc][y]["Value"])
POP30 = lambda y: f(B[y]["Affected Population"])
PWC = lambda y: f(B[y]["Air Pollution Population Weighted Average [ug/m3]"])

add("EEA table: Malta rate 2005 (AD per 100k aged 30+)", R(y0), "per 100k", EBD, "statement: 143.5")
add("EEA table: Malta rate 2023", R(y1), "per 100k", EBD, "statement: 46.3")
fall = 100 * (R(y0) - R(y1)) / R(y0)
add("Fall in the rate, 2005-2023", round(fall, 2), "%", "calculated", "statement: 67.7%")
add("EEA table: Malta attributable deaths 2023 (95% CI)",
    f"{AD(y1):.0f} ({f(B[y1]['Value - lower CI']):.0f}-{f(B[y1]['Value - upper CI']):.0f})", "deaths", EBD,
    "statement: 172 (131-192)")
add("ETC HE technical report: Malta AD 2023 (95% CI) and rate", "173 (132-193); 46.3 (35.2-51.7)", "deaths; per 100k",
    ETC, "Table A4.1, read 6 Oct 2026; one death above the table and the quick-facts page")
add("Deaths implied by the 2023 rate x population aged 30+", round(R(y1) * POP30(y1) / 1e5, 1), "deaths", "calculated",
    f"46.3 x {POP30(y1):.0f} / 100 000; 46.25-46.35 gives {46.25 * POP30(y1) / 1e5:.1f}-{46.35 * POP30(y1) / 1e5:.1f}: "
    "consistent with 172 truncated and 173 rounded")
add("Rate recomputed from table AD / population 30+, 2005", round(AD(y0) / POP30(y0) * 1e5, 2), "per 100k", "calculated")
add("Rate recomputed from table AD / population 30+, 2023", round(AD(y1) / POP30(y1) * 1e5, 2), "per 100k", "calculated",
    "with AD = 172; the table's 46.3 uses the unrounded AD")

# Eurostat sdg_11_52 carries the same numbers
sdg = {(r["geo"], r["unit"], int(r["time"])): (f(r["value"]), r["flag"])
       for r in csv.DictReader(open(D / "eurostat_sdg_11_52.csv", encoding="utf-8"))}
add("Eurostat sdg_11_52: Malta deaths 2005 / 2023", f"{sdg[('MT', 'NR', y0)][0]:.0f} / {sdg[('MT', 'NR', y1)][0]:.0f}",
    "deaths", S_SDG, "no flags on the Malta values" if not (sdg[('MT', 'NR', y0)][1] or sdg[('MT', 'NR', y1)][1]) else "flagged")
add("Eurostat sdg_11_52: Malta rate per 100 000 inhabitants (all ages) 2005 / 2023",
    f"{sdg[('MT', 'RT', y0)][0]:.0f} / {sdg[('MT', 'RT', y1)][0]:.0f}", "per 100k", S_SDG,
    "a different denominator from the statement's (all ages, not 30+)")
add("Eurostat rate (all ages): fall 2005-2023", round(100 * (1 - sdg[('MT', 'RT', y1)][0] / sdg[('MT', 'RT', y0)][0]), 1),
    "%", "calculated")
add("Eurostat sdg_11_52: years in the series", ", ".join(str(y) for y in sorted({y for (g, u, y) in sdg if g == "MT" and u == "NR"})),
    "years", S_SDG, "no 2006 value (the EEA table has none either)")

# the number of deaths fell less than the rate, because the population aged 30+ grew
add("Attributable deaths 2005 -> 2023", f"{AD(y0):.0f} -> {AD(y1):.0f}", "deaths", EBD)
add("Fall in the number of attributable deaths, 2005-2023", round(100 * (1 - AD(y1) / AD(y0)), 1), "%", "calculated",
    "the statement gives the rate, not the number")
add("Population aged 30+ (EEA table) 2005 -> 2023", f"{POP30(y0):.0f} -> {POP30(y1):.0f}", "people", EBD,
    f"+{100 * (POP30(y1) / POP30(y0) - 1):.1f}%")

# Eurostat population aged 30+ on 1 January: cross-check of the denominator
pj = defaultdict(float)
for r in csv.DictReader(open(D / "eurostat_demo_pjan_mt.csv", encoding="utf-8")):
    a = r["age"]
    if a.startswith("Y") and a not in ("Y_LT1",) and (a == "Y_OPEN" or int(a[1:]) >= 30):
        pj[int(r["time"])] += f(r["value"])
for y in (y0, y1):
    add(f"Eurostat demo_pjan: Malta population aged 30+ on 1 Jan {y}", round(pj[y]), "people",
        "Eurostat demo_pjan, retrieved 6 Oct 2026", f"EEA table: {POP30(y):.0f}")

# ------------------------------------------------------------------ the method: concentration, CRF, counterfactual
paf = lambda c: 1 - math.exp(-BETA * max(c - CF, 0))
add("Population-weighted PM2.5 (modelled), 2005 -> 2023", f"{PWC(y0)} -> {PWC(y1)}", "ug/m3", EBD,
    f"fall {100 * (1 - PWC(y1) / PWC(y0)):.1f}%")
add("Excess above 5 ug/m3, 2005 -> 2023", f"{PWC(y0) - CF:.1f} -> {PWC(y1) - CF:.1f}", "ug/m3", "calculated",
    f"fall {100 * (1 - (PWC(y1) - CF) / (PWC(y0) - CF)):.1f}%")
add("2005 reference map (ETC/ATNI 2020/1): Malta population-weighted PM2.5", 21.2, "ug/m3",
    "ETC/ATNI Report 2020/1, Table 2.3", "EEA table now 21.0")
add("Attributable fraction at the national PWC, 2005 / 2023", f"{100 * paf(PWC(y0)):.2f} / {100 * paf(PWC(y1)):.2f}", "%",
    "calculated", "PAF = 1 - exp(-ln(1.08)/10 x (PWC - 5)); the EEA works cell by cell on a 1 km grid")

# baseline mortality: natural deaths aged 30+ (all deaths minus external causes, as the ETC does)
dth = defaultdict(float)
for r in csv.DictReader(open(D / "eurostat_demo_magec_mt.csv", encoding="utf-8")):
    a = r["age"]
    if a.startswith("Y") and a != "Y_LT1" and (a == "Y_OPEN" or int(a[1:]) >= 30):
        dth[int(r["time"])] += f(r["value"])
ext = defaultdict(float)
allc = defaultdict(float)
AGES30 = "Y30-34 Y35-39 Y40-44 Y45-49 Y50-54 Y55-59 Y60-64 Y65-69 Y70-74 Y75-79 Y80-84 Y85-89 Y90-94 Y_GE95".split()
for r in csv.DictReader(open(D / "eurostat_hlth_cd_aro_mt.csv", encoding="utf-8")):
    if r["age"] in AGES30 and r["value"] not in ("", None):
        (ext if r["icd10"] == "V01-Y89" else allc)[int(r["time"])] += f(r["value"])
share = lambda y: ext[y] / allc[y]
natural = {y0: dth[y0] * (1 - share(2011)), y1: dth[y1] * (1 - share(y1 if y1 in ext else max(ext)))}
add("Eurostat: deaths aged 30+ (all causes) 2005 / 2023", f"{dth[y0]:.0f} / {dth[y1]:.0f}", "deaths",
    "Eurostat demo_magec, retrieved 6 Oct 2026")
add("Eurostat: external-cause share of deaths aged 30+, 2011 / 2023", f"{100 * share(2011):.2f} / {100 * share(y1):.2f}",
    "%", "Eurostat hlth_cd_aro (residents), retrieved 6 Oct 2026", "2011 stands in for 2005, as in the ETC method")
for y in (y0, y1):
    est = paf(PWC(y)) * natural[y]
    add(f"Our approximation of attributable deaths {y} (PAF at national PWC x natural deaths 30+)", round(est, 1),
        "deaths", "calculated", f"EEA: {AD(y):.0f}; difference {100 * (est / AD(y) - 1):+.1f}%")
    add(f"Implied natural death rate aged 30+ {y} (EEA AD / PAF / population 30+)",
        round(AD(y) / paf(PWC(y)) / POP30(y) * 1e5, 1), "per 100k", "calculated",
        f"Eurostat-based: {natural[y] / POP30(y) * 1e5:.1f}")
pr = paf(PWC(y1)) / paf(PWC(y0))
mr = (AD(y1) / paf(PWC(y1)) / POP30(y1)) / (AD(y0) / paf(PWC(y0)) / POP30(y0))
add("Decomposition of the rate fall: attributable fraction ratio x baseline death-rate ratio",
    f"{pr:.3f} x {mr:.3f} = {pr * mr:.3f}", "ratio", "calculated",
    f"fall {100 * (1 - pr * mr):.1f}%; with the fraction alone the fall would be {100 * (1 - pr):.1f}%")

# other counterfactuals and CRFs (same maps): the size of the fall depends on them
for sc, lab in (("Baseline from WHO 2005 (HRAPIE 2013)", "previous method (RR 1.062, all concentrations)"),
                ("Sensitivity: WHO 2021 AQG but CF=0 for NO2 and PM2.5; SOMO10 included", "all concentrations (CF 0)"),
                ("Sensitivity: WHO 2021 AQG but CF=20 for NO2 and CF=10 for PM2.5", "above the 2030 EU limit (CF 10)")):
    add(f"Rate fall 2005-2023, {lab}", round(100 * (1 - R(y1, sc) / R(y0, sc)), 1), "%", EBD,
        f"{R(y0, sc)} -> {R(y1, sc)} per 100k aged 30+")

# rough sensitivity of the 2005 start to the map's own error: the ETC's cross-validation RMSE for the 2005 PM2.5 map in
# urban background areas is 2.9 ug/m3 (ETC/ATNI 2020/1, Table A.4). Shifting Malta's 2005 PWC by that amount and
# scaling the 2005 rate by the attributable fraction gives the range below (a Europe-wide error applied to one country:
# indicative only).
RMSE05 = 2.9
for d in (-RMSE05, RMSE05):
    r05 = R(y0) * paf(PWC(y0) + d) / paf(PWC(y0))
    add(f"Rate fall 2005-2023 if Malta's 2005 map value were {d:+.1f} ug/m3", round(100 * (1 - R(y1) / r05), 1), "%",
        "calculated; RMSE from ETC/ATNI Report 2020/1, Table A.4 (urban background, 2005)",
        f"2005 rate would be {r05:.1f}; indicative only")

# other base years
for b in (2007, 2008, 2010):
    add(f"Rate fall {b}-2023 (WHO 2021 baseline)", round(100 * (1 - R(y1) / R(b)), 1), "%", EBD, f"{R(b)} -> {R(y1)}")
add("Highest rate in the series", max((R(y), y) for y in B)[0], "per 100k", EBD, str(max((R(y), y) for y in B)[1]))
add("Rate range 2013-2023", f"{min(R(y) for y in B if y >= 2013)}-{max(R(y) for y in B if y >= 2013)}", "per 100k", EBD)

# ------------------------------------------------------------------ EU comparison
cr = defaultdict(dict)
for r in csv.DictReader(open(D / "eea_ebd_countries_pm25.csv", encoding="utf-8")):
    cr[r["Country Or Territory"]][int(r["Year"])] = r
for r in csv.DictReader(open(D / "eea_ebd_eu27_pm25.csv", encoding="utf-8")):
    if r["Scenario"] == BASE:
        cr["European Union Countries"][int(r["Year"])] = r
falls = {}
for c in EU27:
    if c in cr and y0 in cr[c] and y1 in cr[c]:
        a, b = f(cr[c][y0]["Value for 100k Of Affected Population"]), f(cr[c][y1]["Value for 100k Of Affected Population"])
        falls[c] = 100 * (1 - b / a)
rank = sorted(falls, key=lambda c: -falls[c])
add("EU-27 countries with a 2005 and 2023 rate", len(falls), "count", EBD)
add("Malta's rank by rate fall among EU-27 (1 = largest fall)", rank.index("Malta") + 1, f"of {len(falls)}", "calculated",
    f"largest {rank[0]} {falls[rank[0]]:.1f}%, smallest {rank[-1]} {falls[rank[-1]]:.1f}%")
eu = cr.get("European Union Countries", {})
if eu:
    add("EU-27: rate 2005 -> 2023", f"{eu[y0]['Value for 100k Of Affected Population']} -> {eu[y1]['Value for 100k Of Affected Population']}",
        "per 100k", EBD, f"fall {100 * (1 - f(eu[y1]['Value for 100k Of Affected Population']) / f(eu[y0]['Value for 100k Of Affected Population'])):.1f}%")
    add("EU-27: attributable deaths 2005 -> 2023", f"{eu[y0]['Value']} -> {eu[y1]['Value']}", "deaths", EBD,
        f"fall {100 * (1 - f(eu[y1]['Value']) / f(eu[y0]['Value'])):.1f}% (EEA indicator: 57%)")
    add("EU-27: population-weighted PM2.5 2005 -> 2023",
        f"{eu[y0]['Air Pollution Population Weighted Average [ug/m3]']} -> {eu[y1]['Air Pollution Population Weighted Average [ug/m3]']}",
        "ug/m3", EBD, "EEA indicator: 19.4 -> 10.2")
with open(D / "eu27_rate_change.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["country", "rate_2005", "rate_2023", "fall_pct", "source"])
    for c in rank:
        w.writerow([c, cr[c][y0]["Value for 100k Of Affected Population"], cr[c][y1]["Value for 100k Of Affected Population"],
                    round(falls[c], 1), EBD])

# ------------------------------------------------------------------ measured concentrations (stations)
NAMES = {"MT00002": "MT00002 (PM10 only; closed)", "MT00003": "Kordin", "MT00004": "Żejtun", "MT00005": "Msida",
         "MT00007": "Għarb", "MT00008": "Attard", "MT00009": "St Paul's Bay", "MT00011": "Msida (new site)"}
st = defaultdict(dict)
for r in csv.DictReader(open(D / "eea_stations_malta_annual.csv", encoding="utf-8")):
    st[(r["pollutant"], r["station"])][int(r["year"])] = (f(r["mean_of_valid_days_ug_m3"]), f(r["coverage_pct"]))
pm25_2005 = [s for (p, s), ys in st.items() if p == "PM2.5" and 2005 in ys]
pm10_2005 = [f"{NAMES[s]} {ys[2005][0]:.1f} ({ys[2005][1]:.0f}% of days)" for (p, s), ys in st.items() if p == "PM10" and 2005 in ys]
add("Malta stations with PM2.5 measurements in 2005", len(pm25_2005), "stations", S_ST,
    "first PM2.5 days: Żejtun Aug 2006, Msida Oct 2006, Għarb Jun 2007")
add("Malta stations with PM10 measurements in 2005 (annual mean of valid days)", "; ".join(pm10_2005), "ug/m3", S_ST,
    "PM10 feeds the 'pseudo PM2.5' estimates used in the 2005 map (ETC/ATNI 2020/1)")
# the five stations in PQ 29696 (CC-007) for 2023: Msida = MT00005 to 2023, MT00011 from 2024
five = ["MT00008", "MT00005", "MT00009", "MT00004", "MT00007"]
v23 = [st[("PM2.5", s)][2023][0] for s in five]
add("Mean of the five stations' PM2.5, 2023 (EEA files)", round(sum(v23) / 5, 2), "ug/m3", S_ST,
    "PQ 29696 annex (CC-007): 11.4, 13.9, 9.5, 10.9, 8.9 -> mean 10.9; EEA modelled PWC 10.9")
long3 = ["MT00005", "MT00004", "MT00007"]
out = []
for y in range(2005, 2026):
    vals = [st[("PM2.5", s)].get(y) for s in long3]
    full = all(v and v[1] >= 75 for v in vals)
    out.append({"year": y,
                **{f"{NAMES[s]}_ug_m3": (st[('PM2.5', s)][y][0] if y in st[('PM2.5', s)] else "") for s in long3},
                **{f"{NAMES[s]}_coverage_pct": (st[('PM2.5', s)][y][1] if y in st[('PM2.5', s)] else "") for s in long3},
                "three_station_mean_ug_m3": round(sum(v[0] for v in vals) / 3, 2) if full else "",
                "eea_modelled_pwc_ug_m3": PWC(y) if y in B else "",
                "eea_rate_per_100k_30plus": R(y) if y in B else "",
                "source": f"{S_ST}; {EBD}"})
with open(D / "station_vs_model.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
full_years = [o for o in out if o["three_station_mean_ug_m3"] != "" and o["eea_modelled_pwc_ug_m3"] != ""]
first, last = full_years[0], [o for o in full_years if o["year"] == 2023][0]
add("Three long-running stations (Msida, Żejtun, Għarb): first year all >= 75% of days", first["year"], "year", S_ST,
    f"mean {first['three_station_mean_ug_m3']} vs EEA PWC {first['eea_modelled_pwc_ug_m3']}")
add("Three-station mean PM2.5, first full year -> 2023",
    f"{first['three_station_mean_ug_m3']} -> {last['three_station_mean_ug_m3']}", "ug/m3", S_ST,
    f"fall {100 * (1 - last['three_station_mean_ug_m3'] / first['three_station_mean_ug_m3']):.1f}%; EEA PWC "
    f"{first['eea_modelled_pwc_ug_m3']} -> {last['eea_modelled_pwc_ug_m3']} (fall "
    f"{100 * (1 - last['eea_modelled_pwc_ug_m3'] / first['eea_modelled_pwc_ug_m3']):.1f}%)")
for s in long3:
    ys = st[("PM2.5", s)]
    y_first = min(y for y in ys if ys[y][1] >= 75)
    add(f"{NAMES[s]}: PM2.5 first year with >= 75% of days -> 2023", f"{y_first}: {ys[y_first][0]} -> {ys[2023][0]}", "ug/m3",
        S_ST, f"fall {100 * (1 - ys[2023][0] / ys[y_first][0]):.1f}%; coverage {ys[y_first][1]}% and {ys[2023][1]}%")
diffs = [o["three_station_mean_ug_m3"] - o["eea_modelled_pwc_ug_m3"] for o in full_years]
add("Three-station mean minus EEA PWC, years with full coverage", f"{min(diffs):+.2f} to {max(diffs):+.2f}", "ug/m3",
    "calculated", f"{len(full_years)} years: " + ", ".join(str(o['year']) for o in full_years))

# ------------------------------------------------------------------ emissions (context)
em = defaultdict(dict)
for r in csv.DictReader(open(D / "eurostat_env_air_emis_mt_pm25.csv", encoding="utf-8")):
    em[r["src_nfr"]][int(r["time"])] = (f(r["value"]), r["flag"])
tot = em["NFR_TOT_NAT"]
add("Malta primary PM2.5 emissions, national total, 2005 -> 2023", f"{tot[y0][0]:.0f} -> {tot[y1][0]:.0f}", "tonnes",
    "Eurostat env_air_emis (NECD inventory), retrieved 6 Oct 2026",
    f"fall {100 * (1 - tot[y1][0] / tot[y0][0]):.1f}%; flags: {tot[y0][1] or 'none'}/{tot[y1][1] or 'none'}")
add("Of which public electricity and heat production (NFR 1A1a), 2005 -> 2023",
    f"{em['NFR1A1A'][y0][0]:.0f} -> {em['NFR1A1A'][y1][0]:.0f}", "tonnes", "Eurostat env_air_emis, retrieved 6 Oct 2026")

with open(D / "checks.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for r in rows:
    print(f"{r['check'][:92]:92s} {str(r['value'])[:40]:>40} {r['unit']}  {r['note']}")
