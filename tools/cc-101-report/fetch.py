#!/usr/bin/env python3
"""CC-101: download the data behind the check into data/cc-101/ (each file keeps its source URL and retrieval date).

1. Eurostat env_wat_abs (annual freshwater abstraction by source and sector), Malta, million m3, with Eurostat's
   flags (e = estimated, b = break in series).
2. EEA WISE, Malta's 3rd-cycle WFD reporting (2022): the list of surface water bodies and the significant pressures
   reported for each surface and groundwater body.
3. legislation.mt: the consolidated texts of the Maltese instruments read for this check (header line, amendments,
   SHA-256 of the PDF; the PDFs themselves are not committed) and the titles of every Legal Notice of 2024-2026 in
   the ELI sitemap, to look for a new groundwater-abstraction instrument.

4. legislation.mt, added after review: the title and text-search counts of every Act of 2024-2026 (acts) and the titles
   of the S.L. 549, 423, 545, 355 and 427 series (sl_titles); EEA WISE groundwater-body status (wise_status).

    python fetch.py            # everything
    python fetch.py eurostat   # one part (eurostat | wise | wise_status | laws | notices | acts | sl_titles)
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


def wise_status():
    """Quantitative and chemical status of Malta's groundwater bodies, 3rd-cycle (2022) reporting, from WISE directly
    (the same layer CC-009 used; fetched again so that this check cites the primary source)."""
    q = urllib.parse.urlencode({"where": "countryCode='MT'", "outFields": "cYear,countryCode,euRBDCode,euGroundWaterBodyCode,"
                                "groundWaterBodyName,gwQuantitativeStatusValue,gwQuantitativeAssessmentYear,"
                                "gwChemicalStatusValue,gwChemicalAssessmentYear", "returnGeometry": "false",
                                "orderByFields": "euGroundWaterBodyCode", "f": "json"})
    url = f"{WISE}WFD2022_GroundWaterBody_WM/MapServer/0/query?{q}"
    names = {"2": "Good", "3": "Poor"}   # layer legend: 2 = Good, 3 = Poor
    rows = []
    for f in json.loads(get(url))["features"]:
        a = f["attributes"]
        rows.append({"eu_groundwater_body_code": a["euGroundWaterBodyCode"], "name": a["groundWaterBodyName"],
                     "quantitative_status_code": a["gwQuantitativeStatusValue"],
                     "quantitative_status": names.get(str(a["gwQuantitativeStatusValue"]), "?"),
                     "quantitative_assessment_year": a["gwQuantitativeAssessmentYear"],
                     "chemical_status_code": a["gwChemicalStatusValue"],
                     "chemical_status": names.get(str(a["gwChemicalStatusValue"]), "?"),
                     "reporting_year": a["cYear"],
                     "source": "EEA WISE WFD2022_GroundWaterBody_WM layer 0 (legend: 2 = Good, 3 = Poor)", "url": url,
                     "retrieved": TODAY})
    write("wise_2022_groundwater_status.csv", rows)


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
    ("sl/545.2", "Control of Water Pumps and Wells Order (S.L. 545.02)"),
    ("sl/549.21", "Quality required of Surface Water intended for the Abstraction of Drinking Water Regulations"),
    ("sl/549.53", "Protection of Groundwater against Pollution and Deterioration Regulations"),
    ("sl/549.155", "Groundwater (Prohibition of Discharge to Groundwater Bodies) Regulations"),
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


def _titles(urls, cache_name, pattern):
    """English title and publication date of each legislation.mt ELI page (four at a time, resumable cache)."""
    cache_f = pathlib.Path(__file__).resolve().parent / "out" / cache_name
    cache_f.parent.mkdir(exist_ok=True)
    cache = json.loads(cache_f.read_text()) if cache_f.exists() else {}

    def title_of(u):
        try:
            h = get(u, timeout=60).decode("utf-8", "replace")
            m = re.search(pattern, h)
            d = re.search(r'property="eli:date_publication" content="([^"]+)"', h)
            rec = {"title": re.sub(r"\s+", " ", m.group(1)).strip() if m else "", "published": d.group(1) if d else "",
                   "retrieved": TODAY}
        except Exception as e:  # noqa: BLE001
            rec = {"title": f"ERROR {e}", "published": "", "retrieved": TODAY}
        time.sleep(0.25)
        return u, rec

    todo = [u for u in urls if u not in cache or cache[u]["title"].startswith("ERROR")]
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=4) as pool:
        for i, (u, rec) in enumerate(pool.map(title_of, todo)):
            cache[u] = rec
            if i % 25 == 0:
                cache_f.write_text(json.dumps(cache))
    cache_f.write_text(json.dumps(cache))
    return {u: cache[u] for u in urls}


def acts(years=(2024, 2025, 2026), probe=6):
    """Titles of every Act of these years listed in the ELI sitemap, plus the next `probe` numbers after the last
    listed one in each year (a page that does not exist returns an empty generic page), because the sitemap may lag."""
    sm = get("https://legislation.mt/eli/sitemap.xml").decode("utf-8", "replace")
    listed = {}
    for u, y, n in re.findall(r"<loc>(https://legislation\.mt/eli/act/(\d{4})/(\d+))</loc>", sm):
        if int(y) in years:
            listed.setdefault(int(y), set()).add(int(n))
    urls, in_sitemap = [], {}
    for y in years:
        top = max(listed.get(y, {0}))
        for n in range(1, top + probe + 1):
            u = f"https://legislation.mt/eli/act/{y}/{n}"
            urls.append(u)
            in_sitemap[u] = n in listed.get(y, set())
    t = _titles(urls, "act_cache.json", r'about="mlt:eli/act/[^"]+/eng" property="eli:title" content="([^"]+)"')
    kw = r"(?i)water|groundwater|abstraction|borehole|environment|resources|agricultur|energy|planning|aquifer|\bwells?\b"
    found = [u for u in urls if t[u]["title"]]

    def text_counts(u):
        """Mentions of groundwater / abstraction / borehole in the Act's own consolidated PDF (not kept)."""
        try:
            with tempfile.TemporaryDirectory() as tmp:
                p = pathlib.Path(tmp) / "x.pdf"
                p.write_bytes(get(u + "/eng/pdf", timeout=90))
                txt = subprocess.run(["pdftotext", "-layout", str(p), "-"], capture_output=True, text=True).stdout
            time.sleep(0.25)
            return u, [len(re.findall(k, txt, re.I)) for k in ("groundwater", "abstract", "borehole")] + [len(txt)]
        except Exception:  # noqa: BLE001
            return u, ["ERROR"] * 4

    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=4) as pool:
        counts = dict(pool.map(text_counts, found))
    rows = [{"year": u.split("/")[5], "number": u.split("/")[6], "url": u, "in_sitemap": in_sitemap[u],
             "title_en": t[u]["title"], "published": t[u]["published"],
             "matches_water_or_environment": bool(re.search(kw, t[u]["title"])),
             "text_mentions_groundwater": counts.get(u, ["", "", "", ""])[0],
             "text_mentions_abstract": counts.get(u, ["", "", "", ""])[1],
             "text_mentions_borehole": counts.get(u, ["", "", "", ""])[2],
             "text_characters": counts.get(u, ["", "", "", ""])[3], "retrieved": t[u]["retrieved"]}
            for u in urls]
    write("legislation_mt_acts_2024_2026.csv", rows)
    print("errors:", sum(r["title_en"].startswith("ERROR") for r in rows))


def sl_titles(prefixes=("549", "423", "545", "355", "427")):
    """Titles of every subsidiary-legislation instrument under S.L. 549 (environment), 423 (old MRA), 545 (energy and
    water regulator), 355 (WSC) and 427 in the ELI sitemap: a scan for any older abstraction instrument."""
    sm = get("https://legislation.mt/eli/sitemap.xml").decode("utf-8", "replace")
    urls = sorted({u for u in re.findall(r"<loc>(https://legislation\.mt/eli/sl/(?:%s)\.[0-9]+)</loc>" % "|".join(prefixes),
                                         sm)}, key=lambda u: (u.split("/")[-1].split(".")[0],
                                                              int(u.split(".")[-1])))
    t = _titles(urls, "sl_cache.json", r'about="mlt:eli/sl/[^"]+/eng" property="eli:title" content="([^"]+)"')
    kw = r"(?i)groundwater|abstraction|borehole|water polic|\bwells?\b|pump|aquifer|water.controlled|water resources"
    rows = [{"instrument": "S.L. " + u.rsplit("/", 1)[1], "url": u, "title_en": t[u]["title"],
             "published": t[u]["published"], "matches_water_abstraction": bool(re.search(kw, t[u]["title"])),
             "retrieved": t[u]["retrieved"]} for u in urls]
    write("legislation_mt_sl_titles.csv", rows)
    print("errors:", sum(r["title_en"].startswith("ERROR") or not r["title_en"] for r in rows))


if __name__ == "__main__":
    parts = sys.argv[1:] or ["eurostat", "wise", "wise_status", "laws", "notices", "acts", "sl_titles"]
    for part in parts:
        globals()[part]()
