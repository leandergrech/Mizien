#!/usr/bin/env python3
"""CC-115: fetch Malta's GDP (Eurostat nama_10_gdp: current prices and chain-linked volumes, 2015 and 2020 reference
years) -> data/cc-115/eurostat_nama_10_gdp.csv. The congestion figure itself comes from the National Transport Master
Plan 2030 (read; see literature/CC-115/notes.md) and is recorded in data/cc-115/congestion_estimates.csv by hand."""
import csv, datetime, json, pathlib, urllib.request
ROOT = pathlib.Path(__file__).resolve().parents[2]
URL = ("https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/nama_10_gdp?geo=MT&na_item=B1GQ"
       "&unit=CP_MEUR&unit=CLV20_MEUR&unit=CLV15_MEUR&sinceTimePeriod=2015")
d = json.load(urllib.request.urlopen(URL))
dims, size = d["id"], d["size"]
idx = [{v: k for k, v in d["dimension"][n]["category"]["index"].items()} for n in dims]
rows, today = [], datetime.date.today().isoformat()
for k, val in d["value"].items():
    pos, out = int(k), []
    for s in reversed(size):
        out.append(pos % s); pos //= s
    c = {n: idx[i][x] for i, (n, x) in enumerate(zip(dims, out[::-1]))}
    rows.append([c["geo"], c["unit"], c["time"], val, d.get("status", {}).get(k, ""), d["updated"], URL, today])
with open(ROOT / "data/cc-115/eurostat_nama_10_gdp.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["geo", "unit", "year", "value", "flag", "eurostat_updated", "query_url", "retrieved"])
    w.writerows(sorted(rows))
print(len(rows), d["updated"])
