"""Claim Check 149 report. Run calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("On 27 July 2026 MaltaToday reported, under the headline “Building mad: 12,325 new dwellings approved in "
        "2025”: <b>“Approved residential units reached 12,325 in 2025, the third-highest annual total ever, while "
        "approvals on ODZ land more than doubled to a record 226 units.”</b> It also said the total was 41% above "
        "2024. We rebuilt the annual totals from the National Statistics Office’s quarterly tables.", lead)]
S.append(key_points([
    ("12,325 is right.",
     "The NSO’s four quarterly figures for 2025 (2,143, 3,027, 3,668 and 3,487) add up to 12,325 approved new dwellings, "
     "the figure in its annual summary."),
    ("So is +41%.",
     "The 2024 quarters add up to 8,716. The rise to 12,325 is 41.4%."),
    ("“Third-highest ever” is consistent with what we could find.",
     "Press reports of NSO figures put 2018 at 12,885 and 2019 at 12,485, both higher. 2022–2024 were lower. NSO releases "
     "before 2022 are no longer online, so 2018–2019 are second-hand and earlier years were not checked."),
    ("The ODZ record of 226 could not be checked.",
     "It comes from Planning Authority data, not the NSO, and the Authority’s site blocks automated access."),
    ("Verdict: largely supported (moderate confidence).",
     "The two headline numbers check out exactly against official tables. The ranking and the ODZ record rest on data "
     "we could not read first-hand."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("12,325", GREEN, "approved new dwellings in 2025: sum of the NSO’s quarterly tables"),
             ("+41.4%", GREEN, "on 2024 (8,716), from the same tables"),
             ("2 years", AMBER, "higher on record: 2018 and 2019 (press reports of NSO figures)"),
             ("226", GREY, "ODZ units: Planning Authority data, not read")]),
      Spacer(1, 4 * mm),
      up_down("The Planning Authority’s 2007–2025 dataset showing 226 ODZ units in 2025 as the highest, and NSO "
              "annual totals for 2007–2021 confirming only 2018 and 2019 were higher.",
              "Any year other than 2018 and 2019 above 12,325, or an ODZ count for an earlier year above 226."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "The annual totals"),
          ("4", "Testing the claim"), ("5", "Verdict"), ("6", "Limitations")])
S.append(PageBreak())

S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The article is by James Debono, dated 27 July 2026 [1]. It credits “figures published by the Planning "
           "Authority” and draws on a dataset running from 2007 to 2025 that splits approvals into ODZ, greenfield and "
           "brownfield units and conversions. The NSO publishes approved new dwellings each quarter, using Planning "
           "Authority permits as its source [2, 3]. We read the article from the maintainer’s browser copy, and the NSO "
           "pages and tables in a browser (nso.gov.mt refuses scripts)."))
S.append(std_table([
    [C("Source", cellh), C("What it says", cellh), C("Our access", cellh), C("Status", cellh)],
    [C("<b>MaltaToday</b>, 27 Jul 2026 [1]"),
     C("12,325 in 2025, +41%, third-highest; 226 ODZ units, a record."), C("Maintainer’s copy, read in full."),
     C("<b>The claim</b>")],
    [C("<b>NSO</b>, Economy – Residential Building Permits [2]"), C("2,213 permits and 12,325 new dwellings in 2025."),
     C("Maintainer’s copy."), C("<b>Primary</b>")],
    [C("<b>NSO</b>, Q4 releases 2022–2025 [3–6]"), C("Approved new dwellings by quarter (Table 1)."),
     C("xlsx tables read in a browser, 17 Nov 2026."), C("<b>Primary data</b>")],
    [C("<b>Press reports</b> of NSO 2018–2019 figures [7, 8]"), C("2018: 12,885; 2019: 12,485."),
     C("Search results and articles."), C("<b>Second-hand</b>")],
], [38 * mm, 66 * mm, 40 * mm, 26 * mm]))

S += [Spacer(1, 4 * mm), SectionHeading(2, "Method")]
S.append(P("We copied the quarterly totals from Table 1 of each Q4 release into "
           "<i>data/cc-149/nso_new_dwellings_quarterly.csv</i> and summed them by year in "
           "<i>tools/cc-149-report/calc.py</i> (outputs <i>annual.csv</i> and <i>checks.csv</i>). The NSO’s current website "
           "holds releases from 2022 onwards. For 2018 and 2019 we used press reports of the NSO’s figures, marked "
           "second-hand. NSO statistics are grade C. <b>Verdicts</b> follow the five-point scale in Appendix A."))

S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(3, "The annual totals"))
S.append(fig(FIG / "fig1_annual.png", width=CW * 0.98))
S.append(P("Figure 1. Approved new dwellings per year. Hatched: second-hand.", cap))
S.append(P("The 2025 quarters sum to 12,325, the total in the NSO’s annual summary [2], and the 2024 quarters to 8,716, "
           "so the rise is 41.4%. The second half of 2025 was the strongest: 3,668 approvals in Q3 and 3,487 in Q4, 54% "
           "above Q4 2024 [3]. These are permits approved, not homes built. Some permits lapse or are revised, and the "
           "NSO counts the dwellings in each approved permit."))
S.append(P("For the ranking, press reports of NSO figures give 12,885 for 2018 and 12,485 for 2019 [7, 8]. One "
           "MaltaToday article gives 12,855 for 2018. Either way both years are above 2025, which makes 2025 third, as "
           "MaltaToday says, unless another year is higher. We could not read the NSO totals for 2007–2017 or 2020–2021. "
           "MaltaToday’s own sums make a higher year unlikely. The 2007–2015 approvals total 43,912, an average of about "
           "4,900 a year. Of the 96,194 approved in 2016–2025, the six years we have account for 64,046, leaving an "
           "average of about 8,000 for each of the other four [1]."))
S.append(P("The ODZ figure is a different matter. The NSO tables have no ODZ breakdown. MaltaToday says 226 ODZ units "
           "were approved in 2025, up from 104 in 2024 and the highest “since at least 2007”, mostly farmhouse "
           "redevelopment and conversions. That needs the Planning Authority’s dataset, which we could not open."))

S.append(CondPageBreak(70 * mm))
S.append(SectionHeading(4, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> 12,325 new dwellings approved in 2025"), C("MaltaToday [1]"),
     C("Sum of NSO quarters, and the NSO’s annual figure."), verd("ACCURATE", GREENC)],
    [C("<b>B.</b> A 41% increase over 2024"), C("MaltaToday [1]"),
     C("8,716 in 2024; +41.4%."), verd("ACCURATE", GREENC)],
    [C("<b>C.</b> The third-highest annual total ever"), C("MaltaToday [1]"),
     C("2018 and 2019 higher (second-hand); 2022–2024 lower; other years not read."), verd("CONSISTENT", AMBER)],
    [C("<b>D.</b> A record 226 dwellings approved ODZ"), C("MaltaToday [1]"),
     C("Planning Authority data; not in NSO tables; not read."), verd("NOT CHECKED", GREY)],
], [42 * mm, 26 * mm, 68 * mm, 34 * mm], valign="MIDDLE"))

S += [Spacer(1, 6 * mm), SectionHeading(5, "Verdict"),
      verdict_box("Largely supported", "12,325 and +41% match the NSO exactly; the ranking is consistent with second-hand "
                  "figures; the ODZ record was not checked. Confidence: moderate."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> The article’s main numbers are right. The ranking fits every figure we could find. The ODZ "
           "record is specific and sourced to the Planning Authority, but we could not see the data, so it stays "
           "unchecked rather than wrong. <b>What this verdict does not say.</b> It does not judge whether 12,325 "
           "approvals are too many, and it does not assess any permit."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list(["From the Planning Authority: the 2007–2025 series of approved dwelling units by ODZ, greenfield "
                        "and brownfield, as used by MaltaToday.",
                        "From the NSO: the annual totals of approved new dwellings for 2007–2021."]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag),
               P("Not needed for this verdict (maintainer rule of 5 October 2026).", small)], bg=AMBER_PALE, bar=AMBER)]
S += [Spacer(1, 6 * mm), SectionHeading(6, "Limitations")]
for l in ["2018 and 2019 are second-hand, and two press reports differ by 30 units for 2018.",
          "Planning Authority and NSO counts may differ slightly; MaltaToday uses the Authority’s dataset.",
          "Approvals are not completions. Some approved dwellings are never built."]:
    S.append(P("• " + l, bul))
S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Debono, J. Building mad: 12,325 new dwellings approved in 2025. MaltaToday, 27 July 2026 (maintainer copy).",
     "https://www.maltatoday.com.mt/news/national/143438/building_mad_12325_new_dwellings_approved_in_2025"),
    ("2", "NSO. Economy – Residential Building Permits (last updated 10 April 2026; maintainer copy).",
     "https://nso.gov.mt/economy-residential-building-permits/"),
    ("3", "NSO. Residential Building Permits: Q4/2025, NR 026/2026, 19 February 2026, Table 1.",
     "https://nso.gov.mt/residential-building-permits-q4-2025/"),
    ("4", "NSO. Residential Building Permits: Q4/2024, NR 028/2025, Table 1.",
     "https://nso.gov.mt/wp-content/uploads/NR-028-2025-Table1.xlsx"),
    ("5", "NSO. Residential Building Permits: Q4/2023, NR 033/2024, Table 1.",
     "https://nso.gov.mt/wp-content/uploads/NR-2024-033-T1.xlsx"),
    ("6", "NSO. Residential Building Permits: Q4/2022, NR 028/2023, Table 1.",
     "https://nso.gov.mt/residential-building-permits-q4-2022/"),
    ("7", "MaltaToday. Over 12,400 building permits make 2019 another booming year for construction (NSO figures; "
          "second-hand).", "https://www.maltatoday.com.mt/environment/planning/101532/over_12400_building_permits_make_2019_another_booming_year_for_construction"),
    ("8", "MaltaToday. Planning Authority approved 26 new dwellings a day in 2022, NSO figures show (second-hand for "
          "2018).", "https://www.maltatoday.com.mt/news/national/121416/planning_authority_approved_26_new_dwellings_a_day_in_2022_nso_figures_show"),
    ("9", "MiŻien. Data and script: data/cc-149/; tools/cc-149-report/calc.py.", ""),
])
S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "17 Nov 2026", "First issue. Verdict Largely supported (moderate confidence); no right of "
                    "reply needed.")])

build_report(Report(
    number="149", out=str(FIG / "report.pdf"), kicker="Planning and housing",
    title_lines=["Building", "mad?"],
    subtitle_lines=["Testing MaltaToday’s figures for", "dwellings approved in 2025"],
    quote_lines=["“Approved residential units reached 12,325", "in 2025, the third-highest annual total ever…”"],
    quote_size=13.5,
    attribution="MaltaToday (James Debono), 27 July 2026.",
    context="Also: approvals on ODZ land more than doubled to a record 226 units.",
    verdict="Largely supported", verdict_note="12,325 and +41% exact; ODZ record not checked",
    footer_lines=["Version 1.0  ·  17 November 2026", "Status: no right of reply needed",
                  "Prepared from public sources and open data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Dwellings approved in 2025 – MaltaToday, July 2026", version="1.0", date="17 November 2026",
    pdf_title="Building mad? Claim Check 149",
    pdf_subject="Tests MaltaToday's figures for new dwellings approved in Malta in 2025",
    story=S))
