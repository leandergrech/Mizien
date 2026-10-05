#!/usr/bin/env python3
"""CC-004: test the waste-separation figures against recycling and landfill rates.

Reads data/cc-004/eurostat_municipal_waste.csv (Eurostat cei_wm011, env_wasmun, cei_wm020; retrieved
2 Oct 2026) and data/cc-004/eurostat_cei_wm011_eu27.csv (all EU-27 states; fetch_eurostat.py, retrieved
5 Oct 2026), and writes data/cc-004/checks.csv. Ministry figures are from the press release of
19 January 2026 (PR260072en); NSO figures from News Releases 225/2025 and 023/2026; deposit-scheme rates from
the Commission's SWD(2025) 318, p. 11.
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

# ------------------------------------------------------------------ v1.1 (5 Oct 2026)
# EU-27 comparison: eurostat_cei_wm011_eu27.csv (fetch_eurostat.py, retrieved 5 Oct 2026)
ES5 = "Eurostat cei_wm011, retrieved 5 Oct 2026"
eu27 = defaultdict(dict)
for r in csv.DictReader(open(D / "eurostat_cei_wm011_eu27.csv")):
    eu27[r["geo"]][int(r["year"])] = float(r["value"])
for y in (2019, 2024):  # the two extracts must agree for Malta and the EU-27
    assert eu27["MT"][y] == rate[y] and eu27["EU27_2020"][y] == eu[y], f"cei_wm011 extracts differ for {y}"
states = [g for g in eu27 if g != "EU27_2020"]
both = {g: round(eu27[g][2024] - eu27[g][2019], 1) for g in states if 2019 in eu27[g] and 2024 in eu27[g]}
ranked = sorted(both, key=lambda g: -both[g])
add("Malta recycling-rate change 2019-2024", both["MT"], "pp", ES5, f"{rate[2019]}% -> {rate[2024]}%")
add("Rank of Malta's change among states with 2019 and 2024 data", ranked.index("MT") + 1, f"of {len(both)}",
    ES5, "larger rises: " + ", ".join(f"{g} {both[g]:+.1f}" for g in ranked[:ranked.index("MT")]) +
    "; no 2024 value for " + ", ".join(sorted(g for g in states if g not in both)))
low24 = sorted((eu27[g][2024], g) for g in states if 2024 in eu27[g])
add("Rank of Malta's 2024 rate, lowest first, among states with 2024 data",
    [g for _, g in low24].index("MT") + 1, f"of {len(low24)}", ES5, f"lowest: {low24[0][1]} {low24[0][0]}%")
latest = sorted((eu27[g][max(eu27[g])], g, max(eu27[g])) for g in states)
add("States at or below Malta's rate on latest available data (2023 or 2024)",
    sum(1 for x, g, _ in latest if x <= rate[2024] and g != "MT"), "states", ES5,
    "; ".join(f"{g} {x}% ({y})" for x, g, y in latest if x <= rate[2024] and g != "MT"))
# packaging, before and after the deposit refund scheme (launched November 2022)
for code, lab in (("W1501", "all packaging"), ("W150102", "plastic packaging"), ("W150107", "glass packaging")):
    s = v[("cei_wm020", "MT", f"waste={code}|unit=RT_TGT2025")]
    add(f"Malta recycling rate, {lab}, 2022 -> 2023", round(s[2023] - s[2022], 1), "pp", ES + " cei_wm020",
        f"{s[2022]}% -> {s[2023]}%; link to the deposit refund scheme is our inference")
add("Gap to the 2025 packaging target (65%) in 2023", round(pk[2023] - 65, 1), "pp", "calculated; Directive 94/62/EC Art 6(1)(f)")
add("Deposit refund scheme: containers collected, 2023", 78, "% of containers placed on the market",
    "Commission SWD(2025) 318 p. 11 (citing ERA 2024)", "reported, not recomputed")
add("Deposit refund scheme: containers recycled, 2023", 74, "% of containers placed on the market",
    "Commission SWD(2025) 318 p. 11 (citing ERA 2024)", "reported, not recomputed")
up = 100 * (rcy[2024] + 30) / gen[2024]
add("Recycling rate if 30 million kg of organic waste were all counted as recycled", round(up, 1), "%", "calculated",
    "upper bound, indicative: ministry's 2025 organic tonnage added to Eurostat's 2024 recycled tonnage")
with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for r in rows:
    print(f"{r['check']:65s} {r['value']:>8} {r['unit']}  {r['note']}")
