#!/usr/bin/env python3
"""CC-101: download the data behind the check into data/cc-101/ (each file keeps its source URL and retrieval date).

1. Eurostat env_wat_abs (annual freshwater abstraction by source and sector), Malta, million m3, with Eurostat's
   flags (e = estimated, b = break in series).
2. EEA WISE, Malta's 3rd-cycle WFD reporting (2022): the list of surface water bodies and the significant pressures
   reported for each surface and groundwater body.
3. legislation.mt: the consolidated texts of the Maltese instruments read for this check (header line, amendments,
   SHA-256 of the PDF; the PDFs themselves are not committed) and the titles of every Legal Notice of 2024-2026 in
   the ELI sitemap, to look for a new groundwater-abstraction instrument.

    python fetch.py            # all three
    python fetch.py eurostat   # one part (eurostat | wise | laws | notices)
"""
import csv
import datetime
import hashlib
import json
import pathlib
import re
import subprocess
import sys
import tempfile
import time
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-101"
D.mkdir(exist_ok=True)
TODAY = datetime.date.today().isoformat()
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"


def get(url, timeout=120):
    return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=timeout).read()


def write(name, rows):
    with open(D / name, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(name, len(rows), "rows")


# ------------------------------------------------------------------ 1. Eurostat
def eurostat():
    url = ("https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/env_wat_abs?format=JSON&lang=en"
           "&geo=MT&unit=MIO_M3&sinceTimePeriod=2010")
    d = json.loads(get(url))
    dims, sz = d["id"], d["size"]
    cats = [[c for c, _ in sorted(d["dimension"][k]["category"]["index"].items(), key=lambda kv: kv[1])]
            for k in dims]
    labels = {k: d["dimension"][k]["category"].get("label", {}) for k in dims}
    status = d.get("status", {})
    rows = []
    for key, v in d["value"].items():
        n, pos = int(key), []
        for s in reversed(sz):
            pos.append(n % s)
            n //= s
        pos.reverse()
        r = {k: cats[i][p] for i, (k, p) in enumerate(zip(dims, pos))}
        rows.append({"dataset": "env_wat_abs", "geo": r["geo"], "wat_proc": r["wat_proc"],
                     "wat_proc_label": labels["wat_proc"][r["wat_proc"]], "wat_src": r["wat_src"],
                     "wat_src_label": labels["wat_src"][r["wat_src"]], "unit": r["unit"], "year": r["time"],
                     "value": v, "flag": status.get(key, ""), "eurostat_updated": d.get("updated"),
                     "query_url": url, "retrieved": TODAY})
    rows.sort(key=lambda r: (r["wat_src"], r["wat_proc"], r["year"]))
    write("eurostat_env_wat_abs.csv", rows)


# ------------------------------------------------------------------ 2. EEA WISE (WFD 2022 reporting)
WISE = "https://water.discomap.eea.europa.eu/arcgis/rest/services/WISE_WFD/"


def wise_query(service, layer, fields):
    q = urllib.parse.urlencode({"where": "countryCode='MT'", "outFields": fields, "returnGeometry": "false",
                                "f": "json"})
    url = f"{WISE}{service}/MapServer/{layer}/query?{q}"
    return json.loads(get(url))["features"], url


def wise():
    feats, url = wise_query("WFD2022_SurfaceWaterBody_WM", 17,
                            "thematicIdIdentifier,nameText,specialisedZoneType,sizeValue,sizeUom,cYear")
    rows = [{"eu_code": f["attributes"]["thematicIdIdentifier"], "name": f["attributes"]["nameText"],
             "category": f["attributes"]["specialisedZoneType"], "size": f["attributes"]["sizeValue"],
             "size_unit": f["attributes"]["sizeUom"], "reporting_year": f["attributes"]["cYear"],
             "source": "EEA WISE WFD2022_SurfaceWaterBody_WM layer 17 (SurfaceWaterBody_polygon)", "url": url,
             "retrieved": TODAY} for f in feats]
    rows.sort(key=lambda r: r["eu_code"])
    write("wise_2022_surface_water_bodies.csv", rows)

    out = []
    feats, url = wise_query("WFD2022_SurfaceWaterBody_swSignificantPressureType_WM", 14,
                            "euSurfaceWaterBodyCode,surfaceWaterBodyCategory,swSignificantPressureType,cYear")
    for f in feats:
        a = f["attributes"]
        out.append({"water": "surface", "eu_code": a["euSurfaceWaterBodyCode"], "name": "",
                    "category": a["surfaceWaterBodyCategory"], "significant_pressures": a["swSignificantPressureType"],
                    "reporting_year": a["cYear"],
                    "source": "EEA WISE WFD2022_SurfaceWaterBody_swSignificantPressureType_WM layer 14 (all "
                              "significant pressures reported for each body)", "url": url, "retrieved": TODAY})
    feats, url = wise_query("WFD2022_GroundWaterBody_gwSignificantPressureType_WM", 7,
                            "euGroundWaterBodyCode,groundWaterBodyName,gwSignificantPressureType,cYear")
    for f in feats:
        a = f["attributes"]
        out.append({"water": "ground", "eu_code": a["euGroundWaterBodyCode"], "name": a["groundWaterBodyName"],
                    "category": "GW", "significant_pressures": a["gwSignificantPressureType"],
                    "reporting_year": a["cYear"],
                    "source": "EEA WISE WFD2022_GroundWaterBody_gwSignificantPressureType_WM layer 7 (all "
                              "significant pressures reported for each body)", "url": url, "retrieved": TODAY})
    out.sort(key=lambda r: (r["water"], r["eu_code"]))
    write("wise_2022_significant_pressures.csv", out)


# ------------------------------------------------------------------ 3. legislation.mt
LAWS = [  # (ELI path, what it is)
    ("sl/549.100", "Water Policy Framework Regulations (transposes the WFD)"),
    ("sl/549.164", "Notification of Groundwater Sources Regulations (formerly S.L. 423.12)"),
    ("sl/549.165", "Borehole Drilling and Excavation Works within the Saturated Zone Regulations (formerly S.L. 423.32)"),
    ("sl/549.166", "Groundwater Abstraction (Metering) Regulations (formerly S.L. 423.40)"),
    ("sl/549.168", "Users of Groundwater Sources (Application) Regulations (formerly S.L. 423.45)"),
    ("sl/549.172", "Environmental Permitting (Procedure for Applications and their Determination) Regulations"),
    ("cap/549", "Environment Protection Act"),
    ("cap/355", "Water Services Corporation Act"),
    ("sl/545.14", "Water Supply and Sewerage Services Regulations"),
]


def laws():
    rows = []
    with tempfile.TemporaryDirectory() as tmp:
        for eli, what in LAWS:
            url = f"https://legislation.mt/eli/{eli}/eng/pdf"
            pdf = get(url)
            p = pathlib.Path(tmp) / "x.pdf"
            p.write_bytes(pdf)
            txt = subprocess.run(["pdftotext", "-layout", str(p), "-"], capture_output=True, text=True).stdout
            head = re.search(r"((?:LEGAL NOTICE|ACT) [^\n]+(?:\n[^\n]+)?)", txt)
            hits = len(re.findall(r"(?i)abstract", txt))
            rows.append({"eli": eli, "instrument": what, "header": re.sub(r"\s+", " ", head.group(1)).strip()
                         if head else "", "mentions_of_abstract": hits, "pdf_bytes": len(pdf),
                         "pdf_sha256": hashlib.sha256(pdf).hexdigest(), "url": url, "retrieved": TODAY})
            time.sleep(0.5)
    write("legislation_mt_instruments.csv", rows)


def notices(years=(2024, 2025, 2026)):
    """Titles of every Legal Notice of these years in the ELI sitemap. Resumable: titles already fetched are kept in
    out/ln_cache.json (not committed), so an interrupted run continues where it stopped."""
    cache_f = pathlib.Path(__file__).resolve().parent / "out" / "ln_cache.json"
    cache_f.parent.mkdir(exist_ok=True)
    cache = json.loads(cache_f.read_text()) if cache_f.exists() else {}
    sm = get("https://legislation.mt/eli/sitemap.xml").decode("utf-8", "replace")
    urls = [u for u in re.findall(r"<loc>(https://legislation\.mt/eli/ln/(\d{4})/\d+)</loc>", sm)
            if int(u[1]) in years]
    def title_of(u):
        try:
            h = get(u, timeout=60).decode("utf-8", "replace")
            m = re.search(r'about="mlt:eli/ln/[^"]+/eng" property="eli:title" content="([^"]+)"', h)
            title = m.group(1) if m else ""
        except Exception as e:  # noqa: BLE001  (record and move on; the count of failures is printed)
            title = f"ERROR {e}"
        time.sleep(0.25)
        return u, {"title": re.sub(r"\s+", " ", title).strip(), "retrieved": TODAY}

    todo = [u for u, _ in urls if u not in cache or not cache[u]["title"] or cache[u]["title"].startswith("ERROR")]
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=4) as pool:   # four at a time: polite to a government server
        for i, (u, rec) in enumerate(pool.map(title_of, todo)):
            cache[u] = rec
            if i % 25 == 0:
                cache_f.write_text(json.dumps(cache))
                print(i, len(todo), u, flush=True)
    rows = []
    for u, y in urls:
        t = cache[u]["title"]
        rows.append({"year": y, "url": u, "title_en": t,
                     "matches_groundwater_or_abstraction": bool(re.search(r"(?i)groundwater|abstraction|borehole|"
                                                                          r"water polic|\bwells?\b", t)),
                     "retrieved": cache[u]["retrieved"]})
    cache_f.write_text(json.dumps(cache))
    rows.sort(key=lambda r: (r["year"], int(r["url"].rsplit("/", 1)[1])))
    write("legislation_mt_legal_notices_2024_2026.csv", rows)
    print("errors:", sum(r["title_en"].startswith("ERROR") or not r["title_en"] for r in rows))


if __name__ == "__main__":
    parts = sys.argv[1:] or ["eurostat", "wise", "laws", "notices"]
    for part in parts:
        globals()[part]()
