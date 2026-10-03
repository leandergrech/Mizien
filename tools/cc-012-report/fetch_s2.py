#!/usr/bin/env python3
"""CC-012: Sentinel-2 greenness over the Ta' Qali picnic area, 2023-2026.

Needs network (Microsoft Planetary Computer STAC, anonymous token) and rasterio, pyproj, scipy, numpy.
Writes to data/cc-012/:
  gravel_zone.geojson   pixels inside the OSM park polygon that brightened sharply between summer 2024 and
                        summer 2025 (gravel laid June 2025): above the 95th percentile of brightening outside the
                        polygon. Defined from brightness, not greenness, so the winter-greenness test is independent.
  ndvi_timeseries.csv   per scene: median NDVI and visible brightness in the gravel zone and in the rest of the
                        polygon (control, 20 m buffer excluded). Clear pixels only (SCL 4-7), scenes < 10% cloud.
  rgb_crops.npz         true-colour crops for Feb 2025 and Feb 2026 (figure 1).
Contains modified Copernicus Sentinel data 2023-2026.
"""
import csv, json, pathlib, urllib.request
import numpy as np, rasterio
from rasterio.features import rasterize, shapes
from rasterio.windows import from_bounds
from rasterio.warp import transform_bounds
from pyproj import Transformer
from scipy import ndimage

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-012"
STAC = "https://planetarycomputer.microsoft.com/api/stac/v1/search"
BBOX = (14.410, 35.886, 14.430, 35.900)
TOK = json.load(urllib.request.urlopen(
    "https://planetarycomputer.microsoft.com/api/sas/v1/token/sentinel-2-l2a", timeout=60))["token"]


def search(dt, cloud=10):
    out, seen, nxt = [], set(), {"collections": ["sentinel-2-l2a"], "bbox": list(BBOX), "datetime": dt,
                                 "query": {"eo:cloud_cover": {"lt": cloud}}, "limit": 100}
    while nxt:
        req = urllib.request.Request(STAC, json.dumps(nxt).encode(), {"Content-Type": "application/json"})
        page = json.load(urllib.request.urlopen(req, timeout=120))
        for f in page["features"]:
            d = f["properties"]["datetime"][:10]
            if d not in seen:
                seen.add(d)
                out.append(f)
        link = [l for l in page.get("links", []) if l.get("rel") == "next"]
        nxt = link[0].get("body") if link else None
    return sorted(out, key=lambda f: f["properties"]["datetime"])


def read(f, band):
    with rasterio.open(f["assets"][band]["href"] + "?" + TOK) as src:
        w = from_bounds(*transform_bounds("EPSG:4326", src.crs, *BBOX), transform=src.transform)
        return src.read(1, window=w, boundless=True, fill_value=0).astype("float32"), src.window_transform(w), src.crs


def ndvi(f):
    r, tr, crs = read(f, "B04")
    n = read(f, "B08")[0]
    scl = read(f, "SCL")[0]
    if scl.shape != r.shape:
        scl = np.kron(scl, np.ones((2, 2)))[: r.shape[0], : r.shape[1]]
    v = (n - r) / np.maximum(n + r, 1)
    v[~np.isin(scl, [4, 5, 6, 7])] = np.nan
    return v, tr, crs


def brightness(f):
    return np.mean([read(f, b)[0] for b in ("B02", "B03", "B04")], 0)


def main():
    ref = search("2026-02-01/2026-02-28")[0]
    _, tr, crs = ndvi(ref)
    shape = read(ref, "B04")[0].shape
    T = Transformer.from_crs("EPSG:4326", crs, always_xy=True)
    poly_ll = json.load(open(D / "osm_park_polygon.geojson"))["features"][0]["geometry"]["coordinates"][0]
    poly = {"type": "Polygon", "coordinates": [[T.transform(x, y) for x, y in poly_ll]]}
    inpoly = rasterize([(poly, 1)], out_shape=shape, transform=tr).astype(bool)

    med = lambda dt: np.median(np.stack([brightness(f) for f in search(dt, 5)[:6]]), 0)
    db = med("2025-08-15/2025-09-30") - med("2024-08-15/2024-09-30")
    thr = np.percentile(db[~inpoly], 95)
    zone = inpoly & (db > thr)
    lab, n = ndimage.label(zone)
    sizes = ndimage.sum(zone, lab, range(1, n + 1))
    zone = np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s >= 5])
    ctrl = inpoly & ~ndimage.binary_dilation(zone, iterations=2)
    Ti = Transformer.from_crs(crs, "EPSG:4326", always_xy=True)
    feats = [{"type": "Feature", "properties": {"threshold_brightness_change": round(float(thr))},
              "geometry": {"type": "Polygon", "coordinates": [[list(Ti.transform(x, y)) for x, y in g["coordinates"][0]]]}}
             for g, v in shapes(zone.astype("uint8"), mask=zone, transform=tr) if v == 1]
    json.dump({"type": "FeatureCollection", "features": feats,
               "properties": {"pixels": int(zone.sum()), "area_m2": int(zone.sum() * 100),
                              "control_pixels": int(ctrl.sum())}}, open(D / "gravel_zone.geojson", "w"))
    print("zone", zone.sum() * 100, "m2; control", ctrl.sum(), "px; threshold", round(float(thr)))

    rows = []
    for f in search("2023-01-01/2026-10-03"):
        v, _, _ = ndvi(f)
        if np.isnan(v[zone]).mean() > 0.3 or np.isnan(v[ctrl]).mean() > 0.3:
            continue
        b = brightness(f)
        rows.append([f["properties"]["datetime"][:10], f["id"], round(float(np.nanmedian(v[zone])), 4),
                     round(float(np.nanmedian(v[ctrl])), 4), round(float(np.median(b[zone]))),
                     round(float(np.median(b[ctrl])))])
    with open(D / "ndvi_timeseries.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["date", "scene", "ndvi_gravel_zone", "ndvi_control", "brightness_gravel_zone", "brightness_control"])
        w.writerows(rows)
    print(len(rows), "scenes")

    crops = {}
    for key, dt in (("feb2025", "2025-02-17/2025-02-26"), ("feb2026", "2026-02-20/2026-02-26")):
        f = search(dt)[0]
        rgb = np.dstack([read(f, b)[0] for b in ("B04", "B03", "B02")])
        crops[key] = (np.clip(rgb / 2500, 0, 1) * 255).astype("uint8")
        crops[key + "_date"] = f["properties"]["datetime"][:10]
    crops["zone"] = zone
    crops["poly_rc"] = np.array([rasterio.transform.rowcol(tr, *T.transform(x, y)) for x, y in poly_ll])
    np.savez_compressed(D / "rgb_crops.npz", **crops)


if __name__ == "__main__":
    main()
