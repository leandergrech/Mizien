"""Compare PQ 29696 annual values with EEA validated daily PM2.5 downloads.

Run from the repository root with the optional dependency installed:
    python -m pip install -r tools/cc-007-report/requirements-eea.txt
    python tools/cc-007-report/eea_crosscheck.py

The EEA download service exposes validated E1a station measurements as Parquet.
This script averages valid daily aggregates by calendar year. That transparent
calculation is a cross-check, not a substitute for ERA's regulatory annual mean.
"""
from __future__ import annotations

import csv
import hashlib
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from urllib.request import Request, urlopen

import pyarrow.parquet as pq
import pyarrow as pa

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "cc-007"
DATE = "2026-10-03"
STATIONS = {
    "Attard": ("MT00008", "https://eeadmz1batchservice02.blob.core.windows.net/airquality-p-e1a/MT/SPO-MT00008_06001_100.parquet"),
    "Msida": ("MT00011", "https://eeadmz1batchservice02.blob.core.windows.net/airquality-p-e1a/MT/SPO-MT00011_06001_103.parquet"),
    "St Paul's Bay": ("MT00009", "https://eeadmz1batchservice02.blob.core.windows.net/airquality-p-e1a/MT/SPO-MT00009_06001_101.parquet"),
    "Żejtun": ("MT00004", "https://eeadmz1batchservice02.blob.core.windows.net/airquality-p-e1a/MT/SPO-MT00004_06001_101.parquet"),
    "Għarb": ("MT00007", "https://eeadmz1batchservice02.blob.core.windows.net/airquality-p-e1a/MT/SPO-MT00007_06001_100.parquet"),
}

pq_rows = list(csv.DictReader((DATA / "station_pm25.csv").open(encoding="utf-8", newline="")))
pq_values = {(r["station"], int(r["year"])): r["annual_pm25_ug_m3"] for r in pq_rows}
daily_values: dict[tuple[str, int], list[float]] = {}
manifest = []

for station, (eoi_code, url) in STATIONS.items():
    request = Request(url, headers={"User-Agent": "Mizien/1.0 research; public EEA data"})
    with urlopen(request, timeout=60) as response:
        blob = response.read()
    digest = hashlib.sha256(blob).hexdigest()
    table = pq.read_table(pa.BufferReader(blob))
    manifest.append({
        "station": station,
        "eoi_code": eoi_code,
        "url": url,
        "retrieved_date": DATE,
        "bytes": len(blob),
        "sha256": digest,
        "source_note": "EEA Air Quality download service; E1a validated station data",
    })
    for row in table.to_pylist():
        year = row["Start"].year
        if not 2020 <= year <= 2024:
            continue
        value = row["Value"]
        if (row["AggType"] == "day" and row["Validity"] == 1
                and row["Verification"] == 1 and value is not None and float(value) >= 0):
            daily_values.setdefault((station, year), []).append(float(value))

rows = []
for station in STATIONS:
    for year in range(2020, 2025):
        values = daily_values.get((station, year), [])
        days = 366 if year in (2020, 2024) else 365
        eea_mean = sum(values) / len(values) if values else None
        pq_value = pq_values.get((station, year), "")
        if eea_mean is None:
            relation = "No validated daily series in the retrieved EEA station file"
        elif not pq_value:
            relation = "PQ annex marks n/a; EEA series supplies a value"
        else:
            pq_rounded = Decimal(str(eea_mean)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
            relation = "matches to 0.1" if pq_rounded == Decimal(pq_value) else "does not match to 0.1"
        rows.append({
            "station": station,
            "eoi_code": STATIONS[station][0],
            "year": year,
            "pq_annex_ug_m3": pq_value,
            "eea_mean_of_valid_daily_aggregates_ug_m3": "" if eea_mean is None else f"{eea_mean:.6f}",
            "eea_valid_days": len(values),
            "calendar_days": days,
            "eea_day_coverage_pct": "" if not values else f"{100 * len(values) / days:.1f}",
            "comparison": relation,
            "source_retrieved_date": DATE,
        })

with (DATA / "eea_station_file_manifest.csv").open("w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=manifest[0].keys(), lineterminator="\n")
    writer.writeheader()
    writer.writerows(manifest)
with (DATA / "eea_validated_crosscheck.csv").open("w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys(), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)

available = [r for r in rows if r["eea_mean_of_valid_daily_aggregates_ug_m3"]]
matches = sum(r["comparison"] == "matches to 0.1" for r in available)
checks_path = DATA / "checks.csv"
with checks_path.open(encoding="utf-8", newline="") as f:
    checks = list(csv.DictReader(f))
checks = [r for r in checks if not r["check"].startswith("EEA cross-check")]
attard = next(r for r in rows if r["station"] == "Attard" and r["year"] == 2024)
checks.extend([
    {"check": "EEA cross-check station-years available", "value": len(available),
     "formula_or_method": "count of station-years with at least one valid EEA daily aggregate",
     "source": "EEA E1a validated PM2.5 Parquet files; URLs and SHA-256 in eea_station_file_manifest.csv",
     "retrieved_date": DATE},
    {"check": "EEA cross-check values matching PQ to 0.1 µg/m³", "value": matches,
     "formula_or_method": "round EEA mean of valid daily aggregates to one decimal and compare with annex",
     "source": "EEA E1a validated PM2.5 Parquet files and PQ 29696 annex",
     "retrieved_date": DATE},
    {"check": "Attard 2024 EEA minus PQ annex", "value": f"{float(attard['eea_mean_of_valid_daily_aggregates_ug_m3']) - float(attard['pq_annex_ug_m3']):.6f}",
     "formula_or_method": "EEA mean of valid daily aggregates minus PQ annex value (µg/m³)",
     "source": "EEA E1a validated data; Attard 2024; PQ 29696 annex",
     "retrieved_date": DATE},
])
with checks_path.open("w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["check", "value", "formula_or_method", "source", "retrieved_date"], lineterminator="\n")
    writer.writeheader()
    writer.writerows(checks)
print(f"EEA has {len(available)} station-year means for 2020–2024; {matches}/{len(available)} match the PQ annex to 0.1 µg/m³.")
for row in available:
    print(row["station"], row["year"], row["eea_mean_of_valid_daily_aggregates_ug_m3"],
          row["eea_valid_days"], f"{row['eea_day_coverage_pct']}%", row["pq_annex_ug_m3"], row["comparison"])
