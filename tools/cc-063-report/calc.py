#!/usr/bin/env python3
"""CC-063: test the MDA's June 2021 warning that, without an enduring solution to construction-waste dumping,
development would come to an "almost complete standstill". Reads data/cc-063/eurostat_*.csv (fetch.py) and writes
data/cc-063/checks.csv. Tests (a) did construction output stall after the warning (volume index, sts_copr_a),
(b) how much construction waste arises and where it goes (env_wasgen, env_wastrt)."""
import csv, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-063"
prd = {int(r["time"]): float(r["value"]) for r in csv.DictReader(open(D / "eurostat_sts_copr_a.csv"))}
gen = {(r["nace_r2"], r["waste"], int(r["time"])): float(r["value"]) for r in csv.DictReader(open(D / "eurostat_env_wasgen.csv"))}
trt = {(r["wst_oper"], int(r["time"])): float(r["value"]) for r in csv.DictReader(open(D / "eurostat_env_wastrt.csv"))}
SRC = "Eurostat (sts_copr_a updated 2 Oct 2026; env_wasgen, env_wastrt updated Sep 2025), retrieved 5 Oct 2026"
rows = []


def add(check, value, unit, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": SRC, "note": note})


for y in range(2019, 2023):
    add(f"Construction production volume index {y} (2015=100)", prd[y], "index", "provisional" if y == 2022 else "")
for y in (2020, 2021, 2022):
    add(f"Change in construction volume, {y - 1} to {y}", round(100 * (prd[y] / prd[y - 1] - 1), 1), "%")
add("Change in construction volume, 2020 to 2022", round(100 * (prd[2022] / prd[2020] - 1), 1), "%")
add("Latest year published for Malta in sts_copr_a", max(prd), "year", "2023-2025 not yet published")
for y in (2018, 2020, 2022):
    add(f"Waste from construction (NACE F), all waste, {y}", gen[("F", "TOTAL", y)], "tonnes")
    add(f"Construction's share of all waste generated in Malta, {y}",
        round(100 * gen[("F", "TOTAL", y)] / gen[("TOTAL_HH", "TOTAL", y)], 1), "%")
    add(f"Mineral C&D waste (W121) from construction, {y}", gen[("F", "W121", y)], "tonnes")
add("Change in construction-sector waste, 2020 to 2022",
    round(100 * (gen[("F", "TOTAL", 2022)] / gen[("F", "TOTAL", 2020)] - 1), 1), "%")
add("Change in construction-sector waste, 2018 to 2022",
    round(100 * (gen[("F", "TOTAL", 2022)] / gen[("F", "TOTAL", 2018)] - 1), 1), "%")
for y in (2020, 2022):
    t = trt[("TRT", y)]
    for op, lab in (("RCV_R", "recycling"), ("RCV_B", "backfilling"), ("DSP_L", "landfill (D1, D5, D12)")):
        add(f"Mineral C&D waste treated: {lab} share, {y}", round(100 * trt[(op, y)] / t, 1), "%",
            "backfilling is classed as recovery in Eurostat's scheme")
    add(f"Mineral C&D waste treated, total, {y}", t, "tonnes")
with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
for r in rows:
    print(f"{r['check'][:80]:80s} {r['value']:>10} {r['unit']}")
