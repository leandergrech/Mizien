#!/usr/bin/env python3
"""CC-111: fetch Eurostat municipal waste by waste management operations (env_wasmun), kg per person, Malta and the
EU-27 -> data/cc-111/eurostat_env_wasmun.csv (with status flags, the query URL and the retrieval date). Needs network."""
import csv, datetime, json, pathlib, urllib.request
ROOT = pathlib.Path(__file__).resolve().parents[2]
B = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/env_wasmun?"
URL = B + "geo=MT&geo=EU27_2020&unit=KG_HAB&unit=THS_T&sinceTimePeriod=2012"
# every member state, for the rankings (generation and landfill, 2023-2024)
EU27 = "AT BE BG CY CZ DE DK EE EL ES FI FR HR HU IE IT LT LU LV MT NL PL PT RO SE SI SK".split()
URL_ALL = B + "&".join("geo=" + g for g in EU27) + "&unit=KG_HAB&wst_oper=GEN&wst_oper=DSP_L_OTH&sinceTimePeriod=2023"


def rows(d):
    dims, size = d["id"], d["size"]
    idx = [{v: k for k, v in d["dimension"][n]["category"]["index"].items()} for n in dims]
    def coords(pos):
        out = []
        for s in reversed(size):
            out.append(pos % s); pos //= s
        return {n: idx[i][c] for i, (n, c) in enumerate(zip(dims, out[::-1]))}
    for k, val in d["value"].items():
        yield coords(int(k)), val, d.get("status", {}).get(k, "")


today = datetime.date.today().isoformat()
for url, name in ((URL, "eurostat_env_wasmun.csv"), (URL_ALL, "eurostat_env_wasmun_eu27_2023_2024.csv")):
    d = json.load(urllib.request.urlopen(url))
    with open(ROOT / "data/cc-111" / name, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["geo", "wst_oper", "unit", "year", "value", "flag", "eurostat_updated", "query_url", "retrieved"])
        for c, v, fl in sorted(rows(d), key=lambda r: (r[0]["geo"], r[0]["wst_oper"], r[0]["unit"], r[0]["time"])):
            w.writerow([c["geo"], c["wst_oper"], c["unit"], c["time"], v, fl, d["updated"], url, today])
    print(name, "ok", d["updated"])
