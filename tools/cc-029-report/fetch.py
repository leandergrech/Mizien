#!/usr/bin/env python3
"""CC-029: fetch Malta electricity balance (Eurostat nrg_cb_e, siec E7000, GWh) -> data/cc-029/eurostat_electricity.csv.
Needs network. Only the lines used by calc.py are kept."""
import csv, json, pathlib, urllib.request, datetime
ROOT = pathlib.Path(__file__).resolve().parents[2]
Q = ("https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/nrg_cb_e?geo=MT&siec=E7000&unit=GWH"
     "&nrg_bal=GEP&nrg_bal=IMP&nrg_bal=EXP&nrg_bal=FC&nrg_bal=AFC&sinceTimePeriod=2019&format=JSON")
d = json.load(urllib.request.urlopen(Q))
ids, sz = d["id"], d["size"]
bal = {v: k for k, v in d["dimension"]["nrg_bal"]["category"]["index"].items()}
yr = {v: k for k, v in d["dimension"]["time"]["category"]["index"].items()}
rows = []
for k, val in d["value"].items():
    pos, c = int(k), []
    for s in reversed(sz):
        c.append(pos % s); pos //= s
    m = dict(zip(ids, c[::-1]))
    b = bal[m["nrg_bal"]]
    rows.append(["nrg_cb_e", "MT", b, d["dimension"]["nrg_bal"]["category"]["label"][b], yr[m["time"]], val,
                 d.get("status", {}).get(k, ""), d["updated"], Q, datetime.date.today().isoformat()])
with open(ROOT / "data/cc-029/eurostat_electricity.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["dataset", "geo", "code", "label", "year", "value_gwh", "flag", "eurostat_updated", "query_url", "retrieved"])
    w.writerows(sorted(rows, key=lambda r: (r[2], r[4])))
print(len(rows), "rows")
