#!/usr/bin/env python3
"""CC-124: fetch the Eurostat series that test the CCPI 2026 Malta country text.

Writes data/cc-124/eurostat_*.csv (long format: one value per row, Eurostat status flag, query URL, retrieval date).
Series (Eurostat API, codes as queried):
  cars      road_eqs_carpda  passenger cars by power source, Malta and EU-27, 2015-2025 (TOTAL, ELC = battery electric, plug-in and hybrid)
  carhab    road_eqs_carhab  passenger cars per 1 000 inhabitants, Malta and EU-27, 2015-2025
  fuel      nrg_bal_c        final energy consumption in road transport (FC_TRA_ROAD_E), Malta, ktoe, 2015-2024
  modal     tran_hv_psmod    modal split of inland passenger transport (cars, buses), Malta, 2015-2024
  ren       nrg_ind_ren      renewable energy share (REN), EU-27 + EU aggregate, 2019-2025
  ghg       sdg_13_10        greenhouse gas emissions excl. LULUCF, Malta: index 1990 = 100, Mt CO2e, t per capita (no EU-27 series in this dataset)
  pop       demo_gind        population on 1 January, Malta, 2015-2026
"""
import csv, datetime, json, pathlib, urllib.request

D = pathlib.Path(__file__).resolve().parents[2] / "data" / "cc-124"
B = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
EU = "AT BE BG CY CZ DE DK EE EL ES FI FR HR HU IE IT LT LU LV MT NL PL PT RO SE SI SK".split()
GEO = "&".join(f"geo={g}" for g in EU + ["EU27_2020"])
TODAY = datetime.date.today().isoformat()
Q = {
    "cars": "road_eqs_carpda?geo=MT&geo=EU27_2020&leg_form=TOTAL&mot_nrg=TOTAL&mot_nrg=ELC&mot_nrg=ELC_PET_PI&mot_nrg=ELC_PET_HYB&sinceTimePeriod=2015",
    "carhab": "road_eqs_carhab?geo=MT&geo=EU27_2020&sinceTimePeriod=2015",
    "fuel": "nrg_bal_c?geo=MT&siec=TOTAL&nrg_bal=FC_TRA_ROAD_E&unit=KTOE&sinceTimePeriod=2015",
    "modal": "tran_hv_psmod?geo=MT&vehicle=CAR&vehicle=BUS_TOT&sinceTimePeriod=2015",
    "ren": f"nrg_ind_ren?{GEO}&nrg_bal=REN&sinceTimePeriod=2019",
    "ghg": "sdg_13_10?geo=MT&src_crf=TOTX4_MEMO&sinceTimePeriod=2015",
    "pop": "demo_gind?geo=MT&indic_de=JAN&sinceTimePeriod=2015",
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


if __name__ == "__main__":
    D.mkdir(parents=True, exist_ok=True)
    for name, q in Q.items():
        rows = get(name, q)
        cols = list(dict.fromkeys(c for r in rows for c in r))
        with open(D / f"eurostat_{name}.csv", "w", newline="") as f:
            w = csv.DictWriter(f, cols, lineterminator="\n")
            w.writeheader()
            w.writerows(rows)
        print(name, len(rows), "values")
