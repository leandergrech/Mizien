"""Download the open inputs for CC-135 to data/cc-135/.

- Eurostat demo_gind (population on 1 January, JAN, and average population, AVG), Malta.
- Eurostat tour_occ_nim (nights spent at tourist accommodation establishments, monthly; NACE I551-I553, all residences), Malta.
- Eurostat nrg_cb_e (electricity balance, GWh; siec E7000), Malta: final consumption and supply, used as a control.
- NOAA GHCN-Daily, station MT000016597 (Luqa): daily TAVG/TMAX/TMIN, summarised to monthly means with day counts.

The NSO peak-demand figures cannot be downloaded by script (nso.gov.mt returns 403); they are transcribed in
data/cc-135/nso_max_demand.csv with the release, URL and retrieval date of each row.
Writes long CSVs with source URL, retrieval date and Eurostat status flags."""
import collections, csv, datetime, io, json, pathlib, urllib.request

OUT = pathlib.Path(__file__).resolve().parents[2] / "data" / "cc-135"
OUT.mkdir(exist_ok=True)
B = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
TODAY = datetime.date.today().isoformat()


def eurostat(ds, q):
    url = B + ds + "?" + q + "&format=JSON&lang=EN"
    d = json.load(urllib.request.urlopen(url, timeout=60))
    dims, sizes = d["id"], d["size"]
    inv = {k: {v: c for c, v in d["dimension"][k]["category"]["index"].items()} for k in dims}
    flags = d.get("status", {})
    rows = []
    for idx, val in d["value"].items():
        i = int(idx); c = {}
        for k, n in reversed(list(zip(dims, sizes))):
            c[k] = inv[k][i % n]; i //= n
        rows.append((c, val, flags.get(idx, "")))
    return url, d.get("updated", ""), d.get("label", ""), rows


def main():
    rows = []
    url, upd, lab, r = eurostat("demo_gind", "geo=MT&indic_de=JAN&indic_de=AVG&sinceTimePeriod=2015")
    rows += [["demo_gind", c["indic_de"], c["time"], v, f, url, TODAY, upd] for c, v, f in r]
    url, upd, lab, r = eurostat("tour_occ_nim", "geo=MT&unit=NR&nace_r2=I551-I553&c_resid=TOTAL&sinceTimePeriod=2015-01")
    rows += [["tour_occ_nim", "NIGHTS_I551-I553_TOTAL", c["time"], v, f, url, TODAY, upd] for c, v, f in r]
    url, upd, lab, r = eurostat("nrg_cb_e", "geo=MT&siec=E7000&unit=GWH&sinceTimePeriod=2015")
    rows += [["nrg_cb_e", c["nrg_bal"], c["time"], v, f, url, TODAY, upd] for c, v, f in r
             if c["nrg_bal"] in ("GEP", "IMP", "EXP", "FC", "DL", "NRG_E")]
    with open(OUT / "eurostat_pop_tourism_electricity.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["dataset", "item", "period", "value", "flag", "url", "retrieved", "dataset_updated"])
        w.writerows(sorted(rows, key=lambda x: (x[0], x[1], x[2])))
    print(len(rows), "Eurostat rows")

    gurl = "https://www.ncei.noaa.gov/data/global-historical-climatology-network-daily/access/MT000016597.csv"
    txt = urllib.request.urlopen(gurl, timeout=120).read().decode("utf-8")
    agg = collections.defaultdict(lambda: collections.defaultdict(list))
    for x in csv.DictReader(io.StringIO(txt)):
        if x["DATE"] < "2015":
            continue
        for k in ("TAVG", "TMAX", "TMIN"):
            v = (x.get(k) or "").strip()
            if v:
                agg[x["DATE"][:7]][k].append(int(v) / 10)
    with open(OUT / "ghcnd_luqa_monthly.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["month", "tavg_mean_c", "tavg_days", "tmax_mean_c", "tmax_days", "tmax_highest_c", "tmin_mean_c",
                    "tmin_days", "station", "url", "retrieved"])
        for ym in sorted(agg):
            a = agg[ym]
            m = lambda k: "%.2f" % (sum(a[k]) / len(a[k])) if a[k] else ""
            w.writerow([ym, m("TAVG"), len(a["TAVG"]), m("TMAX"), len(a["TMAX"]), max(a["TMAX"]) if a["TMAX"] else "",
                        m("TMIN"), len(a["TMIN"]), "MT000016597 LUQA", gurl, TODAY])
    print(len(agg), "GHCN months")


main()
