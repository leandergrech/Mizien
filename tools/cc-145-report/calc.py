"""Claim Check 145: WBRU 2025 licences against BirdLife's '10,000 hunters'. Output: data/cc-145/checks.csv"""
import csv
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data/cc-145"
SRC = "WBRU, Game Reporting Data - 2025 Report, pp. 1-2 (data/cc-145/wbru_2025_licences.csv)"
rows = {r["category"]: r for r in csv.DictReader(open(D / "wbru_2025_licences.csv"))}
land = rows["General Licence for Hunting birds on land"]
L, rep = int(land["licences"]), int(land["licensees_reporting"])
out = [
    ("General licences to hunt birds on land, 2025", L, "licences", SRC, "one per licensee in this category"),
    ("Above 10,000?", "yes" if L > 10000 else "no", "", SRC, f"margin {L - 10000}"),
    ("Land licensees who filed any game report in 2025", rep, "licensees", SRC, ""),
    ("Share of land licensees who filed any report", round(100 * rep / L, 1), "%", SRC, "WBRU gives 6.3"),
    ("Individuals filing any report, all categories", 1265, "people", SRC, "5,924 reports in total"),
    ("Specimens reported per land licensee", round(int(land["specimens"]) / L, 2), "birds per licence", SRC,
     "reports are required only when game is bagged"),
]
with open(D / "checks.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["check", "value", "unit", "source", "note"])
    w.writerows(out)
for o in out:
    print(o[0], o[1], o[4])
