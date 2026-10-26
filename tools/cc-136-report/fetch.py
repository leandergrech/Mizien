#!/usr/bin/env python3
"""CC-136: fetch (1) World Bank population density (EN.POP.DNST, people per sq. km of land area) for European states
and microstates, (2) Eurostat demo_r_d3dens (national level, people per km2) for EU/EFTA/candidate countries,
(3) Eurostat demo_gind population on 1 January for Malta and the EU-27.
Outputs in data/cc-136."""
import csv, datetime, json, pathlib, urllib.request
ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-136"
D.mkdir(exist_ok=True)
today = datetime.date.today().isoformat()
UA = {"User-Agent": "Mizien-factcheck/1.0"}


def get(url):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60))


# 1. World Bank
EUROPE = ("ALB AND AUT BLR BEL BIH BGR HRV CYP CZE DNK EST FIN FRA DEU GRC HUN ISL IRL ITA XKX LVA LIE LTU LUX MLT MDA "
          "MCO MNE NLD MKD NOR POL PRT ROU RUS SMR SRB SVK SVN ESP SWE CHE UKR GBR").split()
url = ("https://api.worldbank.org/v2/country/" + ";".join(EUROPE) +
       "/indicator/EN.POP.DNST?format=json&date=2015:2024&per_page=1000")
d = get(url)
with open(D / "worldbank_density.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["iso3", "country", "year", "people_per_km2_land", "indicator_lastupdated", "query_url", "retrieved"])
    for r in d[1]:
        if r["value"] is not None:
            w.writerow([r["countryiso3code"], r["country"]["value"], r["date"], r["value"], d[0]["lastupdated"], url, today])
print("worldbank", len(d[1]), d[0]["lastupdated"])

# 2. Eurostat national density
url = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/demo_r_d3dens?format=JSON&lang=en&sinceTimePeriod=2015&unit=PER_KM2"
d = get(url)
dims, size = d["id"], d["size"]
idx = [{v: k for k, v in d["dimension"][n]["category"]["index"].items()} for n in dims]
lab = d["dimension"]["geo"]["category"]["label"]
with open(D / "eurostat_demo_r_d3dens.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["geo", "geo_label", "year", "value_per_km2", "flag", "eurostat_updated", "query_url", "retrieved"])
    for k, val in sorted(d["value"].items(), key=lambda kv: int(kv[0])):
        pos, out = int(k), []
        for s in reversed(size):
            out.append(pos % s); pos //= s
        c = {n: idx[i][x] for i, (n, x) in enumerate(zip(dims, out[::-1]))}
        if len(c["geo"]) == 2 or c["geo"] in ("EU27_2020",):
            w.writerow([c["geo"], lab[c["geo"]], c["time"], val, d.get("status", {}).get(k, ""), d["updated"], url, today])
print("eurostat density", d["updated"])


# 4. Eurostat population on 1 January (demo_gind JAN) for Malta and EU-27, for the 'nearly 30 percent' sub-claim
url = ("https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/demo_gind?geo=MT&geo=EU27_2020"
       "&indic_de=JAN&sinceTimePeriod=2005")
d = get(url)
dims, size = d["id"], d["size"]
idx = [{v: k for k, v in d["dimension"][n]["category"]["index"].items()} for n in dims]
with open(D / "eurostat_demo_gind_jan.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["geo", "year", "population_1_jan", "flag", "eurostat_updated", "query_url", "retrieved"])
    for k, val in sorted(d["value"].items(), key=lambda kv: int(kv[0])):
        pos, out = int(k), []
        for s in reversed(size):
            out.append(pos % s); pos //= s
        c = {n: idx[i][x] for i, (n, x) in enumerate(zip(dims, out[::-1]))}
        w.writerow([c["geo"], c["time"], val, d.get("status", {}).get(k, ""), d["updated"], url, today])
print("demo_gind", d["updated"])
