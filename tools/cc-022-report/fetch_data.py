#!/usr/bin/env python3
"""CC-022: fetch Eurostat household electricity prices (nrg_pc_204, band DC, all taxes; EUR and PPS per kWh) for all
countries, 2019-2025, and energy-poverty indicators (ilc_mdes01 unable to keep home warm, ilc_mdes07 arrears on utility
bills). Writes data/cc-022/eurostat_prices.csv and eurostat_poverty.csv. Network needed."""
import csv, json, pathlib, urllib.request

D = pathlib.Path(__file__).resolve().parents[2] / "data" / "cc-022"
B = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"


def get(q):
    d = json.load(urllib.request.urlopen(B + q, timeout=180))
    ids, sizes = d["id"], d["size"]
    cats = {k: {i: c for c, i in d["dimension"][k]["category"]["index"].items()} for k in ids}
    out = []
    for k, v in d["value"].items():
        k, pos = int(k), {}
        for dim, n in zip(reversed(ids), reversed(sizes)):
            pos[dim] = cats[dim][k % n]
            k //= n
        pos["value"] = v
        out.append(pos)
    return out


def write(name, rows, keys):
    with open(D / name, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys, lineterminator="\r\n", extrasaction="ignore")
        w.writeheader()
        w.writerows(sorted(rows, key=lambda r: tuple(str(r[k]) for k in keys)))


times = "&".join(f"time={y}-S{s}" for y in range(2019, 2026) for s in (1, 2))
p = get(f"nrg_pc_204?nrg_cons=KWH2500-4999&tax=I_TAX&unit=KWH&currency=EUR&currency=PPS&{times}")
write("eurostat_prices.csv", p, ["currency", "geo", "time", "value"])
pv = []
for ds in ("ilc_mdes01", "ilc_mdes07"):
    for r in get(f"{ds}?hhcomp=TOTAL&rskpovth=TOTAL&unit=PC&sinceTimePeriod=2015&geo=MT&geo=EU27_2020"):
        r["dataset"] = ds
        pv.append(r)
write("eurostat_poverty.csv", pv, ["dataset", "geo", "time", "value"])
print(len(p), "price rows;", len(pv), "poverty rows")
