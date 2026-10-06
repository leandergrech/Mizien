#!/usr/bin/env python3
"""CC-032: download the modelled solar yield and the shuttle route length into data/cc-032/ (needs network).

1. PVGIS 5.3 (European Commission, Joint Research Centre), PVcalc API, at the Ta' Xħajma Park and Ride
   (OpenStreetMap way 1455497043, 36.0380 N, 14.2720 E): 37.5 kWp (15 units x 2.5 kWp, the manufacturer's nominal
   output), crystalline silicon, PVGIS's default 14% system loss, (a) two-axis tracking and (b) a fixed array at the
   optimal tilt and azimuth. Raw JSON is kept; monthly and yearly values go to pvgis_monthly.csv.
2. OSRM (project-osrm.org demo server, OpenStreetMap data): driving distance from the Park and Ride to the Mġarr
   ferry terminal (OSM node 9288572631) and back -> route_osrm.csv.
"""
import csv
import datetime
import json
import pathlib
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-032"
D.mkdir(exist_ok=True)
TODAY = datetime.date.today().isoformat()
HUB = (36.0380313, 14.2719662)        # Ta' Xħajma Park and Ride, OSM way 1455497043 (Nominatim, 6 Oct 2026)
MGARR = (36.0243876, 14.2981580)      # Mġarr ferry terminal, OSM node 9288572631 (Nominatim, 6 Oct 2026)
KWP = 37.5
PV = ("https://re.jrc.ec.europa.eu/api/v5_3/PVcalc?lat={:.4f}&lon={:.4f}&peakpower={}&loss=14&outputformat=json"
      .format(HUB[0], HUB[1], KWP))
RUNS = {"two_axis": PV + "&twoaxis=1", "fixed_optimal": PV + "&optimalangles=1"}


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mizien fact-check (research)"})
    return json.load(urllib.request.urlopen(req, timeout=90))


rows = []
for name, url in RUNS.items():
    d = get(url)
    (D / f"pvgis_{name}.json").write_text(json.dumps(d, indent=1), encoding="utf-8")
    key = "two_axis" if name == "two_axis" else "fixed"
    for m in d["outputs"]["monthly"][key]:
        rows.append({"system": name, "month": m["month"], "E_d_kWh": m["E_d"], "E_m_kWh": m["E_m"],
                     "H_i_d_kWh_m2": m["H(i)_d"], "source": "PVGIS 5.3 PVcalc (JRC); " + d["inputs"]["meteo_data"]["radiation_db"],
                     "url": url, "retrieved": TODAY})
    t = d["outputs"]["totals"][key]
    rows.append({"system": name, "month": "year", "E_d_kWh": t["E_d"], "E_m_kWh": t["E_y"], "H_i_d_kWh_m2": t["H(i)_d"],
                 "source": "PVGIS 5.3 PVcalc (JRC); " + d["inputs"]["meteo_data"]["radiation_db"], "url": url,
                 "retrieved": TODAY})
    print(name, d["inputs"]["mounting_system"], "E_y =", t["E_y"])
with open(D / "pvgis_monthly.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)

route = []
for a, b, label in ((HUB, MGARR, "Park and Ride to Mġarr ferry terminal"), (MGARR, HUB, "Mġarr ferry terminal to Park and Ride")):
    url = f"https://router.project-osrm.org/route/v1/driving/{a[1]},{a[0]};{b[1]},{b[0]}?overview=false"
    r = get(url)["routes"][0]
    route.append({"leg": label, "distance_m": round(r["distance"]), "duration_s": round(r["duration"]),
                  "source": "OSRM demo server, OpenStreetMap road data (car profile)", "url": url, "retrieved": TODAY})
    print(label, round(r["distance"]), "m")
with open(D / "route_osrm.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(route[0]))
    w.writeheader()
    w.writerows(route)
