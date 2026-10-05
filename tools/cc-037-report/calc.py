#!/usr/bin/env python3
"""CC-037: test the Amphora claim (35% reported pollution in 2023, highest in the EU, ~3x the EU average of 12%,
higher earners more affected).
Reads data/cc-037/eurostat_ilc_mddw02.csv and eurostat_ilc_li02.csv (both retrieved 5 Oct 2026 by fetch.py, with
Eurostat's flags); writes data/cc-037/checks.csv."""
import csv, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-037"
EU27 = "BE BG CZ DK DE EE IE EL ES FR HR IT CY LV LT LU HU MT NL AT PL PT RO SI SK FI SE".split()
AGG = ("EU", "EA")   # prefixes of aggregates (EU27_2020, EU28, EA20 ...), excluded from country rankings


def load(f, **flt):
    """{(geo, year): (value, flag)} for rows matching flt."""
    out = {}
    for r in csv.DictReader(open(D / f)):
        if all(r[k] == v for k, v in flt.items()):
            out[(r["geo"], int(r["time"]))] = (float(r["value"]), r.get("flag", ""))
    return out


raw = load("eurostat_ilc_mddw02.csv", hhcomp="TOTAL", rskpovth="TOTAL")
pol = {k: v for k, (v, _) in raw.items()}
flag = {k: f for k, (_, f) in raw.items()}
pol_hi = {k: v for k, (v, _) in load("eurostat_ilc_mddw02.csv", hhcomp="TOTAL", rskpovth="A_60").items()}
pol_lo = {k: v for k, (v, _) in load("eurostat_ilc_mddw02.csv", hhcomp="TOTAL", rskpovth="B_60").items()}
arop = {k: v for k, (v, _) in load("eurostat_ilc_li02.csv", rskpovth="B_60").items()}
rows = []
S2 = "Eurostat ilc_mddw02 (EU-SILC), retrieved 5 Oct 2026"
S11 = "Eurostat ilc_li02 (EU-SILC), retrieved 5 Oct 2026"


def add(check, value, unit, source, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": source, "note": note})


def ranked(yy, geos=EU27):
    return sorted(((pol[(g, yy)], g) for g in geos if (g, yy) in pol), reverse=True)


y = 2023
rank = ranked(y)
n = len(rank)
add("Malta: share reporting pollution, grime or other environmental problems, 2023", pol[("MT", y)], "%", S2,
    f"flag '{flag[('MT', y)]}'" if flag[("MT", y)] else "no Eurostat flag")
add("EU-27: same, 2023", pol[("EU27_2020", y)], "%", S2,
    f"flag '{flag[('EU27_2020', y)]}'" if flag[("EU27_2020", y)] else "no Eurostat flag")
add("Countries with data for 2023 (EU-27)", n, "count", S2)
add("Malta rank among EU-27, 2023 (1 = highest)", [g for _, g in rank].index("MT") + 1, "rank", S2)
for i, label in ((1, "Second"), (2, "Third"), (3, "Fourth")):
    v, g = rank[i]
    add(f"{label}-highest EU-27 country, 2023", v, "%", S2,
        g + (f"; flag '{flag[(g, y)]}' (u = low reliability)" if flag[(g, y)] else ""))
add("Malta minus second-highest, 2023", round(pol[("MT", y)] - rank[1][0], 1), "pp", "calculated")
add("Malta / EU-27 ratio, 2023", round(pol[("MT", y)] / pol[("EU27_2020", y)], 2), "x", "calculated",
    "'nearly three times' tested")
add("Ratio on Amphora's rounded figures (35 / 12)", round(35 / 12, 2), "x", "calculated")
every = sorted(((v, g) for (g, yy), v in pol.items() if yy == y and not g.startswith(AGG)), reverse=True)
nonEU = [(v, g) for v, g in every if g not in EU27]
add("Malta rank among every country in the dataset, 2023", [g for _, g in every].index("MT") + 1,
    f"of {len(every)}", S2, f"highest non-EU: {nonEU[0][1]} {nonEU[0][0]}%")

# every survey year: rank, number of EU-27 countries with data, which are missing
first = 0
for yy in range(2005, 2024):
    if ("MT", yy) not in pol:
        continue
    r = ranked(yy)
    pos = [g for _, g in r].index("MT") + 1
    first += pos == 1
    missing = [g for g in EU27 if (g, yy) not in pol]
    eu = pol.get(("EU27_2020", yy))
    eu_txt = f"{eu}%" + (f" (flag '{flag[('EU27_2020', yy)]}')" if flag.get(("EU27_2020", yy)) else "") if eu else "n/a"
    add(f"Malta rank among EU-27 with data, {yy}", pos, f"of {len(r)}", S2,
        f"Malta {pol[('MT', yy)]}%; EU-27 {eu_txt}; second {r[1][1]} {r[1][0]}%"
        + (f"; no data for {', '.join(missing)}" if missing else ""))
add("Malta: survey years 2005-2023 ranked first among EU-27 countries with data", first, "years", S2,
    "of " + str(sum(1 for yy in range(2005, 2024) if ("MT", yy) in pol)) + " years with data; 2021 and 2022 not collected")
add("Malta: years without data, 2005-2023", ", ".join(str(yy) for yy in range(2005, 2024) if ("MT", yy) not in pol),
    "years", S2, "item moved to the three-yearly module 'Labour market and housing' (collected 2023, 2026)")
add("Eurostat flags on the Malta series, 2005-2023",
    ", ".join(f"{yy}:{flag[('MT', yy)]}" for yy in range(2005, 2024) if flag.get(("MT", yy))) or "none", "flags", S2)
add("Eurostat flags on the EU-27 series",
    ", ".join(f"{yy}:{flag[('EU27_2020', yy)]}" for yy in range(2005, 2024) if flag.get(("EU27_2020", yy))) or "none",
    "flags", S2, "e = estimated")
add("EU-27 change, 2019 to 2023", f"{pol[('EU27_2020', 2019)]} -> {pol[('EU27_2020', 2023)]}", "%", S2,
    "Eurostat news release 1 Sep 2025: 15.1% to 12.2%")

# Malta's trend
mt = {yy: pol[("MT", yy)] for yy in range(2005, 2024) if ("MT", yy) in pol}
peak = max(mt, key=mt.get)
low = min(mt, key=mt.get)
add("Malta: series peak", mt[peak], "%", S2, str(peak))
add("Malta: series low", mt[low], "%", S2, str(low))
add("Malta 2023 vs 2017 (series low)", round(mt[2023] - mt[2017], 1), "pp", S2, f"{mt[2017]}% in 2017")
higher = [yy for yy in mt if yy < 2023 and mt[yy] > mt[2023]]
add("Malta: latest earlier year with a higher share than 2023", max(higher), "year", S2,
    f"{mt[max(higher)]}%; every year {max(higher) + 1}-2020 was lower than 2023's {mt[2023]}%")
add("Malta: 2010-2014 range", f"{min(mt[yy] for yy in range(2010, 2015))}-{max(mt[yy] for yy in range(2010, 2015))}",
    "%", S2)

# income split: above vs below 60% of median equivalised income (the at-risk-of-poverty threshold)
add("Malta: people above 60% of median income, 2023", pol_hi[("MT", y)], "%", S2,
    "Amphora: 'high-earning households were more affected'")
add("Malta: people below 60% of median income (at risk of poverty), 2023", pol_lo[("MT", y)], "%", S2)
add("Malta: above minus below, 2023", round(pol_hi[("MT", y)] - pol_lo[("MT", y)], 1), "pp", "calculated",
    "Eurostat Statistics Explained: Malta 5.5 pp lower for people at risk of poverty")
add("Malta: at-risk-of-poverty rate, 2023", arop[("MT", y)], "%", S11, "share of people below 60% of median income")
add("Malta: share of people in the 'above 60%' group, 2023", round(100 - arop[("MT", y)], 1), "%", "calculated")
add("EU-27: at-risk-of-poverty rate, 2023", arop[("EU27_2020", y)], "%", S11)
rev = [yy for yy in range(2005, 2024) if ("MT", yy) in pol_hi and pol_lo[("MT", yy)] > pol_hi[("MT", yy)]]
add("Malta: years in which people below 60% reported more than people above",
    f"{len(rev)} of {sum(1 for yy in range(2005, 2024) if ('MT', yy) in pol_hi)}", "years", S2,
    ", ".join(map(str, rev)))
add("EU-27: above / below 60% of median income, 2023", f"{pol_hi[('EU27_2020', y)]} / {pol_lo[('EU27_2020', y)]}", "%",
    S2, "the opposite direction to Malta")
with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for r in rows:
    print(f"{r['check']:85s} {r['value']!s:>12} {r['unit']}  {r['note']}")
