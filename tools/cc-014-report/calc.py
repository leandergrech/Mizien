#!/usr/bin/env python3
"""CC-014: test the enforcement-notice claim with formulas, not by eye.

Inputs (data/cc-014/):
  pa_enforcement_series.csv      notices and complaints by year: MEPA annual reports 2004-2011 (read 3 Oct 2026),
                                 PA annual reports 2017-2023 (read 5 Oct 2026 as Issuu page images) and 2024 (read 3 Oct 2026)
  pa_annual_reports_2017_2023.csv every value read in the PA reports 2017-2023, with printed page, image URL and SHA-256
Output: data/cc-014/checks.csv (and outcomes by year, used by figures.py, in outcomes_by_year.csv)
"""
import csv, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-014"
S = {int(r["year"]): r for r in csv.DictReader(open(D / "pa_enforcement_series.csv", encoding="utf-8"))}
N = {y: int(r["enforcement_notices"]) for y, r in S.items() if r["enforcement_notices"]}
K = {y: int(r["complaints"]) for y, r in S.items() if r["complaints"]}
PA = {}
for r in csv.DictReader(open(D / "pa_annual_reports_2017_2023.csv", encoding="utf-8")):
    if r["value"]:
        PA[(int(r["year"]), r["measure"])] = float(r["value"])

# The series must carry exactly the values read in the PA reports (guards against transcription drift).
for y in range(2017, 2024):
    assert N[y] == PA[(y, "notices_issued")], (y, "notices")
    assert K[y] == PA[(y, "complaints_received")], (y, "complaints")

rows = []


def add(check, value, unit, source, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": source, "note": note})


def pct(a, b):
    return round(100 * (a / b - 1))


MEPA, PA24, PAR = "MEPA annual reports 2004-2011", "PA Annual Report 2024", "PA annual reports 2017-2023"
early = [N[y] for y in range(2001, 2010) if y in N]
add("Years 2001-2009 with over 1,000 notices", sum(n > 1000 for n in early), "of " + str(len(early)), MEPA,
    ", ".join(f"{y}: {N[y]}" for y in range(2001, 2010) if y in N))
m_early = sum(early) / len(early)
add("Mean notices a year, 2001-2009", round(m_early), "notices", MEPA)
late = [N[y] for y in range(2020, 2025)]
m_late = sum(late) / len(late)
add("Mean notices a year, 2020-2024", round(m_late), "notices", "PA annual reports 2020-2024",
    ", ".join(f"{y}: {N[y]}" for y in range(2020, 2025)))
add("Change in notices, 2001-09 mean to 2020-24 mean", round(100 * (m_late / m_early - 1)), "%", "calculated")
add("Notices a year, range 2018-2024", f"{min(N[y] for y in range(2018, 2025))}-{max(N[y] for y in range(2018, 2025))}",
    "notices", "PA annual reports 2018-2024", "2017: 315")
add("Change in notices, 2011 to 2017", pct(N[2017], N[2011]), "%", "MEPA AR 2011; PA AR 2017",
    f"{N[2011]} -> {N[2017]}; this fall lies in the 2012-2016 gap")
add("Change in complaints, 2005 (FY 2004/05) to 2024", pct(K[2024], K[2005]), "%",
    "MEPA AR 2005; " + PA24, f"{K[2005]} -> {K[2024]}")
add("Change in complaints, 2009 to 2024", pct(K[2024], K[2009]), "%", "MEPA AR 2009; " + PA24, f"{K[2009]} -> {K[2024]}")
add("Change in complaints, 2017 to 2024", pct(K[2024], K[2017]), "%", "PA AR 2017; " + PA24,
    f"{K[2017]} (rounded in report) -> {K[2024]}")
add("Change in complaints, 2018 to 2024", pct(K[2024], K[2018]), "%", "PA AR 2018; " + PA24, f"{K[2018]} -> {K[2024]}")
add("Change in complaints, 2011 to 2020", pct(K[2020], K[2011]), "%", "MEPA AR 2011; PA AR 2020",
    f"{K[2011]} -> {K[2020]}")
pa_k = [K[y] for y in range(2017, 2025)]
add("Mean complaints a year, 2017-2024", round(sum(pa_k) / len(pa_k)), "complaints", "PA annual reports 2017-2024",
    ", ".join(f"{y}: {K[y]}" for y in range(2017, 2025)))
top = max(K, key=K.get)
add("Most complaints in the series", K[top], "complaints", S[top]["source"][:60],
    f"{top}" + (" (FY 2004/05)" if top == 2005 else ""))
top2 = max((y for y in K if y != top), key=K.get)
add("Most complaints after that year", K[top2], "complaints", S[top2]["source"][:60], f"{top2}")
add("Complaints, 2020 minus 2019", K[2020] - K[2019], "complaints", "PA AR 2019, p. 17; PA AR 2020, p. 27",
    "the 2020 report itself says 139 more, which implies 3,174 for 2019")
ratio = {}
for y in sorted(K):
    if y in N:
        ratio[y] = 100 * N[y] / K[y]
        add(f"Notices per 100 complaints, {y}", round(ratio[y], 1), "per 100", S[y]["source"][:60])
mepa_r = [ratio[y] for y in ratio if y <= 2011]
pa_r = [ratio[y] for y in ratio if y >= 2017]
add("Notices per 100 complaints, range 2005-2011", f"{min(mepa_r):.0f}-{max(mepa_r):.0f}", "per 100", MEPA)
add("Notices per 100 complaints, range 2017-2024", f"{min(pa_r):.0f}-{max(pa_r):.0f}", "per 100", PAR + "; " + PA24)
add("Mean notices per 100 complaints, MEPA years / PA years", round((sum(mepa_r) / len(mepa_r)) / (sum(pa_r) / len(pa_r)), 1),
    "times", "calculated", f"{sum(mepa_r) / len(mepa_r):.1f} vs {sum(pa_r) / len(pa_r):.1f}")

# Outcomes of complaints confirmed as illegal development, 2018-2024
# confirmed = stated share x complaints received (the PA's bases differ; see notes.md)
OUT = []
for y in range(2018, 2024):
    share = PA[(y, "confirmed_share")] / 100
    conf = share * K[y]
    sanc = PA[(y, "sanctioning_applications")]
    note = PA[(y, "notices_from_complaints")]
    if (y, "removed_by_contravener") in PA:
        rem, rem_how = PA[(y, "removed_by_contravener")], "read"
    elif (y, "removed_by_contravener_share") in PA:
        rem, rem_how = PA[(y, "removed_by_contravener_share")] / 100 * conf, "derived from stated % of confirmed"
    else:  # 2018: 'in relation to the rest of the cases' the contraveners removed the works
        rem, rem_how = conf - sanc - note, "derived as the remainder of confirmed cases"
    OUT.append({"year": y, "complaints": K[y], "confirmed_share": round(100 * share), "confirmed": round(conf),
                "sanctioning": round(sanc), "removed": round(rem), "removed_how": rem_how, "persuasion": 0,
                "notice": round(note), "source": f"PA Annual Report {y}"})
conf24 = 0.5 * K[2024]
OUT.append({"year": 2024, "complaints": K[2024], "confirmed_share": 50, "confirmed": round(conf24), "sanctioning": 521,
            "removed": 482, "removed_how": "read", "persuasion": 87, "notice": 162, "source": PA24 + ", pp. 28-30"})
with open(D / "outcomes_by_year.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(OUT[0]))
    w.writeheader()
    w.writerows(OUT)
O = {o["year"]: o for o in OUT}
for o in OUT:
    tot = o["sanctioning"] + o["removed"] + o["persuasion"] + o["notice"]
    add(f"Confirmed illegal cases, {o['year']} ({o['confirmed_share']}% of {o['complaints']:,} complaints)",
        o["confirmed"], "cases", o["source"],
        f"outcomes: {o['sanctioning']} sanctioning, {o['removed']} removed ({o['removed_how']}), "
        + (f"{o['persuasion']} persuasion, " if o["persuasion"] else "") + f"{o['notice']} notice; sum {tot}")
    add(f"  notices per 100 confirmed cases, {o['year']}", round(100 * o["notice"] / o["confirmed"], 1), "per 100",
        o["source"])
nr = [100 * o["notice"] / o["confirmed"] for o in OUT]
add("Notices per 100 confirmed cases, range 2018-2024", f"{min(nr):.0f}-{max(nr):.0f}", "per 100", PAR + "; " + PA24,
    "confirmed = stated share x complaints received")
ns = [100 * o["notice"] / (o["sanctioning"] + o["removed"] + o["persuasion"] + o["notice"]) for o in OUT]
add("Notices per 100 reported outcomes, range 2018-2024", f"{min(ns):.0f}-{max(ns):.0f}", "per 100",
    PAR + "; " + PA24, ", ".join(f"{o['year']}: {v:.1f}" for o, v in zip(OUT, ns)))
add("Sum of reported outcomes, 2019", 737 + 824 + 141, "cases", "PA AR 2019, p. 17",
    "51% of 3,134 received is 1,598; 1,702 is 51% of the 3,340 closed")
outcomes24 = 521 + 482 + 87 + 162
add("Sum of the four 2024 outcome categories", outcomes24, "cases", PA24,
    "more than 'circa half' (1,206); categories may overlap or the confirmed share may be nearer 52%")
add("Sum of the four 2024 outcome categories, share of complaints", round(100 * outcomes24 / K[2024], 1), "%", PA24)
add("Sum of 2023 outcomes, share of complaints", round(100 * (497 + 508 + 185) / K[2023], 1), "%",
    "PA AR 2023, p. 23", "stated confirmed share circa 58%")
add("Sanctioning applications plus removals per notice, 2024", round((521 + 482) / 162, 1), "times", PA24,
    "(521 + 482) / 162")
add("Sanctioning applications plus removals per notice, 2023", round((497 + 508) / 185, 1), "times",
    "PA AR 2023, p. 23", "(497 + 508) / 185")
add("Sanctioning applications plus removals per notice, 2019", round((737 + 824) / 141, 1), "times",
    "PA AR 2019, p. 17", "(737 + 824) / 141")
add("Share of confirmed illegal cases ending in a sanctioning application, 2024", round(100 * 521 / conf24), "%", PA24,
    "denominator 'circa half' (1,206); an application, not a granted permit")
add("Change in confirmed illegal cases, 2020 to 2024", pct(conf24, O[2020]["confirmed"]), "%", "calculated",
    "2024 = 'circa half'; approximate")
add("Change in confirmed illegal cases, 2020 to 2024 (2024 = sum of outcomes)", pct(outcomes24, O[2020]["confirmed"]),
    "%", "calculated", "2024 = 1,252; approximate")
add("Change in confirmed illegal cases, 2021 to 2024", pct(conf24, O[2021]["confirmed"]), "%", "calculated",
    f"{O[2021]['confirmed']} -> {round(conf24)}")
add("Change in confirmed illegal cases, 2018 to 2024", pct(conf24, O[2018]["confirmed"]), "%", "calculated",
    f"{O[2018]['confirmed']} -> {round(conf24)} (2018 and 2024 both 'about half')")
add("Change in confirmed illegal cases, 2018 to 2024 (2024 = sum of outcomes)", pct(outcomes24, O[2018]["confirmed"]),
    "%", "calculated", f"{O[2018]['confirmed']} -> {outcomes24}")
peak = max(OUT, key=lambda o: o["confirmed"])
add("Most confirmed illegal cases, 2018-2024", peak["confirmed"], "cases", "calculated", str(peak["year"]))

# Deterrence: share of notices carrying daily fines (as stated in each report)
add("Notices subject to daily fines, 2018 -> 2023", f"{PA[(2018, 'notices_daily_fine_share')]:.0f} -> "
    f"{PA[(2023, 'notices_daily_fine_share')]:.0f}", "%", PAR,
    ", ".join(f"{y}: {PA[(y, 'notices_daily_fine_share')]:.0f}" for y in range(2018, 2024)))
add("Year daily fines were introduced", int(PA[(2023, "daily_fines_introduced")]), "year", "PA AR 2023, p. 24")

# Backlog arithmetic behind 'more than 90 years'
for y in (2018, 2019, 2020):
    add(f"Pending stop and enforcement notices, end {y}", int(PA[(y, "pending_notices_end_year")]), "notices",
        f"PA AR {y}", "stated as 'almost'" if y != 2019 else "stated as 'almost 6,119'")
add("Pending notices, end 2021", 5382, "notices", "PA data to The Malta Independent, 31 Jan 2022 (second-hand)")
da = {y: int(PA[(y, "notices_closed_direct_action")]) for y in range(2017, 2021)}
add("Notices closed by PA direct action, 2017-2020", sum(da.values()), "notices", PAR,
    ", ".join(f"{y}: {v}" for y, v in da.items()))
m_da = sum(da.values()) / len(da)
add("Mean notices closed by direct action a year, 2017-2020", round(m_da), "notices", "calculated")
add("Years to clear 5,382 at the 2020 direct-action rate", round(5382 / da[2020]), "years", "calculated")
add("Years to clear 5,382 at the 2017-2020 mean direct-action rate", round(5382 / m_da), "years", "calculated",
    "consistent with 'more than 90 years' if ~55-60 a year")
add("Direct actions a year implied by '1,500 in 30 years'", 50, "a year", "calculated", "1,500 / 30")

with open(D / "checks.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
for r in rows:
    print(f"{r['check']:72s} {str(r['value']):>9} {r['unit']:10s} {r['note']}")
