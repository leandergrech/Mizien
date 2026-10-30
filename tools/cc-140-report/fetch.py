#!/usr/bin/env python3
"""CC-140: download Eurostat nrg_ind_id (energy import dependency, % , TOTAL) and nrg_bal_c (Malta, ktoe) to data/cc-140/."""
import csv, json, pathlib, urllib.request, datetime
ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-140"
D.mkdir(exist_ok=True)
API = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
YEARS = range(2015, 2026)


def get(code, q):
    with urllib.request.urlopen(API + code + "?format=JSON&lang=en&" + q, timeout=90) as r:
        return json.load(r)


def rows(d):
    ids, sz = d["id"], d["size"]
    cats = [list(d["dimension"][k]["category"]["index"]) for k in ids]
    for i, v in d["value"].items():
        i = int(i); idx = []
        for s in reversed(sz):
            idx.append(i % s); i //= s
        idx.reverse()
        yield {k: cats[j][idx[j]] for j, k in enumerate(ids)}, v, d["updated"]


d = get("nrg_ind_id", "siec=TOTAL&unit=PC&" + "&".join(f"time={y}" for y in YEARS))
with open(D / "eurostat_nrg_ind_id.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["geo", "year", "value_pc", "dataset_updated", "retrieved"])
    for k, v, u in rows(d):
        w.writerow([k["geo"], k["time"], v, u[:10], datetime.date.today().isoformat()])
d = get("nrg_bal_c", "geo=MT&unit=KTOE&siec=TOTAL&nrg_bal=IMP&nrg_bal=EXP&nrg_bal=GAE&nrg_bal=INTMARB&" + "&".join(f"time={y}" for y in YEARS))
with open(D / "eurostat_nrg_bal_c_MT.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["balance", "year", "value_ktoe", "dataset_updated", "retrieved"])
    for k, v, u in rows(d):
        w.writerow([k["nrg_bal"], k["time"], v, u[:10], datetime.date.today().isoformat()])
