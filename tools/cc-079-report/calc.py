#!/usr/bin/env python3
"""CC-079: test WasteServ's statement that the Magħtab waste-to-energy plant 'will be treating around 192,000 tonnes
of non-recyclable waste' and 'is expected to meet around 4.5% of Malta's total energy needs' (26 Jun 2023).

Inputs (all saved with source and retrieval date):
  data/cc-079/document_figures.csv   figures from WasteServ, the NECP (Dec 2024), the Commission and the literature
  data/cc-079/eurostat_*.csv         Eurostat energy balances, electricity, waste (tools/cc-079-report/fetch.py)
Output: data/cc-079/checks.csv (one row per tested figure).

Readings of '4.5% of Malta's total energy needs' tested:
  numerator: the plant's electricity to the grid (WasteServ: 126 GWh a year), the NECP's 14-16 MW, and, as an
             upper bound that is not energy delivered, the energy content of the waste burnt (fuel input);
  denominator: electricity (final consumption; inland demand) and total energy (final energy consumption, primary
             energy consumption, gross inland consumption, gross available energy), for 2019 (before the first
             statement, Oct 2020), 2022 (before the June 2023 statement), 2024 (latest) and the NECP's 2030 projection.
"""
import csv, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-079"
F = {r["key"]: float(r["value"]) for r in csv.DictReader(open(D / "document_figures.csv"))}
SRCF = {r["key"]: f"{r['source']}, {r['locator']}" for r in csv.DictReader(open(D / "document_figures.csv"))}

bal, balflag, BALSRC = {}, {}, ""
for r in csv.DictReader(open(D / "eurostat_nrg_bal_c.csv")):
    k = (r["nrg_bal"], r["siec"], r["unit"], int(r["year"]))
    bal[k] = float(r["value"]); balflag[k] = r["flag"]
    BALSRC = f"Eurostat nrg_bal_c (updated {r['eurostat_updated'][:10]}), retrieved {r['retrieved']}"
ele, ELESRC = {}, ""
for r in csv.DictReader(open(D / "eurostat_nrg_cb_e.csv")):
    ele[(r["nrg_bal"], int(r["year"]))] = float(r["value"])
    ELESRC = f"Eurostat nrg_cb_e (updated {r['eurostat_updated'][:10]}), retrieved {r['retrieved']}"
wm, WMSRC = {}, ""
for r in csv.DictReader(open(D / "eurostat_env_wasmun.csv")):
    wm[(r["wst_oper"], r["unit"], int(r["year"]))] = float(r["value"])
    WMSRC = f"Eurostat env_wasmun (updated {r['eurostat_updated'][:10]}), retrieved {r['retrieved']}"
wt, WTSRC = {}, ""
for r in csv.DictReader(open(D / "eurostat_env_wastrt.csv")):
    wt[(r["wst_oper"], r["waste"], int(r["year"]))] = float(r["value"])
    WTSRC = f"Eurostat env_wastrt (updated {r['eurostat_updated'][:10]}), retrieved {r['retrieved']}"
wg, WGSRC = {}, ""
for r in csv.DictReader(open(D / "eurostat_env_wasgen.csv")):
    wg[(r["waste"], int(r["year"]))] = float(r["value"])
    WGSRC = f"Eurostat env_wasgen (updated {r['eurostat_updated'][:10]}), retrieved {r['retrieved']}"

rows = []


def add(group, check, value, unit, source, note=""):
    rows.append({"group": group, "check": check, "value": value, "unit": unit, "source": source, "note": note})


def r1(x):
    return round(x, 1)


# ------------------------------------------------------------------ unit conversion, from the dataset itself
gwh_per_ktoe = bal[("GIC", "TOTAL", "GWH", 2024)] / bal[("GIC", "TOTAL", "KTOE", 2024)]
add("units", "GWh per ktoe (Eurostat GIC 2024, GWh / ktoe)", round(gwh_per_ktoe, 3), "GWh/ktoe", BALSRC,
    "Eurostat's own conversion; used for the NECP's ktoe projections")

# ------------------------------------------------------------------ A. capacity
cap = F["wasteserv_capacity_t"]
t_per_h = F["necp_lines"] * F["necp_t_per_h_per_line"]
hours = cap / t_per_h
add("A capacity", "Plant throughput in the NECP design (2 lines x 12 t/h)", t_per_h, "t/h", SRCF["necp_t_per_h_per_line"])
add("A capacity", "Full-load hours a year implied by 192,000 t at 24 t/h", round(hours), "h",
    "calc: WasteServ capacity / NECP throughput", f"{100 * hours / 8760:.1f}% of the 8,760 hours in a year")
add("A capacity", "Commission EIR 2025 capacity vs WasteServ's 192,000 t", F["eir2025_capacity_t"], "t/yr", SRCF["eir2025_capacity_t"],
    f"difference {100 * (cap / F['eir2025_capacity_t'] - 1):.1f}%")
for y in (2019, 2022, 2024):
    gen, lf = wm[("GEN", "THS_T", y)], wm[("DSP_L_OTH", "THS_T", y)]
    add("A capacity", f"Malta municipal waste generated, {y}", gen, "kt", WMSRC)
    add("A capacity", f"Malta municipal waste landfilled (D1-D7, D12), {y}", lf, "kt", WMSRC)
    add("A capacity", f"192,000 t as a share of municipal waste landfilled, {y}", r1(100 * cap / 1000 / lf), "%", "calc")
    add("A capacity", f"192,000 t as a share of municipal waste generated, {y}", r1(100 * cap / 1000 / gen), "%", "calc")
lf22 = wt[("DSP_L_OTH", "TOT_X_MIN", 2022)]
gen22 = wg[("TOT_X_MIN", 2022)]
add("A capacity", "All waste excluding major mineral wastes, landfilled (D1-D7, D12), 2022", lf22, "t", WTSRC,
    "includes non-municipal waste; biennial data, 2022 latest")
add("A capacity", "192,000 t as a share of non-mineral waste landfilled, 2022", r1(100 * cap / lf22), "%", "calc")
add("A capacity", "All waste excluding major mineral wastes, generated, 2022", gen22, "t", WGSRC,
    "includes separately collected recyclables")
gen24 = wm[("GEN", "THS_T", 2024)]
resid = gen24 * (1 - F["eu_recycling_target_2035_pct"] / 100)
add("A capacity", "Municipal waste left after the 2035 recycling target (65%), at 2024 generation", r1(resid), "kt",
    SRCF["eu_recycling_target_2035_pct"] + "; " + WMSRC,
    "the most that could go to energy recovery or landfill if the target were met and generation stayed at 2024 level")
add("A capacity", "Plant capacity minus that residual", r1(cap / 1000 - resid), "kt", "calc",
    "positive: the plant would need other waste streams, or the target missed, to run full")
add("A capacity", "Generation at which 35% of municipal waste equals 192,000 t", r1(cap / 1000 / (1 - F["eu_recycling_target_2035_pct"] / 100)), "kt",
    "calc", f"{100 * (cap / 1000 / (1 - F['eu_recycling_target_2035_pct'] / 100) / gen24 - 1):.0f}% above 2024 generation")

# ------------------------------------------------------------------ E. the 40% on the project page
implied = cap / (F["wasteserv_share_nonrecyclable_pct"] / 100)
add("E 40%", "Non-recyclable waste implied by '40%' with 192,000 t", round(implied), "t", "calc: 192,000 / 0.40")
add("E 40%", "192,000 t as a share of all non-mineral waste generated, 2022", r1(100 * cap / gen22), "%", "calc",
    "the widest basis: includes waste already collected for recycling")

# ------------------------------------------------------------------ D. output, efficiency
e_ws = F["wasteserv_output_gwh"]
lo, hi = F["necp_net_mw_low"] * hours / 1000, F["necp_net_mw_high"] * hours / 1000
add("D output", "Net electricity from the NECP's 14-16 MW at the implied full-load hours", f"{lo:.0f}-{hi:.0f}", "GWh/yr", SRCF["necp_net_mw_low"])
add("D output", "Average net output implied by 126 GWh at the implied hours", round(e_ws * 1000 / hours, 2), "MW", "calc")
add("D output", "NECP Figure 120 slice nearest the plant (2030)", F["necp_2030_slice_127_gwh"], "GWh", SRCF["necp_2030_slice_127_gwh"])
heat_line = F["necp_heat_input_mwth_high"]
ncv = heat_line / F["necp_t_per_h_per_line"] * 3.6               # MWth per (t/h) -> MWh/t -> GJ/t
fuel = F["necp_lines"] * heat_line * hours / 1000                # GWh of waste energy a year at full load
add("D output", "Net calorific value implied (33.33 MWth per line at 12 t/h)", round(ncv, 2), "GJ/t", "calc from NECP p. 132",
    "the design calorific value of the waste")
add("D output", "Energy content of 192,000 t at that value (fuel input)", r1(fuel), "GWh/yr", "calc")
add("D output", "Net electrical efficiency: 126 GWh / fuel input", r1(100 * e_ws / fuel), "%", "calc",
    f"literature, small-medium plants: {F['lit_eff_small_low']:.0f}-{F['lit_eff_small_high']:.0f}%; large plants up to {F['lit_eff_large_max']:.0f}%")
add("D output", "Net electrical efficiency: NECP 14-16 MW / 66.67 MWth", f"{100 * F['necp_net_mw_low'] / (2 * heat_line):.1f}-{100 * F['necp_net_mw_high'] / (2 * heat_line):.1f}",
    "%", "calc", "heat input read as per line")
add("D output", "Same, if 33.33 MWth were the total for both lines", f"{100 * F['necp_net_mw_low'] / heat_line:.0f}-{100 * F['necp_net_mw_high'] / heat_line:.0f}",
    "%", "calc", f"above the {F['lit_eff_large_max']:.0f}% the literature gives for the largest plants: reading rejected")
add("D output", "Electricity per tonne (126 GWh / 192,000 t)", round(e_ws * 1e6 / cap), "kWh/t", "calc")

# ------------------------------------------------------------------ B. the 4.5% share
denoms = {
    "Electricity: final consumption (nrg_cb_e FC)": lambda y: ele[("FC", y)],
    "Electricity: inland demand (nrg_cb_e ID)": lambda y: ele[("ID", y)],
    "Total energy: final energy consumption (nrg_bal_c FEC_EED)": lambda y: bal[("FEC_EED", "TOTAL", "GWH", y)],
    "Total energy: final energy use excl. international aviation (nrg_bal_c FC_E)": lambda y: bal[("FC_E", "TOTAL", "GWH", y)],
    "Total energy: primary energy consumption (nrg_bal_c PEC_EED)": lambda y: bal[("PEC_EED", "TOTAL", "GWH", y)],
    "Total energy: gross inland consumption (nrg_bal_c GIC)": lambda y: bal[("GIC", "TOTAL", "GWH", y)],
    "Total energy: gross available energy incl. marine bunkers (nrg_bal_c GAE)": lambda y: bal[("GAE", "TOTAL", "GWH", y)],
}
for y in (2019, 2022, 2023, 2024):
    for name, fn in denoms.items():
        den = fn(y)
        src = ELESRC if name.startswith("Electricity") else BALSRC
        add("B share", f"{y} {name}", r1(den), "GWh", src)
        add("B share", f"{y} 126 GWh as % of {name}", round(100 * e_ws / den, 3), "%", "calc")
        if not name.startswith("Electricity"):
            add("B share", f"{y} fuel input ({fuel:.0f} GWh) as % of {name}", round(100 * fuel / den, 3), "%", "calc",
                "upper bound: counts the waste's whole energy content, most of which is not delivered")
el2030 = sum(F[k] for k in ("necp_2030_conventional_gwh", "necp_2030_slice_1062_gwh", "necp_2030_slice_453_gwh",
                            "necp_2030_slice_127_gwh", "necp_2030_slice_28_gwh"))
add("B share", "2030 NECP electricity generation, all sources (sum of Figure 120)", el2030, "GWh", SRCF["necp_2030_conventional_gwh"])
add("B share", "2030 126 GWh as % of NECP electricity", round(100 * e_ws / el2030, 3), "%", "calc")
for k, lab in (("necp_2030_pec_ktoe", "primary energy consumption"), ("necp_2030_fec_ktoe", "final energy consumption")):
    den = F[k] * gwh_per_ktoe
    add("B share", f"2030 NECP {lab} ({F[k]:.0f} ktoe)", r1(den), "GWh", SRCF[k])
    add("B share", f"2030 126 GWh as % of NECP {lab}", round(100 * e_ws / den, 3), "%", "calc")
    add("B share", f"2030 fuel input as % of NECP {lab}", round(100 * fuel / den, 3), "%", "calc", "upper bound, as above")
for y in (2022, 2024):
    add("B share", f"{y} electricity final consumption as % of final energy consumption (FEC_EED)",
        r1(100 * ele[("FC", y)] / bal[("FEC_EED", "TOTAL", "GWH", y)]), "%", "calc from " + ELESRC + "; " + BALSRC,
        "electricity is about a third of the final energy Malta uses")
need = e_ws / (F["wasteserv_share_pct"] / 100)
add("B share", "Denominator for which 126 GWh is exactly 4.5%", round(need), "GWh", "calc",
    f"= {need / gwh_per_ktoe:.0f} ktoe; Malta's 2024 gross inland consumption was {bal[('GIC', 'TOTAL', 'KTOE', 2024)]:.0f} ktoe")
add("B share", "Ratio of the claimed share to the share of final energy consumption, 2022",
    round(F["wasteserv_share_pct"] / (100 * e_ws / bal[("FEC_EED", "TOTAL", "GWH", 2022)]), 1), "times", "calc")

# ------------------------------------------------------------------ cross-checks
for y, k in ((2022, "necp_2022_pec_ktoe"), (2022, "necp_2022_fec_ktoe")):
    code = "PEC_EED" if "pec" in k else "FEC_EED"
    add("cross-check", f"{code} {y}: Eurostat (ktoe) vs NECP Table 27", f"{bal[(code, 'TOTAL', 'GWH', y)] / gwh_per_ktoe:.1f} vs {F[k]}",
        "ktoe", BALSRC + "; " + SRCF[k])
add("cross-check", "GIC - international aviation = total energy supply (2024)",
    f"{bal[('GIC', 'TOTAL', 'GWH', 2024)] - bal[('INTAVI', 'TOTAL', 'GWH', 2024)]:.1f} vs {bal[('NRGSUP', 'TOTAL', 'GWH', 2024)]:.1f}",
    "GWh", BALSRC, "so final energy use (FC_E) excludes international aviation")
add("cross-check", "Inland demand = net production + imports - exports (2024)",
    f"{ele[('NEP', 2024)] + ele[('IMP', 2024)] - ele[('EXP', 2024)]:.1f} vs {ele[('ID', 2024)]:.1f}", "GWh", ELESRC)
add("cross-check", "Municipal waste incinerated with energy recovery in Malta, 2024", wm[("RCV_E", "THS_T", 2024)], "kt", WMSRC,
    "Malta burns almost no municipal waste for energy today")
add("cross-check", "Electricity from municipal waste in Malta (renewable + non-renewable), 2024",
    bal[("TI_EHG_E", "W6210", "GWH", 2024)] + bal[("TI_EHG_E", "W6220", "GWH", 2024)], "GWh fuel input", BALSRC)

with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for r in rows:
    print(f"{r['group']:11s} {r['check'][:92]:92s} {str(r['value']):>14} {r['unit']:7s} {r['note'][:70]}")
