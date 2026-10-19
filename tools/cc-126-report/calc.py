"""Claim Check 126: contract-term arithmetic and the pipeline's dated targets. Output: data/cc-126/checks.csv"""
import csv, datetime as dt, hashlib, pathlib

HERE = pathlib.Path(__file__).resolve().parent
D = HERE.parents[1] / "data" / "cc-126"
ENEMALTA = "Enemalta press release 21 Jun 2026 (retrieved 19 Oct 2026)"
ITALPRESS = "Italpress/MNA 22 Jun 2026 (retrieved 19 Oct 2026)"
announce = dt.date(2026, 6, 21)      # Enemalta release date in its URL; PN (22 Jun) says the PM announced "yesterday"
socar_end = dt.date(2026, 8, 13)     # SOCAR contract expiry (Italpress)
bp_end = dt.date(2027, 5, 31)        # "till the end of May 2027" (Enemalta)
m = lambda a, b: (b - a).days / (365.25 / 12)
rows = [
    ("Days from announcement (21 Jun 2026) to end of May 2027", (bp_end - announce).days, "days", ENEMALTA, ""),
    ("Months from announcement to end of May 2027", round(m(announce, bp_end), 1), "months", ENEMALTA, "days / 30.44"),
    ("Days from SOCAR expiry (13 Aug 2026) to end of May 2027", (bp_end - socar_end).days, "days", ITALPRESS + "; " + ENEMALTA, "supply start date not published; SOCAR expiry used"),
    ("Months of supply cover if it starts when SOCAR ends", round(m(socar_end, bp_end), 1), "months", ITALPRESS + "; " + ENEMALTA, ""),
    ("Gap: SOCAR expiry minus announcement", (socar_end - announce).days, "days", ITALPRESS, "'just weeks before' (PN, Italpress)"),
    ("Pipeline target years found: Melita TransGas indicative commissioning", 2030, "year", "melitatransgas.com.mt 'Next Steps' (site last updated 22 Dec 2022; retrieved 19 Oct 2026)", "construction start 2028 (indicative)"),
    ("Years between PN's 'this year' (2026) and the promoter's indicative commissioning", 2030 - 2026, "years", "as above", ""),
    ("Earlier target 2024 (completion expected, July 2019)", 2024, "year", "MaltaToday 26 Jul 2019, second-hand via gem.wiki (not opened)", "second-hand"),
    ("Earlier target 2025 (operations commence, Melita Transgas schedule Sept 2020)", 2025, "year", "gem.wiki citing the schedule (not opened)", "second-hand"),
]
with open(D / "checks.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["check", "value", "unit", "source", "note"]); w.writerows(rows)
for r in rows: print(r[:3])
