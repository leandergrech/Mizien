"""Claim Check 005: fetch Malta's bathing-water classifications per site and season (2015-2025) and the EU-27
coastal share of excellent bathing waters from the EEA. Needs network; standard library only.

Sources
  EEA DiscoMap ArcGIS service BathingWater_Dyna_WM_2025, layer 3 "Bathing water quality (point)": one record per
    bathing water, with its class for the 2025 season and the ten seasons before it (2015-2024), and coordinates.
  EEA DiscoData SQL, WISE Bathing Water Directive dataset, [WISE_BWD].[latest].[assessment_BathingWaterStatus]
    (seasons to 2024): used to cross-check every Maltese site and season, and for the EU-27 shares 2015-2024.

Outputs (data/cc-005/)
  mt_site_classes.csv   one row per site (87), one column per season 2015-2025, coordinates, DiscoData cross-check
  excellent_share.csv   Malta and EU-27 (coastal; all waters) share of excellent bathing waters per season
"""
import csv
import datetime as dt
import json
import pathlib
import time
import urllib.parse
import urllib.request
from collections import Counter, defaultdict

HERE = pathlib.Path(__file__).resolve().parent
D = HERE.parents[1] / "data" / "cc-005"
D.mkdir(parents=True, exist_ok=True)
TODAY = dt.date.today().isoformat()
SVC = ("https://water.discomap.eea.europa.eu/arcgis/rest/services/BathingWater/BathingWater_Dyna_WM_2025/"
       "MapServer/3/query")
SQL = "https://discodata.eea.europa.eu/sql"
NON_EU = ("AL", "CH", "ME", "UK")
SEASONS = list(range(2015, 2026))
FIELD = {2025 - i: ("qualityStatus" if i == 0 else f"qualityStatus_minus{i}") for i in range(11)}
QMAP = {"1 - Excellent": "Excellent", "2 - Good": "Good", "3 - Sufficient": "Sufficient", "4 - Poor": "Poor"}


def get(url, params):
    full = url + "?" + urllib.parse.urlencode(params)
    for i in range(4):
        try:
            with urllib.request.urlopen(full, timeout=300) as r:
                return json.load(r), full
        except OSError:
            if i == 3:
                raise
            time.sleep(5 * (i + 1))


def sql(q):
    d, full = get(SQL, {"query": q, "p": 1, "nrOfHits": 10000})
    return d["results"], full


# ---------------------------------------------------------------- Malta, per site (map service)
svc, svc_url = get(SVC, {"where": "countryCode='MT'", "outFields": "*", "returnGeometry": "false", "f": "json"})
sites = sorted((f["attributes"] for f in svc["features"]), key=lambda a: a["bathingWaterIdentifier"])
assert len(sites) == 87, len(sites)

# cross-check: DiscoData classification per site and season
dd, dd_url = sql("SELECT bathingWaterIdentifier, season, quality FROM [WISE_BWD].[latest].[assessment_BathingWaterStatus] "
                 "WHERE countryCode='MT' AND season BETWEEN 2015 AND 2024")
ddq = {(r["bathingWaterIdentifier"], r["season"]): QMAP.get(r["quality"], r["quality"]) for r in dd}

rows, mismatches = [], 0
for a in sites:
    row = {"site": a["bathingWaterIdentifier"][-3:], "bathingWaterIdentifier": a["bathingWaterIdentifier"],
           "name": a["bathingWaterName"], "latitude": a["latitude"], "longitude": a["longitude"]}
    bad = []
    for y in SEASONS:
        row[str(y)] = a[FIELD[y]]
        chk = ddq.get((a["bathingWaterIdentifier"], y)) if y <= 2024 else None
        if chk != a[FIELD[y]] and y <= 2024:
            bad.append(f"{y}: {chk}")
    mismatches += len(bad)
    row.update({"discodata_check_2015_2024": "; ".join(bad) or "all seasons match",
                "profile": a["bwProfileLink"], "query_url": svc_url, "retrieved": TODAY})
    rows.append(row)
with open(D / "mt_site_classes.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
print("mt_site_classes.csv", len(rows), "sites;", mismatches, "site-season mismatches with DiscoData")

# ---------------------------------------------------------------- EU-27 shares
eu, eu_url = sql("SELECT season, specialisedZoneType, quality, COUNT(*) AS n "
                 "FROM [WISE_BWD].[latest].[assessment_BathingWaterStatus] "
                 f"WHERE countryCode NOT IN {NON_EU} AND season BETWEEN 2015 AND 2024 "
                 "GROUP BY season, specialisedZoneType, quality")
tot, exc = defaultdict(int), defaultdict(int)
for r in eu:
    coastal = r["specialisedZoneType"] == "coastalBathingWater"
    for k in [(r["season"], "all")] + ([(r["season"], "coastal")] if coastal else []):
        tot[k] += r["n"]
        exc[k] += r["n"] if r["quality"] == "1 - Excellent" else 0
stats = json.dumps([{"statisticType": "count", "onStatisticField": "OBJECTID", "outStatisticFieldName": "n"}])
s25, s25_url = get(SVC, {"where": "EU27='EU-27'", "outStatistics": stats,
                         "groupByFieldsForStatistics": "bwWaterCategory,qualityStatus", "f": "json"})
for f_ in s25["features"]:
    r = f_["attributes"]
    for k in [(2025, "all")] + ([(2025, "coastal")] if r["bwWaterCategory"] == "Coastal" else []):
        tot[k] += r["n"]
        exc[k] += r["n"] if r["qualityStatus"] == "Excellent" else 0

out = []
for y in SEASONS:
    c = Counter(a[FIELD[y]] for a in sites)
    out.append({"season": y, "mt_sites": len(sites), "mt_excellent": c["Excellent"], "mt_good": c["Good"],
                "mt_sufficient": c["Sufficient"], "mt_poor": c["Poor"],
                "mt_excellent_pct": f"{100 * c['Excellent'] / len(sites):.1f}",
                "eu27_coastal_total": tot[(y, "coastal")], "eu27_coastal_excellent": exc[(y, "coastal")],
                "eu27_coastal_excellent_pct": f"{100 * exc[(y, 'coastal')] / tot[(y, 'coastal')]:.1f}",
                "eu27_all_total": tot[(y, "all")], "eu27_all_excellent": exc[(y, "all")],
                "eu27_all_excellent_pct": f"{100 * exc[(y, 'all')] / tot[(y, 'all')]:.1f}",
                "source": ("Malta: EEA DiscoMap BathingWater_Dyna_WM_2025 layer 3. EU-27: EEA DiscoData "
                           "[WISE_BWD].[latest].[assessment_BathingWaterStatus] (2015-2024; excludes AL, CH, ME, UK) "
                           "and DiscoMap 2025 layer 3 statistics (2025). Share = excellent / all identified bathing "
                           "waters, including those not classified."),
                "query_url": svc_url if y == 2025 else eu_url, "retrieved": TODAY})
with open(D / "excellent_share.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0]))
    w.writeheader()
    w.writerows(out)
for r in out:
    print(r["season"], r["mt_excellent"], r["mt_excellent_pct"], r["eu27_coastal_excellent_pct"], r["eu27_all_excellent_pct"])
