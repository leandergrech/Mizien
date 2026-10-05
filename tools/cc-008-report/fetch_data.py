"""Claim Check 008: fetch hourly NO2 for Msida and comparison stations from the EEA air-quality download service,
and station metadata from Malta's own reporting to the EEA. Needs network and pyarrow (pip install pyarrow).

Outputs (data/cc-008/):
  no2_daily.csv       daily means per station from 2022 (valid hours only; hourly values are not stored)
  no2_monthly.csv     monthly means per station (valid hours only), coverage and validation flag
  no2_annual.csv      calendar-year means per station (validated E1a years; 2026 = E2a, Jan to latest)
  aq_stations.csv     station and sampling-point metadata (location, type, kerb distance, dates)
  flyovers_osm.geojson  the Msida Creek flyover carriageways as mapped in OpenStreetMap (ODbL)
"""
import calendar
import csv
import datetime as dt
import io
import json
import pathlib
import re
import time
import urllib.request
from collections import defaultdict

import pyarrow.parquet as pq

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
D = ROOT / "data" / "cc-008"
D.mkdir(parents=True, exist_ok=True)
TODAY = dt.date.today().isoformat()
API = "https://eeadmz1-downloads-api-appservice.azurewebsites.net/ParquetFile/urls"
NO2 = "http://dd.eionet.europa.eu/vocabulary/aq/pollutant/8"
CDR_D = ("https://cdr.eionet.europa.eu/mt/eu/aqd/d/envayh2iw/DataFlow_D_measurementConfiguration_2025_V1.xml")
OSM = {"Msida Creek": "https://api.openstreetmap.org/api/0.6/map?bbox=14.486,35.891,14.497,35.899"}
UA = {"User-Agent": "Mizien-factcheck/1.0 (+https://github.com/leandergrech/Mizien)"}

# station code -> (short name, role in this check)
STATIONS = {"MT00005": ("Msida (old point)", "traffic"), "MT00011": ("Msida (new point)", "traffic"),
            "MT00008": ("Attard", "urban background"), "MT00004": ("Żejtun", "urban background"),
            "MT00009": ("St Paul's Bay", "traffic")}
VALIDATION = {1: "E2a (up-to-date; not validated)", 2: "E1a (validated)"}


def get(url, data=None, headers=None, tries=4):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, data=data, headers={**UA, **(headers or {})})
            with urllib.request.urlopen(req, timeout=300) as r:
                return r.read()
        except OSError:
            if i == tries - 1:
                raise
            time.sleep(5 * (i + 1))


def urls(dataset):
    body = json.dumps({"countries": ["MT"], "cities": [], "pollutants": [NO2], "dataset": dataset, "source": "API",
                       "dateTimeStart": None, "dateTimeEnd": None, "aggregationType": None}).encode()
    txt = get(API, body, {"Content-Type": "application/json"}).decode("utf-8-sig")
    return [u.strip() for u in txt.splitlines()[1:] if u.strip()]


# ---------------------------------------------------------------- hourly data
hours = defaultdict(dict)   # station -> {start: (value, dataset, url)}
for ds in (2, 1):           # validated E1a first; E2a only fills hours E1a does not cover
    for u in urls(ds):
        code = re.search(r"SPO-(MT\d{5})_", u).group(1)
        if code not in STATIONS:
            continue
        t = pq.read_table(io.BytesIO(get(u))).to_pydict()
        for s, v, val in zip(t["Start"], t["Value"], t["Validity"]):
            if s in hours[code]:
                continue
            hours[code][s] = (float(v) if v is not None and val >= 1 else None, ds, u)
        print(code, VALIDATION[ds], len(t["Start"]), "rows")

# ---------------------------------------------------------------- monthly and annual means
monthly, annual, daily = [], [], []
for code, h in sorted(hours.items()):
    by_m, by_y, by_d = defaultdict(list), defaultdict(list), defaultdict(list)
    for s, (v, ds, u) in h.items():
        by_m[(s.year, s.month)].append((v, ds, u))
        by_y[s.year].append((v, ds, u))
        if s.year >= 2022:
            by_d[s.date()].append((v, ds))
    for day, rows in sorted(by_d.items()):
        vals = [v for v, _ in rows if v is not None]
        daily.append({"station": code, "date": day.isoformat(),
                      "no2_ugm3": f"{sum(vals) / len(vals):.2f}" if vals else "", "valid_hours": len(vals),
                      "validation": "E1a" if all(ds == 2 for _, ds in rows) else "E2a"})
    for (y, m), rows in sorted(by_m.items()):
        vals = [v for v, _, _ in rows if v is not None]
        n_h = calendar.monthrange(y, m)[1] * 24
        dss = {ds for _, ds, _ in rows}
        monthly.append({"station": code, "name": STATIONS[code][0], "type": STATIONS[code][1],
                        "month": f"{y}-{m:02d}", "no2_ugm3": f"{sum(vals) / len(vals):.2f}" if vals else "",
                        "valid_hours": len(vals), "hours_in_month": n_h,
                        "coverage_pct": f"{100 * len(vals) / n_h:.1f}",
                        "validation": " + ".join(VALIDATION[d] for d in sorted(dss, reverse=True)),
                        "source_url": " ".join(sorted({u for _, _, u in rows})), "retrieved": TODAY})
    for y, rows in sorted(by_y.items()):
        vals = [v for v, _, _ in rows if v is not None]
        n_h = (366 if calendar.isleap(y) else 365) * 24
        dss = {ds for _, ds, _ in rows}
        annual.append({"station": code, "name": STATIONS[code][0], "year": y,
                       "no2_ugm3": f"{sum(vals) / len(vals):.2f}" if vals else "", "valid_hours": len(vals),
                       "coverage_pct": f"{100 * len(vals) / n_h:.1f}",
                       "validation": " + ".join(VALIDATION[d] for d in sorted(dss, reverse=True)),
                       "retrieved": TODAY})
for name, rows in [("no2_monthly.csv", monthly), ("no2_annual.csv", annual), ("no2_daily.csv", daily)]:
    with open(D / name, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print("wrote", D / name, len(rows))

# ---------------------------------------------------------------- station metadata (Malta's D-dataset, 2025)
x = get(CDR_D).decode("utf-8")


def grab(block, pat):
    m = re.search(pat, block, re.S)
    return m.group(1) if m else ""


meta = []
for m in re.finditer(r'<aqd:AQD_Station gml:id="STA-(MT\d{5})".*?</aqd:AQD_Station>', x, re.S):
    code, s = m.group(1), m.group(0)
    sp = re.search(r'<aqd:AQD_SamplingPoint gml:id="SPO-%s_00008_\d+".*?</aqd:AQD_SamplingPoint>' % code, x, re.S)
    sp = sp.group(0) if sp else ""
    sa = re.search(r'<aqd:AQD_Sample gml:id="SPO_F-%s_00008_\d+_\d+".*?</aqd:AQD_Sample>' % code, x, re.S)
    sa = sa.group(0) if sa else ""
    lat, lon = grab(s, r"<gml:pos[^>]*>(.*?)</gml:pos>").split()
    meta.append({"station": code, "name": grab(s, r"<ef:name>(.*?)</ef:name>"),
                 "municipality": grab(s, r"<aqd:municipality>(.*?)</aqd:municipality>"),
                 "lat": lat, "lon": lon, "area": grab(s, r"areaclassification/(\w+)"),
                 "no2_sampling_point": grab(sp, r'gml:id="(SPO-[^"]+)"'),
                 "no2_classification": grab(sp, r"stationclassification/(\w+)"),
                 "kerb_distance_m": grab(sa, r"<aqd:kerbDistance[^>]*>(.*?)</aqd:kerbDistance>"),
                 "inlet_height_m": grab(sa, r"<aqd:inletHeight[^>]*>(.*?)</aqd:inletHeight>"),
                 "begin": grab(s, r"<gml:beginPosition>(.*?)</gml:beginPosition>")[:10],
                 "end": grab(s, r"<gml:endPosition>(.*?)</gml:endPosition>")[:16],
                 "source": "ERA, Air Quality e-Reporting dataset D, 2025 (Eionet CDR, AQD_REP_MT_ERA_D-001_2025)",
                 "url": CDR_D, "retrieved": TODAY})
with open(D / "aq_stations.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(meta[0]))
    w.writeheader()
    w.writerows(meta)
print("wrote aq_stations.csv", len(meta))

# ---------------------------------------------------------------- Msida Creek flyover carriageways from OpenStreetMap
import xml.etree.ElementTree as ET  # noqa: E402

ROADS = {"trunk"}  # the flyover carries Triq Mikiel Anton Vassalli (trunk road) over the Msida Creek junction
feats = []
for junction, url in OSM.items():
    root = ET.fromstring(get(url))
    nodes = {n.get("id"): (float(n.get("lon")), float(n.get("lat"))) for n in root.iter("node")}
    for w_ in root.iter("way"):
        tags = {t.get("k"): t.get("v") for t in w_.iter("tag")}
        if tags.get("highway") in ROADS and tags.get("bridge") == "yes":
            feats.append({"type": "Feature", "properties": {"junction": junction, "osm_way": w_.get("id"),
                                                            "name": tags.get("name", ""), "highway": tags["highway"]},
                          "geometry": {"type": "LineString",
                                       "coordinates": [nodes[n.get("ref")] for n in w_.iter("nd")]}})
json.dump({"type": "FeatureCollection", "attribution": "© OpenStreetMap contributors (ODbL)",
           "source": list(OSM.values()), "retrieved": TODAY, "features": feats},
          open(D / "flyovers_osm.geojson", "w"), ensure_ascii=False)
print("wrote flyovers_osm.geojson", len(feats), "ways")
