"""Reproduce the interim tree-pledge arithmetic without implying linear progress."""
from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "data/cc-010/government_counts.csv"
OUTPUT = ROOT / "data/cc-010/checks.csv"

with INPUT.open(newline="", encoding="utf-8") as f:
    rows = {r["measure"]: r for r in csv.DictReader(f)}

pledge = int(rows["Manifesto pledge"]["value"])
planted = int(rows["Government trees planted"]["value"])
percent = planted / pledge * 100
remaining = pledge - planted

with OUTPUT.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["check", "value", "unit", "source", "note"])
    writer.writerow(["Approximate share of 2022 pledge reported planted by end-2025", f"{percent:.0f}", "%", "Manifesto pledge 305; Parliament PQ 34270", "Approximate count divided by pledge; not a final outcome and not a linear forecast."])
    writer.writerow(["Approximate tree count still to reach pledge", remaining, "trees", "Manifesto pledge 305; Parliament PQ 34270", "Arithmetic difference only; Parliament says around 60000 planted by end-2025 and the five-year period had not expired."])

print(f"Approximate end-2025 progress: {percent:.0f}% ({planted:,} / {pledge:,} trees)")
print(f"Approximate arithmetic balance: {remaining:,} trees; not a claim of final shortfall.")
