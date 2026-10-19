#!/usr/bin/env python3
"""CC-124: test the checkable statements in the CCPI 2026 Malta country text with formulas.

Reads data/cc-124/ (Eurostat, retrieved by fetch.py) and writes data/cc-124/checks.csv.
The CCPI statements are typed in below exactly as printed on https://ccpi.org/country/mlt/ (read 18 and 19 Oct 2026).
"""
import csv, pathlib
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-124"


def load(name):
    return list(csv.DictReader(open(D / f"eurostat_{name}.csv")))


CARS = defaultdict(dict)      # (geo, mot_nrg) -> year -> value
for r in load("cars"):
    CARS[(r["geo"], r["mot_nrg"])][int(r["time"])] = float(r["value"])
HAB = defaultdict(dict)
for r in load("carhab"):
    HAB[r["geo"]][int(r["time"])] = float(r["value"])
FUEL = {int(r["time"]): float(r["value"]) for r in load("fuel")}
MODAL = defaultdict(dict)
MODFLAG = {}
for r in load("modal"):
    MODAL[r["vehicle"]][int(r["time"])] = float(r["value"])
    MODFLAG[(r["vehicle"], int(r["time"]))] = r["flag"]
REN = defaultdict(dict)
RENFLAG = {}
for r in load("ren"):
    REN[r["geo"]][int(r["time"])] = float(r["value"])
    RENFLAG[(r["geo"], int(r["time"]))] = r["flag"]
GHG = defaultdict(dict)
for r in load("ghg"):
    GHG[r["unit"]][int(r["time"])] = float(r["value"])
POP = {int(r["time"]): float(r["value"]) for r in load("pop")}

rows = []


def add(check, value, unit, source, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": source, "note": note})


pc = lambda a, b: round(100 * (b - a) / a, 1)
rank_low = lambda d, k, y: sorted(g for g in d if g not in ("EU27_2020",) and y in d[g]) and \
    1 + sum(1 for g in d if g != "EU27_2020" and y in d[g] and d[g][y] < d[k][y])

# ---- A. rank (second-hand, internal arithmetic only) --------------------------------------------------------------
add("Rank change implied by CCPI text", 34 - 25, "places", "Wikipedia CCPI table (second-hand); ccpi.org/country/mlt",
    "CCPI: 'up nine spots' to 25th; 2025 edition 34th (second-hand): 34 - 25 = 9; internally consistent, scores not tested")

# ---- B. automobile use ---------------------------------------------------------------------------------------------
t = CARS[("MT", "TOTAL")]
add("Passenger cars registered, 2022", int(t[2022]), "cars", "Eurostat road_eqs_carpda", "")
add("Passenger cars registered, 2025", int(t[2025]), "cars", "Eurostat road_eqs_carpda", "")
add("Change in passenger cars 2022-2025", pc(t[2022], t[2025]), "%", "Eurostat road_eqs_carpda",
    f"+{int(t[2025] - t[2022])} cars; free public transport began Oct 2022")
add("Change in population 2022-2025 (1 Jan values 2023 vs 2026)", pc(POP[2023], POP[2026]), "%", "Eurostat demo_gind",
    "denominator for per-head measures; 1 Jan 2023 and 1 Jan 2026")
h = HAB["MT"]
add("Cars per 1,000 inhabitants, Malta 2022 / 2025", f"{int(h[2022])} / {int(h[2025])}", "per 1,000", "Eurostat road_eqs_carhab",
    f"EU-27 {int(HAB['EU27_2020'][2022])} / {int(HAB['EU27_2020'][2025])}; Malta falls because population grew faster than the fleet")
add("Cars per 1,000 inhabitants, Malta 2018 / 2025", f"{int(h[2018]) if 2018 in h else 'n/a'} / {int(h[2025])}", "per 1,000",
    "Eurostat road_eqs_carhab", "")
add("Road-transport final energy, 2022", FUEL[2022], "ktoe", "Eurostat nrg_bal_c FC_TRA_ROAD_E", "all fuels")
add("Road-transport final energy, 2024", FUEL[2024], "ktoe", "Eurostat nrg_bal_c FC_TRA_ROAD_E", "2025 not yet published")
add("Change in road-transport energy 2022-2024", pc(FUEL[2022], FUEL[2024]), "%", "Eurostat nrg_bal_c",
    "2019 (pre-COVID) was %.1f ktoe: 2024 is %s%% on 2019" % (FUEL[2019], pc(FUEL[2019], FUEL[2024])))
per22 = FUEL[2022] / POP[2023] * 1e3 * 1e3   # ktoe -> toe; per 1,000 persons => toe/1000 pop; report toe per person x1000
per24 = FUEL[2024] / POP[2025] * 1e3 * 1e3
add("Road-transport energy per resident, 2022 -> 2024", f"{per22:.0f} -> {per24:.0f}", "kgoe per resident",
    "Eurostat nrg_bal_c; demo_gind", f"{pc(per22, per24)}% (population on 1 Jan 2023 and 1 Jan 2025: a different timing from fuel years)")
c, b = MODAL["CAR"], MODAL["BUS_TOT"]
add("Car share of inland passenger-km, 2022 / 2023 / 2024", f"{c[2022]} / {c[2023]} / {c[2024]}", "%",
    "Eurostat tran_hv_psmod", "flag 'e' (estimated) on every Malta value; shares exclude walking and cycling")
add("Bus (incl. coach, trolley) share, 2022 / 2023 / 2024", f"{b[2022]} / {b[2023]} / {b[2024]}", "%",
    "Eurostat tran_hv_psmod", f"change in car share 2022-2024 {round(c[2024] - c[2022], 1)} percentage points; 2019: car {c[2019]}, bus {b[2019]}")

# ---- C. electric vehicles --------------------------------------------------------------------------------------------
e = CARS[("MT", "ELC")]
add("Battery-electric cars, 2021 -> 2025", f"{int(e[2021])} -> {int(e[2025])}", "cars", "Eurostat road_eqs_carpda ELC",
    f"x{e[2025] / e[2021]:.1f}; 2022: {int(e[2022])}")
add("Battery-electric share of the fleet, Malta 2025", round(100 * e[2025] / t[2025], 2), "%", "Eurostat road_eqs_carpda", "")
ee, et = CARS[("EU27_2020", "ELC")], CARS[("EU27_2020", "TOTAL")]
add("Battery-electric share of the fleet, EU-27 2025", round(100 * ee[2025] / et[2025], 2), "%", "Eurostat road_eqs_carpda", "")
ph = CARS[("MT", "ELC_PET_PI")]
add("Battery-electric + plug-in hybrid share, Malta 2025", round(100 * (e[2025] + ph[2025]) / t[2025], 2), "%", "Eurostat road_eqs_carpda",
    "EU-27: %.2f%%" % (100 * (ee[2025] + CARS[("EU27_2020", "ELC_PET_PI")][2025]) / et[2025]))
add("Fleet growth 2022-2025 explained by battery-electric (gain)", int(e[2025] - e[2022]), "cars", "Eurostat road_eqs_carpda",
    f"total fleet gain {int(t[2025] - t[2022])}")

# ---- D. renewables ----------------------------------------------------------------------------------------------------
m, eu = REN["MT"], REN["EU27_2020"]
add("Renewable share of gross final energy consumption, Malta 2019", m[2019], "%", "Eurostat nrg_ind_ren", "")
add("Renewable share of gross final energy consumption, Malta 2024", m[2024], "%", "Eurostat nrg_ind_ren", f"EU-27 {eu[2024]}%")
add("Renewable share, Malta 2025 (provisional)", m[2025], "%", "Eurostat nrg_ind_ren", f"EU-27 {eu[2025]}% (flag {RENFLAG[('MT', 2025)]})")
add("Rank of Malta from lowest, 2024", rank_low(REN, "MT", 2024), "of 27", "Eurostat nrg_ind_ren",
    "lowest three: " + ", ".join(f"{g} {REN[g][2024]}" for g in sorted((g for g in REN if g != 'EU27_2020'), key=lambda g: REN[g][2024])[:3]))
add("Rank of Malta from lowest, 2025 (provisional)", rank_low(REN, "MT", 2025), "of 27", "Eurostat nrg_ind_ren",
    "lowest four: " + ", ".join(f"{g} {REN[g][2025]}" for g in sorted((g for g in REN if g != 'EU27_2020'), key=lambda g: REN[g][2025])[:4]))
add("Increase in Malta's renewable share 2019-2024", round(m[2024] - m[2019], 1), "percentage points", "Eurostat nrg_ind_ren",
    f"EU-27 {round(eu[2024] - eu[2019], 1)} points")

# ---- E. emissions -------------------------------------------------------------------------------------------------------
pcap, idx, mt = GHG["T_HAB"], GHG["I90"], GHG["MTCO2E"]
add("GHG per capita excl. LULUCF, Malta 2022 / 2023 / 2024", f"{pcap[2022]} / {pcap[2023]} / {pcap[2024]}", "t CO2e", "Eurostat sdg_13_10",
    f"2018: {pcap[2018]}; change 2022-2024 {pc(pcap[2022], pcap[2024])}%")
add("GHG index (1990 = 100), Malta 2022 / 2024", f"{idx[2022]} / {idx[2024]}", "index", "Eurostat sdg_13_10",
    f"total {mt[2022]} -> {mt[2024]} Mt CO2e ({pc(mt[2022], mt[2024])}%); 2015 index {idx[2015]}")

with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, ["check", "value", "unit", "source", "note"], lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
for r in rows:
    print(r["check"], "|", r["value"], r["unit"], "|", r["note"])
