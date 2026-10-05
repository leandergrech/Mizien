#!/usr/bin/env python3
"""CC-053: test "the Milky Way is visible from only about 13% of the Maltese Islands, and 87% of the area has high
light pollution" against the study it summarises (Caruana et al. 2020, Table 1) and the world atlas.

Reads data/cc-053/caruana2020_table1.csv and the island areas in docs/data/geo.json; writes data/cc-053/checks.csv.
Checks: (1) the archipelago-wide shares follow from the island shares weighted by land area; (2) 87% is the share in
Bortle classes 5-9; (3) the result against Falchi et al. (2016)'s 11% and the paper's own threshold sensitivity.
"""
import csv, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-053"
T = {r["bortle_class"]: r for r in csv.DictReader(open(D / "caruana2020_table1.csv"))}
area = {}
for i in json.load(open(ROOT / "docs/data/geo.json"))["islands"]:
    area[i["name"]] = area.get(i["name"], 0) + i["area_m2"] / 1e6
A = {"Malta": area["Malta"] + area.get("Manoel Island", 0), "Gozo": area["Gozo"], "Comino": area["Comino"] + area.get("Cominotto", 0)}
SRC = "Caruana et al. (2020) Table 1; island areas from OpenStreetMap (docs/data/geo.json)"
rows = []


def add(check, value, unit, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": SRC, "note": note})


tot = sum(A.values())
for cls in ("4", "5", "6-7", "8-9"):
    w = sum(float(T[cls][f"{k.lower()}_2017_18_pct"]) * A[k] for k in A) / tot
    add(f"Area-weighted share in Bortle class {cls} (Malta, Gozo, Comino)", round(w, 1), "%", f"paper's 'All' column: {T[cls]['all_2017_18_pct']}%")
add("Paper: share in classes 5-9 (= 100% minus class 4)", round(100 - float(T["4"]["all_2017_18_pct"]), 1), "%", "the '87%' in the claim")
add("Paper: Milky Way visible, class 4 threshold (> 20.4)", 12.8, "%", "2017/18")
add("Paper: Milky Way visible, Falchi midpoint threshold (> 20.3)", 13.5, "%")
add("Paper: threshold sensitivity (> 20.6 to > 20.0)", "6.3 to 25.9", "%")
add("Falchi et al. (2016) world atlas: Milky Way visible (Maltese islands)", 11, "%", "as reported by Caruana et al. (2020)")
add("Island of Malta, class 4 share 2017/18 vs 2018/19", f"{T['4']['malta_2017_18_pct']} vs {T['4']['malta_2018_19_pct']}", "%", "second survey of Malta only")
for k in A:
    add(f"Land area used: {k}", round(A[k], 2), "km2")
with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for r in rows:
    print(f"{r['check'][:70]:70s} {r['value']:>12} {r['unit']}  {r['note']}")
