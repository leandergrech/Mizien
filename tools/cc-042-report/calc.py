"""Claim Check 042: EEA classification of Malta's bathing waters, 2023-2025, and Fajtata (A07) by year.
Reads data/cc-005/ (EEA DiscoMap + DiscoData, retrieved 5 Oct 2026); writes data/cc-042/eea_mt_classification.csv
and prints the figures used in the report."""
import csv
import pathlib
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[2]
sites = list(csv.DictReader(open(ROOT / "data/cc-005/mt_site_classes.csv")))
seasons = {r["season"]: r for r in csv.DictReader(open(ROOT / "data/cc-005/eea_bwd_mt_seasons.csv"))}
a07 = next(r for r in sites if r["site"] == "A07")
rows = []
for y in range(2015, 2026):
    c = Counter(r[str(y)] for r in sites)
    n = sum(c.values())
    rows.append({"season": y, "sites": n, "excellent": c["Excellent"], "good": c["Good"], "sufficient": c["Sufficient"],
                 "poor": c["Poor"], "excellent_pct": round(100 * c["Excellent"] / n, 1), "fajtata_A07": a07[str(y)],
                 "short_term_pollution_samples": seasons.get(str(y), {}).get("short_term_pollution", ""),
                 "source": "EEA DiscoMap BathingWater_Dyna_WM_2025 layer 3 (via data/cc-005), retrieved 2026-10-05"})
with open(ROOT / "data/cc-042/eea_mt_classification.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
for r in rows:
    print(r)
print("Fajtata", a07["name"], a07["bathingWaterIdentifier"])
changed = [(r["site"], r["name"], r["2024"], r["2025"]) for r in sites if r["2024"] != r["2025"]]
print(len(changed), "sites changed class 2024->2025")
for x in changed:
    print(x)
# Excellent share, all 2025: 77/87 = 88.5%; poor 0
