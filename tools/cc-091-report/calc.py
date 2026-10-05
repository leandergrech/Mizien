#!/usr/bin/env python3
"""CC-091: test the OHSA 2025 annual report figures. Reads data/cc-091/ (OHSA annual reports, transcribed 5 Oct 2026;
Eurostat via fetch.py) and writes data/cc-091/checks.csv."""
import csv, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-091"
o = {(r["item"], int(r["year"])): float(r["value"]) for r in csv.DictReader(open(D / "ohsa_annual_reports.csv"))}
fat = {(r["unit"], r["nace_r2"], int(r["year"])): float(r["value"]) for r in csv.DictReader(open(D / "eurostat_hsw_n2_02.csv"))}
emp = {int(r["year"]): float(r["value"]) for r in csv.DictReader(open(D / "eurostat_nama_10_pe.csv"))}
rows = []


def add(check, value, unit, source, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": source, "note": note})


AR = "OHSA Annual Report 2025, Table 14"
i = lambda y: o[("Inspections (total)", y)]
DIV = ("Construction", "General", "Engineering", "Chemicals/Biological", "Accident Investigation")
add("Inspections 2025 / 2024", round(i(2025) / i(2024), 2), "times", AR, "'more than doubled' needs > 2.00")
add("Inspections 2025 vs 2024, change", round(100 * (i(2025) / i(2024) - 1), 1), "%", AR, "report states +152.8%")
add("Inspections 2024 vs 2023, change", round(100 * (i(2024) / i(2023) - 1), 1), "%", AR, "report states +262.8%")
add("Inspections 2023 vs 2022, change", round(100 * (i(2023) / i(2022) - 1), 1), "%", AR, "report states -41.1%")
add("Inspections 2025 / 2023", round(i(2025) / i(2023), 2), "times", AR, "minister's comparison year in the press report")
add("Inspections 2025 / 2021-2022 average", round(i(2025) / ((i(2021) + i(2022)) / 2), 2), "times", AR)
add("Sum of divisions 2025 (Table 18)", sum(o[(f"Inspections: {k}", 2025)] for k in DIV), "inspections", "OHSA AR 2025 Table 18", "should equal 23,711")
add("Sum of divisions 2024 (Table 18)", sum(o[(f"Inspections: {k}", 2024)] for k in DIV), "inspections", "OHSA AR 2025 Table 18", "should equal 9,381")
add("Construction inspections 2025 / 2024", round(o[("Inspections: Construction", 2025)] / o[("Inspections: Construction", 2024)], 2), "times", "OHSA AR 2025 Table 18")
add("Construction share of 2025 inspections", round(100 * o[("Inspections: Construction", 2025)] / i(2025), 1), "%", "OHSA AR 2025 Table 18", "report: 'approximately 80%'")
a, ordr, stop = (o[(f"Construction inspections: {k}", 2025)] for k in ("adequate compliance (%)", "orders issued (%)", "stop work orders (%)"))
add("Construction outcomes sum (adequate + orders + stop works)", a + ordr + stop, "%", "OHSA AR 2025 Table 6")
add("Construction inspections not rated adequate", ordr + stop, "%", "OHSA AR 2025 Table 6")
add("Stop-work orders implied if 5% applied to all 2025 construction inspections", round(stop / 100 * o[("Inspections: Construction", 2025)]), "orders (approx.)",
    "Table 6 x Table 18", "rounded percentage; compare the next row")
add("Stop Orders issued in 2025, all sectors (Table 17)", 526, "orders", "OHSA AR 2025 Table 17 (monthly Table 16 also sums to 526)",
    "smaller than the implied figure above, so Table 6's percentages cannot be a share of all 19,296 construction inspections; base unstated")
add("Improvement notices + Orders implied for 21% of construction inspections", round(ordr / 100 * o[("Inspections: Construction", 2025)]), "inspections (approx.)",
    "Table 6 x Table 18", "report: 'more than 2,500' orders in construction; Table 17 totals 1,616 notices + 2,759 orders in all sectors")
add("Fatal accidents 2025 (Table 1)", o[("Accident investigations: fatal", 2025)], "deaths", "OHSA AR 2025 Table 1")
add("Fatal accidents 2025, by sector (Table 5) sum", sum(o[(f"Fatal accidents: {k}", 2025)] for k in ("Agriculture", "Construction", "Transportation and storage")), "deaths", "OHSA AR 2025 Table 5")
add("Fatal accidents 2025, by nationality sum", o[("Fatal accidents: Maltese nationals", 2025)] + o[("Fatal accidents: third-country nationals", 2025)], "deaths", "OHSA AR 2025 s.4.2.6")
add("Third-country nationals, share of 2025 deaths", round(100 * o[("Fatal accidents: third-country nationals", 2025)] / o[("Accident investigations: fatal", 2025)], 1), "%", "OHSA AR 2025 s.4.2.6")
EU = "Eurostat hsw_n2_02 (fatal accidents at work), retrieved 5 Oct 2026"
for y in (2022, 2023, 2024):
    add(f"Eurostat fatal accidents at work, Malta, all activities, {y}", fat[("NR", "TOTAL", y)], "deaths", EU, "2025 not yet published by Eurostat")
add("Eurostat fatal accidents at work, Malta, construction, 2024", fat[("NR", "F", 2024)], "deaths", EU)
deaths = {2023: o[("Fatal accidents at place of work", 2023)], 2024: o[("Fatal accidents investigated", 2024)], 2025: o[("Accident investigations: fatal", 2025)]}
for y, n in deaths.items():
    add(f"Crude fatality rate per 100,000 persons employed, {y} (OHSA deaths / Eurostat employment)", round(100 * n / emp[y], 2), "per 100,000",
        "OHSA AR 2023-2025; Eurostat nama_10_pe EMP_DC", "crude, domestic-concept employment; OHSA's own 2024 figure is 1.22 (denominator unstated)")
add("Deaths 2025 vs 2024 (OHSA)", f"{deaths[2025]:.0f} vs {deaths[2024]:.0f}", "deaths", "OHSA AR 2024 s.3.2.4; AR 2025 Table 1", "up four while inspections rose 2.5 times")
with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for r in rows:
    print(f"{r['check'][:90]:90s} {str(r['value']):>10} {r['unit']}")
