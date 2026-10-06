"""Claim Check 034: download (and cache) Malta's EEA air-quality files.

The EEA download service lists one Parquet file per sampling point and dataset:
  dataset 3 = AirBase (historical, to 2012), 2 = E1a (validated, 2013 on), 1 = E2a (up-to-date, not validated).
Files are cached in tools/cc-034-report/out/cache/ (git-ignored); fetch.py turns them into data/cc-034/.
Needs network and pyarrow.
"""
import csv
import datetime as dt
import hashlib
import json
import pathlib
import time
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent
CACHE = HERE / "out" / "cache"
API = "https://eeadmz1-downloads-api-appservice.azurewebsites.net/ParquetFile/urls"
UA = {"User-Agent": "Mizien-factcheck/1.0 (+https://github.com/leandergrech/Mizien)"}
POLLUTANTS = {"PM10": 5, "PM2.5": 6001, "NO2": 8, "SO2": 1, "CO": 10}
DATASETS = {3: "AirBase", 2: "E1a", 1: "E2a"}


def get(url, data=None, headers=None, tries=5):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, data=data, headers={**UA, **(headers or {})})
            with urllib.request.urlopen(req, timeout=300) as r:
                return r.read()
        except OSError:
            if i == tries - 1:
                raise
            time.sleep(5 * (i + 1))


def urls(pollutant_code, dataset):
    body = json.dumps({"countries": ["MT"], "cities": [],
                       "pollutants": [f"http://dd.eionet.europa.eu/vocabulary/aq/pollutant/{pollutant_code}"],
                       "dataset": dataset, "source": "API", "dateTimeStart": None, "dateTimeEnd": None,
                       "aggregationType": None}).encode()
    txt = get(API, body, {"Content-Type": "application/json"}).decode("utf-8-sig")
    return [u.strip() for u in txt.splitlines()[1:] if u.strip()]


def fetch_all(refresh=False):
    """Download every Malta file for the five pollutants; return the manifest rows."""
    CACHE.mkdir(parents=True, exist_ok=True)
    man = []
    for pol, code in POLLUTANTS.items():
        for ds, dname in DATASETS.items():
            for u in urls(code, ds):
                local = CACHE / dname / u.rsplit("/", 1)[1]
                local.parent.mkdir(exist_ok=True)
                if refresh or not local.exists():
                    local.write_bytes(get(u))
                b = local.read_bytes()
                man.append({"pollutant": pol, "dataset": dname, "sampling_point": local.stem, "url": u,
                            "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest(),
                            "retrieved": dt.datetime.fromtimestamp(local.stat().st_mtime).date().isoformat()})
                print(pol, dname, local.stem, len(b))
    return man


if __name__ == "__main__":
    m = fetch_all()
    with open(CACHE / "manifest.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(m[0]))
        w.writeheader()
        w.writerows(m)
