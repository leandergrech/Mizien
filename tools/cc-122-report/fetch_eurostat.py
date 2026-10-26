#!/usr/bin/env python3
"""CC-122: fetch Malta bed-places, arrivals and nights in tourist accommodation from Eurostat.
Writes data/cc-122/eurostat_tourism.csv (value, status flag, query URL, retrieval date). Network needed.
  tour_cap_nat     bed-places (accomunit=BEDPL, unit=NR), NACE I551-I553, 2015-2025
  tour_occ_arnat   arrivals at tourist accommodation establishments (unit=NR), I551-I553, residents of other countries (FOR)
  tour_occ_ninat   nights spent (unit=NR), I551-I553, FOR
"""
import csv, datetime, json, pathlib, urllib.request

D = pathlib.Path(__file__).resolve().parents[2] / "data" / "cc-122"
B = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
Q = {
    "tour_cap_nat": "tour_cap_nat?geo=MT&unit=NR&nace_r2=I551-I553&accomunit=BEDPL&sinceTimePeriod=2015",
    "tour_occ_arnat": "tour_occ_arnat?geo=MT&unit=NR&nace_r2=I551-I553&c_resid=FOR&sinceTimePeriod=2015",
    "tour_occ_ninat": "tour_occ_ninat?geo=MT&unit=NR&nace_r2=I551-I553&c_resid=FOR&sinceTimePeriod=2015",
}
today = datetime.date.today().isoformat()
rows = []
for ds, q in Q.items():
    d = json.load(urllib.request.urlopen(B + q, timeout=240))
    times = {i: t for t, i in d["dimension"]["time"]["category"]["index"].items()}
    fl = d.get("status", {})
    for k, v in d["value"].items():
        rows.append([ds, d["label"], times[int(k)], v, fl.get(k, ""), d["updated"], B + q, today])
rows.sort(key=lambda r: (r[0], r[2]))
with open(D / "eurostat_tourism.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["dataset", "label", "year", "value", "flag", "eurostat_updated", "query_url", "retrieved"])
    w.writerows(rows)
for r in rows:
    print(r[0], r[2], r[3], r[4])
