#!/usr/bin/env python3
"""CC-115: test "traffic congestion imposed an estimated cost of €770 million on the Maltese economy, equivalent to
3.4% of GDP" (Malta Chamber, LEAD proposals, 14 May 2026).

Reads data/cc-115/eurostat_nama_10_gdp.csv (fetch.py; Eurostat nama_10_gdp, updated 2 Oct 2026, retrieved 5 Oct
2026) and data/cc-115/congestion_estimates.csv (the National Transport Master Plan 2030 figures, read 5 Oct 2026),
and writes data/cc-115/checks.csv. A cost in euros of 2025 is compared with GDP in euros of 2025 (current prices);
the other ratios are shown because the Chamber's text uses real GDP elsewhere.
"""
import csv, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-115"
g = {(r["unit"], int(r["year"])): float(r["value"]) for r in csv.DictReader(open(D / "eurostat_nama_10_gdp.csv"))}
est = list(csv.DictReader(open(D / "congestion_estimates.csv")))
COST = float(est[0]["value_meur"])
SRC = "Eurostat nama_10_gdp (updated 2 Oct 2026), retrieved 5 Oct 2026; National Transport Master Plan 2030 p. 124"
rows = []


def add(check, value, unit, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": SRC, "note": note})


for unit, y, lab in (("CP_MEUR", 2025, "nominal GDP 2025 (current prices)"), ("CP_MEUR", 2024, "nominal GDP 2024"),
                     ("CLV20_MEUR", 2025, "real GDP 2025 (chain-linked, 2020 prices)"),
                     ("CLV15_MEUR", 2025, "real GDP 2025 (chain-linked, 2015 prices)")):
    add(f"Malta: {lab}", round(g[(unit, y)], 1), "EUR million")
    add(f"EUR {COST:.0f} million as a share of {lab}", round(100 * COST / g[(unit, y)], 2), "%")
add("EUR 770 million as a share of the Chamber's own GDP figure (EUR 20.40 billion, real, 2025)", round(100 * COST / 20400, 2), "%",
    "the Chamber's text gives real GDP of EUR 20.40bn for 2025")
add("GDP that would make EUR 770 million equal to 3.4%", round(COST / 0.034), "EUR million", "for comparison with the series above")
add("Chamber's 2015 real GDP (EUR 11.34bn) vs Eurostat CLV20 2015", round(g[("CLV20_MEUR", 2015)], 1), "EUR million",
    "matches: the Chamber's GDP series is chain-linked volumes at 2020 prices (an earlier vintage for 2025)")
add("Plan: projected increase 2025 to 2030", round(100 * (917 / 770 - 1), 1), "%", "EUR 770m to EUR 917m")
add("Plan: implied annual growth 2025-2030", round(100 * ((917 / 770) ** 0.2 - 1), 2), "%/yr")
with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for r in rows:
    print(f"{r['check'][:90]:90s} {r['value']:>10} {r['unit']}")
