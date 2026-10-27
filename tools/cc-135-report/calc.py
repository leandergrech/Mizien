"""CC-135 calculations. Run fetch.py first. Inputs in data/cc-135/; writes data/cc-135/checks.csv.
Every figure the report and flyer use is written here."""
import csv, pathlib
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-135"
S_NSO = "NSO Electricity Supply releases (nso_max_demand.csv)"
S_EU = "Eurostat demo_gind / tour_occ_nim / nrg_cb_e (eurostat_pop_tourism_electricity.csv)"
S_GH = "NOAA GHCN-Daily MT000016597 Luqa (ghcnd_luqa_monthly.csv)"
S_IMF = "IMF SIP/2025/007 (imf_statements.csv)"

nso = list(csv.DictReader(open(D / "nso_max_demand.csv", encoding="utf-8")))
eu = list(csv.DictReader(open(D / "eurostat_pop_tourism_electricity.csv", encoding="utf-8")))
gh = list(csv.DictReader(open(D / "ghcnd_luqa_monthly.csv", encoding="utf-8")))

# annual peak = highest monthly maximum reported for the year
peak, avgmax = {}, {}
for r in nso:
    y = int(r["year"]); v = int(r["max_demand_mw"])
    if r["month"] == "AVG":
        avgmax[y] = v
    else:
        peak[y] = max(peak.get(y, 0), v)
E = {(r["dataset"], r["item"], r["period"]): float(r["value"]) for r in eu}
pop_jan = lambda y: E[("demo_gind", "JAN", str(y))]
pop_avg = lambda y: E[("demo_gind", "AVG", str(y))]
nights = lambda ym: E[("tour_occ_nim", "NIGHTS_I551-I553_TOTAL", ym)]
elec = lambda b, y: E.get(("nrg_cb_e", b, str(y)))
T = {r["month"]: r for r in gh}

out = []


def add(cid, desc, val, unit, src, note=""):
    v = ("%.3f" % val) if isinstance(val, float) else val
    out.append([cid + " " + desc, v, unit, src, note])


pct = lambda a, b: (b / a - 1) * 100

# A. the IMF's peak-demand figures
add("A1", "Peak electricity demand 2018 (highest monthly maximum)", peak[2018], "MW", S_NSO, "August 2018; IMF: 465")
add("A2", "Peak electricity demand 2023 (highest monthly maximum)", peak[2023], "MW", S_NSO, "July 2023; IMF: 663")
add("A3", "Increase in peak demand 2018-2023", pct(peak[2018], peak[2023]), "%", S_NSO, "IMF: 43 percent")
for y in sorted(peak):
    add("A-%d" % y, "Annual peak demand %d" % y, peak[y], "MW", S_NSO)

# B. sensitivity of the 43% to the end years
for a, b in ((2017, 2023), (2019, 2023), (2018, 2024), (2018, 2025), (2017, 2025)):
    add("B-%d-%d" % (a, b), "Increase in peak demand %d-%d" % (a, b), pct(peak[a], peak[b]), "%", S_NSO,
        "%d MW to %d MW" % (peak[a], peak[b]))
m1 = np.mean([peak[y] for y in (2017, 2018, 2019)]); m2 = np.mean([peak[y] for y in (2021, 2022, 2023)])
m3 = np.mean([peak[y] for y in (2023, 2024, 2025)])
add("B-3y1", "Mean annual peak 2017-2019", float(m1), "MW", S_NSO)
add("B-3y2", "Mean annual peak 2021-2023", float(m2), "MW", S_NSO)
add("B-3y3", "Mean annual peak 2023-2025", float(m3), "MW", S_NSO)
add("B-3yA", "Increase, three-year means 2017-2019 to 2021-2023", pct(m1, m2), "%", S_NSO)
add("B-3yB", "Increase, three-year means 2017-2019 to 2023-2025", pct(m1, m3), "%", S_NSO)
ys = np.array(sorted(peak)); pk = np.array([peak[y] for y in ys], float)
b1, b0 = np.polyfit(ys, pk, 1)
add("B-trend", "Linear trend in annual peak 2017-2025", float(b1), "MW per year", S_NSO,
    "least squares on 9 annual peaks; fitted 2018 %.0f, fitted 2023 %.0f" % (b0 + b1 * 2018, b0 + b1 * 2023))
add("B-trend5", "Trend rise over five years as % of fitted 2018 value", float(5 * b1 / (b0 + b1 * 2018) * 100), "%", S_NSO)

# C. the 13%: population plus tourists in the peak summer month (IMF note: nights in peak month / 31)
def peak_month(y):
    ms = ["%d-%02d" % (y, m) for m in range(1, 13)]
    return max(ms, key=nights)

for y in (2018, 2023):
    pm = peak_month(y)
    add("C-pm%d" % y, "Peak month for tourist nights %d" % y, pm, "month", S_EU, "%d nights" % nights(pm))
    add("C-tour%d" % y, "Tourists present on an average day of the peak month %d (nights / 31)" % y,
        float(nights(pm) / 31), "persons", S_EU)
tour = {y: nights(peak_month(y)) / 31 for y in (2018, 2023)}
variants = {"JAN same year": (pop_jan(2018), pop_jan(2023)),
            "AVG (annual average)": (pop_avg(2018), pop_avg(2023)),
            "end-year (JAN next year)": (pop_jan(2019), pop_jan(2024))}
for i, (k, (p18, p23)) in enumerate(variants.items(), 1):
    add("C%d" % i, "Population plus tourists 2018-2023, population = %s" % k, pct(p18 + tour[2018], p23 + tour[2023]), "%",
        S_EU, "%.0f to %.0f; IMF: 13 percent" % (p18 + tour[2018], p23 + tour[2023]))
    add("C%dp" % i, "Population alone 2018-2023, %s" % k, pct(p18, p23), "%", S_EU, "%.0f to %.0f" % (p18, p23))
add("C-tour", "Tourists alone (peak-month nights / 31) 2018-2023", pct(tour[2018], tour[2023]), "%", S_EU)
add("C-end23", "Population at end-2023 (1 Jan 2024)", pop_jan(2024), "persons", S_EU, "IMF para. 2: around 563,000 at end-2023")
# the gap the IMF describes
add("C-gap", "Peak demand growth minus population-plus-tourist growth (AVG variant), 2018-2023",
    pct(peak[2018], peak[2023]) - pct(pop_avg(2018) + tour[2018], pop_avg(2023) + tour[2023]), "percentage points", S_NSO + "; " + S_EU)
pp18 = peak[2018] * 1000 / (pop_avg(2018) + tour[2018]); pp23 = peak[2023] * 1000 / (pop_avg(2023) + tour[2023])
add("C-pc18", "Peak demand per person present (residents + tourists), 2018", float(pp18), "kW per person", S_NSO + "; " + S_EU)
add("C-pc23", "Peak demand per person present (residents + tourists), 2023", float(pp23), "kW per person", S_NSO + "; " + S_EU)
add("C-pc", "Change in peak demand per person present 2018-2023", pct(pp18, pp23), "%", S_NSO + "; " + S_EU)
# 2018-2024 and 2018-2025 comparisons (later data than the paper)
for b in (2024, 2025):
    pm = peak_month(b) if ("tour_occ_nim", "NIGHTS_I551-I553_TOTAL", "%d-12" % b) in E else None
    if pm:
        g = pct(pop_avg(2018) + tour[2018], pop_avg(b) + nights(pm) / 31)
        add("C-%d" % b, "Population (AVG) plus tourists 2018-%d" % b, g, "%", S_EU, "peak month %s" % pm)

def present(y):
    return pop_avg(y) + nights(peak_month(y)) / 31
for a, b in ((2017, 2023), (2019, 2023)):
    add("C-%d-%d" % (a, b), "Population (AVG) plus tourists %d-%d" % (a, b), pct(present(a), present(b)), "%", S_EU)

# D. controls: energy and the average of monthly maxima grew with population
add("D1", "Mean of the 12 monthly maxima 2018 (NSO 'annual average demand')", avgmax[2018], "MW", S_NSO)
add("D2", "Mean of the 12 monthly maxima 2023, as first published", avgmax[2023], "MW", S_NSO)
add("D3", "Increase in mean of monthly maxima 2018-2023", pct(avgmax[2018], avgmax[2023]), "%", S_NSO,
    "the 2024 release implies a revised 2023 figure of about %.0f (478 / 1.018)" % (478 / 1.018))
add("D3r", "Increase in mean of monthly maxima 2018-2023 with the implied revised 2023 figure", pct(avgmax[2018], 478 / 1.018), "%", S_NSO)
add("D4", "Final electricity consumption 2018", elec("FC", 2018), "GWh", S_EU)
add("D5", "Final electricity consumption 2023", elec("FC", 2023), "GWh", S_EU)
add("D6", "Increase in final electricity consumption 2018-2023", pct(elec("FC", 2018), elec("FC", 2023)), "%", S_EU)
sup = lambda y: elec("GEP", y) + elec("IMP", y) - elec("EXP", y)
add("D7", "Increase in electricity supply (gross production + imports - exports) 2018-2023", pct(sup(2018), sup(2023)), "%", S_EU,
    "%.0f to %.0f GWh" % (sup(2018), sup(2023)))
lf = lambda y: sup(y) * 1000 / 8760 / peak[y] * 100
add("D8", "Load factor 2018 (average load / annual peak)", float(lf(2018)), "%", S_EU + "; " + S_NSO)
add("D9", "Load factor 2023 (average load / annual peak)", float(lf(2023)), "%", S_EU + "; " + S_NSO)

# E. temperature: hottest-month mean (IMF: 27.3 to 29.6 C) and highest daily maximum (IMF fn 3: 34 to almost 42 C)
hot = {}
for y in range(2017, 2026):
    ms = [k for k in T if k.startswith(str(y)) and T[k]["tavg_mean_c"] and int(T[k]["tavg_days"]) >= 28]
    k = max(ms, key=lambda m: float(T[m]["tavg_mean_c"]))
    hot[y] = (k, float(T[k]["tavg_mean_c"]))
    tx = max(float(T[m]["tmax_highest_c"]) for m in T if m.startswith(str(y)) and T[m]["tmax_highest_c"])
    add("E-%d" % y, "Hottest month mean temperature %d, Luqa" % y, hot[y][1], "deg C", S_GH,
        "%s (%s days); highest daily maximum in the year %.1f C" % (k, T[k]["tavg_days"], tx))
add("E1", "Rise in hottest-month mean temperature 2018-2023, Luqa", hot[2023][1] - hot[2018][1], "deg C", S_GH, "IMF: 27.3 to 29.6 (+2.3)")
coolest = min(hot, key=lambda y: hot[y][1]); hottest = max(hot, key=lambda y: hot[y][1])
add("E2", "Year with the coolest hottest-month in 2017-2025", coolest, "year", S_GH)
add("E3", "Year with the hottest hottest-month in 2017-2025", hottest, "year", S_GH)
tm = np.array([hot[y][1] for y in ys])
r = np.corrcoef(tm, pk)[0, 1]
add("E4", "Correlation of annual peak demand with hottest-month mean temperature, 2017-2025", float(r), "Pearson r", S_NSO + "; " + S_GH, "9 years; descriptive only")
X = np.column_stack([np.ones(len(ys)), ys - 2018, tm])
coef, *_ = np.linalg.lstsq(X, pk, rcond=None)
add("E5", "Fit peak = a + b*(year-2018) + c*temperature: b (trend net of temperature)", float(coef[1]), "MW per year",
    S_NSO + "; " + S_GH, "9 points; descriptive, not a forecast")
add("E6", "Same fit: c (per 1 C of hottest-month mean)", float(coef[2]), "MW per deg C", S_NSO + "; " + S_GH, "9 points; descriptive")
fit18 = coef[0] + coef[1] * 0 + coef[2] * np.mean(tm); fit23 = coef[0] + coef[1] * 5 + coef[2] * np.mean(tm)
add("E7", "Fitted rise 2018-2023 at the 2017-2025 mean temperature", float(pct(fit18, fit23)), "%", S_NSO + "; " + S_GH,
    "trend with temperature held at %.2f C" % np.mean(tm))

with open(D / "checks.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh, lineterminator="\r\n")
    w.writerow(["check", "value", "unit", "source", "note"]); w.writerows(out)
for o in out:
    print(o[0][:95], "|", o[1], o[2], "|", o[4])
