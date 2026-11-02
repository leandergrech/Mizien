#!/usr/bin/env python3
"""CC-147: download the Eurostat series used (network) -> data/cc-147/eurostat_aea.csv. Retrieved 2 Nov 2026."""
import csv, json, pathlib, urllib.request
ROOT = pathlib.Path(__file__).resolve().parents[2]
B = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
Q = [("env_ac_ainah_r2", "airpol=GHG&unit=THS_T&geo=MT&geo=EU27_2020&sinceTimePeriod=2008", ("TOTAL", "TOTAL_HH", "H49", "H50", "H51", "H52", "H53")),
     ("nama_10_a64", "unit=CLV20_MEUR&na_item=B1G&geo=MT&geo=EU27_2020&sinceTimePeriod=2008", ("TOTAL", "H50", "H51")),
     ("nama_10_a64", "unit=CP_MEUR&na_item=B1G&geo=MT&geo=EU27_2020&sinceTimePeriod=2008", ("TOTAL", "H50", "H51")),
     ("env_ac_aibrid_r2", "airpol=GHG&unit=THS_T&geo=MT&sinceTimePeriod=2008", ("AEMIS_RES", "AEMIS_TER", "AEMIS_RES_ABR_ATR", "AEMIS_RES_ABR_WTR"))]
rows = []
for ds, q, keep in Q:
    d = json.load(urllib.request.urlopen(f"{B}{ds}?format=JSON&lang=en&{q}", timeout=90))
    ids, dims = d["id"], d["dimension"]
    idx = {k: list(dims[k]["category"]["index"]) for k in ids}
    for pos, v in d["value"].items():
        p, c = int(pos), []
        for s in reversed(d["size"]):
            c.append(p % s); p //= s
        m = dict(zip(ids, [idx[k][i] for k, i in zip(ids, reversed(c))]))
        item = m.get("nace_r2") or m.get("indic_env")
        if item in keep:
            rows.append({"dataset": ds, "unit": m["unit"], "item": item, "geo": m["geo"], "year": m["time"], "value": v,
                         "flag": d.get("status", {}).get(pos, ""), "updated": d["updated"]})
rows.sort(key=lambda r: (r["dataset"], r["unit"], r["item"], r["geo"], r["year"]))
with open(ROOT / "data/cc-147/eurostat_aea.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(len(rows), "rows")
