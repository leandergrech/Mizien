"""Reproduce the interim tree-pledge arithmetic without implying linear progress."""
from datetime import date
from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "data/cc-010/government_counts.csv"
DATES = ROOT / "data/cc-010/dates.csv"
OUTPUT = ROOT / "data/cc-010/checks.csv"

with INPUT.open(newline="", encoding="utf-8") as f:
    rows = {r["measure"]: r for r in csv.DictReader(f)}

with DATES.open(newline="", encoding="utf-8") as f:
    dates = {r["event"]: date.fromisoformat(r["date"]) for r in csv.DictReader(f)}

pledge = int(rows["Manifesto pledge"]["value"])
planted = int(rows["Government trees planted"]["value"])
party_count = int(rows["Labour 2026 manifesto trees planted"]["value"])
percent = planted / pledge * 100
party_percent = party_count / pledge * 100
remaining = pledge - planted

# Share of the five-year window ("fil-hames snin li gejjin") elapsed, counted from the 2022 general election.
start = dates["2022 general election"]
end = start.replace(year=start.year + 5)
window = (end - start).days
elapsed_count = (dates["Latest cumulative count date"] - start).days / window * 100
elapsed_election = (dates["2026 general election (snap)"] - start).days / window * 100

with OUTPUT.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["check", "value", "unit", "source", "note"])
    writer.writerow(["Approximate share of 2022 pledge reported planted by end-2025", f"{percent:.0f}", "%", "Manifesto pledge 305; Parliament PQ 34270", "Approximate count divided by pledge; not a final outcome and not a linear forecast."])
    writer.writerow(["Approximate tree count still to reach pledge", remaining, "trees", "Manifesto pledge 305; Parliament PQ 34270", "Arithmetic difference only; Parliament says around 60000 planted by end-2025; no later cumulative count located."])
    writer.writerow(["Share of pledge in Labour's own 2026 manifesto count (more than 57,000 trees, 2022-2025)", f"{party_percent:.0f}", "%", "Labour 2026 manifesto item 43", "Lower bound ('more than'); the party's figure is lower than the Minister's ~60,000."])
    writer.writerow(["Share of five-year window elapsed by end-2025", f"{elapsed_count:.1f}", "%", "Election dates: IFES ElectionGuide", f"{start} to {dates['Latest cumulative count date']} of {start} to {end} ({window} days)."])
    writer.writerow(["Share of five-year window elapsed at the 30 May 2026 general election", f"{elapsed_election:.1f}", "%", "Election dates: IFES ElectionGuide", "The legislature for which the 2022 manifesto was written ended with this snap election."])

print(f"Approximate end-2025 progress: {percent:.0f}% ({planted:,} / {pledge:,} trees)")
print(f"Approximate arithmetic balance: {remaining:,} trees; not a claim of final shortfall.")
print(f"Labour 2026 manifesto count: >{party_count:,} trees = >{party_percent:.0f}% of the pledge")
print(f"Five-year window elapsed by end-2025: {elapsed_count:.1f}%; at the 30 May 2026 election: {elapsed_election:.1f}%")
