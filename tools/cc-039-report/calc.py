#!/usr/bin/env python3
"""CC-039: test WSC's 2019 statement that the Net Zero Impact Utility project cuts groundwater abstraction by
4 billion litres a year, and the 'no net increase in energy' reading, against WSC production data.
Inputs: data/cc-039/inputs.csv, data/cc-039/eurostat_pws_groundwater.csv. Output: data/cc-039/checks.csv"""
import csv, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-039"
inp = {r["id"]: float(r["value"]) for r in csv.DictReader(open(D / "inputs.csv", encoding="utf-8"))}
eu = {(r["series"], int(r["year"])): float(r["value_million_m3"]) for r in csv.DictReader(open(D / "eurostat_pws_groundwater.csv"))}
M = 1e6
target = inp["pledge_litres"] / 1000 / M  # million m3
rows = []
def add(check, value, unit, source, note=""):
    rows.append([check, round(value, 3), unit, source, note])

add("Pledged cut", target, "million m3 a year", "WSC 2 Apr 2019", "4 billion litres = 4.0 million m3")
gw16 = inp["gw_m3_2016"] / M
for y in (2022, 2023, 2024, 2025):
    gw = inp[f"gw_m3_{y}"] / M
    add(f"WSC groundwater production {y}", gw, "million m3", "WSC AR 2016, AR 2025 Fig 20")
    add(f"Change vs 2016 ({gw16:.3f})", gw - gw16, "million m3", "calculated")
    add(f"Change vs 2016 as share of the 4.0 pledged", (gw16 - gw) / target * 100, "%", "calculated", "positive = fall")
add("WSC groundwater production 2016", gw16, "million m3", "WSC AR 2016 p.10")
add("Groundwater needed for the full cut from 2016 level", gw16 - target, "million m3", "calculated")
add("Pledged cut as share of 2016 WSC groundwater production", target / gw16 * 100, "%", "calculated")
tot16 = (inp["ro_m3_2016"] + inp["gw_m3_2016"]) / M
tot25 = (inp["ro_m3_2025"] + inp["gw_m3_2025"]) / M
add("WSC total potable production 2016", tot16, "million m3", "WSC AR 2016")
add("WSC total potable production 2025", tot25, "million m3", "WSC AR 2025")
add("Growth in total production 2016-2025", (tot25 / tot16 - 1) * 100, "%", "calculated")
add("Groundwater share of production 2016", gw16 / tot16 * 100, "%", "calculated")
add("Groundwater share of production 2025", inp["gw_m3_2025"] / M / tot25 * 100, "%", "calculated")
# Eurostat public water supply groundwater
for y in (2018, 2019, 2024):
    add(f"Eurostat public-supply groundwater abstraction {y}", eu[("public water supply", y)], "million m3", "Eurostat env_wat_abs", "flag e (estimated)")
for base in (2018, 2019):
    d = eu[("public water supply", 2024)] - eu[("public water supply", base)]
    add(f"Eurostat public-supply change {base} to 2024", d, "million m3", "calculated", f"{d / eu[('public water supply', base)] * 100:.1f}%")
    add(f"  as share of the 4.0 pledged", -d / target * 100, "%", "calculated")
nat24 = eu[("all sectors", 2024)]
add("Pledged cut as share of national fresh groundwater abstraction 2024", target / nat24 * 100, "%", "calculated", f"national total {nat24} million m3 (estimated)")
# energy
ro16, ro25 = inp["ro_m3_2016"] / M, inp["ro_m3_2025"] / M
ro24 = inp["ro_m3_2024"] / M
add("RO production 2016", ro16, "million m3", "WSC AR 2016")
add("RO production 2025", ro25, "million m3", "WSC AR 2025 Fig 20")
add("RO production growth 2016-2025", (ro25 / ro16 - 1) * 100, "%", "calculated")
e16 = ro16 * inp["spec_kwh_2016"]
add("RO electricity 2016", e16, "GWh", "calculated", "2016 volume x 4.85 kWh/m3 (WSC AR 2016)")
add("RO electricity 2025 at the 2016 specific energy", ro25 * inp["spec_kwh_2016"], "GWh", "calculated", "scenario, not a measurement")
add("Increase at the 2016 specific energy", (ro25 / ro16 - 1) * 100, "%", "calculated")
add("Specific energy needed in 2025 to keep RO electricity at the 2016 level", e16 / ro25, "kWh/m3", "calculated")
add("  fall from 4.85 that this would take", (1 - e16 / ro25 / inp["spec_kwh_2016"]) * 100, "%", "calculated")
add("Specific energy needed in 2024 to keep RO electricity at the 2016 level", e16 / ro24, "kWh/m3", "calculated")
add("RO electricity share of 2016 electricity bill", 10082017 / inp["elec_eur_2016"] * 100, "%", "WSC AR 2016 note 2", "nominal euro")
# Whole-utility indicator, WSC Impact and Allocation Report FY2024 p.13 (read first-hand 6 Oct 2026).
# Not an RO figure: 'Total Energy Requirement per m3 produced'; the report does not define its boundary.
for y in (2022, 2023, 2024):
    k = inp[f"wsc_total_kwh_m3_{y}"]
    prod = (inp[f"gw_m3_{y}"] + inp[f"ro_m3_{y}"]) / M
    add(f"WSC total energy requirement per m3 produced {y}", k, "kWh/m3", "WSC Impact and Allocation Report FY2024 p.13", "whole-utility indicator; boundary not defined")
    add(f"WSC potable production {y}", prod, "million m3", "WSC AR 2025 Fig 20 (groundwater + RO)")
    add(f"Implied total energy {y} (indicative)", k * prod, "GWh", "calculated", "intensity x production; assumes 'produced' = potable production in Fig 20; boundary unverified")
add("Change in implied total energy 2022 to 2024 (indicative)", ((inp["wsc_total_kwh_m3_2024"] * (inp["gw_m3_2024"] + inp["ro_m3_2024"])) / (inp["wsc_total_kwh_m3_2022"] * (inp["gw_m3_2022"] + inp["ro_m3_2022"])) - 1) * 100, "%", "calculated", "indicative only")
add("Change in total energy per m3 produced 2022 to 2024", (inp["wsc_total_kwh_m3_2024"] / inp["wsc_total_kwh_m3_2022"] - 1) * 100, "%", "calculated")
add("Hondoq RO specific energy 2024", inp["hondoq_kwh_m3_2024"], "kWh/m3", "WSC Impact and Allocation Report FY2024 p.24, p.28", "2021 pre-commissioning baseline 4.1")
with open(D / "checks.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n"); w.writerow(["check", "value", "unit", "source", "note"]); w.writerows(rows)
for r in rows: print(r)
