"""Claim Check 138: counts from the park instruments table. Output: data/cc-138/checks.csv"""
import csv
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data/cc-138"
rows = list(csv.DictReader(open(D / "park_instruments.csv", encoding="utf-8")))
SRC = "Full texts on legislation.mt, read 17 Nov 2026 (data/cc-138/park_instruments.csv)"
out = []
for park in ("white_rocks", "cirkewwa", "majjistral"):
    n = sum(r[park] == "yes" for r in rows)
    out.append((f"{park}: provisions present of {len(rows)} listed", n, "provisions", SRC, ""))
restrict = ["Lists prohibited or restricted activities", "Restricts works or installations inside the park",
            "Prohibits building or development in terms"]
wr = [r for r in rows if r["provision"] in restrict and r["white_rocks"] == "yes"]
out.append(("White Rocks: provisions that restrict any activity or works", len(wr), "provisions", SRC,
            "L.N. 209/2026 has five regulations: title and purpose, definitions, establishment, savings for existing "
            "uses and permits, savings for other law"))
out.append(("White Rocks: regulations in L.N. 209/2026", 5, "regulations", "L.N. 209 of 2026 (Gazette 21,695, 31 Jul 2026)", ""))
mention = 0  # 'Project Green' searched in the extracted text of L.N. 209/2026: no match
out.append(("White Rocks: mentions of Project Green or any manager in L.N. 209/2026", mention, "mentions",
            "L.N. 209 of 2026, text searched", ""))
with open(D / "checks.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["check", "value", "unit", "source", "note"])
    w.writerows(out)
for r in out:
    print(r[0], r[1])
