#!/usr/bin/env python3
"""CC-013 v1.2: fetch population, real house prices, rents and the latest quarterly house prices for every EU-27
Member State, so Malta can be compared with all 27 rather than with the EU aggregate alone.

Writes data/cc-013/eurostat_eu27_pop_prices_rents.csv (long format, Eurostat status flag per value, query URL).
The older eurostat_housing.csv (Malta and EU-27 only; also read by CC-018) is not touched. Network needed.

Series (codes as queried):
  pop      demo_gind     population on 1 January (JAN), 2015 and 2025
  real     tipsho10      house price index deflated by HICP, annual average, 2015 = 100 (I15_A_AVG), 2015 and 2025
  rent     prc_hicp_aind HICP actual rentals for housing (CP041), annual average index (INX_A_AVG), 2015 and 2025
  hpi_q    prc_hpi_q     house price index, all dwellings (TOTAL), annual rate of change (RCH_A), 2025-Q2 to 2026-Q2
  weight   prc_hpi_cow   country weights in the EU-27 house price index (COWEU27_2020, TOTAL, per mille), 2025
"""
import csv, datetime, json, pathlib, urllib.request

D = pathlib.Path(__file__).resolve().parents[2] / "data" / "cc-013"
B = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
EU = "AT BE BG CY CZ DE DK EE EL ES FI FR HR HU IE IT LT LU LV MT NL PL PT RO SE SI SK".split()
GEO = "&".join(f"geo={g}" for g in EU + ["EU27_2020"])
Q = {
    "pop": f"demo_gind?{GEO}&indic_de=JAN&time=2015&time=2025",
    "real": f"tipsho10?{GEO}&unit=I15_A_AVG&time=2015&time=2025",
    "rent": f"prc_hicp_aind?{GEO}&coicop=CP041&unit=INX_A_AVG&time=2015&time=2025",
    "hpi_q": f"prc_hpi_q?{GEO}&purchase=TOTAL&unit=RCH_A"
             "&time=2025-Q2&time=2025-Q3&time=2025-Q4&time=2026-Q1&time=2026-Q2",
    "weight": f"prc_hpi_cow?{GEO}&purchase=TOTAL&statinfo=COWEU27_2020&unit=PM&time=2025",
}


def get(q):
    d = json.load(urllib.request.urlopen(B + q, timeout=240))
    ids, sizes = d["id"], d["size"]
    cats = {k: {i: c for c, i in d["dimension"][k]["category"]["index"].items()} for k in ids}
    out = []
    for k, v in d["value"].items():
        n, pos = int(k), {}
        for dim, s in zip(reversed(ids), reversed(sizes)):
            pos[dim] = cats[dim][n % s]
            n //= s
        pos["value"], pos["flag"] = v, d.get("status", {}).get(k, "")
        out.append(pos)
    return out, d.get("updated", "")


rows, today = [], datetime.date.today().isoformat()
for series, q in Q.items():
    data, upd = get(q)
    for r in data:
        rows.append({"series": series, "dataset": q.split("?")[0], "geo": r["geo"], "time": r["time"],
                     "value": r["value"], "flag": r["flag"], "eurostat_updated": upd, "retrieved": today,
                     "query_url": B + q})
    print(f"{series:7s} {len(data):4d} values")
rows.sort(key=lambda r: (r["series"], r["geo"], r["time"]))
with open(D / "eurostat_eu27_pop_prices_rents.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
print(len(rows), "rows;", sum(1 for r in rows if r["flag"]), "with a status flag")
