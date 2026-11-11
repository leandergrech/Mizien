"""CC-156: Malta's rank among EU-27 states by share of bathing waters rated Excellent, 2015-2025, from the EEA
DiscoMap service BathingWater_Dyna_WM_2025 layer 3 (one record per bathing water, class for 2025 and ten seasons
before). Standard library only; needs network. Output: data/cc-156/country_excellent_share.csv"""
import csv, datetime as dt, json, pathlib, urllib.parse, urllib.request, time
from collections import defaultdict
D = pathlib.Path(__file__).resolve().parents[2] / "data" / "cc-156"
SVC = "https://water.discomap.eea.europa.eu/arcgis/rest/services/BathingWater/BathingWater_Dyna_WM_2025/MapServer/3/query"
FIELD = {2025 - i: ("qualityStatus" if i == 0 else f"qualityStatus_minus{i}") for i in range(11)}
feats, off = [], 0
while True:
    p = {"where": "EU27='EU-27'", "outFields": "countryCode,countryName,bwWaterCategory," + ",".join(FIELD.values()),
         "returnGeometry": "false", "f": "json", "resultOffset": off, "resultRecordCount": 2000, "orderByFields": "OBJECTID"}
    for i in range(4):
        try:
            d = json.load(urllib.request.urlopen(SVC + "?" + urllib.parse.urlencode(p), timeout=300)); break
        except OSError:
            if i == 3: raise
            time.sleep(5)
    feats += [f["attributes"] for f in d["features"]]
    if not d.get("exceededTransferLimit"): break
    off += len(d["features"])
print(len(feats), "records")
rows = []
for scope in ("coastal", "all"):
    for y in range(2015, 2026):
        tot, exc = defaultdict(int), defaultdict(int)
        for a in feats:
            if scope == "coastal" and a["bwWaterCategory"] != "Coastal": continue
            q = a[FIELD[y]]
            if q is None: continue  # not identified / no class that season
            tot[a["countryCode"]] += 1; exc[a["countryCode"]] += q == "Excellent"
        ranked = sorted(tot, key=lambda c: -exc[c] / tot[c])
        for c in tot:
            rows.append({"scope": scope, "season": y, "country": c, "sites": tot[c], "excellent": exc[c],
                         "excellent_pct": round(100 * exc[c] / tot[c], 1),
                         "rank": 1 + sum(exc[o] / tot[o] > exc[c] / tot[c] for o in tot), "n_countries": len(tot)})
with open(D / "country_excellent_share.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]) + ["source", "retrieved"]); w.writeheader()
    for r in rows:
        r.update(source=SVC + " (where EU27='EU-27'; qualityStatus fields). Sites with no class that season excluded.",
                 retrieved=dt.date.today().isoformat()); w.writerow(r)
for s in ("coastal", "all"):
    for y in (2016, 2019, 2022, 2024, 2025):
        m = [r for r in rows if r["scope"] == s and r["season"] == y and r["country"] == "MT"][0]
        print(s, y, m["excellent"], m["sites"], m["excellent_pct"], "rank", m["rank"], "of", m["n_countries"])
