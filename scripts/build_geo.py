#!/usr/bin/env python3
"""Build docs/data/geo.json: stylised outlines of the Maltese islands and the detailed Valletta & Floriana district.

Data: OpenStreetMap via the Overpass API (network needed), (c) OpenStreetMap contributors, ODbL.
Coordinates are written in metres east/north of ORIGIN, rounded to 1 m, so the site can draw them without a map
library. Claims are placed with the same formula from their claim.yml `location` (lat/lon).

    python scripts/build_geo.py            # fetch from Overpass and rebuild
    python scripts/build_geo.py --cache D  # read/write raw Overpass responses in folder D
"""
import argparse, json, math, pathlib, urllib.parse, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "data" / "geo.json"
ORIGIN = (35.94, 14.38)  # lat, lon
API = "https://overpass-api.de/api/interpreter"
ISLANDS = {  # OSM ids: relation (r) or way (w)
    "Malta": ("r", 7118334), "Gozo": ("r", 9353903), "Comino": ("w", 23465078), "Cominotto": ("w", 10365739),
    "Filfla": ("w", 10365721), "St Paul's Islands": ("w", 10365736), "Manoel Island": ("w", 127163329),
}
VALLETTA_BBOX = (35.886, 14.498, 35.905, 14.525)  # s, w, n, e
DISTRICTS = [
    {"id": "valletta", "name": "Valletta & Floriana", "lat": 35.8955, "lon": 14.5105, "radius_m": 1100, "unlock": 9,
     "blurb": "The capital: Parliament, the Prime Minister's office at Castille and the Planning Authority.",
     "landmarks": [
         ["Parliament House", 35.89614, 14.50978], ["Auberge de Castille", 35.8959, 14.51136],
         ["Upper Barrakka Gardens", 35.89493, 14.51194], ["City Gate", 35.89623, 14.50907],
         ["Planning Authority", 35.89, 14.50314], ["Valletta Waterfront", 35.88994, 14.50753],
         ["Family Court", 35.89845, 14.51171]]},
    {"id": "gozo", "name": "Victoria & the Ċittadella", "lat": 36.04666, "lon": 14.23947, "radius_m": 900, "unlock": 15,
     "blurb": "Gozo's capital and its citadel.", "landmarks": []},
    {"id": "harbour", "name": "Grand Harbour & the Three Cities", "lat": 35.8889, "lon": 14.5201, "radius_m": 1300,
     "unlock": 20, "blurb": "Birgu, Senglea, Cospicua and the docks.", "landmarks": []},
]


def xy(lat, lon):
    return (round((lon - ORIGIN[1]) * 111320 * math.cos(math.radians(ORIGIN[0]))),
            round((lat - ORIGIN[0]) * 110574))


def overpass(q, cache, name):
    f = cache / f"{name}.json" if cache else None
    if f and f.exists():
        return json.load(open(f))
    for _ in range(4):
        req = urllib.request.Request(API, urllib.parse.urlencode({"data": q}).encode(), {"User-Agent": "Mizien/1.0"})
        try:
            d = json.load(urllib.request.urlopen(req, timeout=180))
            break
        except Exception:  # noqa: BLE001 - Overpass rate limits; retry
            continue
    else:
        raise SystemExit("Overpass did not answer")
    if f:
        f.write_text(json.dumps(d))
    return d


def stitch(ways):
    """Join way geometries (lists of (lat, lon)) into closed rings."""
    ways = [w[:] for w in ways if len(w) > 1]
    rings = []
    while ways:
        ring = ways.pop(0)
        changed = True
        while ring[0] != ring[-1] and changed:
            changed = False
            for i, w in enumerate(ways):
                if w[0] == ring[-1]:
                    ring += w[1:]
                elif w[-1] == ring[-1]:
                    ring += w[::-1][1:]
                elif w[-1] == ring[0]:
                    ring = w[:-1] + ring
                elif w[0] == ring[0]:
                    ring = w[::-1][:-1] + ring
                else:
                    continue
                ways.pop(i)
                changed = True
                break
        rings.append(ring)
    return rings


def simplify(pts, tol):
    """Douglas-Peucker on metre coordinates. Closed rings are split at their farthest point first."""
    if len(pts) < 3:
        return pts
    if pts[0] == pts[-1]:
        far = max(range(len(pts)), key=lambda i: math.hypot(pts[i][0] - pts[0][0], pts[i][1] - pts[0][1]))
        return simplify(pts[: far + 1], tol)[:-1] + simplify(pts[far:], tol)
    keep = [False] * len(pts)
    keep[0] = keep[-1] = True
    stack = [(0, len(pts) - 1)]
    while stack:
        a, b = stack.pop()
        (x1, y1), (x2, y2) = pts[a], pts[b]
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy) or 1e-9
        best, bi = -1, -1
        for i in range(a + 1, b):
            d = abs(dy * pts[i][0] - dx * pts[i][1] + x2 * y1 - y2 * x1) / L
            if d > best:
                best, bi = d, i
        if best > tol:
            keep[bi] = True
            stack += [(a, bi), (bi, b)]
    return [p for p, k in zip(pts, keep) if k]


def flat(pts):
    return [v for p in pts for v in p]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache")
    a = ap.parse_args()
    cache = pathlib.Path(a.cache) if a.cache else None
    if cache:
        cache.mkdir(parents=True, exist_ok=True)
    ids_r = ",".join(str(v[1]) for v in ISLANDS.values() if v[0] == "r")
    ids_w = ",".join(str(v[1]) for v in ISLANDS.values() if v[0] == "w")
    isl = overpass(f"[out:json][timeout:120];(relation(id:{ids_r});way(id:{ids_w}););out geom;", cache, "islands")
    s, w, n, e = VALLETTA_BBOX
    streets = overpass(f'[out:json][timeout:120];way["highway"~"primary|secondary|tertiary|residential|pedestrian|'
                       f'unclassified|living_street"]({s},{w},{n},{e});out geom;', cache, "valletta_streets")

    islands = []
    for name, (typ, oid) in ISLANDS.items():
        el = next(x for x in isl["elements"] if x["id"] == oid and x["type"] == ("relation" if typ == "r" else "way"))
        if typ == "r":
            ways = [[(p["lat"], p["lon"]) for p in m["geometry"]] for m in el["members"]
                    if m["type"] == "way" and m.get("role") in ("outer", "") and m.get("geometry")]
            rings = stitch(ways)
        else:
            rings = [[(p["lat"], p["lon"]) for p in el["geometry"]]]
        for r in rings:
            m = [xy(*p) for p in r]
            if len(m) < 4:
                continue
            area = abs(sum(x1 * y2 - x2 * y1 for (x1, y1), (x2, y2) in zip(m, m[1:] + m[:1]))) / 2
            if area < 2000:
                continue
            islands.append({"name": name, "area_m2": round(area), "coarse": flat(simplify(m, 30)),
                            "detail": flat(simplify(m, 4)) if name in ("Malta", "Manoel Island") else None})
    major = ("primary", "secondary", "tertiary")
    st = []
    for el in streets["elements"]:
        pts = simplify([xy(p["lat"], p["lon"]) for p in el["geometry"]], 2)
        if len(pts) > 1:
            st.append({"major": el["tags"].get("highway") in major, "pts": flat(pts)})
    dist = []
    for d in DISTRICTS:
        x, y = xy(d["lat"], d["lon"])
        dist.append({**{k: v for k, v in d.items() if k not in ("lat", "lon", "landmarks")}, "x": x, "y": y,
                     "landmarks": [{"name": nm, "x": xy(la, lo)[0], "y": xy(la, lo)[1]} for nm, la, lo in d["landmarks"]],
                     "streets": st if d["id"] == "valletta" else []})
    out = {"origin": {"lat": ORIGIN[0], "lon": ORIGIN[1]}, "units": "metres east (x) and north (y) of origin",
           "attribution": "© OpenStreetMap contributors (ODbL)", "islands": islands, "districts": dist}
    OUT.write_text(json.dumps(out, separators=(",", ":")))
    npts = sum(len(i["coarse"]) // 2 + len(i["detail"] or []) // 2 for i in islands)
    print(f"{OUT.relative_to(ROOT)}: {len(islands)} rings, {npts} points, {len(st)} streets, "
          f"{OUT.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
