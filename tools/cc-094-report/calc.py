#!/usr/bin/env python3
"""CC-094: test the Commission's Malta sentences in COM(2025) 668 with formulas, not by eye.

Inputs (all in data/cc-094/ unless stated; source URL and retrieval date on every row):
- eea_esr_emissions.csv          EEA effort-sharing emissions 2005-2024 (fetch.py, 6 Oct 2026)
- eea_ghg_projections_esr.csv    EEA GHG projections, 2025 and 2023 submissions (fetch.py, 6 Oct 2026)
- esr_legal_inputs.csv           2005 bases, 2030 targets, Malta's allocations and flexibilities (typed from the
                                 implementing decisions and regulations, read 6 Oct 2026)
- com2025_668_statements.csv     the figures the Commission states (typed, printed page numbers)
- data/cc-003/capr2025_esr_malta.csv        the Commission's SWD Tables 25-26 for Malta (typed for CC-003)
- data/cc-003/eurostat_ghg_population.csv   Eurostat nama_10_pe population (retrieved 2 Oct 2026 for CC-003)
Writes data/cc-094/checks.csv and prints every line.
"""
import csv, math, pathlib
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-094"
D3 = ROOT / "data" / "cc-003"
EU27 = "BE BG CZ DK DE EE IE EL ES FR HR IT CY LV LT LU HU MT NL AT PL PT RO SI SK FI SE".split()
S_ESR = "EEA, ESR emissions 2005-2024 (GHG_ESD-ESR_2025.xlsx), retrieved 6 Oct 2026"
S_PRJ = "EEA, GHG projections 2025 submission (GHG_projections_2025_EEA_incl_pivots.xlsx), retrieved 6 Oct 2026"
S_LAW = "Implementing Decisions (EU) 2020/2126, 2024/1884, 2026/895; Regulations (EU) 2018/842, 2023/857"
S_COM = "COM(2025) 668 final"
S_SWD = "Commission SWD, CAPR 2025, Tables 25-26 (typed in data/cc-003/capr2025_esr_malta.csv)"


def rows_of(path):
    return [r for r in csv.DictReader(open(path)) if not r[next(iter(r))].startswith("#")]


# ------------------------------------------------------------------ inputs
esr, esr_status = {}, {}
for r in rows_of(D / "eea_esr_emissions.csv"):
    if r["series"] in ("ESD", "ESR") and r["value"]:
        esr[(r["country"], int(r["year"]))] = float(r["value"]) * 1000   # kt
        esr_status[(r["country"], int(r["year"]))] = r["eea_status"]
    elif r["series"] == "ESD base year 2005":
        esd_base_mt = float(r["value"]) * 1000
proj = defaultdict(dict)        # (submission, country, category, scenario) -> {year: kt}
for r in rows_of(D / "eea_ghg_projections_esr.csv"):
    sub = "2025" if r["submission"].startswith("2025") else "2023"
    proj[(sub, r["country"], r["category"], r["scenario"])][int(r["year"])] = float(r["value_gapfilled"])
base, target, aea, law = {}, {}, {}, {}
for r in rows_of(D / "esr_legal_inputs.csv"):
    if r["item"] == "2005 ESR base":
        base[r["country"]] = float(r["value"]) / 1000            # kt
    elif r["item"] == "2030 target vs 2005":
        target[r["country"]] = float(r["value"])
    elif r["item"] == "Annual emission allocation":
        aea[int(r["year"])] = float(r["value"]) / 1000          # kt
    else:
        law[(r["item"], r["country"])] = float(r["value"])
com = {r["figure"]: r["value"] for r in rows_of(D / "com2025_668_statements.csv")}
swd = {(r["series"], r["year"]): r["value"] for r in csv.DictReader(open(D3 / "capr2025_esr_malta.csv"))
       if not r["table"].startswith("#")}
pop = {int(r["year"]): float(r["value"]) for r in csv.DictReader(open(D3 / "eurostat_ghg_population.csv"))
       if r["geo"] == "MT" and r["item"] == "POP_NC"}

rows = []


def add(check, value, unit, source, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": source, "note": note})


def pct(a, b):
    return 100 * (a / b - 1)


B = base["MT"]
T = target["MT"]
LIMIT = B * (1 + T / 100)
wem = proj[("2025", "MT", "Total excluding LULUCF", "WEM")]
wam = proj[("2025", "MT", "Total excluding LULUCF", "WAM")]

# ------------------------------------------------------------------ A-C: the note to Figure 13 (p. 30)
add("Malta 2005 effort-sharing emissions used for the targets", round(B, 1), "kt CO2e", "Decision 2020/2126 Annex I")
add("Malta 2030 target", T, "% vs 2005", "Regulation (EU) 2023/857 Annex I", "COM p. 30 says 19% reduction target")
add("Malta 2030 limit = 2005 base x (1 + target)", round(LIMIT, 1), "kt CO2e", "calculated",
    f"2030 allocation in Decision 2026/895: {aea[2030]:.1f} kt; Malta's NECP p. 54: 826.7 kt")
for name, s in (("WEM (existing measures)", wem), ("WAM (additional measures)", wam)):
    ch = pct(s[2030], B)
    gap = ch - T
    add(f"Malta 2030 projection, {name}", round(s[2030], 1), "kt CO2e", S_PRJ)
    add(f"Malta 2030 vs 2005, {name}", round(ch, 1), "%", "calculated", f"{s[2030]:.1f} / {B:.1f}")
    add(f"Malta gap to the 2030 target, {name}", round(gap, 1), "pp", "calculated",
        f"Commission: {com['gap_wem' if 'WEM' in name else 'gap_wam']} pp (COM p. 30); SWD Table 25 p. 114: "
        f"{swd[('Malta distance to target WEM' if 'WEM' in name else 'Malta distance to target WAM', '2030')]} pp")
    add(f"Malta 2030 excess over the limit, {name}", round(s[2030] - LIMIT, 1), "kt CO2e", "calculated")
add("Commission's 49 and 61 reproduced to the nearest point",
    "yes" if (round(pct(wam[2030], B) - T) == int(com["gap_wam"]) and round(pct(wem[2030], B) - T) == int(com["gap_wem"]))
    else "NO", "", "calculated")
# robustness: other 2005 values in circulation
for lab, b in (("EEA 2005 estimate (ESD basis, AR4 GWPs)", esr[("Malta", 2005)]),
               ("ESD base year 2005 (2013-2020 rules)", esd_base_mt)):
    add(f"Malta 2030 WAM vs 2005, using the {lab}", round(pct(wam[2030], b), 1), "%", "calculated",
        f"2005 = {b:.1f} kt; WEM: {pct(wem[2030], b):+.1f}%")
# projections start above the reviewed 2023 value: rescale to it
r23 = esr[("Malta", 2023)] / wam[2023]
add("Projection's 2023 starting value vs reviewed 2023 emissions", round(pct(wam[2023], esr[("Malta", 2023)]), 1), "%",
    "calculated", f"projection {wam[2023]:.1f} kt; reviewed {esr[('Malta', 2023)]:.1f} kt (EEA, ESR review)")
for name, s in (("WEM", wem), ("WAM", wam)):
    add(f"Malta 2030 {name} rescaled to reviewed 2023, vs 2005", round(pct(s[2030] * r23, B), 1), "%", "calculated",
        "sensitivity: projection x (reviewed 2023 / projected 2023)")
# 2023 submission
for sc in ("WEM", "WAM"):
    s23 = proj[("2023", "MT", "Total excluding LULUCF", sc)]
    add(f"Malta 2030 {sc}, 2023 submission, vs 2005", round(pct(s23[2030], B), 1), "%", S_PRJ.replace("2025 submission", "2023 submission"),
        f"{s23[2030]:.1f} kt")

# ------------------------------------------------------------------ history and latest year
for y in (2021, 2022, 2023, 2024):
    sw = swd.get(("Malta ESR emissions vs 2005", str(y)))
    add(f"Malta effort-sharing emissions {y} vs 2005", round(pct(esr[("Malta", y)], B), 1), "%", S_ESR,
        f"{esr[('Malta', y)]:.1f} kt; {esr_status[('Malta', y)]}; SWD Table 25: {sw}%")
for y in (2021, 2022, 2023, 2024):
    add(f"Malta {y}: emissions minus annual allocation", round(esr[("Malta", y)] - aea[y], 1), "kt CO2e", "calculated",
        f"allocation {aea[y]:.1f} kt")
add("2024 approximated emissions vs the 2025 projection's value for 2024", round(pct(esr[("Malta", 2024)], wam[2024]), 1),
    "%", "calculated", f"{esr[('Malta', 2024)]:.1f} vs {wam[2024]:.1f} kt (WEM = WAM in 2024)")
cut = pct(LIMIT, esr[("Malta", 2024)])
add("Cut needed from 2024 to reach the 2030 limit", round(cut, 1), "%", "calculated",
    f"{esr[('Malta', 2024)]:.1f} -> {LIMIT:.1f} kt; {100 * ((LIMIT / esr[('Malta', 2024)]) ** (1 / 6) - 1):.1f}% a year")
add("Malta effort-sharing emissions, average yearly change 2005-2024", round(100 * ((esr[("Malta", 2024)] / B) ** (1 / 19) - 1), 1),
    "% a year", "calculated", "from the 2005 base to the 2024 approximated value")
add("Projected change 2024-2030, WAM", round(pct(wam[2030], esr[("Malta", 2024)]), 1), "%", "calculated")
add("Projected change 2024-2030, WEM", round(pct(wem[2030], esr[("Malta", 2024)]), 1), "%", "calculated")

# per person (fairness: population growth)
for y in (2005, 2024):
    e = B if y == 2005 else esr[("Malta", y)]
    add(f"Malta effort-sharing emissions per person, {y}", round(e / pop[y], 2), "t CO2e", "calculated",
        f"{e:.1f} kt / {pop[y]:.2f} thousand people (Eurostat nama_10_pe)")
add("Change per person 2005-2024", round(pct(esr[("Malta", 2024)] / pop[2024], B / pop[2005]), 1), "%", "calculated",
    "CC-003 proxy (national total minus power generation): 2.50 -> 2.52 t")
add("Population change 2005-2024", round(pct(pop[2024], pop[2005]), 1), "%", "Eurostat nama_10_pe (via data/cc-003)")
add("2030 limit per person at the 2024 population", round(LIMIT / pop[2024], 2), "t CO2e", "calculated")

# sectors, 2023 and 2030
SECT = [("Transport", "1.A.3. Transport"), ("Manufacturing and construction (fuel)", "1.A.2. Manufacturing industries and construction"),
        ("Industrial processes (mainly F-gases)", "2. Industrial processes"), ("Agriculture", "3. Agriculture"),
        ("Waste", "5. Waste")]
for sc in ("WEM", "WAM"):
    en = proj[("2025", "MT", "1. Energy", sc)]
    for y in (2023, 2030):
        tot = proj[("2025", "MT", "Total excluding LULUCF", sc)][y]
        parts = {lab: proj[("2025", "MT", cat, sc)][y] for lab, cat in SECT}
        other = en[y] - parts["Transport"] - parts["Manufacturing and construction (fuel)"]
        parts["Buildings and other fuel use"] = other
        for lab, v in parts.items():
            add(f"{sc} {y}: {lab}", round(v, 1), "kt CO2e", S_PRJ,
                f"{100 * v / tot:.0f}% of the total" + ("; 1. Energy minus 1.A.3 and 1.A.2" if lab.startswith("Buildings") else ""))
        add(f"{sc} {y}: sum of sectors minus total", round(sum(parts.values()) - tot, 3), "kt CO2e", "calculated", "should be 0")
for lab, cat in SECT:
    d = proj[("2025", "MT", cat, "WEM")][2030] - proj[("2025", "MT", cat, "WAM")][2030]
    add(f"2030 WEM minus WAM: {lab}", round(d, 1), "kt CO2e", "calculated")

# ------------------------------------------------------------------ D: largest gaps (p. 30)
gaps = {}
for cc in EU27:
    b = base[cc]
    for sc in ("WEM", "WAM"):
        v = proj[("2025", cc, "Total excluding LULUCF", sc)][2030]
        gaps[(cc, sc)] = (pct(v, b) - target[cc], (v - b * (1 + target[cc] / 100)) / 1000)
for sc in ("WAM", "WEM"):
    order = sorted(EU27, key=lambda c: -gaps[(c, sc)][0])
    add(f"Largest 2030 gaps in percentage points, {sc}", ", ".join(f"{c} {gaps[(c, sc)][0]:.1f}" for c in order[:4]),
        "pp", "calculated", f"Commission (p. 30): {com['largest_gaps']}")
    add(f"Largest 2030 overachievement, {sc}", ", ".join(f"{c} {gaps[(c, sc)][0]:.1f}" for c in order[::-1][:3]),
        "pp", "calculated", f"Commission (p. 30): {com['largest_over']}")
    ordt = sorted(EU27, key=lambda c: -gaps[(c, sc)][1])
    add(f"Largest 2030 gaps in tonnes, {sc}", ", ".join(f"{c} {gaps[(c, sc)][1]:.1f}" for c in ordt[:3]), "Mt CO2e",
        "calculated", f"Malta {gaps[('MT', sc)][1]:.2f} Mt, rank {ordt.index('MT') + 1} of 27")
add("Belgium's projection is from its 2024 submission (gap-filled by the EEA)",
    sorted({r["submission_year"] for r in rows_of(D / "eea_ghg_projections_esr.csv") if r["country"] == "BE"})[0],
    "submission year", S_PRJ, "COM p. 17: Belgium had not submitted in 2025")

# ------------------------------------------------------------------ E-F: allocations and flexibilities
ems = {y: esr[("Malta", y)] for y in (2021, 2022, 2023, 2024)}
ETS = law[("ETS flexibility total 2021-2030", "MT")] / 1000
LUL = law[("LULUCF flexibility maximum 2021-2030", "MT")] * 1000
for sc, s in (("WAM", wam), ("WEM", wem)):
    e = {**ems, **{y: s[y] for y in range(2025, 2031)}}
    c25 = sum(aea[y] - e[y] for y in range(2021, 2026))
    c30 = sum(aea[y] - e[y] for y in range(2021, 2031))
    add(f"Cumulative allocations minus emissions 2021-2025, {sc}", round(c25 / 1000, 2), "Mt CO2e", "calculated",
        "2021-2024 reviewed/approximated, 2025 projected; SWD Table 26: -0.4 Mt")
    add(f"Cumulative allocations minus emissions 2021-2030, {sc}", round(c30 / 1000, 2), "Mt CO2e", "calculated",
        "allocations from Decision 2026/895; SWD Table 26 (Commission estimate, WAM): -2.1 Mt")
    add(f"Same, 2021-2025, after the ETS flexibility, {sc}", round((c25 + ETS) / 1000, 2), "Mt CO2e", "calculated",
        f"ETS flexibility {ETS:.1f} kt (Decision 2024/1884), assumed usable when needed, as the Commission assumes (COM p. 31)")
    add(f"Same, 2021-2030, after the ETS flexibility, {sc}", round((c30 + ETS) / 1000, 2), "Mt CO2e", "calculated")
    add(f"Same, 2021-2030, after ETS and the maximum LULUCF flexibility, {sc}", round((c30 + ETS + LUL) / 1000, 2),
        "Mt CO2e", "calculated", f"LULUCF maximum {LUL:.0f} kt (Annex III), only if credits exist")
    short = -(c30 + ETS + LUL) / 1000
    add(f"Shortfall to cover by buying allocations, {sc}, as a share of the EU surplus",
        f"{100 * short / float(com['eu_surplus_high']):.1f}-{100 * short / float(com['eu_surplus_low']):.1f}",
        "%", "calculated", f"{short:.2f} Mt against {com['eu_surplus_low']}-{com['eu_surplus_high']} Mt (COM p. 31)")
add("2021 one-off adjustment in the 2021 allocation", law[("2021 one-off adjustment", "MT")] / 1000, "kt CO2e",
    "Regulation (EU) 2018/842, Annex IV", f"2021 surplus {aea[2021] - ems[2021]:.1f} kt; without the adjustment: "
    f"{aea[2021] - law[('2021 one-off adjustment', 'MT')] / 1000 - ems[2021]:+.1f} kt")
add("2021 surplus vs the 75% banking limit", f"{(aea[2021] - ems[2021]):.1f} / {0.75 * aea[2021]:.1f}", "kt CO2e",
    "calculated", "the whole 2021 surplus can be banked (Regulation 2023/857, Article 5(3)(a))")
add("ETS flexibility check: 2% x 4 years + 7% x 6 years of the 2005 base", round(B * (0.02 * 4 + 0.07 * 6), 1), "kt CO2e",
    "calculated", f"Decision 2024/1884: {ETS:.1f} kt")
add("Malta eligible for the safety reserve", "no" if law[("Safety reserve eligibility", "MT")] == 0 else "yes", "",
    "Commission Decision (EU) 2023/863, recital (5)", "2013-2020 emissions above allocations")
for y in range(2026, 2031):
    est = swd.get(("Malta estimated AEAs", str(y)))
    add(f"Allocation {y}: adopted (Decision 2026/895) vs Commission estimate (SWD Table 26)", f"{aea[y] / 1000:.3f} / {est}",
        "Mt CO2e", S_LAW)

with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
for r in rows:
    print(f"{r['check'][:88]:88s} {r['value']!s:>16} {r['unit']}  {r['note']}")
