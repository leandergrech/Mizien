#!/usr/bin/env python3
"""CC-025: test "per capita emissions down over 44% since 2005" and "emissions per unit of GDP down more than 80%".

Reads data/cc-025/eurostat_gdp_ghg_pop.csv (fetch.py; Eurostat env_air_gge, nama_10_gdp, nama_10_pe, retrieved
5 Oct 2026) and writes data/cc-025/checks.csv. The per-capita result is cross-checked with CC-003's series.
"""
import csv, math, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-025"
v = {}
flags = {}
for r in csv.DictReader(open(D / "eurostat_gdp_ghg_pop.csv")):
    k = (r["dataset"], r["geo"], r["item"], r["unit"], int(r["year"]))
    v[k] = float(r["value"])
    if r["flag"]:
        flags[k] = r["flag"]
ES = "Eurostat env_air_gge, nama_10_gdp, nama_10_pe, retrieved 5 Oct 2026"
rows = []


def add(check, value, unit, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": ES, "note": note})


def ser(g):
    e = {y: v[("env_air_gge", g, "TOTX4_MEMO", "MIO_T", y)] for y in range(2005, 2025)}
    p = {y: v[("nama_10_pe", g, "POP_NC", "THS_PER", y)] for y in range(2005, 2026)}
    r = {y: v[("nama_10_gdp", g, "B1GQ", "CLV20_MEUR", y)] for y in range(2005, 2026)}
    n = {y: v[("nama_10_gdp", g, "B1GQ", "CP_MEUR", y)] for y in range(2005, 2026)}
    return e, p, r, n


pc = lambda a, b: round(100 * (a / b - 1), 1)
for g, lab in (("MT", "Malta"), ("EU27_2020", "EU-27")):
    e, p, r, n = ser(g)
    for y in (2023, 2024):
        add(f"{lab}: per-person GHG change 2005-{y}", pc(e[y] / p[y], e[2005] / p[2005]), "%",
            f"{e[2005]/p[2005]*1000:.2f} t -> {e[y]/p[y]*1000:.2f} t per person; total excl. LULUCF and international transport")
        add(f"{lab}: GHG per unit of GDP, chain-linked volumes (2020 prices), change 2005-{y}",
            pc(e[y] / r[y], e[2005] / r[2005]), "%", f"{e[2005]/r[2005]*1000:.3f} -> {e[y]/r[y]*1000:.3f} kt CO2e per MEUR")
        add(f"{lab}: GHG per unit of GDP, current prices, change 2005-{y}",
            pc(e[y] / n[y], e[2005] / n[2005]), "%", f"{e[2005]/n[2005]*1000:.3f} -> {e[y]/n[y]*1000:.3f} kt CO2e per MEUR")
        add(f"{lab}: total GHG change 2005-{y}", pc(e[y], e[2005]), "%", f"{e[2005]:.3f} -> {e[y]:.3f} Mt CO2e")
        add(f"{lab}: real GDP change 2005-{y}", pc(r[y], r[2005]), "%", "chain-linked volumes, 2020 prices")
        add(f"{lab}: nominal GDP change 2005-{y}", pc(n[y], n[2005]), "%", "current prices")
        add(f"{lab}: implied GDP price change 2005-{y}", pc(n[y] / r[y], n[2005] / r[2005]), "%",
            "nominal / real GDP: price effect that separates the two intensity measures")
    add(f"{lab}: population change 2005-2024", pc(p[2024], p[2005]), "%", f"{p[2005]:.1f} -> {p[2024]:.1f} thousand")
    # latest year in which emissions fall below the claimed thresholds
    add(f"{lab}: GHG intensity (volumes) average annual change 2005-2024",
        round(100 * ((e[2024] / r[2024]) / (e[2005] / r[2005])) ** (1 / 19) - 100, 2), "%/yr")
e, p, r, n = ser("MT")
yrs_real = [y for y in range(2005, 2025) if 100 * (e[y] / r[y]) / (e[2005] / r[2005]) <= 20]
yrs_nom = [y for y in range(2005, 2025) if 100 * (e[y] / n[y]) / (e[2005] / n[2005]) <= 20]
add("Malta: first year with intensity at least 80% below 2005, volumes", min(yrs_real) if yrs_real else "none", "year",
    "no year to 2024 reaches -80% in volumes" if not yrs_real else "")
add("Malta: first year with intensity at least 80% below 2005, current prices", min(yrs_nom) if yrs_nom else "none", "year")
add("Malta: first year with per-person emissions at least 44% below 2005",
    min(y for y in range(2005, 2025) if (e[y] / p[y]) / (e[2005] / p[2005]) <= 0.56), "year")
add("Malta: total GHG change 2016 (low) to 2024", pc(e[2024], e[2016]), "%", f"{e[2016]:.3f} -> {e[2024]:.3f} Mt CO2e")
# flags
fl = sorted({(k[0], k[1], k[4], f) for k, f in flags.items() if k[1] == "MT" and k[3] != "PCH_PRE_PER"})
add("Eurostat status flags on the Malta values used", "; ".join(f"{a} {c}:{f}" for a, b, c, f in fl) or "none", "flags")
# cross-check against CC-003's saved series
c3 = {(r_["geo"], r_["item"], int(r_["year"])): float(r_["value"]) for r_ in
      csv.DictReader(open(ROOT / "data/cc-003/eurostat_ghg_population.csv"))}
add("Cross-check: Malta total GHG 2024, CC-003 file (2 Oct) vs this file (5 Oct)",
    f"{c3[('MT','TOTX4_MEMO',2024)]:.5f} vs {e[2024]:.5f}", "Mt CO2e", "same inventory vintage")
# decomposition of the intensity fall into price and volume parts (log shares)
lt = math.log((e[2024] / n[2024]) / (e[2005] / n[2005]))
lr = math.log((e[2024] / r[2024]) / (e[2005] / r[2005]))
add("Malta: share of the current-price intensity fall (2005-2024) due to price change", round(100 * (1 - lr / lt)), "%",
    "log decomposition: ln(nominal intensity ratio) = ln(real intensity ratio) - ln(GDP price ratio)")
with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
for r_ in rows:
    print(f"{r_['check'][:88]:88s} {r_['value']:>10} {r_['unit']}")
