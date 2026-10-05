#!/usr/bin/env python3
"""CC-112: fetch Eurostat population change by component (demo_gind: population on 1 January, live births, deaths,
natural change, net migration plus statistical adjustment, CNMIGRAT) for Malta and the EU-27 -> data/cc-112/eurostat_demo_gind.csv."""
import csv, datetime, json, pathlib, urllib.request
ROOT = pathlib.Path(__file__).resolve().parents[2]
URL = ("https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/demo_gind?geo=MT&geo=EU27_2020"
       "&indic_de=JAN&indic_de=LBIRTH&indic_de=DEATH&indic_de=NATGROW&indic_de=CNMIGRAT&indic_de=GROW&sinceTimePeriod=2005")
d = json.load(urllib.request.urlopen(URL))
dims, size = d["id"], d["size"]
idx = [{v: k for k, v in d["dimension"][n]["category"]["index"].items()} for n in dims]
rows, today = [], datetime.date.today().isoformat()
for k, val in d["value"].items():
    pos, out = int(k), []
    for s in reversed(size):
        out.append(pos % s); pos //= s
    c = {n: idx[i][x] for i, (n, x) in enumerate(zip(dims, out[::-1]))}
    rows.append([c["geo"], c["indic_de"], c["time"], val, d.get("status", {}).get(k, ""), d["updated"], URL, today])
with open(ROOT / "data/cc-112/eurostat_demo_gind.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["geo", "indic_de", "year", "value", "flag", "eurostat_updated", "query_url", "retrieved"])
    w.writerows(sorted(rows))
print(len(rows), d["updated"])
