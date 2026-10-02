#!/usr/bin/env python3
"""CC-011: share of Malta's population within a 10-minute walk of a green or open space.

Inputs (downloaded if missing, into ./cache/):
  - WorldPop 2025 constrained population, 100 m (R2025A v1), CC BY 4.0
  - OpenStreetMap green/open-space features via Overpass (ODbL), query in green.overpass
Output: data/cc-011/green_access_results.csv (one row per definition x distance)

Method: features are rasterised on a 10 m grid (UTM 33N); a Euclidean distance transform gives each
population cell's straight-line distance to the nearest qualifying feature. Straight-line distance
overstates access compared with walking routes, so 800 m (10 min at 4.8 km/h) is also tested with a
1.3 route-detour factor (615 m). This is a screening estimate, not a network analysis.
"""
import csv, json, os, pathlib, subprocess, sys, datetime
import numpy as np
import rasterio
from rasterio import features
from rasterio.transform import from_origin
from pyproj import Transformer
from shapely.geometry import Polygon, Point, mapping
from shapely.ops import transform as stransform, unary_union
from scipy import ndimage

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
CACHE = HERE / "cache"; CACHE.mkdir(exist_ok=True)
POP_URL = ("https://data.worldpop.org/GIS/Population/Global_2015_2030/R2025A/2025/MLT/v1/100m/constrained/"
           "mlt_pop_2025_CN_100m_R2025A_v1.tif")
POP = CACHE / "mlt_pop_2025_CN_100m_R2025A_v1.tif"
OSM = CACHE / "osm_green.json"
UA = "Mizien-factcheck/0.1 (github.com/leandergrech/Mizien)"

if not POP.exists():
    subprocess.run(["curl", "-sL", "-o", str(POP), POP_URL], check=True)
if not OSM.exists():
    subprocess.run(["curl", "-s", "-A", UA, "--data-urlencode", f"data@{HERE / 'green.overpass'}",
                    "https://overpass-api.de/api/interpreter", "-o", str(OSM)], check=True)
osm = json.load(open(OSM))
osm_ts = osm.get("osm3s", {}).get("timestamp_osm_base", "")

to_utm = Transformer.from_crs("EPSG:4326", "EPSG:32633", always_xy=True).transform
PRIVATE = {"private", "no", "customers"}


def geom_of(e):
    if e["type"] == "node":
        return Point(e["lon"], e["lat"])
    if e["type"] == "way":
        pts = [(p["lon"], p["lat"]) for p in e.get("geometry", [])]
        if len(pts) >= 4 and pts[0] == pts[-1]:
            return Polygon(pts)
        return None  # open ways (e.g. linear pedestrian streets) are skipped
    if e["type"] == "relation":  # outer rings only; inner holes ignored (small overstatement)
        polys = []
        for m in e.get("members", []):
            if m.get("role") == "outer" and m.get("geometry"):
                pts = [(p["lon"], p["lat"]) for p in m["geometry"]]
                if len(pts) >= 4 and pts[0] == pts[-1]:
                    polys.append(Polygon(pts))
        return unary_union(polys) if polys else None
    return None


def classify(t):
    """Return the narrowest definition tier a feature belongs to (1 strict .. 3 broadest), or None."""
    if t.get("access") in PRIVATE or t.get("garden:type") in {"residential", "private"}:
        return None
    le, lu, na = t.get("leisure"), t.get("landuse"), t.get("natural")
    if le in {"park", "garden", "nature_reserve", "common"} or lu in {"village_green", "recreation_ground"}:
        return 1
    if na in {"wood", "scrub", "heath", "grassland", "garrigue"} or lu in {"forest", "meadow", "grass"} \
            or le in {"playground", "dog_park"}:
        return 2
    if na == "beach" or t.get("place") == "square" or t.get("highway") == "pedestrian":
        return 3
    return None


feats = []  # (tier, area_ha, utm_geom)
for e in osm["elements"]:
    tier = classify(e.get("tags", {}))
    if tier is None:
        continue
    g = geom_of(e)
    if g is None or g.is_empty:
        continue
    if not g.is_valid:
        g = g.buffer(0)
    gu = stransform(to_utm, g)
    feats.append((tier, gu.area / 1e4, gu))

DEFS = [  # name, max tier, min area (ha), description
    ("D1 public parks and gardens", 1, 0.0, "leisure=park/garden (not private), nature reserves, village greens, recreation grounds"),
    ("D1 parks >= 0.5 ha", 1, 0.5, "as D1, only features of at least 0.5 ha (WHO Europe indicator size)"),
    ("D1 parks >= 1 ha", 1, 1.0, "as D1, only features of at least 1 ha (WHO Europe additional indicator)"),
    ("D2 green space, broad", 2, 0.0, "D1 plus woodland, scrub, garrigue, heath, grassland, grass, meadow, playgrounds"),
    ("D2 green space >= 0.5 ha", 2, 0.5, "as D2, only features of at least 0.5 ha"),
    ("D3 open or green space", 3, 0.0, "D2 plus beaches, squares and pedestrian areas (the manifesto says 'open or green')"),
]
DISTS = [(300, "300 m straight line (WHO Europe indicator)"), (615, "800 m walk with 1.3 detour factor"),
         (800, "800 m straight line (optimistic 10-minute walk)")]

with rasterio.open(POP) as r:
    pop = r.read(1).astype("float64")
    pop[(pop == r.nodata) | (pop < 0)] = 0
    rows, cols = np.nonzero(pop > 0)
    xs, ys = rasterio.transform.xy(r.transform, rows, cols)
    pw = pop[rows, cols]
ux, uy = to_utm(np.array(xs), np.array(ys))

RES = 10.0
x0, x1 = ux.min() - 3000, ux.max() + 3000
y0, y1 = uy.min() - 3000, uy.max() + 3000
W, H = int((x1 - x0) / RES), int((y1 - y0) / RES)
T = from_origin(x0, y1, RES, RES)
ci = ((ux - x0) / RES).astype(int)
ri = ((y1 - uy) / RES).astype(int)
total = pw.sum()

def weighted_median(v, w):
    o = np.argsort(v)
    c = np.cumsum(w[o])
    return v[o][np.searchsorted(c, c[-1] / 2)]


out = []
for name, maxtier, minha, desc in DEFS:
    shapes = [(mapping(g if g.geom_type != "Point" else g.buffer(5)), 1) for t, a, g in feats
              if t <= maxtier and (a >= minha or (minha == 0))]
    mask = features.rasterize(shapes, out_shape=(H, W), transform=T, fill=0, all_touched=True, dtype="uint8")
    dist = ndimage.distance_transform_edt(mask == 0) * RES
    d = dist[ri, ci]
    for dm, dlabel in DISTS:
        share = pw[d <= dm].sum() / total
        out.append({"definition": name, "definition_detail": desc, "distance_m": dm, "distance_basis": dlabel,
                    "features_used": len(shapes), "population_share_within": round(share, 4),
                    "population_outside": int(round(total - pw[d <= dm].sum())),
                    "median_distance_m": int(weighted_median(d, pw)),
                    "population_total_worldpop": int(round(total))})
        print(f"{name:30s} {dm:4d} m  {share:6.1%}  outside {total - pw[d <= dm].sum():8.0f}")

dst = ROOT / "data" / "cc-011" / "green_access_results.csv"
with open(dst, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0]) + ["osm_timestamp", "population_source", "run_date"])
    w.writeheader()
    for o in out:
        o.update(osm_timestamp=osm_ts, population_source=POP_URL, run_date=datetime.date.today().isoformat())
        w.writerow(o)
print("wrote", dst)
