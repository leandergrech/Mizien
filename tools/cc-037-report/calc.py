#!/usr/bin/env python3
"""CC-037: test the Amphora claim (35% reported pollution in 2023, highest in the EU, ~3x the EU average of 12%).
Reads data/cc-037/eurostat_ilc_mddw02.csv and eurostat_ilc_mddw04.csv (retrieved 5 Oct 2026); writes checks.csv."""
import csv, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-037"
EU27 = "BE BG CZ DK DE EE IE EL ES FR HR IT CY LV LT LU HU MT NL AT PL PT RO SI SK FI SE".split()


def load(f, **flt):
    out = {}
    for r in csv.DictReader(open(D / f)):
        if all(r[k] == v for k, v in flt.items()):
            out[(r["geo"], int(r["time"]))] = float(r["value"])
    return out


pol = load("eurostat_ilc_mddw02.csv", hhcomp="TOTAL", rskpovth="TOTAL")
pol_hi = load("eurostat_ilc_mddw02.csv", hhcomp="TOTAL", rskpovth="A_60")
pol_lo = load("eurostat_ilc_mddw02.csv", hhcomp="TOTAL", rskpovth="B_60")
rows = []
S2 = "Eurostat ilc_mddw02 (EU-SILC), retrieved 5 Oct 2026"


def add(check, value, unit, source, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": source, "note": note})


y = 2023
rank = sorted(((pol[(g, y)], g) for g in EU27 if (g, y) in pol), reverse=True)
n = len(rank)
add("Malta: share reporting pollution, grime or other environmental problems, 2023", pol[("MT", y)], "%", S2)
add("EU-27: same, 2023", pol[("EU27_2020", y)], "%", S2)
add("Countries with data for 2023 (EU-27)", n, "count", S2)
add("Malta rank among EU-27, 2023 (1 = highest)", [g for _, g in rank].index("MT") + 1, "rank", S2)
add("Second-highest EU-27 country, 2023", rank[1][0], "%", S2, f"{rank[1][1]}")
add("Malta minus second-highest, 2023", round(pol[("MT", y)] - rank[1][0], 1), "pp", "calculated")
add("Malta / EU-27 ratio, 2023", round(pol[("MT", y)] / pol[("EU27_2020", y)], 2), "x", "calculated",
    "'nearly three times' tested; 35/12 = 2.92 with the rounded figures")
for yy in range(2005, 2024):
    if ("MT", yy) in pol and yy not in (2021, 2022):
        r = sorted(((pol[(g, yy)], g) for g in EU27 if (g, yy) in pol), reverse=True)
        add(f"Malta rank among EU-27 with data, {yy}", [g for _, g in r].index("MT") + 1, f"of {len(r)}", S2,
            f"Malta {pol[('MT', yy)]}%, EU-27 {pol.get(('EU27_2020', yy), 'n/a')}%")
add("Malta: years 2005-2023 ranked first among EU-27 countries with data",
    sum(1 for yy in range(2005, 2024) if ("MT", yy) in pol and
        max(((pol[(g, yy)], g) for g in EU27 if (g, yy) in pol))[1] == "MT"),
    "years", S2, "years with Malta data; 2021 and 2022 not published")
add("Malta 2023 vs 2017 (series low)", round(pol[("MT", 2023)] - pol[("MT", 2017)], 1), "pp", S2,
    f"{pol[('MT', 2017)]}% in 2017")
add("Malta: households above 60% of median income, 2023", pol_hi[("MT", y)], "%", S2, "Amphora: higher earners more affected")
add("Malta: households below 60% of median income, 2023", pol_lo[("MT", y)], "%", S2)
add("EU-27: above / below 60% of median income, 2023", f"{pol_hi[('EU27_2020', y)]} / {pol_lo[('EU27_2020', y)]}", "%", S2)
with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for r in rows:
    print(f"{r['check']:85s} {r['value']!s:>10} {r['unit']}  {r['note']}")
