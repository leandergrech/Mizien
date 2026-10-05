#!/usr/bin/env python3
"""CC-100: test "over 10 million passengers in 2025" (Malta International Airport plc, full-year traffic update,
14 Jan 2026: 10,061,969 passenger movements, +12.3%) against Eurostat avia_paoc.

Reads data/cc-100/eurostat_avia_paoc.csv (fetch.py; updated 2 Oct 2026, retrieved 5 Oct 2026) and
data/cc-100/mia_announcements.csv; writes data/cc-100/checks.csv. Eurostat's passengers carried (PAS_CRD) at the
reporting airport count each arriving and departing passenger, as MIA's "passenger movements" do.
"""
import csv, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-100"
e = {(r["tra_meas"], r["schedule"], r["tra_cov"], int(r["year"])): float(r["value"]) for r in csv.DictReader(open(D / "eurostat_avia_paoc.csv"))}
m = {r["item"]: float(r["value"]) for r in csv.DictReader(open(D / "mia_announcements.csv"))}
SRC = "Eurostat avia_paoc (updated 2 Oct 2026), retrieved 5 Oct 2026; MIA company announcement 461/2026"
rows = []


def add(check, value, unit, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": SRC, "note": note})


T = lambda y: e[("PAS_CRD", "TOTAL", "TOTAL", y)]
add("MIA: passenger movements 2025", int(m["passenger movements 2025"]), "passengers", "company announcement 14 Jan 2026")
for y in (2019, 2023, 2024, 2025):
    add(f"Eurostat: passengers carried at Malta airport, {y}", int(T(y)), "passengers")
add("Eurostat 2025 minus MIA 2025", int(T(2025) - m["passenger movements 2025"]), "passengers",
    f"{100 * (T(2025) / m['passenger movements 2025'] - 1):.2f}% difference")
add("Eurostat: change 2024 to 2025", round(100 * (T(2025) / T(2024) - 1), 1), "%", "MIA: +12.3%")
add("Eurostat: change 2019 to 2025", round(100 * (T(2025) / T(2019) - 1), 1), "%")
add("Eurostat: first year above 10 million", min(y for y in range(2015, 2026) if ("PAS_CRD", "TOTAL", "TOTAL", y) in e and T(y) > 1e7), "year")
add("Eurostat: share of 2025 passengers on flights to or from outside the EU", round(100 * e[("PAS_CRD", "TOTAL", "INTL_XEU27_2020", 2025)] / T(2025), 1), "%")
with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for r in rows:
    print(f"{r['check'][:70]:70s} {r['value']:>12} {r['unit']}  {r['note']}")
