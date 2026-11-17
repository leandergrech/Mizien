"""Claim Check 152: ERA's NOx projection against the 2030 ceiling. Output: data/cc-152/checks.csv"""
import csv
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data/cc-152"
t4 = {r["pollutant"]: r for r in csv.DictReader(open(D / "era_napcp_table4.csv"))}["NOx"]
es = {r["year"]: float(r["nox_tonnes"]) for r in csv.DictReader(open(D / "eurostat_nox_malta.csv")) if r["nox_tonnes"]}
sh = {r["year"]: r for r in csv.DictReader(open(D / "eurostat_nox_shares.csv"))}
base, ceil30, proj = float(t4["base_2005_kt"]), float(t4["ceiling_2030_kt"]), float(t4["projection_2030_wm_kt"])
ERA = "ERA draft NAPCP first update (June 2026), Tables 1 and 4"
EST = "Eurostat env_air_emis (updated 7 Sep 2026)"
out = [
    ("2030 NOx ceiling from 2005 base and 79% commitment", round(base * (1 - 0.79), 3), "kt", ERA + "; Directive 2016/2284 Annex II",
     f"ERA table: {ceil30}"),
    ("2030 With Measures projection divided by ceiling", round(proj / ceil30, 2), "ratio", ERA, "ERA: 'almost double'"),
    ("Cut still needed from 2023 to reach the 2030 ceiling", round(100 * (1 - ceil30 / float(t4["emissions_2023_kt"])), 1), "%", ERA, ""),
    ("2023 NOx below 2005 (ERA)", round(100 * (1 - float(t4["emissions_2023_kt"]) / base), 1), "%", ERA, "ERA: 55.2%"),
    ("2030 ceiling on Eurostat's 2005 base", round(es["2005"] / 1000 * 0.21, 2), "kt", EST, "later inventory"),
    ("NOx 2024 (Eurostat)", es["2024"] / 1000, "kt", EST, ""),
    ("Range of NOx 2017-2024 (Eurostat)", f"{min(v for y, v in es.items() if int(y) >= 2017) / 1000:.2f}-"
     f"{max(v for y, v in es.items() if int(y) >= 2017) / 1000:.2f}", "kt", EST, "flat since 2017"),
    ("Road transport share 2023 (Eurostat 1A3b1-4)", round(100 * float(sh["2023"]["road_transport_1A3b1-4_t"]) / float(sh["2023"]["total_t"]), 1),
     "%", EST, "ERA: 42.6%"),
    ("National navigation share 2023 (Eurostat 1A3dii)", round(100 * float(sh["2023"]["national_navigation_1A3dii_t"]) / float(sh["2023"]["total_t"]), 1),
     "%", EST, "ERA: 15.5%"),
]
with open(D / "checks.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["check", "value", "unit", "source", "note"])
    w.writerows(out)
for o in out:
    print(o[0], o[1], o[4])
