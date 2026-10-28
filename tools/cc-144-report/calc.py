#!/usr/bin/env python3
"""CC-144: recompute the hunter-density ranking with formulas, not by eye.

Inputs (data/cc-144/):
  face_hunters_2009_10.csv  FACE Annual Report 2009-2010 p.16 table (36 countries; area in thousand km2, rounded)
  malta_inputs.csv          Malta population and area (Eurostat) and hunter counts (FACE; BirdLife Malta via Mongabay)
Output: data/cc-144/checks.csv and data/cc-144/ranking_2010.csv
"""
import csv, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-144"
M = {r["item"]: float(r["value"]) for r in csv.DictReader(open(D / "malta_inputs.csv", encoding="utf-8"))}
AREA, POP10 = M["Malta area"], M["Malta population 1 Jan 2010"]
POP24, POP25 = M["Malta population 1 Jan 2024"], M["Malta population 1 Jan 2025"]

rows = []
for r in csv.DictReader(open(D / "face_hunters_2009_10.csv", encoding="utf-8")):
    if r["hunters"] == "-":
        continue
    h, a, p = int(r["hunters"]), float(r["area_thousand_km2"]) * 1000, float(r["population_million"]) * 1e6
    if r["country"] == "Malta":
        a, p = AREA, POP10  # FACE rounds Malta to 0.3 thousand km2 and 0.4 million
    rows.append({"country": r["country"], "hunters": h, "per_km2": h / a, "per_1000": 1000 * h / p})
for key, col in (("per_km2", "rank_per_km2"), ("per_1000", "rank_per_1000")):
    for i, r in enumerate(sorted(rows, key=lambda x: -x[key]), 1):
        r[col] = i
with open(D / "ranking_2010.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, ["country", "hunters", "per_km2", "rank_per_km2", "per_1000", "rank_per_1000"])
    w.writeheader()
    for r in sorted(rows, key=lambda x: x["rank_per_km2"]):
        w.writerow({k: (round(v, 2) if isinstance(v, float) else v) for k, v in r.items() if k in w.fieldnames})

by = {r["country"]: r for r in rows}
mt = by["Malta"]
second_km2 = sorted(rows, key=lambda x: -x["per_km2"])[1]
out = []


def add(check, value, unit, source, note=""):
    out.append({"check": check, "value": value, "unit": unit, "source": source, "note": note})


F = "FACE Annual Report 2009-2010 p.16"
add("Countries in FACE table with a hunter count", len(rows), "countries", F, "Montenegro has no count")
add("Malta hunters per km2, FACE count 15,000", round(mt["per_km2"], 1), "per km2", F + "; Eurostat area", "rank %d of %d" % (mt["rank_per_km2"], len(rows)))
add("Next highest hunters per km2", f"{second_km2['country']} {second_km2['per_km2']:.1f}", "per km2", F, "")
add("Malta density as multiple of next highest", round(mt["per_km2"] / second_km2["per_km2"], 1), "x", "calculated", "")
for label, n in (("15,000 (FACE)", 15000), ("10,091 (WBRU 2025 land licences, second-hand)", 10091), ("10,000 (BirdLife Malta via Mongabay)", 10000), ("5,000 (stress test: one third of FACE count)", 5000)):
    add("Malta hunters per km2 at " + label, round(n / AREA, 1), "per km2", "calculated", "area 316 km2 (Eurostat)")
add("Malta hunters per 1,000 inhabitants, FACE count and 2010 population", round(mt["per_1000"], 1), "per 1,000", F + "; Eurostat demo_pjan", "rank %d of %d" % (mt["rank_per_1000"], len(rows)))
for c in ("Ireland", "Finland", "Cyprus", "Norway"):
    add(f"{c} hunters per 1,000 inhabitants (FACE)", round(by[c]["per_1000"], 1), "per 1,000", F, "rank %d" % by[c]["rank_per_1000"])
add("Countries ahead of Malta per head (FACE table)", mt["rank_per_1000"] - 1, "countries", "calculated", ", ".join(r["country"] for r in sorted(rows, key=lambda x: x["rank_per_1000"]) if r["rank_per_1000"] < mt["rank_per_1000"]))
for label, n, p in (("10,000 and 1 Jan 2024 population", 10000, POP24), ("10,091 and 1 Jan 2025 population", 10091, POP25)):
    v = 1000 * n / p
    ahead = sum(r["per_1000"] > v for r in rows if r["country"] != "Malta")
    add("Malta hunters per 1,000 inhabitants, " + label, round(v, 1), "per 1,000", "calculated", f"{ahead} of the other FACE-table countries (2010 counts) higher")
add("Malta population growth 2010 to 2024", round(100 * (POP24 / POP10 - 1)), "%", "Eurostat demo_pjan", "")
with open(D / "checks.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, ["check", "value", "unit", "source", "note"])
    w.writeheader(); w.writerows(out)
for r in out:
    print(r["check"], "|", r["value"], r["unit"], "|", r["note"])
