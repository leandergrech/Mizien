#!/usr/bin/env python3
"""CC-018 v1.2: fetch the Eurostat series for the release's further statements, with status flags.

GDP per head (nama_10_pc), house price index (prc_hpi_q, prc_hpi_a), household gross disposable income
(nasa_10_nf_tr, S14_S15, B6G) and population (nama_10_pe) for Malta (and the EU-27 where compared).
Writes data/cc-018/eurostat_more.csv (long format, one row per value; flag p = provisional, b = break,
e = estimated). Network needed (Eurostat dissemination API). tipsho60 is fetched by fetch_data.py.
"""
import csv, datetime, json, pathlib, urllib.request

OUT = pathlib.Path(__file__).resolve().parents[2] / "data" / "cc-018" / "eurostat_more.csv"
API = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
QUERIES = [
    ("nama_10_pc", "nama_10_pc?geo=MT&geo=EU27_2020&na_item=B1GQ&unit=CP_EUR_HAB&unit=CLV20_EUR_HAB"
                   "&unit=PC_EU27_2020_HAB_MPPS_CP&unit=PC_EU27_2020_HAB_MEUR_CP&sinceTimePeriod=2012"),
    ("prc_hpi_q", "prc_hpi_q?geo=MT&purchase=TOTAL&unit=I15_Q&unit=RCH_A&sinceTimePeriod=2015-Q1"),
    ("prc_hpi_a", "prc_hpi_a?geo=MT&purchase=TOTAL&unit=I15_A_AVG&unit=RCH_A_AVG&sinceTimePeriod=2015"),
    ("nasa_10_nf_tr", "nasa_10_nf_tr?geo=MT&sector=S14_S15&na_item=B6G&unit=CP_MEUR&direct=PAID"
                      "&sinceTimePeriod=2015"),
    ("nama_10_pe", "nama_10_pe?geo=MT&na_item=POP_NC&unit=THS_PER&sinceTimePeriod=2015"),
]
today = datetime.date.today().isoformat()
rows = []
for ds, q in QUERIES:
    d = json.load(urllib.request.urlopen(API + q, timeout=120))
    dims, sizes = d["id"], d["size"]
    cats = {k: {i: c for c, i in d["dimension"][k]["category"]["index"].items()} for k in dims}
    status = d.get("status", {})
    for k in sorted(set(d["value"]) | set(status), key=int):
        kk, pos = int(k), {}
        for dim, n in zip(reversed(dims), reversed(sizes)):
            pos[dim] = cats[dim][kk % n]
            kk //= n
        if d["value"].get(k) is None:
            continue
        rows.append({"dataset": ds, "unit": pos["unit"], "item": pos.get("na_item", pos.get("purchase", "")),
                     "geo": pos["geo"], "time": pos["time"], "value": d["value"][k], "flag": status.get(k, ""),
                     "source": API + q, "retrieved": today})
rows.sort(key=lambda r: (r["dataset"], r["unit"], r["geo"], r["time"]))
with open(OUT, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\r\n")
    w.writeheader()
    w.writerows(rows)
print(len(rows), "rows ->", OUT)
