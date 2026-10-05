#!/usr/bin/env python3
"""CC-025: fetch Eurostat GDP (chain-linked volumes), greenhouse gas totals and population for Malta and the EU-27
-> data/cc-025/eurostat_gdp_ghg_pop.csv (with status flags and the query URL). Needs network."""
import csv, json, pathlib, urllib.request, datetime
ROOT = pathlib.Path(__file__).resolve().parents[2]
B = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
Q = {
 "nama_10_gdp": "nama_10_gdp?geo=MT&geo=EU27_2020&na_item=B1GQ&unit=CLV20_MEUR&unit=CP_MEUR&sinceTimePeriod=2005",
 "env_air_gge": "env_air_gge?geo=MT&geo=EU27_2020&unit=MIO_T&airpol=GHG&src_crf=TOTX4_MEMO&src_crf=TOTXMEMO&sinceTimePeriod=2005",
 "nama_10_pe": "nama_10_pe?geo=MT&geo=EU27_2020&na_item=POP_NC&sinceTimePeriod=2005",
}
out = []
for ds, q in Q.items():
    d = json.load(urllib.request.urlopen(B + q))
    dims, size = d["id"], d["size"]
    idx = [{v: k for k, v in d["dimension"][n]["category"]["index"].items()} for n in dims]
    for pos, val in d["value"].items():
        pos = int(pos); coords = []
        for s in reversed(size):
            coords.append(pos % s); pos //= s
        coords = coords[::-1]
        c = {n: idx[i][coords[i]] for i, n in enumerate(dims)}
        item = c.get("src_crf") or c.get("na_item")
        unit = c.get("unit", "THS_PER")
        out.append([ds, c["geo"], item, unit, c["time"], val, d.get("status", {}).get(str(int(list(d["value"]).index(str(int(pos)))) ) , "") if False else "", d["updated"], B + q])
    # flags
    for k, f in d.get("status", {}).items():
        pos = int(k); coords = []
        for s in reversed(size):
            coords.append(pos % s); pos //= s
        coords = coords[::-1]
        c = {n: idx[i][coords[i]] for i, n in enumerate(dims)}
        for r in out:
            if r[0] == ds and r[1] == c["geo"] and r[4] == c["time"] and r[2] == (c.get("src_crf") or c.get("na_item")) and r[3] == c.get("unit", "THS_PER"):
                r[6] = f
with open(ROOT / "data/cc-025/eurostat_gdp_ghg_pop.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["dataset","geo","item","unit","year","value","flag","eurostat_updated","query_url","retrieved"])
    for r in sorted(out): w.writerow(r + [datetime.date.today().isoformat()])
print(len(out), "rows")
