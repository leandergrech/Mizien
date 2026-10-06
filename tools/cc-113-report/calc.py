#!/usr/bin/env python3
"""CC-113: test the EEA statement that in 2023 fossil fuel subsidies were the highest shares of GDP in Malta, Poland
and Slovakia (all at or above 1.5%).

Reads data/cc-113/ (written by fetch.py and measure_fig16.py on 6 Oct 2026, plus other_estimates_transcribed.csv) and
writes data/cc-113/checks.csv and data/cc-113/shares_2023_variants.csv.

The EEA figure uses the European Commission's subsidy inventory (2024 edition). Its 2023 values are provisional: for
measures marked "TBC" (to be confirmed) with no 2023 value, the 2022 value is used as a stand-in (EEA figure note).
We recompute the share of GDP four ways: with the stand-ins (A, B) or with unconfirmed measures set to zero (C, D: a
lower bound), and with the GDP series the inventory used (Enerdata, from IMF and World Bank data) or with Eurostat's
GDP as published on 6 Oct 2026 (nama_10_gdp, current prices), which the EEA could not have had in January 2025.

The workbook's measure rows are Enerdata copyright and are not committed. Country totals come from the workbook's own
pivot (data/cc-113/ec_inventory_ffs_by_country.csv). If fetch.py has written the local measure file
(tools/cc-113-report/out/ec_inventory_measures.csv), calc.py also rebuilds the totals from it as a check.
"""
import csv, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-113"
LOCAL = pathlib.Path(__file__).resolve().parent / "out" / "ec_inventory_measures.csv"
EU27 = "AT BE BG HR CY CZ DK EE FI FR DE EL HU IE IT LV LT LU MT NL PL PT RO SK SI ES SE".split()
S_INV = "EC subsidy inventory 2024 ed. (CIRCABC), retrieved 6 Oct 2026"
S_EEA = "EEA chart data, retrieved 6 Oct 2026"
S_EST = "Eurostat nama_10_gdp (CP_MEUR), updated {}, retrieved 6 Oct 2026"
rows = []


def add(check, value, unit, source, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": source, "note": note})


def rd(name):
    return list(csv.DictReader(open(D / name)))


# ---------------------------------------------------------------- inputs
piv = {(r["geo"], r["column"]): float(r["ffs_eur_million"]) for r in rd("ec_inventory_ffs_by_country.csv")}
ffs23 = {g: piv[(g, "2023")] for g in EU27}
ffs23_tbc = {g: piv[(g, "2023 incl. TBC")] for g in EU27}
ffs22 = {g: piv[(g, "2022")] for g in EU27}
share_piv = {(r["geo"], int(r["year"])): float(r["ffs_share_of_gdp"]) for r in rd("ec_inventory_ffs_share_gdp.csv")}
gdp_inv = {(r["geo"], int(r["year"])): float(r["gdp_eur_million"]) for r in rd("ec_inventory_gdp.csv")}
facts = {r["item"]: r for r in rd("ec_inventory_malta_facts.csv")}
est = rd("eurostat_nama_10_gdp.csv")
gdp_est = {(r["geo"].replace("EU27_2020", "EU27"), int(r["time"])): float(r["value"]) for r in est}
gdp_flag = {(r["geo"].replace("EU27_2020", "EU27"), int(r["time"])): r["flag"] for r in est}
est_upd = est[0]["updated"][:10]
eea_share = {r["geo"]: float(r["ffs_share_of_gdp_pct"]) for r in rd("eea_share_of_gdp_2023.csv")}
eea_fig2 = {(r["geo"], int(r["year"])): float(r["value"]) for r in rd("eea_fig2_ffs_by_country.csv")}
fig16 = {r["geo"]: float(r["ffs_share_of_gdp_pct_measured"]) for r in rd("com2025_17_fig16_measured.csv")
         if r["reliable"] == "yes"}      # bars above 0.8%; lower bars are crossed by the EU-27 line and 2015 markers
mt_trend = {int(r["year"]): float(r["ffs_share_of_gdp_pct"]) for r in rd("eea_malta_trend_soer2025.csv")
            if r["series"] == "Historical trend Malta"}

# ---------------------------------------------------------------- 1. totals: pivot, local rebuild, EEA figure
if LOCAL.exists():
    r23, r23t = {g: 0.0 for g in EU27}, {g: 0.0 for g in EU27}
    for r in csv.DictReader(open(LOCAL)):
        v23, v22 = float(r["y2023"] or 0), float(r["y2022"] or 0)
        r23[r["geo"]] += v23
        r23t[r["geo"]] += v22 if (r["tbc"] == "Yes" and v23 == 0) else v23      # the EEA's 2022 stand-in rule
    add("Rebuilt from local measure rows vs the inventory's pivot, 2023 incl. TBC: largest difference",
        round(max(abs(r23t[g] - ffs23_tbc[g]) for g in EU27), 2), "EUR million", S_INV,
        "measure rows (Enerdata copyright) kept locally, not committed; techno group 'Fossil fuels', no double counting")
    add("Rebuilt from local measure rows vs pivot, 2023 excl. TBC: largest difference",
        round(max(abs(r23[g] - ffs23[g]) for g in EU27), 2), "EUR million", S_INV)
else:
    add("Rebuild from measure rows", "skipped", "", "", "run fetch.py to write the local measure file")
add("Inventory 2023 incl. TBC vs EEA Figure 2 (2023): largest difference",
    round(max(abs(ffs23_tbc[g] / 1000 - eea_fig2[(g, 2023)]) for g in EU27), 4), "EUR billion",
    S_INV + "; " + S_EEA, "the EEA figure is the inventory including the 2022 stand-ins")
eu_tot = sum(ffs23_tbc[g] for g in EU27)
add("EU-27 FFS 2023 incl. TBC (sum of countries)", round(eu_tot / 1000, 1), "EUR billion (2023 prices)", S_INV,
    "EEA text: EUR 111 billion")
add("EU-27 FFS 2023 excl. TBC", round(sum(ffs23[g] for g in EU27) / 1000, 1), "EUR billion (2023 prices)", S_INV)
add("Share of EU-27 2023 total that is TBC stand-in", round(100 * (1 - sum(ffs23[g] for g in EU27) / eu_tot), 1), "%",
    "calculated", "EEA figure note: 'about 7% of total'; COM(2025) 17 footnote 6: 8% 'To be confirmed'")
absr = sorted(EU27, key=lambda g: -ffs23_tbc[g])
add("Malta's rank by absolute amount, 2023 incl. TBC", f"{absr.index('MT') + 1} of 27 (EUR {ffs23_tbc['MT'] / 1000:.2f}bn)",
    "rank", S_INV, f"largest: DE EUR {ffs23_tbc['DE'] / 1000:.1f}bn; smaller than Malta: "
    + ", ".join(g for g in absr[absr.index('MT') + 1:]))

# ---------------------------------------------------------------- 2. shares of GDP, four variants
variants = {
    "A: EEA basis (with 2022 stand-ins; inventory GDP)": (ffs23_tbc, lambda g: gdp_inv[(g, 2023)]),
    "B: with stand-ins; Eurostat GDP as of 6 Oct 2026": (ffs23_tbc, lambda g: gdp_est[(g, 2023)]),
    "C: lower bound (unconfirmed set to zero); inventory GDP": (ffs23, lambda g: gdp_inv[(g, 2023)]),
    "D: lower bound (unconfirmed set to zero); Eurostat GDP as of 6 Oct 2026": (ffs23, lambda g: gdp_est[(g, 2023)]),
}
var_rows = []
for vname, (num, den) in variants.items():
    sh = {g: 100 * num[g] / den(g) for g in EU27}
    order = sorted(EU27, key=lambda g: -sh[g])
    for i, g in enumerate(order, 1):
        var_rows.append({"variant": vname, "rank": i, "geo": g, "ffs_eur_million": round(num[g], 3),
                         "gdp_eur_million": round(den(g), 1), "share_of_gdp_pct": round(sh[g], 3),
                         "gdp_flag": gdp_flag.get((g, 2023), "") if "Eurostat" in vname else ""})
    add(f"{vname}: top three", ", ".join(f"{g} {sh[g]:.2f}%" for g in order[:3]), "% of GDP",
        S_INV + ("; " + S_EST.format(est_upd) if "Eurostat" in vname else ""))
    add(f"{vname}: fourth", f"{order[3]} {sh[order[3]]:.2f}%", "% of GDP", "calculated")
    add(f"{vname}: countries at or above 1.5%", ", ".join(g for g in order if round(sh[g], 2) >= 1.5) or "none",
        "list", "calculated", "share rounded to two decimals, as the EEA chart prints it")
    add(f"{vname}: Malta rank", order.index("MT") + 1, "of 27", "calculated")
    add(f"{vname}: Slovakia share", round(sh["SK"], 3), "% of GDP", "calculated")
    eu_den = gdp_inv[("EU27", 2023)] if "inventory" in vname else gdp_est[("EU27", 2023)]
    add(f"{vname}: EU-27 total / EU GDP", round(100 * sum(num[g] for g in EU27) / eu_den, 3), "% of GDP",
        "calculated", "aggregate ratio, not an average of country shares")
with open(D / "shares_2023_variants.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(var_rows[0]))
    w.writeheader()
    w.writerows(var_rows)

shA = {g: 100 * ffs23_tbc[g] / gdp_inv[(g, 2023)] for g in EU27}
add("EEA printed share vs variant A: largest difference across 27 countries",
    round(max(abs(round(shA[g], 2) - eea_share[g]) for g in EU27), 3), "percentage points", S_EEA + "; calculated",
    "0 means every printed value is reproduced to two decimals")
add("COM(2025) 17 Figure 16 (28 Jan 2025), measured: MT / PL / SK / HR / BG",
    " / ".join(f"{fig16[g]:.3f}" for g in ("MT", "PL", "SK", "HR", "BG")), "% of GDP",
    "COM(2025) 17 via Cellar, pixel measurement (measure_fig16.py)",
    "variant A: " + " / ".join(f"{shA[g]:.3f}" for g in ("MT", "PL", "SK", "HR", "BG")))
add("Largest difference, Figure 16 (measured) vs variant A, top five",
    round(max(abs(fig16[g] - shA[g]) for g in ("MT", "PL", "SK", "HR", "BG")), 3), "percentage points", "calculated",
    "for the top five the CIRCABC file (modified 9 Apr 2025) gives the same values as the report of 28 Jan 2025")
add(f"Largest difference, Figure 16 (measured) vs variant A, the {len([g for g in fig16 if g in EU27])} bars above 0.8%",
    round(max(abs(fig16[g] - shA[g]) for g in fig16 if g in EU27), 3), "percentage points", "calculated",
    "pixel measurement, about +/-0.01 pp; lower bars are hidden by the EU-27 line and 2015 markers, not used")
add("EEA printed: Malta / Poland / Slovakia / EU-27", f"{eea_share['MT']} / {eea_share['PL']} / {eea_share['SK']} / "
    f"{eea_share['EU27']}", "% of GDP", S_EEA, "EU-27 = EU total over EU GDP")
add("EEA lowest three (printed)", ", ".join(f"{g} {eea_share[g]}%" for g in sorted(EU27, key=lambda g: eea_share[g])[:3]),
    "% of GDP", S_EEA, "EEA text: Austria, Denmark and Estonia below 0.2%")
add("Inventory GDP vs Eurostat GDP, Malta 2023", f"{gdp_inv[('MT', 2023)]:.1f} vs {gdp_est[('MT', 2023)]:.1f}",
    "EUR million", S_INV + "; " + S_EST.format(est_upd),
    f"Eurostat {100 * (gdp_est[('MT', 2023)] / gdp_inv[('MT', 2023)] - 1):.1f}% higher; Eurostat flag "
    f"'{gdp_flag[('MT', 2023)] or 'none'}'")
add("Inventory GDP vs Eurostat GDP, Slovakia 2023", f"{gdp_inv[('SK', 2023)]:.1f} vs {gdp_est[('SK', 2023)]:.1f}",
    "EUR million", S_INV + "; " + S_EST.format(est_upd),
    f"Eurostat {100 * (gdp_est[('SK', 2023)] / gdp_inv[('SK', 2023)] - 1):.1f}% higher")
add("Slovakia: TBC stand-in amount in 2023", round(ffs23_tbc["SK"] - ffs23["SK"], 1), "EUR million", S_INV)
hr = sorted(EU27, key=lambda g: -shA[g])[3]
add(f"Malta's 2023 amount that would put it below the fourth country ({hr}, {shA[hr]:.2f}%) on the EEA basis",
    round(shA[hr] / 100 * gdp_inv[("MT", 2023)], 1), "EUR million", "calculated",
    "to fall out of the top three on the EEA's basis Malta's 2023 amount would have to be under this, "
    "below even the IMF-based EUR 293m (1.4% of Eurostat GDP)")

# ---------------------------------------------------------------- 3. what Malta's figure is made of
for item, r in facts.items():
    add(f"Malta FFS item: {item}", f"{float(r['y2022']):.2f} (2022) / {float(r['y2023']):.2f} (2023)",
        "EUR million (2023 prices)", S_INV + " (aggregated)",
        f"{r['classification']}; cost basis: {r['cost_basis']}; to be confirmed: {r['to_be_confirmed']}")
line = facts["Energy Support Measures (compensation to Enemalta)"]
L22, L23 = float(line["y2022"]), float(line["y2023"])
add("Malta: 'Energy Support Measures' share of 2023 FFS (excl. TBC)", round(100 * L23 / ffs23["MT"], 1), "%",
    "calculated")
add("Malta: the Energy Support Measures line alone, share of GDP 2023 (inventory GDP)",
    round(100 * L23 / gdp_inv[("MT", 2023)], 2), "% of GDP", "calculated", "the total incl. stand-in is 3.37%")
crisis = sum(float(r["y2023"]) for i, r in facts.items() if "created for the price crisis" in r["classification"])
add("Malta: crisis-related share of 2023 FFS (excl. TBC)", round(100 * crisis / ffs23["MT"], 1), "%", "calculated",
    "items flagged 'Created or modified to address energy price rising'")
add("Malta: TBC stand-in in 2023 (excise cut on petrol and diesel, 2022 value)", round(ffs23_tbc["MT"] - ffs23["MT"], 2),
    "EUR million", S_INV)
for y in range(2015, 2024):
    order = sorted(EU27, key=lambda g: -share_piv[(g, y)])
    add(f"Malta FFS share of GDP and rank, {y} (inventory pivot, excl. TBC)",
        f"{100 * share_piv[('MT', y)]:.2f}% (rank {order.index('MT') + 1} of 27)", "% of GDP", S_INV,
        f"first: {order[0]}")
add("Malta 2023 FFS vs 2022 (inventory, excl. TBC)", round(100 * (ffs23["MT"] / ffs22["MT"] - 1), 1), "% change",
    "calculated", f"{ffs22['MT']:.1f} -> {ffs23['MT']:.1f} EUR million")
add("EEA Malta country chart (Europe's environment 2025): 2015, 2020, 2021, 2022, 2023",
    " / ".join(f"{mt_trend[y]:.2f}" for y in (2015, 2020, 2021, 2022, 2023)), "% of GDP",
    "EEA, retrieved 6 Oct 2026", "same values as the inventory pivot (2023 incl. TBC)")
falls = [g for g in EU27 if ffs23_tbc[g] < ffs22[g]]
add("Member States whose FFS fell 2022 to 2023 (incl. TBC)", len(falls), "of 27", "calculated",
    "EEA text: 'declined in 20 EU Member States' (not part of the claim); Malta " + ("fell" if "MT" in falls else "rose"))

# electricity imports: Malta's main line is booked wholly to natural gas
nrg = {r["nrg_bal"]: float(r["value"]) for r in rd("eurostat_nrg_cb_e_mt_2023.csv")}
imp_sh = nrg["IMP"] / (nrg["GEP"] + nrg["IMP"])
add("Malta 2023: electricity imports / (gross production + imports)", round(100 * imp_sh, 1), "%",
    "Eurostat nrg_cb_e, retrieved 6 Oct 2026", f"{nrg['IMP']:.1f} of {nrg['GEP'] + nrg['IMP']:.1f} GWh")
adj = ffs23_tbc["MT"] - imp_sh * L23
shm = dict(shA)
shm["MT"] = 100 * adj / gdp_inv[("MT", 2023)]
add("Sensitivity: Malta's 2023 share (EEA basis) if the import share of the Enemalta line were not counted",
    f"{shm['MT']:.2f}% (rank {sorted(EU27, key=lambda g: -shm[g]).index('MT') + 1} of 27)", "% of GDP", "calculated",
    "imports are not all non-fossil; a bound on the pro-rating question, not an estimate")

# ---------------------------------------------------------------- 4. other measures of Malta's support
gov = {(r["unit"], int(r["time"])): float(r["value"]) for r in rd("eurostat_gov_10a_main_mt_subsidies.csv")}
for y in (2019, 2021, 2022, 2023, 2024):
    add(f"Malta general government subsidies (all purposes, D.3), {y}", f"{gov[('MIO_EUR', y)]:.1f} "
        f"({gov[('PC_GDP', y)]}% of GDP)", "EUR million", "Eurostat gov_10a_main, retrieved 6 Oct 2026")
oth = {(r["measure"], int(r["year"])): float(r["value"]) for r in rd("other_estimates_transcribed.csv")}
GOV, IMF = "Energy support measures (Government of Malta)", "Energy subsidies (IMF Article IV)"
eur = {(n, y): oth[(n, y)] / 100 * gdp_est[("MT", y)] for n in (GOV, IMF) for y in (2022, 2023)}
for (n, y), v in eur.items():
    add(f"{n}, {y}, in EUR with Eurostat GDP", round(v, 1), "EUR million", "transcribed % of GDP x Eurostat GDP",
        f"{oth[(n, y)]}% of GDP")
add("Inventory Enemalta line 2022 vs Government and IMF 2022", f"{L22:.1f} vs {eur[(GOV, 2022)]:.1f} vs {eur[(IMF, 2022)]:.1f}",
    "EUR million", "calculated", "the database is lower in 2022")
add("Two-year total 2022-23: inventory Enemalta line / Government / IMF",
    f"{L22 + L23:.1f} / {eur[(GOV, 2022)] + eur[(GOV, 2023)]:.1f} / {eur[(IMF, 2022)] + eur[(IMF, 2023)]:.1f}",
    "EUR million", "calculated", "inventory 2022 in 2023 prices; budget figures nominal; points to timing or basis")
add("Inventory Malta FFS 2022 share (excl. TBC, inventory GDP)", round(100 * share_piv[("MT", 2022)], 2), "% of GDP",
    S_INV, "Government 2.5%, IMF 1.8%")
for name, pct in (("IMF Article IV", oth[(IMF, 2023)]), ("Government of Malta DBP 2024", oth[(GOV, 2023)])):
    shm = dict(shA)
    shm["MT"] = pct
    order = sorted(EU27, key=lambda g: -shm[g])
    add(f"Sensitivity: Malta's rank if its 2023 share were the {name} figure ({pct}%), others on the EEA basis",
        order.index("MT") + 1, "of 27", "calculated", "mixes definitions; a robustness check, not a like-for-like figure")
add("Inventory Malta FFS 2023 (excl. TBC) / IMF Article IV energy subsidies 2023 (EUR, Eurostat GDP)",
    round(ffs23["MT"] / eur[(IMF, 2023)], 2), "x", "calculated", "inventory in 2023 prices = nominal for 2023")
add("Inventory Malta FFS 2023 (excl. TBC) / Government DBP energy support 2023 (EUR, Eurostat GDP)",
    round(ffs23["MT"] / eur[(GOV, 2023)], 2), "x", "calculated", "the Government's figure includes other basic commodities")

imf = rd("imf_ffs_eu27.csv")
ex = {(r["geo"], int(r["year"])): float(r["pct_of_gdp"]) for r in imf
      if r["indicator"] == "Explicit Fossil Fuel Subsidies - Total"}
tot = {(r["geo"], int(r["year"])): float(r["pct_of_gdp"]) for r in imf
       if r["indicator"] == "Fossil Fuel Subsidies - Total Implicit and Explicit"}
add("IMF FFS data (2023 update): Malta explicit subsidies, 2015-2025",
    "zero in every year" if all(ex[("MT", y)] == 0 for y in range(2015, 2026)) else "non-zero", "% of GDP",
    "IMF climate data dashboard, retrieved 6 Oct 2026", "values for 2023 onwards estimated in Aug 2023")
for y in (2022, 2023):
    order = sorted(EU27, key=lambda g: -ex[(g, y)])
    add(f"IMF explicit FFS {y}: top three EU", ", ".join(f"{g} {ex[(g, y)]:.2f}%" for g in order[:3]), "% of GDP",
        "IMF climate data dashboard", f"{sum(1 for g in EU27 if ex[(g, y)] == 0)} of 27 at zero, Malta among them")
    order = sorted(EU27, key=lambda g: -tot[(g, y)])
    add(f"IMF explicit + implicit FFS {y}: Malta", f"{tot[('MT', y)]:.2f}% (rank {order.index('MT') + 1} of 27)",
        "% of GDP", "IMF climate data dashboard", "implicit = unpriced environmental costs and forgone VAT")
trk = rd("oecd_iisd_tracker_malta.csv")
add("OECD/IISD tracker: data sources for Malta", ", ".join(sorted({r["data_source"] for r in trk})), "list",
    "OECD/IISD Fossil Fuel Subsidy Tracker, retrieved 6 Oct 2026", "no OECD-inventory or IEA rows for Malta")
for y in (2022, 2023, 2024):
    add(f"OECD/IISD tracker: Malta total {y}", round(sum(float(r["usd_million_nominal"] or 0) for r in trk
                                                         if int(r["year"]) == y), 2), "USD million", "tracker")

with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
for r in rows:
    print(f"{r['check'][:96]:96s} {r['value']!s:>34} {r['unit']}  {r['note'][:90]}")
