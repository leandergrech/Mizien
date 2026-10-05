#!/usr/bin/env python3
"""CC-014: test the enforcement-notice claim with formulas, not by eye.

Reads data/cc-014/pa_enforcement_series.csv (MEPA/PA annual reports and reports of them, read 3 Oct 2026; 2019
complaints from the PA Annual Report 2019, read 5 Oct 2026) and writes data/cc-014/checks.csv.
"""
import csv, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-014"
S = {int(r["year"]): r for r in csv.DictReader(open(D / "pa_enforcement_series.csv", encoding="utf-8"))}
N = {y: int(r["enforcement_notices"]) for y, r in S.items() if r["enforcement_notices"]}
K = {y: int(r["complaints"]) for y, r in S.items() if r["complaints"]}
rows = []


def add(check, value, unit, source, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": source, "note": note})


MEPA, PA24 = "MEPA annual reports 2004-2011", "PA Annual Report 2024"
early = [N[y] for y in range(2001, 2010) if y in N]
add("Years 2001-2009 with over 1,000 notices", sum(n > 1000 for n in early), "of " + str(len(early)), MEPA,
    ", ".join(f"{y}: {N[y]}" for y in range(2001, 2010) if y in N))
add("Mean notices a year, 2001-2009", round(sum(early) / len(early)), "notices", MEPA)
late = [N[y] for y in range(2020, 2025)]
add("Mean notices a year, 2020-2024", round(sum(late) / len(late)), "notices", "PA reports and PQ answers",
    ", ".join(f"{y}: {N[y]}" for y in range(2020, 2025)))
add("Change in notices, 2001-09 mean to 2020-24 mean",
    round(100 * (sum(late) / len(late) / (sum(early) / len(early)) - 1)), "%", "calculated")
add("Change in complaints, 2005 (FY 2004/05) to 2024", round(100 * (K[2024] / K[2005] - 1)), "%",
    "MEPA AR 2005; " + PA24, f"{K[2005]} -> {K[2024]}")
add("Change in complaints, 2009 to 2024", round(100 * (K[2024] / K[2009] - 1)), "%",
    "MEPA AR 2009; " + PA24, f"{K[2009]} -> {K[2024]}")
add("Change in complaints, 2011 to 2020", round(100 * (K[2020] / K[2011] - 1)), "%",
    "MEPA AR 2011; PA AR 2020 (second-hand)", f"{K[2011]} -> {K[2020]}")
top = max(K, key=K.get)
add("Most complaints in the series", K[top], "complaints", S[top]["source"][:60],
    f"{top}" + (" (FY 2004/05)" if top == 2005 else ""))
top2 = max((y for y in K if y != top), key=K.get)
add("Most complaints after that year", K[top2], "complaints", S[top2]["source"][:60], f"{top2}")
add("Complaints, 2020 minus 2019", K[2020] - K[2019], "complaints", "PA AR 2019 (read); PA AR 2020 (second-hand)",
    "MaltaToday reported 139 more, which implied 3,174 for 2019")
for y in sorted(K):
    if y in N:
        add(f"Notices per 100 complaints, {y}", round(100 * N[y] / K[y], 1), "per 100", S[y]["source"][:60])
# 2024 complaint outcomes (PA AR 2024, pp. 28-30)
confirmed = round(0.5 * K[2024])
add("Complaints confirmed as illegal development, 2024 (about half)", confirmed, "cases", PA24, "circa half of 2,411")
add("  of which: sanctioning application submitted", 521, "cases", PA24)
add("  of which: removed by contravener before action", 482, "cases", PA24)
add("  of which: resolved after persuasion, no notice", 87, "cases", PA24)
add("  of which: enforcement notice issued", 162, "cases", PA24)
outcomes = 521 + 482 + 87 + 162
add("Sum of the four 2024 outcome categories", outcomes, "cases", PA24,
    "more than 'circa half' (1,206); categories may overlap or the confirmed share may be nearer 52%")
add("Sum of the four 2024 outcome categories, share of complaints", round(100 * outcomes / K[2024], 1), "%", PA24)
add("Sanctioning applications plus removals per notice, 2024", round((521 + 482) / 162, 1), "times", PA24,
    "(521 + 482) / 162")
add("Share of confirmed illegal cases ending in a sanctioning application", round(100 * 521 / confirmed), "%", PA24,
    "denominator 'circa half' (1,206); an application, not a granted permit")
add("Share ending in a sanctioning application, denominator = sum of outcomes", round(100 * 521 / outcomes), "%",
    PA24, "denominator 1,252")
add("Confirmed illegal cases, 2020 (55% of complaints)", round(0.55 * K[2020]), "cases",
    "PA AR 2020 (second-hand)")
add("Change in confirmed illegal cases, 2020 to 2024", round(100 * (confirmed / (0.55 * K[2020]) - 1)), "%",
    "calculated", "2024 = 'circa half'; different confirmation shares; approximate")
add("Change in confirmed illegal cases, 2020 to 2024 (2024 = sum of outcomes)",
    round(100 * (outcomes / (0.55 * K[2020]) - 1)), "%", "calculated", "2024 = 1,252; approximate")
# Backlog arithmetic behind 'more than 90 years'
add("Pending notices, end 2021", 5382, "notices", "PA data to The Malta Independent, 31 Jan 2022")
add("Notices closed by PA direct action, 2020", 74, "notices", "PA AR 2020 (second-hand)")
add("Years to clear 5,382 at 2020 direct-action rate", round(5382 / 74), "years", "calculated",
    "consistent with 'more than 90 years' if ~55-60 a year")

with open(D / "checks.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
for r in rows:
    print(f"{r['check']:68s} {r['value']:>7} {r['unit']:10s} {r['note']}")
