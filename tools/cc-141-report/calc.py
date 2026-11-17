"""Claim Check 141: Malta's rank among EU-27 total fertility rates. Output: data/cc-141/checks.csv and ranks.csv"""
import csv
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data/cc-141"
SRC = "Eurostat demo_find, TOTFERRT (updated 13 Nov 2026, retrieved 17 Nov 2026)"
rows = list(csv.DictReader(open(D / "eurostat_demo_find_tfr.csv")))
by = {}
for r in rows:
    if r["tfr"] and r["geo"] != "EU27_2020":
        by.setdefault(r["year"], {})[r["geo"]] = float(r["tfr"])
ranks = []
for y in sorted(by):
    v = by[y]
    if len(v) < 27:
        continue
    order = sorted(v, key=lambda g: v[g])
    ranks.append((y, order.index("MT") + 1, v["MT"], order[0], v[order[0]], order[1], v[order[1]],
                  round(v[order[1]] - v["MT"], 2) if order[0] == "MT" else ""))
with open(D / "ranks.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["year", "malta_rank_from_lowest", "malta_tfr", "lowest", "lowest_tfr", "second", "second_tfr",
                "gap_to_second"])
    w.writerows(ranks)
lowest_years = [r[0] for r in ranks if r[1] == 1]
first = lowest_years[0]
streak = [y for y in lowest_years if int(y) >= int(first)]
last = ranks[-1]
out = [
    ("Malta total fertility rate, latest year", last[2], "live births per woman", SRC, f"year {last[0]}"),
    ("Malta rank among EU-27, latest year (1 = lowest)", last[1], "rank", SRC, f"year {last[0]}"),
    ("Second-lowest Member State, latest year", last[6], "live births per woman", SRC, f"{last[5]}, year {last[0]}"),
    ("Gap between Malta and the second-lowest, latest year", last[7], "live births per woman", SRC, ""),
    ("First year with all 27 values in which Malta is lowest", first, "year", SRC, ""),
    ("Years Malta is lowest, from that year to the latest", f"{len(streak)} of {int(last[0]) - int(first) + 1}", "years",
     SRC, ", ".join(streak)),
    ("EU-27 total fertility rate 2024 (Statistics Explained)", 1.34, "live births per woman",
     "Eurostat, Fertility statistics (Statistics Explained, data extracted 19 Feb 2026)",
     "API value for EU27_2020 2022-2024 flagged not for publication"),
    ("Pre-Budget Document: Malta 2024", 1.01, "live births per woman", "Pre-Budget Document 2027, p. 97", "matches Eurostat"),
]
with open(D / "checks.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["check", "value", "unit", "source", "note"])
    w.writerows(out)
for r in ranks:
    print(r)
for o in out:
    print(o[0], o[1], o[4])
