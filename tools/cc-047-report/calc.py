#!/usr/bin/env python3
"""CC-047: test the arithmetic and the independent monitoring data behind "100-200 mg/L ... two to four times the EU limit".
Reads data/cc-047/*.csv; writes data/cc-047/checks.csv."""
import csv, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-047"
C = {r["item"]: float(r["value"]) for r in csv.DictReader(open(D / "commission_nitrates_malta_2020_2023.csv"))}
LIMIT = 50.0
rows = []


def add(check, value, unit, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "note": note})


n = C["groundwater_monitoring_points"]
add("100 mg/L as multiple of the 50 mg/L limit", 100 / LIMIT, "x", "claim: two times")
add("200 mg/L as multiple of the 50 mg/L limit", 200 / LIMIT, "x", "claim: four times")
for k, lab in [("share_ge_50", ">=50"), ("share_40_49.99", "40-49.99"), ("share_25_39.99", "25-39.99"), ("share_lt_25", "<25")]:
    add(f"Points with average {lab} mg/L implied (share x 44)", round(C[k] / 100 * n, 2), "points", "integer expected")
add("Shares sum", round(C["share_ge_50"] + C["share_40_49.99"] + C["share_25_39.99"] + C["share_lt_25"], 1), "%")
add("Hotspots / points", round(C["pollution_hotspots"] / n * 100, 1), "%", "Commission: 79.5% at NUTS2")
add("Previous period >=50 implied points", round(C["share_ge_50_previous_period_2016_2019"] / 100 * n, 2), "points")
w = sum(C[f"{p}_stations"] * C[f"{p}_share_ge_50"] / 100 for p in ["phreatic_5_15m", "phreatic_15_30m", "phreatic_gt30m"])
add("Points >=50 summed from Table 4 by depth class", round(w, 1), "points", "should equal 30")
with open(D / "checks.csv", "w", newline="") as f:
    wr = csv.DictWriter(f, fieldnames=list(rows[0]))
    wr.writeheader()
    wr.writerows(rows)
for r in rows:
    print(f"{r['check'][:70]:70s} {r['value']:>8} {r['unit']} {r['note']}")
