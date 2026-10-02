"""Recalculate WSC public potable-water production indicators for CC-009."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "cc-009"


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
        {"check": "Groundwater bodies failing nitrate standard", "value": "12", "unit": "of 15 bodies", "source": "ERA/EWA 3rd River Basin Management Plan, Chapter 6", "note": "Three exceptions are named; 14 bodies fail overall chemical status, which is broader than nitrate alone."},
    ])
    with (DATA / "checks.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["check", "value", "unit", "source", "note"])
        writer.writeheader()
        writer.writerows(out)
    print(f"2025 RO share: {by_year[2025][3]:.1f}%")
    print(f"WSC groundwater production change 2022-2025: {change_22_25:.2f}%")
    print(f"2024-2025 chart-derived decline: {-change_24_25:.2f}%; WSC prose says 11.4%")
    print("RBMP: two bodies poor quantitatively; 14 poor chemically; 12 exceed nitrate standard.")


if __name__ == "__main__":
    main()
