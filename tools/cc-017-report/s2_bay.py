#!/usr/bin/env python3
"""CC-017 (v1.2): is there new land anywhere in Marsaxlokk Bay other than Freeport Terminal 2? A Sentinel-2 test.

Needs network and numpy, scipy, rasterio. For each summer (1 May to 15 October) it takes the eight Sentinel-2 L2A
scenes with the least cloud from one relative orbit, 36 (Microsoft Planetary Computer), masks cloud, cloud shadow and
snow with the scene classification layer (SCL 3, 8, 9, 10), and computes the per-pixel median of the modified
normalised difference water index, MNDWI = (green - SWIR1) / (green + SWIR1) (B03 at 10 m; B11 at 20 m, each cell
split into four 10 m pixels; Xu 2006). Reflectance is corrected for the +1000 offset of processing baseline 04.00 and
later. Land = median MNDWI < 0.

New land between two summers = pixels that are land in the later summer and sea in the earlier one, kept only in
connected groups of at least MIN_PX pixels (0.2 ha). Each group is labelled 'Terminal 2' if it touches the v1.1
Terminal 2 window (fetch_data.py) and 'elsewhere' otherwise. Two earlier pairs of summers, when no reclamation is known
in the bay, measure how much 'new land' the method finds by chance, and the reverse change (land to sea) is counted
for every pair. Writes data/cc-017/s2_mndwi_bay.csv (totals per pair) and data/cc-017/s2_mndwi_scenes.csv (scenes).

RESULT (5 Oct 2026): NOT ROBUST, NOT USED FOR FINDINGS. Over open water both bands are close to zero reflectance, so
the index changes sign from scene to scene (haze, glint, atmospheric correction). The control pairs gave 37-80 ha of
spurious 'new land' and up to 190 ha of 'land lost', and the summer 2026 median turned hundreds of hectares of sea
into 'land'. A first run that mixed relative orbits 36 and 79 failed in the same way. Kept as a record of the attempt
(report v1.2, section 8).
"""
import csv, json, pathlib, urllib.request
import numpy as np, rasterio
from rasterio.windows import bounds, from_bounds
from rasterio.warp import transform_bounds
from scipy import ndimage

D = pathlib.Path(__file__).resolve().parents[2] / "data" / "cc-017"
STAC = "https://planetarycomputer.microsoft.com/api/stac/v1/search"
FRAME = (14.505, 35.795, 14.600, 35.862)  # as fetch_bay.py
T2_BBOX, ROW0, COL0, NROW, NCOL = (14.515, 35.805, 14.555, 35.835), 110, 180, 100, 110  # v1.1 Terminal 2 window
MIN_PX = 20
ORBIT = 36  # one relative orbit for every summer, so the viewing geometry is the same
YEARS = ("2017", "2020", "2023", "2026")
PAIRS = (("2017", "2020", "control"), ("2020", "2023", "control"), ("2023", "2026", "test"))
TOK = json.load(urllib.request.urlopen(
    "https://planetarycomputer.microsoft.com/api/sas/v1/token/sentinel-2-l2a", timeout=60))["token"]


def search(yr):
    body = json.dumps({"collections": ["sentinel-2-l2a"], "bbox": list(FRAME), "datetime": f"{yr}-05-01/{yr}-10-15",
                       "query": {"eo:cloud_cover": {"lt": 10}}, "limit": 200}).encode()
    req = urllib.request.Request(STAC, body, {"Content-Type": "application/json"})
    feats = sorted(json.load(urllib.request.urlopen(req, timeout=120))["features"],
                   key=lambda f: f["properties"]["eo:cloud_cover"])
    seen, out = set(), []
    for f in feats:
        d = f["properties"]["datetime"][:10]
        p = f["properties"]
        if d not in seen and p["s2:mgrs_tile"] == "33SVV" and p["sat:relative_orbit"] == ORBIT:
            seen.add(d)
            out.append(f)
    return out[:8]


def window20(f):
    """The frame on the 20 m grid of the tile (B11, SCL), and the same bounds for the 10 m bands."""
    with rasterio.open(f["assets"]["B11"]["href"] + "?" + TOK) as src:
        w = from_bounds(*transform_bounds("EPSG:4326", src.crs, *FRAME), transform=src.transform)
        w = w.round_offsets().round_lengths()
        return bounds(w, src.transform)


def band(f, name, bnds):
    with rasterio.open(f["assets"][name]["href"] + "?" + TOK) as src:
        w = from_bounds(*bnds, transform=src.transform).round_offsets().round_lengths()
        a = src.read(1, window=w)
        if src.res[0] == 20:
            a = np.repeat(np.repeat(a, 2, axis=0), 2, axis=1)
        return a, src.window_transform(w)


SCENES = []


def summer(yr):
    stack, meta = [], None
    for f in search(yr):
        SCENES.append({"summer": yr, "date": f["properties"]["datetime"][:10], "id": f["id"],
                       "cloud_cover_pct": round(f["properties"]["eo:cloud_cover"], 2)})
        bn = window20(f)
        g, tr = band(f, "B03", bn)
        s, _ = band(f, "B11", bn)
        scl, _ = band(f, "SCL", bn)
        off = 1000 if float(f["properties"].get("s2:processing_baseline", "0")) >= 4 else 0
        g = np.clip(g.astype("float32") - off, 0, None)
        s = np.clip(s.astype("float32") - off, 0, None)
        m = (g - s) / np.maximum(g + s, 1)
        m[np.isin(scl, (0, 3, 8, 9, 10))] = np.nan
        stack.append(m)
        meta = meta or tr
    print(yr, len(stack), "scenes")
    return np.nanmedian(stack, axis=0), meta


med, tr = {}, None
for y in YEARS:
    med[y], tr = summer(y)
land = {y: med[y] < 0 for y in YEARS}
# the v1.1 Terminal 2 window in this grid
minx, _, _, maxy = transform_bounds("EPSG:4326", "EPSG:32633", *T2_BBOX)
tx0, ty1 = minx + COL0 * 10, maxy - ROW0 * 10
tx1, ty0 = tx0 + NCOL * 10, ty1 - NROW * 10
H, W = med[YEARS[0]].shape
X = tr.c + (np.arange(W) + 0.5) * tr.a
Y = tr.f + (np.arange(H) + 0.5) * tr.e
GX, GY = np.meshgrid(X, Y)
t2 = (GX >= tx0) & (GX <= tx1) & (GY >= ty0) & (GY <= ty1)
totals = []
for a, b, kind in PAIRS:
    for direction, ch in (("new land", land[b] & ~land[a]), ("land lost", land[a] & ~land[b])):
        lab, n = ndimage.label(ch)
        sizes = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
        res = {"pair": f"{a}->{b}", "kind": kind, "direction": direction, "terminal2_ha": 0.0, "elsewhere_ha": 0.0,
               "elsewhere_groups": 0, "largest_elsewhere_ha": 0.0}
        for i, sz in enumerate(sizes, start=1):
            if sz < MIN_PX:
                continue
            m = lab == i
            where = "Terminal 2" if (m & t2).any() else "elsewhere"
            ha = sz * 0.01
            if where == "Terminal 2":
                res["terminal2_ha"] += ha
            else:
                res["elsewhere_ha"] += ha
                res["elsewhere_groups"] += 1
                res["largest_elsewhere_ha"] = max(res["largest_elsewhere_ha"], ha)
        res = {k: round(v, 2) if isinstance(v, float) else v for k, v in res.items()}
        totals.append(res)
        print(res)
for y in YEARS:
    print(y, "land in the frame", round(land[y].sum() * 0.01, 1), "ha; in the Terminal 2 window",
          round((land[y] & t2).sum() * 0.01, 2), "ha")
with open(D / "s2_mndwi_bay.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(totals[0]), lineterminator="\r\n")
    w.writeheader()
    w.writerows(totals)
with open(D / "s2_mndwi_scenes.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(SCENES[0]), lineterminator="\r\n")
    w.writeheader()
    w.writerows(SCENES)
np.save(pathlib.Path(__file__).resolve().parent / "out" / "mndwi_2023_2026.npy",
        np.stack([med["2023"], med["2026"]]))
json.dump(list(tr)[:6], open(pathlib.Path(__file__).resolve().parent / "out" / "mndwi_grid.json", "w"))
