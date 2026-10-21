#!/usr/bin/env python3
"""CC-127: fetch the Eurostat series behind "Malta has the lowest proportion of organic farming in the EU".
Writes data/cc-127/*.csv (filtered copies; source URLs and retrieval date are in data/cc-127/README.md).
Needs outbound access to ec.europa.eu."""
import csv, io, json, pathlib, urllib.request
ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-127"
D.mkdir(exist_ok=True)
SDMX = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/{}?format=SDMX-CSV&lang=en"
JSON = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/{}?format=JSON&lang=en&{}"
EU27 = "AT BE BG CY CZ DE DK EE EL ES FI FR HR HU IE IT LT LU LV MT NL PL PT RO SE SI SK".split()


def get(url):
    with urllib.request.urlopen(url, timeout=120) as r:
        return r.read().decode("utf-8")


def write(name, rows, fields):
    with open(D / name, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


# sdg_02_40: share of utilised agricultural area under organic farming (%), fully converted + in conversion
rows = [r for r in csv.DictReader(io.StringIO(get(SDMX.format("sdg_02_40"))))
        if r["geo"] in EU27 + ["EU27_2020"] and r["TIME_PERIOD"] >= "2012"]
write("organic_share_pc_uaa.csv", [dict(geo=r["geo"], year=r["TIME_PERIOD"], pc_uaa=r["OBS_VALUE"], flag=r["OBS_FLAG"],
                                         last_update=r["LAST UPDATE"]) for r in rows], ["geo", "year", "pc_uaa", "flag", "last_update"])
# org_cropar: organic area in hectares (all crops = UAAXK0000), by production method
rows = [r for r in csv.DictReader(io.StringIO(get(SDMX.format("org_cropar"))))
        if r["crops"] == "UAAXK0000" and r["unit"] == "HA" and r["geo"] in EU27 + ["EU27_2020"]]
write("organic_area_ha.csv", [dict(geo=r["geo"], year=r["TIME_PERIOD"], method=r["agprdmet"], ha=r["OBS_VALUE"], flag=r["OBS_FLAG"],
                                    last_update=r["LAST UPDATE"]) for r in rows], ["geo", "year", "method", "ha", "flag", "last_update"])
# ef_lus_main: utilised agricultural area, Malta, farm structure surveys (all farm types and sizes)
d = json.loads(get(JSON.format("ef_lus_main", "geo=MT&crops=UAA")))
ids, sz = d["id"], d["size"]
cat = {k: d["dimension"][k]["category"]["index"] for k in ids}
out = []
for t, ti in cat["time"].items():
    sel = dict(statinfo="TOTAL", farmtype="TOTAL", so_eur="TOTAL", uaarea="TOTAL", unit="HA", time=t)
    pos = 0
    for k, s in zip(ids, sz):
        pos = pos * s + (cat[k][sel[k]] if k in sel else 0)
    out.append(dict(geo="MT", year=t, uaa_ha=d["value"].get(str(pos), "")))
write("uaa_malta_ef_lus_main.csv", out, ["geo", "year", "uaa_ha"])
# demo_r_d3area: total land area, Malta (km2)
d = json.loads(get(JSON.format("demo_r_d3area", "geo=MT&landuse=TOTAL&unit=KM2")))
write("land_area_malta_km2.csv", [dict(geo="MT", year=t, km2=d["value"][str(i)]) for t, i in d["dimension"]["time"]["category"]["index"].items()
                                  if str(i) in d["value"]], ["geo", "year", "km2"])
print("ok")
