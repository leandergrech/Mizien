#!/usr/bin/env python3
"""CC-024: test Malta's 2030 renewables contribution against the plan's own path, Eurostat and PV capacity.

Reads data/cc-024/eurostat_nrg_ind_ren.csv (Eurostat, retrieved 5 Oct 2026), necp_commission_inputs.csv (typed from
the plan and the Commission's assessment, printed pages) and nso_pv.csv (second-hand NSO figures); writes
data/cc-024/checks.csv."""
import csv, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-024"
eu = {}
flag = {}
for r in csv.DictReader(open(D / "eurostat_nrg_ind_ren.csv")):
    eu[(r["geo"], r["item"], int(r["year"]))] = float(r["value"])
    if r["flag"]:
        flag[(r["geo"], r["item"], int(r["year"]))] = r["flag"]
inp = {}
for r in csv.DictReader(open(D / "necp_commission_inputs.csv")):
    inp[(r["series"], r["key"])] = float(r["value"])
pv = {r["series"]: float(r["value"]) for r in csv.DictReader(open(D / "nso_pv.csv"))}
rows = []


def add(check, value, unit, source, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": source, "note": note})


ES = "Eurostat nrg_ind_ren, retrieved 5 Oct 2026 (updated 15 Sep 2026)"
PL = "Malta final updated NECP, Table 3 (p.83)"
M = lambda i, y, g="MT": eu[(g, i, y)]
# 1. actual vs the plan's own indicative path
for y in (2023, 2024, 2025):
    plan = inp[("plan_indicative_RES_target", str(y))]
    act = M("REN", y)
    add(f"Malta RES share {y}: Eurostat vs plan's indicative target", f"{act:.2f} vs {plan:.1f}", "%", ES + "; " + PL,
        f"{act - plan:+.2f} points" + (" (Eurostat flag p: provisional)" if ("MT", "REN", y) in flag else ""))
add("Malta RES share 2025 (provisional) vs Commission reference point for 2025", f"{M('REN', 2025):.1f} vs 18", "%",
    ES + "; Commission SWD(2025) 140 s.2.2", f"{M('REN', 2025) - 18:+.1f} points; plan's own 2025 figure is 16.5% (below the 18% reference)")
# 2. straight line from the 2020 outturn to the 2030 contribution
s20, tgt = M("REN", 2020), inp[("plan_indicative_RES_target", "2030")]
for y in (2024, 2025):
    line = s20 + (tgt - s20) * (y - 2020) / 10
    add(f"Straight line 2020 outturn ({s20:.2f}%) to 24.5% in 2030, value in {y}", round(line, 2), "%", ES + "; " + PL,
        f"actual {M('REN', y):.2f}% = {M('REN', y) - line:+.2f} points")
# 3. speed needed
need24 = (tgt - M("REN", 2024)) / 6
add("Rise per year needed 2024 -> 2030 to reach 24.5%", round(need24, 2), "points/yr", ES + "; " + PL)
add("Average rise per year 2020 -> 2024", round((M("REN", 2024) - s20) / 4, 2), "points/yr", ES)
add("Rise per year needed 2025 (provisional) -> 2030", round((tgt - M("REN", 2025)) / 5, 2), "points/yr", ES + "; " + PL)
# 4. where the rise came from
for i, lab in (("REN_ELC", "electricity"), ("REN_HEAT_CL", "heating and cooling"), ("REN_TRA", "transport")):
    add(f"Malta sector share, {lab}: 2020 -> 2024", f"{M(i, 2020):.1f} -> {M(i, 2024):.1f}", "%", ES,
        f"{M(i, 2024) - M(i, 2020):+.1f} points; EU-27 2024: {M(i, 2024, 'EU27_2020'):.1f}%")
add("Malta electricity share, 2022 -> 2024", f"{M('REN_ELC', 2022):.1f} -> {M('REN_ELC', 2024):.1f}", "%", ES,
    "about one point in four years (9.5% in 2020)")
add("Cyprus total RES share 2020 -> 2024 (island comparator)", f"{M('REN', 2020, 'CY'):.1f} -> {M('REN', 2024, 'CY'):.1f}", "%", ES,
    "Cyprus reached 20.8% in 2024; EU-27 25.2%; Malta 17.2%")
# 5. solar PV
c24 = pv["PV_capacity_end_2024"]
add("Solar PV capacity end-2024", c24, "MWp", "NSO NR 111/2025 (second-hand)", "plan: 241 MWp end-2023 (p.74)")
add("Implied end-2023 capacity from NSO's +4.8%", round(c24 / 1.048, 1), "MWp", "calculated", "matches the plan's 241 MWp")
net24 = pv["PV_connected_2024"] - pv["PV_decommissioned_2024"]
add("Net PV added in 2024", round(net24, 2), "MWp", "NSO NR 111/2025 (second-hand)", "11.792 connected minus 0.262 decommissioned")
tgtpv = inp[("plan_PV_capacity_2030", "2030")]
need = (tgtpv - c24) / 6
add("PV capacity to add per year 2025-2030 to reach 350 MWp", round(need, 1), "MWp/yr", "calculated from NSO and " + PL,
    f"{need / net24:.2f} times the net addition of 2024")
cf = pv["PV_generation_2024"] / c24 * 1000
add("PV output per kWp installed, 2024", round(cf), "kWh/kWp", "calculated from NSO NR 111/2025", "grid-connected generation / end-year capacity")
add("PV output in 2030 at 350 MWp and the 2024 yield", round(tgtpv * cf / 1000), "GWh", "calculated", f"vs {pv['PV_generation_2024']:.1f} GWh in 2024")
# 6. offshore wind
add("Offshore wind counted in the 24.5% contribution", 0, "MW", "Malta final updated NECP p.83",
    "\"offshore wind does not contribute ... as it is not envisaged to be completed and commissioned by 2030\"")
add("Plan's offshore capacity figure", "350 MW by 2030 (p.25) / by 2050 (p.78)", "", "Malta final updated NECP",
    "non-binding TEN-E commitment; the plan gives both dates")
# 7. headline numbers
add("Plan 2030 contribution vs Commission formula", f"24.5 vs 28", "%", "NECP p.83; Commission SWD(2025) 140 s.2.2", "3.5 points below")
add("Plan's own trajectory vs Commission reference points", "16.5 vs 18 (2025); 20.7 vs 22 (2027)", "%", "NECP p.83; Commission s.2.2", "below")
add("Eurostat 2022 RES share now vs in the plan", f"{M('REN', 2022):.2f} vs 13.4", "%", ES + "; NECP p.279", "the two differ; the plan used the SHARES figure available in 2024, Eurostat has since published a higher one")

with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
for r in rows:
    print(f"{r['check']:85s} {str(r['value']):>14} {r['unit']}  {r['note']}")
