#!/usr/bin/env python3
"""CC-122: reproduce the arithmetic of The Shift's '30,000 additional hotel beds' claim and set it against Eurostat.

Reads data/cc-122/eurostat_tourism.csv (run fetch_eurostat.py first); writes data/cc-122/checks.csv.
The 30,000 beds, the 5 to 6 night stay and the 70% occupancy are The Shift's own inputs, not measured values.
"""
import csv, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-122"
E = {}
for r in csv.DictReader(open(D / "eurostat_tourism.csv")):
    E[(r["dataset"], int(r["year"]))] = float(r["value"])
rows = []


def add(check, value, unit, source, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": source, "note": note})


BEDS, DAYS = 30000, 365
SH = "The Shift, 29 Aug 2026 and 8 Sep 2026 (inputs)"
full = BEDS * DAYS
add("Bed-nights available from 30,000 beds in a year", full, "nights", "calculated", "30,000 x 365 (100% occupancy)")
add("Guest nights at 70% occupancy", round(0.7 * full), "nights", SH,
    "30,000 x 365 x 0.70 = 7.67 million; The Shift: 'approximately 7.7 million' (reproduces)")
for stay in (5, 6):
    add(f"Additional arrivals to fill every bed all year, {stay}-night stay", round(full / stay), "arrivals", SH,
        "100% occupancy; The Shift: 1.8 to 2.2 million (reproduces at 5 and 6 nights)")
    add(f"Additional arrivals at 70% occupancy, {stay}-night stay", round(0.7 * full / stay), "arrivals", "calculated",
        "not stated in the article: at the 70% used for nights, arrivals are lower than 1.8 to 2.2 million")
st = E[("tour_occ_ninat", 2025)] / E[("tour_occ_arnat", 2025)]
add("Nights per arrival at establishments, non-residents, 2025", round(st, 2), "nights",
    "Eurostat tour_occ_ninat / tour_occ_arnat (FOR, I551-I553)", "11,757,807 / 2,555,515; The Shift assumes 5 to 6")
add("Additional arrivals to fill every bed all year at the 2025 observed stay", round(full / st), "arrivals", "calculated")
add("Additional arrivals at 70% occupancy at the 2025 observed stay", round(0.7 * full / st), "arrivals", "calculated")
for y in (2019, 2025):
    add(f"Non-resident arrivals at establishments, {y}", int(E[('tour_occ_arnat', y)]), "arrivals", "Eurostat tour_occ_arnat")
    add(f"Non-resident nights at establishments, {y}", int(E[('tour_occ_ninat', y)]), "nights", "Eurostat tour_occ_ninat")
    add(f"Bed-places in tourist accommodation, {y}", int(E[('tour_cap_nat', y)]), "bed-places", "Eurostat tour_cap_nat")
add("30,000 beds as a share of 2025 bed-places", round(100 * BEDS / E[("tour_cap_nat", 2025)], 1), "%", "calculated",
    "58,099 bed-places in 2025; Eurostat counts all collective establishments (NACE I551-I553), not only hotels")
add("7.67 million extra nights as a share of 2025 non-resident nights at establishments",
    round(100 * 0.7 * full / E[("tour_occ_ninat", 2025)]), "%", "calculated", "11.76 million nights")
add("1.8 to 2.2 million extra arrivals as a share of 2025 non-resident arrivals at establishments",
    f"{100 * 1.8e6 / E[('tour_occ_arnat', 2025)]:.0f} to {100 * 2.2e6 / E[('tour_occ_arnat', 2025)]:.0f}", "%", "calculated",
    "2.56 million arrivals")
add("Nights per bed-place, 2025 (non-resident nights / bed-places)",
    round(E[("tour_occ_ninat", 2025)] / E[("tour_cap_nat", 2025)]), "nights", "calculated",
    "about 55% of the year; residents' nights are not in this series")
add("Growth in bed-places 2015-2025", round(100 * (E[("tour_cap_nat", 2025)] / E[("tour_cap_nat", 2015)] - 1)), "%",
    "Eurostat tour_cap_nat", "42,883 to 58,099; +5,303 in 2025 alone")
add("Bed-places added in 2025", int(E[("tour_cap_nat", 2025)] - E[("tour_cap_nat", 2024)]), "bed-places", "Eurostat tour_cap_nat")
add("Other pipeline figures (second-hand or other measures; not comparable)", "see notes", "",
    "literature/CC-122/notes.md",
    "MTA pipeline 27,672 beds at end April 2024 (Deloitte for MHRA 2024, p. 69, read); about 35,000 collective beds "
    "in open permits (Deloitte for MHRA 2022, p. 25, read); 21 hotels with 2,256 beds approved in two years (The Shift "
    "2023, via parliamentary information, not opened); 44 TPCC projects, 6,239 beds, data to Oct 2025 (search summary "
    "of Business Now, second-hand)")
with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
for x in rows:
    print(f"{x['check'][:80]:80s} {str(x['value']):>12} {x['unit']}")
