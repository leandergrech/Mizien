#!/usr/bin/env python3
"""CC-100: fetch Eurostat air passenger transport for Malta (avia_paoc: passengers by type of schedule and transport
coverage, annual) -> data/cc-100/eurostat_avia_paoc.csv. MIA's own figures (company announcements) are recorded in
data/cc-100/mia_announcements.csv by hand from the PDFs (read 5 Oct 2026)."""
import csv, datetime, json, pathlib, urllib.request
ROOT = pathlib.Path(__file__).resolve().parents[2]
URL = ("https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/avia_paoc?geo=MT&unit=PAS"
       "&tra_meas=PAS_CRD&tra_meas=PAS_CRD_ARR&tra_meas=PAS_CRD_DEP&freq=A&sinceTimePeriod=2015")
d = json.load(urllib.request.urlopen(URL))
dims, size = d["id"], d["size"]
idx = [{v: k for k, v in d["dimension"][n]["category"]["index"].items()} for n in dims]
rows, today = [], datetime.date.today().isoformat()
for k, val in d["value"].items():
    pos, out = int(k), []
    for s in reversed(size):
        out.append(pos % s); pos //= s
    c = {n: idx[i][x] for i, (n, x) in enumerate(zip(dims, out[::-1]))}
    rows.append([c["geo"], c["tra_meas"], c["schedule"], c["tra_cov"], c["time"], val, d.get("status", {}).get(k, ""), d["updated"], URL, today])
with open(ROOT / "data/cc-100/eurostat_avia_paoc.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["geo", "tra_meas", "schedule", "tra_cov", "year", "value", "flag", "eurostat_updated", "query_url", "retrieved"])
    w.writerows(sorted(rows))
print(len(rows), d["updated"])
