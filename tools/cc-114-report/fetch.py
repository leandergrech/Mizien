#!/usr/bin/env python3
"""CC-114: fetch the Eurostat series behind "Malta is the only EU Member State whose greenhouse gas emissions
intensity rose since 2013" -> data/cc-114/eurostat_extract.csv (one row per value, with its status flag) and
data/cc-114/eurostat_queries.csv (per dataset: label, Eurostat's 'updated' stamp, the query URL and the retrieval
date). Needs network.

Datasets (labels as Eurostat gives them):
  env_ac_aeint_r2  Air emissions intensities by NACE Rev. 2 activity (the indicator Eurostat's news item of
                   23 Jan 2026 cites; residence principle, households excluded)
  env_ac_ainah_r2  Air emissions accounts by NACE Rev. 2 activity (thousand tonnes, residence principle)
  env_ac_aibrid_r2 Air emissions accounts totals bridging to emission inventory totals (Malta and EU-27)
  env_air_gge      Greenhouse gas emissions by source sector (inventory, territory principle; Mt CO2e)
  nama_10_gdp      GDP, chain-linked volumes (2020) and current prices
  nama_10_a64      Gross value added by NACE activity, chain-linked volumes (2020)
  nama_10_pe       Population (national accounts concept)
  nrg_ind_ren      Share of energy from renewable sources (overall and electricity)
"""
import csv
import datetime
import json
import pathlib
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "cc-114" / "eurostat_extract.csv"
QOUT = ROOT / "data" / "cc-114" / "eurostat_queries.csv"
B = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
EU27 = "BE BG CZ DK DE EE IE EL ES FR HR IT CY LV LT LU HU MT NL AT PL PT RO SI SK FI SE".split()
G = "&".join("geo=" + g for g in EU27 + ["EU27_2020"])
NACE = "&".join("nace_r2=" + n for n in ["TOTAL", "TOTAL_HH", "HH", "A", "B", "C", "D", "E", "F", "H", "H49", "H50",
                                         "H51", "G-U_X_H"])
Q = {
    "env_ac_aeint_r2": f"env_ac_aeint_r2?{G}&airpol=GHG&nace_r2=TOTAL&na_item=B1G&unit=G_EUR_CLV20&unit=G_EUR_CP"
                       "&sinceTimePeriod=2008",
    "env_ac_ainah_r2": f"env_ac_ainah_r2?{G}&airpol=GHG&unit=THS_T&{NACE}&sinceTimePeriod=2008",
    "env_ac_aibrid_r2": "env_ac_aibrid_r2?geo=MT&geo=EU27_2020&airpol=GHG&unit=THS_T&sinceTimePeriod=2008",
    "env_air_gge": f"env_air_gge?{G}&unit=MIO_T&airpol=GHG&src_crf=TOTX4_MEMO&src_crf=CRF1D1A&src_crf=CRF1D1B"
                   "&sinceTimePeriod=2005",
    "nama_10_gdp": f"nama_10_gdp?{G}&na_item=B1GQ&unit=CLV20_MEUR&unit=CP_MEUR&sinceTimePeriod=2005",
    "nama_10_a64": f"nama_10_a64?{G}&na_item=B1G&unit=CLV20_MEUR&nace_r2=TOTAL&nace_r2=H&nace_r2=H51"
                   "&sinceTimePeriod=2008",
    "nama_10_pe": f"nama_10_pe?{G}&na_item=POP_NC&unit=THS_PER&sinceTimePeriod=2005",
    "nrg_ind_ren": f"nrg_ind_ren?{G}&nrg_bal=REN&nrg_bal=REN_ELC&unit=PC&sinceTimePeriod=2013",
}
SKIP = {"freq", "geo", "time", "unit"}
today = datetime.date.today().isoformat()
rows, meta = [], []
for ds, q in Q.items():
    d = json.load(urllib.request.urlopen(B + q))
    dims, size = d["id"], d["size"]
    idx = [{v: k for k, v in d["dimension"][n]["category"]["index"].items()} for n in dims]
    status = d.get("status", {})
    for pos, val in d["value"].items():
        p = int(pos)
        coords = []
        for s in reversed(size):
            coords.append(p % s)
            p //= s
        coords = coords[::-1]
        c = {n: idx[i][coords[i]] for i, n in enumerate(dims)}
        item = "|".join(c[n] for n in dims if n not in SKIP)
        rows.append([ds, c["geo"], item, c.get("unit", ""), c["time"], val, status.get(pos, "")])
    flags = d.get("extension", {}).get("status", {}).get("label", {})
    meta.append([ds, d["label"], d["updated"], "; ".join(f"{k} = {v}" for k, v in flags.items()), B + q, today])
    print(ds, d["label"], d["updated"], len(d["value"]), "values")
rows.sort(key=lambda r: (r[0], r[1], r[2], r[3], r[4]))
with open(OUT, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["dataset", "geo", "item", "unit", "year", "value", "flag"])
    w.writerows(rows)
with open(QOUT, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["dataset", "label", "eurostat_updated", "flag_labels", "query_url", "retrieved"])
    w.writerows(meta)
print(len(rows), "rows ->", OUT.relative_to(ROOT), "; queries ->", QOUT.relative_to(ROOT))

# The January 2026 vintage: Eurostat's map "Greenhouse gas emissions intensity of gross value added, 2013-2024"
# (% change, grams per euro in chain-linked volumes 2020), embedded in the news item of 23 Jan 2026 and reproduced in
# the PN's release. The map file carries its data as a JavaScript object `data:{BE:-27.6,...}`.
import re  # noqa: E402

MAP = ("https://ec.europa.eu/eurostat/documents/4187653/22762673/greenhouse-gas-emissions-intensity-2013-2024.html/"
       "98651795-bcd1-3b5a-b273-7da9727ee5f3?t=1768906967687")
req = urllib.request.Request(MAP, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                                           "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"})
html = urllib.request.urlopen(req).read().decode("utf-8", "replace")
block = re.search(r"data:\{(BE:[^}]*)\}", html).group(1)
vals = dict(re.findall(r'([A-Z]{2}):"?(-?[0-9.]+|:)"?', block))
eu = re.search(r"EU = (-?[0-9.]+)%", html)
with open(ROOT / "data" / "cc-114" / "eurostat_map_jan2026.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["geo", "change_2013_2024_pct", "source", "map_timestamp", "url", "retrieved"])
    for g in EU27 + ["NO"]:
        w.writerow([g, vals.get(g, ""), "Eurostat map in news item ddn-20260123-1 (env_ac_aeint_r2)",
                    "t=1768906967687 (20 Jan 2026)", MAP, today])
    w.writerow(["EU27_2020", eu.group(1) if eu else "", "Eurostat map legend, 'EU = ...%'",
                "t=1768906967687 (20 Jan 2026)", MAP, today])
print("map values:", {g: vals.get(g) for g in ("MT", "EE", "IE", "FI")}, "EU", eu.group(1) if eu else None)
