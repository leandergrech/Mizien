#!/usr/bin/env python3
"""CC-132: fetch Eurostat ilc_atst01 / ilc_atst02 (2024; persons 16+, total) -> data/cc-132/. Needs network."""
import csv, itertools, json, pathlib, urllib.request

D = pathlib.Path(__file__).resolve().parents[2] / "data" / "cc-132"
BASE = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
Q = "?format=JSON&lang=en&time=2024&yn_arope=TOTAL&sex=T&age=Y_GE16"


def get(ds, extra, out):
    d = json.load(urllib.request.urlopen(BASE + ds + Q + extra, timeout=90))
    ids = d["id"]
    dims = [list(d["dimension"][k]["category"]["index"]) for k in ids]
    rows = []
    for i, c in enumerate(itertools.product(*dims)):
        v = d["value"].get(str(i))
        if v is not None:
            rows.append(dict(zip(ids, c)) | {"value": v, "flag": d.get("status", {}).get(str(i), ""),
                                             "updated": d["updated"]})
    with open(D / out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


get("ilc_atst01", "", "eurostat_ilc_atst01_2024.csv")
get("ilc_atst02", "&geo=MT&geo=EU27_2020", "eurostat_ilc_atst02_2024_MT_EU.csv")
