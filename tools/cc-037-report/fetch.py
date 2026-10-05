#!/usr/bin/env python3
"""CC-037: download Eurostat data into data/cc-037/ (JSON-stat -> CSV), keeping Eurostat's flags.

- ilc_mddw02 (pollution, grime or other environmental problems), all countries and years, all-household total.
- ilc_li02 (at-risk-of-poverty rate, 60% of median equivalised income), Malta and EU-27, all ages, both sexes:
  the size of the "below 60%" group that ilc_mddw02 compares with the rest of the population.

The `flag` column holds Eurostat's observation status: e = estimated, u = low reliability, b = break in time
series, bu = break and low reliability, n = not significant (labels from the API's extension.status).
"""
import csv, json, pathlib, urllib.request, datetime
ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-037"
API = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/{}?format=JSON&lang=en{}"
D.mkdir(exist_ok=True)


def flat(ds, query=""):
    d = json.load(urllib.request.urlopen(API.format(ds, query), timeout=90))
    dims, sz = d["id"], d["size"]
    # category positions come from the index values, not from the order of the keys
    cats = [[c for c, _ in sorted(d["dimension"][k]["category"]["index"].items(), key=lambda kv: kv[1])]
            for k in dims]
    status = d.get("status", {})
    rows = []
    for key, v in d["value"].items():
        n = int(key); pos = []
        for s in reversed(sz):
            pos.append(n % s); n //= s
        pos.reverse()
        rows.append({k: cats[i][p] for i, (k, p) in enumerate(zip(dims, pos))}
                    | {"value": v, "flag": status.get(key, "")})
    return rows, d.get("updated"), d.get("extension", {}).get("status", {}).get("label", {})


JOBS = (
    ("ilc_mddw02", "", "eurostat_ilc_mddw02.csv", lambda r: r["hhcomp"] == "TOTAL"),
    ("ilc_li02", "&geo=MT&geo=EU27_2020&statinfo=MED_EI&rskpovth=B_60&age=TOTAL&sex=T&unit=PC",
     "eurostat_ilc_li02.csv", lambda r: True),
)
for ds, query, out, keep in JOBS:
    rows, upd, labels = flat(ds, query)
    rows = [r for r in rows if keep(r)]
    for r in rows:
        r["dataset"], r["updated"], r["retrieved"] = ds, upd, datetime.date.today().isoformat()
    with open(D / out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    print(ds, len(rows), "rows, updated", upd, "flags:", labels)
