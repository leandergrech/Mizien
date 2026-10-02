#!/usr/bin/env python3
"""Recalculate the arithmetic in ERA's Comino tree-intervention summary."""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "cc-002"
records = list(csv.DictReader((DATA / "interventions.csv").open(encoding="utf-8", newline="")))
values = {r["category"]: int(r["count"]) for r in records}
source = "ERA Comino clarification, 11 Aug 2026; retrieved 3 Oct 2026"

checks = [
    ("Removal total: 624 non-protected + 54 protected", values["non-protected specimens to be removed"] + values["protected trees to be removed"], "specimens", source, "Matches ERA's stated 678 total."),
    ("Non-protected share of removals", 100 * values["non-protected specimens to be removed"] / values["trees and shrubs to be removed"], "%", source, "92.04%, rounded by ERA to 92%."),
    ("New indigenous trees per protected tree removed", values["indigenous trees required for removed protected trees"] / values["protected trees to be removed"], "trees per tree", source, "540 / 54 = 10."),
    ("Protected share of planned transplants", 100 * values["protected trees among transplants"] / values["trees to be transplanted"], "%", "ERA Clarification on Comino, 7 Aug 2026; retrieved 3 Oct 2026", "341 of 348, i.e. 97.99%; seven are non-protected."),
]

with (DATA / "checks.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["check", "value", "unit", "source", "note"])
    for label, value, unit, src, note in checks:
        w.writerow([label, f"{value:.2f}" if isinstance(value, float) else value, unit, src, note])

for label, value, unit, _, note in checks:
    print(f"{label}: {value:.2f} {unit}" if isinstance(value, float) else f"{label}: {value} {unit}")
    print(f"  {note}")
