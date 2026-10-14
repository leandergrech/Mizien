#!/usr/bin/env python3
"""CC-120: test the Malta noise figures in the EP study (PE 783.089) against the EEA report tables.

Reads data/cc-120/ (EEA 'Environmental noise in Europe 2025' tables, corrected online version of 27 Mar 2026, read 14 Oct 2026;
Eurostat demo_pjan 1 Jan 2022, retrieved 14 Oct 2026) and writes data/cc-120/checks.csv.
"""
import csv, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-120"
POP = {r["geo"]: int(r["population_1_jan_2022"]) for r in csv.DictReader(open(D / "population_2022.csv"))}
EXP = {r["geo"]: r for r in csv.DictReader(open(D / "eea_exposure_lden55.csv"))}
H = {}
for r in csv.DictReader(open(D / "eea_health_burden_table.csv")):
    H[(r["basis"], r["geo"])] = {k: int(v) for k, v in r.items() if k not in ("basis", "geo", "country")}
EU = sorted(EXP)
# Figures stated in the study (PE 783.089, sections 2.3 and key findings) and in the Parliament's text
STUDY = {"road_lden": 54000, "air_lden": 11100, "deaths": 20, "dalys100k": 100}
rows = []


def add(check, value, unit, source, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": source, "note": note})


def rank(vals, geo, reverse=False):
    """1 = lowest (or highest when reverse) among the keys of vals; ties share the best rank."""
    v = vals[geo]
    return 1 + sum((x > v) if reverse else (x < v) for x in vals.values())


def n_tied(vals, geo):
    return sum(x == vals[geo] for x in vals.values()) - 1


m = EXP["MT"]
add("Malta road, Lden >= 55 dB (EEA Table 2.1)", int(m["road"]), "people", "EEA 2025 report p. 23", f"study: {STUDY['road_lden']}")
add("Malta aircraft, Lden >= 55 dB (EEA Table 2.1)", int(m["air"]), "people", "EEA 2025 report p. 23", f"study: {STUDY['air_lden']}")
add("Malta road exposure matches study", int(m["road"]) == STUDY["road_lden"] and int(m["air"]) == STUDY["air_lden"], "bool", "calculated")
add("Road / aircraft exposed people", round(int(m["road"]) / int(m["air"]), 1), "ratio", "calculated")
add("Malta population 1 Jan 2022", POP["MT"], "people", "Eurostat demo_pjan")
road_share = {g: int(EXP[g]["road"]) / POP[g] * 100 for g in EU}
add("Malta road Lden>=55 as % of population", round(road_share["MT"], 1), "%", "calculated (EEA count / Eurostat population)")
add("Malta rank by road-exposed share, 1 = lowest of 27", rank(road_share, "MT"), "of 27", "calculated",
    "ordered list: " + ", ".join(f"{g} {road_share[g]:.1f}" for g in sorted(road_share, key=road_share.get)[:5]))
all_pct = {g: int(EXP[g]["pct_of_population_all_sources"]) for g in EU}
add("Malta all-source share above END Lden threshold (EEA, rounded)", all_pct["MT"], "%", "EEA Table 2.1",
    f"EU-27 range {min(all_pct.values())}-{max(all_pct.values())}%; median {sorted(all_pct.values())[13]}%")
# Health burden
for basis, label in (("END", "END thresholds (EEA Table 3.7)"), ("WHO", "WHO levels (EEA Table 3.12)")):
    deaths = {g: H[(basis, g)]["deaths_total"] for g in EU}
    dal = {g: H[(basis, g)]["dalys100k_total"] for g in EU}
    dpc = {g: deaths[g] / POP[g] * 1e5 for g in EU}
    add(f"[{basis}] Malta premature deaths/yr, total", deaths["MT"], "deaths", f"EEA, {label}", f"study states {STUDY['deaths']}" if basis == "END" else "")
    add(f"[{basis}] Malta rank, absolute deaths (1 = lowest of 27)", rank(deaths, "MT"), "of 27", "calculated",
        "next lowest: " + ", ".join(f"{g} {deaths[g]}" for g in sorted(deaths, key=deaths.get)[1:4]))
    add(f"[{basis}] Malta deaths per 100,000 (calculated)", round(dpc["MT"], 1), "per 100,000", "calculated", "EEA count / Eurostat 2022 population")
    add(f"[{basis}] Malta rank, deaths per 100,000 (1 = lowest of 27)", rank(dpc, "MT"), "of 27", "calculated",
        "lowest five: " + ", ".join(f"{g} {dpc[g]:.1f}" for g in sorted(dpc, key=dpc.get)[:5]))
    add(f"[{basis}] Malta DALYs per 100,000, total", dal["MT"], "per 100,000", f"EEA, {label}", f"study states {STUDY['dalys100k']}" if basis == "END" else "")
    r = rank(dal, "MT")
    add(f"[{basis}] Malta rank, DALYs per 100,000 (1 = lowest of 27)", r, "of 27", "calculated",
        f"{n_tied(dal, 'MT')} other country/ies tied at the same value; lowest five: " + ", ".join(f"{g} {dal[g]}" for g in sorted(dal, key=dal.get)[:6]))
    add(f"[{basis}] Countries with lower DALYs per 100,000 than Malta", sum(dal[g] < dal["MT"] for g in EU), "of 26", "calculated")
    add(f"[{basis}] EU-27 median DALYs per 100,000", sorted(dal.values())[13], "per 100,000", "calculated (unweighted median of country values)")
# Study vs corrected EEA
add("Study deaths / EEA corrected deaths (END basis)", f"{STUDY['deaths']} vs {H[('END','MT')]['deaths_total']}", "deaths", "study s. 2.3; EEA Table 3.7",
    "difference consistent with the EEA corrigendum of 27 Mar 2026; June 2025 version not opened")
add("Study DALYs / EEA corrected DALYs (END basis)", f"{STUDY['dalys100k']} vs {H[('END','MT')]['dalys100k_total']}", "per 100,000", "study s. 2.3; EEA Table 3.7", "same")
# Rank is robust to the study's lower figures?
dal_study = {g: H[("END", g)]["dalys100k_total"] for g in EU}; dal_study["MT"] = STUDY["dalys100k"]
add("Malta rank by DALYs if the study's value (100) were used", rank(dal_study, "MT"), "of 27", "calculated", "shows the ranking claim does not depend on the correction")
deaths_s = {g: H[("END", g)]["deaths_total"] for g in EU}; deaths_s["MT"] = STUDY["deaths"]
add("Malta rank by absolute deaths if the study's value (20) were used", rank(deaths_s, "MT"), "of 27", "calculated")
with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for x in rows:
    print(f"{x['check']:68s} {str(x['value']):>12} {x['unit']:12s} {x['note']}")
