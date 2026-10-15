#!/usr/bin/env python3
"""CC-118: test the Council's recital (30) figures on Malta's water (draft Council Recommendation, 3 Jul 2026).
Inputs: data/cc-118/*.csv (run fetch.py first). Output: data/cc-118/checks.csv"""
import csv, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-118"
rd = lambda n: list(csv.DictReader(open(D / n, encoding="utf-8")))
rows = []
def add(check, value, unit, source, note=""):
    rows.append([check, round(value, 2) if isinstance(value, float) else value, unit, source, note])

# ---- A. seasonal WEI+ (EEA chart, 2023) and annual (Eurostat sdg_06_60)
eea = rd("eea_worst_seasonal_wei_2023.csv")
eu27 = {"Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czechia", "Denmark", "Estonia", "Finland", "France", "Germany",
        "Greece", "Hungary", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg", "Malta", "Netherlands", "Poland",
        "Portugal", "Romania", "Slovakia", "Slovenia", "Spain", "Sweden"}
mem = sorted(((float(r["max_seasonal_wei_plus_pct"]), r["country"], r["worst_quarter"]) for r in eea if r["country"] in eu27), reverse=True)
add("EU Member States in the EEA chart (2023)", len(mem), "countries", "EEA chart data", "Italy..Sweden; list in eea_worst_seasonal_wei_2023.csv")
mt = next(m for m in mem if m[1] == "Malta")
add("Malta: worst seasonal WEI+ 2023", mt[0], "%", "EEA chart data", f"quarter {mt[2]}")
add("Malta's rank among EU Member States (1 = highest)", [m[1] for m in mem].index("Malta") + 1, "rank", "calculated")
add("Highest: " + mem[0][1], mem[0][0], "%", "EEA chart data", f"quarter {mem[0][2]}")
add("Third highest: " + mem[2][1], mem[2][0], "%", "EEA chart data")
add("Malta's WEI+ as multiple of the third-highest Member State", mt[0] / mem[2][0], "x", "calculated")
add("Member States at or above 40% in their worst quarter", sum(1 for m in mem if m[0] >= 40), "countries", "calculated", "40% is the severe-scarcity threshold in Eurostat's metadata (document_facts.csv); Cyprus and Malta only")
es = rd("eurostat_sdg_06_60.csv")
EU2 = {"AT","BE","BG","HR","CY","CZ","DK","EE","FI","FR","DE","EL","HU","IE","IT","LV","LT","LU","MT","NL","PL","PT","RO","SK","SI","ES","SE"}
for si, lab in (("VAL_A", "annual value"), ("AVG_4Y", "four-year average")):
    v = sorted(((float(r["wei_plus_pct"]), r["geo"]) for r in es if r["statinfo"] == si and r["year"] == "2023" and r["geo"] in EU2), reverse=True)
    d = {g: x for x, g in v}
    add(f"Eurostat WEI+ 2023, {lab}: Malta", d["MT"], "%", f"Eurostat sdg_06_60 ({si})", "calendar year; national")
    add(f"  Malta's rank among EU Member States", [g for x, g in v].index("MT") + 1, "rank", "calculated", "; ".join(f"{g} {x}" for x, g in v[:3]))
ro_q = next(float(r["max_seasonal_wei_plus_pct"]) for r in eea if r["country"] == "Romania")
ro_a = next(float(r["wei_plus_pct"]) for r in es if r["geo"] == "RO" and r["year"] == "2023" and r["statinfo"] == "VAL_A")
add("Romania 2023: EEA worst-quarter WEI+ (Nov 2025 chart)", ro_q, "%", "EEA chart data")
add("Romania 2023: Eurostat annual WEI+ (updated 28 Apr 2026)", ro_a, "%", "Eurostat sdg_06_60", "annual above the worst quarter of the EEA chart: the two vintages/methods differ for Romania")

# ---- B. surface water bodies (EEA WISE, WFD 2022 reporting)
sw = rd("wise_2022_surface_water_status.csv")
bod = [r for r in sw if r["category"] != "TeW"]
ter = [r for r in sw if r["category"] == "TeW"]
n = len(bod)
add("Surface water bodies (excl. territorial waters)", n, "bodies", "EEA WISE", "9 coastal, 5 transitional, 3 river, 2 lake")
good_eco = [r for r in bod if r["ecological_status_code"] in ("1", "2")]
add("Good or high ecological status/potential", len(good_eco), "bodies", "EEA WISE")
add("  share by number (denominator 19)", len(good_eco) / n * 100, "%", "calculated", "Council: 58%")
add("  share by number if territorial waters counted (denominator 20)", len(good_eco) / (n + len(ter)) * 100, "%", "calculated", "territorial waters carry no ecological status")
for cat, lab in (("CW", "coastal"), ("TW", "transitional"), ("RW", "river"), ("LW", "lake")):
    c = [r for r in bod if r["category"] == cat]
    add(f"  {lab}: good or high / total", f"{sum(r['ecological_status_code'] in ('1','2') for r in c)} of {len(c)}", "bodies", "EEA WISE")
a = lambda r: float(r["area_km2"] or 0)
tot_area = sum(a(r) for r in bod)
add("Surface water bodies: total area (river by length excluded)", tot_area, "km2", "EEA WISE", "rivers have a length only (3.4 km in all)")
add("  area at good or high ecological status", sum(a(r) for r in good_eco), "km2", "EEA WISE")
add("  share by area", sum(a(r) for r in good_eco) / tot_area * 100, "%", "calculated", "contrast with the by-number figure")
add("  coastal water bodies' share of the area", sum(a(r) for r in bod if r["category"] == "CW") / tot_area * 100, "%", "calculated")
good_chem = [r for r in sw if r["chemical_status_code"] == "2"]
add("Good chemical status (all 20 incl. territorial waters)", len(good_chem), "bodies", "EEA WISE")
add("  share, denominator 20 (territorial waters status 'Unknown')", len(good_chem) / len(sw) * 100, "%", "calculated", "Council: 45%")
add("  share, denominator 19 (excl. territorial waters)", len(good_chem) / n * 100, "%", "calculated")
add("  bodies 'failing to achieve good' chemical status", sum(r["chemical_status_code"] == "3" for r in sw), "bodies", "EEA WISE", "all river, lake and transitional bodies")
add("  chemical status 'without UPBT' differs from headline in", 0, "bodies", "EEA WISE field swChemicalStatusValueWithoutUPBT (queried 2026-10-15)", "identical for all 20 bodies; see notes.md")
add("Surface water assessment years", "2017-2020 (coastal), 2021-2022 (other)", "", "EEA WISE")

# ---- C. groundwater bodies
gw = rd("wise_2022_groundwater_status.csv")
tot = sum(a(r) for r in gw)
poor_q = [r for r in gw if r["quantitative_status_code"] == "3"]
add("Groundwater bodies", len(gw), "bodies", "EEA WISE")
add("  total area", tot, "km2", "EEA WISE")
add("  poor quantitative status: bodies", len(poor_q), "bodies", "EEA WISE", ", ".join(r["eu_code"] for r in poor_q))
add("  poor quantitative status: share by number", len(poor_q) / len(gw) * 100, "%", "calculated")
add("  poor quantitative status: area", sum(a(r) for r in poor_q), "km2", "EEA WISE")
add("  poor quantitative status: share by area", sum(a(r) for r in poor_q) / tot * 100, "%", "calculated", "Council: 82%")
add("  largest body (Malta Mean Sea Level) share of total area", a(next(r for r in gw if r["eu_code"] == "MT001")) / tot * 100, "%", "calculated")
add("  poor chemical status: bodies", sum(r["chemical_status_code"] == "3" for r in gw), "of 15", "EEA WISE", "Council: 100%")
add("  poor chemical status: share by area", sum(a(r) for r in gw if r["chemical_status_code"] == "3") / tot * 100, "%", "calculated")
# ---- D. EWA groundwater-level trends
tr = rd("ewa_gw_level_trends.csv")
neg = sum(r["trend"].startswith("Significant negative") for r in tr)
add("EWA monitoring boreholes with a table row", len(tr), "boreholes", "EWA technical document (May 2024), Table 1")
add("  significant negative trend", neg, "boreholes", "EWA Table 1", "text of the document says 62.9% (22 of 35); table rows give 21")
add("  share with a negative trend (table rows)", neg / len(tr) * 100, "%", "calculated")

with open(D / "checks.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["check", "value", "unit", "source", "note"])
    w.writerows(rows)
for r in rows:
    print(r[0], "=", r[1], r[2], "|", r[4])
