#!/usr/bin/env python3
"""CC-031: scale check for Gozo's electric buses against Malta's emissions (Eurostat, retrieved 6 Oct 2026).

Reads data/cc-031/eurostat_ghg_pop.csv (fetch.py). The operator's estimate of 1,300 t CO2 a year saved (TVM News,
4 Jul 2026, quoting Malta Public Transport) is an input taken from that report, not our own figure. Gozo has no
emissions inventory of its own in Eurostat, so Gozo's share is a population-proportional approximation, labelled so.
Writes data/cc-031/checks.csv."""
import csv, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-031"
v = {(r["geo"], r["item"], int(r["year"])): float(r["value"]) for r in csv.DictReader(open(D / "eurostat_ghg_pop.csv"))}
ES = "Eurostat env_air_gge, demo_r_pjangrp3, retrieved 6 Oct 2026; MPT estimate via TVM News 4 Jul 2026"
BUS_T = 1300.0   # t CO2 a year, Malta Public Transport's estimate for the electric fleet (TVM News, 4 Jul 2026)
rows = []
def add(check, value, unit, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": ES, "note": note})
for y in (2023, 2024):
    tot, tr, road = (v[("MT", k, y)] * 1000 for k in ("TOTX4_MEMO", "CRF1A3", "CRF1A3B"))  # kt CO2e
    pm, pg = v[("MT", "POP", y)], v[("MT002", "POP", y)]
    sh = pg / pm
    add(f"Gozo and Comino share of Malta's population, 1 Jan {y}", round(100 * sh, 2), "%", f"{pg:.0f} of {pm:.0f}")
    add(f"Malta total GHG {y}", round(tot, 1), "kt CO2e", "excl. LULUCF and international aviation and shipping")
    add(f"Malta road-transport GHG {y}", round(road, 1), "kt CO2e", f"{100*road/tot:.1f}% of the total")
    add(f"Malta fuel combustion in transport {y}", round(tr, 1), "kt CO2e", f"{100*tr/tot:.1f}% of the total")
    add(f"Gozo road transport {y}, population-proportional approximation", round(road * sh, 1), "kt CO2e",
        "NOT Gozo data: Malta road transport x Gozo's population share; no regional inventory exists in Eurostat")
    add(f"Gozo all sectors {y}, population-proportional approximation", round(tot * sh, 1), "kt CO2e", "as above; illustrative scale only")
    add(f"Bus saving (1.3 kt) as share of approximate Gozo road transport {y}", round(100 * (BUS_T / 1000) / (road * sh), 1), "%",
        "operator estimate over proportional approximation: order of magnitude only")
    add(f"Bus saving as share of Malta road transport {y}", round(100 * (BUS_T / 1000) / road, 2), "%")
    add(f"Bus saving as share of Malta total GHG {y}", round(100 * (BUS_T / 1000) / tot, 3), "%")
add("Road transport share of Malta total GHG, 2005", round(100 * v[("MT", "CRF1A3B", 2005)] / v[("MT", "TOTX4_MEMO", 2005)], 1), "%")
add("Malta road-transport GHG change 2005-2024", round(100 * (v[("MT", "CRF1A3B", 2024)] / v[("MT", "CRF1A3B", 2005)] - 1), 1), "%")
fl = sorted({(r["dataset"], r["geo"], r["year"], r["flag"]) for r in csv.DictReader(open(D / "eurostat_ghg_pop.csv")) if r["flag"]})
add("Eurostat status flags on the values used", "; ".join(" ".join(x) for x in fl) or "none", "flags")
with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for r in rows: print(f"{r['check'][:84]:84s} {r['value']:>8} {r['unit']}")
