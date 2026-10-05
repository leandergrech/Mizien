"""Claim Check 112 report. Run fetch.py, calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("In a Selected Issues paper on Malta (IMF Country Report No. 26/30, February 2026), International Monetary "
        "Fund staff listed the drivers of Malta’s housing boom, including <b>“population growth (Malta’s population "
        "rose by 25 percent over a decade, largely due to immigration)”</b>. We tested the figure and the cause against "
        "Eurostat’s demographic accounts for every ten-year window to 2026.", lead)]
S.append(key_points([
    ("“Largely due to immigration” is right.",
     "Net migration made up 93–97% of Malta’s population growth in every ten-year window since 2010–2020. Births "
     "minus deaths added about 5,000–8,000 people a decade."),
    ("“25 percent over a decade” is right for the decades to 2020–2022, and low for the latest one.",
     "Growth was 24.4% (2010–2020), 24.4% (2011–2021) and 24.6% (2012–2022). For the decade to 1 January 2025, the "
     "latest year available when the paper was written, it was 30.9% (438,805 to 574,250). The paper gives no years."),
    ("The comparison makes the point stronger, not weaker.",
     "The EU-27 population grew 1.9% from 2015 to 2025. Malta’s growth over that decade was about sixteen times the EU’s."),
    ("Verdict: largely supported (high confidence).",
     "The substance, rapid growth driven by migration, holds. The 25% understates the most recent decade by about "
     "six points; the paper does not say which decade it means."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("+30.9%", AMBER, "Malta’s population growth, 1 Jan 2015 to 1 Jan 2025 (IMF: 25%)"),
             ("+24.6%", GREEN, "Growth over 2012–2022, the latest decade that matches 25%"),
             ("96%", GREEN, "Share of 2015–2025 growth from net migration"),
             ("+1.9%", GREY, "EU-27 population growth over 2015–2025")]),
      Spacer(1, 4 * mm),
      up_down("The paper, or its authors, naming a decade over which growth was 25%, such as 2012–2022.",
              "Evidence that the figure was meant to describe the latest decade, in which growth was about 31%; then "
              "the size of the understatement would matter more."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the data show"),
          ("4", "Where the evidence points different ways"), ("5", "Testing the claim"),
          ("6", "Verdict and requests for evidence"), ("7", "Limitations")])
S.append(PageBreak())

S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The sentence is in paragraph 6 of the paper “Growth-at-Risk in Malta” in <i>Malta: Selected Issues</i> "
           "(IMF Country Report No. 26/30, February 2026) [1], a background paper to the 2025 Article IV consultation. "
           "It is a parenthesis in a list of drivers of house prices. The IMF’s own site refuses automated downloads, "
           "so we read the paper in full from an Internet Archive copy taken on 17 May 2026. Selected Issues papers "
           "carry the views of their staff authors and not necessarily those of the IMF’s Executive Board; we attribute "
           "the sentence to IMF staff."))
S.append(std_table([
    [C("Source", cellh), C("What it says", cellh), C("Our access", cellh), C("Status", cellh)],
    [C("<b>IMF staff</b>, Malta: Selected Issues, Feb 2026, para. 6 [1]"),
     C("“Drivers of the housing boom include robust income growth, population growth (Malta’s population rose by 25 "
       "percent over a decade, largely due to immigration), and low interest rates.”"),
     C("Full paper read (Internet Archive copy, 17 May 2026)."), C("<b>The claim</b>")],
    [C("<b>Eurostat</b>, demo_gind [2]"), C("Population on 1 January, births, deaths, natural change and net migration."),
     C("Downloaded 5 Oct 2026 (data/cc-112/)."), C("<b>Primary data</b>")],
    [C("<b>NSO</b>, via CC-088 [3]"), C("588,254 residents at the end of 2025."), C("Claim record of CC-088; matches "
       "Eurostat’s 1 January 2026."), C("Context")],
], [38 * mm, 74 * mm, 36 * mm, 22 * mm]))

S += [Spacer(1, 4 * mm), SectionHeading(2, "Method")]
S.append(P("<b>Question.</b> Over which decades did Malta’s population grow by about 25%, and how much of the growth "
           "came from migration?"))
S.append(P("<b>Evidence.</b> We downloaded Eurostat’s population change by component (demo_gind, updated 30 "
           "September 2026) for Malta and the EU-27 (<i>tools/cc-112-report/fetch.py</i>) and computed growth for every "
           "ten-year window from 1 January 2005–2015 to 1 January 2016–2026 (<i>calc.py</i>; outputs in "
           "<i>data/cc-112/checks.csv</i>). The migration share is net migration (including Eurostat’s statistical "
           "adjustment) as a share of the sum of natural change and net migration over the window. The sum of "
           "components differs slightly from the change in the population stock because of census revisions."))
S.append(P("<b>Grades.</b> Official statistics, grade C. No literature is needed to test the figure. <b>Verdicts</b> "
           "follow the five-point scale in Appendix A."))

S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(3, "What the data show"))
S.append(fig(FIG / "fig1_population.png", width=CW * 0.98))
S.append(P("Figure 1. Malta’s population on 1 January (left) and its growth over each ten-year window (right). "
           "Highlighted: the windows within 1.5 points of 25%.", cap))
S.append(P("Malta’s population rose from 402,668 on 1 January 2005 to 588,254 on 1 January 2026. Growth over ten years "
           "rose from 9% (2005–2015) to about 24% for the decades ending in 2020–2022, when the pandemic slowed "
           "migration, and to 29–32% for the decades ending in 2023–2026."))
S.append(fig(FIG / "fig2_components.png", width=CW * 0.95))
S.append(P("Figure 2. Components of population change in Malta each year: net migration and natural change.", cap))

S.append(CondPageBreak(80 * mm))
S.append(SectionHeading(4, "Where the evidence points different ways"))
S.append(contested("Is “25 percent over a decade” the right figure?", "DEPENDS ON THE DECADE", AMBER,
                   "Growth was 24.4–24.6% over the three decades ending in 2020, 2021 and 2022. A writer using those "
                   "years would round to 25%.",
                   "The paper was published in February 2026. The latest decade then available (1 Jan 2015 to 1 Jan "
                   "2025) shows 30.9%, and 2014–2024 shows 31.6%. Read as “the last decade”, 25% understates growth.",
                   "The paper names no years. The figure is accurate for one reading and conservative for the other; "
                   "it never overstates growth.", label_a="FOR 25%", label_b="AGAINST"))

S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(5, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> Malta’s population rose by 25 percent over a decade"), C("IMF staff [1]"),
     C("24.4–24.6% for the decades ending 2020–2022; 30.9% for 2015–2025, the latest decade available in Feb 2026. "
       "No years given."), verd("UNDERSTATES RECENT GROWTH", AMBER)],
    [C("<b>B.</b> …largely due to immigration"), C("IMF staff [1]"),
     C("Net migration was 93–97% of the growth in every decade since 2010–2020; natural change was small."),
     verd("ACCURATE", GREENC)],
], [42 * mm, 18 * mm, 76 * mm, 34 * mm], valign="MIDDLE"))

S += [Spacer(1, 6 * mm), SectionHeading(6, "Verdict and requests for evidence"),
      verdict_box("Largely supported", "Rapid, migration-driven growth is right; the 25% is low for the latest "
                  "decade. Confidence: high."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> The causal part is plainly right. The figure matches the decades ending in 2020–2022 but "
           "understates the most recent decade by about six points. Because the figure errs low, it does not "
           "exaggerate the point it supports: that population growth has pushed up demand for housing. "
           "<b>What this verdict does not say.</b> It does not assess the paper’s housing analysis or its policy advice, "
           "and it says nothing for or against immigration; it tests a number and its stated cause."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list(["From the paper’s authors: the years and data source behind “25 percent over a decade”."]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag),
               P("Not needed for this verdict (maintainer rule of 5 October 2026).", small)], bg=AMBER_PALE, bar=AMBER)]
S += [Spacer(1, 6 * mm), SectionHeading(7, "Limitations")]
for l in ["Net migration in Eurostat’s accounts includes a statistical adjustment; it is not a count of arrivals "
          "minus departures alone.",
          "Population figures before and after the 2021 census are not fully consistent; the components and the "
          "change in the stock differ by a few thousand over some windows.",
          "We read the IMF paper from an Internet Archive copy because the IMF site refuses automated access."]:
    S.append(P("• " + l, bul))
S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "International Monetary Fund (Feb 2026). Malta: Selected Issues. IMF Country Report No. 26/30, “Growth-at-Risk "
          "in Malta”, para. 6. Read from the Internet Archive copy of 17 May 2026.",
     "https://www.imf.org/-/media/files/publications/cr/2026/english/1mltea2026002-source-pdf.pdf"),
    ("2", "Eurostat. Population change – demographic balance and crude rates at national level (demo_gind), updated "
          "30 Sep 2026, retrieved 5 Oct 2026.", "https://ec.europa.eu/eurostat/databrowser/view/demo_gind/default/table"),
    ("3", "MiŻien. CC-088 claim record (NSO population 588,254).", ""),
    ("4", "MiŻien. Calculation script and outputs: tools/cc-112-report/calc.py; data/cc-112/checks.csv.", ""),
])
S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "5 Oct 2026", "First issue. Verdict Largely supported (high confidence); no right of reply needed.")])

build_report(Report(
    number="112", out=str(FIG / "report.pdf"), kicker="Statistics and international reports",
    title_lines=["Population up", "25% in a", "decade?"],
    subtitle_lines=["Testing an IMF staff paper on Malta", "against Eurostat’s demographic accounts"],
    quote_lines=["“Malta’s population rose by 25 percent over a decade,", "largely due to immigration.”"], quote_size=15,
    attribution="IMF staff, Malta: Selected Issues (Country Report No. 26/30), February 2026.",
    context="A parenthesis in a list of drivers of the housing boom (para. 6).",
    verdict="Largely supported", verdict_note="Migration-driven growth is right; 25% is low for the latest decade",
    footer_lines=["Version 1.0  ·  5 October 2026", "Status: no right of reply needed",
                  "Prepared from public sources and Eurostat data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Population growth – IMF Selected Issues 2026", version="1.0", date="5 October 2026",
    status_note="no right of reply needed",
    pdf_title="Population up 25% in a decade? Claim Check 112",
    pdf_subject="Tests an IMF staff statement on Malta's population growth and its cause",
    story=S))
