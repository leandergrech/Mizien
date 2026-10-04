#!/usr/bin/env python3
"""CC-051: measure Malta's marine Natura 2000 area and fetch the boundaries of the zones it is measured against.

1. Queries the EEA Natura 2000 map service (2024 release) for all Maltese sites (SAC and SPA layers), dissolves
   overlaps, removes land using the island outlines in docs/data/geo.json (OpenStreetMap), and writes
   data/cc-051/natura2000_marine.csv (per-site and union areas, km2).
2. Writes data/cc-051/boundaries.geojson (WGS84) with:
   - protected: the union of the 18 marine sites, sea only (EEA, as above);
   - territorial_sea: Malta's 12-nm territorial sea, Marine Regions v4 (doi:10.14284/633);
   - fmz: the 25-nm Fisheries Management Zone, rebuilt as the 12-nm zone plus everything landward of it (land and
     internal waters) buffered by a further 13 nm, minus land and internal waters (25 nm from the baselines);
   - within_25nm: the same 25-nm envelope including internal waters, minus land;
   - eez: Malta's exclusive economic zone as mapped by Marine Regions v12 (doi:10.14284/632);
   - eu_marine_waters: the marine waters Malta reports under the Marine Strategy Framework Directive (EEA "Marine
     waters used in MSFD" v1.0, 2020; simplified by the EEA for its map service).
3. Downloads the EMODnet depth grid (via the EEA Bathymetry image service) for the area to out/bathymetry.tif
   (git-ignored; used by calc.py and figures.py).
Needs network, shapely and pyproj."""
import csv, json, math, pathlib, urllib.parse, urllib.request
import pyproj
from shapely import make_valid
from shapely.geometry import Polygon, mapping, shape
from shapely.ops import transform, unary_union

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
D = ROOT / "data" / "cc-051"
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
N2K = "https://bio.discomap.eea.europa.eu/arcgis/rest/services/ProtectedSites/Natura2000Sites/MapServer"
MR = "https://geo.vliz.be/geoserver/MarineRegions/wfs"
EEA_MARINE = "https://water.discomap.eea.europa.eu/arcgis/rest/services/Marine"
NM = 1852
BBOX = (12.4, 34.0, 18.3, 36.8)  # lon/lat extent of the depth grid (covers all of Malta's reported waters)
P = pyproj.Transformer.from_crs(4326, 32633, always_xy=True).transform
W = pyproj.Transformer.from_crs(32633, 4326, always_xy=True).transform


def get(url, params, timeout=180):
    return json.load(urllib.request.urlopen(f"{url}?{urllib.parse.urlencode(params)}", timeout=timeout))


def utm(geojson_geometry):
    return make_valid(transform(P, shape(geojson_geometry))).buffer(0)


# ---------------------------------------------------------------- 1. Natura 2000 sites
sites = {}
for layer in (0, 1):
    for ft in get(f"{N2K}/{layer}/query", {"where": "MS='MT'", "outFields": "SITECODE,SITENAME,SITETYPE",
                                            "returnGeometry": "true", "outSR": 4326, "f": "geojson"})["features"]:
        p = ft["properties"]
        g = utm(ft["geometry"])
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

# ---------------------------------------------------------------- 2. reference zones
wfs = {"service": "WFS", "version": "1.0.0", "request": "GetFeature", "outputFormat": "application/json"}
eez = utm(get(MR, {**wfs, "typeName": "MarineRegions:eez", "CQL_FILTER": "mrgid=5685"})["features"][0]["geometry"])
ts = utm(get(MR, {**wfs, "typeName": "MarineRegions:eez_12nm", "CQL_FILTER": "mrgid=49026"})["features"][0]["geometry"])
landward = unary_union([Polygon(p.exterior) for p in getattr(ts, "geoms", [ts])])  # 12-nm zone + land + internal waters
inner = landward.difference(ts)                                                     # land + internal waters
envelope = landward.buffer(13 * NM, resolution=64)                                  # 25 nm from the baselines
fmz = envelope.difference(inner)
within25 = envelope.difference(land)
mw = {ft["properties"]["Type"]: utm(ft["geometry"]) for ft in
      get(f"{EEA_MARINE}/Marine_waters_EU/MapServer/0/query", {"where": "Country='MT'", "outFields": "Type,Area_km2",
                                                                 "returnGeometry": "true", "outSR": 4326,
                                                                 "f": "geojson"})["features"]}
eu = mw["Area designated for hydrocarbon exploration and exploitation"]
zones = [("protected", union.simplify(5), "EEA Natura 2000 (2024 release): union of 18 marine sites, land removed (OSM)"),
         ("territorial_sea", ts, "Marine Regions, Territorial Seas (12NM) v4, 2023, doi:10.14284/633"),
         ("fmz", fmz, "Rebuilt from Marine Regions 12NM v4: 25 nm from the baselines, excluding land and internal waters"),
         ("within_25nm", within25, "As fmz, but including internal waters"),
         ("eez", eez, "Marine Regions, Maritime Boundaries and EEZ (200NM) v12, 2023, doi:10.14284/632"),
         ("eu_marine_waters", eu, "EEA, Marine waters used in MSFD v1.0 (2020), Malta, type 'Area designated for "
                                  "hydrocarbon exploration and exploitation' (map-service version, simplified)")]


def rnd(c):
    return [rnd(x) for x in c] if isinstance(c[0], (list, tuple)) else [round(c[0], 5), round(c[1], 5)]


fc = {"type": "FeatureCollection", "features": []}
for name, g, src in zones:
    gm = mapping(transform(W, g))
    gm = {"type": gm["type"], "coordinates": rnd(gm["coordinates"])}
    fc["features"].append({"type": "Feature", "properties": {"zone": name, "area_km2_utm33n": round(g.area / 1e6, 1),
                                                             "source": src}, "geometry": gm})
    print(f"{name:18s} {g.area / 1e6:10.1f} km2")
json.dump(fc, open(D / "boundaries.geojson", "w"), separators=(",", ":"))

# ---------------------------------------------------------------- 3. depth grid (EMODnet via the EEA)
q = {"bbox": ",".join(map(str, BBOX)), "bboxSR": 4326, "imageSR": 4326, "size": "2950,1400", "format": "tiff",
     "pixelType": "F32", "noDataInterpretation": "esriNoDataMatchAny", "interpolation": "RSP_NearestNeighbor",
     "f": "image"}
urllib.request.urlretrieve(f"{EEA_MARINE}/Bathymetry/ImageServer/exportImage?{urllib.parse.urlencode(q)}",
                           OUT / "bathymetry.tif")
print("depth grid ->", OUT / "bathymetry.tif")
