#!/usr/bin/env python3
"""CC-071: tests of the Shift's 26 Feb 2026 statement on public-transport subsidies and congestion.
Writes data/cc-071/checks.csv, subsidy_series.csv, cars_population.csv.

Inputs (all sourced; retrieval 10 Oct 2026):
- Subsidy components for 2025 and the 2024 total: The Shift News 26 Feb 2026 (Ivan Camilleri), who cites replies by the Transport
  Minister to PN MP Chris Said; the reply itself (parlament.mt) was not available to us. Newsbook (27 Feb 2026, Maltese) gives the same
  components. Both are second-hand for the figures.
- Payments to Malta Public Transport 2021-2023: Business Now, 18 Apr 2024 (2023 figure from information tabled in Parliament; 2021 and
  2022 as the outlet states them).
- Passenger cars: Eurostat road_eqs_carmot (MT, TOTAL, TOTAL), stock at 31 Dec; population: Eurostat demo_gind (JAN, MT), 1 January.
  Files saved in data/cc-071/ (road_eqs_carmot.json, demo_gind.json).
- Congestion: TomTom Traffic Index, Valletta metro area, annual average congestion level and mean speed, 2025 and 2024 (previous-year
  block on the same page), https://www.tomtom.com/traffic-index/city/valletta/ (values copied from the page's data, 10 Oct 2026)."""
import csv, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-071"
RET = "2026-10-10"

def series(fn, dim_slice=None):
    d = json.load(open(D / fn))
    t = list(d["dimension"]["time"]["category"]["index"])
    return {int(y): d["value"].get(str(i)) for i, y in enumerate(t)}

cars = series("road_eqs_carmot.json")   # all other dimensions have one position (TOTAL), so index = time position
pop = series("demo_gind.json")

# ---- subsidy: components reported for 2025 (EUR million)
comp = [("PSO concession fee (Autobuses de Leon / Malta Public Transport)", 59.0),
        ("Tallinja card scheme (free travel)", 31.2),
        ("Investment in new buses", 3.2)]
total25 = round(sum(v for _, v in comp), 1)
rows = []
def add(check, value, unit, source, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": source, "retrieved": RET, "note": note})

SH = "The Shift News 26 Feb 2026 (second-hand: parliamentary reply not read)"
add("Sum of the three 2025 components reported by the Shift", total25, "EUR million", SH, "59.0 + 31.2 + 3.2")
add("Shortfall of that sum against EUR 100 million", round(100 - total25, 1), "EUR million", SH)
add("Shortfall as a share of EUR 100 million", round((100 - total25), 1), "per cent", SH)
op = round(59.0 + 31.2, 1)
add("Operating payments only (PSO fee + Tallinja card), excluding bus investment", op, "EUR million", SH,
    "bus purchases are capital investment, not an operating subsidy")
add("2025 sum against the Shift's 2024 total (EUR 84 million)", round((total25 / 84 - 1) * 100, 1), "per cent", SH + "; 2024 total also from the Shift")
pay = {2021: 36.3, 2022: 42.8, 2023: 69.4, 2024: 84.0, 2025: total25}
add("2025 sum against 2023 payments (EUR 69.4 million)", round((total25 / 69.4 - 1) * 100, 1), "per cent",
    "Shift 26 Feb 2026; Business Now 18 Apr 2024 (both second-hand)")
add("2024 budget allocation (PSO 49 + free-ride scheme 25), as reported", 74.0, "EUR million", "Business Now 18 Apr 2024 (second-hand)",
    "Budget 2024 documents not readable (finance.gov.mt 403)")
add("2024 payment above the 2024 allocation", round(84 - 74, 1), "EUR million", "Shift 26 Feb 2026; Business Now 18 Apr 2024 (second-hand)")
p25 = pop[2025]
add("2025 sum per resident (population 1 Jan 2025)", round(total25 * 1e6 / p25), "EUR", "Shift 26 Feb 2026 (second-hand); Eurostat demo_gind")

# ---- cars and population
yrs = list(range(2019, 2026))
with open(D / "cars_population.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["year", "passenger_cars_31dec", "population_1jan", "cars_per_1000_same_year_pop", "source", "retrieved"])
    for y in yrs:
        w.writerow([y, cars[y], pop[y], round(cars[y] / pop[y] * 1000, 1),
                    "Eurostat road_eqs_carmot (MT, TOTAL); demo_gind (MT, JAN)", RET])
g = lambda s, a, b: round((s[b] / s[a] - 1) * 100, 1)
add("Passenger cars, growth 2024 to 2025", g(cars, 2024, 2025), "per cent", "Eurostat road_eqs_carmot")
add("Passenger cars, growth 2022 to 2025 (free buses from 1 Oct 2022)", g(cars, 2022, 2025), "per cent", "Eurostat road_eqs_carmot")
add("Passenger cars, growth 2019 to 2022", g(cars, 2019, 2022), "per cent", "Eurostat road_eqs_carmot")
add("Population (1 Jan), growth 2022 to 2025", g(pop, 2022, 2025), "per cent", "Eurostat demo_gind")
add("Cars per 1,000 residents, 2022 (cars at 31 Dec / population 1 Jan same year)", round(cars[2022] / pop[2022] * 1000), "cars", "Eurostat; our ratio",
    "Eurostat's own rate (road_eqs_carhab) uses the next 1 January; ours is a like-for-like ratio for both years")
add("Cars per 1,000 residents, 2025", round(cars[2025] / pop[2025] * 1000), "cars", "Eurostat; our ratio")
add("Cars added per day, 2024 to 2025", round((cars[2025] - cars[2024]) / 365, 1), "cars/day", "Eurostat road_eqs_carmot",
    "net change in passenger cars only; Newsbook (27 Feb 2026) writes of an average of 35 vehicles a day (all vehicles; not tested)")

# ---- TomTom Valletta metro area
tt = [(2024, 49.2, 28.1), (2025, 50.3, 27.6)]
with open(D / "tomtom_valletta.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["year", "congestion_level_pct", "mean_speed_kmh", "source", "retrieved"])
    for y, c, v in tt:
        w.writerow([y, c, v, "TomTom Traffic Index, Valletta metro area, annual (page data, 2024 from the page's previous-year block)", RET])
add("Valletta metro congestion level, change 2024 to 2025", round(50.3 - 49.2, 1), "percentage points", "TomTom Traffic Index",
    "congestion level = extra travel time against free flow; Valletta page shows +1.1; only two years read by us")
add("Valletta metro mean speed, change 2024 to 2025", round(27.6 - 28.1, 1), "km/h", "TomTom Traffic Index")

with open(D / "subsidy_series.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["year", "payments_eur_million", "basis", "source", "retrieved"])
    basis = {2021: "payments to MPT as stated by outlet", 2022: "payments to MPT as stated by outlet",
             2023: "payments to MPT, information tabled in Parliament (as reported)", 2024: "total subsidies as reported",
             2025: "sum of three components reported (the Shift: 'almost EUR 100 million')"}
    src = {2021: "Business Now 18 Apr 2024", 2022: "Business Now 18 Apr 2024", 2023: "Business Now 18 Apr 2024",
           2024: "The Shift News 26 Feb 2026", 2025: "The Shift News 26 Feb 2026; Newsbook 27 Feb 2026"}
    for y, v in pay.items():
        w.writerow([y, v, basis[y], src[y] + " (second-hand)", RET])

# fix the share row (value in per cent)
for r in rows:
    if r["check"].startswith("Shortfall as a share"):
        r["value"] = round((100 - total25) / 100 * 100, 1)
with open(D / "checks.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for r in rows: print(r["value"], r["unit"], "|", r["check"])
