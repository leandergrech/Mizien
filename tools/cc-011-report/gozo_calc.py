#!/usr/bin/env python3
"""CC-011: order-of-magnitude arithmetic for a net-zero Gozo through afforestation.

There is no published greenhouse-gas inventory for Gozo, so emissions are estimated as Gozo's population
times Malta's national per-capita emissions (a range is tested). Sequestration rates come from a
measured semi-arid Aleppo pine afforestation (Grünzweig et al. 2007, Biogeosciences 4:891) and an
optimistic upper bound. Writes data/cc-011/gozo_net_zero_arithmetic.csv.
"""
import csv, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
GOZO_POP = 41253          # Eurostat demo_r_pjanaggr3, MT002 Gozo and Comino, 1 Jan 2025
GOZO_KM2 = 67             # European Commission, Clean energy for EU islands: Malta
PC = {"low": 2.5, "central": 3.81, "high": 5.0}   # t CO2e per person; central = Malta 2024 (data/cc-003/checks.csv)
# Grünzweig et al. 2007: ecosystem C stock 2380 -> 5840 g C/m2 after 35 years
YATIR = (5840 - 2380) / 35 / 100 * 44 / 12   # t CO2 per ha per year
RATES = {"measured semi-arid pine (Yatir)": round(YATIR, 2), "optimistic upper bound": 10.0}

rows = []
for pk, pc in PC.items():
    em = GOZO_POP * pc
    for rk, rate in RATES.items():
        ha = em / rate
        rows.append({"emissions_case": pk, "per_capita_t": pc, "gozo_emissions_t": round(em),
                     "sequestration_case": rk, "t_co2_per_ha_yr": rate, "forest_needed_ha": round(ha),
                     "forest_needed_km2": round(ha / 100, 1), "multiple_of_gozo_area": round(ha / 100 / GOZO_KM2, 1)})
for share in (0.05, 0.10, 0.20):
    ha = GOZO_KM2 * 100 * share
    rows.append({"emissions_case": "central", "per_capita_t": PC["central"],
                 "gozo_emissions_t": round(GOZO_POP * PC["central"]),
                 "sequestration_case": f"afforest {int(share * 100)}% of Gozo at Yatir rate",
                 "t_co2_per_ha_yr": round(YATIR, 2), "forest_needed_ha": round(ha),
                 "forest_needed_km2": round(ha / 100, 1),
                 "multiple_of_gozo_area": f"offsets {100 * ha * YATIR / (GOZO_POP * PC['central']):.1f}% of emissions"})
dst = ROOT / "data" / "cc-011" / "gozo_net_zero_arithmetic.csv"
with open(dst, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for r in rows:
    print(r)
