#!/usr/bin/env python3
"""CC-119: test the Council's statement on Malta's renewables (draft Council Recommendation, 3 Jul 2026, para. 25).

Reads data/cc-119/eurostat_extract.csv (fetch.py; Eurostat, retrieved 12 Oct 2026) and writes data/cc-119/checks.csv
(every figure in the report) and data/cc-119/ranking_2024_2025.csv. Flags: p provisional, e estimated."""
import csv, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-119"
EU27 = "BE BG CZ DK DE EE IE EL ES FR HR IT CY LV LT LU HU MT NL AT PL PT RO SI SK FI SE".split()
V, F = {}, {}
for r in csv.DictReader(open(D / "eurostat_extract.csv")):
    k = (r["dataset"], r["geo"], r["item"], r["year"])
    V[k] = float(r["value"]); F[k] = r["flag"]
rows = []
ES = "Eurostat (data/cc-119/eurostat_extract.csv, retrieved 12 Oct 2026)"
def add(check, value, unit, note="", source=ES):
    rows.append({"check": check, "value": value, "unit": unit, "source": source, "note": note})
def ren(geo, item, y): return V[("nrg_ind_ren", geo, item, str(y))]
def fl(ds, geo, item, y): return F.get((ds, geo, item, str(y)), "")
def pem(geo, siec, y):   # monthly net generation summed over the year
    ks = [(("nrg_cb_pem", geo, f"{siec}", f"{y}-{m:02d}")) for m in range(1, 13)]
    vals = [V[k] for k in ks if k in V]
    return sum(vals) if len(vals) == 12 else None
def pem_flags(geo, siec, y):
    return sorted({F.get(("nrg_cb_pem", geo, siec, f"{y}-{m:02d}"), "") for m in range(1, 13)} - {""})

# 1. overall share of gross final energy consumption
add("Malta renewables share of gross final energy consumption, 2024", round(ren("MT", "REN", 2024), 2), "%",
    f"nrg_ind_ren REN; flag '{fl('nrg_ind_ren','MT','REN',2024)}'")
add("EU-27 renewables share, 2024", round(ren("EU27_2020", "REN", 2024), 2), "%")
add("Gap, Malta to EU-27, 2024", round(ren("EU27_2020", "REN", 2024) - ren("MT", "REN", 2024), 1), "points")
o = sorted(EU27, key=lambda c: ren(c, "REN", 2024))
add("Malta's rank, lowest first (1 = lowest share of 27), 2024", o.index("MT") + 1, "of 27",
    "lowest five: " + ", ".join(f"{c} {ren(c,'REN',2024):.1f}" for c in o[:5]))
add("Malta renewables share 2025 (Eurostat early estimate)", ren("MT", "REN", 2025), "%", f"flag '{fl('nrg_ind_ren','MT','REN',2025)}' (provisional)")
add("EU-27 renewables share 2025 (early estimate)", ren("EU27_2020", "REN", 2025), "%", "flag p")

# 2. electricity: three ways to read 'the electricity mix'
add("Malta renewable electricity, share of gross electricity consumption (SHARES), 2024", round(ren("MT", "REN_ELC", 2024), 2), "%")
add("Same, 2025 (Eurostat early estimate)", ren("MT", "REN_ELC", 2025), "%", f"flag '{fl('nrg_ind_ren','MT','REN_ELC',2025)}'")
add("EU-27, same indicator, 2024 / 2025", f"{ren('EU27_2020','REN_ELC',2024):.1f} / {ren('EU27_2020','REN_ELC',2025):.1f}", "%", "2025 flag p")
for y in (2024, 2025):
    t, r_, pv, bio, wi, hy = (pem("MT", s, y) for s in ("TOTAL", "RA000", "RA420", "CF_R", "RA300", "RA100"))
    add(f"Malta net electricity generation, {y}: total / renewable", f"{t:.1f} / {r_:.1f}", "GWh",
        f"nrg_cb_pem monthly sums; flags {pem_flags('MT','TOTAL',y)}")
    add(f"Malta renewable share of NET GENERATION, {y}", round(100 * r_ / t, 2), "%",
        "domestic generation only: imports not in the denominator")
    add(f"Malta solar PV share of renewable generation, {y}", round(100 * pv / r_, 1), "%", f"PV {pv:.1f} GWh")
    add(f"Malta combustible renewables (biomass, biogas) share of renewable generation, {y}", round(100 * bio / r_, 1), "%",
        f"{bio:.1f} GWh; flags {pem_flags('MT','CF_R',y)}")
    add(f"Malta wind and hydro in monthly net generation, {y}", f"{wi:.1f} / {hy:.1f}", "GWh",
        f"nrg_cb_pem (rounded to 0.1 GWh); flags {pem_flags('MT','RA300',y)}")
gep = lambda y: V[("nrg_cb_e", "MT", "GEP|E7000", str(y))] if ("nrg_cb_e", "MT", "GEP|E7000", str(y)) in V else None
for y in (2024, 2025):
    g, im, ex, fc = (V[("nrg_cb_e", "MT", f"{n}|E7000", str(y))] for n in ("GEP", "IMP", "EXP", "FC"))
    add(f"Malta electricity supply {y}: production / imports / exports / final consumption", f"{g:.0f} / {im:.0f} / {ex:.0f} / {fc:.0f}", "GWh",
        f"nrg_cb_e; flag '{F.get(('nrg_cb_e','MT',f'GEP|E7000',str(y)),'')}'; imports = {100*im/fc:.1f}% of final consumption")
    r_ = pem("MT", "RA000", y)
    add(f"Malta renewable generation as share of final consumption (imports in denominator, no SHARES adjustments), {y}",
        round(100 * r_ / fc, 1), "%", "simple ratio; SHARES applies its own definitions (e.g. gross consumption, statistical adjustments)")
# EU-27 on the same generation basis
for y in (2024, 2025):
    t, r_ = pem("EU27_2020", "TOTAL", y), pem("EU27_2020", "RA000", y)
    add(f"EU-27 renewable share of net generation, {y}", round(100 * r_ / t, 1), "%", f"{r_/1000:.0f} of {t/1000:.0f} TWh")
sh = {}
for c in EU27:
    t, r_ = pem(c, "TOTAL", 2025), pem(c, "RA000", 2025)
    sh[c] = None if not t or r_ is None else 100 * r_ / t
ok = [c for c in EU27 if sh[c] is not None]
oo = sorted(ok, key=lambda c: sh[c])
add("Renewable share of net generation, 2025: Malta's rank, lowest first", f"{oo.index('MT')+1} of {len(ok)}", "",
    "lowest five: " + ", ".join(f"{c} {sh[c]:.1f}" for c in oo[:5]) + (f"; missing: {sorted(set(EU27)-set(ok))}" if len(ok) < 27 else ""))
with open(D / "ranking_2024_2025.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["geo", "ren_share_gross_final_energy_2024_pc", "ren_elc_share_shares_2024_pc",
                                    "ren_share_net_generation_2025_pc"])
    for c in EU27:
        w.writerow([c, round(ren(c, "REN", 2024), 2), round(ren(c, "REN_ELC", 2024), 2), "" if sh[c] is None else round(sh[c], 2)])

# 3. generation by source, annual, 2013-2024 (nrg_bal_peh)
peh = lambda s, y: V.get(("nrg_bal_peh", "MT", f"GEP|{s}", str(y)))
for y in (2013, 2018, 2022, 2023, 2024):
    add(f"Malta electricity generation by source, {y}: wind / hydro / PV / biogas / total renewable", " / ".join(
        "n/a" if peh(s, y) is None else f"{peh(s, y):.3f}" for s in ("RA300", "RA100", "RA420", "R5300", "RA000")), "GWh",
        "nrg_bal_peh (annual, three decimals)")
wind = [(y, peh("RA300", y)) for y in range(2013, 2025) if peh("RA300", y)]
add("Years 2013-2024 with any wind generation recorded (nrg_bal_peh)", "; ".join(f"{y}: {v:.3f} GWh" for y, v in wind) or "none", "GWh",
    f"largest = {max(v for _, v in wind)/peh('TOTAL', 2024)*100:.4f}% of 2024 total generation" if wind else "")
add("Years with any hydro generation recorded", "; ".join(f"{y}: {peh('RA100', y)}" for y in range(2013, 2025) if peh("RA100", y)) or "none", "GWh")
add("Wind 2024 as % of renewable generation", round(100 * peh("RA300", 2024) / peh("RA000", 2024), 3), "%",
    f"{peh('RA300', 2024):.3f} GWh of {peh('RA000', 2024):.1f} GWh")
with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, ["check", "value", "unit", "source", "note"]); w.writeheader(); w.writerows(rows)
for r in rows: print(r["check"], "|", r["value"], r["unit"], "|", r["note"])
