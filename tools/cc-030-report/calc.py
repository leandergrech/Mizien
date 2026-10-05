#!/usr/bin/env python3
"""CC-030: test the Malta International Airport claims with formulas, not by eye.

Reads data/cc-030/mia_emissions.csv (MIA Sustainability Report 2025 and MIA press release, read 5 Oct 2026) and
writes data/cc-030/checks.csv.
"""
import csv, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-030"
V = {(r["item"], r["year"]): float(r["value"]) for r in csv.DictReader(open(D / "mia_emissions.csv", encoding="utf-8"))}
rows = []


def add(check, value, unit, source, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": source, "note": note})


R = "MIA Sustainability Report 2025"
s1, s2l, s2m = V[("Scope 1 GHG emissions", "2025")], V[("Scope 2 GHG emissions (location based)", "2025")], \
    V[("Scope 2 GHG emissions (market based)", "2025")]
bt, offset = V[("Scope 3 Category 6 business travel", "2025")], V[("Carbon credits purchased for residual emissions", "2025")]
s3 = V[("Scope 3 total", "2025")]
cat11 = V[("Scope 3 Category 11 use of sold products (aircraft incl. APU and GPU)", "2025")]
avoid, cost, grant = V[("Avoided CO2 once operational (average)", "2026")], V[("Airfield electrification programme cost", "2026")], \
    V[("EU AFIF grant", "2026")]
mov, pax = V[("Aircraft movements", "2025")], V[("Passengers", "2025")]

add("Scope 1 + Scope 2 (location) + business travel, 2025", s1 + s2l + bt, "t CO2", R, f"{s1:.0f} + {s2l:.0f} + {bt:.0f}")
add("Same with market-based Scope 2", s1 + s2m + bt, "t CO2", R)
add("Credits purchased vs location-based sum", round(offset - (s1 + s2l + bt)), "t CO2", R, "difference; 0.1% of the credits")
add("Credits purchased vs location-based sum, relative", round(100 * (offset - (s1 + s2l + bt)) / offset, 2), "%", R)
add("Scope 1 + 2 (location), 2025", s1 + s2l, "t CO2", R)
add("Scope 1 + 2 (location), 2015 base year", V[("Scope 1 GHG emissions", "2015")] + V[("Scope 2 GHG emissions (location based)", "2015")],
    "t CO2", R)
b = V[("Scope 1 GHG emissions", "2015")] + V[("Scope 2 GHG emissions (location based)", "2015")]
add("Change in Scope 1 + 2, 2015 to 2025", round(100 * ((s1 + s2l) / b - 1)), "%", R, "company target: -65% by 2030")
add("Change in Scope 1 + 2, 2024 to 2025", round(100 * ((s1 + s2l) / (V[("Scope 1 GHG emissions", "2024")] +
    V[("Scope 2 GHG emissions (location based)", "2024")]) - 1), 1), "%", R)
tot = s1 + s2l + s3
add("Total reported footprint 2025 (Scope 1 + 2 + 3)", round(tot), "t CO2", R)
add("Share of reported footprint that is Scope 3", round(100 * s3 / tot, 1), "%", R)
add("Share of reported footprint covered by the credits", round(100 * offset / tot, 2), "%", R)
add("Scope 1 + 2 + business travel as a share of the credits bought", round(100 * (s1 + s2l + bt) / offset, 1), "%", R)
add("Aircraft use of sold products, share of Scope 3", round(100 * cat11 / s3, 1), "%", R)
add("Scope 3 jump 2024 to 2025", round(100 * (s3 / V[("Scope 3 total", "2024")] - 1)), "%", R,
    "method change: landing/take-off cycle to full flight; not a real 7-fold rise")
add("Programme avoided CO2 vs Scope 1 + 2 2025", round(100 * avoid / (s1 + s2l), 1), "%", "press release; " + R)
add("Programme avoided CO2 vs Scope 3 2025", round(100 * avoid / s3, 2), "%", "press release; " + R)
add("Programme avoided CO2 vs aircraft emissions 2025", round(100 * avoid / cat11, 2), "%", "press release; " + R)
add("Programme avoided CO2 vs credits purchased", round(100 * avoid / offset, 1), "%", "press release; " + R)
add("EU grant share of programme cost", round(100 * grant / cost, 1), "%", "press release")
add("Cost per tonne avoided per year (EUR)", round(cost * 1e6 / avoid), "EUR", "press release", "gross; over 10 years ~EUR 1,250 / t")
turn = mov / 2
add("Turnarounds a year (movements / 2)", round(turn), "turnarounds", "second-hand movements", "65,470 / 2")
add("Avoided CO2 per turnaround if spread over every turnaround", round(1e6 * avoid / turn / 1000, 1), "kg CO2", "calculated",
    "30.5 kg; not every turnaround will use a hatch pit")
for kg in (40, 60, 90):
    add(f"GPU-hours a year needed to avoid 1,000 t at {kg} kg CO2 per GPU-hour", round(avoid * 1000 / kg), "hours", "calculated",
        f"{avoid*1000/kg/turn*60:.0f} min per turnaround if all turnarounds; kg/h is an assumption, not a sourced figure")
add("Scope 2 grid factor (Enemalta residual mix)", V[("Scope 2 emission factor (Enemalta residual mix)", "2025")],
    "kg CO2/kWh", R, "electricity supplied to aircraft would add emissions at about this rate")
add("Intensity Scope 1 + 2 per passenger, 2025", round(1000 * (s1 + s2l) / pax, 3), "kg CO2/pax", R, "company reports 0.54")

with open(D / "checks.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
for r in rows:
    print(f"{r['check']:72s} {r['value']:>10} {r['unit']:12s} {r['note']}")
