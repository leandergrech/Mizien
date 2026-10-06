#!/usr/bin/env python3
"""CC-035: download the data behind the EEA's Malta PM2.5 statement into data/cc-035/.

1. EEA 'Burden of disease of air pollution (Countries & NUTS)' table (the EEA's own estimates, the source of the
   quick-facts sentence and of Eurostat sdg_11_52), through the EEA Table publisher (discomap AQViewer, CSV export):
   - eea_ebd_malta_pm25.csv: Malta, country level, all areas, PM2.5, all-cause mortality, both sexes, every scenario
     (WHO 2021 baseline, WHO 2005/HRAPIE, counterfactual 0 and 10 ug/m3), AD and YLL, 2005-2023.
   - eea_ebd_countries_pm25.csv: every country, same filters, WHO 2021 baseline, attributable deaths.
   - eea_ebd_eu27_pm25.csv: the EU-27 total, every scenario, attributable deaths.
2. Eurostat (dissemination API, JSON-stat -> CSV, flags kept in `flag`):
   sdg_11_52 (premature deaths due to PM2.5), demo_pjan (population on 1 January by age), demo_magec (deaths by age),
   hlth_cd_aro (causes of death: all causes and external causes by age), env_air_emis (PM2.5 emissions by sector).
3. EEA station measurements for Malta (Air Quality download service: AirBase 2002-2012 and E1a 2013+ Parquet files,
   PM2.5 and PM10): annual means of valid daily values per station, with the number of valid days
   (eea_stations_malta_annual.csv) and a file manifest with SHA-256 (eea_station_file_manifest.csv).
4. EEA station metadata (PanEuropean_metadata.csv): Malta's PM10 and PM2.5 sampling points with station type, area,
   dates and sampling process (instrument) -> eea_station_metadata_mt.csv.

Usage: python fetch.py [ebd] [eurostat] [stations] [meta]   (no argument = all four parts)
"""
import sys
import csv, datetime, hashlib, io, json, pathlib, urllib.parse, urllib.request, zipfile
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-035"
D.mkdir(parents=True, exist_ok=True)
TODAY = datetime.date.today().isoformat()
UA = {"User-Agent": "Mozilla/5.0 (Mizien research; public EEA and Eurostat data)"}


def get(url, data=None, headers=UA, timeout=180, tries=5):
    """GET (or POST when data is given) with retries: the proxy sometimes resets long transfers."""
    import time
    for i in range(tries):
        try:
            r = urllib.request.Request(url, data=data, headers=headers, method="POST" if data else "GET")
            return urllib.request.urlopen(r, timeout=timeout).read()
        except Exception as e:  # noqa: BLE001
            if i == tries - 1:
                raise
            print("  retry", i + 1, url[:80], e)
            time.sleep(3 * (i + 1))

# ------------------------------------------------------------------ 1. EEA burden-of-disease table
AQV = "https://discomap.eea.europa.eu/App/AQViewer/download?fqn=Airquality_Dissem.ebd.countries_and_nuts&f=csv"
AQV_PAGE = "https://discomap.eea.europa.eu/App/AQViewer/index.html?fqn=Airquality_Dissem.ebd.countries_and_nuts"


def aqviewer(filters):
    req = {"Page": 0, "SortBy": None, "SortAscending": True,
           "RequestFilter": {k: {"FieldName": k, "Values": v} for k, v in filters.items()}}
    blob = get(AQV, json.dumps(req).encode(), UA | {"Content-Type": "application/json"})
    z = zipfile.ZipFile(io.BytesIO(blob))
    text = z.read(z.namelist()[0]).decode("utf-8-sig")
    return list(csv.DictReader(io.StringIO(text))), hashlib.sha256(blob).hexdigest()


COMMON = {"UrbanisationDegree": ["All Areas (incl.unclassified)"], "AirPollutant": ["PM2.5"],
          "Outcome": ["All causes"], "Sex": ["Total"]}
JOBS = [
    ("eea_ebd_malta_pm25.csv", COMMON | {"CountryOrTerritory": ["Malta"], "Detail": ["Country specific"]}),
    ("eea_ebd_countries_pm25.csv", COMMON | {"Detail": ["Country specific"],
                                             "ScenarioDescription": ["Baseline from WHO 2021 AQG"],
                                             "HealthIndicator": ["Attributable deaths (AD)"]}),
    ("eea_ebd_eu27_pm25.csv", COMMON | {"CountryOrTerritory": ["European Union Countries"], "Detail": ["Totals"],
                                        "HealthIndicator": ["Attributable deaths (AD)"]}),
]
PARTS = set(sys.argv[1:]) or {"ebd", "eurostat", "stations", "meta"}

# ------------------------------------------------------------------ 4. EEA station metadata (Malta, PM10 and PM2.5)
META = "https://discomap.eea.europa.eu/map/fme/metadata/PanEuropean_metadata.csv"
if "meta" in PARTS:
    blob = get(META, timeout=300)
    csv.field_size_limit(10 ** 7)
    keep = ["AirQualityStationEoICode", "SamplingPoint", "SamplingProces", "AirPollutantCode", "AirQualityStationType",
            "AirQualityStationArea", "ObservationDateBegin", "ObservationDateEnd", "MeasurementType",
            "MeasurementEquipment", "EquivalenceDemonstrated", "Longitude", "Latitude"]
    seen, meta_rows = set(), []
    for r in csv.DictReader(io.StringIO(blob.decode("utf-8", "replace")), delimiter="\t"):
        if r["Countrycode"] != "MT" or r["AirPollutantCode"].rsplit("/", 1)[-1] not in ("5", "6001"):
            continue
        row = {k: r[k] for k in keep}
        if tuple(row.values()) not in seen:
            seen.add(tuple(row.values())); meta_rows.append(row)
    for r in meta_rows:
        r["source"], r["retrieved"], r["file_sha256"] = META, TODAY, hashlib.sha256(blob).hexdigest()
    with open(D / "eea_station_metadata_mt.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(meta_rows[0])); w.writeheader(); w.writerows(meta_rows)
    print("metadata:", len(meta_rows), "Malta PM sampling-point rows")
for out, flt in (JOBS if "ebd" in PARTS else []):
    rows, sha = aqviewer(flt)
    # the export uses display labels as column names ("Scenario", "Health Indicator", "Value", ...)
    rows = sorted(rows, key=lambda r: (r["Country Or Territory"], r["Scenario"], r["Health Indicator"], r["Year"]))
    for r in rows:
        r["source"], r["retrieved"], r["download_sha256"] = AQV_PAGE, TODAY, sha
    with open(D / out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    print(out, len(rows), "rows")

# ------------------------------------------------------------------ 2. Eurostat
API = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/{}?format=JSON&lang=en{}"


def eurostat(ds, query=""):
    d = json.loads(get(API.format(ds, query)))
    dims, sz = d["id"], d["size"]
    cats = [[c for c, _ in sorted(d["dimension"][k]["category"]["index"].items(), key=lambda kv: kv[1])]
            for k in dims]
    status = d.get("status", {})
    rows = []
    for key, v in d["value"].items():
        n = int(key); pos = []
        for s in reversed(sz):
            pos.append(n % s); n //= s
        pos.reverse()
        rows.append({k: cats[i][p] for i, (k, p) in enumerate(zip(dims, pos))}
                    | {"value": v, "flag": status.get(key, "")})
    return rows, d.get("updated"), d.get("extension", {}).get("status", {}).get("label", {})


YEARS = "".join(f"&time={y}" for y in range(2005, 2025))
ES = (
    ("sdg_11_52", "", "eurostat_sdg_11_52.csv"),
    ("demo_pjan", "&geo=MT&sex=T" + YEARS, "eurostat_demo_pjan_mt.csv"),
    ("demo_magec", "&geo=MT&sex=T" + YEARS, "eurostat_demo_magec_mt.csv"),
    ("hlth_cd_aro", "&geo=MT&sex=T&resid=TOT_RESID&icd10=TOTAL&icd10=V01-Y89", "eurostat_hlth_cd_aro_mt.csv"),
    ("env_air_emis", "&geo=MT&airpol=PM2_5", "eurostat_env_air_emis_mt_pm25.csv"),
)
for ds, q, out in (ES if "eurostat" in PARTS else []):
    rows, upd, labels = eurostat(ds, q)
    for r in rows:
        r["dataset"], r["updated"], r["retrieved"] = ds, upd, TODAY
    with open(D / out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    print(ds, len(rows), "rows, updated", upd, "flags:", labels)

# ------------------------------------------------------------------ 3. EEA station files for Malta
DL_API = "https://eeadmz1-downloads-api-appservice.azurewebsites.net/ParquetFile/urls"
DATASETS = {3: "AirBase (2002-2012)", 2: "E1a verified (2013 onwards)"}
if "stations" not in PARTS:
    sys.exit(0)
import pyarrow as pa, pyarrow.parquet as pq  # noqa: E402  (pip install pyarrow)

manifest = []
daily = defaultdict(list)    # (pollutant, station, date, dataset) -> daily values from every sampling point
hourly = defaultdict(list)   # (pollutant, station, date, dataset) -> valid hourly values
for pol in ("PM2.5", "PM10"):
    for ds, label in DATASETS.items():
        body = {"countries": ["MT"], "cities": [], "pollutants": [pol], "dataset": ds, "source": "Api",
                "dateTimeStart": None, "dateTimeEnd": None, "aggregationType": None}
        raw = get(DL_API, json.dumps(body).encode(), UA | {"Content-Type": "application/json"})
        urls = [u.strip() for u in raw.decode("utf-8-sig").splitlines() if u.strip().startswith("http")]
        for url in urls:
            blob = get(url)
            t = pq.read_table(pa.BufferReader(blob)).to_pylist()
            station = url.rsplit("/", 1)[1].split("-", 1)[1].split("_")[0]   # e.g. MT00004
            manifest.append({"pollutant": pol, "dataset": label, "station": station, "url": url, "bytes": len(blob),
                             "sha256": hashlib.sha256(blob).hexdigest(), "retrieved": TODAY})
            for row in t:
                v = row["Value"]
                # Validity 1-3 = valid; -1/-99 = not valid; negative values are fill codes
                if row["Validity"] not in (1, 2, 3) or v is None or float(v) < 0:
                    continue
                key = (pol, station, row["Start"].date(), label)
                if row["AggType"] == "day":
                    daily[key].append(float(v))
                elif row["AggType"] == "hour":
                    hourly[key].append(float(v))

# a day from hourly data counts if at least 18 of 24 hours (75%) are valid; where two sampling points of one station
# report the same day, their values are averaged so the day counts once
days = defaultdict(dict)
for key, vals in hourly.items():
    if len(vals) >= 18:
        days[(key[0], key[1], key[2].year, key[3], "hourly")][key[2]] = sum(vals) / len(vals)
for key, vals in daily.items():
    days[(key[0], key[1], key[2].year, key[3], "daily")][key[2]] = sum(vals) / len(vals)

rows = []
for (pol, station, year, label, kind), byday in sorted(days.items()):
    vals = list(byday.values())
    ndays = 366 if year % 4 == 0 else 365
    rows.append({"pollutant": pol, "station": station, "year": year, "dataset": label, "time_step": kind,
                 "valid_days": len(vals), "coverage_pct": round(100 * len(vals) / ndays, 1),
                 "mean_of_valid_days_ug_m3": round(sum(vals) / len(vals), 2),
                 "source": "EEA Air Quality download service (Parquet); see eea_station_file_manifest.csv",
                 "retrieved": TODAY})
with open(D / "eea_stations_malta_annual.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
with open(D / "eea_station_file_manifest.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(manifest[0])); w.writeheader(); w.writerows(manifest)
print("stations:", len(manifest), "files,", len(rows), "station-years")
