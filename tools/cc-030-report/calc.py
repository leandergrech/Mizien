#!/usr/bin/env python3
"""CC-030: test the Malta International Airport claims with formulas, not by eye.

Reads data/cc-030/mia_emissions.csv (MIA Sustainability Report 2025, press release, traffic announcement, CINEA list),
data/cc-030/ground_power_inputs.csv (Padhra 2018, IPCC 2006 defaults, MIA's own factors) and
data/cc-030/independent_records.csv (ACA and registry records), all retrieved 5 Oct 2026, and writes
data/cc-030/checks.csv.
"""
import csv
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-030"
V = {(r["item"], r["year"]): float(r["value"]) for r in csv.DictReader(open(D / "mia_emissions.csv", encoding="utf-8"))}
G = {r["item"]: float(r["value"]) for r in csv.DictReader(open(D / "ground_power_inputs.csv", encoding="utf-8"))}
rows = []


def add(check, value, unit, source, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": source, "note": note})


R = "MIA Sustainability Report 2025"
P = "Padhra (2018) accepted manuscript"
s1 = {y: V[("Scope 1 GHG emissions", y)] for y in ("2015", "2024", "2025")}
s2l = {y: V[("Scope 2 GHG emissions (location based)", y)] for y in ("2015", "2024", "2025")}
s2m = {y: V[("Scope 2 GHG emissions (market based)", y)] for y in ("2024", "2025")}
bt = {y: V[("Scope 3 Category 6 business travel", y)] for y in ("2024", "2025")}
s3 = {y: V[("Scope 3 total", y)] for y in ("2024", "2025")}
cat11 = V[("Scope 3 Category 11 use of sold products (mostly aircraft)", "2025")]
offset = V[("Carbon credits purchased for residual emissions", "2025")]
avoid = V[("Avoided CO2 once operational (average)", "2026")]
cost, grant = V[("Airfield electrification programme cost", "2026")], V[("EU AFIF grant", "2026")]
eligible = V[("AFIF recommended eligible costs", "2026")]
mov, pax = V[("Aircraft movements", "2025")], V[("Passengers", "2025")]

# ---------------------------------------------------------------- A. neutrality: the ACA boundary against the credits
loc25, mkt25 = s1["2025"] + s2l["2025"] + bt["2025"], s1["2025"] + s2m["2025"] + bt["2025"]
loc24, mkt24 = s1["2024"] + s2l["2024"] + bt["2024"], s1["2024"] + s2m["2024"] + bt["2024"]
add("ACA boundary 2025: Scope 1 + Scope 2 (location) + business travel", loc25, "t CO2", R,
    f"{s1['2025']:.0f} + {s2l['2025']:.0f} + {bt['2025']:.0f}")
add("ACA boundary 2025 with market-based Scope 2", mkt25, "t CO2", R,
    f"{s1['2025']:.0f} + {s2m['2025']:.0f} + {bt['2025']:.0f}")
add("ACA boundary 2024: Scope 1 + Scope 2 (location) + business travel", loc24, "t CO2", R,
    "ACA's notice says 2024 residual emissions were offset")
add("ACA boundary 2024 with market-based Scope 2", mkt24, "t CO2", R)
add("Credits minus 2025 boundary (location based)", offset - loc25, "t CO2", R, "credits cover it")
add("Credits minus 2025 boundary (market based)", offset - mkt25, "t CO2", R, "negative: credits fall short")
add("Credits minus 2024 boundary (location / market based)", f"{offset - loc24:.0f} / {offset - mkt24:.0f}", "t CO2", R,
    "credits exceed the 2024 boundary on either basis")
found = 1620 + 2160
add("Credits found retired for MIA in public registries", found, "t CO2",
    "Gold Standard block 585497 (1,620 t); Rainbow transaction 9e16ced5 (2,160 t)",
    "both retired 4 Jun 2026; Canada block (1,670 t) not found")
add("Share of the 5,450 t found retired", round(100 * found / offset, 1), "%", "registries; " + R)

# ---------------------------------------------------------------- D. how large the boundary is
tot = s1["2025"] + s2l["2025"] + s3["2025"]
tot24 = s1["2024"] + s2l["2024"] + s3["2024"]
add("Total reported footprint 2025 (Scope 1 + 2 location + 3)", round(tot), "t CO2", R)
add("Share of reported footprint that is Scope 3, 2025", round(100 * s3["2025"] / tot, 1), "%", R,
    "full-flight aircraft accounting from 2025")
add("Share of reported footprint that is Scope 3, 2024 (landing and take-off basis)",
    round(100 * s3["2024"] / tot24, 1), "%", R, "the point stands on either basis")
add("ACA boundary (location) as a share of the 2025 footprint", round(100 * loc25 / tot, 2), "%", R)
add("Share of footprint outside the ACA boundary, 2025", round(100 * (1 - loc25 / tot), 1), "%", R)
add("Credits as a share of the 2025 footprint", round(100 * offset / tot, 2), "%", R)
add("Scope 3 other than use of sold products and business travel, 2025", s3["2025"] - cat11 - bt["2025"], "t CO2", R)
add("Use of sold products (mostly aircraft), share of Scope 3", round(100 * cat11 / s3["2025"], 1), "%", R,
    "category also holds tenants' Scope 1 and passengers' landside traffic (pp.96-97)")
add("Scope 3 jump 2024 to 2025", round(100 * (s3["2025"] / s3["2024"] - 1)), "%", R,
    "method change: landing/take-off cycle to full flight; not a real 7-fold rise")

# ---------------------------------------------------------------- direct emissions over time
b15 = s1["2015"] + s2l["2015"]
for y in ("2024", "2025"):
    add(f"Scope 1 + 2 (location), {y}", s1[y] + s2l[y], "t CO2", R)
    add(f"Change in Scope 1 + 2, 2015 to {y}", round(100 * ((s1[y] + s2l[y]) / b15 - 1), 1), "%", R,
        "MIA elsewhere: -31% (2023, Net Zero Carbon Plan), -32% (ACA notice)")
add("Change in Scope 1 + 2, 2024 to 2025",
    round(100 * ((s1["2025"] + s2l["2025"]) / (s1["2024"] + s2l["2024"]) - 1), 1), "%", R)
target = b15 * (1 - V[("Company target for Scope 1 + 2: reduction by 2030 against 2015", "2030")] / 100)
add("Scope 1 + 2 level implied by -65% by 2030", round(target), "t CO2", "Net Zero Carbon Plan; " + R)
add("Cut still needed from 2025 to reach it", round(s1["2025"] + s2l["2025"] - target), "t CO2", "calculated",
    f"{100 * (1 - target / (s1['2025'] + s2l['2025'])):.0f}% of the 2025 level")
add("Change in Scope 1, 2024 to 2025", round(100 * (s1["2025"] / s1["2024"] - 1)), "%", R)
f24, f25 = V[("Fuel consumption (diesel + petrol + LPG)", "2024")], V[("Fuel consumption (diesel + petrol + LPG)", "2025")]
add("Change in fuel use (GRI 103), 2024 to 2025", round(100 * (f25 / f24 - 1)), "%", R, f"{f24:.0f} to {f25:.0f} MWh")
fuel_co2 = (V[("Diesel consumed", "2025")] * V[("Scope 1 factor used by MIA: diesel", "2025")] +
            V[("Petrol consumed", "2025")] * V[("Scope 1 factor used by MIA: petrol", "2025")] +
            V[("LPG consumed", "2025")] * V[("Scope 1 factor used by MIA: LPG and propane", "2025")]) / 1000
add("Fuel CO2 2025 from the report's litres and its own factors", round(fuel_co2), "t CO2", R + " pp.29, 90-91",
    f"{100 * fuel_co2 / s1['2025']:.0f}% of the reported Scope 1 ({s1['2025']:.0f} t); remainder not broken down")

# ---------------------------------------------------------------- B. the programme
add("EU grant share of programme cost", round(100 * grant / cost, 1), "%", "CINEA; press release")
add("EU grant share of AFIF eligible costs", round(100 * grant / eligible, 1), "%", "CINEA")
add("Programme avoided CO2 vs Scope 1 + 2 2025", round(100 * avoid / (s1["2025"] + s2l["2025"]), 1), "%",
    "press release; " + R)
add("Programme avoided CO2 vs Scope 3 2025", round(100 * avoid / s3["2025"], 2), "%", "press release; " + R)

# ---------------------------------------------------------------- C. what 1,000 t a year would require
turn = mov / 2
ef_diesel = G["Diesel (gas/diesel oil) CO2 emission factor"] * G["Diesel (gas/diesel oil) net calorific value"] / 1e6
gpu = G["Mobile diesel GPU fuel consumption (Zurich Airport average 2004)"] * ef_diesel
apu = G["APU fuel flow in single-cycle events (duration-weighted average)"] * G["Jet A-1 CO2 factor used by MIA for aircraft and APU"]
dur = G["APU switched off between arrival and departure when external power was used (double-cycle events)"]
add("Turnarounds a year (movements / 2)", round(turn), "turnarounds", "MIA announcement 461/2026", "65,470 / 2")
add("Avoided CO2 per turnaround if spread over every turnaround", round(1000 * avoid / turn, 1), "kg CO2", "calculated")
add("Diesel CO2 factor (IPCC 2006 default)", round(ef_diesel, 3), "kg CO2 per kg", "IPCC 2006", "74,100 kg/TJ x 43.0 TJ/Gg")
add("Diesel GPU CO2 per hour", round(gpu, 1), "kg CO2/h", P + " (Fleuti 2006, second-hand); IPCC 2006",
    "7.74 kg diesel/h; indicative")
add("APU CO2 per hour", round(apu), "kg CO2/h", P + "; MIA Jet A-1 factor", "103.2 kg fuel/h x 3.163")
gh = 1000 * avoid / gpu
add("Diesel GPU-hours replaced to avoid 1,000 t (gross)", round(gh, -2), "hours", "calculated", f"{gh:,.0f}")
add("Minutes of diesel GPU per turnaround for 1,000 t, every turnaround", round(60 * gh / turn, 1), "minutes",
    "calculated", f"against {dur:.1f} min of external power per turnaround in Padhra's sample")
gross = gpu * dur / 60 * turn / 1000
add("Gross diesel GPU CO2 if every turnaround used one for 22.5 minutes", round(gross), "t CO2 a year", "calculated",
    f"{gpu * dur / 60:.1f} kg per turnaround; before subtracting grid electricity")
add("Diesel GPU share of the claimed 1,000 t on that basis", round(100 * gross / avoid), "%", "calculated")
ah = 1000 * avoid / apu
add("APU-hours avoided for 1,000 t", round(ah), "hours", "calculated")
add("Minutes of APU running avoided per turnaround for 1,000 t, every turnaround", round(60 * ah / turn, 1),
    "minutes", "calculated")
add("Minutes of APU avoided per turnaround to cover the rest after the 22.5-minute GPU case",
    round(60 * (1000 * avoid - 1000 * gross) / apu / turn, 1), "minutes", "calculated",
    "or electric bus and ground-equipment savings, which MIA has not quantified")
add("Grid electricity factor (MIA, Enemalta residual mix)", G["Malta grid electricity factor used by MIA (Enemalta residual mix)"],
    "kg CO2/kWh", R, "grid power supplied in place of diesel adds emissions at this rate, so net < gross")
add("Intensity Scope 1 + 2 per passenger, 2025", round(1000 * (s1["2025"] + s2l["2025"]) / pax, 3), "kg CO2/pax", R,
    "company reports 0.54")

with open(D / "checks.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
for r in rows:
    print(f"{r['check'][:84]:84s} {str(r['value']):>12} {r['unit']:14s} {r['note']}")
