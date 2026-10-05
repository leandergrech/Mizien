#!/usr/bin/env python3
"""CC-022: test the Energy Ministry's 'lowest electricity burden in the EU' release (6 May 2025) with formulas.

Reads data/cc-022/; writes data/cc-022/checks.csv."""
import csv, pathlib
from collections import defaultdict

D = pathlib.Path(__file__).resolve().parents[2] / "data" / "cc-022"
EU = "AT BE BG CY CZ DE DK EE EL ES FI FR HR HU IE IT LT LU LV MT NL PL PT RO SE SI SK".split()
P = defaultdict(dict)
for r in csv.DictReader(open(D / "eurostat_prices.csv")):
    P[(r["currency"], r["geo"])][r["time"]] = float(r["value"])
POV = defaultdict(dict)
for r in csv.DictReader(open(D / "eurostat_poverty.csv")):
    POV[(r["dataset"], r["geo"])][int(r["time"])] = float(r["value"])
SUB = list(csv.DictReader(open(D / "imf_energy_subsidies.csv")))
rows = []


def add(check, value, unit, source, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": source, "note": note})


def rank(cur, t):
    v = sorted((P[(cur, g)][t], g) for g in EU if t in P[(cur, g)])
    return [g for _, g in v].index("MT") + 1, len(v), v


t = "2024-S2"
r, n, v = rank("PPS", t)
add("Malta rank, PPS price per kWh, 2024-S2 (1 = cheapest)", r, f"of {n}", "Eurostat nrg_pc_204", "claim: lowest")
add("Malta price 2024-S2, PPS per 100 kWh", round(100 * P[("PPS", "MT")][t], 2), "PPS", "Eurostat nrg_pc_204", "claim: 14.33")
for g, c in (("CZ", "41.00"), ("CY", "35.70"), ("DE", "35.23")):
    add(f"{g} price 2024-S2, PPS per 100 kWh", round(100 * P[("PPS", g)][t], 2), "PPS", "Eurostat nrg_pc_204", f"claim: {c}")
r, n, v = rank("EUR", t)
add("Malta rank, nominal EUR price, 2024-S2", r, f"of {n}", "Eurostat nrg_pc_204", "claim: third lowest")
add("Malta nominal price 2024-S2", round(P[("EUR", "MT")][t], 4), "EUR/kWh", "Eurostat nrg_pc_204", "claim: 0.131")
add("Malta vs EU-27 nominal price 2024-S2", round(P[("EUR", "MT")][t] / P[("EUR", "EU27_2020")][t], 2), "ratio",
    "Eurostat nrg_pc_204")
for g in ("MT", "EU27_2020"):
    add(f"{g} nominal price change 2020-S1 -> 2025-S2", round(100 * (P[("EUR", g)]["2025-S2"] / P[("EUR", g)]["2020-S1"] - 1), 1),
        "%", "Eurostat nrg_pc_204")
r25, n25, _ = rank("PPS", "2025-S2")
add("Malta rank, PPS price, 2025-S2 (latest)", r25, f"of {n25}", "Eurostat nrg_pc_204")
tot = 0
for s in SUB:
    eur = float(s["energy_subsidies_pct_gdp"]) / 100 * float(s["gdp_meur"])
    tot += eur
    add(f"Energy subsidies {s['year']}", round(eur), "EUR million", "IMF CR 26/29 x Eurostat GDP",
        f"{s['energy_subsidies_pct_gdp']}% of GDP")
add("Energy subsidies 2022-2025, total", round(tot), "EUR million", "calculated")
# v1.1: Malta's rank in every consumption band (PPS), and its band-DC price history since 2012.
PB = {(r["nrg_cons"], r["geo"], r["time"]): (float(r["value"]), r["flag"])
      for r in csv.DictReader(open(D / "eurostat_prices_bands.csv"))}
BANDS = (("KWH_LT1000", "under 1,000 kWh (DA)"), ("KWH1000-2499", "1,000-2,499 kWh (DB)"),
         ("KWH2500-4999", "2,500-4,999 kWh (DC, standard household)"), ("KWH5000-14999", "5,000-14,999 kWh (DD)"),
         ("KWH_GE15000", "15,000 kWh or more (DE)"), ("TOT_KWH", "all bands (Eurostat average)"))
for t in ("2024-S2", "2025-S2"):
    for b, lab in BANDS:
        v = sorted((PB[(b, g, t)][0], g) for g in EU if (b, g, t) in PB)
        mt, fl = PB[(b, "MT", t)]
        add(f"Malta rank, PPS price, {t}, band {lab}", [g for _, g in v].index("MT") + 1, f"of {len(v)}",
            "Eurostat nrg_pc_204", f"Malta {100 * mt:.2f} PPS/100 kWh" + (f" (flag {fl})" if fl else ""))
H = {r["time"]: (float(r["value"]), r["flag"]) for r in csv.DictReader(open(D / "eurostat_prices_mt_history.csv"))
     if r["geo"] == "MT"}
for t in ("2013-S2", "2014-S1", "2014-S2"):
    add(f"Malta nominal price {t}, band DC", H[t][0], "EUR/kWh", "Eurostat nrg_pc_204")
later = [H[t][0] for t in sorted(H) if t >= "2014-S2"]
add("Malta nominal price range 2014-S2 to 2025-S2, band DC", f"{min(later):.4f} to {max(later):.4f}", "EUR/kWh",
    "Eurostat nrg_pc_204", f"2025-S2 flag {H['2025-S2'][1]}" if H["2025-S2"][1] else "")
for ds, lab in (("ilc_mdes01", "Unable to keep home adequately warm"), ("ilc_mdes07", "Arrears on utility bills")):
    add(f"{lab}, 2025: Malta vs EU-27", f"{POV[(ds, 'MT')][2025]} vs {POV[(ds, 'EU27_2020')][2025]}", "% of people",
        f"Eurostat {ds}")

with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\r\n")
    w.writeheader()
    w.writerows(rows)
for x in rows:
    print(f"{x['check']:60s} {str(x['value']):>14} {x['unit']:12s} {x['note']}")
