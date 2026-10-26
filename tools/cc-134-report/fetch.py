"""Download Eurostat inputs for CC-134 to data/cc-134/ (all 27 Member States + EU-27 aggregate).
env_ac_tax: environmental tax revenue by category; nama_10_gdp: GDP at current prices (B1GQ, CP_MEUR).
Writes long CSVs: dataset, geo, tax/na_item, unit, year, value, flag, source URL, retrieved."""
import csv, datetime, json, pathlib, urllib.request

OUT = pathlib.Path(__file__).resolve().parents[2] / "data" / "cc-134"
B = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
TODAY = datetime.date.today().isoformat()
MS = "BE BG CZ DK DE EE IE EL ES FR HR IT CY LV LT LU HU MT NL AT PL PT RO SI SK FI SE".split()
GEOS = MS + ["EU27_2020"]


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


def main():
    geo = "&".join("geo=" + g for g in GEOS)
    rows = []
    url, upd, r = get("env_ac_tax", geo + "&unit=PC_GDP&unit=MIO_EUR&unit=PC_TSCO_X_ISCO&sinceTimePeriod=2015")
    for c, v, f in r:
        rows.append(["env_ac_tax", c["geo"], c["tax"], c["unit"], c["time"], v, f, url, TODAY, upd])
    url, upd, r = get("nama_10_gdp", geo + "&na_item=B1GQ&unit=CP_MEUR&sinceTimePeriod=2015")
    for c, v, f in r:
        rows.append(["nama_10_gdp", c["geo"], c["na_item"], c["unit"], c["time"], v, f, url, TODAY, upd])
    with open(OUT / "eurostat_envtax_gdp.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh); w.writerow(["dataset", "geo", "item", "unit", "year", "value", "flag", "url", "retrieved", "dataset_updated"])
        w.writerows(sorted(rows, key=lambda x: (x[0], x[1], x[2], x[3], x[4])))
    print(len(rows), "rows")


main()
