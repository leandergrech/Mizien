#!/usr/bin/env python3
"""CC-019: independent check of 'Malta lost ~830,000 m2 of green land to development, 2018-2023'.

Uses Impact Observatory / Esri 10 m annual land use land cover v2 (io-lulc-annual-v02, 2017-2023) from Microsoft
Planetary Computer. Single-year maps are noisy (built area swings by >15 km2 between years), so new built-up land is
counted only where a pixel is consistently not built before and consistently built after:
  strict: not built 2017, 2018, 2019 and built 2021, 2022, 2023
  two-year: not built 2017 and 2018, built 2022 and 2023
The reverse transitions (built -> not built, same rules) gauge the noise. Needs network, numpy, rasterio.

Writes data/cc-019/io_lulc_areas.csv, io_lulc_change.csv, new_built_strict.csv (row, col of 10 m pixels, for the map)
and io_lulc_grid.json (CRS and transform of that pixel grid).
"""
import csv, json, pathlib, urllib.request
import numpy as np, rasterio
from rasterio.windows import from_bounds
from rasterio.warp import transform_bounds

D = pathlib.Path(__file__).resolve().parents[2] / "data" / "cc-019"
STAC = "https://planetarycomputer.microsoft.com/api/stac/v1"
BBOX = (14.17, 35.78, 14.59, 36.09)  # Malta, Gozo, Comino
NAMES = {1: "water", 2: "trees", 4: "flooded vegetation", 5: "crops", 7: "built area", 8: "bare ground",
         9: "snow/ice", 10: "clouds", 11: "rangeland"}
tok = json.load(urllib.request.urlopen(
    "https://planetarycomputer.microsoft.com/api/sas/v1/token/io-lulc-annual-v02", timeout=60))["token"]
body = json.dumps({"collections": ["io-lulc-annual-v02"], "bbox": list(BBOX), "limit": 50}).encode()
feats = json.load(urllib.request.urlopen(urllib.request.Request(STAC + "/search", body,
                                                                {"Content-Type": "application/json"}), timeout=60))["features"]
Y = {}
for f in feats:
    yr = f["properties"]["start_datetime"][:4]
    with rasterio.open(f["assets"]["data"]["href"] + "?" + tok) as src:
        w = from_bounds(*transform_bounds("EPSG:4326", src.crs, *BBOX), transform=src.transform)
        Y[yr] = src.read(1, window=w, boundless=True, fill_value=0)
        meta = {"crs": str(src.crs), "transform": list(src.window_transform(w))[:6]}
yrs = sorted(Y)
KM2 = 1e-4  # 10 m pixel = 100 m2 = 1e-4 km2
land = np.all([Y[y] != 1 for y in yrs], axis=0) & np.all([Y[y] != 0 for y in yrs], axis=0)
with open(D / "io_lulc_areas.csv", "w", newline="") as fh:
    w = csv.writer(fh, lineterminator="\r\n")
    w.writerow(["year", "class", "area_km2"])
    for y in yrs:
        for k, n in NAMES.items():
            a = ((Y[y] == k) & land).sum() * KM2
            if a:
                w.writerow([y, n, round(a, 3)])
B = {y: Y[y] == 7 for y in yrs}
nb = lambda ys: np.all([~B[y] for y in ys], axis=0)
bb = lambda ys: np.all([B[y] for y in ys], axis=0)
rules = {"strict": (("2017", "2018", "2019"), ("2021", "2022", "2023")),
         "two-year": (("2017", "2018"), ("2022", "2023"))}
rows = []
for name, (pre, post) in rules.items():
    gain = land & nb(pre) & bb(post)
    loss = land & bb(pre) & nb(post)
    src = Y["2018"][gain]
    u, c = np.unique(src, return_counts=True)
    shares = {NAMES[int(k)]: round(100 * v / c.sum(), 1) for k, v in zip(u, c)}
    rows.append({"rule": name, "new_built_km2": round(gain.sum() * KM2, 3), "reverse_km2": round(loss.sum() * KM2, 3),
                 "net_km2": round((gain.sum() - loss.sum()) * KM2, 3), "from_crops_pct": shares.get("crops", 0),
                 "from_rangeland_pct": shares.get("rangeland", 0), "from_bare_pct": shares.get("bare ground", 0),
                 "from_trees_pct": shares.get("trees", 0), "land_km2": round(land.sum() * KM2, 1)})
    if name == "strict":
        rr, cc = np.nonzero(gain)
        np.savetxt(D / "new_built_strict.csv", np.c_[rr, cc], fmt="%d", delimiter=",", header="row,col", comments="")
json.dump(meta, open(D / "io_lulc_grid.json", "w"))
with open(D / "io_lulc_change.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator="\r\n")
    w.writeheader()
    w.writerows(rows)
for r in rows:
    print(r)
