#!/usr/bin/env python3
"""CC-009 v1.2: national groundwater data for Malta.

1. Eurostat env_wat_abs (fresh groundwater abstraction by sector) and env_wat_res (recharge into the aquifer,
   precipitation, renewable freshwater resources), Malta, million m3, 2010 onwards
   -> data/cc-009/eurostat_water.csv (with Eurostat's flag per value, the dataset's update stamp, the query URL and
   the retrieval date; flag e = estimated, b = break in series).
2. EEA WISE WFD groundwater bodies, 3rd RBMP reporting (WFD2022_GroundWaterBody_WM, layer 0, Malta), with geometry
   -> data/cc-009/wise_gwb_2022.geojson (polygons simplified to about 10 m for the map; status codes 2 = good,
   3 = poor, as in wise_gwb_status.csv).
"""
import csv
import datetime as dt
import json
import pathlib
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-009"
TODAY = dt.date.today().isoformat()
ES = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
QUERIES = {
    "env_wat_abs": ES + "env_wat_abs?geo=MT&wat_src=FGW&unit=MIO_M3&sinceTimePeriod=2010",
    "env_wat_res": ES + "env_wat_res?geo=MT&unit=MIO_M3&sinceTimePeriod=2010",
}
GWB = ("https://water.discomap.eea.europa.eu/arcgis/rest/services/WISE_WFD/WFD2022_GroundWaterBody_WM/MapServer/0/"
       "query?" + urllib.parse.urlencode({
           "where": "countryCode='MT'",
           "outFields": "cYear,euGroundWaterBodyCode,groundWaterBodyName,gwQuantitativeStatusValue,"
                        "gwChemicalStatusValue",
           "returnGeometry": "true", "outSR": "4326", "maxAllowableOffset": "0.0001", "geometryPrecision": "5",
           "f": "geojson"}))


def get(url):
    with urllib.request.urlopen(url, timeout=120) as r:
        return json.load(r)


def jsonstat_rows(j):
    ids, sizes = j["id"], j["size"]
    cats = [sorted(j["dimension"][d]["category"]["index"].items(), key=lambda kv: kv[1]) for d in ids]
    labels = {d: j["dimension"][d]["category"].get("label", {}) for d in ids}
    status = j.get("status", {})
    for k, v in j["value"].items():
        rem, codes = int(k), []
        for s in reversed(sizes):
            codes.append(rem % s)
            rem //= s
        codes.reverse()
        row = {d: cats[i][codes[i]][0] for i, d in enumerate(ids)}
        row["label"] = labels["wat_proc"].get(row["wat_proc"], "")
        yield row, v, status.get(k, "")


def main():
    with open(D / "eurostat_water.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["dataset", "geo", "wat_proc", "label", "wat_src", "unit", "year", "value", "flag",
                    "eurostat_updated", "query_url", "retrieved"])
        for ds, url in QUERIES.items():
            j = get(url)
            rows = sorted(jsonstat_rows(j), key=lambda x: (x[0]["wat_proc"], x[0]["time"]))
            for r, v, fl in rows:
                w.writerow([ds, r["geo"], r["wat_proc"], r["label"], r.get("wat_src", ""), r["unit"], r["time"], v, fl,
                            j["updated"], url, TODAY])
            print(ds, len(rows), "values, updated", j["updated"])
    g = get(GWB)
    g["metadata"] = {"source": "EEA WISE WFD, WFD2022_GroundWaterBody_WM layer 0 (Malta's 3rd RBMP reporting)",
                     "query_url": GWB, "retrieved": TODAY,
                     "status_codes": "2 = good, 3 = poor (layer legend)"}
    with open(D / "wise_gwb_2022.geojson", "w") as f:
        json.dump(g, f, separators=(",", ":"))
    print("groundwater bodies:", len(g["features"]))


if __name__ == "__main__":
    main()
