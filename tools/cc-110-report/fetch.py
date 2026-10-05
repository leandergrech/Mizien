#!/usr/bin/env python3
"""CC-110: fetch Eurostat new passenger cars (road_eqr_carpda) and the passenger-car stock (road_eqs_carpda) by type
of motor energy, for every member state and the EU-27 -> data/cc-110/*.csv (with flags, query URL, retrieval date)."""
import csv, datetime, json, pathlib, urllib.request
ROOT = pathlib.Path(__file__).resolve().parents[2]
B = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
GEOS = "EU27_2020 AT BE BG CY CZ DE DK EE EL ES FI FR HR HU IE IT LT LU LV MT NL PL PT RO SE SI SK".split()
Q = {"road_eqr_carpda": "road_eqr_carpda?" + "&".join("geo=" + g for g in GEOS) + "&mot_nrg=TOTAL&mot_nrg=ELC&mot_nrg=HYD_FCELL&mot_nrg=ELC_PET_PI&mot_nrg=ELC_DIE_PI&sinceTimePeriod=2019",
     "road_eqs_carpda": "road_eqs_carpda?geo=MT&geo=EU27_2020&mot_nrg=TOTAL&mot_nrg=ELC&mot_nrg=HYD_FCELL&sinceTimePeriod=2019"}
today = datetime.date.today().isoformat()
for ds, q in Q.items():
    d = json.load(urllib.request.urlopen(B + q))
    dims, size = d["id"], d["size"]
    idx = [{v: k for k, v in d["dimension"][n]["category"]["index"].items()} for n in dims]
    rows = []
    for k, val in d["value"].items():
        pos, out = int(k), []
        for s in reversed(size):
            out.append(pos % s); pos //= s
        c = {n: idx[i][x] for i, (n, x) in enumerate(zip(dims, out[::-1]))}
        rows.append([c["geo"], c["mot_nrg"], c.get("unit", "NR"), c["time"], val, d.get("status", {}).get(k, ""), d["updated"], B + q, today])
    with open(ROOT / f"data/cc-110/eurostat_{ds}.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["geo", "mot_nrg", "unit", "year", "value", "flag", "eurostat_updated", "query_url", "retrieved"])
        w.writerows(sorted(rows))
    print(ds, len(rows), d["updated"])
