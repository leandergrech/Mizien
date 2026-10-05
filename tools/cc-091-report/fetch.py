#!/usr/bin/env python3
"""CC-091: fetch Eurostat fatal accidents at work (hsw_n2_02, Malta) and employment (nama_10_pe, Malta) ->
data/cc-091/eurostat_*.csv with flags, query URL and retrieval date. Needs network."""
import csv, datetime, json, pathlib, urllib.request
ROOT = pathlib.Path(__file__).resolve().parents[2]
B = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
Q = {"eurostat_hsw_n2_02.csv": B + "hsw_n2_02?geo=MT&nace_r2=TOTAL&nace_r2=F&sinceTimePeriod=2015&lang=en",
     "eurostat_nama_10_pe.csv": B + "nama_10_pe?geo=MT&na_item=EMP_DC&unit=THS_PER&sinceTimePeriod=2015&lang=en"}


def rows(d):
    dims, size = d["id"], d["size"]
    idx = [{v: k for k, v in d["dimension"][n]["category"]["index"].items()} for n in dims]
    for k, val in d["value"].items():
        pos, out = int(k), []
        for s in reversed(size):
            out.append(pos % s); pos //= s
        yield {n: idx[i][c] for i, (n, c) in enumerate(zip(dims, out[::-1]))}, val, d.get("status", {}).get(k, "")


today = datetime.date.today().isoformat()
for name, url in Q.items():
    d = json.load(urllib.request.urlopen(url))
    with open(ROOT / "data/cc-091" / name, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["dataset", "unit", "nace_r2", "geo", "year", "value", "flag", "eurostat_updated", "query_url", "retrieved"])
        for c, v, fl in sorted(rows(d), key=lambda r: (r[0].get("unit", ""), r[0].get("nace_r2", ""), r[0]["time"])):
            w.writerow([name[9:-4], c.get("unit", ""), c.get("nace_r2", ""), c["geo"], c["time"], v, fl, d["updated"], url, today])
    print(name, "ok", d["updated"])
