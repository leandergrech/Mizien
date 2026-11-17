"""Claim Check 149: annual approved new dwellings from NSO quarterly tables. Output: data/cc-149/checks.csv, annual.csv"""
import csv
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data/cc-149"
q = list(csv.DictReader(open(D / "nso_new_dwellings_quarterly.csv")))
ann = {}
for r in q:
    ann.setdefault(int(r["year"]), []).append(int(r["new_dwellings"]))
annual = {y: sum(v) for y, v in ann.items() if len(v) == 4}
sh = {int(r["year"]): int(r["new_dwellings"]) for r in csv.DictReader(open(D / "annual_second_hand.csv"))}
with open(D / "annual.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["year", "new_dwellings", "basis"])
    for y in sorted(set(annual) | set(sh)):
        w.writerow([y, annual.get(y, sh.get(y)), "NSO quarterly tables" if y in annual else "press reports of NSO (second-hand)"])
SRC = "NSO Q4 news releases, Table 1 (data/cc-149/nso_new_dwellings_quarterly.csv)"
pct = 100 * (annual[2025] / annual[2024] - 1)
allyears = {**sh, **annual}
higher = sorted([y for y, v in allyears.items() if v > annual[2025]])
out = [
    ("Approved new dwellings 2025 (sum of quarters)", annual[2025], "dwellings", SRC, "NSO salient point: 12,325"),
    ("Approved new dwellings 2024 (sum of quarters)", annual[2024], "dwellings", SRC, ""),
    ("Change 2024 to 2025", round(pct, 1), "%", SRC, "MaltaToday: 41%"),
    ("Approved new dwellings 2023", annual[2023], "dwellings", SRC, ""),
    ("Approved new dwellings 2022", annual[2022], "dwellings", SRC, ""),
    ("Years above 2025 among those on file", ", ".join(map(str, higher)), "years",
     SRC + "; 2018-2019 second-hand (data/cc-149/annual_second_hand.csv)", "2007-2017 and 2020-2021 not on file"),
]
with open(D / "checks.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["check", "value", "unit", "source", "note"])
    w.writerows(out)
for o in out:
    print(o[0], o[1])
