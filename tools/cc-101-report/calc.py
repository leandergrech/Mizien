#!/usr/bin/env python3
"""CC-101: every number in the report, recomputed from data/cc-101/ (run fetch.py first) and CC-009's WISE file.

Inputs (each with its source URL and retrieval date):
  data/cc-101/eurostat_env_wat_abs.csv            Eurostat env_wat_abs, Malta, million m3, with flags
  data/cc-101/wise_2022_surface_water_bodies.csv  EEA WISE, Malta's WFD water bodies (2022 reporting)
  data/cc-101/wise_2022_significant_pressures.csv EEA WISE, significant pressures per body (2022 reporting)
  data/cc-101/legislation_mt_legal_notices_2024_2026.csv  titles of every Legal Notice 2024-2026 (legislation.mt)
  data/cc-101/document_facts.csv                  figures and dates transcribed from the documents read
  data/cc-101/wise_2022_groundwater_status.csv    EEA WISE, groundwater-body status (2022 reporting; legend 2 = Good, 3 = Poor)
  data/cc-101/legislation_mt_acts_2024_2026.csv   titles of every Act of 2024-2026 and mentions of groundwater/abstract/borehole in its text
  data/cc-101/legislation_mt_sl_titles.csv        titles of every S.L. under 549, 423, 545, 355 and 427 (legislation.mt)
Output: data/cc-101/checks.csv
"""
import csv
import datetime
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "data" / "cc-101"
rows = []


def add(check, value, unit, source, note=""):
    rows.append({"check": check, "value": value, "unit": unit, "source": source, "note": note})


def read(name, folder=D):
    return list(csv.DictReader(open(folder / name, encoding="utf-8")))


facts = {r["id"]: r for r in read("document_facts.csv")}
fv = lambda k: float(facts[k]["value"])
day = lambda k: datetime.date.fromisoformat(facts[k]["value"])

# ------------------------------------------------------------------ Eurostat: abstraction by source and sector
ES = "Eurostat env_wat_abs (updated 16 Sep 2026), retrieved " + read("eurostat_env_wat_abs.csv")[0]["retrieved"]
E = {(r["wat_src"], r["wat_proc"], int(r["year"])): (float(r["value"]), r["flag"]) for r in read("eurostat_env_wat_abs.csv")}
y = 2024
fsw, ffl = E[("FSW", "ABST", y)]
fgw, gfl = E[("FGW", "ABST", y)]
frw, rfl = E[("FRW", "ABST", y)]
flag = lambda f: f"flag '{f}'" if f else "no flag"
add("Fresh surface water abstraction, 2024", fsw, "million m3", ES, flag(ffl))
add("Fresh groundwater abstraction, 2024", fgw, "million m3", ES, flag(gfl))
add("Fresh surface and groundwater abstraction, 2024", frw, "million m3", ES, flag(rfl))
add("Surface + groundwater equals the total, 2024", round(fsw + fgw, 2) == frw, "check", "calculated")
add("Surface water share of freshwater abstraction, 2024", round(100 * fsw / frw, 1), "%", "calculated",
    "both inputs estimated (flag e)")
add("Groundwater share of freshwater abstraction, 2024", round(100 * fgw / frw, 1), "%", "calculated",
    "both inputs estimated (flag e); desalinated seawater is not freshwater abstraction")
fsw_years = {yy: E[("FSW", "ABST", yy)][0] for yy in range(2010, 2025) if ("FSW", "ABST", yy) in E}
add("Fresh surface water abstraction, distinct values 2010-2024",
    "; ".join(f"{v} ({min(k for k in fsw_years if fsw_years[k] == v)}-{max(k for k in fsw_years if fsw_years[k] == v)})"
              for v in sorted(set(fsw_years.values()))), "million m3", ES,
    "flat within each period: an estimate, not a metered series (our reading)")
for proc, lab in (("ABS_HH", "households"), ("ABS_AGR", "agriculture, forestry, fishing")):
    v, f = E[("FSW", proc, y)]
    add(f"Fresh surface water abstraction by {lab}, 2024", v, "million m3", ES, flag(f))
pws, pfl = E[("FGW", "ABS_PWS", y)]
agr, afl = E[("FGW", "ABS_AGR", y)]
add("Groundwater abstraction for public water supply, 2024", pws, "million m3", ES, flag(pfl))
add("Groundwater abstraction by agriculture, forestry, fishing, 2024", agr, "million m3", ES, flag(afl))
other = round(fgw - pws - agr, 2)
add("Groundwater abstraction by everyone else (households, industry, services, mining), 2024", other, "million m3",
    "calculated", "total minus public supply minus agriculture")
add("Share of groundwater abstraction outside the public water supply, 2024", round(100 * (fgw - pws) / fgw, 1), "%",
    "calculated", "Eurostat's 'public water supply' category taken as the Water Services Corporation (our identification, "
    "not Eurostat's); the Green Paper's proposed framework would exclude WSC sources")
add("Share of groundwater abstraction by agriculture, 2024", round(100 * agr / fgw, 1), "%", "calculated")
add("Eurostat flags on Malta's groundwater total, 2010-2024",
    ", ".join(f"{yy}:{E[('FGW', 'ABST', yy)][1]}" for yy in range(2010, 2025) if ("FGW", "ABST", yy) in E),
    "flags", ES, "e = estimated; b = break in series")

# ------------------------------------------------------------------ WISE: water bodies and abstraction pressures
WS = "EEA WISE WFD 2022 reporting, retrieved " + read("wise_2022_surface_water_bodies.csv")[0]["retrieved"]
swb = [r for r in read("wise_2022_surface_water_bodies.csv") if r["category"] != "territorialWaters"]
cnt = lambda cat: [r for r in swb if r["category"] == cat]
rivers, lakes = cnt("riverWaterBody"), cnt("lakeWaterBody")
add("Surface water bodies reported (excluding territorial waters)", len(swb), "bodies", WS,
    ", ".join(f"{c}: {len(cnt(c))}" for c in sorted({r['category'] for r in swb})))
add("River water bodies (watercourses)", len(rivers), "bodies", WS, "; ".join(f"{r['name']} {r['size']} {r['size_unit']}"
                                                                         for r in rivers))
add("Total length of river water bodies", round(sum(float(r["size"]) for r in rivers), 1), "km", WS)
add("Lake water bodies (pools)", len(lakes), "bodies", WS,
    "; ".join(f"{r['name']} {r['size']} {r['size_unit']}" for r in lakes))
add("Largest lake water body", max(float(r["size"]) for r in lakes), "km2", WS)
pr = read("wise_2022_significant_pressures.csv")
sw_p, gw_p = [r for r in pr if r["water"] == "surface"], [r for r in pr if r["water"] == "ground"]
fresh = [r for r in sw_p if r["category"] in ("RW", "LW")]
add("Surface water bodies with abstraction (P3) as a significant pressure", sum("P3" in r["significant_pressures"] for r in sw_p),
    f"of {len(sw_p)}", WS)
add("Inland fresh surface water bodies (rivers and lakes) with abstraction as a significant pressure",
    sum("P3" in r["significant_pressures"] for r in fresh), f"of {len(fresh)}", WS,
    "pressures reported for them: " + "; ".join(sorted({p for r in fresh for p in r["significant_pressures"].split(";")})))
p3 = [r for r in gw_p if "P3" in r["significant_pressures"]]
p6 = [r for r in gw_p if "P6-2" in r["significant_pressures"]]
add("Groundwater bodies with abstraction (P3) as a significant pressure", len(p3), f"of {len(gw_p)}", WS,
    "; ".join(f"{r['eu_code']} {r['name'].title()} ({'agriculture' if 'P3-1' in r['significant_pressures'] else 'public supply'})"
              for r in p3))
add("Groundwater bodies with alteration of water level or volume (P6-2) as a significant pressure", len(p6),
    f"of {len(gw_p)}", WS, ", ".join(r["eu_code"] for r in p6))
both = {r["eu_code"] for r in p3} | {r["eu_code"] for r in p6}
add("Groundwater bodies with P3 or P6-2", len(both), f"of {len(gw_p)}", "calculated", ", ".join(sorted(both)))
st = read("wise_2022_groundwater_status.csv")
poor_q = [r for r in st if r["quantitative_status"] == "Poor"]
add("Groundwater bodies in poor quantitative status (3rd cycle, assessed 2021)", len(poor_q), f"of {len(st)}",
    "EEA WISE WFD 2022 reporting (WFD2022_GroundWaterBody_WM layer 0), retrieved " + st[0]["retrieved"],
    ", ".join(r["eu_groundwater_body_code"] for r in poor_q))
add("Poor quantitative status bodies that also report abstraction or water-level pressure",
    sum(r["eu_groundwater_body_code"] in both for r in poor_q), f"of {len(poor_q)}", "calculated")

# ------------------------------------------------------------------ Registered sources (Green Paper 2023)
GP = "EWA and ERA, Green Paper on the Regulation of Groundwater Abstraction (Nov 2023)"
agri, comm, wsc = fv("gp_agri_boreholes"), fv("gp_commercial_boreholes"), fv("gp_wsc_boreholes")
add("Agricultural boreholes", int(agri), "boreholes", GP, "PDF p. 5")
add("Commercial boreholes (registered)", int(comm), "boreholes", GP, "PDF p. 5")
add("Agricultural plus commercial boreholes", int(agri + comm), "boreholes", "calculated",
    "domestic boreholes (pools, gardens) have no count in the Green Paper; spieri counted separately")
add("Registered low-yield sources (spieri), not metered", int(fv("gp_low_yield_registered")), "sources", GP, "PDF p. 7")
add("WSC boreholes", int(wsc), "boreholes", GP, "PDF p. 4; plus 12 pumping stations")
add("WSC share of the boreholes counted (agricultural + commercial + WSC)", round(100 * wsc / (agri + comm + wsc), 1), "%",
    "calculated")
add("Private abstraction by sector (agriculture / commercial / domestic)",
    f"{facts['gp_private_share_agriculture']['value']} / {facts['gp_private_share_commercial']['value']} / "
    f"{facts['gp_private_share_domestic']['value']}", "%", GP, "Figure 6; sums to "
    + str(int(fv('gp_private_share_agriculture') + fv('gp_private_share_commercial') + fv('gp_private_share_domestic'))))
add("Second-hand: registered commercial boreholes with no abstraction data", "more than 63", "%",
    "Amphora Media, Aug 2026, reporting ERA records (not seen by us)", "SECOND-HAND; not used for any rating")

# ------------------------------------------------------------------ Dates
lofn, gp_date = day("lofn_date"), day("green_paper_published")
reviewed = datetime.date(2026, 10, 6)
add("Years from the WFD transposition deadline to the letter of formal notice",
    round((lofn - day("wfd_transposition_deadline")).days / 365.25, 1), "years", "calculated", "22 Dec 2003 to 8 Jul 2026")
add("Years from the deadline for operational measures to the letter", round((lofn - day("wfd_measures_operational")).days / 365.25, 1),
    "years", "calculated", "22 Dec 2012 to 8 Jul 2026")
add("Years since the notification deadline for existing groundwater sources", round((reviewed - day("notification_deadline")).days / 365.25, 1),
    "years", "calculated", "20 Nov 2008 to 6 Oct 2026")
add("Months from the Green Paper to the letter of formal notice", round((lofn - gp_date).days / 30.44, 1), "months", "calculated")
add("Months from the Green Paper to this check", round((reviewed - gp_date).days / 30.44, 1), "months", "calculated")
add("Reply deadline (two months from the letter)", "2026-09-08", "date", "INF/26/1376: 'two months to respond'",
    "approximate: the date of receipt of the letter is not public")

# ------------------------------------------------------------------ legislation.mt: new instruments?
ln = read("legislation_mt_legal_notices_2024_2026.csv")
bad = [r for r in ln if not r["title_en"] or r["title_en"].startswith("ERROR")]
hits = [r for r in ln if r["matches_groundwater_or_abstraction"] == "True"]
add("Legal Notices 2024-2026 read (titles)", len(ln) - len(bad), f"of {len(ln)} in the ELI sitemap",
    "legislation.mt, retrieved " + ln[0]["retrieved"], ", ".join(f"{yy}: {sum(r['year'] == str(yy) for r in ln)}"
                                                               for yy in (2024, 2025, 2026)))
add("Titles matching groundwater, abstraction, borehole, water policy or well(s)", len(hits), "notices", "calculated",
    " | ".join(r["title_en"][:120] for r in hits) or "none")
add("What the matching notice does", "L.N. 374 of 2024", "instrument", "legislation.mt, read 6 Oct 2026",
    "adds to S.L. 549.165 reg. 6(2) a new exception to the drilling moratorium: boreholes by a public entity for research "
    "and development, with ERA's prior approval; no abstraction permit")

# ------------------------------------------------------------------ legislation.mt: Acts 2024-2026 and older S.L. titles
acts = [r for r in read("legislation_mt_acts_2024_2026.csv") if r["title_en"]]
listed = [r for r in acts if r["in_sitemap"] == "True"]
probed = [r for r in read("legislation_mt_acts_2024_2026.csv") if r["in_sitemap"] != "True"]
add("Acts 2024-2026 read (title and full text searched)", len(acts), "Acts",
    "legislation.mt ELI sitemap, retrieved " + acts[0]["retrieved"],
    ", ".join(f"{yy}: {sum(r['year'] == str(yy) for r in acts)}" for yy in (2024, 2025, 2026))
    + f"; {len(probed)} further numbers after the last listed one in each year probed: "
    f"{sum(bool(r['title_en']) for r in probed)} exist")
hit = [r for r in acts if any(int(r[k]) > 0 for k in ("text_mentions_groundwater", "text_mentions_abstract",
                                                      "text_mentions_borehole"))]
add("Acts 2024-2026 whose text mentions groundwater, abstract or borehole", len(hit), "Acts", "calculated",
    " | ".join(r["title_en"][:70] for r in hit) or "none")
sl = read("legislation_mt_sl_titles.csv")
add("S.L. titles read under 549, 423, 545, 355 and 427", len(sl), "instruments",
    "legislation.mt ELI sitemap, retrieved " + sl[0]["retrieved"], f"{sum(not r['title_en'] for r in sl)} without a title")
add("S.L. titles mentioning groundwater, abstraction, boreholes, wells, pumps or water-controlled areas",
    sum(r["matches_water_abstraction"] == "True" for r in sl), "instruments", "calculated",
    "; ".join(r["instrument"] for r in sl if r["matches_water_abstraction"] == "True"))
add("Malta's 2019 statement of private groundwater sources metered", "more than 3,000", "sources",
    facts["swd2019_metered_private_sources"]["source"] + ", " + facts["swd2019_metered_private_sources"]["page"],
    "Malta's clarification to the Commission, not a count by us; no current count found")

with open(D / "checks.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
for r in rows:
    print(f"{r['check'][:95]:95s} {r['value']!s:>14} {r['unit']}  {r['note'][:110]}")
