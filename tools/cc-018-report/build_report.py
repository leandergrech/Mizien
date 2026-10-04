"""Claim Check 018 report. Run fetch_data.py, calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []
LG = colors.HexColor("#8DB36B")

# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("In February 2026 the Malta Developers Association (MDA) welcomed the IMF’s annual assessment of Malta, saying: "
        "<b>“The IMF’s assessment of the Maltese housing market confirms what the MDA has been saying for several "
        "years.”</b> MaltaToday summarised the statement as the IMF confirming the “strength and stability” of the "
        "property sector. We read the IMF report in full and tested its housing findings against Eurostat data.", lead)]
S.append(key_points([
    ("The IMF does say the market is sound.",
     "House prices “remained aligned with fundamentals”, price-to-income and price-to-rent ratios “have been "
     "stable”, and the likelihood of a weakening is “currently low”."),
    ("Independent data agree.",
     "Eurostat’s standardised price-to-income ratio for Malta fell 10.7% between 2015 and 2024 and stands below its "
     "long-term average (92.9, EU 98.9). Incomes have kept pace with prices."),
    ("The IMF also flagged risks the statement leaves out.",
     "Banks’ exposure to real estate (72% of private loans, up from 61%) is called “a vulnerability”; the IMF Board "
     "urged vigilance and staff asked for closer monitoring “in view of rapid house price growth”."),
    ("Stability is not affordability.",
     "The IMF assessed valuation and financial stability. The share of people overburdened by housing costs rose from "
     "1.1% to 6.0% between 2015 and 2025, which the report does not address."),
    ("Verdict: largely supported (moderate confidence).",
     "On strength and stability the IMF and Eurostat back the statement; the omitted risks are caveats rather than a "
     "contradiction. The MDA’s own release was not found, so the wording is as quoted by MaltaToday."),
]))
S += [Spacer(1, 4 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("−10.7%", GREEN, "Malta house price-to-income ratio, 2015–2024 (Eurostat)"),
             ("92.9", GREEN, "Ratio vs its long-term average (100), 2024"),
             ("72%", ORANGE, "Bank private loans tied to real estate and construction (IMF)"),
             ("6.0%", RED, "People overburdened by housing costs, 2025 (1.1% in 2015)")]),
      Spacer(1, 4 * mm),
      up_down("The MDA’s release showing it referred only to valuation and financial stability, with the IMF’s risk "
              "warnings acknowledged.",
              "Evidence that the IMF found overvaluation or instability, or a reading of the statement as a claim about "
              "affordability."),
      Spacer(1, 5 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the IMF report says"),
          ("4", "What the data show"), ("5", "Where the evidence points different ways"),
          ("6", "Testing the claim"), ("7", "Verdict and requests for evidence"), ("8", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("MaltaToday reported the statement on 8 February 2026 [1], quoting the association in direct speech. We did "
           "not find the MDA’s own release. The IMF report it refers to is the 2025 Article IV consultation, published "
           "as Country Report 26/29 [2], which we read in full."))
S.append(std_table([
    [C("What was said", cellh), C("Who", cellh), C("Access", cellh)],
    [C("“The IMF’s assessment of the Maltese housing market confirms what the MDA has been saying for several years.”"),
     C("MDA statement, quoted [1]"), C("Read in full")],
    [C("The assessment confirms the “strength and stability” of the property sector"), C("MaltaToday summary [1]"),
     C("Read in full")],
    [C("MDA-commissioned study: prices +59% since 2017; price-to-income 14.0 → 14.5 (2024–25)"),
     C("MaltaToday [1] ◆"), C("Study not seen")],
], [104 * mm, 38 * mm, 28 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("SCOPE NOTE", tag),
               P("This check asks whether the IMF report supports the statement. It does not assess whether more "
                 "building is desirable (see Claim Check 013 on permits and prices) or the environmental cost of "
                 "development.", small)], bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Question.</b> Does the IMF’s 2025 assessment confirm that Malta’s property sector is strong and stable, "
           "and does independent data agree?"))
S.append(P("<b>Evidence.</b> The IMF report, with page references [2]; Eurostat’s standardised house price-to-income "
           "ratio [3]; Eurostat real house prices and housing-cost overburden [4]. Numbers are recomputed by "
           "<i>tools/cc-018-report/calc.py</i>."))
S.append(P("<b>Grades.</b> Official assessments and statistics are grade C. ◆ marks a source known second-hand."))

# ================================================================== 3
S.append(CondPageBreak(80 * mm))
S.append(SectionHeading(3, "What the IMF report says"))
S.append(std_table([
    [C("IMF wording (PDF page)", cellh), C("Supports the statement?", cellh)],
    [C("House prices “remained aligned with fundamentals and price-to-income and price-to-rent ratios have been "
       "stable” (p.19)"), C("Yes")],
    [C("“The likelihood of weakening of property and housing markets is currently low, it is a prospective risk” "
       "(p.12)"), C("Yes, with a caveat")],
    [C("Prices +6.7% in 2024; growth moderated in early 2025 “while the house price-to-income ratio remained stable” "
       "(p.11)"), C("Yes")],
    [C("“Significant exposures of banks to real estate are a vulnerability”: 72% of private loans, from 61% (p.19)"),
     C("Omitted risk")],
    [C("“In view of rapid house price growth, staff recommend enhanced monitoring” (p.20)"), C("Omitted risk")],
    [C("Directors “urged vigilance on vulnerabilities from rising exposures to real estate” (p.3)"), C("Omitted risk")],
    [C("Population density fifteen times the EU’s, “straining infrastructure, housing and public services” (p.8)"),
     C("Context")],
], [130 * mm, 40 * mm]))

# ================================================================== 4
S.append(CondPageBreak(150 * mm))
S.append(SectionHeading(4, "What the data show"))
S.append(fig(FIG / "fig1_price_income.png"))
S.append(P("Figure 1. Left: Malta’s house price-to-income ratio fell below its long-term average after 2020, while the "
           "EU’s rose and then fell back. Right: the share of people overburdened by housing costs rose in Malta.", cap))
S.append(fig(FIG / "fig2_bank_exposure.png"))
S.append(P("Figure 2. Banks’ lending tied to property, about 2015 and mid-2025 [2].", cap))
S.append(std_table([
    [C("Indicator", cellh), C("Malta", cellh), C("EU-27", cellh), C("Source", cellh), C("Grade", cellh)],
    [C("Price-to-income ratio, change 2015–2024"), C("<b>−10.7%</b>"), C("+5.7%"), C("Eurostat tipsho60 [3]"), grade_tag("C")],
    [C("Price-to-income vs long-term average, 2024"), C("92.9"), C("98.9"), C("Eurostat tipsho60 [3]"), grade_tag("C")],
    [C("Real house prices 2015–2025"), C("+34%"), C("+25%"), C("Eurostat tipsho10 [4]"), grade_tag("C")],
    [C("Housing-cost overburden, 2015 → 2025"), C("1.1% → 6.0%"), C("11.2% → 7.7%"), C("Eurostat ilc_lvho07a [4]"), grade_tag("C")],
    [C("Real estate share of bank private loans"), C("61% → 72%"), C("–"), C("IMF [2]"), grade_tag("C")],
], [62 * mm, 30 * mm, 30 * mm, 36 * mm, 12 * mm]))
S.append(P("All values in <i>data/cc-018/checks.csv</i>.", cap))

# ================================================================== 5
S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(5, "Where the evidence points different ways"))
S.append(contested(
    "Q1  Is the market strong and stable?", "YES, ON VALUATION", GREENC,
    "The IMF finds prices in line with fundamentals and ratios stable; Eurostat’s price-to-income ratio fell 10.7% "
    "since 2015 and is below its long-term average.",
    "The IMF calls weakening a “prospective risk” and wants closer monitoring because prices are rising fast.",
    "<b>For this claim:</b> the core of the statement matches the report."))
S.append(contested(
    "Q2  Does the report confirm everything the MDA has said?", "NOT SHOWN", AMBER,
    "The MDA has long argued that prices reflect demand and incomes; the IMF and Eurostat agree on that.",
    "The MDA’s own commissioned study, as reported, said prices outpaced incomes and the price-to-income ratio was "
    "rising, the opposite of the IMF and Eurostat finding. The IMF also warns about banks’ exposure to property.",
    "<b>For this claim:</b> “what the MDA has been saying” is broad; the IMF confirms part of it."))
S.append(contested(
    "Q3  Is the market working for residents?", "OUTSIDE THE IMF’S SCOPE", GREY,
    "Overcrowding and overburden remain below the EU average (Claim Check 013).",
    "Overburden rose fivefold since 2015 and the IMF notes housing is strained by population density.",
    "<b>For this claim:</b> stability for banks and investors is not the same as affordability."))

# ================================================================== 6
S.append(CondPageBreak(100 * mm))
S.append(SectionHeading(6, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> The IMF found the housing market sound (no overvaluation, stable ratios)"),
     C("Stated in the report [2]; confirmed by Eurostat [3]."), verd("SUPPORTED", GREENC)],
    [C("<b>B.</b> The assessment confirms the sector’s “strength and stability”"),
     C("Yes on valuation; the IMF also lists bank exposure as a vulnerability."), verd("LARGELY SUPPORTED", LG)],
    [C("<b>C.</b> It confirms what the MDA has said for years"),
     C("Partly; the MDA’s own study pointed the other way on price-to-income."), verd("PARTLY", AMBER)],
], [52 * mm, 88 * mm, 30 * mm], valign="MIDDLE"))

# ================================================================== 7
S += [Spacer(1, 6 * mm), SectionHeading(7, "Verdict and requests for evidence"),
      verdict_box("Largely supported", "The IMF and Eurostat back the strength and stability claim; the statement "
                  "leaves out the IMF’s warnings on bank exposure. Confidence: moderate."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) The IMF report says what the MDA says it says about valuation and stability. (2) Eurostat’s "
           "independent ratio agrees. (3) The statement does not mention the IMF’s concern about banks’ growing "
           "exposure to property or its call for closer monitoring, and the IMF did not assess affordability. These "
           "omissions qualify the claim without reversing it."))
S.append(P("<b>Confidence is moderate</b> because the MDA’s own release was not found and the statement is known "
           "through a news report."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "The MDA’s statement of 8 February 2026 in full.",
    "The MDA-commissioned study (November 2025) and how its price-to-income ratio is defined.",
]))

# ================================================================== 8
S += [Spacer(1, 6 * mm), SectionHeading(8, "Limitations")]
for l in ["The MDA wording is as quoted in MaltaToday ◆.",
          "Eurostat’s price-to-income ratio uses national-accounts income per head; it can differ from wage-based "
          "measures such as the MDA study’s.",
          "National averages hide differences between first-time buyers, renters and owners."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Zammit J. (8 Feb 2026). Malta Development Association welcomes IMF assessment of housing market. "
          "<i>MaltaToday</i>.",
     "https://www.maltatoday.com.mt/news/national/139634/malta_development_association_welcomes_imf_assessment_housing_market"),
    ("2", "International Monetary Fund (2026). Malta: 2025 Article IV Consultation. IMF Country Report No. 26/29.",
     "https://www.imf.org/-/media/files/publications/cr/2026/english/1mltea2026001-source-pdf.pdf"),
    ("3", "Eurostat. tipsho60, standardised house price-to-income ratio; retrieved 4 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/tipsho60/default/table"),
    ("4", "Eurostat. tipsho10 (real house prices), ilc_lvho07a (housing-cost overburden); retrieved 3 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/"),
    ("5", "MiŻien. Data and calculations: data/cc-018/; tools/cc-018-report/.", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "4 Oct 2026", "First issue. Right of reply to the MDA not yet sent.")])

build_report(Report(
    number="018", out=str(FIG / "report.pdf"), kicker="Housing and planning",
    title_lines=["Did the IMF", "confirm the", "developers?"],
    subtitle_lines=["Testing a developers’ claim about the IMF’s view of Malta’s housing market",
                    "against the IMF report and Eurostat"],
    quote_lines=["“The IMF’s assessment of the Maltese housing", "market confirms what the MDA has been",
                 "saying for several years.”"], quote_size=15,
    attribution="Malta Developers Association, statement quoted by MaltaToday, 8 February 2026.",
    context="On the IMF’s 2025 Article IV consultation with Malta.",
    verdict="Largely supported", verdict_note="Sound on valuation; the IMF’s warnings on bank exposure are omitted",
    footer_lines=["Version 1.0  ·  4 October 2026", "Status: draft (right of reply: MDA)",
                  "Prepared from the IMF report and Eurostat data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="The IMF and the developers – Malta", version="1.0", date="4 October 2026",
    pdf_title="Did the IMF confirm the developers? Claim Check 018",
    pdf_subject="Tests the MDA's claim that the IMF's assessment confirms what it has been saying about housing",
    story=S))
