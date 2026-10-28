#!/usr/bin/env python3
"""CC-137: test the measurable parts of the Malta Chamber's statement of 21 Jul 2026.
Inputs (data/cc-137/, copied from data/cc-135/, same sources and retrieval dates): nso_max_demand.csv,
eurostat_pop_tourism_electricity.csv, ghcnd_luqa_monthly.csv. Output: data/cc-137/checks.csv"""
import csv, pathlib
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-137"
S_NSO = "NSO Electricity Supply releases (nso_max_demand.csv)"
S_EU = "Eurostat demo_gind / tour_occ_nim / nrg_cb_e (eurostat_pop_tourism_electricity.csv)"
S_GH = "NOAA GHCN-Daily MT000016597 Luqa (ghcnd_luqa_monthly.csv)"
nso = list(csv.DictReader(open(D / "nso_max_demand.csv", encoding="utf-8")))
eu = list(csv.DictReader(open(D / "eurostat_pop_tourism_electricity.csv", encoding="utf-8")))
gh = {r["month"]: r for r in csv.DictReader(open(D / "ghcnd_luqa_monthly.csv", encoding="utf-8"))}
E = {(r["dataset"], r["item"], r["period"]): float(r["value"]) for r in eu}
peak = {}
for r in nso:
    if r["month"] != "AVG":
        peak[int(r["year"])] = max(peak.get(int(r["year"]), 0), int(r["max_demand_mw"]))
nights = lambda ym: E[("tour_occ_nim", "NIGHTS_I551-I553_TOTAL", ym)]
pm = lambda y: max(["%d-%02d" % (y, m) for m in range(1, 13) if ("tour_occ_nim", "NIGHTS_I551-I553_TOTAL", "%d-%02d" % (y, m)) in E], key=nights)
present = lambda y: E[("demo_gind", "AVG", str(y))] + nights(pm(y)) / 31
pct = lambda a, b: (b / a - 1) * 100
out = []
def add(cid, desc, val, unit, src, note=""):
    out.append([cid + " " + desc, ("%.3f" % val) if isinstance(val, float) else val, unit, src, note])

# A. was a rise in peak demand foreseeable from the trend?
for y in sorted(peak):
    add("A-%d" % y, "Annual peak demand", peak[y], "MW", S_NSO)
add("A1", "Peak demand growth 2018-2023", pct(peak[2018], peak[2023]), "%", S_NSO, "465 to 663 MW")
add("A2", "Residents plus peak-month tourists, growth 2018-2023", pct(present(2018), present(2023)), "%", S_EU, "tourists = peak-month nights / 31")
add("A3", "Residents alone (annual average), growth 2018-2023", pct(E[("demo_gind", "AVG", "2018")], E[("demo_gind", "AVG", "2023")]), "%", S_EU)
add("A4", "Final electricity consumption growth 2018-2023", pct(E[("nrg_cb_e", "FC", "2018")], E[("nrg_cb_e", "FC", "2023")]), "%", S_EU)
ys = np.arange(2017, 2023); pk = np.array([peak[y] for y in ys], float)
b1, b0 = np.polyfit(ys, pk, 1)
add("A5", "Linear trend in annual peak 2017-2022 (data available before the 2023 peak)", float(b1), "MW per year", S_NSO)
for y in (2023, 2025):
    f = b0 + b1 * y
    add("A6-%d" % y, "Trend 2017-2022 extrapolated to %d" % y, float(f), "MW", S_NSO, "actual %d MW (%+.1f%%)" % (peak[y], pct(f, peak[y])))
ys2 = np.arange(2017, 2026); c1, c0 = np.polyfit(ys2, [peak[y] for y in ys2], 1)
add("A7", "Linear trend in annual peak 2017-2025", float(c1), "MW per year", S_NSO)
add("A8", "Years with a higher peak than the year before, 2018-2025", sum(peak[y] > peak[y - 1] for y in range(2018, 2026)), "of 8", S_NSO)
pp = lambda y: peak[y] * 1000 / present(y)
add("A9", "Peak demand per person present 2018", float(pp(2018)), "kW", S_NSO + "; " + S_EU)
add("A10", "Peak demand per person present 2023", float(pp(2023)), "kW", S_NSO + "; " + S_EU)
add("A11", "Change in peak per person present 2018-2023", pct(pp(2018), pp(2023)), "%", S_NSO + "; " + S_EU)
add("A12", "Peak demand growth 2018-2023 explained by people present, if peak per person had stayed at 2018 level", float(peak[2018] * present(2023) / present(2018)), "MW", S_NSO + "; " + S_EU, "counterfactual peak 2023")
add("A13", "Part of the 198 MW rise accounted for by growth in people present", float((peak[2018] * present(2023) / present(2018) - peak[2018]) / (peak[2023] - peak[2018]) * 100), "%", S_NSO + "; " + S_EU)
# B. temperature of the peak years
hot = lambda y: max(float(gh["%d-%02d" % (y, m)]["tavg_mean_c"]) for m in (6, 7, 8, 9) if "%d-%02d" % (y, m) in gh)
for y in (2018, 2023, 2024, 2025):
    add("B-%d" % y, "Hottest-month mean temperature at Luqa", hot(y), "C", S_GH)
with open(D / "checks.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["check", "value", "unit", "source", "note"]); w.writerows(out)
for r in out: print(r[0], r[1], r[2], r[4])
