#!/usr/bin/env python3
"""CC-143: recompute every figure in the report.
Reads data/cc-143/document_facts.csv, data/cc-101/wise_2022_groundwater_status.csv and data/cc-101/eurostat_env_wat_abs.csv.
Writes data/cc-143/checks.csv."""
import csv
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-143"
D101 = ROOT / "data" / "cc-101"
rows = []


def add(check, value, unit, source, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": source, "note": note})


F = {r["id"]: float(r["value"]) for r in csv.DictReader(open(D / "document_facts.csv")) if r["unit"] != "date"}
N = F["swd26_gwb_total"]
pct = lambda n: round(100 * n / N, 1)
S26, S19 = "SWD(2026) 702", "SWD(2019) 48"

# ---- the claim's percentages are whole numbers of the 15 bodies
add("Good quantitative status, 2nd plan: 13 of 15", pct(F["swd19_quant_good_n_2nd"]), "%", S19, "claim: 86.7%")
add("Good quantitative status, 3rd plan: 11 of 15", pct(F["swd26_quant_good_n_3rd"]), "%", S26, "claim: 73.3%")
add("Change in good quantitative status", round(100 * (11 - 13) / N, 1), "percentage points", "calculated",
    "13.3 points = 2 bodies")
add("One groundwater body is", pct(1), "percentage points", "calculated", "with 15 bodies")
add("Poor quantitative status, 3rd plan: 4 of 15", pct(F["swd26_quant_poor_n_3rd"]), "%", S26, "document: 26.7%")
add("Poor quantitative status: 2nd + good = 15", F["swd19_quant_poor_n_2nd"] + F["swd19_quant_good_n_2nd"], "bodies", S19)
add("Poor quantitative status: 3rd + good = 15", F["swd26_quant_poor_n_3rd"] + F["swd26_quant_good_n_3rd"], "bodies", S26)
add("SWD(2026) and SWD(2019) agree on 2 poor bodies in the 2nd plan",
    F["swd26_quant_poor_n_2nd"] == F["swd19_quant_poor_n_2nd"], "check", "both documents")
add("Poor quantitative status, 1st / 2nd / 3rd plan",
    f"{int(F['swd19_quant_poor_n_1st'])} / {int(F['swd19_quant_poor_n_2nd'])} / {int(F['swd26_quant_poor_n_3rd'])}", "bodies",
    "SWD(2019) 48 p. 79; SWD(2026) 702 p. 8", "the 3rd plan is back at the 1st plan's count")
add("Poor quantitative status, 1st / 2nd / 3rd plan",
    f"{pct(F['swd19_quant_poor_n_1st'])} / {pct(F['swd19_quant_poor_n_2nd'])} / {pct(F['swd26_quant_poor_n_3rd'])}", "%",
    "calculated")
add("Good chemical status, 2nd plan: 3 of 15", pct(F["swd19_chem_good_n_2nd"]), "%", S19, "claim: 'a fifth'")
add("Good chemical status, 2nd plan: 15 - 12 poor", N - F["swd26_chem_poor_n_2015"], "bodies", S26,
    "SWD(2026) section 4.2 says 12 of 15 poor in 2015")
add("Poor chemical status, 1st / 2nd / 3rd plan",
    f"{int(F['swd19_chem_poor_n_1st'])} / {int(F['swd19_chem_poor_n_2nd'])} / {int(F['swd26_chem_poor_n_2021'])}", "bodies",
    "SWD(2019) 48 p. 86; SWD(2026) 702 p. 28")
add("Nitrates cause failure in 80% of 15 bodies", round(F["swd26_nitrate_fail_pct"] / 100 * N, 2), "bodies", S26,
    "whole number expected: 12")
add("Chloride 73.3% / sodium 53.3% / saline 46.7% of 15 bodies",
    f"{round(F['swd26_chloride_fail_pct'] / 100 * N, 2)} / {round(F['swd26_sodium_fail_pct'] / 100 * N, 2)} / "
    f"{round(F['swd26_saline_fail_pct_summary'] / 100 * N, 2)}", "bodies", S26)
add("Saline-intrusion bodies: summary table vs section 4.2 text",
    f"{round(F['swd26_saline_fail_pct_summary'] / 100 * N)} vs {int(F['swd26_saline_fail_n_section42'])} "
    f"(section 3.3 says {int(F['swd26_saline_fail_n_section33'])})", "bodies", S26,
    "the document is not consistent with itself on this point; not part of the claim")
add("Quantitative monitoring, 2nd to 3rd plan",
    f"{int(F['swd26_quant_monitored_2nd'])} to {int(F['swd26_quant_monitored_3rd'])} of 15 bodies", "bodies", S26,
    "SWD(2019) 48 itself gives both 2 (section 5.1.1) and 3 (p. 13) monitored bodies")
add("Unmonitored for quantity, 3rd plan", pct(F["swd26_quant_not_monitored_n"]), "% of bodies", S26, "document: 53.3%")

# ---- EEA WISE, 2022 reporting (assessment year 2021)
WS = "EEA WISE WFD 2022 reporting, retrieved 2026-10-06 (data/cc-101/)"
W = list(csv.DictReader(open(D101 / "wise_2022_groundwater_status.csv")))
q_good = [r for r in W if r["quantitative_status"] == "Good"]
q_poor = [r for r in W if r["quantitative_status"] == "Poor"]
c_poor = [r for r in W if r["chemical_status"] == "Poor"]
add("WISE bodies reported", len(W), "bodies", WS)
add("WISE good quantitative status", len(q_good), "bodies", WS, "matches SWD(2026): 11")
add("WISE poor quantitative status", len(q_poor), "bodies", WS, ", ".join(r["name"].title() for r in q_poor))
add("WISE poor chemical status", len(c_poor), "bodies", WS, "matches SWD(2026): all 15")
add("WISE assessment year(s), quantitative", ", ".join(sorted({r["quantitative_assessment_year"] for r in W})), "year", WS)
add("WISE counts equal the SWD(2026) counts",
    (len(q_good), len(q_poor), len(c_poor)) == (F["swd26_quant_good_n_3rd"], F["swd26_quant_poor_n_3rd"], F["swd26_chem_poor_n_2021"]),
    "check", WS)

# ---- Eurostat: estimated groundwater abstraction (a context check on 'overabstraction')
ES = "Eurostat env_wat_abs, retrieved 2026-10-06 (data/cc-101/)"
E = {int(r["year"]): (float(r["value"]), r["flag"]) for r in csv.DictReader(open(D101 / "eurostat_env_wat_abs.csv"))
     if r["wat_src"] == "FGW" and r["wat_proc"] == "ABST"}
mean = lambda a, b: round(sum(E[y][0] for y in range(a, b + 1)) / (b - a + 1), 2)
add("Fresh groundwater abstraction, 2015 / 2021", f"{E[2015][0]} / {E[2021][0]}", "million m3", ES, "all flagged e (estimated)")
add("Change 2015 to 2021", round(100 * (E[2021][0] / E[2015][0] - 1), 1), "%", "calculated")
add("Mean 2010-2015 / mean 2016-2021", f"{mean(2010, 2015)} / {mean(2016, 2021)}", "million m3", ES)
add("Change in the six-year means", round(100 * (mean(2016, 2021) / mean(2010, 2015) - 1), 1), "%", "calculated")
add("Highest and lowest year, 2010-2024",
    f"{max(E, key=lambda y: E[y][0])}: {max(v for v, _ in E.values())}; {min(E, key=lambda y: E[y][0])}: {min(v for v, _ in E.values())}",
    "million m3", ES)

with open(D / "checks.csv", "w", newline="", encoding="utf-8") as f:
    wr = csv.DictWriter(f, fieldnames=list(rows[0]))
    wr.writeheader()
    wr.writerows(rows)
for r in rows:
    print(f"{r['check'][:75]:75s} {str(r['value']):>22} {r['unit']}")
