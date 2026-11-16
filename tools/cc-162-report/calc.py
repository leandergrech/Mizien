#!/usr/bin/env python3
"""CC-162: test the Commission's Malta sentences in COM(2026) 601 with formulas. Run fetch.py first.

Inputs: data/cc-162/ (EEA 2026 datasets, Commission statements typed from COM(2026) 601, printed pages) and, for the
inputs that did not change, data/cc-094/ (legal inputs; EEA 2025 projections, which the 2026 dataset still carries for
Malta; checks from CC-094). Writes data/cc-162/checks.csv.
"""
import csv, pathlib
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parents[2]
D, D4 = ROOT / "data" / "cc-162", ROOT / "data" / "cc-094"
EU27 = "BE BG CZ DK DE EE IE EL ES FR HR IT CY LV LT LU HU MT NL AT PL PT RO SI SK FI SE".split()
S26 = "EEA, ESR emissions 2005-2025 (GHG_ESD-ESR_2026_updated01102026.xlsx), retrieved 16 Nov 2026"
S25 = "EEA, GHG projections 2025 submission (data/cc-094/), retrieved 6 Oct 2026"
S_LAW = "Implementing Decisions (EU) 2020/2126, 2024/1884, 2026/895; Regulations (EU) 2018/842, 2023/857"


def rows_of(p):
    return [r for r in csv.DictReader(open(p)) if not r[next(iter(r))].startswith("#")]


esr = {int(r["year"]): float(r["value"]) for r in rows_of(D / "eea_esr_malta_2026.csv")}
esr25 = {}
for r in rows_of(D4 / "eea_esr_emissions.csv"):
    if r["country"] == "Malta" and r["series"] in ("ESD", "ESR") and r["value"]:
        esr25[int(r["year"])] = float(r["value"]) * 1000
proj = defaultdict(dict)
for r in rows_of(D4 / "eea_ghg_projections_esr.csv"):
    if r["submission"].startswith("2025"):
        proj[(r["country"], r["category"], r["scenario"])][int(r["year"])] = float(r["value_gapfilled"])
base, target, aea, law = {}, {}, {}, {}
for r in rows_of(D4 / "esr_legal_inputs.csv"):
    if r["item"] == "2005 ESR base":
        base[r["country"]] = float(r["value"]) / 1000
    elif r["item"] == "2030 target vs 2005":
        target[r["country"]] = float(r["value"])
    elif r["item"] == "Annual emission allocation":
        aea[int(r["year"])] = float(r["value"]) / 1000
    else:
        law[(r["item"], r["country"])] = float(r["value"])
subs = {r["country"]: r["submission_years_in_dataset"] for r in rows_of(D / "eea_projections_2026_submissions.csv")}
m26 = rows_of(D / "eea_projections_2026_malta_rows.csv")
com = {r["figure"]: r["value"] for r in rows_of(D / "com2026_statements.csv")}
rows = []


def add(check, value, unit, source, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": source, "note": note})


def pct(a, b):
    return 100 * (a / b - 1)


B, T = base["MT"], target["MT"]
LIMIT = B * (1 + T / 100)
wem, wam = proj[("MT", "Total excluding LULUCF", "WEM")], proj[("MT", "Total excluding LULUCF", "WAM")]

# A-C: the note to Figure 13 (p. 46)
for name, s, key in (("WEM (existing measures)", wem, 61), ("WAM (additional measures)", wam, 49)):
    add(f"Malta 2030 vs 2005, {name}", round(pct(s[2030], B), 1), "%", "calculated", f"{s[2030]:.1f} / {B:.1f} kt")
    add(f"Malta gap to the 2030 target, {name}", round(pct(s[2030], B) - T, 1), "pp", "calculated", f"Commission 2026: {key} pp (p. 46)")
add("Commission's 49 and 61 reproduced to the nearest point",
    "yes" if round(pct(wam[2030], B) - T) == 49 and round(pct(wem[2030], B) - T) == 61 else "NO", "", "calculated")
add("2030 limit (2005 base x 0.81)", round(LIMIT, 1), "kt CO2e", "calculated", f"Decision 2026/895: {aea[2030]:.1f} kt")
add("WAM 2030 projection minus the 2005 level", round(wam[2030] - B, 1), "kt CO2e", "calculated")
add("WEM 2030 projection minus the 2005 level", round(wem[2030] - B, 1), "kt CO2e", "calculated")

# What changed in the data between the two editions: Malta's projections
add("Countries with a 2026 submission in the EEA 2026 projections dataset", ", ".join(sorted(c for c, v in subs.items() if "2026" in v and c != "EU27")),
    "", "EEA GHG_Projections_2026 datahub_dataset.xlsx, retrieved 16 Nov 2026", "Malta is not one of them")
add("Malta's submission year in the 2026 dataset", subs["MT"], "submission year", "EEA GHG_Projections_2026 datahub_dataset.xlsx")
for m in m26:
    if m["sheet"] == "Totals":
        old = (wem if m["scenario"] == "WEM" else wam)[2027]
        add(f"Malta 2027 total, {m['scenario']}: 2026 dataset minus 2025 dataset", round(float(m["gapfilled_value"]) - old, 6), "kt CO2e",
            "EEA 2025 and 2026 projections datasets", f"{float(m['gapfilled_value']):.4f} kt in both")
f26 = {m["scenario"]: float(m["gapfilled_value"]) for m in m26 if m["sheet"] == "Gas"}
add("Malta 2030 F-gas (HFC) gap WEM minus WAM, 2026 dataset", round(f26["WEM"] - f26["WAM"], 1), "kt CO2e", "EEA 2026 projections dataset",
    "CC-094 found the industrial-process difference 34.4 kt in the 2025 dataset")

# Emissions: reviewed values and the new 2025 approximation
for y in (2021, 2022, 2023, 2024, 2025):
    add(f"Malta effort-sharing emissions {y} vs 2005", round(pct(esr[y], B), 1), "%", S26,
        f"{esr[y]:.1f} kt" + ("; approximated" if y == 2025 else "") + (f"; 2025 edition of the dataset: {esr25[y]:.1f} kt" if y in esr25 else ""))
for y in range(2021, 2026):
    add(f"Malta {y}: emissions minus annual allocation", round(esr[y] - aea[y], 1), "kt CO2e", "calculated", f"allocation {aea[y]:.1f} kt")
add("2025 approximated emissions vs the March 2025 projection for 2025", round(pct(esr[2025], wam[2025]), 1), "%", "calculated",
    f"{esr[2025]:.1f} vs {wam[2025]:.1f} kt (WEM = WAM in 2025)")
add("Cut needed from 2025 to the 2030 limit", round(pct(LIMIT, esr[2025]), 1), "%", "calculated",
    f"{esr[2025]:.1f} -> {LIMIT:.1f} kt; {100 * ((LIMIT / esr[2025]) ** (1 / 5) - 1):.1f}% a year")
for sc, s in (("WAM", wam), ("WEM", wem)):
    add(f"Projected change 2025-2030, {sc}", round(pct(s[2030], esr[2025]), 1), "%", "calculated")

# Ledger with the 2026 data: 2021-2025 actual/approximated, 2026-2030 projected
ETS = law[("ETS flexibility total 2021-2030", "MT")] / 1000
LUL = law[("LULUCF flexibility maximum 2021-2030", "MT")] * 1000
for sc, s in (("WAM", wam), ("WEM", wem)):
    e = {**{y: esr[y] for y in range(2021, 2026)}, **{y: s[y] for y in range(2026, 2031)}}
    c25 = sum(aea[y] - e[y] for y in range(2021, 2026))
    c30 = sum(aea[y] - e[y] for y in range(2021, 2031))
    c2630 = sum(aea[y] - e[y] for y in range(2026, 2031))
    add(f"Cumulative allocations minus emissions 2021-2025, {sc}, with 2025 approximated", round(c25 / 1000, 2), "Mt CO2e", "calculated")
    add(f"Same, after the ETS flexibility, {sc}", round((c25 + ETS) / 1000, 2), "Mt CO2e", "calculated", f"ETS {ETS:.1f} kt (Decision 2024/1884)")
    add(f"Cumulative allocations minus emissions 2026-2030, {sc}", round(c2630 / 1000, 2), "Mt CO2e", "calculated")
    add(f"Cumulative allocations minus emissions 2021-2030, {sc}", round(c30 / 1000, 2), "Mt CO2e", "calculated")
    add(f"Same, after ETS and maximum LULUCF, {sc}", round((c30 + ETS + LUL) / 1000, 2), "Mt CO2e", "calculated", f"LULUCF maximum {LUL:.0f} kt")
    short = -(c30 + ETS + LUL) / 1000
    add(f"Remaining shortfall as a share of the EU surplus the Commission now gives (about 140 Mt), {sc}", round(100 * short / 140, 1), "%",
        "calculated", f"{short:.2f} Mt / 140 Mt (COM(2026) 601, p. 47)")
# banking test: year-by-year with banking only from the 2021 surplus
bal = 0.0
for y in range(2021, 2031):
    e = esr[y] if y <= 2025 else wam[y]
    bal += aea[y] - e
    if y in (2025, 2030):
        add(f"Running balance after {y} (banking, no borrowing), WAM", round(bal / 1000, 2), "Mt CO2e", "calculated")

# Ranking on the 2025-submission data (Germany and Ireland have 2026 updates not reproduced here)
gaps = {}
for cc in EU27:
    for sc in ("WEM", "WAM"):
        v = proj[(cc, "Total excluding LULUCF", sc)][2030]
        gaps[(cc, sc)] = pct(v, base[cc]) - target[cc]
for sc in ("WAM", "WEM"):
    order = sorted(EU27, key=lambda c: -gaps[(c, sc)])
    add(f"Gap ranking in percentage points, {sc}, top 5 (2025 submissions)", ", ".join(f"{c} {gaps[(c, sc)]:.1f}" for c in order[:5]), "pp",
        S25, f"Commission 2026 names: {com['largest_gaps']}; DE and IE have 2026 updates in the EEA dataset that are not recomputed here")
    add(f"Largest overachievement, {sc}, top 3 (2025 submissions)", ", ".join(f"{c} {gaps[(c, sc)]:.1f}" for c in order[::-1][:3]), "pp",
        S25, f"Commission 2026 names: {com['largest_over']}")

# 2025 edition vs 2026 edition wording (typed from both reports)
add("Member States asked for a corrective action plan, 2026 edition", 9, "count", "COM(2026) 601, p. 47", com["cap_states"])
add("Member States projected to exceed allocations in 2026-2030, 2025 edition", 6, "count", "COM(2025) 668, p. 31", "AT, EE, DE, MT, IE, SE")
add("Member States projected to exceed allocations in 2026-2030, 2026 edition", 8, "count", "COM(2026) 601, p. 46", com["excess_2026_2030"])

with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
for r in rows:
    print(f"{r['check'][:96]:96s} {r['value']!s:>14} {r['unit']}  {r['note']}")
