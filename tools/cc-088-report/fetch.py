#!/usr/bin/env python3
"""CC-088: fetch Eurostat demo_gind (Malta, since 2015) and demo_r_d3dens (Malta) -> data/cc-088/."""
import csv, datetime, json, pathlib, urllib.request
ROOT = pathlib.Path(__file__).resolve().parents[2]
B = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
today = datetime.date.today().isoformat()


def get(url, fields):
    d = json.load(urllib.request.urlopen(url))
    dims, size = d["id"], d["size"]
    idx = [{v: k for k, v in d["dimension"][n]["category"]["index"].items()} for n in dims]
    rows = []
    for k, val in d["value"].items():
        pos, out = int(k), []
        for s in reversed(size):
            out.append(pos % s); pos //= s
        c = {n: idx[i][x] for i, (n, x) in enumerate(zip(dims, out[::-1]))}
        rows.append([c[f] for f in fields] + [c["time"], val, d.get("status", {}).get(k, ""), d["updated"], url, today])
    return sorted(rows)


u1 = B + ("demo_gind?geo=MT&indic_de=JAN&indic_de=LBIRTH&indic_de=DEATH&indic_de=NATGROW&indic_de=CNMIGRAT&indic_de=GROW"
          "&sinceTimePeriod=2015&format=JSON&lang=en")
u2 = B + "demo_r_d3dens?geo=MT&sinceTimePeriod=2015&format=JSON&lang=en"
for name, u, f in [("eurostat_demo_gind.csv", u1, ["geo", "indic_de"]), ("eurostat_demo_r_d3dens.csv", u2, ["geo"])]:
    rows = get(u, f)
    with open(ROOT / "data/cc-088" / name, "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(f + ["year", "value", "flag", "eurostat_updated", "query_url", "retrieved"]); w.writerows(rows)
    print(name, len(rows))
