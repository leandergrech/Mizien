"""Claim Check 167: energy intensity 2019-2024, with and without marine bunkers. Output: data/cc-167/checks.csv"""
import csv
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data/cc-167"
r = {row["year"]: {k: float(v) for k, v in row.items() if k != "year" and v} for row in csv.DictReader(open(D / "eurostat_malta_energy_gdp.csv"))}
a, b = r["2019"], r["2024"]
pct = lambda x, y: round(100 * (y / x - 1), 1)
SRC = "Eurostat nrg_ind_ei, nrg_bal_s, nama_10_gdp, demo_gind (data/cc-167/eurostat_malta_energy_gdp.csv)"
out = [
    ("Energy intensity of GDP (published, GAE/GDP, CLV10), 2019-2024", pct(a["ei_clv10_mt_kgoe_per_keur"], b["ei_clv10_mt_kgoe_per_keur"]), "%", SRC, "Survey: -27.1%"),
    ("EU-27 energy intensity (published), 2019-2024", pct(a["ei_clv10_eu27_kgoe_per_keur"], b["ei_clv10_eu27_kgoe_per_keur"]), "%", SRC, ""),
    ("Malta intensity level 2024 vs EU-27 (published)", round(b["ei_clv10_mt_kgoe_per_keur"] / b["ei_clv10_eu27_kgoe_per_keur"], 2), "ratio", SRC, "bunkers inflate Malta's level"),
    ("International maritime bunkers share of GAE, 2024", round(100 * b["intl_maritime_bunkers_ktoe"] / b["gae_ktoe"], 1), "%", SRC, ""),
    ("Real GDP, 2019-2024 (current vintage)", pct(a["gdp_clv10_meur"], b["gdp_clv10_meur"]), "%", SRC, ""),
    ("Gross available energy, 2019-2024", pct(a["gae_ktoe"], b["gae_ktoe"]), "%", SRC, ""),
    ("International maritime bunkers, 2019-2024", pct(a["intl_maritime_bunkers_ktoe"], b["intl_maritime_bunkers_ktoe"]), "%", SRC, ""),
    ("Gross inland consumption (excludes bunkers), 2019-2024", pct(a["gic_ktoe"], b["gic_ktoe"]), "%", SRC, ""),
    ("Final energy consumption, 2019-2024", pct(a["final_energy_ktoe"], b["final_energy_ktoe"]), "%", SRC, ""),
    ("GAE per GDP (current GDP vintage), 2019-2024", pct(a["gae_ktoe"] / a["gdp_clv10_meur"], b["gae_ktoe"] / b["gdp_clv10_meur"]), "%", SRC, ""),
    ("Gross inland consumption per GDP, 2019-2024", pct(a["gic_ktoe"] / a["gdp_clv10_meur"], b["gic_ktoe"] / b["gdp_clv10_meur"]), "%", SRC, "intensity without bunkers"),
    ("Final energy per GDP, 2019-2024", pct(a["final_energy_ktoe"] / a["gdp_clv10_meur"], b["final_energy_ktoe"] / b["gdp_clv10_meur"]), "%", SRC, ""),
    ("Population, 2019-2024", pct(a["population"], b["population"]), "%", SRC, ""),
    ("Final energy per person, 2019-2024", pct(a["final_energy_ktoe"] / a["population"], b["final_energy_ktoe"] / b["population"]), "%", SRC, ""),
]
with open(D / "checks.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["check", "value", "unit", "source", "note"])
    w.writerows(out)
for o in out:
    print(o[0], o[1], o[4])
