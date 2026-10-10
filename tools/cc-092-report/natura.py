#!/usr/bin/env python3
"""CC-092: how much of Gozo's CORINE land lies inside Natura 2000 sites. Needs network and shapely.

Fetches, in the equal-area projection EPSG:3035 (so areas can be measured directly), the CORINE Land Cover 2018
polygons around Gozo (EEA map service CLC2018_WM, layer 0) and Malta's Natura 2000 sites (EEA map service
Natura2000Sites: layer 0, Habitats Directive sites; layer 1, Birds Directive sites; MS = 'MT'), assigns CORINE
polygons to Gozo by extent as calc.py does, and measures the overlap by land-cover group.
Writes data/cc-092/natura2000_overlap.csv."""
import csv, datetime, json, pathlib, urllib.parse, urllib.request
from shapely.geometry import Polygon
from shapely.ops import unary_union

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-092"
UA = {"User-Agent": "Mizien-factcheck/1.0"}
CLC = "https://image.discomap.eea.europa.eu/arcgis/rest/services/Corine/CLC2018_WM/MapServer/0/query"
N2K = "https://bio.discomap.eea.europa.eu/arcgis/rest/services/ProtectedSites/Natura2000Sites/MapServer"


def get(url, params):
    u = url + "?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=240) as r:
        return json.loads(r.read().decode())


def esri_geom(rings):
    """Esri rings: exteriors run clockwise (negative shoelace area), holes anticlockwise."""
    def signed(r):
        return sum(r[i][0] * r[i + 1][1] - r[i + 1][0] * r[i][1] for i in range(len(r) - 1)) / 2
    ext = [Polygon(r).buffer(0) for r in rings if signed(r) < 0]
    holes = [Polygon(r).buffer(0) for r in rings if signed(r) > 0]
    g = unary_union(ext)
    return g.difference(unary_union(holes)) if holes else g


clc = get(CLC, {"where": "1=1", "geometry": "14.15,35.97,14.37,36.10", "geometryType": "esriGeometryEnvelope",
                "inSR": "4326", "spatialRel": "esriSpatialRelIntersects", "outFields": "OBJECTID,Code_18",
                "returnGeometry": "true", "outSR": "3035", "f": "json"})
ext = {r["objectid"]: r for r in csv.DictReader(open(D / "clc2018_gozo_polygons.csv"))}


def island(oid):
    r = ext[str(oid)]
    if float(r["lat_max"]) < 36.0:
        return "Malta"
    if float(r["lat_min"]) < 36.025 and float(r["lon_min"]) > 14.31:
        return "Comino"
    return "Gozo"


GROUP = {"112": "built", "131": "built", "142": "built", "211": "farmland", "242": "farmland", "243": "farmland",
         "323": "semi-natural", "333": "semi-natural"}
groups = {}
for ft in clc["features"]:
    a = ft["attributes"]
    if a["Code_18"] == "523" or island(a["OBJECTID"]) != "Gozo":
        continue
    groups.setdefault(GROUP.get(a["Code_18"], "other"), []).append(esri_geom(ft["geometry"]["rings"]))
groups = {k: unary_union(v) for k, v in groups.items()}
groups["all Gozo land (CORINE)"] = unary_union(list(groups.values()))

sites = {}
for layer, kind in ((0, "Habitats Directive (SAC/SCI)"), (1, "Birds Directive (SPA)")):
    d = get(f"{N2K}/{layer}/query", {"where": "MS='MT'", "outFields": "SITECODE,SITENAME", "returnGeometry": "true",
                                     "outSR": "3035", "f": "json"})
    sites[kind] = unary_union([esri_geom(ft["geometry"]["rings"]) for ft in d["features"]])
sites["either"] = unary_union(list(sites.values()))

rows, today = [], datetime.date.today().isoformat()
for g, geom in groups.items():
    row = {"land_group": g, "area_ha": round(geom.area / 1e4, 1)}
    for k, s in sites.items():
        ov = geom.intersection(s).area / 1e4
        row[f"in_{k}_ha"] = round(ov, 1)
        row[f"in_{k}_pct"] = round(100 * ov / (geom.area / 1e4), 1)
    row.update({"source": "EEA CORINE Land Cover 2018 (CLC2018_WM) and Natura 2000 sites (Natura2000Sites, MS='MT'), "
                          "both in EPSG:3035", "retrieved": today})
    rows.append(row)
    print(row)
with open(D / "natura2000_overlap.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
