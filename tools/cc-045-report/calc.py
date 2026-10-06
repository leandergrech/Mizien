#!/usr/bin/env python3
"""CC-045: rainfall context for the flood-tunnel claim, computed from saved data (not by eye).

Input:  data/cc-045/ghcnd_luqa_prcp_raw.csv  (NOAA NCEI GHCN-Daily, station MT000016597 Luqa, daily PRCP in tenths of mm;
        retrieved 6 Oct 2026 from the NCEI access service, URL in data/cc-045/README.md)
        data/cc-045/lengths.csv               (tunnel lengths as stated by each source)
Output: data/cc-045/luqa_annual.csv, data/cc-045/heavy_days_since_2015.csv, data/cc-045/checks.csv
"""
import csv, pathlib, collections

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-045"
MIN_DAYS = 330        # a year counts for annual maxima only if at least 330 of its days have a reading
HEAVY_MM = 50.0       # a "heavy day" for this check; arbitrary round figure, used only to list events, not as a design value

days = {}
for r in csv.DictReader(open(D / "ghcnd_luqa_prcp_raw.csv", encoding="utf-8")):
    if r["PRCP"].strip() != "":
        days[r["DATE"]] = float(r["PRCP"]) / 10.0     # tenths of mm -> mm
by_year = collections.defaultdict(dict)
for d, v in days.items():
    by_year[int(d[:4])][d] = v

rows = []
for y in sorted(by_year):
    vals = by_year[y]
    mx_d = max(vals, key=vals.get)
    rows.append({"year": y, "days_with_reading": len(vals), "complete": int(len(vals) >= MIN_DAYS),
                 "total_mm": round(sum(vals.values()), 1), "max_day_mm": vals[mx_d], "max_day": mx_d,
                 "days_ge_50mm": sum(v >= HEAVY_MM for v in vals.values())})
with open(D / "luqa_annual.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

full = [r for r in rows if r["complete"]]
mx = sorted((r["max_day_mm"] for r in full), reverse=True)
n = len(mx)
# Weibull plotting position: return period T = (n + 1) / rank for the rank-th largest annual maximum
def level_for_T(T):
    k = (n + 1) / T                     # fractional rank
    lo = int(k); fr = k - lo
    a = mx[lo - 1]; b = mx[lo] if lo < n else mx[-1]
    return a + (b - a) * fr
five = level_for_T(5)
two = level_for_T(2)
out = []
def add(check, value, unit, note=""):
    out.append({"check": check, "value": value, "unit": unit, "note": note})

add("Years with at least %d daily readings (Luqa, 1990-2025)" % MIN_DAYS, n, "years",
    "first %d, last %d; years below the cut-off are not used for annual maxima" % (full[0]["year"], full[-1]["year"]))
add("Years excluded for missing readings", ", ".join(str(r["year"]) for r in rows if not r["complete"]), "",
    "daily readings missing; the maximum of an incomplete year could be understated")
add("Median annual maximum daily rainfall", round(sorted(mx)[n // 2], 1), "mm", "empirical, complete years")
add("Empirical 2-year daily rainfall at Luqa (Weibull)", round(two, 1), "mm")
add("Empirical 5-year daily rainfall at Luqa (Weibull)", round(five, 1), "mm",
    "single gauge, 24-hour totals; the NFRP design storm is a catchment flow criterion, not this figure")
add("Largest daily total in the record", max(mx), "mm", next(r["max_day"] for r in full if r["max_day_mm"] == max(mx)))

since = [(d, v) for d, v in sorted(days.items()) if d >= "2015-01-01" and v >= HEAVY_MM]
with open(D / "heavy_days_since_2015.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["date", "luqa_mm"]); w.writerows(since)
add("Days at or above %.0f mm at Luqa, 1 Jan 2015 to 5 Oct 2026" % HEAVY_MM, len(since), "days",
    "; ".join("%s %.1f" % x for x in since))
add("Luqa daily rainfall on 14 Sep 2020 (the day before Lovin Malta's report of flooding)", days.get("2020-09-14"), "mm",
    "Luqa is about 6 km from Birkirkara; 13 Sep has no reading; below the empirical 2-year level, so a single gauge "
    "does not show the storm")
add("Years 2015-2025 with complete readings", sum(1 for r in full if r["year"] >= 2015), "of 11",
    "2020-2023 and 2025 are incomplete: too few years to compare 'before' and 'after' the tunnels")

L = list(csv.DictReader(open(D / "lengths.csv", encoding="utf-8")))
for r in L:
    add("Length stated: " + r["source"], r["km"], "km", r["what"])
add("Gap between 20 km (claim) and 16 km (Public Works Department, 4 Jul 2025)", 20 - 16, "km",
    "the department describes 16 km as in use and 4 km more as planned")
with open(D / "checks.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["check", "value", "unit", "note"]); w.writeheader(); w.writerows(out)
for r in out: print(r["check"], "|", r["value"], r["unit"], "|", r["note"][:140])
