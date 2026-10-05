#!/usr/bin/env python3
"""Build docs/data/geo.json: stylised outlines of the Maltese islands, the main roads and the town centres.

Data: OpenStreetMap via the Overpass API (network needed), (c) OpenStreetMap contributors, ODbL.
Coordinates are written in metres east/north of ORIGIN, rounded to 1 m, so the site can draw them without a map
library. Claims are placed with the same formula from their claim.yml `location` (lat/lon).

    python scripts/build_geo.py            # fetch from Overpass and rebuild
    python scripts/build_geo.py --cache D  # read/write raw Overpass responses in folder D
    python scripts/build_geo.py --keep-islands  # keep the island outlines already in geo.json (reports use their areas)
"""
import argparse, json, math, pathlib, re, time, unicodedata, urllib.parse, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "data" / "geo.json"
ORIGIN = (35.94, 14.38)  # lat, lon
APIS = ["https://overpass-api.de/api/interpreter", "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
        "https://overpass.kumi.systems/api/interpreter"]
ISLANDS = {  # OSM ids: relation (r) or way (w)
    "Malta": ("r", 7118334), "Gozo": ("r", 9353903), "Comino": ("w", 23465078), "Cominotto": ("w", 10365739),
    "Filfla": ("w", 10365721), "St Paul's Islands": ("w", 10365736), "Manoel Island": ("w", 127163329),
}
BBOX = (35.78, 14.17, 36.09, 14.60)  # s, w, n, e: all the islands
ROADS = ("motorway", "trunk", "primary", "secondary")  # main roads only: the map is a simplified view
ARTICLE = re.compile(r"^(Il|L|Ix|Iż|Iz|Is|In|Ir|Id|It|Iċ|Ic|Tas|Ħal|Ħaż|Ħaz|Ħas)[- ]", re.I)
EXONYMS = {"Victoria", "Valletta", "Floriana", "Cospicua", "Senglea", "Vittoriosa", "Mdina", "St Paul's Bay",
           "St Julian's"}  # English names in everyday use; elsewhere the Maltese name without its article
SHORT = {"Wied il-Għajn": "Marsaskala", "Raħal Ġdid": "Paola", "Ħ'Attard": "Attard", "Ħad-Dingli": "Dingli",
         "Tal-Pietà": "Pietà", "Ta' Sannat": "Sannat", "Ta' Kerċem": "Kerċem", "L-Imsida": "Msida",
         "L-Imqabba": "Mqabba", "L-Imtarfa": "Mtarfa", "L-Imġarr": "Mġarr"}  # the names used in everyday speech


def xy(lat, lon):
    return (round((lon - ORIGIN[1]) * 111320 * math.cos(math.radians(ORIGIN[0]))),
            round((lat - ORIGIN[0]) * 110574))


def overpass(q, cache, name):
    f = cache / f"{name}.json" if cache else None
    if f and f.exists():
        return json.load(open(f))
    for i in range(6):
        req = urllib.request.Request(APIS[i % len(APIS)], urllib.parse.urlencode({"data": q}).encode(), {"User-Agent": "Mizien/1.0"})
        try:
            d = json.load(urllib.request.urlopen(req, timeout=180))
            break
        except Exception:  # noqa: BLE001 - Overpass rate limits and timeouts; try the next mirror
            time.sleep(5)
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


def lines(ways):
    """Join way geometries that share end points into longer polylines."""
    ways = [w[:] for w in ways if len(w) > 1]
    out = []
    while ways:
        ln = ways.pop(0)
        changed = True
        while changed:
            changed = False
            for i, w in enumerate(ways):
                if w[0] == ln[-1]:
                    ln += w[1:]
                elif w[-1] == ln[-1]:
                    ln += w[::-1][1:]
                elif w[-1] == ln[0]:
                    ln = w[:-1] + ln
                elif w[0] == ln[0]:
                    ln = w[::-1][:-1] + ln
                else:
                    continue
                ways.pop(i)
                changed = True
                break
        out.append(ln)
    return out


def plain(t):
    return "".join(c for c in unicodedata.normalize("NFD", t) if unicodedata.category(c) != "Mn").lower().replace("ħ", "h")


def town_name(tags):
    """Maltese name without its article (Il-Ħamrun -> Ħamrun), or the English name in everyday use (Victoria)."""
    mt = tags.get("name", "")
    en = (tags.get("name:en") or "").replace("Saint ", "St ")
    return en if en in EXONYMS else SHORT.get(mt) or ARTICLE.sub("", mt).strip() or mt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache")
    ap.add_argument("--keep-islands", action="store_true")
    a = ap.parse_args()
    cache = pathlib.Path(a.cache) if a.cache else None
    if cache:
        cache.mkdir(parents=True, exist_ok=True)
    s, w, n, e = BBOX
    if a.keep_islands:
        islands = json.load(open(OUT))["islands"]
    else:
        islands = []
        ids_r = ",".join(str(v[1]) for v in ISLANDS.values() if v[0] == "r")
        ids_w = ",".join(str(v[1]) for v in ISLANDS.values() if v[0] == "w")
        isl = overpass(f"[out:json][timeout:120];(relation(id:{ids_r});way(id:{ids_w}););out geom;", cache, "islands")
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
                                "detail": flat(simplify(m, 4)) if name in ("Malta", "Gozo", "Manoel Island") else None})
    rd = overpass(f'[out:json][timeout:120];way["highway"~"^({"|".join(ROADS)})$"]({s},{w},{n},{e});out geom;',
                  cache, "roads")
    tw = overpass(f'[out:json][timeout:120];node["place"~"^(city|town|village)$"]({s},{w},{n},{e});out;', cache, "towns")
    roads = []
    for cls in ROADS:
        ways = [[(p["lat"], p["lon"]) for p in el["geometry"]] for el in rd["elements"]
                if el["tags"].get("highway") == cls and el.get("geometry")]
        for ln in lines(ways):
            pts = simplify([xy(*p) for p in ln], 12)
            if len(pts) > 1 and sum(math.dist(p, q) for p, q in zip(pts, pts[1:])) > 150:
                roads.append({"k": "main" if cls in ("motorway", "trunk", "primary") else "minor", "pts": flat(pts)})
    towns = []
    for el in tw["elements"]:
        t = el["tags"]
        if not t.get("name"):
            continue
        x, y = xy(el["lat"], el["lon"])
        towns.append({"name": town_name(t), "mt": t["name"], "kind": t["place"], "pop": int(t["population"])
                      if t.get("population", "").isdigit() else None, "x": x, "y": y})
    towns.sort(key=lambda t: -(t["pop"] or 0))
    for t in towns:  # Żebbuġ is both a Malta and a Gozo village
        if sum(u["name"] == t["name"] for u in towns) > 1:
            t["name"] += " (Gozo)" if t["y"] > 9000 else ""
    out = {"origin": {"lat": ORIGIN[0], "lon": ORIGIN[1]}, "units": "metres east (x) and north (y) of origin",
           "attribution": "© OpenStreetMap contributors (ODbL)", "islands": islands, "roads": roads, "towns": towns}
    OUT.write_text(json.dumps(out, separators=(",", ":"), ensure_ascii=False))
    npts = sum(len(r["pts"]) // 2 for r in roads)
    print(f"{OUT.relative_to(ROOT)}: {len(islands)} rings, {len(roads)} roads ({npts} points), {len(towns)} towns, "
          f"{OUT.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
