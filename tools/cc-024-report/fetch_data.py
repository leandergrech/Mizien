#!/usr/bin/env python3
"""CC-024: fetch Eurostat nrg_ind_ren (share of energy from renewable sources) for Malta, Cyprus and the EU-27,
with status flags, into data/cc-024/eurostat_nrg_ind_ren.csv. Needs network."""
import csv, datetime, json, pathlib, urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
URL = ("https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/nrg_ind_ren?format=JSON&lang=EN"
       "&geo=MT&geo=CY&geo=EU27_2020&nrg_bal=REN&nrg_bal=REN_ELC&nrg_bal=REN_TRA&nrg_bal=REN_HEAT_CL&unit=PC&sinceTimePeriod=2013")
d = json.load(urllib.request.urlopen(URL, timeout=60))
dims = d["id"]
idx = {k: dict(d["dimension"][k]["category"]["index"]) for k in dims}
sizes = d["size"]
rows = []
for key, val in d["value"].items():
    pos = int(key)
    coords = {}
    for k, s in zip(reversed(dims), reversed(sizes)):
        coords[k] = pos % s
        pos //= s
    name = {k: next(c for c, i in idx[k].items() if i == coords[k]) for k in dims}
    flag = d.get("status", {}).get(key, "")
    rows.append({"dataset": "nrg_ind_ren", "geo": name["geo"], "item": name["nrg_bal"], "year": name["time"],
                 "value": val, "flag": flag, "unit": "%", "eurostat_updated": d["updated"],
                 "retrieved": datetime.date.today().isoformat()})
rows.sort(key=lambda r: (r["geo"], r["item"], r["year"]))
out = ROOT / "data" / "cc-024" / "eurostat_nrg_ind_ren.csv"
with open(out, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
print(len(rows), "rows ->", out, "; updated", d["updated"])
