#!/usr/bin/env python3
"""CC-003 v1.2: fetch greenhouse-gas totals and population for every EU-27 Member State, 2005 and 2024, so that
Malta's per-person and total cuts can be ranked against all 27.

- env_air_gge, src_crf TOTX4_MEMO (total excluding LULUCF and international bunkers, the series calc.py already
  uses for Malta and the EU), unit MIO_T, airpol GHG;
- nama_10_pe, na_item POP_NC (total population, national concept, annual average), unit THS_PER.

Writes data/cc-003/eurostat_ghg_pop_eu27.csv with the Eurostat status flag of every value (p provisional,
b break in series, e estimated; empty = none) and the query URL. Network needed. The older file
eurostat_ghg_population.csv (Malta and EU-27 only, all years) is left as it is."""
import csv, datetime, json, pathlib, urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-003"
B = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
EU = "AT BE BG CY CZ DE DK EE EL ES FI FR HR HU IE IT LT LU LV MT NL PL PT RO SE SI SK".split()
GEO = "&".join(f"geo={g}" for g in EU + ["EU27_2020"])
YRS = "&time=2005&time=2024"
Q = {
    "env_air_gge": f"env_air_gge?{GEO}&unit=MIO_T&airpol=GHG&src_crf=TOTX4_MEMO{YRS}",
    "nama_10_pe": f"nama_10_pe?{GEO}&unit=THS_PER&na_item=POP_NC{YRS}",
}


def get(q):
    d = json.load(urllib.request.urlopen(B + q, timeout=180))
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


rows = []
today = datetime.date.today().isoformat()
for ds, q in Q.items():
    data, upd = get(q)
    for r in data:
        rows.append({"dataset": ds, "geo": r["geo"], "item": r.get("src_crf") or r.get("na_item"),
                     "year": r["time"], "value": r["value"], "flag": r["flag"],
                     "unit": "Mt CO2e" if ds == "env_air_gge" else "thousand persons",
                     "eurostat_updated": upd, "retrieved": today, "query_url": B + q})
rows.sort(key=lambda r: (r["dataset"], r["geo"], r["year"]))
with open(D / "eurostat_ghg_pop_eu27.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
print(len(rows), "rows;", sum(1 for r in rows if r["flag"]), "with a status flag")
