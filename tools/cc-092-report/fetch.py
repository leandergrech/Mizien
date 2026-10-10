#!/usr/bin/env python3
"""CC-092: fetch the open data behind the afforestation arithmetic. Needs network. Writes into data/cc-092/:

- eurostat_extract.csv: env_air_gge (Malta: total excl. LULUCF, LULUCF, forest land), demo_r_pjangrp3 (Malta and
  MT002 Gozo and Comino), reg_area3 (area of MT002), for_area (Malta's forest and other wooded land, FAO definitions),
  sdg_06_60 (water exploitation index plus, Malta and EU), each with Eurostat's status flag and update date.
- clc2018_gozo_polygons.csv: CORINE Land Cover 2018 polygons around Gozo (EEA discomap map service, vector layer),
  with each polygon's area (the service's Area_Ha) and extent, and the island it lies on (by extent; see calc.py).
- nasa_power_gozo.json, nasa_power_yatir.json: NASA POWER 1991-2020 climatology (MERRA-2) for Gozo and for the Yatir
  forest (Grünzweig et al. 2007 site coordinates), rainfall and temperature.
"""
import csv, datetime, json, pathlib, urllib.parse, urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-092"
D.mkdir(parents=True, exist_ok=True)
TODAY = datetime.date.today().isoformat()
UA = {"User-Agent": "Mizien-factcheck/1.0"}
ES = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
QUERIES = {
    "env_air_gge": "env_air_gge?geo=MT&unit=THS_T&airpol=GHG&src_crf=TOTX4_MEMO&src_crf=CRF4&src_crf=CRF4A&sinceTimePeriod=2005",
    "demo_r_pjangrp3": "demo_r_pjangrp3?geo=MT&geo=MT002&sex=T&age=TOTAL&unit=NR&sinceTimePeriod=2016",
    "reg_area3": "reg_area3?geo=MT&geo=MT002",
    "for_area": "for_area?geo=MT",
    "sdg_06_60": "sdg_06_60?geo=MT&geo=EU27_2020&sinceTimePeriod=2015",
}


def get_json(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
        return json.loads(r.read().decode())


def eurostat():
    out = []
    for ds, q in QUERIES.items():
        url = ES + q + "&format=JSON&lang=EN"
        d = get_json(url)
        dims, size = d["id"], d["size"]
        idx = [{v: k for k, v in d["dimension"][n]["category"]["index"].items()} for n in dims]
        lab = {n: d["dimension"][n]["category"].get("label", {}) for n in dims}
        for k, val in d["value"].items():
            pos, c = int(k), []
            for s in reversed(size):
                c.append(pos % s)
                pos //= s
            c = c[::-1]
            co = {n: idx[i][c[i]] for i, n in enumerate(dims)}
            item = "|".join(f"{n}={co[n]}" for n in dims if n not in ("freq", "geo", "time"))
            label = "; ".join(lab[n].get(co[n], co[n]) for n in dims if n not in ("freq", "geo", "time"))
            out.append([ds, co["geo"], item, label, co["time"], val, d.get("status", {}).get(k, ""), d.get("updated", ""),
                        url, TODAY])
    with open(D / "eurostat_extract.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["dataset", "geo", "item", "item_label", "year", "value", "flag", "eurostat_updated", "query_url",
                    "retrieved"])
        w.writerows(sorted(out))
    print("eurostat rows", len(out))


CLC_URL = ("https://image.discomap.eea.europa.eu/arcgis/rest/services/Corine/CLC2018_WM/MapServer/0/query?"
           + urllib.parse.urlencode({"where": "1=1", "geometry": "14.15,35.97,14.37,36.10",
                                     "geometryType": "esriGeometryEnvelope", "inSR": "4326",
                                     "spatialRel": "esriSpatialRelIntersects", "outFields": "OBJECTID,Code_18,Area_Ha",
                                     "returnGeometry": "true", "outSR": "4326", "f": "json"}))


def corine():
    d = get_json(CLC_URL)
    rows = []
    for ft in d["features"]:
        pts = [p for r in ft["geometry"]["rings"] for p in r]
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        a = ft["attributes"]
        rows.append({"objectid": a["OBJECTID"], "code_18": a["Code_18"], "area_ha": round(a["Area_Ha"], 2),
                     "lon_min": round(min(xs), 4), "lon_max": round(max(xs), 4), "lat_min": round(min(ys), 4),
                     "lat_max": round(max(ys), 4), "source": "EEA, CORINE Land Cover 2018 vector (CLC2018_WM layer 0)",
                     "query_url": CLC_URL, "retrieved": TODAY})
    with open(D / "clc2018_gozo_polygons.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(sorted(rows, key=lambda r: r["objectid"]))
    print("corine polygons", len(rows))


def power():
    for name, lon, lat in (("gozo", 14.24, 36.04), ("yatir", 35.05, 31.333)):
        url = ("https://power.larc.nasa.gov/api/temporal/climatology/point?parameters=PRECTOTCORR,T2M&community=AG"
               f"&longitude={lon}&latitude={lat}&format=JSON&start=1991&end=2020")
        d = get_json(url)
        d["_mizien"] = {"query_url": url, "retrieved": TODAY}
        json.dump(d, open(D / f"nasa_power_{name}.json", "w"), indent=1)
        print("power", name, d["properties"]["parameter"]["PRECTOTCORR"]["ANN"], "mm/day")


if __name__ == "__main__":
    eurostat()
    corine()
    power()
