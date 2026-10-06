#!/usr/bin/env python3
"""CC-031: fetch Eurostat Malta greenhouse-gas emissions (total, transport, road transport) and population of Malta and
Gozo and Comino (NUTS 3 MT002) -> data/cc-031/eurostat_ghg_pop.csv. Needs network."""
import csv, json, pathlib, urllib.request, datetime
ROOT = pathlib.Path(__file__).resolve().parents[2]
B = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
Q = {
 "env_air_gge": "env_air_gge?geo=MT&unit=MIO_T&airpol=GHG&src_crf=TOTX4_MEMO&src_crf=CRF1A3&src_crf=CRF1A3B&sinceTimePeriod=2005",
 "demo_r_pjangrp3": "demo_r_pjangrp3?geo=MT&geo=MT002&sex=T&age=TOTAL&unit=NR&sinceTimePeriod=2015",
}
out = []
for ds, q in Q.items():
    d = json.load(urllib.request.urlopen(B + q))
    dims, size = d["id"], d["size"]
    idx = [{v: k for k, v in d["dimension"][n]["category"]["index"].items()} for n in dims]
    lab = {n: d["dimension"][n]["category"].get("label", {}) for n in dims}
    def coords(pos):
        c = []
        for s in reversed(size):
            c.append(pos % s); pos //= s
        c = c[::-1]
        return {n: idx[i][c[i]] for i, n in enumerate(dims)}
    for k, val in d["value"].items():
        c = coords(int(k))
        item = c.get("src_crf", "POP")
        out.append([ds, c["geo"], item, lab.get("src_crf", {}).get(item, "Population on 1 January"), c["time"], val,
                    d.get("status", {}).get(k, ""), d["updated"], B + q])
with open(ROOT / "data/cc-031/eurostat_ghg_pop.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["dataset","geo","item","item_label","year","value","flag","eurostat_updated","query_url","retrieved"])
    for r in sorted(out): w.writerow(r + [datetime.date.today().isoformat()])
print(len(out), "rows")
