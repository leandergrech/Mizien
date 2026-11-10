"""CC-156: coastal bathing waters rated Excellent, by EU-27 country, for the 2016 and 2025 seasons.
2016: EEA DiscoData WISE_BWD assessment_BathingWaterStatus; 2025: EEA DiscoMap BathingWater_Dyna_WM_2025 layer 3.
Output: data/cc-156/country_excellent_share.csv"""
import csv, datetime as dt, json, pathlib, time, urllib.parse, urllib.request
from collections import defaultdict
D = pathlib.Path(__file__).resolve().parents[2] / "data" / "cc-156"
TODAY = dt.date.today().isoformat()
SVC = "https://water.discomap.eea.europa.eu/arcgis/rest/services/BathingWater/BathingWater_Dyna_WM_2025/MapServer/3/query"
SQL = "https://discodata.eea.europa.eu/sql"
def get(url, params):
    full = url + "?" + urllib.parse.urlencode(params)
    for i in range(4):
        try:
            with urllib.request.urlopen(full, timeout=300) as r:
                return json.load(r), full
        except OSError:
            if i == 3: raise
            time.sleep(5 * (i + 1))
res = {}
for season in (2016, 2024):
    d, u1 = get(SQL, {"query": "SELECT countryCode, quality, COUNT(*) AS n FROM [WISE_BWD].[latest].[assessment_BathingWaterStatus] "
        f"WHERE specialisedZoneType='coastalBathingWater' AND season={season} GROUP BY countryCode, quality", "p": 1, "nrOfHits": 10000})
    res[season] = (d["results"], u1)
tot, exc = defaultdict(int), defaultdict(int)
for r in res[2016][0]:
    tot[("2016", r["countryCode"])] += r["n"]
    if r["quality"] == "1 - Excellent": exc[("2016", r["countryCode"])] += r["n"]
for r in res[2024][0]:
    tot[("2024", r["countryCode"])] += r["n"]
    if r["quality"] == "1 - Excellent": exc[("2024", r["countryCode"])] += r["n"]
stats = json.dumps([{"statisticType": "count", "onStatisticField": "OBJECTID", "outStatisticFieldName": "n"}])
s, u25 = get(SVC, {"where": "EU27='EU-27' AND bwWaterCategory='Coastal'", "outStatistics": stats,
                   "groupByFieldsForStatistics": "countryCode,qualityStatus", "f": "json"})
for f in s["features"]:
    a = f["attributes"]; tot[("2025", a["countryCode"])] += a["n"]
    if "Excellent" in str(a["qualityStatus"]): exc[("2025", a["countryCode"])] += a["n"]
rows = []
for (y, c), t in sorted(tot.items()):
    if c in ("AL", "CH", "ME", "UK", "GB", "XK"): continue
    rows.append({"season": y, "country": c, "coastal_sites": t, "excellent": exc[(y, c)],
                 "excellent_pct": round(100 * exc[(y, c)] / t, 2),
                 "source": "EEA DiscoData WISE_BWD assessment_BathingWaterStatus" if y != "2025" else "EEA DiscoMap BathingWater_Dyna_WM_2025 layer 3",
                 "url": res[2016][1] if y == "2016" else (res[2024][1] if y == "2024" else u25), "retrieved": TODAY})
with open(D / "country_excellent_share.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, rows[0].keys()); w.writeheader(); w.writerows(rows)
print(len(rows), "rows")
