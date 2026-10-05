#!/usr/bin/env python3
"""CC-019 (v1.2): Amphora's change polygons against the independent land cover, and the CORINE change layers.

Needs network and numpy, scipy, rasterio, pyproj, shapely. Steps:
1. Downloads Amphora Media's change polygons (the GeoJSON behind its Green to Grey map) to out/malta-change.geojson.
   The file is NOT committed (its licence is not stated); data/cc-019/amphora_record.csv records the URL, SHA-256, size,
   server date and the file's own metadata. data/cc-019/amphora_classes.csv: polygons and area per 2018 class.
   Areas are computed from the geometry in UTM 33N (EPSG:32633); the file's own 'area_m2' field is summed alongside.
2. Reads Impact Observatory / Esri 10 m annual land cover on the v1.0 pixel grid (data/cc-019/io_lulc_grid.json):
   2017-2023 from Microsoft Planetary Computer (as fetch_data.py) and 2017-2025 from Esri's Living Atlas image service
   (Sentinel2_10m_LandCover, one year per request, nearest neighbour, no rendering). The Esri maps are used only if they
   reproduce the Planetary Computer maps for 2017-2023 pixel for pixel (data/cc-019/io_esri_series.csv).
   Arrays are cached in out/io_*.npy (git-ignored).
3. Rasterises Amphora's polygons on that grid (pixel centres) and measures, for each persistence rule (fetch_data.py,
   plus rules that use the 2024 and 2025 maps), how much of Amphora's area the independent data class as new built-up
   land, how much of the independent new built-up land lies inside Amphora's polygons, and what Amphora's area was in
   the 2018 map. A 20 m tolerance (two pixels) tests whether the result depends on small misalignments.
   Writes data/cc-019/io_lulc_change_ext.csv and data/cc-019/amphora_io_overlap.csv.
4. Queries the EEA's CORINE Land Cover change layers (CHA 2006-2012 and 2012-2018, discomap map service) for Malta:
   data/cc-019/corine_change.csv. Change layers map changes of at least 5 ha (the service's layer description).
"""
import csv, datetime, hashlib, json, pathlib, urllib.parse, urllib.request
import numpy as np, pyproj, rasterio
from rasterio import features
from rasterio.windows import from_bounds
from rasterio.warp import transform_bounds
from scipy import ndimage
from shapely.geometry import shape
from shapely.ops import transform

HERE = pathlib.Path(__file__).resolve().parent
D = HERE.parents[1] / "data" / "cc-019"
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
TODAY = datetime.date.today().isoformat()
AMPHORA = "https://www.amphora.media/greentogrey/data/malta-change.geojson"
STAC = "https://planetarycomputer.microsoft.com/api/stac/v1"
ESRI = "https://ic.imagery1.arcgis.com/arcgis/rest/services/Sentinel2_10m_LandCover/ImageServer"
CLC = "https://image.discomap.eea.europa.eu/arcgis/rest/services/Corine/{}/MapServer/0/query"
BBOX = (14.17, 35.78, 14.59, 36.09)  # as fetch_data.py
NAMES = {1: "water", 2: "trees", 4: "flooded vegetation", 5: "crops", 7: "built area", 8: "bare ground",
         9: "snow/ice", 10: "clouds", 11: "rangeland"}
P = pyproj.Transformer.from_crs(4326, 32633, always_xy=True).transform
GEOD = pyproj.Geod(ellps="WGS84")


UA = {"User-Agent": "Mizien fact-check (github.com/leandergrech/Mizien)"}  # the site refuses Python's default agent


def get(url, params=None, timeout=300):
    return urllib.request.urlopen(urllib.request.Request(url + ("?" + urllib.parse.urlencode(params) if params else ""),
                                                         headers=UA), timeout=timeout)


def write(name, rows):
    with open(D / name, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\r\n")
        w.writeheader()
        w.writerows(rows)


# ---------------------------------------------------------------- 1. Amphora's polygons
r = get(AMPHORA)
raw = r.read()
(OUT / "malta-change.geojson").write_bytes(raw)
gj = json.loads(raw)
meta = gj.get("properties", {})
write("amphora_record.csv", [{
    "url": AMPHORA, "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
    "server_last_modified": r.headers.get("Last-Modified", ""), "file_generatedAt": meta.get("generatedAt", ""),
    "file_source": meta.get("source", ""), "file_featureCount": meta.get("featureCount", ""),
    "file_missingLc2018": meta.get("missingLc2018", ""), "file_yearRange": "-".join(map(str, meta.get("yearRange", []))),
    "retrieved": TODAY, "licence": "not stated; file not committed"}])
polys = [(shape(f["geometry"]), f["properties"]) for f in gj["features"]]
utm = [transform(P, g) for g, _ in polys]
cls = {}
for (g, p), u in zip(polys, utm):
    c = cls.setdefault(p["lc2018"], {"polygons": 0, "area_m2": 0.0, "area_m2_geodesic": 0.0, "area_m2_field": 0.0})
    c["polygons"] += 1
    c["area_m2"] += u.area
    c["area_m2_geodesic"] += abs(GEOD.geometry_area_perimeter(g)[0])
    c["area_m2_field"] += p["area_m2"]
tot = {k: sum(c[k] for c in cls.values()) for k in ("polygons", "area_m2", "area_m2_geodesic", "area_m2_field")}
known = {k: tot[k] - cls["unknown"][k] for k in tot}
rows = []
for name, c in sorted(cls.items(), key=lambda x: -x[1]["area_m2"]) + [("all", tot)]:
    rows.append({"lc2018": name, "polygons": c["polygons"], "area_m2": round(c["area_m2"]),
                 "area_m2_geodesic": round(c["area_m2_geodesic"]), "area_m2_field": round(c["area_m2_field"]),
                 "share_of_all_pct": round(100 * c["area_m2"] / tot["area_m2"], 1),
                 "share_of_known_pct": "" if name in ("unknown", "all") else round(100 * c["area_m2"] / known["area_m2"], 1),
                 "share_of_known_by_count_pct": "" if name in ("unknown", "all")
                 else round(100 * c["polygons"] / known["polygons"], 1),
                 "share_of_known_by_field_pct": "" if name in ("unknown", "all")
                 else round(100 * c["area_m2_field"] / known["area_m2_field"], 1)})
write("amphora_classes.csv", rows)
for x in rows:
    print(x)

# ---------------------------------------------------------------- 2. independent land cover on the v1.0 grid
G = json.load(open(D / "io_lulc_grid.json"))
a, _, x0, _, e, y0 = G["transform"]


def pc_years():
    tok = json.load(get("https://planetarycomputer.microsoft.com/api/sas/v1/token/io-lulc-annual-v02"))["token"]
    body = json.dumps({"collections": ["io-lulc-annual-v02"], "bbox": list(BBOX), "limit": 50}).encode()
    feats = json.load(urllib.request.urlopen(urllib.request.Request(STAC + "/search", body,
                                                                    {"Content-Type": "application/json"}), timeout=60))
    for f in feats["features"]:
        yr = f["properties"]["start_datetime"][:4]
        if (OUT / f"io_pc_{yr}.npy").exists():
            continue
        with rasterio.open(f["assets"]["data"]["href"] + "?" + tok) as src:
            w = from_bounds(*transform_bounds("EPSG:4326", src.crs, *BBOX), transform=src.transform)
            assert list(src.window_transform(w))[:6] == G["transform"], "grid differs from v1.0"
            np.save(OUT / f"io_pc_{yr}.npy", src.read(1, window=w, boundless=True, fill_value=0))


pc_years()
PC = {y: np.load(OUT / f"io_pc_{y}.npy") for y in map(str, range(2017, 2024))}
H, W = PC["2017"].shape
items = json.load(get(f"{ESRI}/query", {"where": "1=1", "outFields": "OBJECTID,ProductName", "returnGeometry": "false",
                                         "geometry": ",".join(map(str, BBOX)), "geometryType": "esriGeometryEnvelope",
                                         "inSR": 4326, "f": "json"}))["features"]
ES = {}
for it in items:
    oid, yr = it["attributes"]["OBJECTID"], it["attributes"]["ProductName"]
    fn = OUT / f"io_esri_{yr}.npy"
    if not fn.exists():
        q = {"bbox": f"{x0},{y0 + H * e},{x0 + W * a},{y0}", "bboxSR": 32633, "imageSR": 32633, "size": f"{W},{H}",
             "format": "tiff", "pixelType": "U8", "interpolation": "RSP_NearestNeighbor", "noData": 0, "f": "image",
             "mosaicRule": json.dumps({"mosaicMethod": "esriMosaicLockRaster", "lockRasterIds": [oid]}),
             "renderingRule": json.dumps({"rasterFunction": "None"})}
        with rasterio.MemoryFile(get(f"{ESRI}/exportImage", q).read()) as m, m.open() as s:
            assert s.shape == (H, W) and abs(s.transform.c - x0) < 0.01 and abs(s.transform.f - y0) < 0.01
            np.save(fn, s.read(1))
    ES[yr] = np.load(fn)
YRS = sorted(ES)
land = np.all([(ES[y] != 1) & (ES[y] != 0) for y in YRS], axis=0)
KM2 = 1e-4
series = []
for y in YRS:
    row = {"year": y, "source": "Esri Living Atlas"}
    if y in PC:
        v = PC[y] > 0
        row["identical_to_planetary_computer_pct"] = round(100 * ((ES[y] == PC[y]) & v).sum() / v.sum(), 3)
    else:
        row["identical_to_planetary_computer_pct"] = "n/a (not on Planetary Computer)"
    for k in (7, 5, 11, 8, 2):
        row[NAMES[k].replace(" ", "_") + "_km2"] = round(((ES[y] == k) & land).sum() * KM2, 2)
    series.append(row)
    print(row)
write("io_esri_series.csv", series)
same = all(r["identical_to_planetary_computer_pct"] == 100.0 for r in series if r["year"] in PC)
print("Esri reproduces the Planetary Computer maps 2017-2023:", same)
Y = ES if same else PC

# ---------------------------------------------------------------- 3. overlap with Amphora's polygons
A = features.rasterize([(u, 1) for u in utm], out_shape=(H, W), transform=rasterio.Affine(a, 0, x0, 0, e, y0),
                       fill=0, dtype="uint8").astype(bool)
A20 = ndimage.binary_dilation(A, iterations=2)
B = {y: Y[y] == 7 for y in Y}
nb = lambda ys: np.all([~B[y] for y in ys], axis=0)
bb = lambda ys: np.all([B[y] for y in ys], axis=0)
rules = {"strict": (("2017", "2018", "2019"), ("2021", "2022", "2023"), "first mapped as built in 2020-21"),
         "two-year": (("2017", "2018"), ("2022", "2023"), "first mapped as built in 2019-22"),
         "single-year": (("2018",), ("2023",), "2018 vs 2023 maps only (noisy)")}
if same:
    rules |= {"strict-2025": (("2017", "2018", "2019"), ("2023", "2024", "2025"), "first mapped as built in 2020-23"),
              "two-year-2025": (("2017", "2018"), ("2024", "2025"), "first mapped as built in 2019-24")}
ch, ov = [], []
add = lambda m, v, u, n="": ov.append({"measure": m, "value": v, "unit": u, "note": n})
add("Amphora polygons: area (UTM 33N geometry)", round(sum(u.area for u in utm)), "m2")
add("Amphora polygons: pixels whose centre falls inside", int(A.sum()), "pixels",
    f"{A.sum() * 100:,} m2 at 100 m2 per pixel")
for yr in ("2018", "2023") + (("2025",) if same else ()):
    u, c = np.unique(Y[yr][A], return_counts=True)
    for k, n in zip(u, c):
        add(f"Amphora area in the {yr} map: {NAMES.get(int(k), 'no data')}", round(100 * n / A.sum(), 1), "%")
ar = np.array([u.area for u in utm])
add("Amphora polygons: median area", round(float(np.median(ar))), "m2",
    f"{(ar < 1000).sum()} of {len(ar)} polygons under 1,000 m2, holding {100 * ar[ar < 1000].sum() / ar.sum():.0f}% "
    "of the area")
core = ndimage.binary_erosion(A, iterations=2)
for lab, m in (("Amphora area", A), ("Amphora area at least 20 m inside a polygon edge", core)):
    add(f"{lab}: built in the 2018 map", round(100 * (m & (Y['2018'] == 7)).sum() / m.sum(), 1), "%",
        f"{m.sum()} pixels")
    allb = np.all([Y[y] == 7 for y in ("2017", "2018", "2019")], axis=0)
    nob = np.all([Y[y] != 7 for y in ("2017", "2018", "2019")], axis=0)
    add(f"{lab}: built in all of the 2017, 2018 and 2019 maps", round(100 * (m & allb).sum() / m.sum(), 1), "%")
    add(f"{lab}: built in none of the 2017, 2018 and 2019 maps", round(100 * (m & nob).sum() / m.sum(), 1), "%")
add("Amphora area: built, year by year", "; ".join(f"{y} {100 * (A & (Y[y] == 7)).sum() / A.sum():.0f}%" for y in sorted(Y)),
    "%")
for name, (pre, post, win) in rules.items():
    gain = land & nb(pre) & bb(post)
    loss = land & bb(pre) & nb(post)
    u, c = np.unique(Y["2018"][gain], return_counts=True)
    sh = {NAMES[int(k)]: round(100 * n / c.sum(), 1) for k, n in zip(u, c)}
    ch.append({"rule": name, "window": win, "years": "maps " + ",".join(pre) + " -> " + ",".join(post),
               "new_built_km2": round(gain.sum() * KM2, 3), "reverse_km2": round(loss.sum() * KM2, 3),
               "net_km2": round((gain.sum() - loss.sum()) * KM2, 3), "from_crops_pct": sh.get("crops", 0),
               "from_rangeland_pct": sh.get("rangeland", 0), "from_bare_pct": sh.get("bare ground", 0),
               "from_trees_pct": sh.get("trees", 0), "maps": "Esri 2017-2025" if same else "Planetary Computer"})
    add(f"{name}: share of Amphora's area that IO maps as new built-up", round(100 * (gain & A).sum() / A.sum(), 1),
        "%", win)
    add(f"{name}: share of IO new built-up inside Amphora's polygons", round(100 * (gain & A).sum() / gain.sum(), 1),
        "%", f"{(gain & A).sum() * KM2:.3f} of {gain.sum() * KM2:.3f} km2")
    add(f"{name}: share of IO new built-up within 20 m of Amphora's polygons",
        round(100 * (gain & A20).sum() / gain.sum(), 1), "%", "tolerance for misalignment")
    if name == "two-year-2025" or (not same and name == "two-year"):
        rr, cc = np.nonzero(gain)
        np.savetxt(OUT / "new_built_for_map.csv", np.c_[rr, cc], fmt="%d", delimiter=",", header="row,col", comments="")
for x in ch:
    print(x)
for x in ov:
    print(f"{x['measure']:80s} {x['value']!s:>10} {x['unit']} {x['note']}")
write("io_lulc_change_ext.csv", ch)
for x in ov:
    x["retrieved"] = TODAY
write("amphora_io_overlap.csv", ov)

# ---------------------------------------------------------------- 4. CORINE land cover change layers
clc = []
for svc, period, c0, c1 in (("CHA2006_2012_WM", "2006-2012", "code_06", "code_12"),
                            ("CHA2012_2018_WM", "2012-2018", "Code_12", "Code_18")):
    q = {"geometry": ",".join(map(str, BBOX)), "geometryType": "esriGeometryEnvelope", "inSR": 4326, "outSR": 4326,
         "spatialRel": "esriSpatialRelIntersects", "outFields": "*", "returnGeometry": "true", "f": "geojson"}
    for f in json.load(get(CLC.format(svc), q))["features"]:
        p = f["properties"]
        g = shape(f["geometry"])
        frm, to = str(p[c0]), str(p[c1])
        clc.append({"period": period, "id": p["ID"], "from_code": frm, "to_code": to,
                    "area_ha": round(p.get("Area_ha") or p.get("Area_Ha"), 2),
                    "land_take": "yes" if to.startswith("1") and not frm.startswith("1") else "no",
                    "lon": round(g.centroid.x, 4), "lat": round(g.centroid.y, 4), "source": CLC.format(svc),
                    "retrieved": TODAY})
for x in clc:
    print(x)
write("corine_change.csv", clc)
