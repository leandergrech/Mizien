#!/usr/bin/env python3
"""CC-022 v1.2: fetch the Eurostat inputs for testing 'burden' against income and use, not price alone.

Writes data/cc-022/eurostat_burden_inputs.csv (long format, one row per value, with the Eurostat status flag
and the query URL). All EU-27 Member States plus the EU-27 aggregate. Network needed.

Series (codes as queried):
  price       nrg_pc_204    household electricity price, all taxes and levies (I_TAX), EUR per kWh, bands DA-DE and the
                            all-band average (TOT_KWH), 2024-S1 to 2025-S2
  volume      nrg_pc_204_v  share of household electricity consumption by band (PC), 2024 and 2025
  income      ilc_di03      mean and median equivalised net income (MEAN_EI, MED_EI), EUR, EU-SILC 2024 and 2025
  quintile    ilc_di01      top cut-off of the first income quintile (QU1, TC) and its income share (SHARE), EUR,
                            EU-SILC 2024 and 2025
  use         nrg_d_hhq     final electricity consumption of households, energy use (FC_OTH_HH_E, E7000), GWh, 2023-2024
  enduse      nrg_d_hhq     the same by end use (space heating, cooling, water heating, cooking, lighting and appliances,
                            other), Malta and EU-27, 2024
  households  lfst_hhnhtych number of private households (all compositions), thousand, 2023-2024 (EU Labour Force Survey)
  hhincome    nasa_10_nf_tr gross disposable income (B6G) of households and NPISH (S14_S15), resources (RECV),
                            million EUR, current prices, 2023-2024
  spending    hbs_str_t211  structure of consumption expenditure, electricity (CP0451), per mille, 2020 (latest)
  warm        ilc_mdes01    inability to keep home adequately warm, % of people, total and below 60% of median
                            income, 2024-2025
  arrears     ilc_mdes07    arrears on utility bills, % of people, same breakdowns, 2024-2025
  cool        ilc_hcmp03    dwelling not comfortably cool in summer, % of people, total and first quintile, 2012 (the only
                            year Eurostat publishes; the 2023 housing module has no summer-cooling table)
"""
import csv, datetime, json, pathlib, urllib.request

D = pathlib.Path(__file__).resolve().parents[2] / "data" / "cc-022"
B = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
EU = "AT BE BG CY CZ DE DK EE EL ES FI FR HR HU IE IT LT LU LV MT NL PL PT RO SE SI SK".split()
GEO = "&".join(f"geo={g}" for g in EU + ["EU27_2020"])
BANDS = "&".join(f"nrg_cons={b}" for b in ("KWH_LT1000", "KWH1000-2499", "KWH2500-4999", "KWH5000-14999",
                                            "KWH_GE15000", "TOT_KWH"))
Q = {
    "price": f"nrg_pc_204?{GEO}&tax=I_TAX&unit=KWH&currency=EUR&{BANDS}"
             "&time=2024-S1&time=2024-S2&time=2025-S1&time=2025-S2",
    "volume": f"nrg_pc_204_v?{GEO}&time=2024&time=2025",
    "income": f"ilc_di03?{GEO}&age=TOTAL&sex=T&unit=EUR&statinfo=MED_EI&statinfo=MEAN_EI&time=2024&time=2025",
    "quintile": f"ilc_di01?{GEO}&unit=EUR&quant_inc=QU1&statinfo=TC&statinfo=SHARE&time=2024&time=2025",
    "use": f"nrg_d_hhq?{GEO}&siec=E7000&nrg_bal=FC_OTH_HH_E&unit=GWH&time=2023&time=2024",
    "enduse": "nrg_d_hhq?geo=MT&geo=EU27_2020&siec=E7000&unit=GWH&time=2024" + "".join(
        f"&nrg_bal={x}" for x in ("FC_OTH_HH_E", "FC_OTH_HH_E_SH", "FC_OTH_HH_E_SC", "FC_OTH_HH_E_WH", "FC_OTH_HH_E_CK",
                                  "FC_OTH_HH_E_LE", "FC_OTH_HH_E_OE")),
    "households": f"lfst_hhnhtych?{GEO}&phhcomp=TOTAL&n_child=TOTAL&agechild=TOTAL&unit=THS_HH&time=2023&time=2024",
    "hhincome": f"nasa_10_nf_tr?{GEO}&na_item=B6G&sector=S14_S15&direct=RECV&unit=CP_MEUR&time=2023&time=2024",
    "spending": f"hbs_str_t211?{GEO}&coicop=CP0451&unit=PM&time=2020",
    "warm": f"ilc_mdes01?{GEO}&hhcomp=TOTAL&rskpovth=TOTAL&rskpovth=B_60&unit=PC&time=2024&time=2025",
    "arrears": f"ilc_mdes07?{GEO}&hhcomp=TOTAL&rskpovth=TOTAL&rskpovth=B_60&unit=PC&time=2024&time=2025",
    "cool": f"ilc_hcmp03?{GEO}&unit=PC&deg_urb=TOTAL&quant_inc=TOTAL&quant_inc=QU1&time=2012",
}
KEEP = ("nrg_cons", "statinfo", "quant_inc", "rskpovth", "coicop", "nrg_bal")  # dimensions that vary within a series


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
        item = "|".join(f"{k}={r[k]}" for k in KEEP if k in r)
        rows.append({"series": series, "dataset": q.split("?")[0], "item": item, "geo": r["geo"], "time": r["time"],
                     "value": r["value"], "flag": r["flag"], "eurostat_updated": upd, "retrieved": today,
                     "query_url": B + q})
    print(f"{series:11s} {len(data):4d} values")
rows.sort(key=lambda r: (r["series"], r["item"], r["geo"], r["time"]))
with open(D / "eurostat_burden_inputs.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\r\n")
    w.writeheader()
    w.writerows(rows)
print(len(rows), "rows;", sum(1 for r in rows if r["flag"]), "with a status flag")
