"""Claim Check 094 report. Run fetch.py, calc.py and figures.py first. Output: out/report.pdf"""
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
      P("In its EU Climate Action Progress Report 2025 (6 November 2025) the European Commission wrote, under a chart of "
        "every Member State’s 2030 outlook: <b>“Malta’s gap to target is 49 and 61 percentage points, exceeding its 19% "
        "reduction target. This means Malta is projected to emit more in 2030 than in 2005.”</b> [1] It also named "
        "Malta among the countries with the largest gaps. We tested these sentences against Malta’s own projections, "
        "the official emissions data and the EU law that sets the target.", lead)]
S.append(key_points([
    ("The numbers reproduce exactly.",
     "Malta’s March 2025 projections put its effort-sharing emissions at 1,324 kt in 2030 with planned measures and "
     "1,450 kt with existing ones: +29.7% and +42.1% on the 2005 level of 1,021 kt, a gap of 48.7 and 61.1 points to "
     "the −19% target [3, 4, 7]."),
    ("“More in 2030 than in 2005” holds every way we tried:",
     "both scenarios, every 2005 figure we found, and projections re-based on reviewed 2023 data (+26% and +38%). "
     "2024 emissions were already 41% above 2005 [3]."),
    ("Malta’s gap is the EU’s largest in percentage points:",
     "49, then Ireland 20 and Germany 13 (planned measures), as the Commission says. In tonnes it is small (0.5 Mt)."),
    ("Flexibilities shrink the gap but do not close it.",
     "Malta is projected 2.1 Mt over its yearly limits in 2021–2030. Its own flexibilities cover 0.54 Mt; about 1.6 Mt "
     "would have to be bought from other Member States (about 1% of the expected EU surplus) or cut."),
    ("Verdict: supported (high confidence).",
     "The Commission’s words match the data and the law. “Missing its target”, in our claim list, is a paraphrase: "
     "true of Malta’s own emissions, but Malta can still comply by buying allocations."),
]))
S += [Spacer(1, 4 * mm), VerdictMeter(0), Spacer(1, 3 * mm),
      tiles([("+30–42%", RED, "Malta’s effort-sharing emissions in 2030 vs 2005 (planned / existing measures)"),
             ("49 / 61", GREEN, "points of gap to the −19% target (planned / existing): the Commission’s figures, reproduced"),
             ("+41%", ORANGE, "2024 emissions vs 2005 (latest year; approximated data)"),
             ("1.6 Mt", ORANGE, "still to buy or cut over 2021–2030 after Malta’s own flexibilities (planned measures)")]),
      Spacer(1, 4 * mm),
      up_down("None: Supported is the top of the scale.",
              "Evidence that the EEA dataset misrecords Malta’s March 2025 submission, or a revision of the 2005 level or "
              "of the reviewed 2021–2023 emissions large enough to bring the 2030 projection down to the 2005 level "
              "(it is 303 kt above it with planned measures)."),
      Spacer(1, 5 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "How the effort-sharing target works"),
          ("4", "What the data show"), ("5", "Flexibilities: does Malta miss its target?"),
          ("6", "Where the evidence points different ways"), ("7", "Testing the claim"),
          ("8", "Verdict and requests for evidence"), ("9", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The speaker is the European Commission, in its annual report to the European Parliament and the Council "
           "under the Governance Regulation, COM(2025) 668 final [1]. We read every sentence that mentions Malta. Three "
           "passages concern the 2030 effort-sharing target; we rate all three. The claim list’s summary (“missing its "
           "target”) is our intake’s paraphrase, not the Commission’s wording."))
S.append(std_table([
    [C("What the Commission says", cellh), C("Where", cellh), C("Access", cellh)],
    [C("“Malta’s gap to target is 49 and 61 percentage points, exceeding its 19% reduction target. This means Malta is "
       "projected to emit more in 2030 than in 2005.”"), C("Note to Figure 13, p. 30 [1]"),
     C("Read in full (Publications Office copy)")],
    [C("“Prior to any use of ESR flexibilities by Member States to meet their targets, Germany, Ireland and Malta show "
       "the largest projected gaps in 2030 whereas Bulgaria, Greece and Portugal show the largest overachievement of "
       "their 2030 targets.”"), C("Section 3.2, p. 30 [1]"), C("Read in full")],
    [C("“…Austria, Estonia, Germany, Malta, Ireland and Sweden are projected to have excess emissions in the second "
       "compliance period (2026-2030).”"), C("Section 3.2, p. 31 [1]"), C("Read in full")],
], [104 * mm, 36 * mm, 30 * mm]))
S.append(Spacer(1, 2 * mm))
S.append(P("The note does not say which of 49 and 61 belongs to which projection; Figure 13 and the accompanying staff "
           "working document (Table 25, p. 114) show 49 with additional (planned) measures and 61 with existing "
           "measures [1, 2]. The third sentence rests on stated assumptions: planned measures are implemented, Member "
           "States bank and borrow allocations between years, and those that notified the ETS flexibility use it. On "
           "the same page the Commission adds that, given the expected EU-wide surplus of allocations, it “cannot, at "
           "this stage, conclude that Member States are not making sufficient progress” [1]."))
S += [Spacer(1, 1 * mm),
      callout([P("FAIRNESS NOTE", tag),
               P("This check holds an EU institution to the same standard as Maltese speakers. It tests what the "
                 "Commission said, not whether Malta’s target is fair; the Maltese government’s view of the target, set "
                 "out in its climate plan, is given in section 6. Related checks: CC-003 (the Climate Action Authority’s "
                 "per-person figures, which omitted this projection), CC-025 (Malta’s COP30 statement) and CC-024 "
                 "(renewables).", small)],
              bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Question.</b> Do Malta’s reported projections, the official emissions data and the law give a 2030 gap of "
           "49 and 61 points against a −19% target, so that Malta is projected to emit more in 2030 than in 2005? Is "
           "Malta’s gap among the largest, and does it survive the flexibilities the law allows?"))
S.append(P("<b>Evidence.</b> We downloaded from the European Environment Agency (EEA) its effort-sharing emissions for "
           "2005–2024 [3] and the Member States’ 2025 greenhouse gas projections [4], kept each value’s status (reviewed "
           "or approximated) and recomputed every figure with <i>tools/cc-094-report/calc.py</i> from <i>data/cc-094/</i>. "
           "The 2005 levels, targets, yearly limits and flexibilities come from the legal texts themselves [5–10], read "
           "through the EU Publications Office on 6 October 2026, as was the report [1]. We read the ESR section of "
           "Malta’s climate plan [12] and the Commission’s assessment of it [13]. Crossref was searched for peer-reviewed "
           "work on effort-sharing gaps and the accuracy of national projections; none on Malta was found "
           "(search log in <i>literature/CC-094/notes.md</i>)."))
S.append(P("<b>Grades.</b> Official statistics, projections reported under EU law and legal texts are grade C under our "
           "scale. <b>Verdicts</b> follow the five-point scale in Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(60 * mm))
S.append(SectionHeading(3, "How the effort-sharing target works"))
S.append(P("The Effort Sharing Regulation (ESR) covers the emissions outside the EU’s main emissions trading system: "
           "domestic transport, buildings, agriculture, small industry and waste [1], including industrial gases, which in "
           "Malta come almost entirely (over 95%) from refrigeration and air conditioning [12]. Power generation falls under the trading system: in "
           "Malta’s projections, energy industries add under 1 kt to its effort-sharing emissions [4]. Each Member State "
           "has a 2030 target against its 2005 level. Malta’s is −19%, the same in the 2018 regulation and in the 2023 "
           "revision that raised every other Member State’s target [5, 6]. The 2005 level used is fixed in law at 1,020,601 t CO₂e [7], so the 2030 "
           "limit is 826.7 kt, the figure Malta’s own plan gives [12]."))
S.append(P("The target is enforced through yearly limits, the annual emission allocations, set for 2021–2025 and, "
           "after a review of 2021–2023 emissions, for 2026–2030 (adopted 24 April 2026) [8]. Malta’s 2021 limit includes "
           "a one-off 774 kt adjustment, part of one made for lower-income Member States [5, 11]. Compliance is checked in 2027 (for 2021–2025) "
           "and 2032 (for 2026–2030). A Member State over its limits may bank surpluses and borrow from the next year, "
           "use the ETS flexibility (cancelling trading-system allowances) or land-use credits, or buy allocations from "
           "others. An excess left after all that is added to the next year’s emissions with a 1.08 multiplier [5, 6]."))
S.append(KeepTogether([fig(FIG / "fig1_path.png"), P(
    "Figure 1. Malta’s effort-sharing emissions against its yearly limits, 2005–2030. Emissions have been above the "
    "limits since 2022 and, on both projections, stay well above the 2030 limit of 827 kt. 2005–2020 are on the older "
    "Effort Sharing Decision basis and are shown for context only. Sources [3, 4, 7, 8].", cap)]))

# ================================================================== 4
S.append(CondPageBreak(90 * mm))
S.append(SectionHeading(4, "What the data show"))
S.append(P("Projections and the 2005 level", h2))
S.append(KeepTogether([
    std_table([
        [C("Measure", cellh), C("Existing measures (WEM)", cellh), C("Planned measures (WAM)", cellh), C("Source", cellh),
         C("Grade", cellh)],
        [C("Malta’s 2030 effort-sharing emissions, March 2025 projection"), C("1,450.1 kt"), C("1,323.8 kt"), C("EEA [4]"),
         grade_tag("C")],
        [C("Change vs the legal 2005 level (1,020.6 kt)"), C("<b>+42.1%</b>"), C("<b>+29.7%</b>"), C("calculated"),
         grade_tag("C")],
        [C("Gap to the −19% target"), C("<b>61.1 points</b> (Commission: 61)"), C("<b>48.7 points</b> (Commission: 49)"),
         C("calculated; [1, 2]"), grade_tag("C")],
        [C("Excess over the 2030 limit of 826.7 kt"), C("623 kt"), C("497 kt"), C("calculated"), grade_tag("C")],
        [C("Against the EEA’s own 2005 estimate (1,007.4 kt, older basis)"), C("+43.9%"), C("+31.4%"), C("EEA [3]"),
         grade_tag("C")],
        [C("Against the 2013–2020 base year (1,116.1 kt)"), C("+29.9%"), C("+18.6%"), C("EEA [3]"), grade_tag("C")],
        [C("Re-based on reviewed 2023 emissions (projection starts 2.6% high)"), C("+38.5%"), C("+26.4%"),
         C("calculated"), grade_tag("C")],
        [C("Previous projection, March 2023"), C("+46.3%"), C("+46.3%"), C("EEA [4]"), grade_tag("C")],
    ], [62 * mm, 34 * mm, 34 * mm, 24 * mm, 16 * mm]),
    P("All values in <i>data/cc-094/checks.csv</i>. The legal 2005 level is from Implementing Decision (EU) 2020/2126 "
      "[7]; the other two 2005 figures are shown only to test how much the choice matters.", cap)]))
S.append(P("Every combination leaves 2030 above 2005: the smallest margin, +18.6%, uses an older base year that the "
           "current rules do not use. Recent years point the same way. Reviewed emissions were 30%, 43% and 42% above "
           "the 2005 level in 2021–2023 and approximated emissions 41% above in 2024 (1,437 kt), matching the "
           "Commission’s Table 25 [2, 3]. Malta was over its yearly limit by 220, 257 and 301 kt in 2022–2024. The 2024 "
           "value is 3.3% below what the projection expected for that year, a small easing. Reaching 827 kt by 2030 "
           "would need a 42.5% cut from 2024, about 8.8% a year; the planned-measures projection has 7.9% in all over "
           "six years, and the existing-measures one has emissions flat."))
S.append(P("Where the projected emissions come from", h2))
S.append(P("Transport is half of Malta’s effort-sharing emissions (745 kt in 2023) and is projected at 737 kt in 2030 "
           "in <i>both</i> scenarios [4]. The two projections differ only in waste (165 kt with existing measures, 73 kt "
           "with planned ones: landfill gas capture, which Malta’s plan describes [12]) and industrial gases (198 and 163 "
           "kt). Buildings, manufacturing fuel and agriculture are the same in both. The Commission’s assessment of the "
           "plan found “insufficient details” on how Malta will meet the target and noted that the projections leave out "
           "the new trading system for buildings and road fuel (ETS2) [13]."))
S.append(KeepTogether([fig(FIG / "fig3_sectors.png"), P(
    "Figure 2. Malta’s projected effort-sharing emissions by sector. Transport alone (737 kt in 2030, the same in both "
    "projections) would take up 89% of the 2030 limit of 827 kt. Source [4].", cap)]))
S.append(CondPageBreak(90 * mm))
S.append(P("Is Malta’s gap among the largest?", h2))
S.append(P("We recomputed the gap for all 27 Member States from the same projections, the legal 2005 levels and the "
           "2030 targets [4, 6, 7]. With planned measures, the measure the Commission’s section uses, the largest gaps "
           "are Malta (48.7 points), Ireland (20.3) and Germany (13.2), then Austria (8.0); the largest overachievement "
           "is Bulgaria (25.6 points), Greece (20.6) and Portugal (11.4). Both lists are the Commission’s. With existing "
           "measures Malta is still first (61.1), but Cyprus (28.2) and Belgium (25.3) rank above Germany. In tonnes, the "
           "largest gaps are Germany (64.1 Mt), Italy (10.9) and Ireland (9.7); Malta’s is 0.5 Mt, tenth. Belgium did "
           "not report in 2025, so its figures are from 2024."))
S.append(KeepTogether([fig(FIG / "fig2_gaps.png"), P(
    "Figure 3. Projected 2030 gap to target by Member State, with planned measures (bars) and existing measures (dashes). "
    "Malta’s gap is the largest in percentage points in both. Our recalculation of the Commission’s Figure 13 from the "
    "EEA data [4, 6, 7].", cap)]))

# ================================================================== 5
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(5, "Flexibilities: does Malta miss its target?"))
S.append(P("The Commission’s first two sentences describe emissions before any flexibility. Its third applies "
           "banking, borrowing and the ETS flexibility. We added up Malta’s position over 2021–2030 with the adopted "
           "yearly limits [8], reviewed and approximated emissions for 2021–2024 [3] and the projections for 2025–2030 [4]."))
S.append(std_table([
    [C("Step, 2021–2030 total", cellh), C("Planned measures (WAM)", cellh), C("Existing measures (WEM)", cellh),
     C("Source", cellh)],
    [C("Yearly limits minus emissions, 2021–2025 (2025 projected)"), C("−0.44 Mt"), C("−0.44 Mt"), C("[3, 4, 8]")],
    [C("…after the ETS flexibility (510.3 kt in all)"), C("+0.07 Mt: covered"), C("+0.07 Mt: covered"), C("[9]")],
    [C("Yearly limits minus emissions, 2021–2030"), C("−2.09 Mt"), C("−2.71 Mt"), C("[3, 4, 8]")],
    [C("…after the ETS flexibility"), C("−1.58 Mt"), C("−2.20 Mt"), C("[9]")],
    [C("…after the maximum land-use (LULUCF) credit, 0.03 Mt"), C("<b>−1.55 Mt</b>"), C("<b>−2.17 Mt</b>"), C("[5]")],
    [C("As a share of the EU surplus the Commission expects (125–175 Mt)"), C("0.9–1.2%"), C("1.2–1.7%"), C("[1]")],
], [76 * mm, 34 * mm, 34 * mm, 26 * mm]))
S.append(Spacer(1, 2 * mm))
S.append(P("This reproduces the Commission’s finding: Malta is covered for 2021–2025, partly thanks to the 2021 surplus "
           "(740 kt, which exists only because of the one-off 774 kt adjustment), and has excess emissions in 2026–2030. Our "
           "−2.09 Mt matches the Commission’s own −2.1 Mt [2]; the yearly limits it then estimated for 2026–2030 match "
           "those adopted in April 2026 [8]. The land-use credit is small in law (0.03 Mt) and Malta’s land sector has "
           "produced almost none so far [1, 2]. Malta cannot use the EU’s safety reserve: its emissions exceeded its "
           "limits in 2013–2020 [10]."))
S.append(KeepTogether([fig(FIG / "fig4_ledger.png"), P(
    "Figure 4. Malta’s effort-sharing balance over 2021–2030 and what its own flexibilities cover. The rest would have "
    "to be bought from other Member States or cut further. Sources [3–5, 8, 9].", cap)]))
S.append(P("So two readings of “missing its target” are both right in their own terms. Malta’s own emissions are "
           "projected to miss the 2030 level by about 0.5 Mt even with planned measures. Legally, Malta can still comply "
           "by buying about 1.6 Mt of allocations (2.2 Mt without the planned measures) from Member States with a surplus, "
           "which the regulation allows. The price is not public, so we do not estimate the cost. The Commission’s "
           "wording (“gap”, “excess emissions”, “prior to any use of ESR flexibilities”) keeps the two apart."))

# ================================================================== 6
S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(6, "Where the evidence points different ways"))
S.append(contested(
    "Q1  Is a projection a fair basis for “will emit more”?", "YES, AS WORDED", GREEN,
    "The Commission says Malta “is projected to” emit more, which is what Malta’s own projections show [4]. Measured "
    "emissions agree: 41% above 2005 in 2024, over the yearly limit for three years running [3, 8].",
    "Projections can be wrong. Malta’s started 2.6% above the reviewed 2023 value, its 2024 emissions came in 3.3% "
    "below the projection, and ETS2 is not modelled [13]. A new projection is due in 2027.",
    "<b>For this claim:</b> even re-based on the reviewed 2023 value, 2030 is 26–38% above 2005. Closing that by 2030 "
    "would take a cut of 42.5% from 2024 levels, far beyond any projection Malta has reported."))
S.append(contested(
    "Q2  Is the −19% target a fair yardstick for Malta?", "CONTEXT; NOT TESTED", GREY,
    "The target is binding law, unchanged since 2018 [5, 6]. Malta’s own plan states the 826.7 kt limit and calls "
    "flexibilities “crucial” to meet it [12].",
    "Malta’s plan says the target rests on 2005 projections that “differ markedly from today’s reality, particularly "
    "in terms of population growth” [12]; population grew 41% from 2005 to 2024 [15], and effort-sharing emissions "
    "per person were 2.53 t in both years. EU lawmakers accepted that Malta’s target is “significantly above its "
    "cost-effective reduction potential” and raised its ETS flexibility to 7% [6].",
    "<b>For this claim:</b> both points are fair context and both sides are quoted. Neither changes what the "
    "Commission said: the target is −19% in total tonnes, and the projection misses it."))
S.append(contested(
    "Q3  Does “missing its target” overstate the Commission?", "PARAPHRASE, NOT RATED", GREY,
    "Domestic emissions are projected above the 2030 limit and above the yearly limits from 2026 on; Malta’s own "
    "flexibilities cover about a quarter of the excess with planned measures and a fifth without (section 5).",
    "Compliance can be bought: the expected EU surplus is 80 to 110 times Malta’s shortfall, and the Commission says it "
    "cannot yet conclude that progress is insufficient [1].",
    "<b>For this claim:</b> the Commission did not say “missing its target”; its own words separate the gap before "
    "flexibilities from compliance after them. We rate its words."))

# ================================================================== 7
S.append(CondPageBreak(60 * mm))
S.append(SectionHeading(7, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> “Malta’s gap to target is 49 and 61 percentage points”"),
     C("48.7 (planned measures) and 61.1 (existing) from Malta’s March 2025 projections, the legal 2005 level and the "
       "−19% target [4, 6, 7]."), verd("ACCURATE", GREENC)],
    [C("<b>B.</b> “…exceeding its 19% reduction target. This means Malta is projected to emit more in 2030 than in 2005.”"),
     C("+29.7% and +42.1% on 2005; above 2005 against every 2005 figure and if re-based on reviewed 2023 data "
       "(+26% and +38%) [3, 4]."), verd("ACCURATE", GREENC)],
    [C("<b>C.</b> Germany, Ireland and Malta show the largest projected 2030 gaps before flexibilities"),
     C("With planned measures, in points: Malta 48.7, Ireland 20.3, Germany 13.2, Austria next at 8.0. Not so with "
       "existing measures (Cyprus, Belgium above Germany) or in tonnes (Malta 0.5 Mt) [4]."), verd("ACCURATE", GREENC)],
    [C("<b>D.</b> Malta projected to have excess emissions in 2026–2030"),
     C("Covered to 2025 after the ETS flexibility (+0.07 Mt); −1.58 Mt by 2030 (planned measures), −1.55 Mt with the "
       "maximum land-use credit [3–5, 8, 9]."), verd("ACCURATE", GREENC)],
    [C("<b>E.</b> “Missing its target” (our claim list’s paraphrase)"),
     C("Not the Commission’s words. Domestically 0.5 Mt over in 2030; legally, compliance possible by buying about "
       "1.6 Mt (1.2% or less of the EU surplus). No safety reserve for Malta [1, 10]."),
     verd("NOT RATED (PARAPHRASE)", GREY)],
], [62 * mm, 78 * mm, 30 * mm], valign="MIDDLE"))
S.append(Spacer(1, 3 * mm))
S.append(P("<b>The Commission’s reasoning.</b> “Exceeding its 19% reduction target” is a compressed way of saying the "
           "gap is larger than the cut required. Because the gap is the projected change minus the target, a gap of "
           "more than 19 points means emissions above the 2005 level, so the second sentence follows from the first. "
           "<b>Consistency with CC-003.</b> CC-003 used the same Commission tables (+41% in 2024; +42% and +30% in 2030; "
           "−2.1 Mt by 2030) and its own estimate of effort-sharing emissions per person (2.50 t to 2.52 t). Here we use the "
           "EEA’s official series and the legal 2005 level (2.53 t in both years); the conclusions are the same [17]."))

# ================================================================== 8
S += [CondPageBreak(85 * mm), Spacer(1, 4 * mm), SectionHeading(8, "Verdict and requests for evidence"),
      verdict_box("Supported", "The Commission’s figures and its inference reproduce from Malta’s own reported "
                  "projections, the EEA’s data and the legal 2005 level. Confidence: high."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) The 49 and 61 points reproduce from Malta’s projections as held by the EEA, the 2005 "
           "level and the target in EU law. (2) “More in 2030 than in 2005” holds under both projections and every 2005 "
           "figure we found; 2024 emissions were already 41% above 2005. (3) The ranking and the 2026–2030 excess "
           "reproduce under the Commission’s stated assumptions, and its words are conditioned on flexibilities that, "
           "by our ledger, do not close the gap. Confidence is high: the projections, reviewed emissions, legal texts, "
           "the Commission’s tables and Malta’s plan all agree."))
S.append(P("<b>What this verdict does not say.</b> That Malta will fail its legal obligations (it can buy "
           "allocations), whether the −19% target is fair to Malta, or anything about anyone’s intentions."))
S.append(KeepTogether([P("Evidence we are asking for", h2), requests_list([
    "From the Ministry for the Environment and the Climate Action Authority: how Malta intends to cover its 2026–2030 "
    "excess (purchases of allocations, from whom, at what cost), which its plan does not quantify.",
    "Malta’s approximated 2025 effort-sharing emissions and its 2027 projection update, when submitted.",
    "A quantified estimate of ETS2’s effect on Malta’s transport and buildings emissions, which the Commission says the "
    "projections leave out.",
])]))

# ================================================================== 9
S += [Spacer(1, 2 * mm), SectionHeading(9, "Limitations")]
for l in ["Projections are Malta’s March 2025 submission as quality-checked by the EEA (we did not see Malta’s own "
          "files); the next are due in 2027. 2024 emissions are approximated; 2025 figures were not yet in the EEA "
          "datastore on 6 October 2026.",
          "Our 2021–2030 balance treats the ETS flexibility as usable when needed, as the Commission does; in law it is "
          "cancelled in yearly instalments, which does not change the total.",
          "Whether and at what price Malta will buy allocations is not public; we do not estimate the cost.",
          "No peer-reviewed study of Malta’s effort-sharing gap was found; this check rests on official data and law "
          "(grade C)."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 2 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "European Commission (6 Nov 2025). EU Climate Action Progress Report 2025. COM(2025) 668 final, pp. 30–31. Read "
          "in full for Malta via the EU Publications Office, 6 Oct 2026 (EUR-Lex refused scripts).",
     "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX%3A52025DC0668"),
    ("2", "European Commission (Nov 2025). Climate Action Progress Report 2025, staff working document SWD(2025) 347: "
          "Table 25 (p. 114), Table 26 (p. 125), p. 111, Table 27 (p. 131).",
     "https://climate.ec.europa.eu/document/download/35f83a2d-f77d-4895-b616-d579069b23d3_en?filename=capr2025_swd_en.pdf"),
    ("3", "European Environment Agency. Greenhouse gas emissions under the Effort Sharing Legislation, 2005–2024 "
          "(sheet dated 4 Nov 2025). Retrieved 6 Oct 2026.",
     "https://sdi.eea.europa.eu/catalogue/srv/api/records/f80bebef-447e-4882-b3e9-c4a91cbae4f5"),
    ("4", "European Environment Agency. Member States’ greenhouse gas (GHG) emission projections 2025. "
          "doi:10.2909/d6938865-05e5-4016-a15c-a09bb898421d. Retrieved 6 Oct 2026.",
     "https://doi.org/10.2909/d6938865-05e5-4016-a15c-a09bb898421d"),
    ("5", "Regulation (EU) 2018/842 (Effort Sharing Regulation), Articles 4–11 and Annexes II–IV. OJ L 156, 19.6.2018, "
          "p. 26.", "https://data.europa.eu/eli/reg/2018/842/oj"),
    ("6", "Regulation (EU) 2023/857 amending Regulation (EU) 2018/842, recitals and Annex. OJ L 111, 26.4.2023, p. 1.",
     "https://data.europa.eu/eli/reg/2023/857/oj"),
    ("7", "Commission Implementing Decision (EU) 2020/2126, Annex I (2005 values). OJ L 426, 17.12.2020, p. 58.",
     "https://data.europa.eu/eli/dec_impl/2020/2126/oj"),
    ("8", "Commission Implementing Decision (EU) 2026/895 of 24 April 2026 (annual emission allocations 2021–2030, as "
          "replaced; 2023–2025 first set by Decision (EU) 2023/1319).", "https://data.europa.eu/eli/dec_impl/2026/895/oj"),
    ("9", "Commission Implementing Decision (EU) 2024/1884 (ETS flexibility: Malta 510,300 t).",
     "https://data.europa.eu/eli/dec_impl/2024/1884/oj"),
    ("10", "Commission Decision (EU) 2023/863 (safety reserve), recital (5).", "https://data.europa.eu/eli/dec/2023/863/oj"),
    ("11", "European Commission. Effort sharing 2021–2030: targets and flexibilities (web page). Read 6 Oct 2026.",
     "https://climate.ec.europa.eu/areas-action/carbon-removals-and-carbon-farming/effort-sharing-member-states-emission-targets/effort-sharing-2021-2030-targets-and-flexibilities_en"),
    ("12", "Government of Malta (Dec 2024). Final updated National Energy and Climate Plan 2021–2030, pp. 54–58, 138 "
           "and 327–329 (Commission copy).",
     "https://commission.europa.eu/publications/malta-final-updated-necp-2021-2030-submitted-2025_en"),
    ("13", "European Commission (2025). Assessment of the final updated NECPs, SWD(2025) 140, Malta extract, pp. 160–162.",
     "https://commission.europa.eu/document/download/bf1c1e17-293c-4c50-92ca-1ae663ab6cae_en?filename=MT_Extract_SWD+2025_140.pdf"),
    ("14", "European Environment Agency. NECPR: progress to targets for GHG emissions and removals (Annex I), 2025. "
           "Retrieved 6 Oct 2026 (Malta’s reported 2023 effort-sharing emissions).",
     "https://sdi.eea.europa.eu/catalogue/srv/api/records/fb3f4e09-0318-400d-beae-f1082153b2bb"),
    ("15", "Eurostat. nama_10_pe, population (as retrieved for CC-003, 2 Oct 2026).",
     "https://ec.europa.eu/eurostat/databrowser/view/nama_10_pe/default/table"),
    ("16", "Camilleri R., Attard M., Hickman R. (2024). Participatory Policy Packaging for Transport Backcasting: A Pathway "
           "for Reducing CO2 Emissions from Transport in Malta. <i>Sustainability</i> 16(1):430. doi:10.3390/su16010430. "
           "(Abstract read; context.)", "https://doi.org/10.3390/su16010430"),
    ("17", "Miżien. Claim Check 003: per-capita emissions vs the 2030 projection (v1.2, 5 Oct 2026).",
     "https://github.com/leandergrech/Mizien/tree/main/claims/CC-003"),
    ("18", "Miżien. Data and calculations: data/cc-094/; tools/cc-094-report/calc.py.", ""),
])

S.append(CondPageBreak(150 * mm))
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance, "
                "official statistics or legal text · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += revision_log([("1.0", "6 Oct 2026", "First issue. No right of reply needed for a Supported verdict.")])

build_report(Report(
    number="094", out=str(FIG / "report.pdf"), kicker="EU assessments and effort-sharing data",
    title_lines=["More in 2030", "than in 2005?"],
    subtitle_lines=["Testing the European Commission’s projection of Malta’s", "effort-sharing emissions against "
                    "the data and the law"],
    quote_lines=["“Malta’s gap to target is 49 and 61 percentage points,", "exceeding its 19% reduction target. "
                 "This means Malta", "is projected to emit more in 2030 than in 2005.”"],
    quote_size=13.2,
    attribution="European Commission, EU Climate Action Progress Report 2025, COM(2025) 668, p. 30, 6 Nov 2025.",
    context="Effort-sharing sectors: transport, buildings, waste, agriculture, small industry, refrigerant gases.",
    verdict="Supported", verdict_note="Reproduced from Malta’s own projections and EU law",
    footer_lines=["Version 1.0  ·  6 October 2026", "Status:",
                  "Prepared from public sources, EEA data and EU legal texts.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Malta’s 2030 effort-sharing gap", version="1.0", date="6 October 2026",
    pdf_title="More in 2030 than in 2005? Claim Check 094",
    pdf_subject="Tests the European Commission's statement that Malta is projected to emit more in 2030 than in 2005 in "
                "effort-sharing sectors",
    story=S))
