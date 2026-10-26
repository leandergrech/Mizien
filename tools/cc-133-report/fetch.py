"""Download Eurostat inputs for CC-133 to data/cc-133/eurostat_housing.csv (Malta and EU-27).
tipsho60: standardised house price-to-income ratio (MIP auxiliary indicator: nominal HPI / adjusted household gross
disposable income per head); prc_hpi_a: house price index, total purchases; prc_hicp_aind CP041: actual rentals;
nasa_10_nf_tr: household (S14_S15) gross disposable income B6G and adjusted B7G, current prices; nama_10_pe: population.
Writes a long CSV: dataset, geo, item, unit, year, value, flag, url, retrieved, dataset_updated."""
import csv, datetime, json, pathlib, urllib.request

OUT = pathlib.Path(__file__).resolve().parents[2] / "data" / "cc-133"
B = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
TODAY = datetime.date.today().isoformat()
GEO = "geo=MT&geo=EU27_2020"


def get(ds, q):
    url = B + ds + "?" + q + "&format=JSON&lang=EN"
    d = json.load(urllib.request.urlopen(url))
    dims = d["id"]; sizes = d["size"]; pos = {k: d["dimension"][k]["category"]["index"] for k in dims}
    inv = {k: {v: c for c, v in pos[k].items()} for k in dims}
    flags = d.get("status", {})
    rows = []
    for idx, val in d["value"].items():
        i = int(idx); coords = {}
        for k, n in reversed(list(zip(dims, sizes))):
            coords[k] = inv[k][i % n]; i //= n
        rows.append((coords, val, flags.get(idx, "")))
    return url, d.get("updated", ""), rows


QUERIES = [
    ("tipsho60", GEO, lambda c: "PTIR"),
    ("prc_hpi_a", GEO + "&purchase=TOTAL&unit=I15_A_AVG&unit=RCH_A_AVG&sinceTimePeriod=2004", lambda c: c["purchase"]),
    ("prc_hicp_aind", GEO + "&coicop=CP041&unit=INX_A_AVG&unit=RCH_A_AVG&sinceTimePeriod=2004", lambda c: c["coicop"]),
    ("nasa_10_nf_tr", GEO + "&na_item=B6G&na_item=B7G&sector=S14_S15&direct=RECV&unit=CP_MEUR&sinceTimePeriod=2004",
     lambda c: c["na_item"] + "_" + c["sector"]),
    ("nama_10_pe", GEO + "&na_item=POP_NC&unit=THS_PER&sinceTimePeriod=2004", lambda c: c["na_item"]),
    # EU-SILC median equivalised net income (survey year t refers to income year t-1): a household-level cross-check
    ("ilc_di03", GEO + "&statinfo=MED_EI&unit=EUR&age=TOTAL&sex=T&sinceTimePeriod=2005", lambda c: c["statinfo"]),
]


def main():
    rows = []
    for ds, q, item in QUERIES:
        url, upd, r = get(ds, q)
        for c, v, f in r:
            rows.append([ds, c["geo"], item(c), c["unit"], c["time"], v, f, url, TODAY, upd])
        print(ds, len(r), "values; updated", upd)
    with open(OUT / "eurostat_housing.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh); w.writerow(["dataset", "geo", "item", "unit", "year", "value", "flag", "url", "retrieved", "dataset_updated"])
        w.writerows(sorted(rows, key=lambda x: (x[0], x[1], x[2], x[3], x[4])))
    print(len(rows), "rows")


main()
