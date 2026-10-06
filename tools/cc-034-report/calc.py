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
import itertools
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
    "2015-2023 from the old Msida point (MT00005); 2024-2025 are zone counts from other stations (see A-2024-25)")
for y in (2024, 2025):
    r = g(y, "PM10", "daysAbove")
    used = " ".join(sorted({u.split("_")[0].replace("SPO-", "") for u in r["stations_used"].split()}))
    add(f"A-{y}-zone", f"Agglomeration PM10 days above 50 in {y}, before / after natural deduction (ERA's zone count)",
        f"{r['base_count']} / {r['final_count']}", "days", G, f"stations used (stationUsed in ERA's file): {used}")
add("A-2024-25", "Agglomeration PM10 days above 50 after natural deduction, 2024 and 2025 (ERA's zone counts)",
    f"{g(2024, 'PM10', 'daysAbove')['final_count']} and {g(2025, 'PM10', 'daysAbove')['final_count']}", "days", G,
    "2024: new Msida point (MT00011) and Attard (MT00008); 2025: Attard, new Msida point and Żejtun (MT00004); "
    "not comparable with 2015-2023 at the old Msida point; both under the 35 allowed")
diffs = []
for y in range(2015, 2026):
    r = g(y, "PM10", "daysAbove")
    if r and r["base_count"]:
        st = "MT00005" if y <= 2023 else "MT00011"
        ours = sum(1 for d, v in pm10[st].items() if d.year == y and v > 50)
        diffs.append(f"{y}: {ours} vs {r['base_count']}")
add("A-eea-vs-era", "Msida PM10 days above 50 before deduction: our EEA count vs ERA's reported count",
    "; ".join(diffs), "days", f"{EEA}; {G}", "2024-2025: new Msida point (MT00011)")
mx = max((t for t in series if t[0] <= 2023), key=lambda t: t[1])
add("A-max", "Year with most PM10 days after deduction, 2015-2023 at the old Msida point", f"{mx[0]} ({mx[1]} days)",
    "", G, "2024-2025 are not comparable (A-2024-25)")
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
# sensitivity: the 2021-23 window excludes only 2020 (lockdowns); 2021 (27.1) is still low, so use 2022-23 alone
n1517, n2223 = mean_years("MT00005", "NO2", B1), mean_years("MT00005", "NO2", (2022, 2023))
add("B-NO2-msida-2223", "Msida NO2, mean of annual means 2015-17 → 2022-23 (sensitivity: leaves out 2021 as well)",
    f"{r1(n1517)} → {r1(n2223)}", "µg/m³", EEA, f"change {n2223 - n1517:+.1f} ({100 * (n2223 - n1517) / n1517:+.0f}%); "
    f"2021 annual mean {r1(am('MT00005', 'NO2', 2021))}, 2020 {r1(am('MT00005', 'NO2', 2020))}")
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
# The reform's own steps are 2015-2017 (interconnector April 2015; Marsa closed 2015; Delimara on gas 2017; plan p. 57).
# Emissions are given from 2008 and from 2014, the last year before the reform: the plan credits an earlier shift to
# low-sulphur fuel separately (section 9.1, p. 41; p. 42 attributes the fall in SO2 emissions to both).
for p, lab in (("NOX", "NOx"), ("SOX", "SOx"), ("PM2_5", "PM2.5")):
    e = lambda y: emis[(p, "NFR1A1A", y)]
    a, m, b, c = e(2008), e(2014), e(2018), e(2024)
    add(f"C-emis-{lab}", f"{lab} from public electricity and heat production, 2008 → 2014 → 2018 → 2024",
        f"{a:,.0f} → {m:,.0f} → {b:,.0f} → {c:,.0f}", "t", EMIS,
        f"2008→2018 {100 * (b - a) / a:+.1f}%; 2014→2018 {100 * (b - m) / m:+.1f}%; share of the 2008→2018 fall that "
        f"came before 2015: {100 * (a - m) / (a - b):.0f}%")
    sh = 100 * a / emis[(p, "NFR_TOT_NAT", 2008)]
    add(f"C-share-{lab}", f"Power sector share of Malta's {lab} emissions, 2008", r1(sh), "%", EMIS)
kord = "; ".join(f"{y}: {r1(am('MT00003', 'SO2', y))} ({cov('MT00003', 'SO2', y):.0f}%)" for y in range(2009, 2017)
                 if ("MT00003", "SO2", y) in annual)
add("C-so2-kordin-series", "SO2 at Kordin (downwind of Marsa power station), annual mean (share of year measured), "
    "2009-2016", kord, "µg/m³", EEA, "2010-13 rest on 10-62% of the year; the monitor closed at the end of 2016")
add("C-so2-kordin", "SO2 at Kordin, 2014 → 2015 → 2016 (around the interconnector of April 2015)",
    f"{r1(am('MT00003', 'SO2', 2014))} → {r1(am('MT00003', 'SO2', 2015))} → {r1(am('MT00003', 'SO2', 2016))}", "µg/m³",
    EEA, f"coverage {cov('MT00003', 'SO2', 2014):.0f}%, {cov('MT00003', 'SO2', 2015):.0f}%, "
    f"{cov('MT00003', 'SO2', 2016):.0f}%; already low in 2014, before the reform")
for st in ("MT00004", "MT00005", "MT00007"):
    base = [y for y in range(2008, 2013) if cov(st, "SO2", y) >= 60]   # leave out years with under 60% of the year
    a = mean_years(st, "SO2", base)
    b = mean_years(st, "SO2", (2018, 2019, 2020, 2021, 2022, 2023))
    left = ", ".join(f"{y} ({cov(st, 'SO2', y):.1f}%)" for y in range(2008, 2013) if y not in base) or "none"
    add(f"C-so2-{st}", f"SO2 at {st}, mean of {', '.join(map(str, base))} → 2018-23", f"{r1(a)} → {r1(b)}", "µg/m³", EEA,
        f"{100 * (b - a) / a:+.0f}%; baseline years with at least 60% of the year measured (left out: {left})")
a2 = mean_years("MT00004", "SO2", (2010, 2011, 2012))
add("C-so2-MT00004-v1", "SO2 at Żejtun, mean 2010-12 → 2018-23 (first draft's baseline, kept for comparison)",
    f"{r1(a2)} → {r1(mean_years('MT00004', 'SO2', (2018, 2019, 2020, 2021, 2022, 2023)))}", "µg/m³", EEA,
    f"2011 rests on {cov('MT00004', 'SO2', 2011):.1f}% of the year; not used in the report")
a3, b3 = mean_years("MT00004", "SO2", (2013, 2014, 2015, 2016)), mean_years("MT00004", "SO2", (2018, 2019, 2020, 2021, 2022, 2023))
add("C-so2-MT00004-1316", "SO2 at Żejtun, mean 2013-16 → 2018-23 (the years just before and after the reform)",
    f"{r1(a3)} → {r1(b3)}", "µg/m³", EEA, f"{100 * (b3 - a3) / a3:+.0f}%; 2014 rests on {cov('MT00004', 'SO2', 2014):.0f}% "
    f"of the year; 2018-23 includes four years after the IMO's 0.5% fuel-sulphur cap for ships outside emission control "
    f"areas (1 January 2020; imo.org, Sulphur 2020 page, read 6 Oct 2026)")
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
        "the plan's Figures 25-26 comparison, recomputed; hours are the EEA Start time (beginning of the hour, fixed "
        "UTC+1 clock, no daylight saving; see section G); the plan's own labels follow no stated convention")
    d07 = prof["b"][7] - prof["a"][7]
    add(f"E-{pol}-07", f"Msida {pol}, Oct-Dec, 07:00-08:00: 2014-17 → 2018-19", f"{prof['a'][7]:.2f} → {prof['b'][7]:.2f}",
        unit, EEA, f"change {d07:+.2f}")
    morning = [prof["b"][h] - prof["a"][h] for h in range(6, 12)]
    evening = [prof["b"][h] - prof["a"][h] for h in range(16, 23)]
    hm = 6 + morning.index(min(morning))
    he = 16 + evening.index(min(evening))
    add(f"E-{pol}-range", f"Msida {pol}, Oct-Dec, change by hour 2014-17 → 2018-19: morning 06-11 / evening 16-22",
        f"{min(morning):+.2f} to {max(morning):+.2f} / {min(evening):+.2f} to {max(evening):+.2f}", unit, EEA,
        f"largest morning fall at {hm:02d}:00-{hm + 1:02d}:00 ({min(morning):+.2f}); largest evening fall at "
        f"{he:02d}:00-{he + 1:02d}:00 ({min(evening):+.2f}); hours are the EEA Start time (see section G)")
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
pre, post = [yearly[y] for y in range(2013, 2018)], [yearly[y] for y in range(2019, 2024)]
add("E-no2-sustained", "Msida NO2, Oct-Dec weekday 07:00-09:59: mean of the annual values 2013-17 → 2019-23",
    f"{sum(pre) / 5:.1f} → {sum(post) / 5:.1f}", "µg/m³", EEA,
    f"change {sum(post) / 5 - sum(pre) / 5:+.1f}; the step came in 2019 (2018: {yearly[2018]:.1f}); the later window "
    "includes the 2020-21 lockdown years; cannot be separated from fleet renewal or tested against a control")


def weekdays(y, m0=10, m1=12):
    d, n = dt.date(y, m0, 1), 0
    while d <= dt.date(y, m1, 31):
        n += d.weekday() < 5
        d += dt.timedelta(1)
    return n


def morn_cov(pol, y):
    got = sum(diurnal.get(("MT00005", pol, y, "Oct-Dec", "weekday", h), (0.0, 0))[1] for h in MORN)
    return 100 * got / (3 * weekdays(y))


add("E-no2-morning-cov", "Msida NO2, Oct-Dec weekday 07:00-09:59: share of the hours that have a valid value, by year",
    "; ".join(f"{y}: {morn_cov('NO2', y):.0f}%" for y in range(2013, 2024)), "%", EEA,
    "years under 85% are drawn hollow in Figure 4")
add("E-co-morning-cov", "Msida CO, Oct-Dec weekday 07:00-09:59: share of the hours that have a valid value, by year",
    "; ".join(f"{y}: {morn_cov('CO', y):.0f}%" for y in range(2013, 2024)), "%", EEA)
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

# ------------------------------------------------------------------ G. time labels: EEA hours against the plan's hours
# The EEA's hourly files give each value a "Start" (beginning of the hour). The plan's Figures 25-26 do not say which
# convention their hour labels follow. Test: do the EEA's Msida profiles reproduce the plan's NO2 curves (Figure 26,
# digitised from the PDF by digitise_fig26.py), and under which labelling?
clock = list(csv.DictReader(open(D / "clock_check.csv", encoding="utf-8")))
add("G-clock", "Hourly values per day on the days Malta's clocks changed (last Sunday of March and October), Msida NO2",
    f"{min(int(r['hourly_rows']) for r in clock)} on all {len(clock)} days, 2013-2023", "values", EEA,
    "26 Mar 2017: " + next(r["hourly_rows"] for r in clock if r["date"] == "2017-03-26") + "; 29 Oct 2017: " +
    next(r["hourly_rows"] for r in clock if r["date"] == "2017-10-29") + "; Start to End is one hour in every row. "
    "A local clock would give 23 and 25; this one has no daylight saving")


def hacc(pol, season, dtype):
    out = defaultdict(lambda: [0.0, 0])
    for (st, p_, y, se, dty, h), (sm, n) in diurnal.items():
        if st == "MT00005" and p_ == pol and se == season and (dtype == "all" or dty == dtype):
            out[(y, h)][0] += sm
            out[(y, h)][1] += n
    return out


def profile(acc, years, shift=0):
    """Hourly means pooled over `years`, labelled by label = Start hour + shift (shift 1 = hour-ending labels)."""
    out = []
    for lab in range(24):
        s_ = n_ = 0
        for y in years:
            a_, b_ = acc.get((y, (lab - shift) % 24), (0.0, 0))
            s_, n_ = s_ + a_, n_ + b_
        out.append(s_ / n_ if n_ else None)
    return out


def rmse(u, v):
    d_ = [(a_ - b_) ** 2 for a_, b_ in zip(u, v) if a_ is not None and b_ is not None]
    return (sum(d_) / len(d_)) ** 0.5 if d_ else float("inf")


for pol in ("NO2", "CO"):
    for season, nm in (("Oct-Dec", "winter"), ("Jun-Aug", "summer")):
        acc = hacc(pol, season, "all")
        ph = {}
        for y in range(2013, 2024):
            pr = [acc[(y, h)][0] / acc[(y, h)][1] if acc.get((y, h), (0, 0))[1] >= 30 else None for h in range(24)]
            if any(v is not None for v in pr):
                ph[y] = pr.index(max(v for v in pr if v is not None))
        add(f"G-{pol}-{nm}-peakhour", f"Msida {pol}, {season} ({nm}): hour (EEA Start) of the day's highest mean, by year",
            "; ".join(f"{y}: {h:02d}" for y, h in ph.items()), "hour", EEA,
            "all days; a year is skipped if no hour has 30 valid values (CO 2016)")
plan = defaultdict(list)
for r in csv.DictReader(open(D / "plan_fig26_digitised.csv", encoding="utf-8")):
    plan[r["series"]].append(float(r["no2_ugm3"]) if r["no2_ugm3"] else None)
pk = {k: max((v, i) for i, v in enumerate(vs) if v is not None) for k, vs in plan.items()}
add("G-plan-winter-peaks", "Plan Figure 26 (digitised), winter NO2 peak: 2014-17 → 2018-19",
    f"{pk['winter_2014-17'][0]:.1f} (label {pk['winter_2014-17'][1]:02d}) → {pk['winter_2018-19'][0]:.1f} "
    f"(label {pk['winter_2018-19'][1]:02d})", "µg/m³", "ERA, Air Quality Plan for Malta (2025), Figure 26, p. 60; digitised at 300 dpi",
    f"peak to peak {pk['winter_2018-19'][0] - pk['winter_2014-17'][0]:+.1f}; reading error about ±1 at a peak; the plan "
    "says 'around 10'; the 2018-19 peak sits one label later than the 2014-17 peak")
accw = hacc("NO2", "Oct-Dec", "all")
accwd = hacc("NO2", "Oct-Dec", "weekday")
a_all, b_all = max(profile(accw, P1)), max(profile(accw, P2))
a_wd, b_wd = max(profile(accwd, P1)), max(profile(accwd, P2))
add("G-eea-winter-peaks", "Msida NO2, Oct-Dec, peak of the mean daily profile: 2014-17 → 2018-19, all days / weekdays only",
    f"all days {a_all:.1f} → {b_all:.1f}; weekdays {a_wd:.1f} → {b_wd:.1f}", "µg/m³", EEA,
    f"peak to peak {b_all - a_all:+.1f} (all days), {b_wd - a_wd:+.1f} (weekdays); both periods peak at Start 07; "
    "the same under any shift applied to both periods")
b_off = profile(accw, P2, shift=1)[7]
add("G-offset", "Msida NO2, Oct-Dec: 2014-17 at Start 07 against 2018-19 labelled one hour later (label 07 = Start 06)",
    f"{profile(accw, P1)[7]:.1f} → {b_off:.1f}", "µg/m³", EEA,
    f"{b_off - profile(accw, P1)[7]:+.1f}: a one-hour offset between the periods alone gives a 'fall' of this size "
    "at label 07, close to the plan's peak to peak")
fits = {}
for key, season, yrs in (("winter_2014-17", "Oct-Dec", P1), ("winter_2018-19", "Oct-Dec", P2),
                         ("summer_2014-17", "Jun-Aug", P1), ("summer_2018-19", "Jun-Aug", P2)):
    res = []
    for dtype in ("all", "weekday"):
        acc = hacc("NO2", season, dtype)
        for shift in (0, 1):
            res.append((rmse(profile(acc, yrs, shift), plan[key]), dtype, shift))
    res.sort()
    fits[key] = res
    r0 = min(x for x in res if x[2] == 0)
    r1_ = min(x for x in res if x[2] == 1)
    add(f"G-fit-{key}", f"Msida NO2, {season}, {yrs[0]}-{str(yrs[-1])[2:]}: RMSE of the EEA profile against the plan's curve",
        f"label = Start: {r0[0]:.1f} ({r0[1]}); label = Start + 1: {r1_[0]:.1f} ({r1_[1]})", "µg/m³", f"{EEA}; plan Figure 26",
        "best day-type in brackets; Start + 1 means hour-ending labels")
pool = [y for y in range(2013, 2020)]
best = []
for k in range(1, len(pool) + 1):
    for sub in itertools.combinations(pool, k):
        for dtype in ("all", "weekday"):
            acc = hacc("NO2", "Oct-Dec", dtype)
            for shift in (0, 1):
                best.append((rmse(profile(acc, sub, shift), plan["winter_2014-17"]), sub, dtype, shift))
best.sort(key=lambda t: t[0])
add("G-fit-subset", "Plan's winter 2014-17 NO2 curve: best RMSE over any subset of the years 2013-2019, either day-type, "
    "either labelling", f"{best[0][0]:.1f}", "µg/m³", EEA, f"best subset {best[0][1]}, {best[0][2]}, shift {best[0][3]}; "
    "the best-fitting subsets are not the years 2014-17")
add("G-conclusion", "Reading of G-fit and G-eea-winter-peaks", "2018-19 reproduces with hour-ending labels; 2014-17 does not "
    "reproduce under either labelling", "", f"{EEA}; plan Figure 26", "so the plan's gap lies in its 2014-17 baseline; "
    "like for like the winter peak does not fall (all days -1.0; weekdays +0.7)")

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
