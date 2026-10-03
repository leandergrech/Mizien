#!/usr/bin/env python3
"""CC-017: test the Budget 2026 land-reclamation statement with formulas, not by eye.

Reads data/cc-017/ (retrieved 3 Oct 2026) and writes data/cc-017/checks.csv.
"""
import csv, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-017"
L = {r["year"]: float(r["land_ha"]) for r in csv.DictReader(open(D / "s2_land_t2.csv"))}
N = list(csv.DictReader(open(D / "natura2000_near_freeport.csv")))
rows = []


def add(check, value, unit, source, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": source, "note": note})


add("Land in Terminal 2 window, 2017-2023 (mean)", round(sum(L[y] for y in ("2017", "2020", "2023")) / 3, 1), "ha",
    "Sentinel-2")
add("New land at Terminal 2, 2023 -> 2026", round(L["2026"] - L["2023"], 1), "ha", "Sentinel-2",
    "stated: about 3.0 ha (30,000 m2), Malta Freeport Corporation")
add("New land at Terminal 2, 2025 -> 2026", round(L["2026"] - L["2025"], 1), "ha", "Sentinel-2")
add("Fill per hectare of the Terminal 2 reclamation", round(1_000_000 / 3.0), "t/ha", "calculated",
    "about 1 million tonnes of inert material for 30,000 m2 (Malta Freeport Corporation)")
near = [n for n in N if float(n["distance_from_freeport_km"]) <= 1.5]
add("Natura 2000 sites within 1.5 km of the Freeport", len({n["sitecode"] for n in near}), "sites", "EEA Natura 2000",
    "; ".join(f"{n['sitecode']} {n['designation'].split()[0]} {n['distance_from_freeport_km']} km" for n in near))
lbic = next(n for n in N if n["sitecode"] == "MT0000111")
add("Distance to marine SPA Żona fil-Baħar fil-Lbiċ", float(lbic["distance_from_freeport_km"]), "km", "EEA Natura 2000",
    f"{lbic['area_km2']} km2")
add("Land reclamation allocated in budgets 2023 / 2024 / 2025", "500,000 / 100,000 / 10,000", "EUR",
    "MaltaToday analysis, 15 Apr 2025 (second-hand)", "EUR 9,500 spent of the 2023 allocation")
add("Years since the seabed study was said to be the basis for a Cabinet decision", 2026 - 2019, "years", "calculated",
    "MaltaToday, Sep 2019; study not published")

with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\r\n")
    w.writeheader()
    w.writerows(rows)
for x in rows:
    print(f"{x['check']:72s} {str(x['value']):>26} {x['unit']:6s} {x['note']}")
