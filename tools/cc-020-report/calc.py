#!/usr/bin/env python3
"""CC-020: test the figures around the EP study on Malta's noise law with formulas, not by eye.

Reads data/cc-020/ (Eurostat ilc_mddw01, retrieved 5 Oct 2026; figures read from the study) and writes checks.csv.
"""
import csv, pathlib
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-020"
S = defaultdict(dict)
for r in csv.DictReader(open(D / "eurostat_noise.csv")):
    S[r["geo"]][int(r["year"])] = float(r["value"])
R23 = {r["geo"]: float(r["value_2023_pct"]) for r in csv.DictReader(open(D / "eurostat_noise_2023_eu27.csv"))}
F = {r["item"]: float(r["value"]) for r in csv.DictReader(open(D / "study_figures.csv"))}
T = {r["item"]: int(r["count"]) for r in csv.DictReader(open(D / "transposition_tally.csv"))}
rows = []


def add(check, value, unit, source, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": source, "note": note})


mt, eu = S["MT"], S["EU27_2020"]
add("Malta: population reporting noise from neighbours or street, 2023", mt[2023], "%", "Eurostat ilc_mddw01")
add("EU-27: same, 2023", eu[2023], "%", "Eurostat ilc_mddw01")
add("Malta minus EU-27, 2023", round(mt[2023] - eu[2023], 1), "points", "calculated")
add("Malta / EU-27, 2023", round(mt[2023] / eu[2023], 2), "ratio", "calculated")
rank = sorted(R23, key=R23.get, reverse=True).index("MT") + 1
add("Malta's rank among EU-27, 2023 (1 = most affected)", rank, f"of {len(R23)}", "calculated",
    f"next: {sorted(R23, key=R23.get, reverse=True)[1]} {sorted(R23.values(), reverse=True)[1]}%")
yrs = [y for y in range(2010, 2024) if y in mt and y in eu]
add("Years 2010-2023 (available) with Malta above EU-27", sum(mt[y] > eu[y] for y in yrs), f"of {len(yrs)}", "calculated")
add("Malta change 2010 -> 2023", f"{mt[2010]} -> {mt[2023]}", "%", "Eurostat ilc_mddw01",
    "2015 shows a drop to 24.6 then recovery; possible series effect not checked")
pop_share = F["Malta share above END Lden 55 dB (percent of population)"]
add("Malta share above END Lden 55 dB (study, EEA 2025a)", pop_share, "%", "study section 2.3",
    "roads and air only, major infrastructure")
add("Self-reported noise problem vs END-threshold exposure", round(mt[2023] / pop_share, 1), "times", "calculated",
    "different concepts: perception of all sources vs modelled exposure to END sources")
add("END Lnight threshold minus WHO road Lnight level", F["END reporting threshold Lnight"] - F["WHO 2018 recommended Lnight road"],
    "dB", "study section 2.1", "END 50 dB, WHO 45 dB")
add("END Lden threshold minus WHO road Lden level", F["END reporting threshold Lden"] - F["WHO 2018 recommended Lden road"],
    "dB", "study section 2.1", "END 55 dB, WHO 53 dB")
add("END Lden threshold minus WHO aircraft Lden level", F["END reporting threshold Lden"] - F["WHO 2018 recommended Lden aircraft"],
    "dB", "study section 2.1", "END 55 dB, WHO 45 dB")
add("EEA-32 road exposure: WHO levels / END thresholds", round(F["EEA-32 road population exposed above WHO levels"] /
    F["EEA-32 road population exposed above END thresholds"], 2), "ratio", "study section 2.1")
n_no, n_yes = T["Transposition table rows marked No"], T["Transposition table rows marked Yes"]
add("Transposition table rows marked No (approx.)", n_no, f"of {n_no + n_yes}", "study Annex 1, our count",
    f"{round(100 * n_no / (n_no + n_yes), 1)}%; authors judge 2 meaningful")
add("Survey: Malta vs EU28 ratio (21% vs 9%)", round(F["Survey: Malta share ranking noise among top four environmental issues (2019)"] /
    F["Survey: EU28 average same question"], 2), "ratio", "study chapter 6, citing ERA 2023c", "in ERA annex pp. 5-6 (read 6 Oct 2026; no survey named); not in Marmara 2019 summary; origin unidentified")

with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
for x in rows:
    print(f"{x['check']:70s} {str(x['value']):>12} {x['unit']:10s} {x['note']}")
