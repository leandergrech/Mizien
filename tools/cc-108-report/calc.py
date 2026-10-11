#!/usr/bin/env python3
"""CC-108: test the Green Paper's statements (EWA, Nov 2023) that WSC's groundwater abstraction is capped at 14 million m3
a year up to 2030 and that WSC is 'moving towards' a net-zero impact on the groundwater environment.
Inputs: data/cc-108/inputs.csv. Output: data/cc-108/checks.csv"""
import csv, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-108"
inp = {r["id"]: float(r["value"]) for r in csv.DictReader(open(D / "inputs.csv", encoding="utf-8"))}
cap = inp["cap_mm3"]
rows = []
def add(check, value, unit, source, note=""):
    rows.append([check, round(value, 3), unit, source, note])

add("Proposed WSC cap to 2030", cap, "million m3 a year", "Green Paper p.12")
years = (2016, 2022, 2023, 2024, 2025)
for y in years:
    g = inp[f"gw_{y}"]
    add(f"WSC groundwater production {y}", g, "million m3", "WSC AR 2016; AR 2025 Fig 20")
    add(f"  as share of the cap {y}", g / cap * 100, "%", "calculated")
    add(f"  headroom under the cap {y}", cap - g, "million m3", "calculated")
mx = max(inp[f"gw_{y}"] for y in years)
add("Highest year read (2016, 2022-25)", mx, "million m3", "calculated")
add("Cap above the highest year read", (cap / mx - 1) * 100, "%", "calculated")
add("Cap above 2025 production", (cap / inp["gw_2025"] - 1) * 100, "%", "calculated")
add("Change in WSC production 2016 to 2025", inp["gw_2025"] - inp["gw_2016"], "million m3", "calculated")
add("  as % of 2016", (inp["gw_2025"] / inp["gw_2016"] - 1) * 100, "%", "calculated")
add("Change in WSC production 2022 to 2025", inp["gw_2025"] - inp["gw_2022"], "million m3", "calculated")
add("  as % of 2022", (inp["gw_2025"] / inp["gw_2022"] - 1) * 100, "%", "calculated")
add("Eurostat public-supply groundwater 2024", inp["pws_gw_2024"], "million m3", "Eurostat env_wat_abs", "flag e")
add("Eurostat public-supply 2024 above the cap", inp["pws_gw_2024"] - cap, "million m3", "calculated", "different measure from WSC production; not the capped quantity")
add("Eurostat public-supply 2024 minus WSC production 2024", inp["pws_gw_2024"] - inp["gw_2024"], "million m3", "calculated")
add("WSC production as share of national fresh groundwater abstraction 2024", inp["gw_2024"] / inp["nat_gw_2024"] * 100, "%", "calculated", "national total 38.46 (estimated)")
add("National abstraction as share of estimated recharge 2024", inp["nat_gw_2024"] / inp["recharge_2024"] * 100, "%", "calculated", "both estimates")
# give-back arithmetic (Sapiano's definition: aquifer recharge plus treated wastewater used in place of groundwater)
add("New Water produced 2022 as share of WSC groundwater production 2022", inp["newwater_2022"] / inp["gw_2022"] * 100, "%", "calculated", "if all counted as give-back; it substitutes farmers' groundwater, not WSC's")
add("New Water target (7.0) as share of WSC groundwater production 2025", inp["newwater_target"] / inp["gw_2025"] * 100, "%", "calculated", "even at the stated maximum, below 100% before any recharge")
add("New Water target as share of WSC production 2022", inp["newwater_target"] / inp["gw_2022"] * 100, "%", "calculated")
add("New Water 2022 as share of the 7.0 maximum", inp["newwater_2022"] / inp["newwater_target"] * 100, "%", "calculated")
add("Give-back shortfall at 7.0 maximum, 2025", inp["gw_2025"] - inp["newwater_target"], "million m3", "calculated", "volume of abstraction not matched by New Water even at the maximum")
with open(D / "checks.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n"); w.writerow(["check", "value", "unit", "source", "note"]); w.writerows(rows)
for r in rows: print(r)
