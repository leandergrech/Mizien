#!/usr/bin/env python3
"""CC-018: fetch Eurostat tipsho60 (standardised house price-to-income ratio) for Malta and the EU-27.

Writes data/cc-018/eurostat_tipsho60.csv. Network needed (Eurostat dissemination API).
"""
import csv, json, pathlib, urllib.request

OUT = pathlib.Path(__file__).resolve().parents[2] / "data" / "cc-018" / "eurostat_tipsho60.csv"
URL = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/tipsho60?geo=MT&geo=EU27_2020"
d = json.load(urllib.request.urlopen(URL, timeout=120))
dims = d["id"]
cats = {k: {i: c for c, i in d["dimension"][k]["category"]["index"].items()} for k in dims}
labels = d["dimension"]["unit"]["category"]["label"]
sizes = d["size"]
rows = []
for k, v in d["value"].items():
    k, pos = int(k), {}
    for dim, n in zip(reversed(dims), reversed(sizes)):
        pos[dim] = cats[dim][k % n]
        k //= n
    rows.append({"unit": pos["unit"], "unit_label": labels[pos["unit"]], "geo": pos["geo"], "year": pos["time"], "value": v})
rows.sort(key=lambda r: (r["unit"], r["geo"], r["year"]))
with open(OUT, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\r\n")
    w.writeheader()
    w.writerows(rows)
print(len(rows), "rows ->", OUT)
