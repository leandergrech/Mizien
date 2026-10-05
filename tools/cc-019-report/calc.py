#!/usr/bin/env python3
"""CC-019: test Amphora Media's 'Green to Grey' figures with formulas, not by eye.

Reads data/cc-019/ and docs/data/geo.json (island areas, OpenStreetMap); writes data/cc-019/checks.csv.
"""
import csv, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-019"
A = {r["item"]: float(r["value"]) for r in csv.DictReader(open(D / "amphora_figures.csv"))}
C = {r["rule"]: r for r in csv.DictReader(open(D / "io_lulc_change.csv"))}
ISL = {i["name"]: i["area_m2"] for i in json.load(open(ROOT / "docs" / "data" / "geo.json"))["islands"]}
rows = []


def add(check, value, unit, source, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": source, "note": note})


lost = A["Green land built up 2018-2023"]
land = ISL["Malta"] + ISL["Gozo"] + ISL["Comino"] + ISL["Cominotto"] + ISL["Filfla"] + ISL["St Paul's Islands"] + ISL["Manoel Island"]
add("Malta's land area (OSM outlines)", round(land / 1e6, 1), "km2", "OpenStreetMap via geo.json")
add("830,000 m2 as a share of the land area", round(100 * lost / land, 3), "%", "calculated", "Amphora: 0.26%")
add("830,000 m2 in FIFA pitches (105 x 68 m)", round(lost / (105 * 68)), "pitches", "calculated", "Amphora: 116")
add("830,000 m2 vs Comino (OSM outline)", round(lost / ISL["Comino"], 2), "x Comino", "calculated",
    f"Comino {ISL['Comino'] / 1e6:.2f} km2 in OSM; Amphora: roughly a quarter")
add("830,000 m2 vs Comino at 3.5 km2 (area often quoted)", round(lost / 3.5e6, 2), "x Comino", "calculated",
    "Amphora: roughly a quarter")
add("830,000 m2 vs Manoel Island", round(lost / ISL["Manoel Island"], 1), "x Manoel", "calculated", "Amphora: two")
add("EEA 2006-2012 + 2012-2018 + Amphora 2018-2023",
    round((A["Land take 2006-2012 (EEA)"] + A["Land take 2012-2018 (EEA)"] + lost) / 1e6, 2), "km2", "calculated",
    "Amphora: at least 1.94 km2 (methods differ)")
for rule, lab, win in (("strict", "3-year rule", "first mapped as built in 2020-2021"),
                       ("two-year", "2-year rule", "first mapped as built in 2019-2022")):
    r = C[rule]
    add(f"IO land cover, new built-up {win} ({lab})", float(r["new_built_km2"]), "km2", "Impact Observatory LULC v2",
        f"reverse change {r['reverse_km2']} km2; net {r['net_km2']} km2")
    add(f"IO land cover, new built-up from crops / rangeland ({lab})", f"{r['from_crops_pct']} / {r['from_rangeland_pct']}",
        "%", "Impact Observatory LULC v2", "Amphora: nearly 95% farmland")
r = C["single-year"]
add("IO land cover, simple 2018 vs 2023 comparison (single-year maps)", float(r["new_built_km2"]), "km2",
    "Impact Observatory LULC v2", f"reverse change {r['reverse_km2']} km2; net {r['net_km2']} km2 (noise, not credible)")
BU = {int(r["year"]): float(r["area_km2"]) for r in csv.DictReader(open(D / "io_lulc_areas.csv"))
      if r["class"] == "built area"}
steps = {f"{y - 1}->{y}": round(BU[y] - BU[y - 1], 1) for y in sorted(BU)[1:]}
add("IO built-up total, change from one year to the next (largest / smallest)",
    f"{max(abs(v) for v in steps.values())} / {min(abs(v) for v in steps.values())}", "km2",
    "Impact Observatory LULC v2", "; ".join(f"{k} {v:+}" for k, v in steps.items()))
T = {r["item"]: float(r["value"]) for r in csv.DictReader(open(D / "eea_land_take.csv"))}
lo, hi = T["Malta land take 2012-2018 (low reading)"], T["Malta land take 2012-2018 (high reading)"]
add("EEA chart: Malta land take 2012-2018", f"{lo * land / 1e12:.2f}-{hi * land / 1e12:.2f}", "km2", "EEA chart x land area",
    "Amphora quotes 920,000 m2 (0.92 km2)")
add("EEA chart: Malta's rank for land take 2012-2018", int(T["Malta rank among EEA39 countries 2012-2018"]), "of 39",
    "EEA chart", "proportion of country area")
s = C["strict"]
add("Amphora figure vs IO net change (3-year rule)", round(lost / 1e6 / float(s["net_km2"]), 2), "ratio", "calculated",
    "below 1 = Amphora lower than the independent estimate; periods differ (Amphora 2018-2023, IO first built 2020-21)")

with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\r\n")
    w.writeheader()
    w.writerows(rows)
for x in rows:
    print(f"{x['check']:70s} {str(x['value']):>14} {x['unit']:9s} {x['note']}")
