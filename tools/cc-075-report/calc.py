#!/usr/bin/env python3
"""CC-075: test Lovin Malta's report that Malta ranks seventh in the EU with 585 passenger cars per 1,000
inhabitants (article of 21 Sep 2024), and the article's other figures.

Reads data/cc-075/ (Eurostat road_eqs_carhab, road_eqs_carmot, demo_gind, reg_area3, retrieved 6 Oct 2026 by
fetch.py with Eurostat's flags; reported_values.csv for figures stated in texts we read, second-hand rows marked);
writes data/cc-075/checks.csv."""
import csv, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-075"
EU27 = "BE BG CZ DK DE EE IE EL ES FR HR IT CY LV LT LU HU MT NL AT PL PT RO SI SK FI SE".split()
NAMES = {"DE": "Germany", "PL": "Poland", "IT": "Italy", "LV": "Latvia", "LU": "Luxembourg", "FI": "Finland",
         "CY": "Cyprus", "EE": "Estonia", "CZ": "Czechia", "NL": "Netherlands", "RO": "Romania", "HU": "Hungary",
         "LT": "Lithuania", "SI": "Slovenia", "EL": "Greece", "FR": "France", "AT": "Austria", "BE": "Belgium"}


def load(f):
    """{(geo, year): (value, flag)}"""
    out = {}
    for r in csv.DictReader(open(D / f)):
        out[(r["geo"], int(r["time"]))] = (float(r["value"]), r.get("flag", ""))
    return out


HAB = load("eurostat_road_eqs_carhab.csv")
STOCK = load("eurostat_road_eqs_carmot.csv")
POP = load("eurostat_demo_gind_jan.csv")
LAND = load("eurostat_reg_area3_land.csv")
REP = list(csv.DictReader(open(D / "reported_values.csv")))
S_HAB = "Eurostat road_eqs_carhab, updated 30 Jul 2026, retrieved 6 Oct 2026"
S_STK = "Eurostat road_eqs_carmot, updated 1 Sep 2026, retrieved 6 Oct 2026"
S_POP = "Eurostat demo_gind (1 January), updated 30 Sep 2026, retrieved 6 Oct 2026"
S_LAND = "Eurostat reg_area3 (land area), updated 22 Jan 2026, retrieved 6 Oct 2026"
rows = []


def add(check, value, unit, source, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": source, "note": note})


def fl(g, y, d=HAB):
    f = d.get((g, y), (None, ""))[1]
    return f"flag '{f}'" if f else "no flag"


def ranked(y, d=HAB):
    return sorted(((d[(g, y)][0], g) for g in EU27 if (g, y) in d), reverse=True)


def rank_of(g, y, d=HAB):
    return [x for _, x in ranked(y, d)].index(g) + 1


def rep(geo, year, indicator, source_start):
    for r in REP:
        if r["geo"] == geo and r["year"] == year and r["indicator"] == indicator and r["source"].startswith(source_start):
            return float(r["value"])
    raise KeyError((geo, year, indicator, source_start))


# ---- A, B: the figure and the rank, 2022 (the year the article's figures match)
y = 2022
r22 = ranked(y)
pos = rank_of("MT", y)
add("Malta: passenger cars per 1,000 inhabitants, 2022", HAB[("MT", y)][0], "per 1,000", S_HAB, fl("MT", y))
add("EU-27 countries with a 2022 value", len(r22), "of 27", S_HAB,
    "flags among the 27: " + ", ".join(f"{g} '{HAB[(g, y)][1]}'" for g in EU27 if HAB[(g, y)][1]))
add("Malta rank among EU-27, 2022 (1 = most cars per person)", pos, "rank", S_HAB)
above, below = r22[pos - 2], r22[pos]
add("Country ranked just above Malta, 2022", above[0], "per 1,000", S_HAB, f"{above[1]} ({NAMES[above[1]]}); {fl(above[1], y)}")
add("Country ranked just below Malta, 2022", below[0], "per 1,000", S_HAB, f"{below[1]} ({NAMES[below[1]]}); {fl(below[1], y)}")
add("Highest EU-27 value, 2022", r22[0][0], "per 1,000", S_HAB, f"{r22[0][1]}; {fl(r22[0][1], y)}")
add("Lowest EU-27 value, 2022", r22[-1][0], "per 1,000", S_HAB, f"{r22[-1][1]}; {fl(r22[-1][1], y)}")
add("EU-27 average, 2022", HAB[("EU27_2020", y)][0], "per 1,000", S_HAB, fl("EU27_2020", y))
gap = [v for v, g in r22]
add("Values of the 5th to 9th places, 2022", f"{gap[4]:.0f}-{gap[8]:.0f}", "per 1,000", S_HAB,
    "5th " + r22[4][1] + ", 9th " + r22[8][1] + f": five countries within {gap[4] - gap[8]:.0f} cars per 1,000")
add("Countries within 5 cars per 1,000 of Malta, 2022",
    ", ".join(f"{g} {v:.0f}" for v, g in r22 if g != "MT" and abs(v - HAB[('MT', y)][0]) <= 5), "list", S_HAB)

every = sorted(((v, g) for (g, yy), (v, _) in HAB.items() if yy == y and not g.startswith("EU")), reverse=True)
higher_non_eu = [f"{g} {v:.0f}" + (f" ('{HAB[(g, y)][1]}')" if HAB[(g, y)][1] else "") for v, g in every
                 if g not in EU27 and v > HAB[("MT", y)][0]]
add("Malta rank among every country in the dataset, 2022", [g for _, g in every].index("MT") + 1, f"of {len(every)}",
    S_HAB, "non-EU countries above Malta: " + ", ".join(higher_non_eu))

# ---- the denominator: stock at 31 Dec / population on 1 Jan of the next year
mt_end = STOCK[("MT", y)][0] / POP[("MT", y + 1)][0] * 1000
mt_start = STOCK[("MT", y)][0] / POP[("MT", y)][0] * 1000
add("Malta: passenger car stock at end of 2022", int(STOCK[("MT", y)][0]), "cars", S_STK, fl("MT", y, STOCK))
add("Malta: population on 1 January 2023", int(POP[("MT", y + 1)][0]), "people", S_POP, fl("MT", y + 1, POP))
add("Malta: stock / population on 1 Jan 2023 x 1,000", round(mt_end, 1), "per 1,000", "calculated",
    "reproduces Eurostat's 585")
add("Malta: stock / population on 1 Jan 2022 x 1,000 (start-of-year denominator)", round(mt_start, 1), "per 1,000",
    "calculated", "for comparison only; Eurostat uses the end-of-year population")
match = [g for g in EU27 if abs(STOCK[(g, y)][0] / POP[(g, y + 1)][0] * 1000 - HAB[(g, y)][0]) <= 1.0]
add("EU-27 countries whose 2022 rate is reproduced by stock / population on 1 Jan 2023 (within 1 per 1,000)",
    len(match), "of 27", "calculated", "the denominator is the population at the end of the reference year")
for yy in (2021, 2022, 2023, 2024, 2025):
    v = STOCK[("MT", yy)][0] / POP[("MT", yy + 1)][0] * 1000
    add(f"Malta {yy}: stock / population on 1 Jan {yy + 1} x 1,000 vs Eurostat", f"{v:.1f} vs {HAB[('MT', yy)][0]:.0f}",
        "per 1,000", "calculated")

# ---- C: what the 2023-2025 data show (published after or around the article)
for yy in (2023, 2024, 2025):
    rr = ranked(yy)
    eu = HAB[("EU27_2020", yy)][0]
    n_above_eu = sum(1 for v, g in rr if v > eu)
    add(f"Malta rank among EU-27, {yy}", rank_of("MT", yy), f"of {len(rr)}", S_HAB,
        f"Malta {HAB[('MT', yy)][0]:.0f} ({fl('MT', yy)}); EU-27 {eu:.0f} ({fl('EU27_2020', yy)}); "
        f"{n_above_eu} countries above the EU-27 value; flagged: "
        + (", ".join(f"{g} '{HAB[(g, yy)][1]}'" for g in EU27 if HAB[(g, yy)][1]) or "none"))
add("Malta minus EU-27, 2025", HAB[("MT", 2025)][0] - HAB[("EU27_2020", 2025)][0], "per 1,000", S_HAB)
add("Malta minus EU-27, 2024", HAB[("MT", 2024)][0] - HAB[("EU27_2020", 2024)][0], "per 1,000", S_HAB)

# ---- trend: Malta's rank over time
hist = []
for yy in range(1990, 2026):
    if ("MT", yy) in HAB:
        hist.append((yy, HAB[("MT", yy)][0], rank_of("MT", yy), len(ranked(yy))))
third = [yy for yy, _, p, _ in hist if p <= 3]
add("Years Malta ranked in the EU-27's top three", f"{len(third)} years", "years", S_HAB,
    ", ".join(map(str, third)))
peak = max(hist, key=lambda h: h[1])
add("Malta's highest value in the series", peak[1], "per 1,000", S_HAB, f"{peak[0]}; rank {peak[2]} of {peak[3]}")
add("Malta: years with no value", ", ".join(str(yy) for yy in range(1990, 2026) if ("MT", yy) not in HAB), "years", S_HAB)
add("Eurostat flags on Malta's series, 1990-2025",
    ", ".join(f"{yy}:{HAB[('MT', yy)][1]}" for yy in range(1990, 2026) if HAB.get(("MT", yy), (0, ""))[1]) or "none",
    "flags", S_HAB)
first_below = min(yy for yy, v, _, _ in hist if ("EU27_2020", yy) in HAB and v < HAB[("EU27_2020", yy)][0])
add("First year Malta's rate is below the EU-27 value", first_below, "year", S_HAB,
    f"Malta {HAB[('MT', first_below)][0]:.0f} vs EU-27 {HAB[('EU27_2020', first_below)][0]:.0f}; EU-27 series starts 2000 (gaps to 2010)")
gap10 = HAB[("MT", 2010)][0] - HAB[("EU27_2020", 2010)][0]
add("Malta minus EU-27, 2010", gap10, "per 1,000", S_HAB)

# ---- population growth vs fleet growth
for a, b in ((2012, 2025), (2021, 2022), (2022, 2025)):
    sg = (STOCK[("MT", b)][0] / STOCK[("MT", a)][0] - 1) * 100
    pg = (POP[("MT", b + 1)][0] / POP[("MT", a + 1)][0] - 1) * 100
    add(f"Malta {a}-{b}: change in car stock vs change in population (end-year)", f"{sg:+.1f}% vs {pg:+.1f}%", "%",
        "calculated from " + S_STK + " and " + S_POP,
        f"stock {int(STOCK[('MT', a)][0]):,} -> {int(STOCK[('MT', b)][0]):,}; population on 1 Jan "
        f"{a + 1} {int(POP[('MT', a + 1)][0]):,} -> {b + 1} {int(POP[('MT', b + 1)][0]):,}")
add("Malta: net addition to the car stock, 2023-2025 (per year)",
    ", ".join(f"{yy}: {int(STOCK[('MT', yy)][0] - STOCK[('MT', yy - 1)][0]):+,}" for yy in (2023, 2024, 2025)),
    "cars", S_STK)
add("Malta: years 2006-2025 in which the car stock fell", ", ".join(
    str(yy) for yy in range(2006, 2026) if STOCK[("MT", yy)][0] < STOCK[("MT", yy - 1)][0]) or "none", "years", S_STK)

# ---- D: Italy and Latvia, and vintages
add("Italy 2022: article / Eurostat news (Jan 2024) / dataset now",
    f"{rep('IT', 'unstated', 'passenger cars per 1000 inhabitants', 'Lovin'):.0f} / "
    f"{rep('IT', '2022', 'passenger cars per 1000 inhabitants', 'Eurostat news'):.0f} / {HAB[('IT', 2022)][0]:.0f}",
    "per 1,000", "reported_values.csv; " + S_HAB, fl("IT", 2022))
add("Latvia 2022: article / Eurostat news (Jan 2024) / dataset now",
    f"{rep('LV', 'unstated', 'passenger cars per 1000 inhabitants', 'Lovin'):.0f} / "
    f"{rep('LV', '2022', 'passenger cars per 1000 inhabitants', 'Eurostat news'):.0f} / {HAB[('LV', 2022)][0]:.0f}",
    "per 1,000", "reported_values.csv; " + S_HAB, fl("LV", 2022) + " (b = break in time series)")
for g in ("LU", "FI", "CY"):
    add(f"{NAMES[g]} 2022: Eurostat news (Jan 2024) / dataset now",
        f"{rep(g, '2022', 'passenger cars per 1000 inhabitants', 'Eurostat news'):.0f} / {HAB[(g, 2022)][0]:.0f}",
        "per 1,000", "reported_values.csv; " + S_HAB, "revised since the January 2024 release")
add("EU-27 2022: Eurostat news (Jan 2024) / dataset now",
    f"{rep('EU27_2020', '2022', 'passenger cars per 1000 inhabitants', 'Eurostat news'):.0f} / {HAB[('EU27_2020', 2022)][0]:.0f}",
    "per 1,000", "reported_values.csv; " + S_HAB)

# ---- E: 'approximately 1 car for every 2 people'
add("People per passenger car in Malta, 2022 (1,000 / 585)", round(1000 / HAB[("MT", 2022)][0], 2), "people", "calculated",
    "the article: 'approximately 1 car for every 2 people'")
add("Passenger cars per person in Malta, 2022", round(HAB[("MT", 2022)][0] / 1000, 3), "cars", "calculated")

# ---- F: land area and cars per km2 of land
land_mt = LAND[("MT", 2022)][0]
add("Malta: land area (whole country), 2022", land_mt, "km2", S_LAND, fl("MT", 2022, LAND))
add("Malta island (NUTS 3 MT001): land area, 2022", LAND[("MT001", 2022)][0], "km2", S_LAND, "the article: 246 km2")
add("Gozo and Comino (MT002): land area, 2022", LAND[("MT002", 2022)][0], "km2", S_LAND)
dens = sorted(((STOCK[(g, y)][0] / LAND[(g, y)][0], g) for g in EU27 if (g, y) in STOCK and (g, y) in LAND), reverse=True)
add("EU-27 countries with both car stock and land area, 2022", len(dens), "of 27", "calculated")
add("Malta: passenger cars per km2 of land, 2022", round(dens[0][0]) if dens[0][1] == "MT" else None, "cars/km2",
    "calculated", f"rank {[g for _, g in dens].index('MT') + 1} of {len(dens)}")
add("Second-highest EU-27 cars per km2 of land, 2022", round(dens[1][0]), "cars/km2", "calculated",
    f"{dens[1][1]} ({NAMES.get(dens[1][1], dens[1][1])}); Malta / second = {dens[0][0] / dens[1][0]:.1f}x")
add("Malta: cars per km2 if only Malta island's land (245 km2) were used, 2022",
    round(STOCK[("MT", y)][0] / LAND[("MT001", 2022)][0]), "cars/km2", "calculated",
    "for comparison; the stock is national")
d25 = sorted(((STOCK[(g, 2025)][0] / LAND[(g, 2025)][0], g) for g in EU27 if (g, 2025) in STOCK and (g, 2025) in LAND),
             reverse=True)
add("Malta: passenger cars per km2 of land, 2025", round(dict((g, v) for v, g in d25)["MT"]), "cars/km2", "calculated",
    f"rank {[g for _, g in d25].index('MT') + 1} of {len(d25)}")

# ---- registered vs licensed: Eurostat stock vs NSO licensed stock (NSO second-hand)
nso_total = rep("MT", "2022", "licensed motor vehicles at end of December", "NSO")
nso_share = rep("MT", "2022", "share of passenger cars in licensed stock (%)", "NSO")
lo, hi = nso_total * (nso_share - 0.05) / 100, nso_total * (nso_share + 0.05) / 100
add("NSO licensed passenger cars, end 2022, implied by 74.7% of 424,904 (second-hand)",
    f"{nso_total * nso_share / 100:,.0f} ({lo:,.0f}-{hi:,.0f} for 74.65-74.75%)", "cars", "NSO News2023_023 via search summary ◆",
    f"Eurostat stock {int(STOCK[('MT', 2022)][0]):,}: inside the range" if lo <= STOCK[("MT", 2022)][0] <= hi
    else f"Eurostat stock {int(STOCK[('MT', 2022)][0]):,}: outside the range")

with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for r in rows:
    print(f"{r['check'][:96]:96s} {r['value']!s:>16} {r['unit']}  {r['note']}")
