#!/usr/bin/env python3
"""CC-117: test the Commission's statement (July 2026 infringement package) against Eurostat data.

Reads data/cc-117/eurostat_*.csv (fetch.py; retrieved 13 Oct 2026) and writes data/cc-117/checks.csv.
Targets are those the Commission page lists (Directive 94/62/EC as amended: total packaging 55% minimum, paper and
cardboard 60%, metals 50%, glass 60%, plastics 22.5%, wood 15%, to be reached by 31 Dec 2008) and the 50% municipal
preparing-for-reuse-and-recycling target for 2020 (Directive 2008/98/EC). We did not open the Directives themselves.
Eurostat's recycling rates are Eurostat's own calculation from national reports: indicative of, not identical to, the
compliance calculation the Commission applies.
"""
import csv, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-117"
ES = "Eurostat, retrieved 13 Oct 2026"
EU27 = {"AT", "BE", "BG", "CY", "CZ", "DE", "DK", "EE", "EL", "ES", "FI", "FR", "HR", "HU", "IE", "IT", "LT", "LU", "LV", "MT", "NL", "PL", "PT", "RO", "SE", "SI", "SK"}
rows = []


def add(check, value, unit, source, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": source, "note": note})


mun = {}
for r in csv.DictReader(open(D / "eurostat_cei_wm011.csv")):
    mun[(r["geo"], int(r["time"]))] = float(r["value"])
for y in (2020, 2021, 2022, 2023, 2024):
    add(f"Malta municipal recycling rate {y}", mun[("MT", y)], "%", ES + " cei_wm011",
        f"EU-27 {mun[('EU27_2020', y)]}%")
add("Gap to the 50% target in 2020", round(mun[("MT", 2020)] - 50, 1), "pp", "calculated",
    "target by 2020, Directive 2008/98/EC (as stated on the Commission page)")
add("Years 2020-2024 at or above 50%", sum(mun[("MT", y)] >= 50 for y in range(2020, 2025)), "years", "calculated")
y20 = {g: v for (g, y), v in mun.items() if y == 2020 and g in EU27}
low = sorted((v, g) for g, v in y20.items())
add("Malta's 2020 rank, lowest first", [g for _, g in low].index("MT") + 1, f"of {len(low)}", ES + " cei_wm011",
    "lowest: " + ", ".join(f"{g} {v}%" for v, g in low[:3]))
below = sorted(g for g, v in y20.items() if v < 50)
add("States below 50% in 2020 (Eurostat)", len(below), f"of {len(y20)}", ES + " cei_wm011",
    ", ".join(below) + "; the Commission names 12 states (BG, CZ, DE, EL, ES, HR, CY, HU, MT, PL, PT, RO): "
    "its count rests on the member states' reported compliance data and calculation methods, not on this indicator")

pk = {}
for r in csv.DictReader(open(D / "eurostat_env_waspac.csv")):
    if r["unit"] == "PC" and r["wst_oper"] == "RCY":
        pk[(r["geo"], r["waste"], int(r["time"]))] = (float(r["value"]), r["flag"])
T = {"W1501": ("total packaging", 55), "W150101": ("paper and cardboard packaging", 60),
     "W150104": ("metal packaging", 50), "W150107": ("glass packaging", 60),
     "W150102": ("plastic packaging", 22.5), "W150103": ("wood packaging", 15)}
for code, (lab, tgt) in T.items():
    for y in range(2020, 2024):
        v, fl = pk[("MT", code, y)]
        add(f"Malta {lab} recycling rate {y}", v, "%", ES + " env_waspac",
            f"target {tgt}%: {'met' if v >= tgt else 'missed'} by {abs(round(v - tgt, 1))} pp" + (f"; flag {fl}" if fl else ""))
    miss = [y for y in range(2020, 2024) if pk[("MT", code, y)][0] < tgt]
    add(f"Years 2020-2023 below target, {lab}", len(miss), "of 4", "calculated", "years: " + (", ".join(map(str, miss)) or "none"))
# peer comparison, total packaging 2023
t23 = {g: v for (g, c, y), (v, _) in pk.items() if c == "W1501" and y == 2023 and g in EU27}
add("Member states below 55% total packaging recycling in 2023 (Eurostat)", sum(v < 55 for v in t23.values()), f"of {len(t23)}",
    ES + " env_waspac", ", ".join(f"{g} {t23[g]}%" for g in sorted(t23, key=t23.get) if t23[g] < 55))
add("Malta's 2023 total packaging rate vs EU-27", pk[("MT", "W1501", 2023)][0], "%", ES + " env_waspac",
    f"EU-27 {pk[('EU27_2020', 'W1501', 2023)][0] if ('EU27_2020', 'W1501', 2023) in pk else 'n/a'}")
with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for r in rows:
    print(f"{r['check'][:70]:70s} {r['value']:>8} {r['unit']:6s} {r['note'][:110]}")
