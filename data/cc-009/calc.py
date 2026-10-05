"""Recalculate WSC public potable-water production indicators for CC-009.

v1.2 adds national checks from eurostat_water.csv (tools/cc-009-report/fetch_data.py) and published values from
Sapiano (2020), Table 1. Writes checks.csv.
"""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "cc-009"


def national_checks(by_year: dict) -> list:
    """v1.2: WSC's figures against national abstraction and recharge (Eurostat, eurostat_water.csv)."""
    es = {}
    for r in csv.DictReader((DATA / "eurostat_water.csv").open(encoding="utf-8")):
        es[(r["wat_proc"], int(r["year"]))] = (float(r["value"]), r["flag"])
    src_abs = "Eurostat env_wat_abs (updated 2026-09-16), retrieved 2026-10-05"
    src_res = "Eurostat env_wat_res (updated 2026-07-03), retrieved 2026-10-05"

    def v(code, year):
        return es[(code, year)][0]

    def fl(code, year):
        f = es[(code, year)][1]
        return f"Eurostat flag '{f}'" + (" (estimated)" if "e" in f else "") if f else "no flag"

    tot, agr, pws = v("ABST", 2024), v("ABS_AGR", 2024), v("ABS_PWS", 2024)
    rows = [
        {"check": "National fresh groundwater abstraction 2024", "value": f"{tot:.2f}", "unit": "million m3",
         "source": src_abs, "note": fl("ABST", 2024)},
        {"check": "Agricultural groundwater abstraction 2024", "value": f"{agr:.2f}", "unit": "million m3",
         "source": src_abs, "note": f"{fl('ABS_AGR', 2024)}; {100 * agr / tot:.1f}% of the national total"},
        {"check": "Agricultural groundwater abstraction change 2023 to 2024", "value": f"{agr - v('ABS_AGR', 2023):.2f}",
         "unit": "million m3", "source": src_abs, "note": f"{v('ABS_AGR', 2023):.2f} -> {agr:.2f}; both estimated"},
        {"check": "Public water supply groundwater abstraction 2024", "value": f"{pws:.2f}", "unit": "million m3",
         "source": src_abs, "note": f"{fl('ABS_PWS', 2024)}; {100 * pws / tot:.1f}% of the national total"},
    ]
    other = tot - agr - pws
    rows.append({"check": "Other groundwater abstraction 2024 (households, industry, services, mining)",
                 "value": f"{other:.2f}", "unit": "million m3", "source": src_abs,
                 "note": "total minus agriculture minus public water supply; sector values: " + ", ".join(
                     f"{c} {v(c, 2024):.2f}" for c in ("ABS_HH", "ABS_IND", "ABS_SER", "ABS_MIN"))})
    cut = (by_year[2024][1] - by_year[2025][1]) / 1e6
    rows += [
        {"check": "WSC groundwater production cut 2024 to 2025", "value": f"{cut:.3f}", "unit": "million m3",
         "source": "WSC Annual Report 2025 Figure 20", "note": "chart values; WSC prose implies 11.4% of 2024"},
        {"check": "WSC 2025 cut as share of national groundwater abstraction 2024", "value": f"{100 * cut / tot:.2f}",
         "unit": "%", "source": "calculated", "note": "years differ: 2025 national data not yet published"},
        {"check": "WSC 2025 cut as share of the 2024 rise in agricultural abstraction",
         "value": f"{100 * cut / (agr - v('ABS_AGR', 2023)):.0f}", "unit": "%", "source": "calculated",
         "note": "indicative only: different years, and agricultural values are estimates"},
    ]
    for y in (2022, 2023, 2024):
        rows.append({"check": f"Eurostat public-supply groundwater abstraction minus WSC groundwater production {y}",
                     "value": f"{v('ABS_PWS', y) - by_year[y][1] / 1e6:.2f}", "unit": "million m3",
                     "source": src_abs + "; WSC Annual Report 2025 Figure 20",
                     "note": f"{v('ABS_PWS', y):.2f} vs {by_year[y][1] / 1e6:.2f}; different measures (abstraction vs "
                             "production); difference not explained in either source"})
    pws_years = [y for y in range(2015, 2025) if ("ABS_PWS", y) in es]
    low = min(pws_years, key=lambda y: v("ABS_PWS", y))
    rows.append({"check": "Lowest Eurostat public-supply groundwater abstraction 2015-2024", "value": f"{v('ABS_PWS', low):.2f}",
                 "unit": "million m3", "source": src_abs,
                 "note": f"in {low}; no value for " + ", ".join(str(y) for y in range(2015, 2025) if y not in pws_years)})
    rch = v("AQUI", 2024)
    rows += [
        {"check": "Estimated recharge into the aquifer 2024", "value": f"{rch:.2f}", "unit": "million m3",
         "source": src_res, "note": fl("AQUI", 2024)},
        {"check": "National groundwater abstraction as share of estimated recharge 2024", "value": f"{100 * tot / rch:.1f}",
         "unit": "%", "source": "calculated", "note": "both estimates; recharge is not all available for abstraction "
                                                       "(Sapiano 2020 sets aside natural discharge to the sea)"},
        {"check": "Lowest estimated recharge 2010-2024", "value": f"{min(v('AQUI', y) for y in range(2010, 2025)):.2f}",
         "unit": "million m3", "source": src_res,
         "note": f"in {min(range(2010, 2025), key=lambda y: v('AQUI', y))}"},
        {"check": "National groundwater abstraction change 2015 to 2024", "value": f"{100 * (tot / v('ABST', 2015) - 1):.1f}",
         "unit": "%", "source": "calculated", "note": f"{v('ABST', 2015):.2f} -> {tot:.2f}; estimates"},
        {"check": "Available groundwater, long-term annual average (published estimate)", "value": "37",
         "unit": "million m3", "source": "Sapiano 2020, Acque Sotterranee 9(3), Table 1",
         "note": "renewable 65 minus natural subsurface discharge 24 and unrecoverable runoff 4; 35 in 2019; reported, "
                 "not recomputed"},
        {"check": "Total abstraction/utilisation, long-term average and 2019 (published estimate)", "value": "38; 41",
         "unit": "million m3", "source": "Sapiano 2020, Table 1", "note": "WEI+ 78% (long-term) and 89% (2019) as "
                                                                         "published; EU high-stress threshold 40%"},
    ]
    return rows


def main() -> None:
    with (DATA / "wsc_production.csv").open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    out = []
    by_year = {}
    for row in rows:
        year = int(row["year"])
        ro = int(row["ro_m3"])
        groundwater = int(row["groundwater_m3"])
        total = ro + groundwater
        share = 100 * ro / total
        by_year[year] = (ro, groundwater, total, share)
        out.extend([
            {"check": f"{year} RO share of WSC potable production", "value": f"{share:.4f}", "unit": "%", "source": row["source"], "note": "Calculated as RO production / (RO + WSC groundwater production)."},
            {"check": f"{year} total WSC potable production", "value": str(total), "unit": "m3", "source": row["source"], "note": "RO plus groundwater production."},
        ])
    first = by_year[2022][1]
    last = by_year[2025][1]
    change_22_25 = 100 * (last / first - 1)
    prev = by_year[2024][1]
    change_24_25 = 100 * (last / prev - 1)
    reported_change = -11.4
    out.extend([
        {"check": "WSC groundwater production change 2022 to 2025", "value": f"{change_22_25:.4f}", "unit": "%", "source": "WSC Annual Report 2025 Figure 20", "note": "Calculated from the annual report chart values; WSC production series, not all-user national abstraction."},
        {"check": "WSC groundwater production change 2024 to 2025 from chart", "value": f"{change_24_25:.4f}", "unit": "%", "source": "WSC Annual Report 2025 Figure 20", "note": f"WSC narrative states {reported_change:.1f}%; chart values imply {change_24_25:.2f}%, a small internal difference retained rather than reconciled."},
        {"check": "WSC groundwater production change 2024 to 2025 as reported", "value": f"{reported_change:.1f}", "unit": "%", "source": "WSC Annual Report 2025 p.43", "note": "Directly stated by WSC; separate from calculation using chart values."},
        {"check": "Groundwater bodies failing nitrate standard", "value": "12", "unit": "of 15 bodies", "source": "ERA/EWA 3rd River Basin Management Plan, Chapter 6", "note": "Three exceptions are named; the plan records 14 bodies failing chemical status, which is broader than nitrate alone (Malta's 3rd-cycle EU reporting lists 15; see wise_gwb_status.csv)."},
    ])
    out.extend(national_checks(by_year))
    with (DATA / "checks.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["check", "value", "unit", "source", "note"])
        writer.writeheader()
        writer.writerows(out)
    print(f"2025 RO share: {by_year[2025][3]:.1f}%")
    print(f"WSC groundwater production change 2022-2025: {change_22_25:.2f}%")
    print(f"2024-2025 chart-derived decline: {-change_24_25:.2f}%; WSC prose says 11.4%")
    print("RBMP chapter 6 (as recorded): Malta and Gozo MSL poor quantitatively; 14 poor chemically; 12 exceed nitrate standard.")
    print("WISE 3rd-cycle reporting (wise_gwb_status.csv): 4 poor quantitatively; 15 poor chemically.")


if __name__ == "__main__":
    main()
