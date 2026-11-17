"""Claim Check 141 report. Run calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("In his foreword to the Pre-Budget Consultation Document 2027, published by the Ministry for Finance on 30 "
        "September 2026, the Minister for Finance, Clyde Caruana, wrote: <b>“Malta’s fertility rate is the lowest in the "
        "EU27, while an ageing population will continue to place pressure on pensions, healthcare and long-term care in "
        "the years ahead.”</b> We tested the first half, the ranking, against Eurostat’s fertility table for all 27 Member "
        "States.", lead)]
S.append(key_points([
    ("The ranking is right.",
     "In 2024, the latest year Eurostat has published, Malta’s total fertility rate was 1.01 live births per woman, the "
     "lowest in the EU. Spain (1.10) and Lithuania (1.11) were next."),
    ("It has been true for eight years running.",
     "Malta has had the EU’s lowest rate in every year from 2017 to 2024. Before 2017 it was never lowest; in 2016 it "
     "ranked fourth from the bottom."),
    ("The document’s own figures match.",
     "Its demography chapter gives 1.01 for Malta in 2024 against an EU average of 1.34, the figures Eurostat publishes."),
    ("Verdict: supported (high confidence).",
     "The foreword gives no year, but the claim holds for the latest data and for each of the seven years before it. "
     "We did not test the second half, on ageing and pressure on services."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(0), Spacer(1, 3 * mm),
      tiles([("1.01", RED, "Malta’s total fertility rate in 2024, live births per woman (Eurostat)"),
             ("27th", RED, "of 27 Member States in 2024: the lowest"),
             ("8 of 8", GREEN, "years Malta has been lowest, 2017–2024"),
             ("1.34", GREY, "EU-27 total fertility rate in 2024; replacement is about 2.1")]),
      Spacer(1, 4 * mm),
      up_down("Already at the top of the scale. A 2025 figure keeping Malta lowest would confirm it again.",
              "A revision or a 2025 release putting another Member State below Malta, if the claim were repeated "
              "without a year."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "Malta’s rank, 2000–2024"),
          ("4", "Testing the claim"), ("5", "Verdict"), ("6", "Limitations")])
S.append(PageBreak())

S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The sentence is in the Minister’s foreword, on printed page 6 (PDF page 8) of the Pre-Budget Consultation "
           "Document 2027 [1]. finance.gov.mt refuses scripts. We read the full PDF from a browser copy supplied by the "
           "maintainer on 16 November 2026. The demography chapter repeats the point with a year and figures: “Malta "
           "registered the lowest total fertility rate among the European Union Member States in 2024, at 1.01 live "
           "births per woman, compared with the EU average of 1.34” (printed page 97) [1]."))
S.append(std_table([
    [C("Source", cellh), C("What it says", cellh), C("Our access", cellh), C("Status", cellh)],
    [C("<b>Ministry for Finance</b>, Pre-Budget Document 2027, foreword [1]"),
     C("“Malta’s fertility rate is the lowest in the EU27…”"), C("Maintainer’s browser copy; full text read."),
     C("<b>The claim</b>")],
    [C("<b>Eurostat</b>, demo_find [2]"),
     C("Total fertility rate by Member State, 2000–2024."), C("API, retrieved 17 Nov 2026 (table updated 13 Nov 2026)."),
     C("<b>Primary data</b>")],
    [C("<b>Eurostat</b>, Fertility statistics [3]"),
     C("EU-27 rate 1.34 in 2024; Malta lowest at 1.01."), C("Read 17 Nov 2026 (data extracted 19 Feb 2026)."),
     C("<b>Official summary</b>")],
], [38 * mm, 66 * mm, 40 * mm, 26 * mm]))

S += [Spacer(1, 4 * mm), SectionHeading(2, "Method")]
S.append(P("The total fertility rate is the average number of children a woman would have over her life if she "
           "experienced the age-specific birth rates of a given year. We downloaded it for every Member State from 2000 "
           "to 2024 (<i>data/cc-141/eurostat_demo_find_tfr.csv</i>) and ranked the 27 countries in each year with all 27 "
           "values (<i>tools/cc-141-report/calc.py</i>; output <i>data/cc-141/ranks.csv</i> and <i>checks.csv</i>). "
           "Eurostat’s table flags its EU-27 value for 2022–2024 as not for publication, so the EU figure for 2024 is "
           "taken from Eurostat’s Statistics Explained article [3]. Eurostat data are official statistics (grade C). "
           "<b>Verdicts</b> follow the five-point scale in Appendix A."))

S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(3, "Malta’s rank, 2000–2024"))
S.append(fig(FIG / "fig1_trend.png", width=CW * 0.98))
S.append(P("Figure 1. Total fertility rate in the 27 Member States, 2000–2024. Shaded: the years in which Malta’s rate "
           "is the EU’s lowest.", cap))
S.append(P("Malta’s rate fell from 1.37 in 2016 to 1.26 in 2017, below Spain’s 1.31, and has been the EU’s lowest every "
           "year since. The gap to the next country has been between 0.03 and 0.09 births per woman. In 2024 it was "
           "0.09 (Malta 1.01, Spain 1.10). Before 2017 Malta was mid-table or low but never lowest. Between 2001 and 2016 "
           "it ranked between 3rd and 18th from the bottom."))
S.append(fig(FIG / "fig2_2024.png", width=CW * 0.98))
S.append(P("Figure 2. Total fertility rate by Member State, 2024, lowest to highest.", cap))

S.append(CondPageBreak(70 * mm))
S.append(SectionHeading(4, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> “Malta’s fertility rate is the lowest in the EU27”"), C("Minister for Finance [1]"),
     C("Lowest in 2024 (1.01) and in every year since 2017 (Eurostat)."), verd("ACCURATE", GREENC)],
    [C("<b>B.</b> Malta 1.01 in 2024 against an EU average of 1.34"), C("Ministry for Finance [1]"),
     C("Both figures match Eurostat [2, 3]."), verd("ACCURATE", GREENC)],
], [42 * mm, 26 * mm, 68 * mm, 34 * mm], valign="MIDDLE"))

S += [Spacer(1, 6 * mm), SectionHeading(5, "Verdict"),
      verdict_box("Supported", "Malta has had the EU’s lowest total fertility rate every year since 2017, at 1.01 in "
                  "2024. Confidence: high."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> The ranking holds in the latest year published and in each of the seven years before it, and "
           "the document’s chapter gives the year and figures that the foreword leaves out. <b>What this verdict does "
           "not say.</b> It does not test the second half of the sentence, on what ageing will cost, or the Budget "
           "measures the document proposes."))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag),
               P("Not needed for this verdict (maintainer rule of 5 October 2026).", small)], bg=AMBER_PALE, bar=AMBER)]
S += [Spacer(1, 6 * mm), SectionHeading(6, "Limitations")]
for l in ["Eurostat’s 2024 figures may be revised. The 2025 figure is not yet published; the Ministry reports that "
          "resident live births fell 0.8% in 2025 [1].",
          "Ranks use the two-decimal values Eurostat publishes. The smallest gap to second place in the period was "
          "0.03 (2018), so the ranking does not depend on rounding.",
          "The total fertility rate is a period measure. It does not show how many children women born in a given year "
          "will have in the end."]:
    S.append(P("• " + l, bul))
S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Ministry for Finance. Pre-Budget Consultation Document 2027, September 2026; foreword p. 6 (PDF p. 8), "
          "section 5.2 p. 97 (maintainer’s browser copy, read 16–17 Nov 2026).",
     "https://finance.gov.mt/wp-content/uploads/2026/09/PRE-BUDGET-2027-DOC.pdf"),
    ("2", "Eurostat. Fertility indicators (demo_find), total fertility rate, updated 13 Nov 2026, retrieved 17 Nov 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/demo_find/default/table"),
    ("3", "Eurostat. Fertility statistics, Statistics Explained (data extracted 19 Feb 2026), read 17 Nov 2026.",
     "https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Fertility_statistics"),
    ("4", "MiŻien. Data and script: data/cc-141/; tools/cc-141-report/calc.py.", ""),
])
S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "17 Nov 2026", "First issue. Verdict Supported (high confidence); no right of reply needed.")])

build_report(Report(
    number="141", out=str(FIG / "report.pdf"), kicker="Population",
    title_lines=["Lowest in", "the EU?"],
    subtitle_lines=["Testing the Pre-Budget Document’s ranking", "of Malta’s fertility rate"],
    quote_lines=["“Malta’s fertility rate is the", "lowest in the EU27…”"], quote_size=16,
    attribution="Clyde Caruana, Minister for Finance, Pre-Budget Consultation Document 2027, foreword.",
    context="Published 30 September 2026, ahead of Budget 2027.",
    verdict="Supported", verdict_note="Lowest every year since 2017; 1.01 in 2024",
    footer_lines=["Version 1.0  ·  17 November 2026", "Status: no right of reply needed",
                  "Prepared from public sources and open data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Fertility rate – Pre-Budget Document 2027", version="1.0", date="17 November 2026",
    pdf_title="Lowest in the EU? Claim Check 141",
    pdf_subject="Tests the Pre-Budget Document 2027 statement that Malta's fertility rate is the lowest in the EU27",
    story=S))
