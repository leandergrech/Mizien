#!/usr/bin/env python3
"""CC-095: test the Finance Minister's statements of 30 Sep 2026 (Pre-Budget Document 2027 launch): energy subsidies of
about EUR 400 million in 2026 (EUR 391.7 million in his figures) and about the same in 2027; fuel, electricity and gas
prices 'have not changed'; Malta 'the only country' still shielding families and businesses.

Reads data/cc-095/ (fetch.py, 10 Oct 2026; statements_and_estimates.csv typed from the sources it names) and, without
copying them, three CC-113 files: other_estimates_transcribed.csv (Draft Budgetary Plans 2024 and 2025; IMF CR 26/29),
ec_inventory_malta_facts.csv (the Commission's 2023 entries for Malta) and nothing else.
Writes data/cc-095/checks.csv (every number in the report) and data/cc-095/cost_series.csv (Figure 3).
"""
import csv
import datetime as dt
import pathlib
import statistics

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-095"
D113 = ROOT / "data" / "cc-113"
EU27 = "AT BE BG CY CZ DE DK EE EL ES FI FR HR HU IE IT LT LU LV MT NL PL PT RO SE SI SK".split()
rows = []


def add(check, value, unit, source, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": source, "note": note})


def rd(path):
    return list(csv.DictReader(open(path, encoding="utf-8")))


S_HICP = "Eurostat prc_hicp_minr (ECOICOP ver.2), updated 2 Oct 2026, retrieved 10 Oct 2026"
S_WOB = "European Commission Weekly Oil Bulletin, history workbook, retrieved 10 Oct 2026"
S_204 = "Eurostat nrg_pc_204 band DC, all taxes, updated 9 Oct 2026, retrieved 10 Oct 2026"
S_205 = "Eurostat nrg_pc_205 band ID, excl. VAT, retrieved 10 Oct 2026"
S_COF = "Eurostat gov_10a_exp COFOG 04.3, updated 16 Sep 2026, retrieved 10 Oct 2026"
S_GDP = "Eurostat nama_10_gdp CP_MEUR, retrieved 10 Oct 2026"

# ================================================================ A. prices unchanged
hm = rd(D / "eurostat_hicp_energy_mt_eu_history.csv")
idx = {}
for r in hm:
    if r["unit"] == "I25" and r["value"]:
        idx.setdefault((r["geo"], r["coicop18"]), []).append((r["time"], float(r["value"]), r["flag"]))
for k in idx:
    idx[k].sort()
NAMES = {"CP0451": "electricity", "CP0452": "gas (LPG in Malta)", "CP07221": "diesel", "CP07222": "petrol",
         "NRG": "all energy"}
for code, name in NAMES.items():
    s = idx[("MT", code)]
    last = [b for a, b in zip(s, s[1:]) if abs(b[1] - a[1]) > 0.005]
    since = last[-1][0] if last else s[0][0]
    add(f"Malta HICP {name}: month from which the index has not changed", since, "month", S_HICP,
        f"index {s[-1][1]:.2f} (2025=100) in {s[-1][0]}{' (flag ' + s[-1][2] + ')' if s[-1][2] else ''}")
    add(f"Malta HICP {name}: latest month", s[-1][0], "month", S_HICP, f"value {s[-1][1]:.2f}")


def change(geo, code, t0, t1):
    s = dict((t, v) for t, v, _ in idx[(geo, code)])
    return round(100 * (s[t1] / s[t0] - 1), 1)


for code, name in (("NRG", "energy"), ("CP07221", "diesel"), ("CP07222", "petrol"), ("CP0451", "electricity"),
                   ("CP0452", "gas")):
    add(f"EU-27 HICP {name}: change Dec 2025 to Aug 2026", change("EU27_2020", code, "2025-12", "2026-08"), "%",
        S_HICP)
    add(f"Malta HICP {name}: change Dec 2025 to Aug 2026", change("MT", code, "2025-12", "2026-08"), "%", S_HICP)
add("EU-27 HICP energy: change Jan 2020 to Aug 2026", change("EU27_2020", "NRG", "2020-01", "2026-08"), "%", S_HICP)
add("Malta HICP energy: change Jan 2020 to Aug 2026", change("MT", "NRG", "2020-01", "2026-08"), "%", S_HICP,
    "Malta's energy index fell in Jun-Jul 2020 (fuel price cut) and has not moved since")

# annual rates, August 2026, every EU country
he = rd(D / "eurostat_hicp_energy_eu_2025_2026.csv")
ann = {}
for r in he:
    if r["unit"] == "RCH_A" and r["time"] == "2026-08" and r["value"]:
        ann.setdefault(r["coicop18"], {})[r["geo"]] = float(r["value"])
for code, name in (("NRG", "energy"), ("FUEL", "liquid and transport fuels"), ("CP07221", "diesel"),
                   ("CP0451", "electricity")):
    d = {g: v for g, v in ann[code].items() if g in EU27}
    order = sorted(d, key=lambda g: d[g])
    add(f"HICP {name}, annual change Aug 2026: Malta", d["MT"], "%", S_HICP)
    add(f"HICP {name}, annual change Aug 2026: EU-27", ann[code]["EU27_2020"], "%", S_HICP)
    add(f"HICP {name}, annual change Aug 2026: countries at 0.0% or below", sum(1 for v in d.values() if v <= 0),
        "of 27", S_HICP, ", ".join(f"{g} {d[g]}" for g in order if d[g] <= 0))
    add(f"HICP {name}, annual change Aug 2026: lowest three", "; ".join(f"{g} {d[g]}" for g in order[:3]), "%",
        S_HICP, "")
    if code == "NRG":
        add("HICP energy, annual change Aug 2026: countries below 2%", sum(1 for v in d.values() if v < 2), "of 27",
            S_HICP, ", ".join(f"{g} {d[g]}" for g in order if d[g] < 2))
        ANN_NRG = d

# Weekly Oil Bulletin
wob = rd(D / "oil_bulletin_mt_it_eu_weekly.csv")
ser = {}
for r in wob:
    ser.setdefault((r["geo"], r["product"], r["basis"]), []).append((r["date"], float(r["eur_per_1000"])))
for k in ser:
    ser[k].sort()
for prod, name in (("diesel", "diesel"), ("euro95", "petrol (Euro-super 95)")):
    s = ser[("MT", prod, "with taxes")]
    cur = s[-1][1]
    first = [d for d, v in s if v == cur and all(v2 == cur for d2, v2 in s if d2 >= d)][0]
    prev = [v for d, v in s if d < first][-1]
    n = sum(1 for d, v in s if d >= first)
    add(f"Malta {name} pump price (with taxes), unchanged since", first, "week", S_WOB,
        f"EUR {cur / 1000:.2f} per litre in {n} weekly reports to {s[-1][0]}; before: EUR {prev / 1000:.2f}")
    add(f"Malta {name} pump price, latest week", round(cur / 1000, 3), "EUR per litre", S_WOB, s[-1][0])
    for g in ("EU", "IT"):
        s2 = ser[(g, prod, "with taxes")]
        add(f"{'EU weighted average' if g == 'EU' else 'Italy'} {name} pump price, {s2[-1][0]}",
            round(s2[-1][1] / 1000, 3), "EUR per litre", S_WOB)
        sm = dict(s2)
        add(f"{'EU weighted average' if g == 'EU' else 'Italy'} {name} pump price, 2026-09-28", round(sm['2026-09-28'] / 1000, 3),
            "EUR per litre", S_WOB, "the week before the minister's comparison (30 Sep 2026)")
    for g in ("MT", "EU", "IT"):
        s3 = ser[(g, prod, "without taxes")]
        add(f"{g} {name} price before taxes, {s3[-1][0]}", round(s3[-1][1] / 1000, 3), "EUR per litre", S_WOB)
mt_pre = ser[("MT", "diesel", "without taxes")][-1][1]
add("Malta diesel price before taxes as share of the EU average before taxes (latest week)",
    round(100 * mt_pre / ser[("EU", "diesel", "without taxes")][-1][1], 1), "%", S_WOB,
    "the regulated Maltese price leaves less than half the EU's average pre-tax margin and product cost")
add("EU average diesel price before taxes as a multiple of Malta's (latest week)",
    round(ser[("EU", "diesel", "without taxes")][-1][1] / mt_pre, 1), "times", S_WOB)

lat = rd(D / "oil_bulletin_latest_all.csv")
for prod, name in (("diesel", "diesel"), ("euro95", "petrol")):
    d = {r["geo"]: float(r["eur_per_1000"]) / 1000 for r in lat if r["product"] == prod and r["geo"] != "EU"}
    order = sorted(d, key=lambda g: d[g])
    add(f"Oil Bulletin {lat[0]['date']}: Malta's rank for {name} (1 = cheapest)", order.index("MT") + 1,
        f"of {len(d)} reporting", S_WOB, f"next cheapest {order[1]} EUR {d[order[1]]:.3f}")
    add(f"Oil Bulletin {lat[0]['date']}: median {name} price of reporting countries", round(statistics.median(d.values()), 3),
        "EUR per litre", S_WOB, "the minister: 'the EU median is EUR 2 per litre' (Newsbook, outlet paraphrase)"
        if prod == "diesel" else "")

# electricity prices (half-yearly)
for fname, src, lab in (("eurostat_nrg_pc_204_dc.csv", S_204, "households, band DC (all taxes)"),
                        ("eurostat_nrg_pc_205_id.csv", S_205, "non-households, band ID (excl. VAT)")):
    e = rd(D / fname)
    mt = sorted((r["time"], float(r["value"]), r["flag"]) for r in e if r["geo"] == "MT" and r["value"])
    eu = sorted((r["time"], float(r["value"])) for r in e if r["geo"] == "EU27_2020" and r["value"])
    mt19 = [x for x in mt if x[0] >= "2019-S1"]
    add(f"Malta electricity price, {lab}: range 2019-S1 to {mt19[-1][0]}",
        f"{min(v for _, v, _ in mt19):.4f}-{max(v for _, v, _ in mt19):.4f}", "EUR per kWh", src,
        f"latest {mt19[-1][1]:.4f}{' (flag ' + mt19[-1][2] + ')' if mt19[-1][2] else ''}")
    add(f"EU-27 electricity price, {lab}: {eu[-1][0]}", eu[-1][1], "EUR per kWh", src,
        f"2019-S1 {eu[0][1]:.4f}; peak {max(eu, key=lambda x: x[1])[0]} {max(v for _, v in eu):.4f}")
    if "households" in lab and "non" not in lab:
        add("Malta household price as share of the EU-27 average, band DC, 2025-S2",
            round(100 * dict((t, v) for t, v, _ in mt)["2025-S2"] / dict(eu)["2025-S2"], 1), "%", src)

# ================================================================ B, C. what the support costs
gdp = {int(r["time"]): float(r["value"]) for r in rd(D / "eurostat_nama_10_gdp_mt.csv")}
st = {r["id"]: r for r in rd(D / "statements_and_estimates.csv")}
m23, m25, m26, m27 = (float(st[k]["value"]) for k in ("S01", "S02", "S03", "S04"))
five = float(st["S07"]["value"])
cof = {}
for r in rd(D / "eurostat_cofog_fuel_energy.csv"):
    if r["value"]:
        cof[(r["geo"], r["na_item"], r["unit"], int(r["time"]))] = float(r["value"])
oth = rd(D113 / "other_estimates_transcribed.csv")
gov = {int(r["year"]): float(r["value"]) for r in oth if r["measure"].startswith("Energy support measures")}
imf = {int(r["year"]): float(r["value"]) for r in oth if r["measure"] == "Energy subsidies (IMF Article IV)"}
inv = {r["item"]: r for r in rd(D113 / "ec_inventory_malta_facts.csv")}
inv23 = sum(float(r["y2023"]) for r in inv.values())
inv23_tbc = inv23 + float(inv["Cut in excise duty on petrol and diesel"]["y2022"])

add("Minister's figures (as reported): energy and food subsidies 2023", m23, "EUR million", "Lovin Malta, 30 Sep 2026")
add("Minister's figures (as reported): 2025", m25, "EUR million", "Lovin Malta, 30 Sep 2026")
add("Minister's figures (as reported): 2026 (projection)", m26, "EUR million", "Lovin Malta, 30 Sep 2026",
    "Italpress/MNA: EUR 392 million; BusinessNow: EUR 400 million 'for this year'")
add("Minister's figures (as reported): 2027 (forecast)", m27, "EUR million (rounded)", "Lovin Malta, 30 Sep 2026")
add("2026 projection against 2025", round(m26 / m25, 2), "times", "calculated", f"+EUR {m26 - m25:.1f} million")
for y, v in ((2023, m23), (2025, m25)):
    add(f"Minister's {y} figure as % of GDP", round(100 * v / gdp[y], 2), "% of GDP", S_GDP, f"GDP {gdp[y]:.1f}")
add("Eurostat COFOG 04.3 fuel and energy subsidies (D.3), Malta 2019", cof[("MT", "D3", "MIO_EUR", 2019)],
    "EUR million", S_COF, "pre-crisis level")
for y in (2021, 2022, 2023, 2024):
    add(f"Eurostat COFOG 04.3 fuel and energy subsidies (D.3), Malta {y}", cof[("MT", "D3", "MIO_EUR", y)],
        "EUR million", S_COF, f"{cof[('MT', 'D3', 'PC_GDP', y)]}% of GDP")
base = cof[("MT", "D3", "MIO_EUR", 2019)]
add("COFOG 2023 above the 2019 level", round(cof[("MT", "D3", "MIO_EUR", 2023)] - base, 1), "EUR million",
    "calculated", "a rough measure of the crisis support; the minister's 2023 figure is EUR 242.5 million (energy and food)")
add("IMF Article IV 2023 (1.4% of GDP) in euros", round(imf[2023] * gdp[2023] / 100, 1), "EUR million",
    "IMF CR 26/29 Table 2 (data/cc-113/other_estimates_transcribed.csv) x Eurostat GDP")
add("Government DBP 2024: 2023 expected (1.7% of GDP, other basic commodities included) in euros",
    round(gov[2023] * gdp[2023] / 100, 1), "EUR million", "DBP 2024 (data/cc-113/) x Eurostat GDP")
add("Commission subsidy inventory, Malta 2023 (fossil-fuel subsidies; with stand-in)", round(inv23, 1),
    "EUR million", "data/cc-113/ec_inventory_malta_facts.csv", f"with the EUR 28.2m stand-in {inv23_tbc:.1f}")
add("Government DBP 2025: 2025 planned (0.72% of GDP) in euros", round(gov[2025] * gdp[2025] / 100, 1), "EUR million",
    "DBP 2025 (data/cc-113/) x Eurostat GDP")
add("IMF Article IV 2025 projection (0.8% of GDP) in euros", round(imf[2025] * gdp[2025] / 100, 1), "EUR million",
    "IMF CR 26/29 x Eurostat GDP")
# five-year total
rest = five - (m23 + m25 + m26)
add("Five-year total (EUR 1,350 million) less the three years given: implied 2022 plus 2024", round(rest, 1),
    "EUR million", "calculated from S01-S03, S07")
c2224 = cof[("MT", "D3", "MIO_EUR", 2022)] + cof[("MT", "D3", "MIO_EUR", 2024)]
add("COFOG 04.3 subsidies 2022 plus 2024", round(c2224, 1), "EUR million", S_COF,
    f"{c2224 - 2 * base:.1f} above twice the 2019 level")
# planned vs outturn, 2023
plan23 = float(st["F04"]["value"])
add("Draft Budgetary Plan 2023 (Oct 2022): energy subsidies allocated for 2023", plan23, "EUR million",
    "MFAC USP 2023-2026 assessment, Box C, p. 89", "electricity 500 + gas fund 15 + petroleum 80")
add("Update of Stability Programme (spring 2023): energy subsidies for 2023", float(st["F05"]["value"]), "EUR million",
    "MFAC Box C, p. 89")
add("Minister's 2023 figure (energy and food) as share of the Oct 2022 allocation", round(100 * m23 / plan23), "%",
    "calculated")
add("Oct 2022 allocation for 2023 as a multiple of the minister's 2023 figure", round(plan23 / m23, 1), "times",
    "calculated", "the allocation equals the Commission database's 2023 entries for Malta (CC-113)")
add("Commission inventory 2023, Enemalta line plus Gas Stabilisation Fund", float(inv["Energy Support Measures (compensation to Enemalta)"]["y2023"]) +
    float(inv["Gas Stabilisation Fund"]["y2023"]), "EUR million", "data/cc-113/ec_inventory_malta_facts.csv",
    "equals the DBP 2023 allocation (500 + 80 + 15 = 595); the Enemalta line 580 = 500 + 80")
# 2026 forecasts of total subsidies
f06, f07, f08 = (float(st[k]["value"]) for k in ("F06", "F07", "F08"))
gdp26 = 26087.5    # APR 2026 nominal GDP forecast, MFAC APR26 assessment table p. 8 (F07 note)
add("Total subsidies 2026: DBP 2026 forecast (Oct 2025)", f06, "EUR million", "MFAC DBP26 assessment")
add("Total subsidies 2026: APR 2026 forecast (Apr 2026)", f07, "EUR million", "MFAC APR26 assessment",
    f"+{f07 - f06:.1f} on the DBP 2026 forecast")
add("APR 2026: higher allocation for energy-related subsidies, about 0.3% of GDP", round(0.003 * gdp26, 1),
    "EUR million", "MFAC APR26 assessment p. 29; GDP 2026 forecast 26,087.5 (same report)")
add("Minister's 2026 increase on 2025 less the APR 2026 energy uplift", round((m26 - m25) - 0.003 * gdp26, 1),
    "EUR million", "calculated", "the September figure implies a further upward revision after April; different "
    "bases (energy and food subsidies vs ESA subsidies), so indicative only")
add("Total subsidies 2025 outturn", f08, "EUR million", "MFAC Council Note 03/2026, p. 7")
add("Total subsidies Q1 2026", 119.0, "EUR million", "MFAC Council Note 03/2026, p. 7",
    f"{100 * 119.0 / f07:.1f}% of the APR 2026 forecast for the year")

# ================================================================ E. 'the only country'
for y in (2022, 2023, 2024):
    d = {g: cof[(g, "D3", "PC_GDP", y)] for g in EU27 if (g, "D3", "PC_GDP", y) in cof}
    order = sorted(d, key=lambda g: -d[g])
    rank = 1 + sum(1 for v in d.values() if v > d["MT"])
    ties = sum(1 for v in d.values() if v == d["MT"])
    rk = f"{rank}" if ties == 1 else f"joint {rank}-{rank + ties - 1}"
    add(f"COFOG 04.3 subsidies as % of GDP, {y}: Malta and rank", f"{d['MT']} ({rk} of {len(d)})",
        "% of GDP", S_COF, "top five: " + ", ".join(f"{g} {d[g]}" for g in order[:5]) +
        f"; EU-27 {cof[('EU27_2020', 'D3', 'PC_GDP', y)]}")
add("EU: budgetary cost of 2026 energy measures adopted 1 Mar-4 May 2026", float(st["F10"]["value"]), "EUR billion",
    "European Commission, Spring 2026 forecast box", "0.07% of EU GDP")

with open(D / "checks.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["check", "value", "unit", "source", "note"], lineterminator="\r\n")
    w.writeheader()
    w.writerows(rows)

# ---------------------------------------------------------------- cost series for Figure 3
cs = []
for y in range(2019, 2025):
    cs.append({"series": "Eurostat COFOG 04.3 fuel and energy subsidies (outturn)", "year": y,
               "eur_million": cof[("MT", "D3", "MIO_EUR", y)], "kind": "outturn"})
for y, v, k in ((2023, m23, "as presented"), (2025, m25, "as presented"), (2026, m26, "projection"),
                (2027, m27, "forecast")):
    cs.append({"series": "Minister, 30 Sep 2026: energy and food subsidies", "year": y, "eur_million": v, "kind": k})
for y in (2022, 2023, 2024):
    cs.append({"series": "IMF Article IV (share of Eurostat GDP)", "year": y,
               "eur_million": round(imf[y] * gdp[y] / 100, 1), "kind": "estimate"})
cs.append({"series": "IMF Article IV (share of Eurostat GDP)", "year": 2025,
           "eur_million": round(imf[2025] * gdp[2025] / 100, 1), "kind": "projection"})
cs.append({"series": "Draft Budgetary Plan 2023: allocation for 2023", "year": 2023, "eur_million": plan23,
           "kind": "allocation"})
cs.append({"series": "Commission subsidy inventory (CC-113)", "year": 2023, "eur_million": round(inv23, 1),
           "kind": "as booked"})
with open(D / "cost_series.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["series", "year", "eur_million", "kind"], lineterminator="\r\n")
    w.writeheader()
    w.writerows(cs)
for r in rows:
    print(f"{r['check']}: {r['value']} {r['unit']}  [{r['note']}]")
print(len(rows), "checks written", dt.date.today())
