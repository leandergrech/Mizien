#!/usr/bin/env python3
"""CC-117: fetch Eurostat inputs (Malta, EU-27 and other states) via the dissemination API.

Writes data/cc-117/eurostat_*.csv with Eurostat's flag, dataset update stamp, query URL and retrieval date.
"""
import csv, datetime as dt, json, pathlib, urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-117"
B = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
Q = {
    "eurostat_cei_wm011.csv": ("cei_wm011", "?wst_oper=RCY&unit=PC&sinceTimePeriod=2018"),
    "eurostat_env_waspac.csv": ("env_waspac", "?wst_oper=RCY&wst_oper=GEN&unit=PC&unit=RT_T2008&unit=T&sinceTimePeriod=2019"),
    "eurostat_env_wasmun.csv": ("env_wasmun", "?wst_oper=GEN&wst_oper=RCY&unit=THS_T&geo=MT&sinceTimePeriod=2018"),
}


def rows(j):
    ids, sizes = j["id"], j["size"]
    cats = [sorted(j["dimension"][d]["category"]["index"].items(), key=lambda kv: kv[1]) for d in ids]
    st = j.get("status", {})
    for k, v in j["value"].items():
        rem, codes = int(k), []
        for s in reversed(sizes):
            codes.append(rem % s); rem //= s
        codes.reverse()
        r = {d: cats[i][codes[i]][0] for i, d in enumerate(ids)}
        r.update(value=v, flag=st.get(k, ""))
        yield r


for fn, (ds, q) in Q.items():
    url = B + ds + q
    with urllib.request.urlopen(url, timeout=90) as r:
        j = json.load(r)
    out = sorted(rows(j), key=lambda r: tuple(r[d] for d in j["id"]))
    cols = [d for d in j["id"] if d != "freq"]
    with open(D / fn, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["dataset"] + cols + ["value", "flag", "eurostat_updated", "query_url", "retrieved"])
        for r in out:
            w.writerow([ds] + [r[c] for c in cols] + [r["value"], r["flag"], j["updated"], url, dt.date.today().isoformat()])
    print(fn, len(out), j["updated"])
