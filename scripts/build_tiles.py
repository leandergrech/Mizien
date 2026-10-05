#!/usr/bin/env python3
"""Build docs/data/malta.pmtiles and docs/data/fonts/: the vector map of the Maltese islands used by the map view.

The tiles are an extract of OpenFreeMap's OpenStreetMap tiles (OpenMapTiles schema; (c) OpenMapTiles,
(c) OpenStreetMap contributors, ODbL) for the islands, zoom 0 to 14. They are trimmed to the layers and fields the
map draws (no translations of names), so the whole extract is one small file served from the site itself: no map
service is contacted when someone opens the map. MapLibre draws zoom levels above 14 from the zoom-14 tiles.

    python scripts/build_tiles.py            # network needed (tiles.openfreemap.org)
    python scripts/build_tiles.py --cache D  # keep the downloaded tiles in folder D and reuse them

Needs: pip install mapbox-vector-tile pmtiles (only to rebuild; the site uses the committed files).
"""
import argparse, concurrent.futures as cf, gzip, json, math, pathlib, urllib.parse, urllib.request

from mapbox_vector_tile.Mapbox import vector_tile_pb2
from pmtiles.tile import Compression, TileType, zxy_to_tileid
from pmtiles.writer import Writer

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "data" / "malta.pmtiles"
FONTS = ROOT / "docs" / "data" / "fonts"
BBOX = (35.78, 14.17, 36.09, 14.60)   # s, w, n, e: all the islands (as scripts/build_geo.py)
MAXZOOM = 14
UA = {"User-Agent": "Mizien/1.0 (map extract for the Maltese islands; github.com/leandergrech/Mizien)"}
# Layers the map draws, and the fields it reads from each feature.
KEEP = {
    "water": {"class"}, "waterway": {"class"}, "landcover": {"class", "subclass"}, "landuse": {"class"},
    "park": {"class"}, "transportation": {"class", "subclass", "brunnel", "ramp"},
    "transportation_name": {"class", "name", "name:latin", "ref"}, "place": {"class", "name", "name:latin", "rank", "capital"},
    "aeroway": {"class"}, "building": set(), "water_name": {"class", "name", "name:latin"},
}
FONT_STACKS = ["Noto Sans Regular", "Noto Sans Bold", "Noto Sans Italic"]
FONT_RANGES = ["0-255", "256-511", "512-767", "7680-7935", "8192-8447"]   # Latin, Latin Extended (ċ ġ ħ ż), punctuation


def get(url):
    r = urllib.request.urlopen(urllib.request.Request(url, headers={**UA, "Accept-Encoding": "gzip"}), timeout=90)
    b = r.read()
    return gzip.decompress(b) if b[:2] == b"\x1f\x8b" else b


def tile_xy(lat, lon, z):
    n = 2 ** z
    return int((lon + 180) / 360 * n), int((1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * n)


def trim(raw):
    """Keep only the layers and fields in KEEP; geometry is left exactly as it was."""
    src, out = vector_tile_pb2.tile(), vector_tile_pb2.tile()
    src.ParseFromString(raw)
    for L in src.layers:
        if L.name not in KEEP:
            continue
        want, keys, vals = KEEP[L.name], {}, {}
        N = out.layers.add()
        N.name, N.version, N.extent = L.name, L.version, L.extent
        for f in L.features:
            g = N.features.add()
            g.type = f.type
            g.geometry.extend(f.geometry)
            if f.HasField("id"):
                g.id = f.id
            tags = []
            for i in range(0, len(f.tags), 2):
                k, v = L.keys[f.tags[i]], L.values[f.tags[i + 1]]
                if k not in want:
                    continue
                if k not in keys:
                    keys[k] = len(keys)
                    N.keys.append(k)
                vk = v.SerializeToString()
                if vk not in vals:
                    vals[vk] = len(vals)
                    N.values.add().CopyFrom(v)
                tags += [keys[k], vals[vk]]
            g.tags.extend(tags)
        if not N.features:
            out.layers.remove(N)
    return out.SerializeToString()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", type=pathlib.Path)
    a = ap.parse_args()
    base = json.loads(get("https://tiles.openfreemap.org/planet"))["tiles"][0]
    s, w, n, e = BBOX
    jobs = [(z, x, y) for z in range(MAXZOOM + 1)
            for x in range(tile_xy(n, w, z)[0], tile_xy(s, e, z)[0] + 1)
            for y in range(tile_xy(n, w, z)[1], tile_xy(s, e, z)[1] + 1)]

    def fetch(j):
        z, x, y = j
        f = a.cache / f"{z}/{x}/{y}.pbf" if a.cache else None
        if f and f.exists():
            return j, f.read_bytes()
        b = get(base.format(z=z, x=x, y=y))
        if f:
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_bytes(b)
        return j, b

    with cf.ThreadPoolExecutor(6) as ex:
        tiles = sorted(ex.map(fetch, jobs), key=lambda t: zxy_to_tileid(*t[0]))
    raw = sum(len(b) for _, b in tiles)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "wb") as fh:
        wr = Writer(fh)
        for (z, x, y), b in tiles:
            wr.write_tile(zxy_to_tileid(z, x, y), gzip.compress(trim(b), 9))
        wr.finalize({
            "tile_type": TileType.MVT, "tile_compression": Compression.GZIP,
            "min_zoom": 0, "max_zoom": MAXZOOM,
            "min_lon_e7": int(w * 1e7), "min_lat_e7": int(s * 1e7), "max_lon_e7": int(e * 1e7), "max_lat_e7": int(n * 1e7),
            "center_zoom": 10, "center_lon_e7": int(14.42 * 1e7), "center_lat_e7": int(35.94 * 1e7),
        }, {
            "name": "Maltese islands (Miżien extract)", "format": "pbf",
            "attribution": "© OpenMapTiles © OpenStreetMap contributors",
            "source": base, "vector_layers": [{"id": k, "fields": {f: "String" for f in v}} for k, v in KEEP.items()],
        })
    print(f"{len(tiles)} tiles, {raw / 1e6:.1f} MB as downloaded -> {OUT.stat().st_size / 1e6:.2f} MB {OUT.relative_to(ROOT)}")

    for stack in FONT_STACKS:
        for r in FONT_RANGES:
            f = FONTS / stack / f"{r}.pbf"
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_bytes(get(f"https://tiles.openfreemap.org/fonts/{urllib.parse.quote(stack)}/{r}.pbf"))
    print(f"glyphs: {len(FONT_STACKS)} fonts x {len(FONT_RANGES)} ranges in {FONTS.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
