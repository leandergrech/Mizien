#!/usr/bin/env python3
"""CC-017: shortest distances from the Terminal 2 reclamation to every Maltese Natura 2000 site (added in v1.1).

Needs network and numpy, scipy, rasterio, pyproj, shapely. Reads data/cc-017/s2_mask_{2023,2026}.csv (fetch_data.py)
and the EEA Natura 2000 map service (2024 release; layers 0 and 1, MS='MT', full-resolution boundaries, outSR 4326).
All distances are computed in UTM 33N (EPSG:32633), from three geometries:
  new land    Sentinel-2 pixels (10 m) that are land in summer 2026 and sea in summer 2023, in connected groups of at
              least 20 pixels (0.2 ha), which drops isolated specks (moored ships, glint): the Terminal 2 reclamation
  window      the 1.0 x 1.1 km Terminal 2 window that fetch_data.py measures (Terminal 2 and the sea off it)
  point       the reference point used in version 1.0 (14.531 E, 35.819 N), on the shore west of Terminal 2
The pixel grid is placed as fetch_data.py reads it: origin at the north-west corner of its BBOX in UTM 33N, 10 m
pixels. Checked against the OpenStreetMap coastline (92% of pixels agree; best fit within 10 m of that origin).
Writes data/cc-017/natura2000_distances.csv.
"""
import csv, datetime, json, pathlib, urllib.parse, urllib.request
import numpy as np, pyproj
from rasterio.warp import transform_bounds
from scipy import ndimage
from shapely.geometry import Point, box, shape
from shapely.ops import transform, unary_union

D = pathlib.Path(__file__).resolve().parents[2] / "data" / "cc-017"
N2K = "https://bio.discomap.eea.europa.eu/arcgis/rest/services/ProtectedSites/Natura2000Sites/MapServer"
BBOX = (14.515, 35.805, 14.555, 35.835)  # as fetch_data.py
ROW0, COL0, NROW, NCOL = 110, 180, 100, 110  # fetch_data.py WIN
REF = (14.531, 35.819)
P = pyproj.Transformer.from_crs(4326, 32633, always_xy=True).transform

minx, _, _, maxy = transform_bounds("EPSG:4326", "EPSG:32633", *BBOX)
x0, y0 = minx + COL0 * 10, maxy - ROW0 * 10
m23 = np.loadtxt(D / "s2_mask_2023.csv", delimiter=",")
m26 = np.loadtxt(D / "s2_mask_2026.csv", delimiter=",")
lab, n = ndimage.label((m26 == 1) & (m23 == 0))
keep = [i for i in range(1, n + 1) if (lab == i).sum() >= 20]
r, c = np.nonzero(np.isin(lab, keep))
geoms = {
    "new_land": unary_union([box(x0 + j * 10, y0 - (i + 1) * 10, x0 + (j + 1) * 10, y0 - i * 10) for i, j in zip(r, c)]),
    "t2_window": box(x0, y0 - NROW * 10, x0 + NCOL * 10, y0),
    "reference_point": Point(*P(*REF)),
}
print(f"new land {geoms['new_land'].area / 1e4:.1f} ha in {len(keep)} groups")

sites = []
for layer, kind in ((0, "SAC/SCI (Habitats Directive)"), (1, "SPA (Birds Directive)")):
    q = urllib.parse.urlencode({"where": "MS='MT'", "outFields": "SITECODE,SITENAME", "returnGeometry": "true",
                                "outSR": 4326, "f": "geojson"})
    for ft in json.load(urllib.request.urlopen(f"{N2K}/{layer}/query?{q}", timeout=180))["features"]:
        p = ft["properties"]
        sites.append({"sitecode": p["SITECODE"], "sitename": p["SITENAME"], "designation": kind,
                      "geom": transform(P, shape(ft["geometry"]))})
rows = []
for s in sites:
    g = s["geom"]
    over = [f"{t['sitecode']} {t['designation'].split()[0]} ({100 * g.intersection(t['geom']).area / g.area:.1f}%)"
            for t in sites if t is not s and g.intersects(t["geom"]) and g.intersection(t["geom"]).area > 0.5 * g.area]
    rows.append({"sitecode": s["sitecode"], "sitename": s["sitename"], "designation": s["designation"],
                 "marine": "yes" if s["sitename"].startswith("Żona fil-Baħar") else "no",
                 "area_km2": round(g.area / 1e6, 2),
                 **{f"km_from_{k}": round(g.distance(v) / 1000, 2) for k, v in geoms.items()},
                 "mostly_inside": "; ".join(over), "retrieved": datetime.date.today().isoformat()})
rows.sort(key=lambda x: (x["km_from_new_land"], x["sitecode"]))
with open(D / "natura2000_distances.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\r\n")
    w.writeheader()
    w.writerows(rows)
for x in rows[:8]:
    print(x)
