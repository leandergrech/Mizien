#!/usr/bin/env python3
"""CC-158: test the NAO's ClimateScanner figures (overall 6.92; axes 6.55, 8.00, 6.20) and put them beside Malta's
emissions outcomes. Reads data/cc-158/components.csv and the CC-094 / CC-025 data files. Writes data/cc-158/checks.csv."""
import csv, pathlib, statistics as st
ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-158"
rows = []
def add(check, value, unit, source, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": source, "note": note})

NAO = "NAO ClimateScanner review (Oct 2025), Appendix (data/cc-158/components.csv)"
TIER = {"items_advanced": 10.0, "items_intermediate": 6.66, "items_early": 3.33, "items_none": 0.0}
comp = [r for r in csv.DictReader(open(D / "components.csv"))]
rated = [r for r in comp if r["nao_score"]]
bad = 0
for r in rated:
    n = sum(int(r[k]) for k in TIER)
    s = sum(TIER[k] * int(r[k]) for k in TIER) / n
    ok = abs(s - float(r["nao_score"])) < 0.011   # the NAO truncates or rounds to two decimals
    bad += not ok
    add(f"{r['component']} {r['name']}: score from item ratings", round(s, 3), "of 10", NAO,
        f"NAO {r['nao_score']}; {n} items; {'matches' if ok else 'DIFFERS'}")
add("Components whose published score is reproduced from their item ratings", f"{len(rated) - bad} of {len(rated)}", "", NAO)
axes = {}
for r in rated:
    axes.setdefault(r["axis"], []).append(float(r["nao_score"]))
pub = {"Governance": 6.55, "Public Policies": 8.00, "Finance": 6.20}
for a, v in axes.items():
    add(f"{a} axis: mean of its component scores", round(st.mean(v), 3), "of 10", NAO, f"NAO {pub[a]:.2f}; {len(v)} components")
overall_axes = st.mean(st.mean(v) for v in axes.values())
add("Overall: mean of the three axis scores", round(overall_axes, 3), "of 10", NAO, "NAO 6.92 (PDF p. 14)")
add("Overall: mean of the 18 rated component scores (alternative)", round(st.mean(float(r["nao_score"]) for r in rated), 3),
    "of 10", NAO, "the Handbook defines component and axis scores only")
strong = [r["component"] for r in rated if float(r["nao_score"]) >= 6.66]
add("Components at or above 6.66 ('strengths')", f"{len(strong)} of {len(rated)}", "", NAO, " ".join(strong))
add("Components at or below 3.33 ('challenges')", sum(float(r["nao_score"]) <= 3.33 for r in rated), "", NAO)
for k, lab in (("items_advanced", "advanced"), ("items_intermediate", "intermediate"), ("items_early", "early"), ("items_none", "no progress")):
    add(f"Items rated {lab} (P5 counted once)", sum(int(r[k]) for r in rated), "items", NAO)
add("Score of an item rated 'intermediate stage' (many aspects present, room for improvement)", 6.66, "of 10",
    "ClimateScanner Handbook (May 2024), p. 10; NAO Table 1 (PDF p. 14)", "equal to the threshold for a strength")
add("Overall score above the 'intermediate' value", round(overall_axes - 6.66, 2), "points", NAO)

# Outcomes (not measured by the ClimateScanner): effort-sharing emissions, EEA (saved for CC-094)
EEA = "EEA GHG_ESD-ESR_2025.xlsx via data/cc-094/eea_esr_emissions.csv, retrieved 6 Oct 2026"
esr = {int(r["year"]): float(r["value"]) * 1000 for r in csv.DictReader(open(ROOT / "data/cc-094/eea_esr_emissions.csv"))
       if r["country"] == "Malta" and r["series"] in ("ESD", "ESR")}
leg = {(r["item"], r["year"]): float(r["value"]) for r in csv.DictReader(open(ROOT / "data/cc-094/esr_legal_inputs.csv"))
       if r["country"] == "MT" and not r["item"].startswith("#")}
base = leg[("2005 ESR base", "2005")] / 1000
LEG = "Implementing Decisions (EU) 2020/2126 and 2026/895; Regulation (EU) 2023/857 (data/cc-094/esr_legal_inputs.csv)"
for y in (2022, 2023, 2024):
    add(f"Malta effort-sharing emissions {y} vs the legal 2005 base", round(100 * (esr[y] / base - 1), 1), "%", f"{EEA}; {LEG}",
        f"{esr[y]:.1f} kt vs {base:.1f} kt")
    alloc = leg[("Annual emission allocation", str(y))] / 1000
    add(f"Malta {y}: effort-sharing emissions minus the annual allocation", round(esr[y] - alloc, 1), "kt CO2e", f"{EEA}; {LEG}",
        f"allocation {alloc:.1f} kt")
add("Malta 2030 effort-sharing target vs 2005", leg[("2030 target vs 2005", "2030")], "%", LEG)
cc094 = {r["check"]: r for r in csv.DictReader(open(ROOT / "data/cc-094/checks.csv"))}
add("Malta 2030 projection with planned measures vs 2005 (from CC-094)", float(cc094["Malta 2030 vs 2005, WAM (additional measures)"]["value"]),
    "%", "EEA GHG projections 2025 submission via data/cc-094/checks.csv, retrieved 6 Oct 2026")
ES = "Eurostat env_air_gge (total excl. LULUCF, incl. international aviation memo), via data/cc-025/eurostat_gdp_ghg_pop.csv, retrieved 5 Oct 2026"
tot = {(r["geo"], int(r["year"])): float(r["value"]) for r in csv.DictReader(open(ROOT / "data/cc-025/eurostat_gdp_ghg_pop.csv"))
       if r["dataset"] == "env_air_gge" and r["item"] == "TOTX4_MEMO"}
for g, lab in (("MT", "Malta"), ("EU27_2020", "EU-27")):
    add(f"{lab} total GHG change 2005-2024", round(100 * (tot[(g, 2024)] / tot[(g, 2005)] - 1), 1), "%", ES,
        f"{tot[(g, 2005)]:.3f} -> {tot[(g, 2024)]:.3f} Mt CO2e")
add("Malta total GHG change 2016 (lowest year) to 2024", round(100 * (tot[("MT", 2024)] / tot[("MT", 2016)] - 1), 1), "%", ES)

with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for r in rows:
    print(f"{r['check'][:78]:78s} {str(r['value']):>9} {r['unit']:9s} {r['note'][:60]}")
