#!/usr/bin/env python3
"""CC-017: fetch the satellite and protected-area data behind the land-reclamation check.

Needs network and numpy, rasterio, pyproj, shapely. Writes to data/cc-017/:
  s2_land_t2.csv          land area (ha) in a window over Freeport Terminal 2, per summer, from a per-pixel median of
                          up to eight clear Sentinel-2 L2A scenes (NDWI < 0 = land; 10 m pixels)
  s2_mask_{2023,2026}.csv the land mask of that window (1 = land), for the figure
  natura2000_near_freeport.csv  Natura 2000 sites within the search box and their distance from the Freeport
  natura2000.geojson      their boundaries (EEA Natura 2000 2024 release), simplified to 20 m
"""
import csv, json, pathlib, urllib.parse, urllib.request
import numpy as np, pyproj, rasterio
from rasterio.windows import from_bounds
from rasterio.warp import transform_bounds
from shapely.geometry import Point, mapping, shape
from shapely.ops import transform

D = pathlib.Path(__file__).resolve().parents[2] / "data" / "cc-017"
STAC = "https://planetarycomputer.microsoft.com/api/stac/v1/search"
BBOX = (14.515, 35.805, 14.555, 35.835)
WIN = (slice(110, 210), slice(180, 290))  # rows, cols of BBOX at 10 m: Terminal 2 and the sea off it
FREEPORT = (14.531, 35.819)
N2K = "https://bio.discomap.eea.europa.eu/arcgis/rest/services/ProtectedSites/Natura2000Sites/MapServer"
TOK = json.load(urllib.request.urlopen(
    "https://planetarycomputer.microsoft.com/api/sas/v1/token/sentinel-2-l2a", timeout=60))["token"]


def search(dt, cloud=10):
    body = json.dumps({"collections": ["sentinel-2-l2a"], "bbox": list(BBOX), "datetime": dt,
                       "query": {"eo:cloud_cover": {"lt": cloud}}, "limit": 100}).encode()
    req = urllib.request.Request(STAC, body, {"Content-Type": "application/json"})
    feats = sorted(json.load(urllib.request.urlopen(req, timeout=120))["features"],
                   key=lambda f: f["properties"]["eo:cloud_cover"])
    seen, out = set(), []
    for f in feats:
        d = f["properties"]["datetime"][:10]
        if d not in seen:
            seen.add(d)
            out.append(f)
    return out[:8]


def read(f, band):
    with rasterio.open(f["assets"][band]["href"] + "?" + TOK) as src:
        w = from_bounds(*transform_bounds("EPSG:4326", src.crs, *BBOX), transform=src.transform)
        return src.read(1, window=w, boundless=True, fill_value=0).astype("float32")


rows = []
for yr in ("2017", "2020", "2023", "2024", "2025", "2026"):
    fs = search(f"{yr}-05-01/{yr}-10-15")
    med = np.median([(lambda g, n: (g - n) / np.maximum(g + n, 1))(read(f, "B03"), read(f, "B08")) for f in fs], axis=0)
    land = med[WIN] < 0
    rows.append({"year": yr, "land_ha": round(land.sum() * 0.01, 2), "scenes": len(fs),
                 "dates": " ".join(sorted(f["properties"]["datetime"][:10] for f in fs))})
    if yr in ("2023", "2026"):
        np.savetxt(D / f"s2_mask_{yr}.csv", land.astype(int), fmt="%d", delimiter=",")
    print(rows[-1])
with open(D / "s2_land_t2.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\r\n")
    w.writeheader()
    w.writerows(rows)

P = pyproj.Transformer.from_crs(4326, 32633, always_xy=True).transform
fp = transform(P, Point(*FREEPORT))
sites, feats = [], []
for layer, kind in ((0, "SAC/SCI (Habitats Directive)"), (1, "SPA (Birds Directive)")):
    q = urllib.parse.urlencode({"geometry": "14.40,35.75,14.65,35.90", "geometryType": "esriGeometryEnvelope",
                                "inSR": 4326, "outSR": 4326, "spatialRel": "esriSpatialRelIntersects",
                                "outFields": "SITECODE,SITENAME,SITETYPE", "returnGeometry": "true", "f": "geojson"})
    for ft in json.load(urllib.request.urlopen(f"{N2K}/{layer}/query?{q}", timeout=120))["features"]:
        g = shape(ft["geometry"])
        gm = transform(P, g)
        p = ft["properties"]
        sites.append({"sitecode": p["SITECODE"], "sitename": p["SITENAME"], "designation": kind,
                      "area_km2": round(gm.area / 1e6, 1), "distance_from_freeport_km": round(gm.distance(fp) / 1000, 2)})
        feats.append({"type": "Feature", "properties": {"sitecode": p["SITECODE"], "layer": layer},
                      "geometry": mapping(g.simplify(0.0002))})
sites.sort(key=lambda s: s["distance_from_freeport_km"])
with open(D / "natura2000_near_freeport.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(sites[0]), lineterminator="\r\n")
    w.writeheader()
    w.writerows(sites)
json.dump({"type": "FeatureCollection", "features": feats}, open(D / "natura2000.geojson", "w"))
print(len(sites), "Natura 2000 sites")
