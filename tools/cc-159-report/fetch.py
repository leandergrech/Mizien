#!/usr/bin/env python3
"""CC-159: fetch Eurostat (1) demo_r_d3dens national density, people per km2 (total area), 2015-latest, all EU states
and the EU-27 aggregate; (2) demo_gind population on 1 January for Malta and the EU-27; (3) reg_area3 land/total area
(km2) national level; (4) World Bank EN.POP.DNST (land-area basis) for EU states. Outputs in data/cc-159."""
import csv, datetime, json, pathlib, urllib.request
ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-159"; D.mkdir(exist_ok=True)
today = datetime.date.today().isoformat()
UA = {"User-Agent": "Mizien-factcheck/1.0"}
EUS = "AT BE BG CY CZ DE DK EE EL ES FI FR HR HU IE IT LT LU LV MT NL PL PT RO SE SI SK".split()
GEO = "&".join(f"geo={g}" for g in EUS + ["EU27_2020"])
B = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"


def get(url):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120))


def flat(d):
    dims, size = d["id"], d["size"]
    idx = [{v: k for k, v in d["dimension"][n]["category"]["index"].items()} for n in dims]
    for k, val in sorted(d["value"].items(), key=lambda kv: int(kv[0])):
        pos, out = int(k), []
        for s in reversed(size):
            out.append(pos % s); pos //= s
        c = {n: idx[i][x] for i, (n, x) in enumerate(zip(dims, out[::-1]))}
        yield c, val, d.get("status", {}).get(k, "")


def dump(name, url, cols, rowf):
    d = get(url)
    with open(D / name, "w", newline="") as f:
        w = csv.writer(f); w.writerow(cols + ["label", "eurostat_updated", "query_url", "retrieved"])
        for c, val, fl in flat(d):
            w.writerow(rowf(c, val, fl) + [d.get("label", ""), d.get("updated", ""), url, today])
    print(name, d.get("label"), d.get("updated"))


dump("eurostat_demo_r_d3dens.csv", f"{B}demo_r_d3dens?{GEO}&unit=PER_KM2&sinceTimePeriod=2015&format=JSON",
     ["geo", "year", "value_per_km2", "flag"], lambda c, v, f: [c["geo"], c["time"], v, f])
dump("eurostat_demo_gind_jan.csv", f"{B}demo_gind?{GEO}&indic_de=JAN&sinceTimePeriod=2015&format=JSON",
     ["geo", "year", "population_1_jan", "flag"], lambda c, v, f: [c["geo"], c["time"], v, f])
d = get(f"{B}reg_area3?{GEO}&landuse=TOTAL&format=JSON")
print("reg_area3 dims", d["id"], d["size"], d.get("label"))
dump("eurostat_reg_area3.csv", f"{B}reg_area3?{GEO}&landuse=TOTAL&format=JSON",
     ["geo", "year", "area_km2", "flag"], lambda c, v, f: [c["geo"], c["time"], v, f])
wb = ("https://api.worldbank.org/v2/country/AUT;BEL;BGR;HRV;CYP;CZE;DNK;EST;FIN;FRA;DEU;GRC;HUN;IRL;ITA;LVA;LTU;LUX;MLT;NLD;POL;PRT;ROU;SVK;SVN;ESP;SWE"
      "/indicator/EN.POP.DNST?format=json&date=2015:2024&per_page=1000")
d = get(wb)
with open(D / "worldbank_density_eu27.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["iso3", "country", "year", "people_per_km2_land", "indicator_lastupdated", "query_url", "retrieved"])
    for r in d[1]:
        if r["value"] is not None:
            w.writerow([r["countryiso3code"], r["country"]["value"], r["date"], r["value"], d[0]["lastupdated"], wb, today])
print("worldbank", d[0]["lastupdated"])
