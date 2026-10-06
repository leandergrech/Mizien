"""Claim Check 034: build data/cc-034/ from Malta's measured air quality and related statistics.

Sources (all public; network needed; run from the repository root or anywhere):
  1. EEA Air Quality download service: every Maltese sampling point for PM10, PM2.5, NO2, SO2 and CO, datasets
     AirBase (to 2012), E1a (validated, 2013-2025) and E2a (up-to-date, not validated, 2026). eea_cache.py downloads
     them; this script summarises them. Values with Validity < 1 are dropped. Where two validated sampling points of
     one station overlap, the higher-numbered (newer) point is kept; E1a is preferred to AirBase, and both to E2a.
  2. ERA's attainment reports to the EEA (Air Quality e-Reporting dataflow G, Eionet CDR), 2015-2025: the PM10, PM2.5
     and NO2 values before and after the deduction of natural sources (g_cache.py downloads them).
  3. Eurostat env_air_emis (air pollutant emissions by NFR source sector, Malta, tonnes) and road_eqs_carhab /
     road_eqs_carpda (passenger cars), with Eurostat's flags.

Outputs (data/cc-034/):
  eea_files.csv        manifest of the EEA files used (URL, dataset, SHA-256, retrieval date)
  pm10_daily.csv       daily PM10 (µg/m³, 3 decimals as reported), one column per station; blank = no valid value
  pm25_daily.csv       daily PM2.5, same layout
  no2_daily.csv        daily mean NO2 from hourly values, days with at least 18 valid hours only
  annual.csv           station x pollutant x year: mean, valid days or hours, coverage, PM10 days > 50, datasets
  monthly.csv          station x pollutant x month: mean, valid count, dataset
  diurnal.csv          NO2 and CO hour-of-day means, by station, year, season (Jun-Aug, Oct-Dec) and weekday/weekend
                       (hour = the hour of the EEA "Start" time stamp: the beginning of the hour)
  clock_check.csv      hourly values per day on the days the clocks changed (last Sunday of March and October),
                       Msida NO2, 2013-2023: 24 on every one, so the EEA's hourly clock has no daylight saving
  g_attainment.csv     ERA's reported attainment values (before and after natural-source deduction), 2015-2025
  eurostat_emissions.csv  Malta NOx, SOx, PM2.5, PM10 emissions by sector (selected NFR codes), tonnes
  eurostat_cars.csv    Malta passenger cars (stock and per 1,000 inhabitants)
"""
import calendar
import csv
import datetime as dt
import json
import pathlib
import sys
import urllib.request
import xml.etree.ElementTree as ET
from collections import defaultdict

import pyarrow.parquet as pq

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import eea_cache  # noqa: E402
import g_cache  # noqa: E402

ROOT = HERE.parents[1]
D = ROOT / "data" / "cc-034"
D.mkdir(parents=True, exist_ok=True)
TODAY = dt.date.today().isoformat()
STATIONS = {"MT00002": "(AirBase, 2004-06)", "MT00003": "Kordin", "MT00004": "Żejtun", "MT00005": "Msida (old point)",
            "MT00007": "Għarb", "MT00008": "Attard", "MT00009": "St Paul's Bay", "MT00011": "Msida (new point)"}
RANK = {"E1a": 3, "AirBase": 2, "E2a": 1}
UNIT = {"CO": "mg/m3"}   # every other pollutant is in µg/m3 (EEA unit codes mg.m-3 and ug.m-3)


def write(name, rows, fields=None):
    with open(D / name, "w", newline="", encoding="utf-8") as f:
        if fields is None:
            fields = list(dict.fromkeys(k for r in rows for k in r))
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print("wrote", name, len(rows))


# ------------------------------------------------------------------ 1. EEA measurements
manifest = eea_cache.fetch_all()
write("eea_files.csv", manifest)

# best[(station, pollutant)][timestamp] = (value, rank, sp_number, aggtype, dataset)
best = defaultdict(dict)
for m in manifest:
    f = eea_cache.CACHE / m["dataset"] / (m["sampling_point"] + ".parquet")
    st, _, spn = m["sampling_point"].replace("SPO-", "").split("_")
    t = pq.read_table(f, columns=["Start", "Value", "AggType", "Validity"]).to_pydict()
    rk = RANK[m["dataset"]]
    for s, v, agg, val in zip(t["Start"], t["Value"], t["AggType"], t["Validity"]):
        if v is None or val is None or val < 1:
            continue
        key = (st, m["pollutant"])
        old = best[key].get(s)
        if old is None or (rk, int(spn)) > (old[1], old[2]):
            best[key][s] = (float(v), rk, int(spn), agg, m["dataset"])

# daily values: PM keeps daily aggregates (or daily means of hourly E2a with >= 18 h); gases from hourly
daily = defaultdict(dict)       # (station, pollutant) -> {date: (value, n_hours or None, dataset)}
hourly = defaultdict(dict)      # (station, pollutant) -> {datetime: value}  (hourly series only)
for key, series in best.items():
    by_day = defaultdict(list)
    for s, (v, rk, spn, agg, ds) in series.items():
        if agg == "day":
            # a validated daily value wins over a day assembled from unvalidated hours
            daily[key][s.date()] = (v, None, ds)
        elif agg == "hour":
            hourly[key][s] = v
            by_day[s.date()].append((v, ds))
    for day, vals in by_day.items():
        if day in daily[key] or len(vals) < 18:
            continue
        dss = {d for _, d in vals}
        daily[key][day] = (sum(v for v, _ in vals) / len(vals), len(vals), "+".join(sorted(dss)))


def wide(pollutant, name, start=dt.date(2004, 1, 1)):
    sts = sorted({st for (st, p) in daily if p == pollutant})
    days = sorted({d for (st, p), dd in daily.items() if p == pollutant for d in dd if d >= start})
    rows = []
    for d in days:
        r = {"date": d.isoformat()}
        for st in sts:
            v = daily[(st, pollutant)].get(d)
            r[st] = f"{v[0]:.3f}" if v else ""   # unrounded to 3 dp: a day counts as over 50 on the exact value
        rows.append(r)
    write(name, rows, ["date"] + sts)


wide("PM10", "pm10_daily.csv")
wide("PM2.5", "pm25_daily.csv")
wide("NO2", "no2_daily.csv")

# annual and monthly summaries
annual, monthly = [], []
for (st, pol), dd in sorted(daily.items()):
    by_y, by_m = defaultdict(list), defaultdict(list)
    for d, (v, nh, ds) in dd.items():
        by_y[d.year].append((v, ds))
        by_m[(d.year, d.month)].append((v, ds))
    hrs = hourly.get((st, pol), {})
    hy = defaultdict(list)
    for s, v in hrs.items():
        hy[s.year].append(v)
    for y, vals in sorted(by_y.items()):
        ndays = 366 if calendar.isleap(y) else 365
        if hy.get(y):   # gases: annual mean of all valid hours, as the EU directive computes it
            mean, n, cov = sum(hy[y]) / len(hy[y]), len(hy[y]), 100 * len(hy[y]) / (ndays * 24)
            unit_n = "hours"
        else:
            mean, n, cov = sum(v for v, _ in vals) / len(vals), len(vals), 100 * len(vals) / ndays
            unit_n = "days"
        annual.append({"station": st, "name": STATIONS.get(st, st), "pollutant": pol, "year": y,
                       "mean": f"{mean:.2f}", "unit": UNIT.get(pol, "ug/m3"), "n_valid": n, "n_unit": unit_n, "coverage_pct": f"{cov:.1f}",
                       "days_over_50": sum(1 for v, _ in vals if v > 50) if pol == "PM10" else "",
                       "days_with_value": len(vals),
                       "datasets": "+".join(sorted({p for _, ds in vals for p in ds.split("+")},
                                                   key=lambda x: -RANK[x])),
                       "retrieved": TODAY})
    for (y, mo), vals in sorted(by_m.items()):
        monthly.append({"station": st, "pollutant": pol, "month": f"{y}-{mo:02d}",
                        "mean": f"{sum(v for v, _ in vals) / len(vals):.2f}", "unit": UNIT.get(pol, "ug/m3"), "days_with_value": len(vals),
                        "datasets": "+".join(sorted({p for _, ds in vals for p in ds.split("+")},
                                                    key=lambda x: -RANK[x]))})
write("annual.csv", annual)
write("monthly.csv", monthly)

# diurnal profiles (NO2, CO): the plan's Figures 25-26 compare Jun-Aug and Oct-Dec at Msida, 2014-17 vs 2018-19
diur = []
for (st, pol), hrs in sorted(hourly.items()):
    if pol not in ("NO2", "CO"):
        continue
    acc = defaultdict(list)
    for s, v in hrs.items():
        season = "Oct-Dec" if s.month >= 10 else "Jun-Aug" if s.month in (6, 7, 8) else None
        if season is None or not 2012 <= s.year <= 2025:   # validated years only; 2026 is E2a
            continue
        acc[(s.year, season, "weekday" if s.weekday() < 5 else "weekend", s.hour)].append(v)
    for (y, season, dtp, h), vals in sorted(acc.items()):
        diur.append({"station": st, "pollutant": pol, "year": y, "season": season, "daytype": dtp, "hour": h,
                     "mean": f"{sum(vals) / len(vals):.{2 if pol == 'CO' else 1}f}", "unit": UNIT.get(pol, "ug/m3"), "n_hours": len(vals)})
write("diurnal.csv", diur)

# the EEA's hourly time stamps ("Start"): do they follow the clock changes? Count hourly rows on the 22 days (2013-2023)
# on which Malta's clocks changed; the E1a file for Msida NO2 is read as downloaded (all validity flags).
def last_sunday(y, m):
    d = dt.date(y, m, 31)
    while d.weekday() != 6:
        d -= dt.timedelta(days=1)
    return d


change_days = {last_sunday(y, m): m for y in range(2013, 2024) for m in (3, 10)}
f = eea_cache.CACHE / "E1a" / "SPO-MT00005_00008_100.parquet"
t = pq.read_table(f, columns=["Start", "End", "Validity"]).to_pydict()
per_day, valid_day, hour_len = defaultdict(int), defaultdict(int), set()
for s, e, val in zip(t["Start"], t["End"], t["Validity"]):
    hour_len.add((e - s).total_seconds() / 3600)
    if s.date() in change_days:
        per_day[s.date()] += 1
        valid_day[s.date()] += val >= 1
write("clock_check.csv", [{"station": "MT00005", "pollutant": "NO2", "date": d.isoformat(),
                           "change": "clocks forward" if m == 3 else "clocks back", "hourly_rows": per_day[d],
                           "valid_rows": valid_day[d], "end_minus_start_hours": "/".join(str(int(h)) for h in sorted(hour_len)),
                           "file": f.name} for d, m in sorted(change_days.items())])

# ------------------------------------------------------------------ 2. ERA's attainment reports (dataflow G)
NS = {"aqd": "http://dd.eionet.europa.eu/schemaset/id2011850eu-1.0", "gml": "http://www.opengis.net/gml/3.2",
      "base": "http://inspire.ec.europa.eu/schemas/base/3.3", "xlink": "http://www.w3.org/1999/xlink"}
HREF = "{http://www.w3.org/1999/xlink}href"
POLS = {"5": "PM10", "6001": "PM2.5", "8": "NO2", "1": "SO2", "10": "CO"}
grow = []
for y, (url, local) in g_cache.fetch().items():
    root = ET.parse(local).getroot()
    for att in root.iter("{%s}AQD_Attainment" % NS["aqd"]):
        pol = att.find("aqd:pollutant", NS).get(HREF).rsplit("/", 1)[1]
        if pol not in POLS:
            continue
        eo = att.find("aqd:environmentalObjective/aqd:EnvironmentalObjective", NS)
        obj = {k: eo.find(f"aqd:{k}", NS).get(HREF).rsplit("/", 1)[1]
               for k in ("objectiveType", "reportingMetric", "protectionTarget")}
        r = {"year": y, "pollutant": POLS[pol], **obj,
             "zone": (att.find("aqd:zone", NS).get(HREF) or "").rsplit("/", 1)[-1]}
        for part in ("Base", "Adjustment", "Final"):
            ed = att.find(f"aqd:exceedanceDescription{part}/aqd:ExceedanceDescription", NS)
            g = lambda tag: (ed.find(f"aqd:{tag}", NS).text if ed is not None and ed.find(f"aqd:{tag}", NS)
                             is not None else "")
            r[f"{part.lower()}_exceedance"] = g("exceedance")
            r[f"{part.lower()}_value"] = g("numericalExceedance")
            r[f"{part.lower()}_count"] = g("numberExceedances")
            if part == "Base":
                r["stations_used"] = " ".join(s.get(HREF).rsplit("/", 1)[-1]
                                              for s in (ed.iter("{%s}stationUsed" % NS["aqd"]) if ed is not None else []))
        r["source_url"] = url
        r["retrieved"] = TODAY
        grow.append(r)
write("g_attainment.csv", grow)

# ------------------------------------------------------------------ 3. Eurostat
API = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/{}?format=JSON&lang=en{}"


def flat(ds, query=""):
    d = json.load(urllib.request.urlopen(API.format(ds, query), timeout=120))
    dims, sz = d["id"], d["size"]
    cats = [[c for c, _ in sorted(d["dimension"][k]["category"]["index"].items(), key=lambda kv: kv[1])]
            for k in dims]
    status = d.get("status", {})
    rows = []
    for key, v in d["value"].items():
        n = int(key)
        pos = []
        for s in reversed(sz):
            pos.append(n % s)
            n //= s
        pos.reverse()
        rows.append({k: cats[i][p] for i, (k, p) in enumerate(zip(dims, pos))}
                    | {"value": v, "flag": status.get(key, ""), "dataset": ds, "updated": d.get("updated"),
                       "retrieved": TODAY})
    return rows


NFR = ["NFR_TOT_NAT", "NFR1A1A", "NFR1A3B1", "NFR1A3B2", "NFR1A3B3", "NFR1A3B4", "NFR1A3B6", "NFR1A3B7",
       "NFR1A3D2", "NFR2A5A", "NFR2A5B"]
q = "&geo=MT&unit=T" + "".join(f"&airpol={p}" for p in ("NOX", "SOX", "PM2_5", "PM10")) + \
    "".join(f"&src_nfr={s}" for s in NFR)
write("eurostat_emissions.csv", flat("env_air_emis", q))
cars = flat("road_eqs_carhab", "&geo=MT") + flat("road_eqs_carpda", "&geo=MT&mot_nrg=TOTAL&unit=NR")
write("eurostat_cars.csv", cars)
