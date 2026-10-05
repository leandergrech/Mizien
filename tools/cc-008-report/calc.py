"""Claim Check 008: January-September NO2 before and after the Msida Creek flyover opened to traffic
(18 December 2025), and distance checks for the map. Reads data/cc-008/ (from fetch_data.py); writes
data/cc-008/no2_jan_sep.csv and data/cc-008/checks.csv. Works offline.
Means are hour-weighted (sum of valid hourly values / valid hours) = the mean of all valid hours in the window."""
import calendar
import csv
import json
import math
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
D = HERE.parents[1] / "data" / "cc-008"
M = list(csv.DictReader(open(D / "no2_monthly.csv")))
A = {(r["station"], int(r["year"])): r for r in csv.DictReader(open(D / "no2_annual.csv"))}
S = {r["station"]: r for r in csv.DictReader(open(D / "aq_stations.csv"))}
FLY = [pt for f in json.load(open(D / "flyovers_osm.geojson"))["features"] for pt in f["geometry"]["coordinates"]]
MARSA = (14.49449, 35.88289)  # Marsa junction, as located in claims/CC-008/claim.yml
ST = ["MT00011", "MT00008", "MT00004", "MT00009"]
BACKGROUND = ["MT00008", "MT00004"]  # Attard and Żejtun, urban background


def window(code, year, months):
    s = n = 0
    for r in M:
        y, m = map(int, r["month"].split("-"))
        if r["station"] == code and y == year and m in months and r["no2_ugm3"]:
            s += float(r["no2_ugm3"]) * int(r["valid_hours"])
            n += int(r["valid_hours"])
    return (s / n if n else math.nan), n


def metres(a, b):
    """Great-circle distance in metres between (lon, lat) points."""
    la1, la2 = math.radians(a[1]), math.radians(b[1])
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin(math.radians(b[0] - a[0]) / 2) ** 2
    return 2 * 6371000 * math.asin(math.sqrt(h))


rows = []
res = {}
for label, months in [("Jan-Sep", range(1, 10)), ("Jan-Aug", range(1, 9))]:
    for year in (2024, 2025, 2026):
        r_ = {c: window(c, year, months) for c in ST}
        bg = sum(r_[c][0] for c in BACKGROUND) / len(BACKGROUND)
        possible = sum(calendar.monthrange(year, m)[1] * 24 for m in months)
        for c in ST:
            v, n = r_[c]
            res[(label, year, c)] = v
            res[(label, year, "bg")] = bg
            rows.append({"window": label, "year": year, "station": c, "no2_ugm3": f"{v:.2f}", "valid_hours": n,
                         "coverage_pct": f"{100 * n / possible:.1f}",
                         "background_mean_ugm3": f"{bg:.2f}",
                         "difference_from_background_ugm3": f"{v - bg:.2f}",
                         "validation": "E2a (up-to-date; not validated)" if year == 2026 else "E1a (validated)"})
with open(D / "no2_jan_sep.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)

pt = lambda c: (float(S[c]["lon"]), float(S[c]["lat"]))
pct = lambda a, b: f"{100 * (b / a - 1):+.1f}"
J = "Jan-Sep"
checks = [
    ("Distance, old Msida point MT00005 to new point MT00011 (m)", f"{metres(pt('MT00005'), pt('MT00011')):.0f}"),
    ("Distance, MT00005 to nearest point of the flyover as mapped (m)", f"{min(metres(pt('MT00005'), q) for q in FLY):.0f}"),
    ("Distance, MT00011 to nearest point of the flyover as mapped (m)", f"{min(metres(pt('MT00011'), q) for q in FLY):.0f}"),
    ("Distance, Marsa junction to Kordin station MT00003 (closed 2016) (m)", f"{metres(MARSA, pt('MT00003')):.0f}"),
    ("Distance, Marsa junction to nearest station operating in 2026 (m)",
     f"{min(metres(MARSA, pt(c)) for c in ('MT00004', 'MT00008', 'MT00009', 'MT00011')):.0f}"),
    ("MT00005 annual mean 2013 (ug/m3)", A[("MT00005", 2013)]["no2_ugm3"]),
    ("MT00005 annual mean 2023 (ug/m3)", A[("MT00005", 2023)]["no2_ugm3"]),
    ("MT00011 Jan-Sep change 2025 to 2026 (%)", pct(res[(J, 2025, "MT00011")], res[(J, 2026, "MT00011")])),
    ("Attard Jan-Sep change 2025 to 2026 (%)", pct(res[(J, 2025, "MT00008")], res[(J, 2026, "MT00008")])),
    ("Zejtun Jan-Sep change 2025 to 2026 (%)", pct(res[(J, 2025, "MT00004")], res[(J, 2026, "MT00004")])),
    ("St Paul's Bay Jan-Sep change 2025 to 2026 (%)", pct(res[(J, 2025, "MT00009")], res[(J, 2026, "MT00009")])),
    ("MT00011 minus background, Jan-Sep 2024/2025/2026 (ug/m3)",
     "/".join(f"{res[(J, y, 'MT00011')] - res[(J, y, 'bg')]:.1f}" for y in (2024, 2025, 2026))),
    ("MT00011 minus background, Jan-Aug 2024/2025/2026 (ug/m3)",
     "/".join(f"{res[('Jan-Aug', y, 'MT00011')] - res[('Jan-Aug', y, 'bg')]:.1f}" for y in (2024, 2025, 2026))),
]
with open(D / "checks.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["check", "value"])
    w.writerows(checks)
for r in rows:
    print(r["window"], r["year"], r["station"], r["no2_ugm3"], r["coverage_pct"], r["difference_from_background_ugm3"])
for c, v in checks:
    print(c, v)
