"""Claim Check 150: '412 million kg diverted from landfill over five years' against NSO municipal waste tables.
Output: data/cc-150/checks.csv and five_year.csv"""
import csv
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data/cc-150"
rows = {r["series"]: {int(k): float(v) for k, v in r.items() if k.isdigit()} for r in csv.DictReader(open(D / "nso_municipal_waste.csv"))}
YRS = [2020, 2021, 2022, 2023, 2024]
SRC = "NSO, Municipal Waste: 2024 (NR 225/2025), Tables 1, 2 and 4 (data/cc-150/nso_municipal_waste.csv)"
CLAIM = 412000


def s(keys):
    return {y: sum(rows[k][y] for k in keys) for y in rows["landfill"]}


sep = s(["generated_paper_cardboard", "generated_metals", "generated_glass", "generated_mixed_packaging", "collected_organic"])
recovered = s(["recycling_material", "composting_digestion", "energy_recovery", "preparing_for_reuse", "incineration"])
not_landfilled = {y: rows["generated_total"][y] - rows["landfill"][y] for y in rows["landfill"]}
avoided_vs_2019 = {y: rows["landfill"][2019] - rows["landfill"][y] for y in rows["landfill"]}
with open(D / "five_year.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["year", "separately_collected_recyclables_and_organic", "recovered_or_recycled", "generated_minus_landfilled",
                "landfill", "landfill_below_2019"])
    for y in sorted(rows["landfill"]):
        w.writerow([y, round(sep[y]), round(recovered[y]), round(not_landfilled[y]), round(rows["landfill"][y]),
                    round(avoided_vs_2019[y])])
tot = lambda d: round(sum(d[y] for y in YRS))
out = [
    ("Claim: diverted from landfill over five years", CLAIM, "tonnes", "Minister Dalli, PR260072EN, 19 Jan 2026", "412 million kg"),
    ("Separately collected paper, metals, glass, mixed packaging and organic, 2020-2024", tot(sep), "tonnes", SRC,
     f"{100 * tot(sep) / CLAIM:.0f}% of the claim; gross collection, before rejects"),
    ("Municipal waste recycled, recovered or reused, 2020-2024", tot(recovered), "tonnes", SRC,
     f"{100 * tot(recovered) / CLAIM:.0f}% of the claim"),
    ("Municipal waste generated minus landfilled, 2020-2024", tot(not_landfilled), "tonnes", SRC,
     f"{100 * tot(not_landfilled) / CLAIM:.0f}% of the claim; includes treatment losses"),
    ("Landfill below the 2019 level, summed 2020-2024", tot(avoided_vs_2019), "tonnes", SRC,
     f"{100 * tot(avoided_vs_2019) / CLAIM:.0f}% of the claim; 2019 is the peak year"),
    ("Municipal waste landfilled 2024", round(rows["landfill"][2024]), "tonnes", SRC,
     f"share of generated {100 * rows['landfill'][2024] / rows['generated_total'][2024]:.0f}%"),
    ("Municipal waste landfilled 2020", round(rows["landfill"][2020]), "tonnes", SRC, ""),
    ("Organic waste collected 2024", round(rows["collected_organic"][2024]), "tonnes", SRC, "Minister: 30 million kg in 2025"),
]
with open(D / "checks.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["check", "value", "unit", "source", "note"])
    w.writerows(out)
for o in out:
    print(o[0], o[1], o[4])
for y in sorted(rows["landfill"]):
    print(y, round(sep[y]), round(recovered[y]), round(not_landfilled[y]))
