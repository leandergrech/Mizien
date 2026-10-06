#!/usr/bin/env python3
"""CC-032: test the solar-flower figures with formulas, not by eye.

Reads data/cc-032/inputs.csv (transcribed inputs, each with its source), data/cc-032/pvgis_monthly.csv (PVGIS 5.3,
JRC) and data/cc-032/route_osrm.csv (OpenStreetMap via OSRM), all retrieved 6 Oct 2026 (run fetch.py first), and
writes data/cc-032/checks.csv.
"""
import csv
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-032"
I = {r["item"]: r for r in csv.DictReader(open(D / "inputs.csv", encoding="utf-8"))}
v = lambda k: float(I[k]["value"])
PV = {(r["system"], r["month"]): float(r["E_d_kWh"]) for r in csv.DictReader(open(D / "pvgis_monthly.csv", encoding="utf-8"))}
PVY = {r["system"]: float(r["E_m_kWh"]) for r in csv.DictReader(open(D / "pvgis_monthly.csv", encoding="utf-8"))
       if r["month"] == "year"}
ROUTE = [float(r["distance_m"]) for r in csv.DictReader(open(D / "route_osrm.csv", encoding="utf-8"))]
rows = []


def add(check, value, unit, source, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": source, "note": note})


n, kwp = v("Solar flowers installed at Ta' Xħajma"), v("Nominal output per SmartFlower")
cap = n * kwp
add("Installed capacity if each unit is the 2.5 kWp model", cap, "kWp", "data sheet; pv magazine 2024",
    f"{n:.0f} x {kwp}; the Gozo capacity is not published")

# ---------------------------------------------------------------- output (PVGIS, two-axis vs optimal fixed)
y2, yf = PVY["two_axis"], PVY["fixed_optimal"]
add("Modelled yearly output, two-axis tracking, 37.5 kWp", round(y2), "kWh a year", "PVGIS 5.3 (SARAH3, 2005-2023)",
    "14% system loss (PVGIS default)")
add("Modelled yearly output per unit", round(y2 / n), "kWh a year", "PVGIS 5.3",
    "manufacturer's range 4,000-6,500 kWh per unit")
add("Modelled specific yield, two-axis", round(y2 / cap), "kWh per kWp a year", "PVGIS 5.3")
add("Modelled yearly output, same capacity fixed at the optimal angle", round(yf), "kWh a year", "PVGIS 5.3",
    "optimal tilt 32 degrees, azimuth 3 degrees")
gain = 100 * (y2 / yf - 1)
add("Tracking gain over an optimally tilted fixed array at the site", round(gain, 1), "%", "PVGIS 5.3",
    "statement: 'up to 40%'; Bahrami et al. 2016: 17.7-31.2% across Europe and Africa (irradiation)")
lo, hi = v("Manufacturer's yearly output per unit (low)"), v("Manufacturer's yearly output per unit (high)")
add("Manufacturer's range for 15 units", f"{n * lo:,.0f}-{n * hi:,.0f}", "kWh a year", "data sheet Rev G (2019)")
day = PV[("two_axis", "year")]
dec, jul = PV[("two_axis", "12")], PV[("two_axis", "7")]
add("Modelled average output a day, two-axis", day, "kWh a day", "PVGIS 5.3")
add("Modelled output a day, December / July", f"{dec} / {jul}", "kWh a day", "PVGIS 5.3", "lowest / highest month")

# ---------------------------------------------------------------- scale check against the Park and Ride shuttle
rt = sum(ROUTE) / 1000
head = v("Park and Ride shuttle headway")
km_h = 60 / head * rt
add("Shuttle round trip, Park and Ride - Mġarr ferry terminal - Park and Ride", round(rt, 2), "km", "OSRM (OpenStreetMap)",
    f"{ROUTE[0]:.0f} m + {ROUTE[1]:.0f} m, car routing")
add("Shuttle distance per hour of service every 10 minutes", round(km_h, 1), "km per hour of service",
    "GRDA (headway); OSRM", "six round trips an hour; operating hours not published")
cons = {"1.45 (simulated WLTP cycle, Li et al. 2025)": v("Electric bus consumption (simulated WLTP Class 2 cycle)"),
        "1.8 (modelled route, off-peak, Czapla and Sierpinski 2023)": v("Electric bus consumption (modelled urban route; off-peak)"),
        "2.1 (modelled route, peak, Czapla and Sierpinski 2023)": v("Electric bus consumption (modelled urban route; peak)")}
for lab, c in cons.items():
    e = km_h * c
    add(f"Energy per hour of 10-minute service at {lab} kWh/km", round(e, 1), "kWh per hour of service",
        "calculated; indicative", "consumption from other routes and buses, not Gozo data")
    add(f"Hours of 10-minute service the flowers' average day equals, at {lab.split(' ')[0]} kWh/km", round(day / e, 1),
        "hours a day", "calculated; indicative", f"December {dec / e:.1f} h, July {jul / e:.1f} h")
    add(f"Bus-km the flowers' average day equals, at {lab.split(' ')[0]} kWh/km", round(day / c), "km a day",
        "calculated; indicative", "Malta Public Transport gives a range of up to 300 km per charge")

# ---------------------------------------------------------------- cost and EU funding
stated, pq, ted = v("Cost stated by the Government"), v("Cost given in reply to a parliamentary question (excl. VAT)"), \
    v("Award value of TED notice 742398-2024 (CT3013/2024 dual axis solar PV system for the Public Works Department)")
vat = v("Malta standard VAT rate (1 July 2025)") / 100
add("PQ figure plus VAT at 18%", round(pq * (1 + vat), 2), "EUR", "Newsbook (second-hand); EPRS",
    "against 'about EUR 850,000'")
add("TED award value plus VAT at 18%", round(ted * (1 + vat), 2), "EUR", "TED 742398-2024 (our identification); EPRS",
    "against 'about EUR 850,000'")
add("Difference between TED award value and PQ figure", round(ted - pq, 2), "EUR", "calculated", "reason not stated")
add("Stated cost per flower", round(stated / n), "EUR", "TVM News; EC page")
add("PQ cost per flower, excl. VAT", round(pq / n), "EUR", "Newsbook (second-hand)")
add("Share of the RRF C1-I5 target (143 kWp) if 37.5 kWp", round(100 * cap / v("RRF measure C1-I5 target: installed PV in public spaces"), 1),
    "%", "Council 11894/26 ADD 1", "the target counts kWp installed, not energy")

with open(D / "checks.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
for r in rows:
    print(f"{r['check'][:96]:96s} {str(r['value']):>18} {r['unit']:24s} {r['note']}")
