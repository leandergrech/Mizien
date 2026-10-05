#!/usr/bin/env python3
"""CC-004 v1.1: municipal recycling rates for every EU-27 state (Eurostat cei_wm011).

Writes data/cc-004/eurostat_cei_wm011_eu27.csv (one row per country and year, with Eurostat's flag, the
dataset's last-update stamp, the query URL and the retrieval date). The Malta and EU-27 series in
eurostat_municipal_waste.csv (retrieved 2 Oct 2026) are left as they are; calc.py checks that the two agree.
"""
import csv
import datetime as dt
import json
import pathlib
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "cc-004" / "eurostat_cei_wm011_eu27.csv"
URL = ("https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/cei_wm011"
       "?wst_oper=RCY&unit=PC&sinceTimePeriod=2019")
EU27 = ["AT", "BE", "BG", "CY", "CZ", "DE", "DK", "EE", "EL", "ES", "FI", "FR", "HR", "HU", "IE", "IT", "LT",
        "LU", "LV", "MT", "NL", "PL", "PT", "RO", "SE", "SI", "SK", "EU27_2020"]


def jsonstat_rows(j):
    """Flatten a JSON-stat 2.0 response into dicts of dimension codes plus value and flag."""
    ids, sizes = j["id"], j["size"]
    cats = [sorted(j["dimension"][d]["category"]["index"].items(), key=lambda kv: kv[1]) for d in ids]
    status = j.get("status", {})
    for k, v in j["value"].items():
        k = int(k)
        rem, codes = k, []
        for s in reversed(sizes):
            codes.append(rem % s)
            rem //= s
        codes = list(reversed(codes))
        row = {d: cats[i][codes[i]][0] for i, d in enumerate(ids)}
        row["value"] = v
        row["flag"] = status.get(str(k), "")
        yield row


def main():
    with urllib.request.urlopen(URL, timeout=60) as r:
        j = json.load(r)
    today = dt.date.today().isoformat()
    rows = [r for r in jsonstat_rows(j) if r["geo"] in EU27]
    rows.sort(key=lambda r: (r["geo"], r["time"]))
    with open(OUT, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["dataset", "geo", "year", "value", "flag", "eurostat_updated", "query_url", "retrieved"])
        for r in rows:
            w.writerow(["cei_wm011", r["geo"], r["time"], r["value"], r["flag"], j["updated"], URL, today])
    print(f"{len(rows)} rows, dataset updated {j['updated']}, written to {OUT}")


if __name__ == "__main__":
    main()
