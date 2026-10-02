#!/usr/bin/env python3
"""Recompute 2026 hunting quotas against the mortality benchmarks in L.N. 80/81."""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INPUTS = [
    ("Common Quail", 241638, 2416, 2400, "L.N. 80/2026, reg. 4"),
    ("European Turtle-dove", 251032, 2510, 1500, "L.N. 81/2026, reg. 4"),
]

out = ROOT / "data/cc-006/checks.csv"
out.parent.mkdir(parents=True, exist_ok=True)
with out.open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["species", "annual_mortality", "statutory_1pct_benchmark", "quota", "quota_pct_mortality",
                "quota_pct_benchmark", "source", "retrieved_date", "formula"])
    for species, mortality, benchmark, quota, source in INPUTS:
        w.writerow([species, mortality, benchmark, quota, f"{quota / mortality * 100:.6f}",
                    f"{quota / benchmark * 100:.6f}", source, "2026-10-02",
                    "quota / annual_mortality * 100; quota / statutory_1pct_benchmark * 100"])
        print(f"{species}: {quota / mortality:.3%} of modeled annual mortality; "
              f"{quota / benchmark:.1%} of the statutory 1% benchmark")
print(f"Wrote {out.relative_to(ROOT)}")
