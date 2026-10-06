#!/usr/bin/env python3
"""CC-029: plausibility checks on the project's published figures, and the timeline, against Eurostat electricity data.

Inputs: data/cc-029/eurostat_electricity.csv (fetch.py; Eurostat nrg_cb_e, retrieved 6 Oct 2026) and the figures stated
by InterConnect Malta (icm.mt project page, read 6 Oct 2026): about 300 MW, up to 0.8 TWh a year, "around 25% of Malta's
overall electricity demand as it stood in 2025" (ICM news, 22 Apr 2026). Writes data/cc-029/checks.csv."""
import csv, pathlib, datetime
ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-029"
v = {(r["code"], int(r["year"])): (float(r["value_gwh"]), r["flag"]) for r in csv.DictReader(open(D / "eurostat_electricity.csv"))}
SRC = "Eurostat nrg_cb_e (E7000, GWh), retrieved 6 Oct 2026; ICM project page and news of 22 Apr 2026"
CAP_MW, E_GWH = 300.0, 800.0
rows = []
def add(check, value, unit, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": SRC, "note": note})
add("Implied capacity factor (0.8 TWh a year from 300 MW)", round(100 * E_GWH / (CAP_MW * 8760 / 1000), 1), "%", "800 GWh / (300 MW x 8,760 h)")
for y in (2024, 2025):
    fc, gep, imp, exp = v[("FC", y)][0], v[("GEP", y)][0], v[("IMP", y)][0], v[("EXP", y)][0]
    sup = gep + imp - exp
    fl = "; ".join(sorted({v[(k, y)][1] for k in ("FC", "GEP", "IMP", "EXP") if v[(k, y)][1]})) or "none"
    add(f"Final electricity consumption {y}", fc, "GWh", f"flags: {fl}")
    add(f"Electricity supplied (production + imports - exports) {y}", round(sup, 1), "GWh", "flags as above")
    add(f"0.8 TWh as share of final consumption {y}", round(100 * E_GWH / fc, 1), "%")
    add(f"0.8 TWh as share of electricity supplied {y}", round(100 * E_GWH / sup, 1), "%")
add("Share of 2025 supply that was imported", round(100 * v[("IMP", 2025)][0] / (v[("GEP", 2025)][0] + v[("IMP", 2025)][0] - v[("EXP", 2025)][0]), 1), "%", "interconnector imports")
d = lambda a, b: (datetime.date.fromisoformat(b) - datetime.date.fromisoformat(a)).days
add("Days from PQQ launch (5 Dec 2024) to submissions deadline (21 Jul 2025, extended from 28 Mar 2025)", d("2024-12-05", "2025-07-21"), "days", "ICM news 5 Dec 2024, 27 Mar 2025; TVM News 22 Jul 2025")
add("Extension of the submissions deadline", d("2025-03-28", "2025-07-21"), "days", "28 Mar 2025 (original, offshoreWIND.biz) to 21 Jul 2025 (ICM)")
add("Days from the submissions deadline to 30 Jun 2026 (end of 'the first part' of 2026, our reading)", d("2025-07-21", "2026-06-30"), "days")
add("Days from 30 Jun 2026 to the check date (6 Oct 2026)", d("2026-06-30", "2026-10-06"), "days", "no public notice of candidates qualifying or of the dialogue stage found on ICM's news list")
with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for r in rows: print(f"{r['check'][:90]:90s} {r['value']:>8} {r['unit']}")
