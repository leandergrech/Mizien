#!/usr/bin/env python3
"""CC-119: fetch the Eurostat series behind the Council's statement on Malta's renewables (recital 25, draft Council
Recommendation, 3 Jul 2026) -> data/cc-119/eurostat_extract.csv and eurostat_queries.csv. Needs network.

  nrg_ind_ren   Share of energy from renewable sources (REN overall; REN_ELC electricity), % (SHARES method)
  nrg_cb_pem    Net electricity generation by type of fuel, monthly (GWh): domestic generation shares, all Member States
  nrg_cb_e      Electricity supply (GWh): gross production, imports, exports, final consumption
  nrg_bal_peh   Production of electricity and derived heat by type of fuel (GWh), Malta and EU-27
  nrg_ind_ren is also fetched for all Member States for the 'below the EU average' check.
"""
import csv, datetime, json, pathlib, urllib.request
ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-119"
B = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
EU27 = "BE BG CZ DK DE EE IE EL ES FR HR IT CY LV LT LU HU MT NL AT PL PT RO SI SK FI SE".split()
G = "&".join("geo=" + g for g in EU27 + ["EU27_2020"])
Q = {
    "nrg_ind_ren": f"nrg_ind_ren?{G}&nrg_bal=REN&nrg_bal=REN_ELC&unit=PC&sinceTimePeriod=2013",
    "nrg_cb_pem": f"nrg_cb_pem?{G}&unit=GWH&sinceTimePeriod=2024-01&untilTimePeriod=2025-12"
                  "&siec=TOTAL&siec=RA000&siec=RA100&siec=RA300&siec=RA420&siec=CF_R",
    "nrg_cb_e": "nrg_cb_e?geo=MT&geo=EU27_2020&siec=E7000&nrg_bal=IMP&nrg_bal=EXP&nrg_bal=GEP&nrg_bal=FC&sinceTimePeriod=2013",
    "nrg_bal_peh": "nrg_bal_peh?geo=MT&geo=EU27_2020&unit=GWH&nrg_bal=GEP&sinceTimePeriod=2013"
                   + "".join("&siec=" + s for s in ["TOTAL", "RA000", "RA100", "RA200", "RA300", "RA400", "RA410", "RA420",
                                                    "R5000", "R5110-5150_W6000RI", "R5300", "R5160", "R5210P", "R5220P", "R5230P",
                                                    "W6100_6220", "RA500", "RA600", "N900H", "C0000X0350-0370", "G3000", "O4000XBIO"]),
}
SKIP = {"freq", "geo", "time", "unit"}
today = datetime.date.today().isoformat()
rows, meta = [], []
for ds, q in Q.items():
    try:
        d = json.load(urllib.request.urlopen(B + q))
    except Exception as e:
        print(ds, "FAILED", e); continue
    dims, size = d["id"], d["size"]
    idx = [{v: k for k, v in d["dimension"][n]["category"]["index"].items()} for n in dims]
    status = d.get("status", {})
    for pos, val in d["value"].items():
        p = int(pos); coords = []
        for s in reversed(size):
            coords.append(p % s); p //= s
        coords = coords[::-1]
        c = {n: idx[i][coords[i]] for i, n in enumerate(dims)}
        item = "|".join(c[n] for n in dims if n not in SKIP)
        rows.append([ds, c["geo"], item, c.get("unit", ""), c["time"], val, status.get(pos, "")])
    flags = d.get("extension", {}).get("status", {}).get("label", {})
    meta.append([ds, d["label"], d["updated"], "; ".join(f"{k} = {v}" for k, v in flags.items()), B + q, today])
    print(ds, d["label"], d["updated"], len(d["value"]), "values")
rows.sort(key=lambda r: (r[0], r[1], r[2], r[3], r[4]))
with open(D / "eurostat_extract.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["dataset", "geo", "item", "unit", "year", "value", "flag"]); w.writerows(rows)
with open(D / "eurostat_queries.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["dataset", "label", "updated", "flags", "url", "retrieved"]); w.writerows(meta)
