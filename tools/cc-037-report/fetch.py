#!/usr/bin/env python3
"""CC-037: download Eurostat ilc_mddw02 (pollution, grime) into data/cc-037/ (JSON-stat -> CSV)."""
import csv, json, pathlib, urllib.request, datetime
ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-037"
API = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/{}?format=JSON&lang=en"
D.mkdir(exist_ok=True)


def flat(ds):
    d = json.load(urllib.request.urlopen(API.format(ds), timeout=90))
    dims, sz = d["id"], d["size"]
    cats = [list(d["dimension"][k]["category"]["index"]) for k in dims]
    rows = []
    for n, v in d["value"].items():
        n = int(n); pos = []
        for s in reversed(sz):
            pos.append(n % s); n //= s
        pos.reverse()
        rows.append({k: cats[i][p] for i, (k, p) in enumerate(zip(dims, pos))} | {"value": v})
    return rows, d.get("updated")


for ds, out, keep in (("ilc_mddw02", "eurostat_ilc_mddw02.csv", lambda r: r["hhcomp"] == "TOTAL"),):
    rows, upd = flat(ds)
    rows = [r for r in rows if keep(r)]
    for r in rows:
        r["dataset"], r["updated"], r["retrieved"] = ds, upd, datetime.date.today().isoformat()
    with open(D / out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    print(ds, len(rows), "rows, updated", upd)
