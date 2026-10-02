"""Recalculate CC-007 station summary metrics from the transcribed PQ 29696 annex."""
import csv
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DATA = ROOT / "data" / "cc-007"
rows = list(csv.DictReader((DATA / "station_pm25.csv").open(encoding="utf-8", newline="")))
values = [float(r["annual_pm25_ug_m3"]) for r in rows if r["annual_pm25_ug_m3"]]
missing = [r for r in rows if not r["annual_pm25_ug_m3"]]
assert len(rows) == 25, f"Expected five stations × five years, got {len(rows)}"
assert len(values) == 23 and len(missing) == 2, "Unexpected reported/missing observation count"

metrics = [
    ("Available station-years", len(values), "count of reported numeric observations", "Parliamentary Question 29696 annex"),
    ("Missing station-years", len(missing), "count of n/a observations", "Parliamentary Question 29696 annex"),
    ("Above WHO annual guideline", sum(v > 5 for v in values), "count(value > 5 µg/m³)", "WHO 2021 annual guideline 5 µg/m³; PQ 29696 values"),
    ("At or below historical EU annual limit", sum(v <= 25 for v in values), "count(value <= 25 µg/m³)", "Directive 2024/2881 Annex I Table 2; PQ 29696 values"),
    ("Above EU 2030 annual limit", sum(v > 10 for v in values), "count(value > 10 µg/m³)", "Directive 2024/2881 Annex I Table 1; contextual comparison only"),
    ("Minimum annual station value", min(values), "min(value)", "Parliamentary Question 29696 annex"),
    ("Maximum annual station value", max(values), "max(value)", "Parliamentary Question 29696 annex"),
]
for station in dict.fromkeys(r["station"] for r in rows):
    series = [float(r["annual_pm25_ug_m3"]) for r in rows
              if r["station"] == station and r["annual_pm25_ug_m3"]]
    metrics.append((f"Mean, {station}", sum(series) / len(series),
                    "arithmetic mean of reported annual station means; missing years excluded",
                    "Parliamentary Question 29696 annex"))

with (DATA / "checks.csv").open("w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["check", "value", "formula_or_method", "source", "retrieved_date"])
    writer.writerows((*metric, "2026-10-02") for metric in metrics)

print(f"{len(values)} reported values; {len(missing)} missing; range {min(values):.1f}–{max(values):.1f}; "
      f"{sum(v > 5 for v in values)} above WHO 5; {sum(v > 10 for v in values)} above EU 2030 10; "
      f"all {sum(v <= 25 for v in values)} at or below historical EU 25 µg/m³")
for station in dict.fromkeys(r["station"] for r in rows):
    metric = next(m for m in metrics if m[0] == f"Mean, {station}")
    print(f"{station}: {metric[1]:.2f} µg/m³")
