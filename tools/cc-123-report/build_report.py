"""Claim Check 123 report. Run calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []
LG = colors.HexColor("#8DB36B")
Q1 = ("According to data published by the NSO, a total of 8,716 residential units were granted approval in 2024, "
      "representing a 7.4% increase compared with 2023")
Q2 = ("Between January and June 2025, 5,170 permits were sanctioned, reflecting a significant year-on-year increase of 9.7%.")
Q3 = ("Should this upward trend persist in the latter half of the year, the total number of permits approved in 2025 is "
      "expected to surpass the levels recorded in 2024.")

# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("Section 2.1 of KPMG’s <i>Construction Industry and Property Market Report 2025</i>, prepared for the Malta "
        "Development Association (MDA), says: <b>“" + Q1 + "”</b> and that <b>“" + Q2 + "”</b> We checked the "
        "figures against the Planning Authority’s series of approved dwelling units, the National Statistics Office’s "
        "(NSO) quarterly releases and Eurostat. The figures reproduce. One word is loose: the 5,170 are dwelling "
        "units, not permits.", lead)]
S.append(key_points([
    ("8,716 units in 2024 reproduces.",
     "The Planning Authority’s series has 8,716 approved dwelling units for 2024 and 8,112 for 2023 (transcribed 3 Oct 2026)."),
    ("The 7.4% reproduces.",
     "8,716 / 8,112 is +7.45%. Eurostat’s index of dwellings permitted rises 7.3% (a narrower measure)."),
    ("The 5,170 and 9.7% reproduce, as units.",
     "The NSO’s quarters sum to 2,143 + 3,027 = 5,170 new dwellings (second-hand ◆), +9.7% on 4,714. The number of "
     "building permits was about 1,023 (+9.0%)."),
    ("The forecast came true, by a wide margin.",
     "KPMG expected 2025 to surpass 2024. The Planning Authority’s series has 12,325 units for 2025 (+41%); the NSO’s "
     "first three quarters alone were 8,838 ◆."),
    ("Verdict: largely supported (moderate confidence).",
     "Every number matches the data. The caveats are the word “permits” for units and that the NSO figures were "
     "read second-hand."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("8,716", GREEN, "Dwelling units approved in 2024: KPMG and the Planning Authority agree"),
             ("+7.4%", GREEN, "on 2023 (8,112): +7.45% from the Planning Authority series"),
             ("5,170", AMBER, "H1 2025: NSO dwelling units ◆, which KPMG calls “permits”"),
             ("12,325", GREEN, "units approved in 2025 (Planning Authority): the forecast was borne out")]),
      Spacer(1, 4 * mm),
      up_down("Nothing further is needed to support the figures; the verdict would reach Supported if the NSO release pages "
              "were read directly and KPMG used “dwelling units” for the January–June 2025 count.",
              "Evidence that the Planning Authority or NSO series has been revised so that 2024 or 2023 differ materially "
              "from the figures here, or that the 5,170 is not the NSO’s count."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the data show"),
          ("4", "Where the evidence points different ways"), ("5", "Testing the claim"),
          ("6", "Verdict and requests for evidence"), ("7", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The passage is in section 2.1, “Residential permits”, on PDF p. 37 of the report [1]. The report states that "
           "it was prepared for the Malta Development Association; footnote 19 says the permit data were “retrieved "
           "from NSO News releases and from the Central Bank of Malta Development Permits for Dwellings, by Type” [1]. "
           "We read section 2.1 and the surrounding page in full; the claim record named the speaker as KPMG, and the "
           "sentences are KPMG’s own."))
S.append(std_table([
    [C("What was said", cellh), C("Who", cellh), C("Access", cellh)],
    [C("“" + Q1 + "”"), C("KPMG, section 2.1 [1]"), C("Read in full (PDF p. 37)")],
    [C("“" + Q2 + "”"), C("KPMG, section 2.1 [1]"), C("Read in full (PDF p. 37)")],
    [C("“" + Q3 + "”"), C("KPMG, section 2.1 [1]"), C("Read in full (PDF p. 37)")],
], [100 * mm, 36 * mm, 34 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("SCOPE NOTE", tag),
               P("This check is about the four figures and the forecast in section 2.1: 8,716 units in 2024, +7.4% on "
                 "2023, 5,170 in January–June 2025 (+9.7%), and the expectation that 2025 exceeds 2024. It does not "
                 "assess the report’s other findings, the report’s Figure 2.1 (its values are not printed), or "
                 "whether so many approvals are desirable.", small)],
              bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Question.</b> Do official counts of approved dwellings match KPMG’s 2024 total, its two growth rates and "
           "its forecast, and does the report use “units” and “permits” consistently?"))
S.append(P("<b>Evidence.</b> (a) The Planning Authority’s Approved Dwelling Units series, 2022–2025, transcribed on 3 Oct "
           "2026 for Claim Check 013 (pa.org.mt returns 403 to scripts, so it was not re-read for this check) [2]. "
           "(b) The NSO’s quarterly <i>Residential Building Permits</i> releases for Q1 2023 to Q3 2025. nso.gov.mt "
           "also returns 403 to scripts, so these figures come from search-engine summaries of the releases and from one "
           "outlet article that we read in full (Business Now, on Q2 2025); they are second-hand (◆) [3]. "
           "(c) Eurostat’s sts_cobp_a, the index of dwellings in permitted residential buildings with two or more "
           "dwellings, Malta [4]. Every number is recomputed by <i>tools/cc-123-report/calc.py</i> from "
           "<i>data/cc-123/</i> and written to <i>data/cc-123/checks.csv</i>."))
S.append(P("<b>Grades.</b> Official statistics are grade C; KPMG’s report is a commissioned analysis of official statistics "
           "and is graded C. No peer-reviewed study is needed to count approvals. <b>Verdicts</b> follow the five-point "
           "scale in Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(100 * mm))
S.append(SectionHeading(3, "What the data show"))
S.append(P("<b>2024 and the 7.4%.</b> The Planning Authority’s series gives 8,112 approved dwelling units for 2023 and "
           "8,716 for 2024, the number KPMG prints [2]. The ratio is +7.45%, which rounds to the 7.4% KPMG prints. The "
           "NSO’s four quarterly releases give 8,112 for 2023 (the same total) and 8,717 for 2024, one more ◆ [3]. "
           "Eurostat’s index of dwellings permitted in buildings with two or more dwellings rises 7.3% from 2023 to "
           "2024 (108.9 to 116.9, 2021 = 100) [4]; it is a narrower measure and agrees in direction and size."))
S.append(fig(FIG / "fig1_annual.png"))
S.append(P("Figure 1. Approved dwelling units per year, Planning Authority. 2024 (+7.4% on 2023) follows a contraction "
           "from 2022; 2025 is far higher.", cap))
S.append(P("<b>January to June 2025.</b> The NSO’s Q1 2025 release reports 2,143 new dwellings (425 building permits) and "
           "Q2 2025 reports 3,027 (598 permits) ◆ [3]. The sum is 5,170, exactly KPMG’s number, so KPMG’s “5,170 permits "
           "were sanctioned” is the NSO’s count of <i>dwellings</i>. The same quarters of 2024 give 4,714 dwellings, and "
           "5,170 / 4,714 is +9.7%, matching KPMG’s rate. The count of building permits themselves is 1,023 (+9.0% on "
           "939), about five dwellings per permit. The report uses “units” for 2024 and “permits” for 2025 for the same "
           "quantity (Figure 2)."))
S.append(KeepTogether([fig(FIG / "fig2_quarters.png"),
                       P("Figure 2. NSO quarterly new dwellings approved (wide bars) and building permits (narrow bars). "
                         "The January–June 2025 dwelling units sum to the 5,170 that KPMG calls permits.", cap)]))
S.append(P("<b>The forecast.</b> KPMG expected the full-year 2025 total to surpass 2024 if first-half growth continued. "
           "The NSO’s first three quarters of 2025 sum to 8,838 dwellings ◆, already above the 8,716 of all of 2024, "
           "and the Planning Authority’s series gives 12,325 for 2025, +41% [2][3]. We have assumed that the 2025 entry of "
           "the Planning Authority’s series is a full year (Section 7). The forecast was cautious, not wrong."))
S.append(std_table([
    [C("Figure", cellh), C("Value", cellh), C("Source", cellh), C("Grade", cellh)],
    [C("Units approved 2023 / 2024"), C("<b>8,112 / 8,716</b>"), C("Planning Authority [2]"), grade_tag("C")],
    [C("Change 2024 on 2023"), C("<b>+7.45%</b> (KPMG: 7.4%); Eurostat index +7.3%"), C("Calculated [2][4]"),
     grade_tag("C")],
    [C("Dwellings approved, Jan–Jun 2024 / 2025 ◆"), C("4,714 / <b>5,170</b>; +9.7%"), C("NSO releases [3]"),
     grade_tag("C")],
    [C("Building permits (count), Jan–Jun 2024 / 2025 ◆"), C("939 / 1,023; +9.0%"), C("NSO releases [3]"),
     grade_tag("C")],
    [C("Units approved 2025"), C("<b>12,325</b> (+41% on 2024); Jan–Sep ◆ 8,838"), C("Planning Authority [2]; NSO [3]"),
     grade_tag("C")],
], [58 * mm, 52 * mm, 48 * mm, 12 * mm]))
S.append(P("All values in <i>data/cc-123/checks.csv</i>. ◆ = known only from search summaries of the NSO releases, not read "
           "on nso.gov.mt.", cap))

# ================================================================== 4
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(4, "Where the evidence points different ways"))
S.append(contested(
    "Q1  Are 8,716 units and +7.4% right, when other counts show permits falling?", "YES; DIFFERENT COUNTS", GREEN,
    "The Planning Authority’s series and the sum of the NSO’s quarters both give 8,112 for 2023 and 8,716–8,717 for 2024; "
    "Eurostat’s index rises 7.3% [2][3][4].",
    "MaltaToday, reporting parliamentary data, gave building permits falling from a 2018 peak of 2,868 to 1,749 in "
    "2024 (second-hand, from the claim record). That counts permits, not dwellings. The NSO’s permit counts sum to 1,750 "
    "for 2024 and 1,695 for 2023 (+3.2%) ◆ [3]; the dwellings they cover rose faster (+7.4%) because the average permit "
    "covered about five dwellings in 2024.",
    "<b>For this claim:</b> the two series do not conflict. KPMG’s sentence is about units, and units rose 7.4% while "
    "the number of permits rose about 3%."))
S.append(contested(
    "Q2  Are the 5,170 “permits” permits?", "NO, THEY ARE DWELLING UNITS", AMBER,
    "The NSO quarters sum to exactly 5,170 dwellings, and the growth rate is the 9.7% KPMG prints ◆ [3].",
    "The sentence calls them “permits”. The NSO’s count of building permits for January–June 2025 is about 1,023 ◆. "
    "The report’s footnote 19 cites NSO news releases and the Central Bank’s “Development Permits for Dwellings” as "
    "its sources [1].",
    "<b>For this claim:</b> the number and growth rate are right; the noun is loose. A reader taking “permits” "
    "literally would overstate the permit count about five-fold. We rate the figure as supported and note the label."))

# ================================================================== 5
S.append(CondPageBreak(90 * mm))
S.append(SectionHeading(5, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> 8,716 residential units were granted approval in 2024"),
     C("Planning Authority: 8,716 (2024). NSO quarters ◆: 8,717."), verd("SUPPORTED", GREENC)],
    [C("<b>B.</b> A 7.4% increase on 2023"),
     C("8,716 / 8,112 = +7.45%. Eurostat’s index of dwellings permitted: +7.3%."), verd("SUPPORTED", GREENC)],
    [C("<b>C.</b> 5,170 permits sanctioned January–June 2025, +9.7% on a year earlier"),
     C("NSO Q1 + Q2 2025 ◆ = 2,143 + 3,027 = 5,170 dwellings, +9.7% on 4,714. These are units; building permits "
       "were about 1,023."), verd("LARGELY SUPPORTED", LG)],
    [C("<b>D.</b> 2025 is expected to surpass 2024 if the trend persists"),
     C("Planning Authority: 12,325 units in 2025 vs 8,716; NSO Jan–Sep ◆ already 8,838."), verd("SUPPORTED", GREENC)],
], [52 * mm, 88 * mm, 30 * mm], valign="MIDDLE"))

# ================================================================== 6
S += [CondPageBreak(75 * mm), Spacer(1, 6 * mm), SectionHeading(6, "Verdict and requests for evidence"),
      verdict_box("Largely supported", "Every figure matches official counts; “permits” is used for dwelling units, and the "
                  "NSO quarters were read second-hand. Confidence: moderate."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) The 2024 total and the 7.4% come straight from the Planning Authority’s series, and the NSO’s "
           "quarters and Eurostat’s index agree. (2) The January–June 2025 figure and its 9.7% reproduce exactly from the "
           "NSO’s two quarters. (3) The forecast was borne out. (4) The one flaw is the noun “permits” for dwelling units, "
           "and the NSO quarters, though they reconcile with the Planning Authority’s totals, were not read on the NSO site. "
           "That is a minor caveat on the substance, which our scale calls <i>Largely supported</i>. Confidence is moderate "
           "because the January–June 2025 test rests on second-hand quarterly figures."))
S.append(P("<b>What this verdict does not say.</b> It does not say that this number of approvals is a good or bad thing, that "
           "approvals become completions, or anything about the report’s other findings. It says the figures in section "
           "2.1 match the official counts."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "The NSO’s Q1 and Q2 2025 release pages, read directly, to confirm 2,143 and 3,027 new dwellings.",
    "The Planning Authority’s file (pa.org.mt/file.aspx?f=37489) re-read in a browser, to confirm the 2025 entry is a full year.",
    "KPMG’s clarification of whether “permits” in section 2.1 means dwelling units.",
]))

# ================================================================== 7
S += [Spacer(1, 6 * mm), SectionHeading(7, "Limitations")]
for l in ["We read section 2.1 of a 124-page report, not the whole report; Figure 2.1’s values are not printed.",
          "nso.gov.mt (release pages) and pa.org.mt return 403 to scripts. The NSO quarterly figures come from web-search "
          "summaries of the releases, except Q2 2025, which we read in a Business Now article; they are second-hand (◆). "
          "They reconcile exactly with the Planning Authority totals for 2023 and, within one unit, for 2024.",
          "The Planning Authority series was transcribed on 3 Oct 2026 for Claim Check 013 and was not re-read here. We "
          "assume its 2025 entry is a full year; the NSO’s first three quarters (8,838 ◆) leave an implied fourth quarter "
          "of 3,487, which is plausible but not an NSO figure.",
          "The one-unit difference for 2024 (8,716 vs 8,717) is unexplained; it may be a revision.",
          "Eurostat’s sts_cobp_a covers permitted buildings with two or more dwellings only, so it corroborates the "
          "direction and size of change, not the level. The 2025 value carried no status flag in our extract.",
          "The MaltaToday permit counts (2,868 to 1,749) are quoted second-hand from the claim record and were not "
          "retrieved."]:
    S.append(P("• " + l, bul))

S += [CondPageBreak(60 * mm), Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "KPMG (Dec 2025). Construction Industry and Property Market Report 2025, for the Malta Development Association. "
          "124 pp. Section 2.1, PDF p. 37; read 16 Oct 2026.",
     "https://assets.kpmg.com/content/dam/kpmgsites/mt/pdf/2025/12/kpmg-mda-construction-industry-and-property-market-report-2025.pdf"),
    ("2", "Planning Authority (2026). Approved Dwelling Units 2007–2025; transcribed in data/cc-013 on 3 Oct 2026.",
     "https://www.pa.org.mt/file.aspx?f=37489"),
    ("3", "National Statistics Office Malta. Residential Building Permits, quarterly news releases, Q1 2023 to Q3 2025 ◆ "
          "(second-hand; Q2 2025 via Business Now, 21 Aug 2025).", "https://nso.gov.mt/economy-residential-building-permits/"),
    ("4", "Eurostat. sts_cobp_a: building permits, annual data, Malta, number of dwellings, residential buildings with 2+ "
          "dwellings; retrieved 16 Oct 2026.", "https://ec.europa.eu/eurostat/databrowser/view/sts_cobp_a/"),
    ("5", "MiŻien. Data and calculations: data/cc-123/; tools/cc-123-report/calc.py.", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "16 Oct 2026", "First issue. No right of reply needed (verdict Largely supported).")])

build_report(Report(
    number="123", out=str(FIG / "report.pdf"), kicker="Planning and housing",
    title_lines=["How many homes", "were approved?"],
    subtitle_lines=["Testing a KPMG report’s residential approval figures",
                    "against the Planning Authority, NSO and Eurostat"],
    quote_lines=["“…8,716 residential units were granted", "approval in 2024, representing a 7.4%", "increase compared with 2023.”"],
    quote_size=15,
    attribution="KPMG, Construction Industry and Property Market Report 2025, section 2.1.",
    context="Dec 2025; prepared for the Malta Development Association.",
    verdict="Largely supported", verdict_note="Figures match; “permits” are dwelling units",
    footer_lines=["Version 1.0  ·  16 October 2026", "Status: draft · no right of reply needed",
                  "Prepared from public sources, KPMG’s report and official statistics.",
                  "Repository: github.com/leandergrech/Mizien"],
    running_head="Residential approvals – Malta", version="1.0", date="16 October 2026",
    pdf_title="How many homes were approved? Claim Check 123",
    pdf_subject="Tests KPMG's residential approval figures against the Planning Authority, NSO and Eurostat",
    story=S))
