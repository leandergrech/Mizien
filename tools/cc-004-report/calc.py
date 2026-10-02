#!/usr/bin/env python3
"""CC-004: test the waste-separation figures against recycling and landfill rates.

Reads data/cc-004/eurostat_municipal_waste.csv (Eurostat cei_wm011, env_wasmun, cei_wm020; retrieved
2 Oct 2026) and writes data/cc-004/checks.csv. Ministry figures are from the press release of
19 January 2026 (PR260072en); NSO figures from News Releases 225/2025 and 023/2026.
"""
import csv, pathlib
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-004"
v = defaultdict(dict)
for r in csv.DictReader(open(D / "eurostat_municipal_waste.csv")):
    v[(r["dataset"], r["geo"], r["item"])][int(r["year"])] = float(r["value"])
ES = "Eurostat, retrieved 2 Oct 2026"
PR = "Ministry press release PR260072en, 19 Jan 2026"
NSO = "NSO News Release 225/2025 (Municipal Waste 2024)"
rows = []


def add(check, value, unit, source, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": source, "note": note})


rate = v[("cei_wm011", "MT", "wst_oper=RCY|unit=PC")]
eu = v[("cei_wm011", "EU27_2020", "wst_oper=RCY|unit=PC")]
for y in (2019, 2020, 2024):
    add(f"Malta municipal recycling rate {y}", rate[y], "%", ES + " cei_wm011", f"EU-27: {eu.get(y)}%")
add("Gap to 2020 target (50%) in 2020", round(rate[2020] - 50, 1), "pp", "calculated; Directive 2008/98/EC Art 11(2)(a)")
add("Gap to 2025 target (55%) in 2024", round(rate[2024] - 55, 1), "pp", "calculated; Directive (EU) 2018/851 Art 11(2)(c)")
yrs = sorted(y for y in rate if y >= 2019)
gain = (rate[2024] - rate[2019]) / (2024 - 2019)
add("Average gain in recycling rate per year, 2019-2024", round(gain, 2), "pp/yr", "calculated")
add("Years to reach 55% at 2019-2024 pace", round((55 - rate[2024]) / gain, 0), "years", "calculated",
    "linear extrapolation, illustrative only")

g = lambda op, u="THS_T": v[("env_wasmun", "MT", f"wst_oper={op}|unit={u}")]
land, trt, gen, rcy, rcv = g("DSP_L_OTH"), g("TRT"), g("GEN"), g("RCY"), g("RCV_E")
add("Share of treated municipal waste landfilled 2024", round(100 * land[2024] / trt[2024], 1), "%", ES + " env_wasmun",
    "NSO reports 79.2% for 2024")
add("Municipal waste landfilled change 2019-2024", round(100 * (land[2024] / land[2019] - 1), 1), "%", ES,
    f"{land[2019]:.0f} -> {land[2024]:.0f} thousand t")
add("Municipal waste generated change 2019-2024", round(100 * (gen[2024] / gen[2019] - 1), 1), "%", ES,
    f"{gen[2019]:.0f} -> {gen[2024]:.0f} thousand t")
r5 = sum(rcy[y] for y in range(2020, 2025))
e5 = sum(rcv[y] for y in range(2020, 2025))
add("Municipal waste recycled 2020-2024 (sum)", r5, "thousand t", ES)
add("Municipal waste energy-recovered 2020-2024 (sum)", e5, "thousand t", ES)
add("Ministry: waste diverted from landfill over five years", 412, "thousand t", PR, "412 million kg")
add("Ministry figure minus Eurostat recycled + recovered", 412 - r5 - e5, "thousand t", "calculated",
    "unexplained difference; scope of the 412 figure not stated")
add("Ministry: mixed waste change", round(100 * (95.5 / 141 - 1), 1), "%", PR,
    "141 -> 95.5 million kg; start year not stated")
add("Ministry: organic waste 2025 as share of 2024 municipal generation", round(100 * 30 / gen[2024], 1), "%",
    "calculated", "30 million kg vs Eurostat 2024 generation; years differ, indicative only")
pk = v[("cei_wm020", "MT", "waste=W1501|unit=RT_TGT2025")]
add("Malta packaging recycling rate 2023", pk[2023], "%", ES + " cei_wm020", "2025 target 65%")
with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for r in rows:
    print(f"{r['check']:65s} {r['value']:>8} {r['unit']}  {r['note']}")
