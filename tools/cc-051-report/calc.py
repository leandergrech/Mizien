#!/usr/bin/env python3
"""CC-051: protected share of Malta's seas under each reference area. Writes data/cc-051/checks.csv."""
import csv, pathlib

D = pathlib.Path(__file__).resolve().parents[2] / "data" / "cc-051"
N = list(csv.DictReader(open(D / "natura2000_marine.csv")))
A = list(csv.DictReader(open(D / "reference_areas.csv")))
prot = float(next(r for r in N if r["sitecode"] == "UNION")["sea_km2"])
nsites = sum(1 for r in N if r["sitecode"] != "UNION" and r["sea_km2"] and float(r["sea_km2"]) >= 1)
summed = sum(float(r["sea_km2"]) for r in N if r["sitecode"] != "UNION" and float(r["sea_km2"] or 0) >= 1)
rows = [{"check": "Marine Natura 2000 sites", "value": nsites, "unit": "sites", "source": "EEA", "note": "ERA: 18 sites"},
        {"check": "Protected sea area (union, overlaps counted once)", "value": prot, "unit": "km2", "source": "EEA",
         "note": "ERA: over 4,100 km2"},
        {"check": "Sum of site areas (overlaps double-counted)", "value": round(summed, 1), "unit": "km2", "source": "EEA", "note": ""}]
for a in [x for x in A if "Territorial" not in x["reference_area"]]:
    rows.append({"check": f"Protected share of {a['reference_area']}", "value": round(100 * prot / float(a["km2"]), 1),
                 "unit": "%", "source": "calculated", "note": a["note"]})
rows.append({"check": "Extra protected area needed for 30% of EU-reported marine waters", "value": round(0.3 * 75715 - prot),
             "unit": "km2", "source": "calculated", "note": ""})
with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\r\n")
    w.writeheader()
    w.writerows(rows)
for r in rows:
    print(f"{r['check']:72s} {str(r['value']):>9} {r['unit']:6s} {r['note']}")
