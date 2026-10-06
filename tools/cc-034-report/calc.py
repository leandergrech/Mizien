"""Claim Check 034: test ERA's statement that measures named in the Air Quality Plan for Malta (2025) have
"already contributed to improvements in air quality" against measured data.

Reads data/cc-034/ (written by fetch.py on 6 Oct 2026); writes data/cc-034/checks.csv. Every number in the report,
flyer and claim record comes from checks.csv.

Stations (EEA codes): MT00005 Msida, traffic (to end 2023); MT00011 Msida, new traffic point ~300 m away (from
17 Jan 2024); MT00004 Żejtun, urban background; MT00008 Attard, urban background; MT00007 Għarb (Gozo), rural
background; MT00003 Kordin, industrial (closed end 2016); MT00009 St Paul's Bay, traffic (from 2022).
"""
import csv
import datetime as dt
import pathlib
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-034"
EEA = "EEA Air Quality download service (E1a validated; AirBase before 2013), retrieved 6 Oct 2026"
G = "ERA attainment reports to the EEA (dataflow G, Eionet CDR), retrieved 6 Oct 2026"
EMIS = "Eurostat env_air_emis (Malta, tonnes), updated 7 Sep 2026, retrieved 6 Oct 2026"
CARS = "Eurostat road_eqs_carpda / road_eqs_carhab, retrieved 6 Oct 2026"
rows = []


def add(cid, check, value, unit, source, note=""):
    rows.append({"id": cid, "check": check, "value": value, "unit": unit, "source": source, "note": note})


def r1(x):
    return round(x + 1e-9, 1)


# ------------------------------------------------------------------ loaders
annual = {}
for r in csv.DictReader(open(D / "annual.csv", encoding="utf-8")):
    annual[(r["station"], r["pollutant"], int(r["year"]))] = r


def am(st, pol, y):
    r = annual.get((st, pol, y))
    return float(r["mean"]) if r else None


def cov(st, pol, y):
    r = annual.get((st, pol, y))
    return float(r["coverage_pct"]) if r else 0.0


def mean_years(st, pol, years):
    vals = [am(st, pol, y) for y in years]
    assert all(v is not None for v in vals), (st, pol, years)
    return sum(vals) / len(vals)


def daily(name):
    out = defaultdict(dict)
    for r in csv.DictReader(open(D / name, encoding="utf-8")):
        d = dt.date.fromisoformat(r["date"])
        for k, v in r.items():
            if k != "date" and v != "":
                out[k][d] = float(v)
    return out


pm10, pm25, no2 = daily("pm10_daily.csv"), daily("pm25_daily.csv"), daily("no2_daily.csv")
gatt = list(csv.DictReader(open(D / "g_attainment.csv", encoding="utf-8")))
emis = {}
for r in csv.DictReader(open(D / "eurostat_emissions.csv", encoding="utf-8")):
    emis[(r["airpol"], r["src_nfr"], int(r["time"]))] = float(r["value"])
cars = {}
for r in csv.DictReader(open(D / "eurostat_cars.csv", encoding="utf-8")):
    if r["dataset"] == "road_eqs_carpda" and r.get("leg_form") == "TOTAL":
        cars[("stock", int(r["time"]))] = float(r["value"])
    if r["dataset"] == "road_eqs_carhab":
        cars[("per1000", int(r["time"]))] = float(r["value"])
diurnal = defaultdict(lambda: [0.0, 0])
for r in csv.DictReader(open(D / "diurnal.csv", encoding="utf-8")):
    k = (r["station"], r["pollutant"], int(r["year"]), r["season"], r["daytype"], int(r["hour"]))
    diurnal[k] = [float(r["mean"]) * int(r["n_hours"]), int(r["n_hours"])]


def dmean(st, pol, years, season, daytypes, hours):
    s = n = 0
    for y in years:
        for dtp in daytypes:
            for h in hours:
                a, b = diurnal.get((st, pol, y, season, dtp, h), (0.0, 0))
                s += a
                n += b
    return s / n if n else None


def g(year, pol, metric, zone="ZON-MT0001"):
    for r in gatt:
        if (int(r["year"]) == year and r["pollutant"] == pol and r["reportingMetric"] == metric
                and r["objectiveType"] == "LV" and r["protectionTarget"] == "H" and r["zone"] == zone):
            return r
    return None


# ------------------------------------------------------------------ A. the plan's own reason: Msida PM10
for y in (2018, 2023):
    r = g(y, "PM10", "daysAbove")
    add(f"A-{y}-final", f"Msida PM10 days above 50 µg/m³, {y}, after deduction of natural sources (ERA)",
        int(r["final_count"]), "days", G, f"limit: 35 days; exceedance flag '{r['final_exceedance']}'")
    add(f"A-{y}-base", f"Msida PM10 days above 50 µg/m³, {y}, before deduction (ERA)", int(r["base_count"]), "days",
        G, f"stations used: {r['stations_used']}")
    raw = sum(1 for d, v in pm10["MT00005"].items() if d.year == y and v > 50)
    add(f"A-{y}-eea", f"Msida PM10 days above 50 µg/m³, {y}, counted from EEA daily values", raw, "days", EEA,
        "our count; differs from ERA's by %+d" % (raw - int(r["base_count"])))
series = []
for y in range(2015, 2026):
    r = g(y, "PM10", "daysAbove")
    if r and r["final_count"]:
        series.append((y, int(r["final_count"]), r["stations_used"].split(" ")[0] if r["stations_used"] else ""))
add("A-series", "Agglomeration PM10 days above 50 after natural deduction, 2015-2025 (ERA)",
    "; ".join(f"{y}: {n}" for y, n, _ in series), "days", G,
    "2015-2023 from the old Msida point (MT00005); 2024-2025 from the new point (MT00011) and others")
diffs = []
for y in range(2015, 2026):
    r = g(y, "PM10", "daysAbove")
    if r and r["base_count"]:
        st = "MT00005" if y <= 2023 else "MT00011"
        ours = sum(1 for d, v in pm10[st].items() if d.year == y and v > 50)
        diffs.append(f"{y}: {ours} vs {r['base_count']}")
add("A-eea-vs-era", "Msida PM10 days above 50 before deduction: our EEA count vs ERA's reported count",
    "; ".join(diffs), "days", f"{EEA}; {G}", "2024-2025: new Msida point (MT00011)")
mx = max(series, key=lambda t: t[1])
add("A-max", "Year with most PM10 days after deduction, 2015-2025", f"{mx[0]} ({mx[1]} days)", "", G)
for y in (2018, 2023):
    r = g(y, "PM10", "aMean")
    add(f"A-{y}-amean", f"Msida PM10 annual mean {y}, before / after natural deduction (ERA)",
        f"{r['base_value']} / {r['final_value']}", "µg/m³", G, "annual limit 40 µg/m³")
add("A-2023-amean-eea", "Msida PM10 annual mean 2023 from EEA daily values", r1(am("MT00005", "PM10", 2023)), "µg/m³",
    EEA)

# ------------------------------------------------------------------ B. trends at the traffic site vs background
B1, B2 = (2015, 2016, 2017), (2021, 2022, 2023)
for pol, bgs in (("PM10", ("MT00007", "MT00004")), ("PM2.5", ("MT00007", "MT00004")),
                 ("NO2", ("MT00008", "MT00004", "MT00007"))):
    a, b = mean_years("MT00005", pol, B1), mean_years("MT00005", pol, B2)
    lowcov = [y for y in B1 + B2 if cov("MT00005", pol, y) < 85]
    add(f"B-{pol}-msida", f"Msida {pol}, mean of annual means 2015-17 → 2021-23", f"{r1(a)} → {r1(b)}", "µg/m³", EEA,
        f"change {b - a:+.1f} ({100 * (b - a) / a:+.0f}%)" + (f"; years below 85% coverage: {lowcov}" if lowcov else ""))
    for bg in bgs:
        c, d = mean_years(bg, pol, B1), mean_years(bg, pol, B2)
        add(f"B-{pol}-{bg}", f"{pol} at {bg}, 2015-17 → 2021-23", f"{r1(c)} → {r1(d)}", "µg/m³", EEA,
            f"change {d - c:+.1f}; Msida increment over it {a - c:.1f} → {b - d:.1f}")
# PM10 increment over the rural background, by year (the plan: natural sources affect every station alike)
inc = {y: am("MT00005", "PM10", y) - am("MT00007", "PM10", y) for y in range(2013, 2024)}
add("B-PM10-inc-series", "Msida minus Għarb PM10 annual mean, 2013-2023", "; ".join(f"{y}: {r1(v)}" for y, v in inc.items()),
    "µg/m³", EEA, "urban increment over the rural background")
ym = max(inc, key=inc.get)
add("B-PM10-inc-max", "Year with the largest Msida increment over Għarb (PM10)", f"{ym} ({r1(inc[ym])})", "µg/m³", EEA)
for y in (2018, 2023):
    add(f"B-gharb-days-{y}", f"Għarb PM10 days above 50, {y} (regional and natural episodes)",
        sum(1 for d, v in pm10["MT00007"].items() if d.year == y and v > 50), "days", EEA)
gh = {y: sum(1 for d, v in pm10["MT00007"].items() if d.year == y and v > 50) for y in range(2013, 2024)}
add("B-gharb-days-series", "Għarb PM10 days above 50, 2013-2023", "; ".join(f"{y}: {v}" for y, v in gh.items()), "days",
    EEA)
add("B-msida-days-1517-2123", "Msida PM10 days above 50 (EEA count), mean 2015-17 → 2021-23",
    f"{r1(sum(sum(1 for d, v in pm10['MT00005'].items() if d.year == y and v > 50) for y in B1) / 3)} → "
    f"{r1(sum(sum(1 for d, v in pm10['MT00005'].items() if d.year == y and v > 50) for y in B2) / 3)}", "days", EEA)
gfin = {y: n for y, n, _ in series}
add("B-msida-days-final-1517-2123", "Msida PM10 days above 50 after natural deduction (ERA), mean 2015-17 → 2021-23",
    f"{r1(sum(gfin[y] for y in B1) / 3)} → {r1(sum(gfin[y] for y in B2) / 3)}", "days", G)

# ------------------------------------------------------------------ C. power-sector reform
for p, lab in (("NOX", "NOx"), ("SOX", "SOx"), ("PM2_5", "PM2.5")):
    a, b, c = emis[(p, "NFR1A1A", 2008)], emis[(p, "NFR1A1A", 2018)], emis[(p, "NFR1A1A", 2024)]
    add(f"C-emis-{lab}", f"{lab} from public electricity and heat production, 2008 → 2018 → 2024", f"{a:,.0f} → {b:,.0f} → "
        f"{c:,.0f}", "t", EMIS, f"2008→2018 {100 * (b - a) / a:+.1f}%")
    sh = 100 * a / emis[(p, "NFR_TOT_NAT", 2008)]
    add(f"C-share-{lab}", f"Power sector share of Malta's {lab} emissions, 2008", r1(sh), "%", EMIS)
add("C-so2-kordin", "SO2 at Kordin (downwind of Marsa power station), 2012 → 2015", f"{r1(am('MT00003', 'SO2', 2012))} → "
    f"{r1(am('MT00003', 'SO2', 2015))}", "µg/m³", EEA, f"coverage 2012 {cov('MT00003', 'SO2', 2012):.0f}%, 2015 "
    f"{cov('MT00003', 'SO2', 2015):.0f}%")
for st in ("MT00004", "MT00005", "MT00007"):
    a = mean_years(st, "SO2", (2010, 2011, 2012))
    b = mean_years(st, "SO2", (2018, 2019, 2020, 2021, 2022, 2023))
    add(f"C-so2-{st}", f"SO2 at {st}, mean 2010-12 → 2018-23", f"{r1(a)} → {r1(b)}", "µg/m³", EEA,
        f"{100 * (b - a) / a:+.0f}%")
for pol in ("NO2", "PM2.5", "PM10"):
    a = mean_years("MT00004", pol, (2013, 2014, 2015, 2016))
    b = mean_years("MT00004", pol, (2018, 2019, 2021, 2022, 2023))
    add(f"C-zejtun-{pol}", f"Żejtun {pol}, mean 2013-16 → 2018-23 (excl. 2020)", f"{r1(a)} → {r1(b)}", "µg/m³", EEA,
        f"change {b - a:+.1f}; Żejtun lies about 3 km from Delimara (station coordinates in data/cc-008/aq_stations.csv)")

# ------------------------------------------------------------------ D. vehicles and road-transport emissions
road = lambda p, y: sum(emis[(p, s, y)] for s in ("NFR1A3B1", "NFR1A3B2", "NFR1A3B3", "NFR1A3B4"))
a, b = road("NOX", 2015), road("NOX", 2022)
add("D-road-nox", "Road-transport exhaust NOx (cars, vans, lorries and buses, motorcycles), 2015 → 2022",
    f"{a:,.0f} → {b:,.0f}", "t", EMIS, f"{100 * (b - a) / a:+.0f}% (modelled inventory, not measured)")
a, b = mean_years("MT00005", "NO2", B1), mean_years("MT00005", "NO2", B2)
add("D-msida-no2-pct", "Msida NO2, 2015-17 → 2021-23", f"{100 * (b - a) / a:+.0f}", "%", EEA)
ex = lambda y: road("PM10", y)
ne = lambda y: emis[("PM10", "NFR1A3B6", y)] + emis[("PM10", "NFR1A3B7", y)]
add("D-pm10-exh-nonexh", "Road-transport PM10: exhaust vs tyre, brake and road wear, 2015 → 2023",
    f"exhaust {ex(2015):.0f} → {ex(2023):.0f}; wear {ne(2015):.0f} → {ne(2023):.0f}", "t", EMIS)
add("D-construction-pm10", "PM10 from construction and demolition (NFR 2A5b), 2013 → 2023 → 2024",
    f"{emis[('PM10', 'NFR2A5B', 2013)]:.0f} → {emis[('PM10', 'NFR2A5B', 2023)]:.0f} → {emis[('PM10', 'NFR2A5B', 2024)]:.0f}",
    "t", EMIS)
add("D-cars", "Passenger cars licensed, 2013 → 2025", f"{cars[('stock', 2013)]:,.0f} → {cars[('stock', 2025)]:,.0f}",
    "cars", CARS, f"{100 * (cars[('stock', 2025)] - cars[('stock', 2013)]) / cars[('stock', 2013)]:+.0f}%")
add("D-cars-1000", "Passenger cars per 1,000 inhabitants, 2013 → 2025",
    f"{cars[('per1000', 2013)]:.0f} → {cars[('per1000', 2025)]:.0f}", "cars", CARS)

# ------------------------------------------------------------------ E. free school transport (from Sept 2018)
P1, P2 = range(2014, 2018), (2018, 2019)
for pol, unit in (("NO2", "µg/m³"), ("CO", "mg/m³")):
    prof = {per: [dmean("MT00005", pol, yrs, "Oct-Dec", ("weekday", "weekend"), [h]) for h in range(24)]
            for per, yrs in (("a", P1), ("b", P2))}
    mxa, mxb = max(prof["a"]), max(prof["b"])
    add(f"E-{pol}-maxhour", f"Msida {pol}, Oct-Dec, highest hourly mean of the day: 2014-17 → 2018-19",
        f"{mxa:.2f} (hour {prof['a'].index(mxa):02d}) → {mxb:.2f} (hour {prof['b'].index(mxb):02d})", unit, EEA,
        "the plan's Figures 25-26 comparison, recomputed; hours as reported to the EEA")
    d07 = prof["b"][7] - prof["a"][7]
    add(f"E-{pol}-07", f"Msida {pol}, Oct-Dec, 07:00-08:00: 2014-17 → 2018-19", f"{prof['a'][7]:.2f} → {prof['b'][7]:.2f}",
        unit, EEA, f"change {d07:+.2f}")
    morning = [prof["b"][h] - prof["a"][h] for h in range(6, 12)]
    evening = [prof["b"][h] - prof["a"][h] for h in range(16, 23)]
    add(f"E-{pol}-range", f"Msida {pol}, Oct-Dec, change by hour 2014-17 → 2018-19: morning 06-11 / evening 16-22",
        f"{min(morning):+.2f} to {max(morning):+.2f} / {min(evening):+.2f} to {max(evening):+.2f}", unit, EEA)
# difference in differences: school term (Oct-Dec) minus holidays (Jun-Aug), weekday 07:00-09:59
MORN = range(7, 10)
for st in ("MT00005", "MT00008", "MT00004"):
    w = dmean(st, "NO2", P2, "Oct-Dec", ("weekday",), MORN) - dmean(st, "NO2", P1, "Oct-Dec", ("weekday",), MORN)
    s = dmean(st, "NO2", P2, "Jun-Aug", ("weekday",), MORN) - dmean(st, "NO2", P1, "Jun-Aug", ("weekday",), MORN)
    add(f"E-did-{st}", f"NO2 weekday 07-10 at {st}: change in term (Oct-Dec) minus change in holidays (Jun-Aug), "
        "2014-17 → 2018-19", f"{w - s:+.1f}", "µg/m³", EEA, f"term {w:+.1f}, holidays {s:+.1f}")
yearly = {y: dmean("MT00005", "NO2", [y], "Oct-Dec", ("weekday",), MORN) for y in range(2013, 2024)}
add("E-no2-yearly", "Msida NO2, Oct-Dec weekday 07:00-09:59, by year",
    "; ".join(f"{y}: {v:.1f}" for y, v in yearly.items()), "µg/m³", EEA)
rank = sorted(yearly, key=yearly.get, reverse=True)
add("E-no2-2018-rank", "Rank of Oct-Dec 2018 (first term of free school transport) among 2013-2023, highest = 1",
    rank.index(2018) + 1, "rank", EEA, f"2017: {yearly[2017]:.1f}; 2018: {yearly[2018]:.1f}; 2019: {yearly[2019]:.1f}")
coy = {y: dmean("MT00005", "CO", [y], "Oct-Dec", ("weekday",), MORN) for y in range(2013, 2024)}
add("E-co-yearly", "Msida CO, Oct-Dec weekday 07:00-09:59, by year", "; ".join(
    f"{y}: {v:.2f}" for y, v in coy.items() if v is not None), "mg/m³", EEA)
inc_m = {}
for r in csv.DictReader(open(D / "monthly.csv", encoding="utf-8")):
    if r["pollutant"] == "NO2" and r["station"] in ("MT00005", "MT00008"):
        inc_m[(r["station"], r["month"])] = float(r["mean"])
oct_dec = lambda y: sum(inc_m[("MT00005", f"{y}-{m}")] - inc_m[("MT00008", f"{y}-{m}")] for m in ("10", "11", "12")) / 3
add("E-no2-inc-octdec", "Msida minus Attard NO2, Oct-Dec 2017 → Oct-Dec 2018 (monthly means)",
    f"{oct_dec(2017):.1f} → {oct_dec(2018):.1f}", "µg/m³", EEA)

# ------------------------------------------------------------------ F. free public transport (from 1 Oct 2022)
W0 = (dt.date(2021, 10, 1), dt.date(2022, 9, 30))
W1 = (dt.date(2022, 10, 1), dt.date(2023, 9, 30))


def wmean(series, w):
    v = [x for d, x in series.items() if w[0] <= d <= w[1]]
    return (sum(v) / len(v) if v else float("nan")), len(v)


improved = total = 0
for pol, s in (("PM10", pm10), ("PM2.5", pm25), ("NO2", no2)):
    for st in ("MT00005", "MT00004", "MT00008", "MT00007", "MT00009"):
        if st not in s:
            continue
        (a, na), (b, nb) = wmean(s[st], W0), wmean(s[st], W1)
        if na < 300 or nb < 300:
            add(f"F-{pol}-{st}", f"{pol} at {st}, Oct 2021-Sep 2022 → Oct 2022-Sep 2023", "n/a", "", EEA,
                f"too few days ({na}, {nb})")
            continue
        total += 1
        improved += b < a
        add(f"F-{pol}-{st}", f"{pol} at {st}, Oct 2021-Sep 2022 → Oct 2022-Sep 2023", f"{a:.1f} → {b:.1f}", "µg/m³", EEA,
            f"change {b - a:+.1f}; days {na}, {nb}")
add("F-improved", "Station-pollutant pairs lower in the 12 months after free public transport began",
    f"{improved} of {total}", "", EEA, "stations with at least 300 valid days in both windows")
for st in ("MT00005", "MT00007"):
    c0 = sum(1 for d, v in pm10[st].items() if W0[0] <= d <= W0[1] and v > 50)
    c1 = sum(1 for d, v in pm10[st].items() if W1[0] <= d <= W1[1] and v > 50)
    add(f"F-days-{st}", f"PM10 days above 50 at {st}, Oct 2021-Sep 2022 → Oct 2022-Sep 2023", f"{c0} → {c1}", "days", EEA)

with open(D / "checks.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["id", "check", "value", "unit", "source", "note"])
    w.writeheader()
    w.writerows(rows)
for r in rows:
    print(f"{r['id']:24s} {r['value']} {r['unit']}  {r['note']}")
