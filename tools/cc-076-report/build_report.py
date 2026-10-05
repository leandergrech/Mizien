"""Claim Check 076 report. Run fetch.py, calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []

# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("In its news release on motor vehicles for the first quarter of 2026 (NR 085/2026, 13 May 2026), the National "
        "Statistics Office (NSO) wrote: <b>“At the end of March 2026, the stock of licensed motor vehicles stood at "
        "460,648”</b> and that <b>“the stock of licensed motor vehicles increased at a net average rate of 36 motor "
        "vehicles per day”</b>. We rebuilt both figures from the NSO’s own table.", lead)]
S.append(key_points([
    ("The stock and the increase reproduce exactly.",
     "NSO Table 1 gives 457,403 vehicles at the end of 2025 and 460,648 at the end of March 2026: a rise of 3,245 over "
     "the 90 days of the quarter, or 36.06 a day. The vehicle categories add up to the printed totals in all 13 "
     "quarters of the table."),
    ("It is a net figure, and the release says so.",
     "5,680 vehicles were newly licensed (63 a day), 6,963 were taken off the road under restrictions and 4,140 came "
     "back. “36 more a day” is what is left after those flows, not the number of new registrations."),
    ("Two NSO methods differ slightly.",
     "The headline uses the change in the stock. Adding the quarter’s flows to the opening stock gives a rise of 2,857 "
     "(about 32 a day), 388 less. The release says cut-off dates of the databases can cause such differences."),
    ("The pace is recent, not long-standing.",
     "Daily increases were 9 and 8 in the first half of 2024 and 19 in Q1 2025, then 37, 36, 35 and 36 over the last "
     "four quarters. The European Commission’s “35 a day” matches Q4 2025 (35.5)."),
    ("Verdict: supported (high confidence).",
     "The figures are exactly those in the NSO’s own table, the arithmetic is right and the release states the "
     "method. Nothing here tests whether the data are right at source; they come from Transport Malta’s records."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(0), Spacer(1, 3 * mm),
      tiles([("460,648", GREEN, "Licensed motor vehicles at the end of March 2026 (NSO Table 1)"),
             ("+3,245", GREEN, "Net increase in Q1 2026: 36.06 a day over 90 days"),
             ("63 a day", GREY, "Gross: 5,680 vehicles newly licensed in the quarter"),
             ("+8.0%", GREY, "Growth of the stock in three years, end Q1 2023 to end Q1 2026")]),
      Spacer(1, 4 * mm),
      up_down("None: Supported is the top of the scale.",
              "A revision of the NSO data (the release says its figures are subject to revision), or evidence that "
              "Transport Malta’s register overstates the stock."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the data show"),
          ("4", "Where the evidence points different ways"), ("5", "Testing the claim"),
          ("6", "Verdict and requests for evidence"), ("7", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The claim record for this check cites a Newsbook article of 11 November 2025 [3] that reports the same kind of "
           "figure for the third quarter of 2025 (454,138 vehicles; 36 a day). The statement checked here is the NSO’s "
           "newer release for the first quarter of 2026 [1], which carries the numbers in the claim record (460,648 and "
           "36 a day). The NSO site refuses automated requests, so we read the release and its Table 1 workbook from the "
           "Internet Archive’s copy captured on 13 May 2026, the day of release."))
S.append(std_table([
    [C("Source", cellh), C("What it says", cellh), C("Our access", cellh), C("Status", cellh)],
    [C("<b>National Statistics Office</b>, Motor Vehicles: Q1/2026, NR 085/2026, 13 May 2026 [1]"),
     C("“In the first quarter of 2026, the stock of licensed motor vehicles increased by 3,245 over the previous quarter. "
       "At the end of March 2026, the stock of licensed motor vehicles stood at 460,648.” … “During the quarter under "
       "review, the stock of licensed motor vehicles increased at a net average rate of 36 motor vehicles per day.”"),
     C("Release text and Table 1 workbook read (Internet Archive copy), 5 Oct 2026."), C("<b>The claim</b> (verbatim)")],
    [C("<b>NSO</b>, same release, methodological notes 6 and 7 [1]"),
     C("Note 7: net average daily increase = stock in the quarter minus stock in the previous quarter, divided by the "
       "number of days in the quarter. Note 6 gives a flow identity that “might differ slightly from the actual stock”."),
     C("Read."), C("<b>Method</b>")],
    [C("<b>European Commission</b>, 2026 Country Report – Malta, p. 18 [2]"),
     C("“…the overall vehicle fleet continues to grow at a net average rate of 35 motor vehicles per day”, citing NSO "
       "Motor Vehicles: Q4/2025."), C("Council PDF read, 5 Oct 2026."), C("Context")],
    [C("<b>Newsbook</b>, 14 May 2026 and 11 Nov 2025 [3, 4]"), C("Report the Q1 2026 and Q3 2025 releases."),
     C("Read."), C("Locator, not evidence")],
], [38 * mm, 78 * mm, 32 * mm, 22 * mm]))

# ================================================================== 2
S += [Spacer(1, 4 * mm), SectionHeading(2, "Method")]
S.append(P("<b>Question.</b> Do the stock and the daily increase in the NSO statement reproduce from the NSO’s own table, "
           "and is the figure described accurately as a net increase?"))
S.append(P("<b>Evidence.</b> We read Table 1 of the release (stock of licensed motor vehicles by vehicle group, "
           "Q1 2023 to Q1 2026) with <i>tools/cc-076-report/fetch.py</i>, checked that the vehicle categories add up to "
           "the printed total for each quarter, and recomputed the net daily increase for each quarter by the NSO’s own "
           "formula (<i>calc.py</i>; outputs in <i>data/cc-076/</i>). The flows (newly licensed, restricted, restrictions "
           "ended) are taken from the release text, where they are published numbers."))
S.append(P("<b>Grades.</b> Official statistics are grade C in our scale. The claim is arithmetic on a published series; "
           "no literature is needed to test it. <b>Verdicts</b> follow the five-point scale in Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(3, "What the data show"))
S.append(KeepTogether([fig(FIG / "fig1_daily.png", width=CW * 0.98),
                       P("Figure 1. Net average daily increase in licensed motor vehicles, by quarter, Q2 2023 to Q1 2026.", cap)]))
S.append(P("The stock reached 460,648 at the end of March 2026, 8.0% above the 426,720 of March 2023. The increase of "
           "3,245 in Q1 2026 over 90 days is 36.06 a day, which the NSO rounds to 36. Over the four quarters to the end of "
           "March 2026 the stock rose by 13,193, or 36.2 a day; over calendar 2025 it rose by 11,692, or 32.0 a day. The "
           "pace was much lower in the first half of 2024 (9 and 8 a day) and in Q1 2025 (19 a day)."))
S.append(KeepTogether([fig(FIG / "fig2_flows.png", width=CW * 0.98),
                       P("Figure 2. The flows behind the Q1 2026 figure. The net rise is what remains after vehicles taken off "
                         "the road.", cap)]))
S.append(P("In Q1 2026, 5,680 vehicles were newly licensed (3,699 passenger cars; 3,174 were new and 2,506 used), an average "
           "of 63 a day. Against that, 6,963 vehicles went under restriction (41.4% garaged, 29.1% resold, 28.1% scrapped) "
           "and 4,140 restrictions ended. The net daily increase is therefore about 57% of the gross daily licensing."))

# ================================================================== 4
S.append(CondPageBreak(80 * mm))
S.append(SectionHeading(4, "Where the evidence points different ways"))
S.append(contested("Is the quarter’s net rise 3,245 or 2,857?", "BOTH ARE NSO FIGURES", AMBER,
                   "The headline rise is the difference between two published stocks (460,648 and 457,403): 3,245, or 36.06 a "
                   "day. This is the formula in methodological note 7, and the release says it uses it for the daily rate.",
                   "Note 6 builds the stock from flows: opening stock plus new licences, minus restrictions started, plus "
                   "restrictions ended. With the published flows that gives 460,260, a rise of 2,857 (31.7 a day).",
                   "The gap is 388 vehicles, 0.08% of the stock. The release states that the two can differ because the "
                   "databases have different cut-off dates. It does not change the rounded claim by much, but it shows the "
                   "daily figure is not exact to the vehicle.", label_a="STOCK DIFFERENCE (THE HEADLINE)", label_b="FLOW IDENTITY"))
S.append(Spacer(1, 3 * mm))
S.append(contested("Is “36 a day” the trend, or one quarter?", "ACCURATE FOR THE QUARTER", AMBER,
                   "Four consecutive quarters (Q2 2025 to Q1 2026) sit at 35 to 37 a day, so Q1 2026 is typical of the recent "
                   "pace; the Commission’s 35 (Q4 2025) agrees.",
                   "Over calendar 2025 the average was 32 a day, and in 2024 two quarters were below 10. The figure is a quarterly "
                   "average, not a long-run rate.",
                   "The statement is accurate for what it says. It should not be read as the pace of every year.",
                   label_a="RECENT QUARTERS", label_b="LONGER RUN"))

# ================================================================== 5
S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(5, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> The stock of licensed motor vehicles stood at 460,648 at the end of March 2026"), C("NSO [1]"),
     C("Table 1 total for Q1 2026 is 460,648. The vehicle categories add up to the total in all 13 quarters."),
     verd("ACCURATE", GREENC)],
    [C("<b>B.</b> The stock rose by 3,245 over the quarter, a net average of 36 vehicles a day"), C("NSO [1]"),
     C("460,648 minus 457,403 is 3,245; over 90 days that is 36.06 a day, by the NSO’s stated formula."),
     verd("ACCURATE", GREENC)],
    [C("<b>C.</b> The figure is a net increase, not a count of new registrations"), C("NSO [1]"),
     C("Gross licensing was 63 a day; 6,963 vehicles went under restriction and 4,140 returned. The release gives both."),
     verd("ACCURATE", GREENC)],
    [C("<b>D.</b> The fleet grows at a net average of 35 vehicles a day"), C("Commission [2]"),
     C("Q4 2025: 3,265 over 92 days is 35.5 a day, matching the Commission’s figure and its NSO citation. We derived "
       "this from Table 1; we did not retrieve the Q4 release."), verd("ACCURATE", GREENC)],
], [42 * mm, 18 * mm, 76 * mm, 34 * mm], valign="MIDDLE"))

# ================================================================== 6
S += [CondPageBreak(75 * mm), Spacer(1, 6 * mm), SectionHeading(6, "Verdict and requests for evidence"),
      verdict_box("Supported", "The stock and the net daily increase reproduce exactly from the NSO’s own table. "
                  "Confidence: high."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> Both figures (460,648 and 36 a day) follow from the NSO’s Table 1 by the NSO’s stated formula, the "
           "description as a net increase is correct, and the nearest comparable official statement (the Commission’s 35 a "
           "day) agrees with the preceding quarter. The release’s own caveats (data subject to revision; cut-off "
           "differences) are small."))
S.append(P("<b>What this verdict does not say.</b> It does not test the Transport Malta register that the NSO uses, "
           "or say whether the growth of the fleet is good or bad. It does not rate any policy on congestion."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "From the NSO: confirmation that the Q1 2026 figures have not been revised, and the Q4 2025 release for the "
    "Commission’s 35 a day.",
    "From Transport Malta: the reason for the low net growth in 2024 (about 8 to 9 a day in the first half) compared with "
    "2025 and 2026, which the data alone do not explain.",
]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag),
               P("Not needed for this verdict (maintainer rule of 5 October 2026: a reply is sought only for "
                 "<i>Not substantiated</i>, <i>Misleading</i> or <i>Contradicted</i>).", small)], bg=AMBER_PALE, bar=AMBER)]

# ================================================================== 7
S += [Spacer(1, 6 * mm), SectionHeading(7, "Limitations")]
for l in ["We tested the NSO’s arithmetic against its own table. We did not test the underlying register of Transport Malta.",
          "The NSO website refuses automated access; we used the Internet Archive’s copy of the release, captured on the day of "
          "release (13 May 2026). The NSO notes its data are subject to revision.",
          "The Q4 2025 NSO release was not retrieved; the Commission’s 35 a day is checked from Table 1, not from that release.",
          "The released text does not give the number of vehicles in each flow by day; the flow identity is the NSO’s, with "
          "its own caveat about cut-off dates."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "National Statistics Office, Malta (13 May 2026). Motor Vehicles: Q1/2026. News release NR 085/2026, with Table 1 "
          "workbook. Read from the Internet Archive copy captured 13 May 2026.",
     "https://nso.gov.mt/motor-vehicles-q1-2026/"),
    ("2", "European Commission (3 June 2026). 2026 Country Report – Malta. SWD(2026) 218 final; Council document 10135/26 "
          "ADD 1, p. 18 and footnote 11.", "https://data.consilium.europa.eu/doc/document/ST-10135-2026-ADD-1/en/pdf"),
    ("3", "◆ Newsbook (11 Nov 2025). Malta’s roads grow more congested as vehicle fleet tops 454,000 (reports the Q3 2025 "
          "release).", "https://newsbook.com.mt/en/maltas-roads-grow-more-congested-as-vehicle-fleet-tops-454000/"),
    ("4", "◆ Newsbook (14 May 2026). Over 3,200 new vehicles added to Malta’s roads in three months (reports the Q1 2026 "
          "release).", "https://newsbook.com.mt/en/over-3200-new-vehicles-added-to-maltas-roads-in-three-months/"),
    ("5", "MiŻien. Calculation script and outputs: tools/cc-076-report/calc.py; data/cc-076/checks.csv.", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "5 Oct 2026", "First issue. Verdict Supported (high confidence); no right of reply needed.")])

build_report(Report(
    number="076", out=str(FIG / "report.pdf"), kicker="Transport and official statistics",
    title_lines=["36 more", "vehicles", "a day?"],
    subtitle_lines=["Testing the National Statistics Office’s", "Q1 2026 motor vehicle release"],
    quote_lines=["“…the stock of licensed motor vehicles increased at a", "net average rate of 36 motor vehicles per day.”"],
    quote_size=14,
    attribution="National Statistics Office, Motor Vehicles: Q1/2026, NR 085/2026, 13 May 2026.",
    context="The same release gives the stock at the end of March 2026 as 460,648.",
    verdict="Supported", verdict_note="Reproduces exactly from the NSO’s own table",
    footer_lines=["Version 1.0  ·  5 October 2026", "Status: no right of reply needed",
                  "Prepared from public sources and NSO data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Licensed motor vehicles – NSO Q1 2026", version="1.0", date="5 October 2026",
    status_note="no right of reply needed",
    pdf_title="36 more vehicles a day? Claim Check 076",
    pdf_subject="Tests the NSO Q1 2026 figures on the stock of licensed motor vehicles in Malta",
    story=S))
