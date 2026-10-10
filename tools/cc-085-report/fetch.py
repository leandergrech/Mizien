#!/usr/bin/env python3
"""CC-085: fetch Eurostat tourism data for Malta -> data/cc-085/eurostat_tourism.csv.

Datasets (Eurostat dissemination API, JSON-stat):
  tour_cap_nat   establishments, bedrooms and bed-places in tourist accommodation (NACE I55.1 hotels; I55.1-I55.3 all)
  tour_occ_anor  net occupancy rate of bed-places and bedrooms in hotels and similar accommodation (I55.1), annual
  tour_occ_arnat arrivals at tourist accommodation establishments, annual (by residence: TOTAL, FOR = foreign)
  tour_occ_ninat nights spent at tourist accommodation establishments, annual (by residence)
Each row keeps the dataset label, Eurostat's 'updated' stamp and status flag, the query URL and the retrieval date.
These are accommodation-establishment statistics (NSO's collective accommodation survey). They are not the NSO's
inbound tourism (frontier) survey, which counts all tourists, including those in private and non-rented homes.
"""
import csv
import datetime
import json
import pathlib
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "cc-085" / "eurostat_tourism.csv"
API = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
QUERIES = {
    "tour_cap_nat": "?geo=MT&unit=NR&nace_r2=I551&nace_r2=I551-I553&accomunit=BEDPL&accomunit=BEDRM&accomunit=ESTBL"
                    "&sinceTimePeriod=2010",
    "tour_occ_anor": "?geo=MT&unit=PC&hotelsize=TOTAL&accomunit=BEDPL&accomunit=BEDRM&sinceTimePeriod=2010",
    "tour_occ_arnat": "?geo=MT&unit=NR&nace_r2=I551&nace_r2=I551-I553&c_resid=TOTAL&c_resid=FOR&sinceTimePeriod=2010",
    "tour_occ_ninat": "?geo=MT&unit=NR&nace_r2=I551&nace_r2=I551-I553&c_resid=TOTAL&c_resid=FOR&sinceTimePeriod=2010",
}


def flat(d):
    dims, size = d["id"], d["size"]
    idx = [{v: k for k, v in d["dimension"][n]["category"]["index"].items()} for n in dims]
    for k, val in d["value"].items():
        pos, out = int(k), []
        for s in reversed(size):
            out.append(pos % s)
            pos //= s
        c = {n: idx[i][x] for i, (n, x) in enumerate(zip(dims, out[::-1]))}
        yield c, val, d.get("status", {}).get(k, "")


rows, today = [], datetime.date.today().isoformat()
for ds, q in QUERIES.items():
    url = API + ds + q
    d = json.load(urllib.request.urlopen(url, timeout=90))
    for c, val, flag in flat(d):
        series = "|".join(f"{k}={c[k]}" for k in ("nace_r2", "accomunit", "c_resid", "hotelsize", "unit") if k in c)
        rows.append([ds, d["label"], series, c["time"], val, flag, d["updated"], url, today])
rows.sort(key=lambda r: (r[0], r[2], r[3]))
with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["dataset", "label", "series", "year", "value", "flag", "eurostat_updated", "query_url", "retrieved"])
    w.writerows(rows)
print(len(rows), "rows ->", OUT.relative_to(ROOT))
