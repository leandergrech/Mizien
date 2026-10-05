#!/usr/bin/env python3
"""CC-018: test 'the IMF's assessment confirms what the MDA has been saying' with formulas, not by eye.

Reads data/cc-018/ and data/cc-013/eurostat_housing.csv; writes data/cc-018/checks.csv. Housing-cost overburden
comes from data/cc-018/eurostat_ilc_lvho07a.csv (retrieved 5 Oct 2026 with Eurostat's status flags): Malta's 2023
value is flagged b (break in time series), so the series is split at the break.
"""
import csv, pathlib
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-018"
P = defaultdict(dict)
for r in csv.DictReader(open(D / "eurostat_tipsho60.csv")):
    P[(r["unit"], r["geo"])][int(r["year"])] = float(r["value"])
E = defaultdict(dict)
for r in csv.DictReader(open(ROOT / "data" / "cc-013" / "eurostat_housing.csv")):
    if r["dataset"] != "#":
        E[(r["dataset"], r["geo"])][int(r["year"])] = float(r["value"])
I = {r["item"]: r["value"] for r in csv.DictReader(open(D / "imf_extracts.csv"))}
rows = []


def add(check, value, unit, source, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": source, "note": note})


for geo, lab in (("MT", "Malta"), ("EU27_2020", "EU-27")):
    i15, lt = P[("PTIR_I15", geo)], P[("PTIR_LT_AVG", geo)]
    last = max(i15)
    add(f"{lab}: price-to-income ratio, 2015 -> {last}", round(i15[last] - 100, 1), "% change", "Eurostat tipsho60")
    add(f"{lab}: price-to-income ratio vs long-term average, {last}", lt[last], "index (100 = average)",
        "Eurostat tipsho60")
    yrs = [y for y in range(2020, last + 1) if y in i15]
    add(f"{lab}: years 2020-{last} with a rising ratio", sum(i15[y] > i15[y - 1] for y in yrs), f"of {len(yrs)}",
        "Eurostat tipsho60")
mt = P[("PTIR_I15", "MT")]
add("Malta: peak of price-to-income ratio since 2010", max((v, y) for y, v in mt.items() if y >= 2010)[1], "year",
    "Eurostat tipsho60")
add("Banks: real estate and construction share of private loans",
    f"{I['Real estate and construction share of private loans a decade earlier']} -> "
    f"{I['Real estate and construction share of private loans mid-2025']}", "%", "IMF CR 26/29 p.19")
add("Banks: residential mortgages share of private lending",
    f"{I['Residential mortgages share a decade earlier']} -> {I['Residential mortgages share of private lending']}", "%",
    "IMF CR 26/29 p.19")
OB = defaultdict(dict)
for x in csv.DictReader(open(D / "eurostat_ilc_lvho07a.csv")):
    OB[x["geo"]][int(x["year"])] = (float(x["value"]), x["flag"])
brk = min(y for y, (_, f) in OB["MT"].items() if "b" in f)
for geo, lab in (("MT", "Malta"), ("EU27_2020", "EU-27")):
    o = {y: v for y, (v, _) in OB[geo].items()}
    add(f"{lab}: housing-cost overburden 2015 -> {brk - 1} (before Malta's series break)",
        f"{o[2015]} -> {o[brk - 1]}", "% of people", "Eurostat ilc_lvho07a",
        "affordability, not covered by the IMF assessment")
    add(f"{lab}: housing-cost overburden {brk} -> {max(o)} (after the break)",
        " / ".join(f"{o[y]}" for y in range(brk, max(o) + 1)), "% of people", "Eurostat ilc_lvho07a",
        f"Malta {brk} flagged b (break in time series)" if geo == "MT" else "")
r = E[("tipsho10", "MT")]
add("Malta: real house prices 2015 -> 2025", round(100 * (r[2025] / r[2015] - 1)), "%", "Eurostat tipsho10")
add("MDA-commissioned study: price-to-income 2024 -> 2025", "14.0 -> 14.5", "ratio",
    "MaltaToday, 8 Feb 2026 (second-hand)", "different measure from Eurostat's; method not seen")

# ---- v1.2: the release's further statements (data/cc-018/eurostat_more.csv, imf_consultation_cycles.csv)
M = defaultdict(dict)
FL = {}
for x in csv.DictReader(open(D / "eurostat_more.csv")):
    M[(x["dataset"], x["unit"], x["geo"])][x["time"]] = float(x["value"])
    FL[(x["dataset"], x["unit"], x["geo"], x["time"])] = x["flag"]
cyc = list(csv.DictReader(open(D / "imf_consultation_cycles.csv")))
now = [r for r in cyc if "(" not in r["member"]]
on24 = [r["member"] for r in now if r["cycle_months"] == "24"]
add("EU members on the IMF's 24-month Article IV cycle in their latest staff report (2025-26)",
    f"{len(on24)} of {len(now)} ({', '.join(on24)})", "members", "IMF eLibrary, latest staff reports",
    "all others: 12-month cycle")
lux = [r["member"] for r in cyc if r["member"].startswith("Luxembourg (") and r["cycle_months"] == "24"]
add("Earlier EU member placed on the 24-month cycle", "; ".join(lux), "", "IMF CR 00/65 para. 45; CR 02/118 para. 34",
    "Luxembourg, an EU member then as now: 2000 and 2002 consultations two years apart")
usd13, usd24 = float(I["Per capita income 2013"]), float(I["Per capita income 2024"])
add("IMF: per capita income 2013 -> 2024 (US$ thousand)", f"{usd13:g} -> {usd24:g} (x{usd24 / usd13:.2f})", "ratio",
    "IMF CR 26/29 p.8", "the IMF's own 'nearly doubled'")
g = M[("nama_10_pc", "CP_EUR_HAB", "MT")]
r_ = M[("nama_10_pc", "CLV20_EUR_HAB", "MT")]
last = max(g)
add(f"Malta: GDP per head, current prices, 2013 -> {last}", f"{g['2013']:,.0f} -> {g[last]:,.0f} "
    f"(x{g[last] / g['2013']:.2f})", "EUR", "Eurostat nama_10_pc CP_EUR_HAB",
    f"2013 -> 2024: x{g['2024'] / g['2013']:.2f}")
add(f"Malta: GDP per head, chain-linked volumes (2020 prices), 2013 -> {last}",
    f"{r_['2013']:,.0f} -> {r_[last]:,.0f} (x{r_[last] / r_['2013']:.2f})", "EUR (2020 prices)",
    "Eurostat nama_10_pc CLV20_EUR_HAB", "real terms: about half again, not nearly double")
eu = M[("nama_10_pc", "CP_EUR_HAB", "EU27_2020")]
pps = M[("nama_10_pc", "PC_EU27_2020_HAB_MPPS_CP", "MT")]
eur = M[("nama_10_pc", "PC_EU27_2020_HAB_MEUR_CP", "MT")]
add(f"Malta vs EU-27: GDP per head at market prices, {last}", f"{g[last]:,.0f} vs {eu[last]:,.0f} "
    f"({eur[last]:g}% of EU)", "EUR", "Eurostat nama_10_pc", f"{eur[last] - 100:+.1f}% above the EU average")
add(f"Malta vs EU-27: GDP per head in purchasing power standards, {last}", pps[last], "index (EU-27 = 100)",
    "Eurostat nama_10_pc PC_EU27_2020_HAB_MPPS_CP", f"2013: {pps['2013']:g}")
hq = M[("prc_hpi_q", "RCH_A", "MT")]
qs = sorted(hq)
add("Malta: house prices, annual change by quarter, 2024", " / ".join(f"{hq[q]:g}" for q in qs if q[:4] == "2024"),
    "% y/y", "Eurostat prc_hpi_q RCH_A", "before the IMF's 'moderated in early 2025'")
add("Malta: house prices, annual change, 2025-Q1 / Q2", f"{hq['2025-Q1']:g} / {hq['2025-Q2']:g}", "% y/y",
    "Eurostat prc_hpi_q RCH_A", "the IMF's 'moderated in early 2025'")
latest = [q for q in qs if q >= "2026"]
add(f"Malta: house prices, annual change, {' / '.join(latest)}", " / ".join(f"{hq[q]:g}" for q in latest), "% y/y",
    "Eurostat prc_hpi_q RCH_A", "flag " + ", ".join(FL[("prc_hpi_q", "RCH_A", "MT", q)] or "-" for q in latest)
    + " (p = provisional)")
ha = M[("prc_hpi_a", "RCH_A_AVG", "MT")]
add("Malta: house prices, annual average change, 2025", ha["2025"], "%", "Eurostat prc_hpi_a RCH_A_AVG",
    "flag " + (FL[("prc_hpi_a", "RCH_A_AVG", "MT", "2025")] or "-"))
# Household gross disposable income per head (B6G, S14_S15, current prices / population), 2015 = 100
inc = M[("nasa_10_nf_tr", "CP_MEUR", "MT")]
pop = M[("nama_10_pe", "THS_PER", "MT")]
iph = {y: inc[y] / pop[y] * 1000 for y in inc if y in pop}
yi = max(iph)
hpa = M[("prc_hpi_a", "I15_A_AVG", "MT")]
add(f"Malta: household gross disposable income per head, 2015 -> {yi}", f"{iph['2015']:,.0f} -> {iph[yi]:,.0f} "
    f"(index {100 * iph[yi] / iph['2015']:.1f})", "EUR", "Eurostat nasa_10_nf_tr B6G S14_S15 / nama_10_pe POP_NC",
    f"{yi} flagged {FL[('nasa_10_nf_tr', 'CP_MEUR', 'MT', yi)] or '-'}; no data after {yi}")
add(f"Malta: house price index {yi} (2015 = 100)", hpa[yi], "index", "Eurostat prc_hpi_a I15_A_AVG")
add(f"Malta: house prices relative to income per head, 2015 -> {yi}",
    round(100 * (hpa[yi] / (100 * iph[yi] / iph["2015"]) - 1), 1), "% change", "calculated",
    f"cross-check of tipsho60 ({P[('PTIR_I15', 'MT')][int(yi)] - 100:+.1f}%)")
hq15 = M[("prc_hpi_q", "I15_Q", "MT")]
add(f"Malta: house price index, {qs[-1]} (2015 = 100)", hq15[qs[-1]], "index", "Eurostat prc_hpi_q I15_Q",
    "flag " + (FL[("prc_hpi_q", "I15_Q", "MT", qs[-1])] or "-"))
add(f"Malta: GDP per head index {last} (2015 = 100)", round(100 * g[last] / g["2015"], 1), "index",
    "Eurostat nama_10_pc CP_EUR_HAB", "proxy for income after the last household-income year")

with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\r\n")
    w.writeheader()
    w.writerows(rows)
for x in rows:
    print(f"{x['check']:66s} {str(x['value']):>14} {x['unit']:22s} {x['note']}")
