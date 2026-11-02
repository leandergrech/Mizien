#!/usr/bin/env python3
"""CC-147: recompute the Climate Action Authority factsheet's 87.2% and 19% from Eurostat data
(data/cc-147/eurostat_aea.csv, retrieved 2 Nov 2026) -> data/cc-147/checks.csv."""
import csv, pathlib
from collections import defaultdict
ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-147"
V, FL = {}, {}
for r in csv.DictReader(open(D / "eurostat_aea.csv")):
    k = (r["dataset"], r["unit"], r["item"], r["geo"], int(r["year"]))
    V[k] = float(r["value"]); FL[k] = r["flag"]
em = lambda it, y, g="MT": V[("env_ac_ainah_r2", "THS_T", it, g, y)]
clv = lambda it, y, g="MT": V[("nama_10_a64", "CLV20_MEUR", it, g, y)]
cp = lambda it, y, g="MT": V[("nama_10_a64", "CP_MEUR", it, g, y)]
br = lambda it, y: V[("env_ac_aibrid_r2", "THS_T", it, "MT", y)]
pc = lambda a, b: 100 * (b / a - 1)
rows = []
def add(check, value, unit, source, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": source, "note": note})
S = "Eurostat env_ac_ainah_r2, nama_10_a64, retrieved 2 Nov 2026"
HH = "TOTAL_HH"
# A. weight of aviation and shipping
for y in (2020, 2024):
    add(f"Malta {y}: air transport (H51) share of GHG emissions, residence principle", round(100 * em("H51", y) / em(HH, y), 1), "%", S, "all NACE activities plus households")
    add(f"Malta {y}: water transport (H50) share", round(100 * em("H50", y) / em(HH, y), 1), "%", S)
add("Malta: air-transport emissions 2020 -> 2024", f"{em('H51',2020):.0f} -> {em('H51',2024):.0f}", "kt CO2e", S, f"x{em('H51',2024)/em('H51',2020):.1f}")
add("Malta: air + water transport removed, emissions 2020 -> 2024", f"{em(HH,2020)-em('H50',2020)-em('H51',2020):.1f} -> {em(HH,2024)-em('H50',2024)-em('H51',2024):.1f}", "kt CO2e", S,
    "factsheet p.3 chart: 2016.34 -> 2116.77 (our 2024 value is 8.5 kt lower: data vintage)")
add("Malta: emissions all activities plus households, 2020 -> 2024", f"{em(HH,2020):.2f} -> {em(HH,2024):.2f}", "kt CO2e", S, f"{pc(em(HH,2020),em(HH,2024)):+.1f}%; matches factsheet p.3 (2755.00 -> 6951.29); Eurostat flag 2024: i")
add("EU-27: emissions all activities plus households, 2020 -> 2024", round(pc(em(HH,2020,'EU27_2020'), em(HH,2024,'EU27_2020')), 1), "%", S)
add("Malta: air transport share, 2013 -> 2024 (residence principle)", f"{100*em('H51',2013)/em(HH,2013):.1f} -> {100*em('H51',2024)/em(HH,2024):.1f}", "%", S)
add("EU-27: air transport share of GHG, 2024", round(100 * em("H51", 2024, "EU27_2020") / em(HH, 2024, "EU27_2020"), 1), "%", S)
# B. 87.2%
for lab, it in (("all activities plus households", HH), ("all NACE activities (no households)", "TOTAL")):
    a = [em(it, y) / clv("TOTAL", y) for y in (2020, 2024)]
    add(f"Malta GHG intensity 2020 -> 2024, {lab}, per euro of GVA (CLV 2020)", f"{1000*a[0]:.1f} -> {1000*a[1]:.1f}", "g CO2e/EUR", S, f"{pc(*a):+.1f}%; factsheet says Eurostat figures 'summed up' show +87.2%")
a = [em(HH, y, "EU27_2020") / clv("TOTAL", y, "EU27_2020") for y in (2020, 2024)]
add("EU-27 GHG intensity 2020 -> 2024 (activities plus households / GVA CLV 2020)", round(pc(*a), 1), "%", S)
# C. 19%
def excl_clv(y, items):
    return clv("TOTAL", y) - sum(clv(i, y) for i in items)
def excl_cp(y, items):
    return cp("TOTAL", y) - sum(cp(i, y) for i in items)
for lab, items in (("air and water transport (H50+H51)", ("H50", "H51")), ("air transport only (H51)", ("H51",))):
    e = lambda y: em(HH, y) - sum(em(i, y) for i in items)
    ig = [e(y) / excl_clv(y, items) for y in (2020, 2024)]
    add(f"Malta intensity 2020 -> 2024 excluding {lab}: emissions / GVA (CLV subtraction)", round(pc(*ig), 1), "%", S,
        f"emissions {pc(e(2020), e(2024)):+.1f}%; GVA {pc(excl_clv(2020, items), excl_clv(2024, items)):+.1f}%; chain-linked series are not additive, so the subtraction is approximate; factsheet: -19%")
    ng = [e(y) / excl_cp(y, items) for y in (2020, 2024)]
    add(f"Malta intensity 2020 -> 2024 excluding {lab}: emissions / GVA at current prices", round(pc(*ng), 1), "%", S,
        f"GVA {pc(excl_cp(2020, items), excl_cp(2024, items)):+.1f}% nominal (not inflation-adjusted); cross-check only")
add("Malta: air transport GVA 2020 (base year), current prices = CLV 2020", cp("H51", 2020), "EUR m", S, "negative: air transport made a loss in 2020, so removing it RAISES the 2020 denominator")
add("Malta: air transport GVA 2021-2024 (CLV 2020)", ", ".join(f"{y}: {clv('H51',y):.0f}" for y in range(2021, 2025)), "EUR m", S, "sign changes between years: chain-linked volumes of a small sector, volatile")
add("Malta: GVA all activities 2020 -> 2024 (CLV 2020)", round(pc(clv("TOTAL", 2020), clv("TOTAL", 2024)), 1), "%", S, f"{clv('TOTAL',2020):.0f} -> {clv('TOTAL',2024):.0f} EUR m")
# D. territorial inventory (bridging table)
add("Malta: emissions on the territory principle (UNFCCC basis) 2020 -> 2024", f"{br('AEMIS_TER',2020):.0f} -> {br('AEMIS_TER',2024):.0f}", "kt CO2e", "Eurostat env_ac_aibrid_r2, retrieved 2 Nov 2026", f"{pc(br('AEMIS_TER',2020), br('AEMIS_TER',2024)):+.1f}%; 2024 flag i")
ti = [br("AEMIS_TER", y) / clv("TOTAL", y) for y in (2020, 2024)]
add("Malta: territory-principle emissions per euro of GVA (CLV 2020) 2020 -> 2024", round(pc(*ti), 1), "%", "Eurostat env_ac_aibrid_r2 and nama_10_a64", "independent of the CLV-subtraction; compare factsheet -19%")
add("Malta 2024: residents' air-transport emissions from fuel bought abroad, share of residence total", round(100 * br("AEMIS_RES_ABR_ATR", 2024) / br("AEMIS_RES", 2024), 1), "%", "Eurostat env_ac_aibrid_r2", "i.e. most of the residence-principle total is air fuel bought abroad")
# E. start-year sensitivity
items = ("H51",)  # chain-linked H50 starts in 2020 and H51 in 2017, so only air transport can be removed for earlier start years
for y0 in range(2017, 2024):
    full = pc(em(HH, y0) / clv("TOTAL", y0), em(HH, 2024) / clv("TOTAL", 2024))
    ex = pc((em(HH, y0) - sum(em(i, y0) for i in items)) / excl_clv(y0, items), (em(HH, 2024) - sum(em(i, 2024) for i in items)) / excl_clv(2024, items))
    add(f"Start-year sensitivity {y0} -> 2024: intensity, all / excluding air transport only (CLV subtraction)", f"{full:+.1f} / {ex:+.1f}", "%", S)
with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for x in rows: print(f"{x['check'][:95]:95s} {str(x['value']):>20} {x['unit']:10s} {x['note'][:100]}")
