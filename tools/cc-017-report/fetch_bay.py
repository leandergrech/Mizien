#!/usr/bin/env python3
"""CC-017 (v1.2): data for the Marsaxlokk Bay map, and the statistics drawn from it.

Needs network and numpy, rasterio, pyproj, shapely. The map frame is FRAME (lon/lat). Writes:
  data/cc-017/natura2000_bay.geojson   Natura 2000 sites in the frame, full-resolution boundaries from the EEA service
                                       (2024 release, layers 0 and 1), clipped to the frame (EEA data, as
                                       natura2000.geojson).
  data/cc-017/seagrass_emodnet_bay.geojson  EMODnet Seabed Habitats 'Seagrass cover (EOV)' polygons, version 2025
                                       (European subset, CC BY 4.0), clipped to the frame (map EUSM16me, 2016, gridded
                                       at about 230 m; the source field is blank for the polygons in the bay). The only
                                       seagrass layer used (maintainer decision, 5 Oct 2026).
  data/cc-017/article17_1120_mt.csv    Malta's Article 17 assessment of habitat 1120 (Posidonia beds), periods 2013-2018
                                       and 2019-2024, parsed from the EEA Article 17 web tool.
  data/cc-017/bay_stats.csv            derived statistics (seagrass area and distance, depths) for the report.
  out/bathymetry_bay.tif               EMODnet Digital Bathymetry (DTM 2024) for the frame, via the EMODnet WCS
                                       (coverage emodnet__mean, 1/16 arc-minute cells). Kept in out/ only.
New land at Terminal 2 = the Sentinel-2 pixels that are land in summer 2026 and sea in summer 2023, in connected groups
of at least 20 pixels, placed as in distances.py (data/cc-017/s2_mask_*.csv).

  python fetch_bay.py           fetch everything (network), then compute the statistics
  python fetch_bay.py --stats   statistics only (offline), from the committed files and out/bathymetry_bay.tif
"""
import csv, datetime, html, json, math, pathlib, re, sys, urllib.parse, urllib.request
import numpy as np, pyproj, rasterio, shapely
from rasterio.warp import transform_bounds
from scipy import ndimage
from shapely import make_valid
from shapely.geometry import Polygon, box, mapping, shape
from shapely.ops import transform, unary_union

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
D = ROOT / "data" / "cc-017"
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
TODAY = datetime.date.today().isoformat()
FRAME = (14.505, 35.795, 14.600, 35.862)
N2K = "https://bio.discomap.eea.europa.eu/arcgis/rest/services/ProtectedSites/Natura2000Sites/MapServer"
SBH = "https://ows.emodnet-seabedhabitats.eu/geoserver/emodnet_open/wfs"
WCS = "https://ows.emodnet-bathymetry.eu/wcs"
A17 = "https://nature-art17.eionet.europa.eu/article17/habitat/summary/?period={}&subject=1120"
P = pyproj.Transformer.from_crs(4326, 32633, always_xy=True).transform
FR = box(*FRAME)
FRU = transform(P, FR)


def get(url, params=None, timeout=180):
    return urllib.request.urlopen(url + ("?" + urllib.parse.urlencode(params) if params else ""), timeout=timeout).read()


def rnd(c):
    return [rnd(x) for x in c] if isinstance(c[0], (list, tuple)) else [round(c[0], 6), round(c[1], 6)]


def fc(feats):
    out = []
    for g, props in feats:
        g = make_valid(g).intersection(FR)
        if g.is_empty or g.area == 0:
            continue
        gm = mapping(g)
        if gm["type"] == "GeometryCollection":
            polys = [p for p in g.geoms if p.geom_type in ("Polygon", "MultiPolygon")]
            gm = mapping(unary_union(polys))
        out.append({"type": "Feature", "properties": props, "geometry": {"type": gm["type"],
                                                                          "coordinates": rnd(gm["coordinates"])}})
    return {"type": "FeatureCollection", "features": out}


# ---------------------------------------------------------------- new land at Terminal 2 (as distances.py)
BBOX = (14.515, 35.805, 14.555, 35.835)
ROW0, COL0 = 110, 180
minx, _, _, maxy = transform_bounds("EPSG:4326", "EPSG:32633", *BBOX)
x0, y0 = minx + COL0 * 10, maxy - ROW0 * 10
m23 = np.loadtxt(D / "s2_mask_2023.csv", delimiter=",")
m26 = np.loadtxt(D / "s2_mask_2026.csv", delimiter=",")
lab, n = ndimage.label((m26 == 1) & (m23 == 0))
keep = [i for i in range(1, n + 1) if (lab == i).sum() >= 20]
r, c = np.nonzero(np.isin(lab, keep))
NEW = unary_union([box(x0 + j * 10, y0 - (i + 1) * 10, x0 + (j + 1) * 10, y0 - i * 10) for i, j in zip(r, c)])
print(f"new land {NEW.area / 1e4:.2f} ha")


def fetch():
    # ------------------------------------------------------------ 1. Natura 2000, full resolution
    n2k = []
    for layer, kind in ((0, "SAC"), (1, "SPA")):
        q = {"geometry": ",".join(map(str, FRAME)), "geometryType": "esriGeometryEnvelope", "inSR": 4326, "outSR": 4326,
             "spatialRel": "esriSpatialRelIntersects", "where": "MS='MT'", "outFields": "SITECODE,SITENAME",
             "returnGeometry": "true", "f": "geojson"}
        for ft in json.loads(get(f"{N2K}/{layer}/query", q))["features"]:
            p = ft["properties"]
            n2k.append((shape(ft["geometry"]), {"sitecode": p["SITECODE"], "sitename": p["SITENAME"], "type": kind}))
    json.dump(fc(n2k), open(D / "natura2000_bay.geojson", "w"), ensure_ascii=False, separators=(",", ":"))
    print(len(n2k), "Natura 2000 designations in the frame:", sorted(f"{p['sitecode']} {p['type']}" for _, p in n2k))

    # ------------------------------------------------------------ 2. seagrass: EMODnet Seabed Habitats (CC BY 4.0)
    q = {"service": "WFS", "version": "1.1.0", "request": "GetFeature", "typeName": "emodnet_open:seagrass_eov_poly_2025",
         "bbox": f"{FRAME[1]},{FRAME[0]},{FRAME[3]},{FRAME[2]},urn:ogc:def:crs:EPSG::4326",
         "outputFormat": "application/json", "srsName": "EPSG:4326"}
    em = [(shape(f["geometry"]), {k: f["properties"][k] for k in ("habsubtype", "anxi_code", "map_id", "source",
                                                                  "det_date")})
          for f in json.loads(get(SBH, q))["features"]]
    json.dump(fc(em), open(D / "seagrass_emodnet_bay.geojson", "w"), ensure_ascii=False, separators=(",", ":"))
    print(len(em), "EMODnet seagrass polygons in the frame")

    # ------------------------------------------------------------ 3. depth: EMODnet DTM 2024
    url = (f"{WCS}?service=WCS&version=2.0.1&request=GetCoverage&coverageId=emodnet__mean&subset=Lat({FRAME[1] - 0.01},"
           f"{FRAME[3] + 0.01})&subset=Long({FRAME[0] - 0.01},{FRAME[2] + 0.01})&format=image/tiff")
    open(OUT / "bathymetry_bay.tif", "wb").write(get(url))

    # ------------------------------------------------------------ 4. Article 17, habitat 1120, Malta
    a17 = []
    for period, label in ((5, "2013-2018"), (6, "2019-2024")):
        t = get(A17.format(period)).decode("utf-8", "replace")
        m = list(re.finditer(r"(?:<span>|>)\s*MT\s*(?:</span>|</a>)\s*</td>", t))[-1]
        row = t[m.end():t.index("</tr>", m.end())]
        sec = dict(re.findall(r"<!--\s*([A-Za-z ]+?)\s*-->(.*?)(?=<!--|$)", row, flags=re.S))
        td = lambda s: [re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", x))).strip()
                        for x in re.findall(r"<td[^>]*>(.*?)</td>", s, flags=re.S)]
        concl = lambda s: re.findall(r'class="conclusion[^"]*">\s*([^<]*?)\s*<', s)
        ar, sf = td(sec["Area"]), td(sec["Structure and functions"])
        ov = td(sec["Overall assessment"])
        a17.append({"period": label, "region": "MMED", "range_km2": td(sec["Range"])[0],
                    "range_status": re.search(r'class="(\w+) "\s*>\s*<span class="conclusion', sec["Range"]).group(1),
                    "area_km2": ar[2], "area_method": ar[4],
                    "area_status": re.search(r'class="(\w+) "\s*>\s*<span class="conclusion', sec["Area"]).group(1),
                    "sf_good_km2": sf[0], "sf_not_good_km2": sf[1], "sf_status": concl(sec["Structure and functions"])[0],
                    "future_status": concl(sec["Future prospects"])[0],
                    "overall_status": concl(sec["Overall assessment"])[0],
                    "overall_trend": ov[1], "source": A17.format(period), "retrieved": TODAY})
        print(a17[-1])
    with open(D / "article17_1120_mt.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(a17[0]), lineterminator="\r\n")
        w.writeheader()
        w.writerows(a17)


if "--stats" not in sys.argv:
    fetch()

# ---------------------------------------------------------------- 5. statistics (from the committed files and out/)
rows = []


def add(item, value, unit, source, note=""):
    rows.append({"item": item, "value": value, "unit": unit, "source": source, "note": note, "retrieved": TODAY})
    print(f"{item:78s} {value!s:>12} {unit:4s} {note}")


EM, SRC = "EMODnet Seabed Habitats 2025 (map EUSM16me)", "EMODnet Seabed Habitats (2025)"
emf = json.load(open(D / "seagrass_emodnet_bay.geojson"))["features"]
SG = make_valid(unary_union([make_valid(transform(P, shape(f["geometry"]))) for f in emf])).buffer(0).intersection(FRU)
# the map's grid: spacing of the polygon vertices (one-cell steps only), in degrees and in metres
ux = np.diff(sorted({round(x, 6) for f in emf for x, _ in shape(f["geometry"]).exterior.coords}))
uy = np.diff(sorted({round(y, 6) for f in emf for _, y in shape(f["geometry"]).exterior.coords}))
dx, dy = ux[(ux > 0.0015) & (ux < 0.0025)].mean(), uy[(uy > 0.0015) & (uy < 0.0025)].mean()
lat0 = (FRAME[1] + FRAME[3]) / 2
cw, ch = dx * 111320 * math.cos(math.radians(lat0)), dy * 110574
# coastline (OpenStreetMap, docs/data/geo.json): how far the grid cells reach onto land
geo = json.load(open(ROOT / "docs" / "data" / "geo.json"))
o = geo["origin"]
k = 111320 * math.cos(math.radians(o["lat"]))
rr = [i for i in geo["islands"] if i["name"] == "Malta"][0]["detail"]
LAND = make_valid(Polygon([P(o["lon"] + rr[i] / k, o["lat"] + rr[i + 1] / 110574) for i in range(0, len(rr) - 1, 2)]))

add(f"Mapped P. oceanica in the map frame: {EM}", round(SG.area / 1e4, 1), "ha", SRC,
    f"frame {FRAME}; {len(emf)} polygons, about {SG.area / (cw * ch):.0f} grid cells")
add("EMODnet seagrass map EUSM16me: grid cell size", f"{cw:.0f} x {ch:.0f}", "m", SRC,
    f"east-west x north-south; vertex spacing {dx:.5f} x {dy:.5f} degrees")
add(f"Mapped P. oceanica on land (OpenStreetMap coastline) in the map frame: {EM}",
    round(SG.intersection(LAND).area / 1e4, 1), "ha", SRC, "grid cells that overlap the coast")
for km in (0.5, 1, 2):
    g = SG.intersection(NEW.buffer(km * 1000))
    add(f"Mapped P. oceanica within {km} km of the new land: {EM}", round(g.area / 1e4, 1), "ha", SRC,
        f"of which on land (OpenStreetMap coastline): {g.intersection(LAND).area / 1e4:.1f} ha")
add(f"Shortest distance, new land to mapped P. oceanica: {EM}", round(SG.distance(NEW) / 1000, 2), "km", SRC,
    f"to the nearest grid cell; cells about {cw:.0f} x {ch:.0f} m, so the map cannot place a meadow's edge more "
    "precisely than about one cell")

with rasterio.open(OUT / "bathymetry_bay.tif") as s:
    a = s.read(1).astype(float)
    H, W = a.shape
    lon = s.bounds.left + (np.arange(W) + 0.5) * s.res[0]
    lat = s.bounds.top - (np.arange(H) + 0.5) * s.res[1]
GX, GY = P(*np.meshgrid(lon, lat))
sea = a < 0
dep = -a
add("EMODnet DTM 2024 cell size", f"{s.res[0] * 3600:.2f} arc-seconds", "", "EMODnet Bathymetry Consortium (2024)",
    "about 95 m east-west by 115 m north-south")
pct = lambda d: " / ".join(f"{v:.0f}" for v in np.percentile(d, [10, 50, 90]))
for km in (0.5, 1, 2):
    near = sea & shapely.contains_xy(NEW.buffer(km * 1000), GX, GY)
    d = dep[near]
    add(f"Depth of the sea within {km} km of the new land: 10th / 50th / 90th percentile", pct(d), "m",
        "EMODnet Bathymetry Consortium (2024)",
        f"{near.sum()} grid cells; shallower than 10 m: {100 * (d < 10).mean():.0f}%; shallower than 20 m: "
        f"{100 * (d < 20).mean():.0f}%")
on = sea & shapely.contains_xy(SG, GX, GY)
add(f"Depth of grid cells on mapped P. oceanica in the frame: 10th / 50th / 90th percentile ({EM})", pct(dep[on]), "m",
    "EMODnet Bathymetry Consortium (2024)", f"{on.sum()} grid cells")
for km in (0.5, 1):
    on = sea & shapely.contains_xy(SG.intersection(NEW.buffer(km * 1000)), GX, GY)
    add(f"Depth of grid cells on mapped P. oceanica within {km} km of the new land: 10th / 50th / 90th percentile "
        f"({EM})", pct(dep[on]), "m", "EMODnet Bathymetry Consortium (2024)", f"{on.sum()} grid cells")
with open(D / "bay_stats.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\r\n")
    w.writeheader()
    w.writerows(rows)
