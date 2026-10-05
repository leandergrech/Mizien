#!/usr/bin/env python3
"""CC-019 (v1.2, maintainer decision 5 Oct 2026): spot-check a sample of Amphora's change polygons against high-resolution
satellite imagery from Esri World Imagery Wayback.

Needs network (first run), numpy, pillow, pyproj, shapely, and out/malta-change.geojson (crosscheck.py downloads it;
SHA-256 in data/cc-019/amphora_record.csv). Steps:

1. Sample. 40 draws by systematic probability-proportional-to-size (PPS) sampling on polygon area (UTM 33N): the
   polygons are put in a random order (seed SEED), laid end to end on a line of their areas, and a draw is taken every
   total/40 m2 from a random start. Each draw is a point on Amphora's area, so the share of draws that land in a
   confirmed polygon estimates the share of Amphora's AREA that is confirmed. A polygon larger than the interval can be
   drawn twice and then counts once per draw.
2. Imagery. For each sampled polygon the script walks back through the Wayback releases with Esri's tilemap endpoint
   (zoom-18 tile at the polygon centroid) to list the distinct imagery versions, and reads each version's acquisition
   date (SRC_DATE) from that release's imagery metadata layer at the centroid. Panels: "before" = the latest version
   acquired before 1 July 2018; "2018-19" = the earliest version acquired 1 July 2018 to 31 December 2019 (context only);
   "2023" = the latest version acquired in 2023 or earlier (checks the article's end year); "after" = the latest release.
   Tiles (zoom 19, or 18 where 19 has no data) are mosaicked over a square around the polygon, the outline is drawn on
   top, and the strip is saved as out/spotcheck/NN_iIII.png. Tiles and mosaics stay in out/ (git-ignored): Esri's terms
   do not allow redistribution, so only this script and the results are committed.
3. Classes, by eye, after looking at every strip (CLASS below; see the rules in the docstring of CLASS). Writes
   data/cc-019/imagery_spotcheck.csv (one row per sampled polygon) and data/cc-019/imagery_spotcheck_summary.csv
   (shares of draws by class, with Wilson 95% intervals).

Run: python spotcheck.py           (sample, imagery, strips; then classes if CLASS is filled in)
"""
import concurrent.futures as cf
import csv, datetime, io, json, math, pathlib, urllib.error, urllib.parse, urllib.request

import numpy as np, pyproj
from PIL import Image, ImageDraw, ImageFont
from shapely.geometry import shape
from shapely.ops import transform

HERE = pathlib.Path(__file__).resolve().parent
D = HERE.parents[1] / "data" / "cc-019"
OUT = HERE / "out"
SC = OUT / "spotcheck"
TILES = SC / "tiles"
TILES.mkdir(parents=True, exist_ok=True)
TODAY = datetime.date.today().isoformat()
SEED, N = 20261005, 40
CONFIG = "https://s3-us-west-2.amazonaws.com/config.maptiles.arcgis.com/waybackconfig.json"
WB = "https://wayback.maptiles.arcgis.com/arcgis/rest/services/World_Imagery"
TILE = WB + "/WMTS/1.0.0/default028mm/MapServer/tile/{r}/{z}/{y}/{x}"
TILEMAP = WB + "/MapServer/tilemap/{r}/{z}/{y}/{x}"
LAYER = {18: 5, 19: 4}  # metadata layer for a zoom level (60 cm and 30 cm layers; as the Wayback app)
UA = {"User-Agent": "Mizien fact-check (github.com/leandergrech/Mizien)"}
P = pyproj.Transformer.from_crs(4326, 32633, always_xy=True).transform
FONT = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
FONTB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def get(url, timeout=60, tries=4):
    for k in range(tries):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout).read()
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            if k == tries - 1:
                raise
        except Exception:
            if k == tries - 1:
                raise


# ---------------------------------------------------------------- 1. sample
gj = json.load(open(OUT / "malta-change.geojson"))
POLYS = [shape(f["geometry"]) for f in gj["features"]]
PROPS = [f["properties"] for f in gj["features"]]
AREA = np.array([transform(P, g).area for g in POLYS])
TOTAL = AREA.sum()
rng = np.random.default_rng(SEED)
order = rng.permutation(len(POLYS))
step = TOTAL / N
start = rng.uniform(0, step)
cum = np.cumsum(AREA[order])
points = start + step * np.arange(N)
hit = order[np.searchsorted(cum, points, side="right")]
DRAWS = {}
for i in hit:
    DRAWS[int(i)] = DRAWS.get(int(i), 0) + 1
SAMPLE = sorted(DRAWS, key=lambda i: list(hit).index(i))  # in draw order
print(f"total {TOTAL:,.0f} m2, interval {step:,.1f} m2, start {start:,.1f} m2; {len(SAMPLE)} polygons, {N} draws")


# ---------------------------------------------------------------- 2. imagery versions and dates
cfg = json.loads(get(CONFIG))
REL = sorted(((int(k), v["itemTitle"].split("Wayback ")[1].rstrip(")"), v["metadataLayerUrl"]) for k, v in cfg.items()),
             key=lambda t: t[1])
RIDX = {r: i for i, (r, _, _) in enumerate(REL)}
RDATE = {r: d for r, d, _ in REL}
RMETA = {r: m for r, _, m in REL}


def tile_of(lon, lat, z):
    n = 2 ** z
    x = (lon + 180) / 360 * n
    y = (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * n
    return x, y  # fractional tile coordinates


def meta(r, lon, lat, z, bbox=None):
    q = {"geometryType": "esriGeometryPoint" if bbox is None else "esriGeometryEnvelope",
         "geometry": f"{lon},{lat}" if bbox is None else ",".join(map(str, bbox)), "inSR": 4326,
         "spatialRel": "esriSpatialRelIntersects", "outFields": "SRC_DATE,SRC_RES,SRC_DESC,NICE_DESC",
         "returnGeometry": "false", "f": "json"}
    d = json.loads(get(f"{RMETA[r]}/{LAYER[z]}/query?" + urllib.parse.urlencode(q)))
    return [f["attributes"] for f in d.get("features", [])]


def versions(lon, lat, z=18):
    """Distinct imagery versions of the tile at (lon, lat), newest first: (release where it changed, SRC_DATE...)."""
    x, y = map(int, tile_of(lon, lat, z))
    i, out = len(REL) - 1, []
    while i >= 0:
        d = json.loads(get(TILEMAP.format(r=REL[i][0], z=z, y=y, x=x)))
        if not d.get("data") or d["data"][0] == 0:
            break
        s = d["select"][0] if d.get("select") else REL[i][0]
        m = meta(s, lon, lat, z)
        out.append({"release": s, "release_date": RDATE[s], "src_date": max((a["SRC_DATE"] for a in m), default=None),
                    "sensor": "/".join(sorted({a["SRC_DESC"].strip() for a in m})),
                    "res": min((round(a["SRC_RES"], 2) for a in m), default=None),
                    "provider": "/".join(sorted({(a["NICE_DESC"] or "").strip() for a in m}))})
        i = RIDX[s] - 1
    return out


VCACHE = SC / "versions.json"
VER = json.loads(VCACHE.read_text()) if VCACHE.exists() else {}


def work(i):
    if str(i) in VER:
        return
    c = POLYS[i].centroid
    VER[str(i)] = versions(c.x, c.y)


with cf.ThreadPoolExecutor(8) as ex:
    list(ex.map(work, SAMPLE))
VCACHE.write_text(json.dumps(VER, indent=1))


def pick(vs):
    """before / 2018-19 / 2023 / after versions from a newest-first list."""
    ok = [v for v in vs if v["src_date"]]
    before = next((v for v in ok if v["src_date"] < 20180701), None)
    mid = [v for v in ok if 20180701 <= v["src_date"] <= 20191231]
    y23 = next((v for v in ok if v["src_date"] <= 20231231), None)
    return before, (mid[-1] if mid else None), y23, (vs[0] if vs else None)


# ---------------------------------------------------------------- strips
def fetch_tile(r, z, y, x):
    fn = TILES / f"{r}_{z}_{y}_{x}.jpg"
    if not fn.exists():
        b = get(TILE.format(r=r, z=z, y=y, x=x))
        if b is None:
            return None
        fn.write_bytes(b)
    return Image.open(fn).convert("RGB")


def panel(i, v, size=460):
    """Mosaic of release v['release'] over a square around polygon i, outline on top; returns (image, zoom, dates)."""
    g = POLYS[i]
    x0, y0, x1, y1 = g.bounds
    u = transform(P, g)
    ux0, uy0, ux1, uy1 = u.bounds
    side = max(ux1 - ux0, uy1 - uy0) * 1.6 + 40  # metres
    c = g.centroid
    for z in (19, 18):
        xc, yc = tile_of((x0 + x1) / 2, (y0 + y1) / 2, z)
        mpp = 156543.03392 * math.cos(math.radians(c.y)) / 2 ** z  # ground metres per pixel
        half = side / 2 / mpp / 256  # in tiles
        tx0, tx1, ty0, ty1 = int(xc - half), int(xc + half), int(yc - half), int(yc + half)
        d = json.loads(get(TILEMAP.format(r=v["release"], z=z, y=int(tile_of(c.x, c.y, z)[1]),
                                          x=int(tile_of(c.x, c.y, z)[0]))))
        if z == 19 and (not d.get("data") or d["data"][0] == 0):
            continue
        jobs = [(v["release"], z, ty, tx) for ty in range(ty0, ty1 + 1) for tx in range(tx0, tx1 + 1)]
        with cf.ThreadPoolExecutor(8) as ex:
            ims = list(ex.map(lambda a: fetch_tile(*a), jobs))
        if z == 19 and any(im is None for im in ims):
            continue
        mos = Image.new("RGB", ((tx1 - tx0 + 1) * 256, (ty1 - ty0 + 1) * 256), (40, 40, 40))
        for (r, _, ty, tx), im in zip(jobs, ims):
            if im is not None:
                mos.paste(im, ((tx - tx0) * 256, (ty - ty0) * 256))
        px = lambda lon, lat: ((tile_of(lon, lat, z)[0] - tx0) * 256, (tile_of(lon, lat, z)[1] - ty0) * 256)
        cx, cy = px((x0 + x1) / 2, (y0 + y1) / 2)
        h = half * 256
        crop = mos.crop((int(cx - h), int(cy - h), int(cx + h), int(cy + h)))
        k = size / crop.width
        crop = crop.resize((size, size), Image.LANCZOS)
        dr = ImageDraw.Draw(crop)
        for ring in [g.exterior] + list(g.interiors):
            pts = [((px(a, b)[0] - (cx - h)) * k, (px(a, b)[1] - (cy - h)) * k) for a, b in ring.coords]
            dr.line(pts, fill=(0, 0, 0), width=4)
            dr.line(pts, fill=(255, 230, 0), width=2)
        bar = 20 if side < 120 else 50  # scale bar, metres
        bl = bar / mpp * k
        dr.rectangle((10, size - 22, 10 + bl, size - 16), fill=(255, 255, 255), outline=(0, 0, 0))
        dr.text((14 + bl, size - 28), f"{bar} m", fill=(255, 255, 255), font=ImageFont.truetype(FONTB, 14),
                stroke_width=2, stroke_fill=(0, 0, 0))
        m = meta(v["release"], c.x, c.y, z)
        mb = meta(v["release"], 0, 0, z, bbox=(x0, y0, x1, y1))
        return crop, z, (max((a["SRC_DATE"] for a in m), default=None),
                         sorted({a["SRC_DATE"] for a in mb}))
    return None, None, (None, [])


def fmt(d):
    return "–" if not d else datetime.datetime.strptime(str(d), "%Y%m%d").strftime("%-d %b %Y")


def strip(n, i):
    fn = SC / f"{n:02d}_i{i:03d}.png"
    vs = VER[str(i)]
    picks = pick(vs)
    labels = ("Before (< Jul 2018)", "2018–19 (context)", "By end 2023", "After (latest)")
    S = 460
    im = Image.new("RGB", (4 * S + 30, S + 74), (255, 255, 255))
    dr = ImageDraw.Draw(im)
    f, fb = ImageFont.truetype(FONT, 15), ImageFont.truetype(FONTB, 17)
    info = []
    for k, (lab, v) in enumerate(zip(labels, picks)):
        x = k * (S + 10)
        if v is None:
            dr.rectangle((x, 52, x + S, 52 + S), fill=(230, 230, 230))
            dr.text((x + 6, 4), lab + ": none", fill=(0, 0, 0), font=fb)
            info.append(None)
            continue
        p, z, (dc, db) = panel(i, v, S)
        im.paste(p, (x, 52))
        dr.text((x + 6, 4), f"{lab}: imagery {fmt(dc)}", fill=(0, 0, 0), font=fb)
        dr.text((x + 6, 28), f"release {v['release_date']}, z{z}, {v['sensor']} {v['res']} m"
                + (f"; bbox dates {','.join(map(str, db))}" if len(db) > 1 else ""), fill=(60, 60, 60), font=f)
        info.append({"release": v["release"], "release_date": v["release_date"], "src_date": dc, "bbox_dates": db,
                     "zoom": z, "sensor": v["sensor"], "res": v["res"]})
    pr = PROPS[i]
    dr.text((6, S + 54), f"#{n:02d}  polygon {i} ({pr['id']}), {AREA[i]:,.0f} m2, Amphora 2018 class: {pr['lc2018']}, "
            f"{pr['address']}  ·  draws: {DRAWS[i]}", fill=(0, 0, 0), font=f)
    im.save(fn)
    return info


PCACHE = SC / "panels.json"
OLD = json.loads(PCACHE.read_text()) if PCACHE.exists() else {}
INFO = {}
for n, i in enumerate(SAMPLE, 1):
    done = str(i) in OLD and (SC / f"{n:02d}_i{i:03d}.png").exists()
    INFO[i] = OLD[str(i)] if done else strip(n, i)
    print(n, i, f"{AREA[i]:,.0f}", [x and (x["release_date"], x["src_date"]) for x in INFO[i]])
json.dump({str(k): v for k, v in INFO.items()}, open(PCACHE, "w"), indent=1)


# ---------------------------------------------------------------- 3. classes (by eye; filled in after viewing)
"""Rules, applied to every strip (before = July 2015 to August 2016 for every sampled polygon: Wayback has no imagery of
these spots acquired between August 2016 and September 2018; context = 4 September 2018; after = June to September 2025).
confirmed: open or green land (field, grass, scrub, garrigue, trees) in the before image and built or grey (buildings,
paving, roads, car park, yard in use, quarry, active construction site) in the after image, for most of the polygon.
already grey: mostly built, paved, quarried or graded already in the before image. still open: still mostly open or green
in the after image. partial: change over part of the polygon only (the note gives the shares). unclear: the imagery
cannot decide. Timing: the before image is two years older than 2018, so the 4 September 2018 image is checked as well;
where more than half of the polygon was already under construction, built, used as a yard or quarried by then, the class
is unclear (timing), because the change may predate 2018. Bare soil alone (a ploughed or levelled field) still counts as
open. Before land types: cultivated field (ploughed or cropped), fallow field (field walls or terraces, grass, not
cropped), orchard (trees in rows or plots), grass-scrub-garrigue (rough grass, scrub, garrigue, vacant plots without
field pattern), trees (not an orchard), other. Shares in the notes are by eye."""
CLASS = {  # index: (class, before land type, state on 4 Sep 2018, grey by May 2023, note)
    357: ("confirmed", "cultivated field", "open", "no",
          "Ploughed fields in 2016 and 2018; overgrown with rubble dumped in 2023; by 2025 a building slab and "
          "materials yard over most of it, scrub on the south-west edge."),
    154: ("confirmed", "grass-scrub-garrigue", "partly cleared", "yes",
          "Dense scrub with a few trees in 2016; east third cleared by Sep 2018; residential blocks by 2023."),
    167: ("confirmed", "cultivated field", "open", "yes",
          "Walled fields in 2016; field walls removed and ground levelled by Sep 2018, no construction; excavated "
          "construction site in 2023; building works with cranes in 2025."),
    64: ("confirmed", "grass-scrub-garrigue", "open", "yes",
         "Rocky ground, about half bare rock or rubble with tracks, scrub on the rest, in 2016 and 2018 (borderline: "
         "possibly disturbed earlier, but not built or paved); cemetery extension with graves and paths by 2023."),
    45: ("confirmed", "cultivated field", "open", "yes",
         "Cultivated fields in 2016 and 2018; construction over about 70% in 2023; a large building over about two "
         "thirds by 2025, the south end bare or garden."),
    328: ("unclear", "grass-scrub-garrigue", "open", "no",
          "Scrub and grass beside woodland in 2016 and 2018; cleared bare ground in 2023; in 2025 a pale surface with "
          "outdoor exercise equipment: cleared and in use, but whether it is paved cannot be seen."),
    276: ("unclear", "cultivated field", "mostly cleared or built", "yes",
          "Ploughed field in Jun 2016; earthworks over the whole footprint by Sep 2018 (timing); building and yard by "
          "2023."),
    238: ("confirmed", "cultivated field", "open", "yes",
          "Small red-soil fields (about 60%) and garrigue (about 40%) in 2016 and 2018; quarry or stone yard over about "
          "85% in 2023 and all of it by 2025."),
    243: ("confirmed", "grass-scrub-garrigue", "open", "yes",
          "Vacant scrub with tracks in 2016 and 2018; cleared storage yard with containers and machinery by 2023."),
    272: ("confirmed", "grass-scrub-garrigue", "open", "yes",
          "Garrigue on rocky ground in 2016 and 2018; warehouses and yards by 2023, fully built by 2025."),
    292: ("confirmed", "orchard", "open", "yes",
          "Edge of an olive grove beside farm buildings (about 20% pale yard) in 2016 and 2018; a red-roofed farm "
          "building by 2023."),
    273: ("already grey", "other", "mostly cleared or built", "yes",
          "Graded, cleared development platform (bare fill with tracks, sparse scrub) in Aug 2016 and Sep 2018, not "
          "green land; buildings under construction by 2023."),
    156: ("confirmed", "grass-scrub-garrigue", "open", "yes",
          "Rough rocky scrub and abandoned terraces with tracks (about a third bare) in 2016 and 2018; building and yard "
          "over about 60% by 2023; yard and buildings over all of it by 2025."),
    209: ("partial", "fallow field", "partly cleared", "yes",
          "West part (about 55%) abandoned walled fields with grass and scrub, built by 2023; east part (about 45%) "
          "already a yard with stored materials and a building in 2016."),
    173: ("unclear", "fallow field", "mostly cleared or built", "yes",
          "Walled grassy field in Jul 2015; cleared, with two long sheds on about a third, by Sep 2018 (timing); farm "
          "sheds over all of it by 2023."),
    336: ("partial", "cultivated field", "open", "partly",
          "Ploughed field in 2015 and 2018; by 2023 boats stored on about 60%; in 2025 an unsealed dirt yard with boats, "
          "weeds over about 40%: open storage, not built or paved."),
    146: ("unclear", "grass-scrub-garrigue", "mostly cleared or built", "yes",
          "Scrub and trees with a track in Jul 2015; cleared with a building under construction by Sep 2018 (timing); "
          "house with solar panels by 2023."),
    93: ("confirmed", "grass-scrub-garrigue", "open", "yes",
         "Dense scrub with a ploughed field in the south lobe (about 20%) in 2016 and 2018; buildings and yards over "
         "the north (about 60%) by 2023; in 2025 the south lobe is an unsealed riding arena (about 35%)."),
    298: ("confirmed", "cultivated field", "open", "yes",
          "Ploughed red-soil field in 2016 and 2018; walled yard with a building by 2023."),
    220: ("confirmed", "fallow field", "open", "no",
          "Walled field with dry grass in 2016, 2018 and 2023; building under construction over all of it by 2025."),
    139: ("confirmed", "grass-scrub-garrigue", "partly cleared", "yes",
          "Overgrown plot with trees and a small building (about 10%) in 2016; about a quarter cleared by Sep 2018; "
          "vehicle and equipment yard by 2023."),
    63: ("confirmed", "fallow field", "open", "no",
         "Small walled fields with trees in 2016, 2018 and 2023; building and paved yard over about 65% by 2025."),
    237: ("confirmed", "orchard", "open", "partly",
          "Orchard in 2016 and 2018; pool and paving in 2023; by 2025 a house, pool and paving, lawn on about 30%."),
    274: ("partial", "cultivated field", "partly cleared", "partly",
          "Mixed in 2016: small fields (about 40%), scrub (about 20%) and already disturbed ground and spoil (about "
          "40%); quarry fill over part by 2023 and all of it by 2025."),
    82: ("confirmed", "fallow field", "open", "yes",
         "Flat plot of dry grass, no field walls visible (could be vacant land), in 2016 and 2018; vehicle scrapyard by "
         "2023."),
    195: ("confirmed", "grass-scrub-garrigue", "open", "yes",
          "Vacant scrub inside an industrial estate, a small field in the south-east, in 2016 and 2018; factories by "
          "2023."),
    25: ("confirmed", "cultivated field", "open", "yes",
         "Cultivated fields in Jul 2015 and Sep 2018; apartment blocks under construction by 2023."),
    102: ("unclear", "cultivated field", "mostly cleared or built", "yes",
          "Fields and olive trees in Jun 2016; cleared, with a building under construction, by Sep 2018 (timing); depot "
          "and yard by 2023."),
    81: ("unclear", "fallow field", "mostly cleared or built", "yes",
         "Rough grassy fields with tracks in Jun 2016; trailer yard over about 60% by Sep 2018 (timing); yard over all of "
         "it by 2023."),
    333: ("confirmed", "cultivated field", "partly cleared", "yes",
          "Cultivated terraces in 2016; narrow plots built on about 15% by Sep 2018; built or yards over most of it by "
          "2023."),
    271: ("unclear", "grass-scrub-garrigue", "mostly cleared or built", "yes",
          "Garrigue in 2016; north lobe (about two thirds) excavated by Sep 2018 (timing); south lobe partly cleared "
          "later; quarry by 2023."),
    20: ("confirmed", "fallow field", "open", "partly",
         "Abandoned walled fields in 2016 and 2018; roads and apartment blocks by 2025."),
    69: ("confirmed", "cultivated field", "open", "yes",
         "Field edges, verges and a tree line south of a narrow road (the old road is about a quarter of the polygon) "
         "in 2016 and 2018; dual carriageway (Central Link) by 2023."),
    202: ("confirmed", "fallow field", "open", "yes",
          "Walled grassy plot with a tree in 2016 and 2018; commercial building and car park by 2023."),
    83: ("confirmed", "grass-scrub-garrigue", "open", "yes",
         "Scrub over rubble and old foundations, with an old shed (about 12%), in 2016 and 2018; large building with a "
         "planted roof by 2023."),
    324: ("confirmed", "grass-scrub-garrigue", "open", "partly",
          "Scrub around a bare field (about 35%) in 2016 and 2018; north part cleared in 2023; two buildings and a yard "
          "by 2025."),
    134: ("confirmed", "cultivated field", "open", "yes",
          "Strip along the edge of a cultivated field beside the road in 2016 and 2018; road widening by 2023."),
    19: ("confirmed", "fallow field", "open", "yes",
         "Small walled fields, overgrown, in 2016 and 2018; apartment blocks under construction by 2023."),
    313: ("confirmed", "cultivated field", "open", "partly",
          "Cultivated terraces in 2016 and 2018; partly cleared with a structure in 2023; villa, pool and yard by "
          "2025."),
}


def wilson(k, n, z=1.959964):
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return round(100 * max(0, c - h), 1), round(100 * min(1, c + h), 1)


if CLASS and set(CLASS) >= set(SAMPLE):
    rows = []
    for n, i in enumerate(SAMPLE, 1):
        b, mid, y23, a = INFO[i]
        cl, bt, s18, g23, note = CLASS[i]
        c = POLYS[i].centroid
        brackets = bool(b and a and b["src_date"] and a["src_date"] and b["src_date"] < 20180701
                        and a["src_date"] >= 20240101)
        rows.append({
            "sample_no": n, "polygon_index": i, "amphora_id": PROPS[i]["id"], "draws": DRAWS[i],
            "area_m2_utm": round(AREA[i]), "lat": round(c.y, 5), "lon": round(c.x, 5),
            "amphora_lc2018": PROPS[i]["lc2018"], "amphora_place": PROPS[i]["address"],
            "before_release": b and b["release_date"], "before_acquired": b and b["src_date"],
            "before_sensor": b and f"{b['sensor']} {b['res']} m",
            "mid_release": mid and mid["release_date"], "mid_acquired": mid and mid["src_date"],
            "y2023_release": y23 and y23["release_date"], "y2023_acquired": y23 and y23["src_date"],
            "after_release": a and a["release_date"], "after_acquired": a and a["src_date"],
            "after_sensor": a and f"{a['sensor']} {a['res']} m",
            "dates_bracket_2018_2025": "yes" if brackets else "no",
            "all_versions_acquired": ";".join(str(v["src_date"]) for v in VER[str(i)]),
            "class": cl, "before_land_type": bt, "state_sep_2018": s18, "grey_by_may_2023": g23, "note": note,
            "seed": SEED, "sample_size_draws": N, "sampling_interval_m2": round(step, 1), "random_start_m2": round(start, 1),
            "total_area_m2": round(TOTAL), "classified_by": "Miżien (by eye)", "retrieved": TODAY})
    with open(D / "imagery_spotcheck.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\r\n")
        w.writeheader()
        w.writerows(rows)
    summ = []
    tot_d = sum(r["draws"] for r in rows)
    classes = ("confirmed", "partial", "already grey", "still open", "unclear")
    for cl in classes:
        k = sum(r["draws"] for r in rows if r["class"] == cl)
        lo, hi = wilson(k, tot_d)
        summ.append({"group": "class", "item": cl, "draws": k, "polygons": sum(r["class"] == cl for r in rows),
                     "sampled_area_m2": sum(r["area_m2_utm"] for r in rows if r["class"] == cl),
                     "share_of_draws_pct": round(100 * k / tot_d, 1), "wilson95_lo_pct": lo, "wilson95_hi_pct": hi})
    k = sum(r["draws"] for r in rows if r["class"] == "confirmed") + 0.5 * sum(r["draws"] for r in rows
                                                                                 if r["class"] == "partial")
    lo, hi = wilson(k, tot_d)
    summ.append({"group": "rule", "item": "confirmed + half of partial", "draws": k, "polygons": "",
                 "sampled_area_m2": "", "share_of_draws_pct": round(100 * k / tot_d, 1), "wilson95_lo_pct": lo,
                 "wilson95_hi_pct": hi})
    # count-based picture: Hansen-Hurwitz weights 1/area turn the PPS draws into an estimate by number of polygons
    wt = {cl: sum(r["draws"] / r["area_m2_utm"] for r in rows if r["class"] == cl) for cl in classes}
    tw = sum(wt.values())
    for cl in classes:
        summ.append({"group": "class, by number of polygons (weights 1/area; rough)", "item": cl, "draws": "",
                     "polygons": "", "sampled_area_m2": "", "share_of_draws_pct": round(100 * wt[cl] / tw, 1),
                     "wilson95_lo_pct": "", "wilson95_hi_pct": ""})
    green = [r for r in rows if r["class"] != "already grey"]  # open in the before image
    gd = sum(r["draws"] for r in green)
    grp = "before land type (draws open in the before image)"
    for bt in ("cultivated field", "fallow field", "orchard", "grass-scrub-garrigue", "trees", "other"):
        k = sum(r["draws"] for r in green if r["before_land_type"] == bt)
        lo, hi = wilson(k, gd)
        summ.append({"group": grp, "item": bt, "draws": k,
                     "polygons": sum(r["before_land_type"] == bt for r in green),
                     "sampled_area_m2": sum(r["area_m2_utm"] for r in green if r["before_land_type"] == bt),
                     "share_of_draws_pct": round(100 * k / gd, 1), "wilson95_lo_pct": lo, "wilson95_hi_pct": hi})
    for lab, types in (("fields (cultivated + fallow)", ("cultivated field", "fallow field")),
                       ("farmland (fields + orchards)", ("cultivated field", "fallow field", "orchard"))):
        k = sum(r["draws"] for r in green if r["before_land_type"] in types)
        lo, hi = wilson(k, gd)
        summ.append({"group": grp, "item": lab, "draws": k,
                     "polygons": sum(r["before_land_type"] in types for r in green), "sampled_area_m2": "",
                     "share_of_draws_pct": round(100 * k / gd, 1), "wilson95_lo_pct": lo, "wilson95_hi_pct": hi})
    for cl in ("confirmed", "unclear"):
        sub = [r for r in rows if r["class"] == cl]
        cd = sum(r["draws"] for r in sub)
        for s18 in ("open", "partly cleared", "mostly cleared or built"):
            k = sum(r["draws"] for r in sub if r["state_sep_2018"] == s18)
            summ.append({"group": f"{cl} draws: state on 4 Sep 2018", "item": s18, "draws": k,
                         "polygons": sum(r["state_sep_2018"] == s18 for r in sub), "sampled_area_m2": "",
                         "share_of_draws_pct": round(100 * k / cd, 1), "wilson95_lo_pct": "", "wilson95_hi_pct": ""})
    conf = [r for r in rows if r["class"] == "confirmed"]
    cd = sum(r["draws"] for r in conf)
    for g in ("yes", "partly", "no"):
        k = sum(r["draws"] for r in conf if r["grey_by_may_2023"] == g)
        summ.append({"group": "confirmed draws: mostly grey by 6 May 2023", "item": g, "draws": k,
                     "polygons": sum(r["grey_by_may_2023"] == g for r in conf), "sampled_area_m2": "",
                     "share_of_draws_pct": round(100 * k / cd, 1), "wilson95_lo_pct": "", "wilson95_hi_pct": ""})
    k = sum(r["draws"] for r in conf if r["grey_by_may_2023"] == "yes")
    lo, hi = wilson(k, tot_d)
    summ.append({"group": "rule", "item": "confirmed and mostly grey by 6 May 2023 (article's 2018-2023)", "draws": k,
                 "polygons": sum(r["grey_by_may_2023"] == "yes" for r in conf), "sampled_area_m2": "",
                 "share_of_draws_pct": round(100 * k / tot_d, 1), "wilson95_lo_pct": lo, "wilson95_hi_pct": hi})
    k = sum(r["draws"] for r in rows if r["dates_bracket_2018_2025"] == "yes")
    summ.append({"group": "imagery", "item": "draws whose before/after dates bracket mid-2018 to 2024+", "draws": k,
                 "polygons": sum(r["dates_bracket_2018_2025"] == "yes" for r in rows), "sampled_area_m2": "",
                 "share_of_draws_pct": round(100 * k / tot_d, 1), "wilson95_lo_pct": "", "wilson95_hi_pct": ""})
    ba = sorted(r["before_acquired"] for r in rows)
    aa = sorted(r["after_acquired"] for r in rows)
    summ.append({"group": "imagery", "item": f"acquired: before {ba[0]}-{ba[-1]}; context 20180904; "
                 f"by 2023 20230506; after {aa[0]}-{aa[-1]}", "draws": tot_d, "polygons": len(rows),
                 "sampled_area_m2": "", "share_of_draws_pct": "", "wilson95_lo_pct": "", "wilson95_hi_pct": ""})
    for x in summ:
        x.update({"seed": SEED, "note": "rough: small polygons weigh heavily" if "number of polygons" in x["group"]
                  else "" if x["group"] == "imagery" else
                  ("share of draws = estimated share of Amphora's area (PPS on area)" if x["group"] in ("class", "rule")
                   else "share of the draws in this group (PPS on area)")
                  + ("; Wilson 95% interval" if x["wilson95_lo_pct"] != "" else "")})
    with open(D / "imagery_spotcheck_summary.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(summ[0]), lineterminator="\r\n")
        w.writeheader()
        w.writerows(summ)
    for x in summ:
        print(x)
else:
    print("CLASS not filled in for every sampled polygon: look at out/spotcheck/*.png first.")
