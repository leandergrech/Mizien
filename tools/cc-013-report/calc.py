#!/usr/bin/env python3
"""CC-013: test 'issuing permits keeps property prices in check' with formulas, not by eye.

Reads data/cc-013/ (Eurostat, PA approved dwellings, NSO Census 2021; retrieved 3 Oct 2026) and writes
data/cc-013/checks.csv.
"""
import csv, pathlib, re
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-013"
E = defaultdict(dict)
FL = {}  # Eurostat status flags recorded in the note column ("flag b", "flag p", ...)
for r in csv.DictReader(open(D / "eurostat_housing.csv")):
    if r["dataset"] in ("#", "sts_cobp_a"):  # sts_cobp_a holds two series per year (dwellings, floor area); unused
        continue
    E[(r["dataset"], r["geo"])][int(r["year"])] = float(r["value"])
    m = re.search(r"flag (\w+)", r["note"])
    if m:
        FL[(r["dataset"], r["geo"], int(r["year"]))] = m.group(1)


def flags(ds, geo, *years):
    """Note listing Eurostat flags on the given years, e.g. '2025: p (provisional)'."""
    names = {"b": "break in series", "p": "provisional", "e": "estimated"}
    f = [f"{y}: {FL[(ds, geo, y)]} ({names.get(FL[(ds, geo, y)], 'see Eurostat')})" for y in years
         if (ds, geo, y) in FL]
    return "Eurostat flag " + "; ".join(f) if f else ""


PA = {int(r["year"]): int(r["approved_units_total"]) for r in csv.DictReader(open(D / "pa_approved_dwellings.csv"))}
rows = []


def add(check, value, unit, source, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": source, "note": note})


add("Approved dwelling units, 2015-2024", sum(PA[y] for y in range(2015, 2025)), "units", "PA approved dwellings",
    "interviewer's figure: about 91,000 in the past decade")
add("Approved dwelling units, 2014-2023", sum(PA[y] for y in range(2014, 2024)), "units", "PA approved dwellings")
add("Approved units, 2009-2014 average", round(sum(PA[y] for y in range(2009, 2015)) / 6), "units/yr", "PA")
add("Approved units, 2016-2024 average", round(sum(PA[y] for y in range(2016, 2025)) / 9), "units/yr", "PA")
for geo, lab in (("MT", "Malta"), ("EU27_2020", "EU-27")):
    n, r = E[("prc_hpi_a", geo)], E[("tipsho10", geo)]
    add(f"{lab}: nominal house prices 2015-2024", round(100 * (n[2024] / n[2015] - 1)), "%", "Eurostat prc_hpi_a")
    add(f"{lab}: real house prices 2015-2024", round(100 * (r[2024] / r[2015] - 1)), "%", "Eurostat tipsho10")
    add(f"{lab}: real house prices 2015-2025", round(100 * (r[2025] / r[2015] - 1)), "%", "Eurostat tipsho10",
        "; ".join(x for x in ("used in the report", flags("tipsho10", geo, 2015, 2025)) if x))
    yrs = [y for y in range(2016, 2026) if y in r and y - 1 in r]
    add(f"{lab}: years 2016-2025 with real price growth", sum(r[y] > r[y - 1] for y in yrs), f"of {len(yrs)}",
        "Eurostat tipsho10")
    p = E[("demo_gind", geo)]
    add(f"{lab}: population growth 2015-2025", round(100 * (p[2025] / p[2015] - 1), 1), "%", "Eurostat demo_gind")
    o, c = E[("ilc_lvho07a", geo)], E[("ilc_lvho05a", geo)]
    # Like-for-like runs only: Eurostat flags a break in Malta's series in 2023, so 2015 and 2025 are not compared.
    add(f"{lab}: housing cost overburden 2015 -> 2022", f"{o[2015]} -> {o[2022]}", "% of pop.", "Eurostat ilc_lvho07a",
        flags("ilc_lvho07a", geo, *range(2015, 2023)))
    add(f"{lab}: housing cost overburden 2023 -> 2024 -> 2025", f"{o[2023]} -> {o[2024]} -> {o[2025]}", "% of pop.",
        "Eurostat ilc_lvho07a", flags("ilc_lvho07a", geo, 2023, 2024, 2025))
    add(f"{lab}: overcrowding 2015 -> 2025", f"{c[2015]} -> {c[2025]}", "% of pop.", "Eurostat ilc_lvho05a")
# Did prices grow more slowly in the record-permit years? (descriptive only, not causal)
r = E[("tipsho10", "MT")]
hi = [y for y in range(2016, 2025) if PA[y] >= 9000]
lo = [y for y in range(2016, 2025) if PA[y] < 9000]
g = lambda ys: round(sum(100 * (r[y] / r[y - 1] - 1) for y in ys) / len(ys), 1)
add("Malta: mean real price growth in years with >=9,000 approvals", g(hi), "%/yr", "calculated", ", ".join(map(str, hi)))
add("Malta: mean real price growth in years with <9,000 approvals", g(lo), "%/yr", "calculated", ", ".join(map(str, lo)))
pop = E[("demo_gind", "MT")]
add("Malta: approved units per additional resident, 2015-2024",
    round(sum(PA[y] for y in range(2015, 2025)) / (pop[2025] - pop[2015]), 2), "units/person", "calculated",
    f"population +{int(pop[2025] - pop[2015]):,}")
C = {r["item"]: float(r["value"]) for r in csv.DictReader(open(D / "census2021_dwellings.csv"))}
add("Census 2021: dwellings not used as main residence", int(C["Secondary, seasonally used or vacant 2021"]), "dwellings",
    "NSO Census 2021 vol. 2", f"{C['Secondary, seasonally used or vacant share 2021 (%)']}% of stock (2011: 31.8%)")

with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
for x in rows:
    print(f"{x['check']:66s} {str(x['value']):>14} {x['unit']:10s} {x['note']}")
