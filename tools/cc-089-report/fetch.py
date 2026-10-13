#!/usr/bin/env python3
"""CC-089: fetch the public data that tests the Malta Chamber / PwC population and infrastructure figures.

Writes data/cc-089/*.csv (long format: one value per row, Eurostat status flag, query URL, retrieval date).
Network needed. Series (Eurostat API, codes as queried):
  pop       demo_gind       population on 1 January (JAN), all EU-27 + EU aggregate, 2015-2026
  proj      proj_25np       EUROPOP2025 projections for Malta, all variants, 2025-2035
  beds_nr   hlth_rs_bds1    hospital beds, number (NR), Malta, 2015-2025
  beds_100k hlth_rs_bds1    hospital beds per 100 000 inhabitants (P_HTHAB), EU-27, 2015-2025
  elec      nrg_cb_e        electricity (E7000), GWh: GEP, IMP, EXP, DL, AFC, Malta, 2015-2025
  medage    demo_pjanind    median age of the population on 1 January (MEDAGEPOP), EU-27, 2024-2025
  area      demo_r_d3area   land area, Malta (km2)
World Bank (EN.POP.DNST, people per km2 of land area, 2023) is saved by the same script.
"""
import csv, datetime, json, pathlib, urllib.request

D = pathlib.Path(__file__).resolve().parents[2] / "data" / "cc-089"
B = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
EU = "AT BE BG CY CZ DE DK EE EL ES FI FR HR HU IE IT LT LU LV MT NL PL PT RO SE SI SK".split()
GEO = "&".join(f"geo={g}" for g in EU + ["EU27_2020"])
TODAY = datetime.date.today().isoformat()
Q = {
    "pop": f"demo_gind?{GEO}&indic_de=JAN&sinceTimePeriod=2015",
    "proj": "proj_25np?geo=MT&sex=T&age=TOTAL&sinceTimePeriod=2025&untilTimePeriod=2035",
    "beds_nr": "hlth_rs_bds1?geo=MT&unit=NR&facility=HBEDT&hlthcare=TOTAL&sinceTimePeriod=2015",
    "beds_100k": f"hlth_rs_bds1?{GEO}&unit=P_HTHAB&facility=HBEDT&hlthcare=TOTAL&sinceTimePeriod=2015",
    "elec": "nrg_cb_e?geo=MT&siec=E7000&unit=GWH&nrg_bal=GEP&nrg_bal=IMP&nrg_bal=EXP&nrg_bal=DL&nrg_bal=AFC"
            "&sinceTimePeriod=2015",
    "medage": f"demo_pjanind?{GEO}&indic_de=MEDAGEPOP&sinceTimePeriod=2024",
    "area": "demo_r_d3area?geo=MT&landuse=TOTAL&unit=KM2",
}


def get(name, q):
    url = B + q + "&format=JSON&lang=EN"
    d = json.load(urllib.request.urlopen(url, timeout=240))
    ids, sizes = d["id"], d["size"]
    cats = {k: {i: c for c, i in d["dimension"][k]["category"]["index"].items()} for k in ids}
    out = []
    for k, v in d["value"].items():
        n, pos = int(k), {}
        for dim, s in zip(reversed(ids), reversed(sizes)):
            pos[dim] = cats[dim][n % s]
            n //= s
        pos.pop("freq", None)
        out.append({"series": name, **pos, "value": v, "flag": d.get("status", {}).get(k, ""),
                    "dataset_updated": d.get("updated", ""), "url": url, "retrieved": TODAY})
    return out


def write(name, rows):
    cols = list(dict.fromkeys(c for r in rows for c in r))
    with open(D / f"eurostat_{name}.csv", "w", newline="") as f:
        w = csv.DictWriter(f, cols, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(name, len(rows), "values")


if __name__ == "__main__":
    D.mkdir(parents=True, exist_ok=True)
    for name, q in Q.items():
        write(name, get(name, q))
    wb = "https://api.worldbank.org/v2/country/all/indicator/EN.POP.DNST?format=json&date=2023&per_page=400"
    j = json.load(urllib.request.urlopen(wb, timeout=120))[1]
    with open(D / "worldbank_density_2023.csv", "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["iso3", "name", "year", "people_per_km2_land", "url", "retrieved"])
        for r in j:
            w.writerow([r["countryiso3code"], r["country"]["value"], r["date"], r["value"], wb, TODAY])
    print("worldbank", len(j))
