#!/usr/bin/env python3
"""CC-111: test the European Commission's 2026 Country Report figures on municipal waste in Malta.

Reads data/cc-111/eurostat_env_wasmun*.csv (fetch.py; Eurostat env_wasmun, updated 30 Mar 2026, retrieved
5 Oct 2026) and writes data/cc-111/checks.csv. The Commission cites env_wasmun (footnotes 156 and 158).
"Landfill rate" here is waste landfilled (D1-D7, D12) as a share of waste generated, the basis that reproduces the
report's 82% and 74%; the share of waste treated is given alongside, because other sources use it.
"""
import csv, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-111"
v, fl = {}, {}
for r in csv.DictReader(open(D / "eurostat_env_wasmun.csv")):
    k = (r["geo"], r["wst_oper"], r["unit"], int(r["year"]))
    v[k] = float(r["value"]); fl[k] = r["flag"]
a = {}
for r in csv.DictReader(open(D / "eurostat_env_wasmun_eu27_2023_2024.csv")):
    a[(r["geo"], r["wst_oper"], int(r["year"]))] = float(r["value"])
SRC = "Eurostat env_wasmun (updated 30 Mar 2026), retrieved 5 Oct 2026"
rows = []


def add(check, value, unit, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": SRC, "note": note})


def k(g, op, y, u="KG_HAB"):
    return v[(g, op, u, y)]


def rate(g, y, base="GEN"):
    return round(100 * k(g, "DSP_L_OTH", y) / k(g, base, y), 1)


for y in (2023, 2024):
    add(f"Malta: municipal waste generated per person, {y}", k("MT", "GEN", y), "kg", "flag: " + (fl[("MT", "GEN", "KG_HAB", y)] or "none"))
    add(f"EU-27: municipal waste generated per person, {y}", k("EU27_2020", "GEN", y), "kg", "flag: " + (fl[("EU27_2020", "GEN", "KG_HAB", y)] or "none"))
add("Malta vs EU-27, waste per person 2024", round(100 * (k("MT", "GEN", 2024) / k("EU27_2020", "GEN", 2024) - 1), 1), "% above")
for y in (2013, 2014, 2022, 2023, 2024):
    add(f"Malta: landfill rate {y} (landfilled / generated)", rate("MT", y), "%")
    add(f"Malta: landfill rate {y} (landfilled / treated)", rate("MT", y, "TRT"), "%")
for y in (2022, 2024):
    add(f"EU-27: landfill rate {y} (landfilled / generated)", rate("EU27_2020", y), "%", "EU-27 landfill value for 2023 not published in env_wasmun")
add("Malta: incineration with and without energy recovery, 2023 (share of generated)",
    round(100 * k("MT", "DSP_I_RCV_E", 2023) / k("MT", "GEN", 2023), 1), "%")
add("Malta: recycling (material, composting, digestion), 2024 (share of generated)",
    round(100 * k("MT", "RCY", 2024) / k("MT", "GEN", 2024), 1), "%", "Eurostat's official recycling rate (cei_wm011) uses a different method; the report gives 16.7%")
add("Malta: years 2013-2024 with landfilled tonnage above generated", ", ".join(str(y) for y in range(2013, 2025) if k("MT", "DSP_L_OTH", y) > k("MT", "GEN", y)) or "none", "years",
    "2015: 676 kg landfilled against 643 kg generated; the dataset gives no reason; 2015 is not used in any test")
for y in (2023, 2024):
    gen = sorted(((a[(g, "GEN", y)], g) for g in {x[0] for x in a} if (g, "GEN", y) in a), reverse=True)
    lf = sorted(((a[(g, "DSP_L_OTH", y)] / a[(g, "GEN", y)], g) for g in {x[0] for x in a} if (g, "DSP_L_OTH", y) in a and (g, "GEN", y) in a), reverse=True)
    add(f"Malta's rank, waste per person {y}", f"{[g for _, g in gen].index('MT') + 1} of {len(gen)}", "rank", "member states with data, highest first")
    add(f"Malta's rank, landfill rate {y}", f"{[g for _, g in lf].index('MT') + 1} of {len(lf)}", "rank",
        "higher: " + ", ".join(f"{g} {100 * x:.1f}%" for x, g in lf[:[g for _, g in lf].index('MT')]) or "none")
with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for r in rows:
    print(f"{r['check'][:80]:80s} {r['value']:>10} {r['unit']}  {r['note'][:60]}")
