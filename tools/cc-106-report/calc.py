#!/usr/bin/env python3
"""CC-106: test "Malta's population is estimated to be around 1,600-1,800 pairs, constituting approximately 10% of the
global population" (BirdLife Malta). Reads data/cc-106/population_estimates.csv (sources read 5 Oct 2026; see
literature/CC-106/notes.md) and writes data/cc-106/checks.csv with Malta's share under each pair of estimates.
The widest range divides the lowest Malta estimate by the highest global one and the reverse; the central value
uses the midpoints."""
import csv, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-106"
E = list(csv.DictReader(open(D / "population_estimates.csv")))
mal = [e for e in E if e["scope"] == "Malta"]; glo = [e for e in E if e["scope"] == "Global"]
rows = []
for m in mal:
    ml, mh = float(m["low_pairs"]), float(m["high_pairs"])
    for g in glo:
        gl, gh = float(g["low_pairs"]), float(g["high_pairs"])
        rows.append({"malta": m["estimate"], "global": g["estimate"], "share_low_pct": round(100 * ml / gh, 1),
                     "share_mid_pct": round(100 * (ml + mh) / (gl + gh), 1), "share_high_pct": round(100 * mh / gl, 1),
                     "note": f"{ml:.0f}-{mh:.0f} pairs of {gl:.0f}-{gh:.0f}"})
with open(D / "checks.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for r in rows:
    print(f"{r['malta'][:34]:34s} / {r['global'][:24]:24s}  {r['share_low_pct']:>5}% - {r['share_high_pct']:>5}%  (central {r['share_mid_pct']}%)")
