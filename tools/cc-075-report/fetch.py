#!/usr/bin/env python3
"""CC-075: download Eurostat data into data/cc-075/ (JSON-stat -> CSV), keeping Eurostat's flags.

- road_eqs_carhab   passenger cars per thousand inhabitants, every country and year (the claim's dataset)
- road_eqs_carmot   stock of passenger cars (all motor energies, all engine sizes), every country and year
- demo_gind         population on 1 January, every country and year (the denominator, tested in calc.py)
- reg_area3         land area (km2), national level (for the article's car-density sentence)

The `flag` column holds Eurostat's observation status as the API labels it (extension.status): b break in time
series, i imputed by Eurostat or other receiving agencies, p provisional, e estimated, d definition differs,
m missing value (data cannot exist); combinations such as 'ip' or 'be' carry both meanings.
"""
import csv, json, pathlib, urllib.request, datetime
ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-075"
API = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/{}?format=JSON&lang=en{}"
D.mkdir(exist_ok=True)


def flat(ds, query=""):
    d = json.load(urllib.request.urlopen(API.format(ds, query), timeout=120))
    dims, sz = d["id"], d["size"]
    # category positions come from the index values, not from the order of the keys
    cats = [[c for c, _ in sorted(d["dimension"][k]["category"]["index"].items(), key=lambda kv: kv[1])]
            for k in dims]
    status = d.get("status", {})
    rows = []
    for key, v in d["value"].items():
        n = int(key); pos = []
        for s in reversed(sz):
            pos.append(n % s); n //= s
        pos.reverse()
        rows.append({k: cats[i][p] for i, (k, p) in enumerate(zip(dims, pos))}
                    | {"value": v, "flag": status.get(key, "")})
    return rows, d.get("updated"), d.get("label"), d.get("extension", {}).get("status", {}).get("label", {})


LOG = []
JOBS = (
    ("road_eqs_carhab", "", "eurostat_road_eqs_carhab.csv", lambda r: True),
    ("road_eqs_carmot", "&mot_nrg=TOTAL&engine=TOTAL&unit=NR", "eurostat_road_eqs_carmot.csv", lambda r: True),
    ("demo_gind", "&indic_de=JAN", "eurostat_demo_gind_jan.csv", lambda r: (len(r["geo"]) == 2 or r["geo"] == "EU27_2020") and r["time"] >= "1990"),
    ("reg_area3", "&landuse=L0008&unit=KM2", "eurostat_reg_area3_land.csv",
     lambda r: len(r["geo"]) == 2 or r["geo"] in ("MT001", "MT002")),
)
for ds, query, out, keep in JOBS:
    rows, upd, label, labels = flat(ds, query)
    rows = sorted((r for r in rows if keep(r)), key=lambda r: (r["geo"], r["time"]))
    today = datetime.date.today().isoformat()
    for r in rows:
        r["dataset"], r["updated"], r["retrieved"] = ds, upd, today
    with open(D / out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    LOG.append(f"| `{out}` | {ds}: {label} | {API.format(ds, query)} | {upd} | {today} | {len(rows)} |")
    print(ds, len(rows), "rows, updated", upd, "|", label, "| flags:", labels)

(D / "README.md").write_text(
    "# CC-075 data\n\nWritten by `tools/cc-075-report/fetch.py` (Eurostat dissemination API, JSON-stat flattened to CSV).\n"
    "The `flag` column keeps Eurostat's observation status: b break in time series, i imputed by Eurostat or other "
    "receiving agencies, p provisional, e estimated, d definition differs, m missing (data cannot exist); combinations "
    "carry both meanings. `checks.csv` is written by `calc.py`.\n\n"
    "| File | Dataset | API URL | Updated (Eurostat) | Retrieved | Rows |\n|---|---|---|---|---|---|\n"
    + "\n".join(LOG) + "\n\n"
    "## Earlier vintages (what Eurostat had published before 21 Sep 2024)\n\n"
    "Eurostat's API serves only current data. `fetch_vintage.py` saves Eurostat's own earlier publications: the "
    "Statistics Explained article 'Passenger cars in the EU' through its MediaWiki API (revision list; revisions 627098 "
    "of 31 Jan 2024 and 647912 of 19 Aug 2024, the latter live until 5 Nov 2024), the two 'Motorisation rate' Figure 3 "
    "images those revisions show, and the infographic of Eurostat's news release of 17 Jan 2024. Each file's URL, sha1 "
    "and retrieval date are in `vintage_sources.csv`. `read_charts.py` reads the three bar charts by pixel measurement "
    "(calibrated on the gridlines, checked against the values Eurostat prints) into `chart_reads.csv`. "
    "`reported_values.csv` holds figures stated in texts and tables we read (second-hand rows marked). Eurostat content "
    "is reused under Eurostat's copyright notice (https://ec.europa.eu/eurostat/help/copyright-notice: re-use authorised, source acknowledged; read via search summary 6 Oct 2026).\n")
