#!/usr/bin/env python3
"""CC-022: fetch Eurostat household electricity prices (nrg_pc_204, band DC, all taxes; EUR and PPS per kWh) for all
countries, 2019-2025, and energy-poverty indicators (ilc_mdes01 unable to keep home warm, ilc_mdes07 arrears on utility
bills). Writes data/cc-022/eurostat_prices.csv and eurostat_poverty.csv. Network needed.

Added for v1.1 (5 Oct 2026): eurostat_prices_bands.csv (PPS per kWh in every consumption band, 2024-S2 and 2025-S2,
all countries) and eurostat_prices_mt_history.csv (Malta and EU-27, band DC, EUR per kWh, 2012-S1 to 2025-S2), both
with Eurostat status flags."""
import csv, json, pathlib, urllib.request

D = pathlib.Path(__file__).resolve().parents[2] / "data" / "cc-022"
B = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"


def get(q):
    d = json.load(urllib.request.urlopen(B + q, timeout=180))
    ids, sizes = d["id"], d["size"]
    cats = {k: {i: c for c, i in d["dimension"][k]["category"]["index"].items()} for k in ids}
    out = []
    for k, v in d["value"].items():
        k0 = k
        k, pos = int(k), {}
        for dim, n in zip(reversed(ids), reversed(sizes)):
            pos[dim] = cats[dim][k % n]
            k //= n
        pos["value"] = v
        pos["flag"] = d.get("status", {}).get(str(k0), "")
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
bands = get("nrg_pc_204?tax=I_TAX&unit=KWH&currency=PPS&time=2024-S2&time=2025-S2"
             "&nrg_cons=KWH_LT1000&nrg_cons=KWH1000-2499&nrg_cons=KWH2500-4999&nrg_cons=KWH5000-14999"
             "&nrg_cons=KWH_GE15000&nrg_cons=TOT_KWH")
write("eurostat_prices_bands.csv", bands, ["currency", "nrg_cons", "geo", "time", "value", "flag"])
hist = get("nrg_pc_204?geo=MT&geo=EU27_2020&nrg_cons=KWH2500-4999&tax=I_TAX&unit=KWH&currency=EUR"
           "&sinceTimePeriod=2012-S1")
write("eurostat_prices_mt_history.csv", hist, ["currency", "geo", "time", "value", "flag"])
print(len(p), "price rows;", len(pv), "poverty rows;", len(bands), "band rows;", len(hist), "history rows")
