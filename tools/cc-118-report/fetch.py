#!/usr/bin/env python3
"""CC-118: download the data behind the check into data/cc-118/ (each file keeps its source URL and retrieval date).

1. EEA indicator page 'Worst seasonal water scarcity conditions for European countries in 2023, measured by the
   water exploitation index plus (WEI+)': the chart's values (maximum seasonal WEI+ per country and the quarter
   in which it occurs), read from the page's embedded chart data.
2. Eurostat sdg_06_60 (annual WEI+, %), all countries, 2023.
3. EEA WISE, Malta's WFD 2022 reporting (third cycle, assessment 2017-2021): ecological status or potential and
   chemical status of every surface water body; quantitative and chemical status and area of every groundwater body.

    python fetch.py            # everything
4. Energy and Water Agency, Technical Document in support of the 3rd RBMP: Monitoring Results for the Groundwater
   Quantitative Status Assessment (May 2024), Table 1: groundwater-level trend at each monitoring borehole.

    python fetch.py eea | eurostat | wise | ewa
"""
import csv, datetime, json, pathlib, subprocess, sys, urllib.parse, urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-118"
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


def eea():
    url = ("https://www.eea.europa.eu/en/analysis/indicators/use-of-freshwater-resources-in-europe-1/"
           "worst-seasonal-water-scarcity-conditions")
    t = get(url).decode("utf8")
    s = t[t.index("window.__data=") + 14:]
    s = s[:s.index("</script>")].rstrip().rstrip(";").replace(": undefined", ": null")
    c = json.loads(s)["reduxAsyncConnect"]["content"]
    ds = c["visualization"]["dataSources"]
    ys, xs = ds["Country (worst quarter)"], ds["Max Value (%)"]
    rows = []
    for y, x in zip(ys, xs):
        if not y:
            continue
        country, q = y.rsplit(" (", 1)
        rows.append({"country": country, "worst_quarter": q.rstrip(")"), "max_seasonal_wei_plus_pct": x.rstrip("%"),
                     "year": 2023, "indicator_modified": c.get("modified"), "source": "EEA indicator page (chart data)",
                     "url": url, "retrieved": TODAY})
    write("eea_worst_seasonal_wei_2023.csv", rows)


def eurostat():
    url = ("https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sdg_06_60?format=JSON&lang=en"
           "&time=2023&time=2022&time=2021")
    d = json.loads(get(url))
    dims, sz = d["id"], d["size"]
    cats = [[c for c, _ in sorted(d["dimension"][k]["category"]["index"].items(), key=lambda kv: kv[1])] for k in dims]
    glab = d["dimension"]["geo"]["category"]["label"]
    slab = d["dimension"]["statinfo"]["category"]["label"]
    rows = []
    for key, v in d["value"].items():
        n, pos = int(key), []
        for s in reversed(sz):
            pos.append(n % s); n //= s
        pos.reverse()
        r = {k: cats[i][p] for i, (k, p) in enumerate(zip(dims, pos))}
        rows.append({"dataset": "sdg_06_60", "geo": r["geo"], "geo_label": glab[r["geo"]], "statinfo": r["statinfo"], "statinfo_label": slab[r["statinfo"]], "unit": r["unit"], "year": r["time"],
                     "wei_plus_pct": v, "flag": d.get("status", {}).get(key, ""), "eurostat_updated": d.get("updated"),
                     "query_url": url, "retrieved": TODAY})
    rows.sort(key=lambda r: (r["statinfo"], r["year"], -r["wei_plus_pct"]))
    write("eurostat_sdg_06_60.csv", rows)


WISE = "https://water.discomap.eea.europa.eu/arcgis/rest/services/WISE_WFD/"


def q(service, layer):
    p = urllib.parse.urlencode({"where": "countryCode='MT'", "outFields": "*", "returnGeometry": "false", "f": "json"})
    url = f"{WISE}{service}/MapServer/{layer}/query?{p}"
    return [f["attributes"] for f in json.loads(get(url))["features"]], url


ECO = {"1": "High", "2": "Good", "3": "Moderate", "4": "Poor", "5": "Bad", "6": "Unknown", "0": "Unknown"}
CHEM = {"2": "Good", "3": "Failing to achieve good"}
GW = {"2": "Good", "3": "Poor"}


def wise():
    rows = []
    for layer in (3, 4, 5, 6, 14):  # river, lake, transitional, coastal, territorial (one layer per category)
        feats, url = q("WFD2022_SurfaceWaterBody_WM", layer)
        for a in feats:
            rows.append({"eu_code": a["euSurfaceWaterBodyCode"], "category": a["surfaceWaterBodyCategory"],
                         "natural_or_hmwb": a["naturalAWBHMWB"], "area_km2": a["cArea"], "length_km": a["cLength"],
                         "ecological_status_code": a["swEcologicalStatusOrPotentialValue"],
                         "ecological_status_label_unverified": ECO.get(a["swEcologicalStatusOrPotentialValue"], "?"),
                         "ecological_assessment_year": a["swEcologicalAssessmentYear"],
                         "chemical_status_code": a["swChemicalStatusValue"],
                         "chemical_status_label_unverified": CHEM.get(a["swChemicalStatusValue"], "?"),
                         "chemical_assessment_year": a["swChemicalAssessmentYear"],
                         "reporting_year": a["cYear"], "source": f"EEA WISE WFD2022_SurfaceWaterBody_WM layer {layer}",
                         "url": url, "retrieved": TODAY})
    rows.sort(key=lambda r: r["eu_code"])
    write("wise_2022_surface_water_status.csv", rows)
    feats, url = q("WFD2022_GroundWaterBody_WM", 0)
    rows = [{"eu_code": a["euGroundWaterBodyCode"], "name": a["groundWaterBodyName"], "area_km2": a["cArea"],
             "geological_formation": a["geologicalFormation"], "quantitative_status_code": a["gwQuantitativeStatusValue"],
             "quantitative_status": GW.get(a["gwQuantitativeStatusValue"], "?"),
             "quantitative_assessment_year": a["gwQuantitativeAssessmentYear"],
             "chemical_status_code": a["gwChemicalStatusValue"], "chemical_status": GW.get(a["gwChemicalStatusValue"], "?"),
             "chemical_assessment_year": a["gwChemicalAssessmentYear"], "reporting_year": a["cYear"],
             "source": "EEA WISE WFD2022_GroundWaterBody_WM layer 0 (legend: 2 = Good, 3 = Poor)", "url": url,
             "retrieved": TODAY} for a in feats]
    rows.sort(key=lambda r: r["eu_code"])
    write("wise_2022_groundwater_status.csv", rows)


def ewa():
    import re, tempfile
    url = ("https://energywateragency.gov.mt/wp-content/uploads/2024/05/"
           "Technical-Document-Status-of-the-Quantitative-monitoring-network_Final.pdf")
    with tempfile.TemporaryDirectory() as t:
        pdf = pathlib.Path(t) / "ewa.pdf"
        subprocess.run(["curl", "-sSL", "-A", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126", "-o", str(pdf), url], check=True)  # energywateragency.gov.mt: 403 to urllib and to the longer Chrome UA string; 200 to curl with this one
        txt = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True).stdout
    rows = []
    for m in re.finditer(r"^\s*(MT\d{3})\s+(\d{5})\s+(.+?)\s{2,}(No trend|Significant (?:negative|positive) trend)\s*$", txt, re.M):
        rows.append({"gwb": m.group(1), "borehole_id": m.group(2), "borehole": m.group(3).strip(), "trend": m.group(4),
                     "period": "Jan 2000 - Dec 2021 (Table 1 title)", "source": "EWA technical document, May 2024, Table 1",
                     "url": url, "retrieved": TODAY})
    write("ewa_gw_level_trends.csv", rows)


if __name__ == "__main__":
    for name, fn in (("eea", eea), ("eurostat", eurostat), ("wise", wise), ("ewa", ewa)):
        if len(sys.argv) == 1 or name in sys.argv[1:]:
            fn()
