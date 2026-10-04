#!/usr/bin/env python3
"""CC-051: measure Malta's marine Natura 2000 area from the EEA's site boundaries.

Queries the EEA Natura 2000 map service (2024 release) for all Maltese sites (SAC and SPA layers), dissolves overlaps,
removes land using the island outlines in docs/data/geo.json (OpenStreetMap), and writes data/cc-051/natura2000_marine.csv
(per-site and union areas, km2). Needs network, shapely and pyproj."""
import csv, json, math, pathlib, urllib.parse, urllib.request
import pyproj
from shapely.geometry import Polygon, shape
from shapely.ops import transform, unary_union

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-051"
N2K = "https://bio.discomap.eea.europa.eu/arcgis/rest/services/ProtectedSites/Natura2000Sites/MapServer"
P = pyproj.Transformer.from_crs(4326, 32633, always_xy=True).transform
sites = {}
for layer in (0, 1):
    q = urllib.parse.urlencode({"where": "MS='MT'", "outFields": "SITECODE,SITENAME,SITETYPE", "returnGeometry": "true",
                                "outSR": 4326, "f": "geojson"})
    for ft in json.load(urllib.request.urlopen(f"{N2K}/{layer}/query?{q}", timeout=180))["features"]:
        p = ft["properties"]
        g = transform(P, shape(ft["geometry"])).buffer(0)
        k = p["SITECODE"]
        sites[k] = (p["SITENAME"], p["SITETYPE"], unary_union([sites[k][2], g]) if k in sites else g)
geo = json.load(open(ROOT / "docs" / "data" / "geo.json"))
o = geo["origin"]
k = 111320 * math.cos(math.radians(o["lat"]))
land = unary_union([transform(P, Polygon([(o["lon"] + r[i] / k, o["lat"] + r[i + 1] / 110574)
                                          for i in range(0, len(r) - 1, 2)])).buffer(0) for isl in geo["islands"]
                    for r in [isl.get("detail") or isl["coarse"]]])
rows = []
for code, (name, typ, g) in sorted(sites.items()):
    sea = g.difference(land)
    rows.append({"sitecode": code, "sitename": name, "sitetype": typ, "area_km2": round(g.area / 1e6, 2),
                 "sea_km2": round(sea.area / 1e6, 2)})
marine = [s for s in rows if s["sea_km2"] >= 1]
union = unary_union([sites[s["sitecode"]][2] for s in marine]).difference(land)
rows.append({"sitecode": "UNION", "sitename": f"Union of {len(marine)} sites with >= 1 km2 of sea", "sitetype": "",
             "area_km2": "", "sea_km2": round(union.area / 1e6, 1)})
with open(D / "natura2000_marine.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\r\n")
    w.writeheader()
    w.writerows(rows)
print(len(sites), "sites;", len(marine), "with sea; union sea area", round(union.area / 1e6, 1), "km2")
