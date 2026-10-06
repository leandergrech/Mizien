"""CC-102: recompute the Ombudsman's non-implementation rates from the annual-report tables.
Input: data/cc-102/ombudsman_sustained_cases.csv (typed from Tables 1.3 and 1.22 of the 2023-2025 annual reports).
Output: data/cc-102/rates.csv. Run: python calc.py"""
import csv
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
rows = list(csv.DictReader(open(ROOT / "data" / "cc-102" / "ombudsman_sustained_cases.csv")))
out = []
for r in rows:
    n = {k: int(v) for k, v in r.items() if k not in ("year", "office", "source_table")}
    sustained, ni = n["sustained_cases"], n["not_implemented"]
    with_rec = sustained - n["no_recommendation"] - n["awaiting_outcome"]
    out.append({
        "year": r["year"], "office": r["office"], "sustained_cases": sustained, "not_implemented": ni,
        "rate_of_sustained_pct": round(100 * ni / sustained, 1),
        "cases_with_recommendation": with_rec,
        "rate_of_cases_with_recommendation_pct": round(100 * ni / with_rec, 1) if with_rec else "",
        "reports_to_parliament": n["reports_to_parliament"],
    })
for office in sorted({r["office"] for r in rows}):
    sel = [r for r in rows if r["office"] == office]
    s = sum(int(r["sustained_cases"]) for r in sel)
    ni = sum(int(r["not_implemented"]) for r in sel)
    wr = sum(int(r["sustained_cases"]) - int(r["no_recommendation"]) - int(r["awaiting_outcome"]) for r in sel)
    out.append({"year": "2023-2025", "office": office, "sustained_cases": s, "not_implemented": ni,
                "rate_of_sustained_pct": round(100 * ni / s, 1), "cases_with_recommendation": wr,
                "rate_of_cases_with_recommendation_pct": round(100 * ni / wr, 1) if wr else "",
                "reports_to_parliament": sum(int(r["reports_to_parliament"]) for r in sel)})
# 2025 consistency checks against the report's own totals
y25 = [r for r in rows if r["year"] == "2025"]
tot_ni = sum(int(r["not_implemented"]) for r in y25)
tot_rep = sum(int(r["reports_to_parliament"]) for r in y25)
tot_s = sum(int(r["sustained_cases"]) for r in y25)
assert (tot_s, tot_ni, tot_rep) == (81, 22, 22), (tot_s, tot_ni, tot_rep)
# Chapter 3 of the 2025 report (Commissioner for Environment and Planning): 5 implemented, 2 implemented after
# referral to the House, 5 still not implemented, of 12 sustained cases.
still_open = 5
# Reconciliation of Table 1.3 (4 implemented + 1 partly, 7 not) with the chapter (5 implemented, 2 later, 5 open):
e25 = next(r for r in y25 if r["office"] == "Environment and Planning")
assert int(e25["implemented"]) + int(e25["partly_implemented"]) == 5      # chapter's "five implemented"
assert int(e25["not_implemented"]) == 2 + still_open == 7                 # 2 implemented later + 5 still open
assert 5 + 2 + still_open == int(e25["sustained_cases"]) == 12
out.append({"year": "2025 (chapter 3, at time of writing)", "office": "Environment and Planning", "sustained_cases": 12,
            "not_implemented": still_open, "rate_of_sustained_pct": round(100 * still_open / 12, 1),
            "cases_with_recommendation": 12, "rate_of_cases_with_recommendation_pct": round(100 * still_open / 12, 1),
            "reports_to_parliament": 7})
with open(ROOT / "data" / "cc-102" / "rates.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0]))
    w.writeheader()
    w.writerows(out)
for o in out:
    print(o)
