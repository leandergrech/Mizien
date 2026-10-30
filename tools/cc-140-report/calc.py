#!/usr/bin/env python3
"""CC-140: test "Malta's energy import dependency is approximately 98.0 per cent, the highest in the European Union"
(Ministry for Finance, Pre-Budget Document 2027) against Eurostat nrg_ind_id and nrg_bal_c (run fetch.py first).
Writes data/cc-140/checks.csv. Rebuild: indicator = (imports - exports) / gross available energy (GAE), total, ktoe."""
import csv, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-140"
EU = {"BE", "BG", "CZ", "DK", "DE", "EE", "IE", "EL", "ES", "FR", "HR", "IT", "CY", "LV", "LT", "LU", "HU", "MT", "NL", "AT",
      "PL", "PT", "RO", "SI", "SK", "FI", "SE"}
ind = {(r["geo"], int(r["year"])): float(r["value_pc"]) for r in csv.DictReader(open(D / "eurostat_nrg_ind_id.csv"))}
bal = {(r["balance"], int(r["year"])): float(r["value_ktoe"]) for r in csv.DictReader(open(D / "eurostat_nrg_bal_c_MT.csv"))}
SRC = "Eurostat nrg_ind_id (updated 2026-07-16) and nrg_bal_c (updated 2026-08-27), retrieved 2026-10-30"
rows = []
add = lambda c, v, u, n="": rows.append({"check": c, "value": v, "unit": u, "source": SRC, "note": n})
for y in range(2019, 2025):
    add(f"Malta import dependency {y}", round(ind[("MT", y)], 1), "%")
    eu = sorted(((v, g) for (g, yy), v in ind.items() if yy == y and g in EU), reverse=True)
    add(f"Malta rank among EU-27, {y}", [g for _, g in eu].index("MT") + 1, "rank", f"next: {eu[1][1]} {eu[1][0]:.1f}%")
    add(f"EU-27 average {y}", round(ind[("EU27_2020", y)], 1), "%")
    reb = 100 * (bal[("IMP", y)] - bal[("EXP", y)]) / bal[("GAE", y)]
    add(f"Malta rebuilt (imports-exports)/GAE {y}", round(reb, 1), "%", f"indicator {ind[('MT', y)]:.1f}%")
    add(f"Malta international maritime bunkers / GAE {y}", round(100 * bal[("INTMARB", y)] / bal[("GAE", y)], 1), "%")
add("Malta 2024 minus 98.0", round(ind[("MT", 2024)] - 98.0, 1), "points", "latest year available")
add("Years 2019-2024 with a value within 1 point of 98.0", sum(abs(ind[("MT", y)] - 98.0) <= 1 for y in range(2019, 2025)), "years")
add("Years 2015-2024 Malta ranks first", sum(1 for y in range(2015, 2025) if max((v, g) for (g, yy), v in ind.items() if yy == y and g in EU)[1] == "MT"), "years")
with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for r in rows: print(r["check"], r["value"], r["unit"], r["note"])
