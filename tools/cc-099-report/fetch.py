#!/usr/bin/env python3
"""CC-099: download the data behind the check into data/cc-099/ (CSV, with Eurostat's flags kept).

Eurostat (dissemination API, JSON-stat), Malta only:
- migr_pop1ctz  population on 1 January by citizenship (Maltese, other EU, non-EU, stateless), all years
- migr_pop3ctb  population on 1 January by country of birth, all years
- demo_gind     population on 1 January 2026 and the 2025 balance (births, deaths, net migration)
- proj_25np     EUROPOP2025 projections of the total population, 2025-2036, every projection type
- cens_21ctz_r3 and cens_21cob_r3  Census 2021 by citizenship and by country of birth
- migr_imm1ctz, migr_emi1ctz, migr_acq  immigration, emigration and acquisitions of citizenship, by citizenship
- demo_faczc, demo_maczc  live births by the mother's citizenship and deaths by citizenship
Jobsplus (public employment service), Malta and Gozo, December of each year:
- employed foreign nationals by group (EU, EEA/EFTA, EU dependants, third-country nationals), full- and part-time
- total employment (full- and part-time) and full-time gainfully occupied

The `flag` column holds Eurostat's observation status (e estimated, b break in series, p provisional ...; empty = none).
"""
import csv, datetime, io, json, pathlib, urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-099"
D.mkdir(exist_ok=True)
API = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/{}?format=JSON&lang=en&geo=MT{}"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0 Safari/537.36"}
TODAY = datetime.date.today().isoformat()


def flat(ds, query=""):
    d = json.load(urllib.request.urlopen(API.format(ds, query), timeout=120))
    dims, sz = d["id"], d["size"]
    cats = [[c for c, _ in sorted(d["dimension"][k]["category"]["index"].items(), key=lambda kv: kv[1])] for k in dims]
    status = d.get("status", {})
    rows = []
    for key, v in d["value"].items():
        n = int(key); pos = []
        for s in reversed(sz):
            pos.append(n % s); n //= s
        pos.reverse()
        r = {k: cats[i][p] for i, (k, p) in enumerate(zip(dims, pos))}
        rows.append(r | {"value": v, "flag": status.get(key, ""), "dataset": ds, "label": d.get("label"),
                         "updated": d.get("updated"), "retrieved": TODAY})
    rows.sort(key=lambda r: tuple(str(r[k]) for k in dims))
    return rows, d.get("extension", {}).get("status", {}).get("label", {})


def write(name, rows):
    fields = list(dict.fromkeys(k for r in rows for k in r))
    with open(D / name, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
    print(f"{name}: {len(rows)} rows")


CTZ = "&citizen=" + "&citizen=".join(["TOTAL", "NAT", "FOR_STLS", "STLS", "EU27_2020_FOR", "NEU27_2020_FOR", "UNK"])
CTB = "&c_birth=" + "&c_birth=".join(["TOTAL", "NAT", "FOR", "EU27_2020_FOR", "NEU27_2020_FOR", "UNK"])
JOBS = [
    ("eurostat_migr_pop1ctz.csv", [("migr_pop1ctz", "&age=TOTAL&sex=T&unit=NR" + CTZ)]),
    ("eurostat_migr_pop3ctb.csv", [("migr_pop3ctb", "&age=TOTAL&sex=T&unit=NR" + CTB)]),
    ("eurostat_demo_gind.csv", [("demo_gind", "&sinceTimePeriod=2010" + "".join(
        f"&indic_de={i}" for i in ("JAN", "GROW", "NATGROW", "CNMIGRAT", "LBIRTH", "DEATH")))]),
    ("eurostat_proj_25np.csv", [("proj_25np", "&age=TOTAL&sex=T&sinceTimePeriod=2025&untilTimePeriod=2036")]),
    ("eurostat_census2021.csv", [("cens_21ctz_r3", "&age=TOTAL&sex=T" + CTZ),
                                 ("cens_21cob_r3", "&age=TOTAL&sex=T" + CTB)]),
    ("eurostat_migr_flows.csv", [(ds, "&age=TOTAL&sex=T&agedef=COMPLET&sinceTimePeriod=2010" + CTZ)
                                 for ds in ("migr_imm1ctz", "migr_emi1ctz", "migr_acq")]),
    ("eurostat_births_deaths_ctz.csv", [("demo_faczc", "&age=TOTAL&sinceTimePeriod=2010&citizen=TOTAL&citizen=NAT"),
                                        ("demo_maczc", "&age=TOTAL&sex=T&sinceTimePeriod=2010&citizen=TOTAL&citizen=NAT")]),
]
for out, parts in JOBS:
    rows = []
    for ds, q in parts:
        r, labels = flat(ds, q)
        print(f"  {ds}: updated {r[0]['updated']}, flag labels {labels or 'none'}")
        rows += r
    write(out, rows)

# ------------------------------------------------------------------ Jobsplus workbooks
JP = "https://jobsplus.gov.mt"
FOREIGN = JP + "/media/h4vb5bur/trend-of-employed-foreign-nationals-2015-2025.xlsx"
TOTAL = JP + "/media/4svdnudg/total-employment-by-economic-sector-2015-25.xlsx?fileId=52342"
FULLTIME = JP + "/media/1h2duaou/ftempdatabylaboursupply-2015-2025-dec.xlsx"


def sheet(url):
    """jobsplus.gov.mt returns 403 to Python's urllib but serves the files to curl with a browser User-Agent."""
    import openpyxl, subprocess  # only needed for this part
    raw = subprocess.run(["curl", "-sS", "-L", "--fail", "-A", UA["User-Agent"], url], check=True,
                         capture_output=True, timeout=180).stdout
    ws = openpyxl.load_workbook(io.BytesIO(raw), data_only=True).worksheets[0]
    grid = [list(row) for row in ws.iter_rows(values_only=True)]
    while grid and all(not r or r[0] is None for r in grid):   # the workbooks start with an empty column
        grid = [r[1:] for r in grid]
    return grid


rows = []
grid = sheet(FOREIGN)
years = next(r for r in grid if r and r[0] and str(r[0]).startswith("Foreign Nationals"))
years = [(i, c.year) for i, c in enumerate(years) if hasattr(c, "year")]
group = None
for r in grid:
    name = (str(r[0]).strip() if r and r[0] is not None else "")
    if name in ("EU National", "EEA & EFTA", "EU Dependent", "Third Country National", "Grand Total"):
        group, kind = name, "Total"
    elif name in ("Full-time", "Part-Time") and group:
        kind = name
    else:
        continue
    for i, y in years:
        rows.append({"group": group, "type": kind, "year_end_dec": y, "value": r[i], "source":
                     "Jobsplus, Trend of employed foreign nationals 2015-2025 (xlsx)", "url": FOREIGN,
                     "retrieved": TODAY})
write("jobsplus_foreign_employment.csv", rows)

rows = []
grid = sheet(TOTAL)
hdr = next(r for r in grid if r and len(r) > 1 and r[1] == "NACE Group / Year")
tot = next(r for r in grid if r and any(str(c).startswith("Total Employed") for c in r if c))
for i, y in enumerate(hdr):
    if isinstance(y, int):
        rows.append({"series": "Total employed (full- and part-time)", "year_end_dec": y, "value": tot[i],
                     "source": "Jobsplus, Total employment by economic sector 2015-2025 (xlsx)", "url": TOTAL,
                     "retrieved": TODAY})
grid = sheet(FULLTIME)
hdr = next(r for r in grid if r and str(r[0]).startswith("Labour Supply (FullTime"))
ft = next(r for r in grid if r and str(r[0]).startswith("Gainfully Employed"))
for i, y in enumerate(hdr):
    if isinstance(y, int):
        rows.append({"series": "Gainfully employed (full-time)", "year_end_dec": y, "value": ft[i],
                     "source": "Jobsplus, Full-time employment data by labour supply 2015-2025 (xlsx)", "url": FULLTIME,
                     "retrieved": TODAY})
write("jobsplus_total_employment.csv", rows)
