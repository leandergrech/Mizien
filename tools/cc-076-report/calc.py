#!/usr/bin/env python3
"""CC-076: test the NSO statement "At the end of March 2026, the stock of licensed motor vehicles stood at 460,648 ... increased
by 3,245 ... at a net average rate of 36 motor vehicles per day" (NR 085/2026, 13 May 2026) and the Commission's "35 a day".

Reads data/cc-076/nso_stock_by_quarter.csv (fetch.py) and writes data/cc-076/checks.csv and daily_increase.csv. The daily rate
follows NSO's methodological note 7: (stock this quarter - stock previous quarter) / days in quarter. The flows (5,680 newly
licensed, 6,963 restricted, 4,140 restrictions ended) are quoted from the NSO release text, where they are published numbers."""
import calendar, csv, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-076"
rows_in = list(csv.DictReader(open(D / "nso_stock_by_quarter.csv")))
stock = {(int(r["year"]), r["quarter"]): int(r["total"]) for r in rows_in}
SRC = "NSO NR 085/2026 Table 1, via Internet Archive, retrieved 5 Oct 2026"
rows = []


def add(check, value, unit, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": SRC, "note": note})


def days(y, q):
    ms = {"Q1": (1, 2, 3), "Q2": (4, 5, 6), "Q3": (7, 8, 9), "Q4": (10, 11, 12)}[q]
    return sum(calendar.monthrange(y, m)[1] for m in ms)


keys = sorted(stock)
bad = [(r["year"], r["quarter"]) for r in rows_in if int(r["sum_of_columns"]) != int(r["total"])]
add("Quarters where the category columns do not sum to the printed total", ", ".join(map(str, bad)) or "none", "quarters")
series = []
for prev, cur in zip(keys, keys[1:]):
    d = stock[cur] - stock[prev]; n = days(*cur)
    series.append((cur, stock[cur], d, n, d / n))
    add(f"Net increase in stock, {cur[1]} {cur[0]}", d, "vehicles", f"{n} days; {d / n:.2f} per day")
q1 = stock[(2026, "Q1")] - stock[(2025, "Q4")]
add("Stock at end of March 2026", stock[(2026, "Q1")], "vehicles", "NSO text: 460,648")
add("Net increase Q1 2026", q1, "vehicles", "NSO text: 3,245")
add("Days in Q1 2026", days(2026, "Q1"), "days")
add("Net average daily increase, Q1 2026 (note 7)", round(q1 / days(2026, "Q1"), 2), "vehicles per day", "NSO text: 36")
add("Net average daily increase, Q4 2025", round((stock[(2025, "Q4")] - stock[(2025, "Q3")]) / days(2025, "Q4"), 2), "vehicles per day",
    "Commission's 2026 Country Report says 35 and cites NSO Q4/2025")
add("Net average daily increase, Q3 2025", round((stock[(2025, "Q3")] - stock[(2025, "Q2")]) / days(2025, "Q3"), 2), "vehicles per day",
    "Newsbook (11 Nov 2025) reports 3,344 and 36 a day for Q3 2025")
y = stock[(2025, "Q4")] - stock[(2024, "Q4")]
add("Net average daily increase over calendar 2025", round(y / 365, 2), "vehicles per day", f"{y} vehicles over 365 days")
y2 = stock[(2026, "Q1")] - stock[(2025, "Q1")]
add("Net average daily increase, four quarters to end Q1 2026", round(y2 / 365, 2), "vehicles per day", f"{y2} vehicles over 365 days")
add("Growth of stock, end Q1 2023 to end Q1 2026", round(100 * (stock[(2026, "Q1")] / stock[(2023, "Q1")] - 1), 1), "%", "")
new, start, end = 5680, 6963, 4140
add("Gross newly licensed per day, Q1 2026", round(new / days(2026, "Q1")), "vehicles per day", "NSO text: 63")
ident = stock[(2025, "Q4")] + new - start + end
add("Stock by NSO note 6 (previous stock + new - restricted + restrictions ended)", ident, "vehicles",
    f"differs from the published stock by {stock[(2026, 'Q1')] - ident}; NSO says cut-off dates of databases can cause small differences")
add("Net change by the flow identity", new - start + end, "vehicles", f"{(new - start + end) / days(2026, 'Q1'):.1f} per day")
add("Net as share of gross newly licensed, Q1 2026", round(100 * q1 / new, 1), "%", "36 net a day against 63 newly licensed a day")
with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
with open(D / "daily_increase.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["year", "quarter", "stock_end", "net_increase", "days", "per_day"])
    for (y_, q_), s, d, n, p in series:
        w.writerow([y_, q_, s, d, n, round(p, 2)])
for r in rows:
    print(f"{r['check'][:78]:78s} {str(r['value']):>10} {r['unit']}  {r['note'][:50]}")
