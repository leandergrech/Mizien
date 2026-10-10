#!/usr/bin/env python3
"""CC-085: test the MHRA's "4.7 million tourists ... 80 percent occupancy" figure.

Wording (MHRA president Tony Zahra, Horeca Malta, 23 Dec 2022): the Deloitte report "concluded that Malta will need to
attract 4.7 million tourists each spending an average of 7 nights in Malta" to "reach 80 percent occupancy throughout the
year", counting beds operating and those approved or being approved. Again (Malta Independent on Sunday, via Malta
Business Weekly 28 Nov 2024): "If we want the 80% occupancy rate of hotels we had in 2019, with the number of beds we have,
we need 4.7 million tourists."

Inputs (all saved under data/cc-085/):
  mhra_studies.csv               transcribed tables of the 2022 study, its launch slides and the 2024 update (page refs)
  eurostat_tourism.csv           Eurostat tour_cap_nat, tour_occ_anor, tour_occ_arnat, tour_occ_ninat (fetch.py)
  inbound_tourists_secondhand.csv NSO inbound tourists, all second-hand (via the studies or outlets)
Output: data/cc-085/checks.csv (check, value, unit, source, note). Second-hand values are marked in 'source'.
"""
import csv
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-085"

M = {}
for r in csv.DictReader(open(D / "mhra_studies.csv", encoding="utf-8")):
    M[(r["doc"], int(r["page"]), r["item"], r["scenario"], r["unit"])] = float(r["value"])
E = {}
for r in csv.DictReader(open(D / "eurostat_tourism.csv", encoding="utf-8")):
    E[(r["dataset"], r["series"], int(r["year"]))] = float(r["value"])
upd = sorted({r["eurostat_updated"][:10] for r in csv.DictReader(open(D / "eurostat_tourism.csv", encoding="utf-8"))})
INB = {int(r["year"]): r for r in csv.DictReader(open(D / "inbound_tourists_secondhand.csv", encoding="utf-8"))}

S22 = "Deloitte for MHRA, Carrying Capacity Study (2022)"
SL = "Deloitte for MHRA, launch slides (Sep 2022)"
S24 = "Deloitte for MHRA, Market update (24 Sep 2024)"
ES = f"Eurostat ({', '.join(upd)} releases), retrieved 10 Oct 2026"
SH = "second-hand (◆)"
rows = []


def add(check, value, unit, source, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": source, "note": note})


def m(doc, page, item, scen, unit=None):
    hits = [v for (d, p, i, sc, u), v in M.items() if (d, p, i, sc) == (doc, page, item, scen) and unit in (None, u)]
    assert len(hits) == 1, (doc, page, item, scen, unit, hits)
    return hits[0]


SC = ["Base FY19", "Sc1", "Sc2", "Sc3"]

# The study labels the stay "7" but divides by the 2019 ratio of guest nights to arrivals (p. 66 inputs, NSO data).
arr19 = m("TCC2022", 66, "Total number of arrivals", "Base FY19")
n19 = m("TCC2022", 66, "FY19 guest nights", "Base FY19")
ALOS19 = n19 / arr19

# ---------------------------------------------------------------- 1. the 2022 study's bed-stock table (p. 27)
non_rented_2019 = m("TCC2022", 66, "Total number of arrivals", "Base FY19") - m("TCC2022", 27, "Total implied demand required", "Base FY19", "arrivals")
for s in SC:
    cb = m("TCC2022", 27, "Collective: updated supply of bed stock", s)
    pb = m("TCC2022", 27, "Private: updated supply of bed stock", s)
    cd = m("TCC2022", 27, "Collective: implied demand required", s)
    pdm = m("TCC2022", 27, "Private: implied demand required", s)
    # occupancy implied by the table's own figures (printed to one decimal as 76.7% and 59.3%)
    occ_c = cd / (cb * 365)
    occ_p = pdm / m("TCC2022", 27, "Private: implied number of available guest nights", s)
    arr = (cd + pdm) / ALOS19
    printed = m("TCC2022", 27, "Total implied demand required", s, "arrivals")
    add(f"2022 study p. 27, {s}: rented arrivals = (collective + private demand nights) / 2019 stay (7.024)",
        f"{arr:,.0f}", "arrivals", S22 + ", p. 27",
        f"collective {cb:,.0f} beds x 365 x {occ_c:.2%} = {cd:,.0f} nights; private {pb:,.0f} beds, {pdm:,.0f} nights "
        f"(occupancy {occ_p:.2%}); printed {printed:,.0f}")
add("2022 study: tourists in non-rented accommodation in 2019 (p. 66 total minus p. 27 rented)", f"{non_rented_2019:,.0f}", "arrivals",
    S22 + ", pp. 27 and 66", "2,753,240 - 2,239,319; held constant in the slides' scenarios")
for s, slide in zip(["Sc1", "Sc2", "Sc3"], [4.1, 4.3, 4.5]):
    tot = (m("TCC2022", 27, "Collective: implied demand required", s) + m("TCC2022", 27, "Private: implied demand required", s)) \
        / ALOS19 + non_rented_2019
    add(f"2022 slides, {s}: arrivals required for 2019 occupancy (rented + non-rented)", f"{tot / 1e6:.2f}", "million",
        S22 + " p. 27 and " + SL + " slide 11", f"slide prints {slide}m; reproduced {tot:,.0f}")

# ---------------------------------------------------------------- 2. the 2022 study's connectivity table (p. 66): the 4.7 million
add("2022 study: 2019 average length of stay = 2019 guest nights / 2019 arrivals", f"{n19 / arr19:.3f}", "nights",
    S22 + ", p. 66 (NSO data, " + SH + " for NSO)", f"{n19:,.0f} / {arr19:,.0f}; table labels it 7")
for s, g in zip(["Sc1", "Sc2", "Sc3"], [0.6, 0.7, 0.8]):
    calc = arr19 * (1 + g)
    printed = m("TCC2022", 66, "Total number of arrivals", s)
    add(f"2022 study p. 66, {s} (+{g:.0%} guest nights): arrivals = 2019 arrivals x {1 + g:.1f}", f"{calc:,.0f}", "arrivals",
        S22 + ", p. 66", f"printed {printed:,.0f}; difference {printed - calc:+.0f}")
add("2022 study: the claim's 4.7 million is p. 66's Sc2", f"{m('TCC2022', 66, 'Total number of arrivals', 'Sc2'):,.0f}", "arrivals",
    S22 + ", p. 66", "Sc2 = +70% guest nights on 2019 at 2019 occupancy and 7-night stays; Sc1 4.41m, Sc3 4.96m")

# ---------------------------------------------------------------- 3. the same bed scenarios at the claim's 80% occupancy
for s in ["Sc1", "Sc2", "Sc3"]:
    cb = m("TCC2022", 27, "Collective: updated supply of bed stock", s)
    pb = m("TCC2022", 27, "Private: updated supply of bed stock", s)
    both = (cb + pb) * 365 * 0.80 / ALOS19 + non_rented_2019
    coll_only = (cb * 365 * 0.80 + m("TCC2022", 27, "Private: implied demand required", s)) / ALOS19 + non_rented_2019
    add(f"2022 study beds, {s}, at 80% occupancy in collective and private rented beds (2019 stay, + non-rented)", f"{both / 1e6:.2f}",
        "million", S22 + " p. 27 inputs; 80% from the claim", f"{both:,.0f}")
    add(f"2022 study beds, {s}, at 80% occupancy in collective beds only (private at 59.3%)", f"{coll_only / 1e6:.2f}", "million",
        S22 + " p. 27 inputs; 80% from the claim", f"{coll_only:,.0f}")

# ---------------------------------------------------------------- 4. the 2024 update (pp. 9, 69, 72, 74)
b23 = m("UPDATE2024", 72, "2023 licenced bed stock", "2023")
pipe = m("UPDATE2024", 69, "Equivalent additional beds", "pipeline")
add("2024 update: MTA-approved pipeline as a share of 2023 licensed collective beds", f"{100 * pipe / b23:.1f}", "%",
    S24 + ", pp. 69 and 72 (MTA data, end April 2024)", f"{pipe:,.0f} beds / {b23:,.0f} beds; 13,543 rooms in 483 establishments")
for s, ret, rl in [("Sc1", .05, .6), ("Sc2", .10, .8), ("Sc3", .15, 1.0)]:
    beds = b23 * (1 - ret) + pipe * rl
    nights = beds * 365 * 0.658
    coll = nights / 4.7 - 388000
    add(f"2024 update, {s}: collective arrivals = beds x 365 x 65.8% / 4.7 - local demand", f"{coll:,.0f}", "arrivals",
        S24 + ", p. 72", f"beds {beds:,.0f} (printed {m('UPDATE2024', 72, 'Projected total beds', s):,.0f}); printed "
        f"{m('UPDATE2024', 72, 'Total arrivals required (collective)', s) * 1000:,.0f} (within 0.4%: occupancy and stay are printed rounded)")
tot3 = sum(m("UPDATE2024", 74, k, "Sc3") for k in ["Scenario B: tourist arrivals - collective",
                                                   "Scenario B: tourist arrivals - rented accommodation",
                                                   "Scenario B: tourist arrivals - non-rented accommodation"])
add("2024 update, Sc3 (full pipeline, 15% retired): total arrivals", f"{tot3:,.0f}", "thousand", S24 + ", p. 74",
    f"printed {m('UPDATE2024', 74, 'Scenario B: total tourist arrivals', 'Sc3'):,.0f} thousand ('4.4m')")
noret = b23 * 0.15 * 365 * 0.658 / 4.7
add("2024 update: extra collective arrivals if no beds retired (6,595 beds x 365 x 65.8% / 4.7)", f"{noret:,.0f}", "arrivals",
    S24 + ", pp. 9 and 72", f"printed 338 thousand; total {tot3 / 1000 + noret / 1e6:.2f}m ('4.8m')")

# ---------------------------------------------------------------- 5. hotel occupancy in 2019 and since (Eurostat; MHRA survey)
rm = lambda y: E[("tour_occ_anor", "accomunit=BEDRM|hotelsize=TOTAL|unit=PC", y)]
bp = lambda y: E[("tour_occ_anor", "accomunit=BEDPL|hotelsize=TOTAL|unit=PC", y)]
add("Hotels: net room occupancy, 2019", rm(2019), "%", ES + " (tour_occ_anor)", f"bed-places {bp(2019)}%")
add("Hotels: net room occupancy, 2025", rm(2025), "%", ES + " (tour_occ_anor)", f"bed-places {bp(2025)}%")
yrs = [y for y in range(2012, 2026)]
best = max(yrs, key=rm)
add("Hotels: highest net room occupancy, 2012-2025", rm(best), "%", ES + " (tour_occ_anor)",
    f"in {best}; years at or above 80%: {sum(rm(y) >= 80 for y in yrs)}")
add("2022 study: 2019 occupancy assumed for collective / private rented beds", "76.7 / 59.3", "%", S22 + ", p. 27",
    "the scenarios hold these rates; no 80% occupancy condition appears in the report or slides (text searched)")
for cat in ["5-star", "4-star"]:
    add(f"MHRA/Deloitte hotel performance survey: {cat} occupancy, 2019", m("UPDATE2024", 27, f"Hotel occupancy, {cat}", "2019"), "%",
        S24 + ", p. 27 (chart label)", f"2023: {m('UPDATE2024', 27, f'Hotel occupancy, {cat}', '2023')}%")

# ---------------------------------------------------------------- 6. bed stock since 2019 (Eurostat)
cap = lambda nace, unit, y: E[("tour_cap_nat", f"nace_r2={nace}|accomunit={unit}|unit=NR", y)]
for nace, lab in [("I551", "hotels"), ("I551-I553", "all tourist accommodation establishments")]:
    a, b = cap(nace, "BEDPL", 2019), cap(nace, "BEDPL", 2025)
    add(f"Bed-places in {lab}, 2019 to 2025", f"{100 * (b / a - 1):+.1f}", "%", ES + " (tour_cap_nat)", f"{a:,.0f} -> {b:,.0f}")
a, b = cap("I551", "BEDRM", 2019), cap("I551", "BEDRM", 2025)
add("Hotel bedrooms, 2019 to 2025", f"{100 * (b / a - 1):+.1f}", "%", ES + " (tour_cap_nat)", f"{a:,.0f} -> {b:,.0f}")
add("Hotel bed-places, 2024 to 2025", f"{100 * (cap('I551', 'BEDPL', 2025) / cap('I551', 'BEDPL', 2024) - 1):+.1f}", "%",
    ES + " (tour_cap_nat)", f"{cap('I551', 'BEDPL', 2024):,.0f} -> {cap('I551', 'BEDPL', 2025):,.0f}")
a, b = cap("I551", "ESTBL", 2019), cap("I551", "ESTBL", 2025)
add("Hotels and similar establishments, 2019 to 2025", f"{b - a:+,.0f}", "establishments", ES + " (tour_cap_nat)", f"{a:,.0f} -> {b:,.0f}")
add("2022 study scenarios: collective bed stock growth assumed over 4-5 years", "+80 to +100", "%", S22 + ", pp. 25 and 27",
    "stakeholder consensus; c. 35,000 beds in open permits")

# ---------------------------------------------------------------- 7. nights and stays at establishments (Eurostat)
ni = lambda nace, res, y: E[("tour_occ_ninat", f"nace_r2={nace}|c_resid={res}|unit=NR", y)]
ar = lambda nace, res, y: E[("tour_occ_arnat", f"nace_r2={nace}|c_resid={res}|unit=NR", y)]
for y in (2019, 2025):
    add(f"Nights per arrival at tourist accommodation establishments, {y}", f"{ni('I551-I553', 'TOTAL', y) / ar('I551-I553', 'TOTAL', y):.2f}",
        "nights", ES + " (tour_occ_ninat / tour_occ_arnat)",
        f"{ni('I551-I553', 'TOTAL', y):,.0f} / {ar('I551-I553', 'TOTAL', y):,.0f}; foreign residents "
        f"{ni('I551-I553', 'FOR', y) / ar('I551-I553', 'FOR', y):.2f}")
s19 = ni("I551-I553", "TOTAL", 2019) / ar("I551-I553", "TOTAL", 2019)
s25 = ni("I551-I553", "TOTAL", 2025) / ar("I551-I553", "TOTAL", 2025)
add("Change in nights per arrival at establishments, 2019 to 2025", f"{100 * (s25 / s19 - 1):+.1f}", "%", ES, "shorter stays need more arrivals for the same nights")
add("2022 study Sc2 arrivals if stays were shorter by that change", f"{m('TCC2022', 66, 'Total number of arrivals', 'Sc2') * s19 / s25 / 1e6:.2f}",
    "million", S22 + " p. 66 and " + ES, "sensitivity: the study's nights held, the stay shortened in proportion")
add("Nights at tourist accommodation establishments, 2019 to 2025",
    f"{100 * (ni('I551-I553', 'TOTAL', 2025) / ni('I551-I553', 'TOTAL', 2019) - 1):+.1f}", "%", ES + " (tour_occ_ninat)",
    f"{ni('I551-I553', 'TOTAL', 2019):,.0f} -> {ni('I551-I553', 'TOTAL', 2025):,.0f}")

# ---------------------------------------------------------------- 8. inbound tourists since 2019 (all second-hand)
t19, t25 = float(INB[2019]["inbound_tourists"]), float(INB[2025]["inbound_tourists"])
add("Inbound tourists, 2025", f"{t25:,.0f}", "tourists", SH + ": " + INB[2025]["source"], "NSO release itself 403")
add("Inbound tourists, 2019 to 2025", f"{100 * (t25 / t19 - 1):+.1f}", "%", SH + ": NSO via the 2022 study and Malta Business Weekly")
add("Inbound tourists in 2025 as a share of 4.7 million", f"{100 * t25 / 4.7e6:.1f}", "%", SH)
for y in (2019, 2023, 2025):
    r = INB[y]
    add(f"Average stay of inbound tourists, {y}", f"{float(r['nights']) / float(r['inbound_tourists']):.2f}", "nights",
        SH + ": " + r["source"])

with open(D / "checks.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
for r in rows:
    print(f"{r['check'][:84]:84s} {str(r['value']):>14} {r['unit'][:9]:9s} {r['note'][:90]}")
