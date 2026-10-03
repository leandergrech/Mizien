#!/usr/bin/env python3
"""CC-012: seasonal greenness of the Ta' Qali gravel zone against the rest of the park.

Reads data/cc-012/ndvi_timeseries.csv (written by fetch_s2.py) and writes data/cc-012/checks.csv.
Seasons: winter = December to March (labelled by the year it ends), summer = June to September.
"""
import csv, json, pathlib
from statistics import median

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-012"
T = list(csv.DictReader(open(D / "ndvi_timeseries.csv")))
Z = json.load(open(D / "gravel_zone.geojson"))["properties"]
rows = []


def add(check, value, unit, source, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": source, "note": note})


S2 = "Sentinel-2 L2A (Copernicus) via Planetary Computer; data/cc-012/ndvi_timeseries.csv"
add("Gravel zone area (brightening Aug-Sep 2025 vs 2024, inside OSM park polygon)", Z["area_m2"], "m2",
    "data/cc-012/gravel_zone.geojson", "Momentum's inspection reported about 22,000 m2")


def season(r):
    y, m = int(r["date"][:4]), int(r["date"][5:7])
    if m in (12, 1, 2, 3):
        return f"winter {y if m != 12 else y + 1}"
    if m in (6, 7, 8, 9):
        return f"summer {y}"
    return None


seasons = {}
for r in T:
    s = season(r)
    if s:
        seasons.setdefault(s, []).append(r)
for s in sorted(seasons, key=lambda s: (s.split()[1], s)):
    rs = seasons[s]
    z = median(float(r["ndvi_gravel_zone"]) for r in rs)
    c = median(float(r["ndvi_control"]) for r in rs)
    add(f"{s}: NDVI gravel zone / rest of park", f"{z:.2f} / {c:.2f}", "NDVI", S2, f"{len(rs)} scenes; ratio {z / c:.2f}")
pre = [float(r["ndvi_gravel_zone"]) / float(r["ndvi_control"]) for r in T
       if season(r) and season(r).startswith("winter") and r["date"] < "2025-06-01"]
post = [float(r["ndvi_gravel_zone"]) / float(r["ndvi_control"]) for r in T
        if season(r) and season(r).startswith("winter") and r["date"] > "2025-10-01"]
add("Winter ratio zone/rest of park, before gravel (2023-2025)", round(median(pre), 2), "ratio", S2, f"{len(pre)} scenes")
add("Winter ratio zone/rest of park, after gravel (2025-26)", round(median(post), 2), "ratio", S2, f"{len(post)} scenes")
bz = lambda a, b: median(float(r["brightness_gravel_zone"]) for r in T if a <= r["date"] <= b)
add("Brightness in zone, May 2025 -> Aug 2025", f"{bz('2025-05-01', '2025-05-31'):.0f} -> {bz('2025-08-01', '2025-08-31'):.0f}",
    "reflectance x 10^4", S2, "gravel laid June 2025")
last = T[-1]
add("Latest clear scene", last["date"], "date", S2,
    f"NDVI zone {float(last['ndvi_gravel_zone']):.2f} vs rest {float(last['ndvi_control']):.2f}; "
    f"brightness {last['brightness_gravel_zone']} vs {last['brightness_control']}")
add("Brightness in zone, Aug-Sep 2026 median", round(bz("2026-08-01", "2026-09-30")), "reflectance x 10^4", S2,
    "no return to pre-gravel levels (about 2,000-3,000) by end of September 2026")

with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
for r in rows:
    print(f"{r['check']:72s} {str(r['value']):>14} {r['unit']:8s} {r['note']}")
