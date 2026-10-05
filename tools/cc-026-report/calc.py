#!/usr/bin/env python3
"""CC-026: recompute the Eurostat '+169.4% in Malta's greenhouse gas emissions 2015-2025' and test what drives it.

Reads data/cc-026/ (Eurostat env_ac_ainah_r2 and env_air_gge; retrieved 5 Oct 2026) and writes data/cc-026/checks.csv.
"""
import csv, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-026"
A = {int(r["year"]): r for r in csv.DictReader(open(D / "malta_ainah_ghg.csv"))}
U = {int(r["year"]): r for r in csv.DictReader(open(D / "malta_unfccc_inventory.csv"))}
EU = {r["geo"]: r for r in csv.DictReader(open(D / "eu_ainah_ghg_total_hh.csv"))}
f = lambda r, k: float(r[k])
rows = []


def add(check, value, unit, source, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": source, "note": note})


pct = lambda a, b: 100 * (b / a - 1)
ch = {g: pct(float(r["y2015"]), float(r["y2025"])) for g, r in EU.items() if r["y2015"] and r["y2025"]}
countries = {g: v for g, v in ch.items() if g != "EU27_2020"}
rank = sorted(countries, key=countries.get, reverse=True)
add("Malta: all-activity emissions 2015 -> 2025", f"{f(A[2015], 'TOTAL_HH'):.0f} -> {f(A[2025], 'TOTAL_HH'):.0f}",
    "kt CO2e", "Eurostat env_ac_ainah_r2", "2025 is an early estimate")
add("Malta: change 2015-2025 (recomputed)", round(ch["MT"], 1), "%", "Eurostat env_ac_ainah_r2",
    "Eurostat release of 16 Jun 2026 and Newsbook: +169.4% (series since revised)")
add("EU-27: change 2015-2025", round(ch["EU27_2020"], 1), "%", "Eurostat env_ac_ainah_r2", "Eurostat release: -17.2%")
add("Member states with higher emissions in 2025 than 2015", sum(v > 0 for v in countries.values()), f"of {len(countries)}",
    "Eurostat env_ac_ainah_r2", ", ".join(f"{g} {countries[g]:+.1f}%" for g in rank[:4]))
add("Malta: rank of increase", 1, f"of {len(countries)}", "Eurostat env_ac_ainah_r2",
    f"next: {rank[1]} {countries[rank[1]]:+.1f}%")
add("Malta: share of 2025 EU-27 total", round(100 * float(EU["MT"]["y2025"]) / float(EU["EU27_2020"]["y2025"]), 2), "%",
    "Eurostat env_ac_ainah_r2")
# decomposition (2015-2024: last year with activity detail)
t15, t24 = f(A[2015], "TOTAL_HH"), f(A[2024], "TOTAL_HH")
h15, h24 = f(A[2015], "H51"), f(A[2024], "H51")
add("Malta: change 2015-2024, all activities and households", round(pct(t15, t24), 1), "%", "Eurostat env_ac_ainah_r2")
add("Malta: air transport (NACE H51) 2015 -> 2024", f"{h15:.0f} -> {h24:.0f}", "kt CO2e", "Eurostat env_ac_ainah_r2",
    f"x{h24 / h15:.1f}")
add("Air transport: share of the 2015-2024 increase", round(100 * (h24 - h15) / (t24 - t15), 1), "%", "calculated")
add("Air transport: share of Malta total, 2015 -> 2024", f"{100 * h15 / t15:.0f} -> {100 * h24 / t24:.0f}", "%", "calculated")
add("Malta excluding air transport: 2015 -> 2024", f"{t15 - h15:.0f} -> {t24 - h24:.0f}", "kt CO2e", "calculated",
    f"{pct(t15 - h15, t24 - h24):+.1f}%")
add("Malta: electricity, gas, steam (NACE D) 2015 -> 2024", f"{f(A[2015], 'D'):.0f} -> {f(A[2024], 'D'):.0f}", "kt CO2e",
    "Eurostat env_ac_ainah_r2", f"{pct(f(A[2015], 'D'), f(A[2024], 'D')):+.1f}%")
add("Malta: 2025 vs 2024 (all activities, early estimate)", round(pct(t24, f(A[2025], "TOTAL_HH")), 1), "%", "calculated")
# territorial inventory
u15, u24 = f(U[2015], "TOTX4_MEMO"), f(U[2024], "TOTX4_MEMO")
add("Malta: UNFCCC inventory total (no LULUCF, no memo items) 2015 -> 2024", f"{u15:.0f} -> {u24:.0f}", "kt CO2e",
    "Eurostat env_air_gge", f"{pct(u15, u24):+.1f}%")
add("Malta: UNFCCC inventory change 2005-2024", round(pct(f(U[2005], 'TOTX4_MEMO'), u24), 1), "%", "Eurostat env_air_gge")
i15, i24 = f(U[2015], "CRF1D1A"), f(U[2024], "CRF1D1A")
add("Malta: international aviation, memo item (fuel sold in Malta) 2015 -> 2024", f"{i15:.0f} -> {i24:.0f}", "kt CO2e",
    "Eurostat env_air_gge", f"{pct(i15, i24):+.1f}%")
add("Malta 2024: Eurostat account total vs UNFCCC inventory total", round(t24 / u24, 2), "ratio", "calculated",
    f"{t24:.0f} vs {u24:.0f} kt")
add("Malta 2024: air transport (account) vs international aviation memo item", round(h24 / i24, 1), "ratio", "calculated",
    "residence principle (operator) vs fuel bunkered in Malta")

with open(D / "checks.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
for x in rows:
    print(f"{x['check']:78s} {str(x['value']):>16} {x['unit']:10s} {x['note']}")
