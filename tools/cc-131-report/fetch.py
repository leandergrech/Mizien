"""Download Eurostat inputs for CC-131 to data/cc-131/ (all 27 Member States + EU-27 aggregate).
env_wastrt: treatment of waste by category and operation (W121 mineral waste from construction and demolition;
W126 soils), hazardous + non-hazardous and non-hazardous only, tonnes, 2010-2022.
env_wasgen: generation of W121 and W126, all NACE activities plus households, tonnes.
Writes one long CSV: dataset, geo, waste, hazard, oper, unit, year, value, flag, source URL, retrieved, dataset_updated."""
import csv, datetime, json, pathlib, urllib.request

OUT = pathlib.Path(__file__).resolve().parents[2] / "data" / "cc-131"
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
    url, upd, r = get("env_wastrt", geo + "&waste=W121&waste=W126&hazard=HAZ_NHAZ&hazard=NHAZ&unit=T&sinceTimePeriod=2010")
    for c, v, f in r:
        rows.append(["env_wastrt", c["geo"], c["waste"], c["hazard"], c["wst_oper"], c["unit"], c["time"], v, f, url, TODAY, upd])
    url, upd, r = get("env_wasgen", geo + "&waste=W121&waste=W126&hazard=HAZ_NHAZ&hazard=NHAZ&unit=T&nace_r2=TOTAL_HH&sinceTimePeriod=2010")
    for c, v, f in r:
        rows.append(["env_wasgen", c["geo"], c["waste"], c["hazard"], "GEN", c["unit"], c["time"], v, f, url, TODAY, upd])
    with open(OUT / "eurostat_cdw.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["dataset", "geo", "waste", "hazard", "oper", "unit", "year", "value", "flag", "url", "retrieved", "dataset_updated"])
        w.writerows(sorted(rows, key=lambda x: (x[0], x[1], x[2], x[3], x[4], x[6])))
    print(len(rows), "rows")


main()
