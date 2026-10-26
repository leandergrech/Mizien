#!/usr/bin/env python3
"""CC-123: test KPMG's '8,716 residential units approved in 2024 (+7.4%), 5,170 in H1 2025 (+9.7%)'.

Reads data/cc-123/ and writes data/cc-123/checks.csv.
"""
import csv, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-123"
rows = []


def add(check, value, unit, source, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": source, "note": note})


R = lambda x, n=2: round(x, n)
K = {r["item"]: r for r in csv.DictReader(open(D / "kpmg_text.csv"))}
PA = {int(r["year"]): int(r["approved_units_total"]) for r in csv.DictReader(open(D / "pa_approved_dwellings_2022_2025.csv"))}
Q = {}
for r in csv.DictReader(open(D / "nso_quarterly_secondhand.csv")):
    Q[(int(r["year"]), r["quarter"])] = (int(r["permits"]), int(r["dwellings"]))
qd = lambda y, q: Q[(y, q)][1]
qp = lambda y, q: Q[(y, q)][0]
yr = lambda y, f: sum(f(y, q) for q in ("Q1", "Q2", "Q3", "Q4"))

# 1. The 2024 total and the 7.4% against the Planning Authority series
add("KPMG prints: units approved 2024", K["Residential units granted approval in 2024"]["value"], "units", "KPMG p. 37")
add("PA approved dwelling units 2023", PA[2023], "units", "PA, via data/cc-013 (transcribed 3 Oct 2026)")
add("PA approved dwelling units 2024", PA[2024], "units", "PA, via data/cc-013 (transcribed 3 Oct 2026)", "equals KPMG's 8,716")
g_pa = 100 * (PA[2024] / PA[2023] - 1)
add("PA 2024 on 2023", R(g_pa), "%", "calculated", "KPMG prints 7.4%")
add("PA 2024 on 2023, rounded to one decimal", R(g_pa, 1), "%", "calculated")

# 2. NSO quarterly releases (second-hand)
n23, n24 = yr(2023, qd), yr(2024, qd)
add("NSO quarterly dwellings, sum Q1-Q4 2023 (second-hand)", n23, "dwellings", "nso_quarterly_secondhand.csv",
    "equals PA 2023 (8,112)")
add("NSO quarterly dwellings, sum Q1-Q4 2024 (second-hand)", n24, "dwellings", "nso_quarterly_secondhand.csv",
    "PA and KPMG: 8,716; difference 1")
add("NSO quarterly 2024 on 2023 (second-hand)", R(100 * (n24 / n23 - 1)), "%", "calculated")
p23, p24 = yr(2023, qp), yr(2024, qp)
add("NSO building permits (count), sum 2023 (second-hand)", p23, "permits", "nso_quarterly_secondhand.csv")
add("NSO building permits (count), sum 2024 (second-hand)", p24, "permits", "nso_quarterly_secondhand.csv",
    "MaltaToday, citing parliamentary data, gave 1,749")
add("NSO permits 2024 on 2023 (second-hand)", R(100 * (p24 / p23 - 1)), "%", "calculated")
add("Dwellings per building permit, 2024", R(n24 / p24), "ratio", "calculated")

# 3. January to June 2025 against January to June 2024
h24 = qd(2024, "Q1") + qd(2024, "Q2")
h25 = qd(2025, "Q1") + qd(2025, "Q2")
add("NSO dwellings January-June 2024 (second-hand)", h24, "dwellings", "nso_quarterly_secondhand.csv")
add("NSO dwellings January-June 2025 (second-hand)", h25, "dwellings", "nso_quarterly_secondhand.csv",
    "equals KPMG's 5,170 'permits'")
add("NSO dwellings H1 2025 on H1 2024 (second-hand)", R(100 * (h25 / h24 - 1)), "%", "calculated", "KPMG prints 9.7%")
hp24 = qp(2024, "Q1") + qp(2024, "Q2")
hp25 = qp(2025, "Q1") + qp(2025, "Q2")
add("NSO building permits (count) January-June 2025 (second-hand)", hp25, "permits", "nso_quarterly_secondhand.csv",
    "KPMG's 5,170 is not this count")
add("NSO building permits (count) H1 2025 on H1 2024 (second-hand)", R(100 * (hp25 / hp24 - 1)), "%", "calculated")
add("KPMG 5,170 less NSO dwellings H1 2025", int(K["Permits 'sanctioned' January to June 2025, as printed"]["value"]) - h25,
    "dwellings", "calculated", "0 means KPMG's 'permits' are dwelling units")

# 4. The forecast: 2025 surpasses 2024
q13 = sum(qd(2025, q) for q in ("Q1", "Q2", "Q3"))
add("NSO dwellings Q1-Q3 2025 (second-hand)", q13, "dwellings", "nso_quarterly_secondhand.csv")
add("NSO dwellings Q1-Q3 2025 less PA 2024 total", q13 - PA[2024], "dwellings", "calculated",
    "positive: nine months of 2025 already exceed all of 2024")
add("PA approved dwelling units 2025", PA[2025], "units", "PA, via data/cc-013 (transcribed 3 Oct 2026)",
    "series titled 2007-2025; assumed full year")
add("PA 2025 on 2024", R(100 * (PA[2025] / PA[2024] - 1)), "%", "calculated")
add("Implied Q4 2025 (PA 2025 less NSO Q1-Q3, second-hand)", PA[2025] - q13, "dwellings", "calculated",
    "implied, not an NSO figure")
# KPMG's simple projection: H1 growth carried to the full year
add("KPMG's own projection logic: 2024 total x (1 + H1 growth)", round(PA[2024] * h25 / h24), "units", "calculated",
    "illustration of 'assumption that H1 growth continues'; actual PA 2025 is higher")

# 5. Eurostat cross-check (different measure: residential buildings with 2+ dwellings, index 2021 = 100)
d = json.load(open(D / "sts_cobp_a_MT_DW.json"))
t = d["dimension"]["time"]["category"]["index"]
E = {int(y): d["value"].get(str(i)) for y, i in t.items()}
for y in (2023, 2024, 2025):
    add(f"Eurostat sts_cobp_a Malta, dwellings in 2+ dwelling buildings, {y}", E[y], "index 2021=100", "Eurostat sts_cobp_a",
        "no status flag in the extract")
add("Eurostat index 2024 on 2023", R(100 * (E[2024] / E[2023] - 1)), "%", "calculated", "different scope from PA/NSO")
add("Eurostat index 2025 on 2024", R(100 * (E[2025] / E[2024] - 1)), "%", "calculated")

with open(D / "checks.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, ["check", "value", "unit", "source", "note"])
    w.writeheader()
    w.writerows(rows)
for r in rows:
    print(f"{r['check'][:90]:90s} {r['value']} {r['unit']}")
