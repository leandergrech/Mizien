"""Claim Check 037 report. Run fetch.py, calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []
LG = colors.HexColor("#8DB36B")

REV_11 = ("Corrections: (1) Amphora names no source and links none; the cover, flyer, references and claim record no "
          "longer say it cites Eurostat, and section 1 now says that only the income sentence is attributed, to an "
          "unnamed “report”. Likely source added: Eurostat’s Statistics Explained article (last edited 14 Aug 2025) and "
          "news release (1 Sep 2025) [5, 6]. (2) Sub-claim D re-rated Accurate (official wording): “reporting exposure "
          "to pollution” is Eurostat’s own description of the indicator, so the verdict no longer treats it as a "
          "caveat. (3) Sub-claim E re-rated Largely accurate: the split is above against below 60% of median income, "
          "and the “above” group is 83.4% of people; the direction reversed in 6 of 17 years; EU-wide it runs the other "
          "way (14.0% below, 11.8% above). (4) TL;DR point 4 “Not a recent deterioration” replaced: +8.2 points since "
          "2017, the highest since 2014 (37.4%). (5) The 2021–22 gap explained: the question moved to a three-yearly "
          "EU-SILC module collected in 2023 and 2026 [8–10]; removed from the requests. (6) “Move the verdict up” box: "
          "none (top of the scale); a Eurostat revision or a survey artefact moved to “down”. (7) Unsourced sentence on "
          "density and traffic removed; the indicator is now defined precisely (people living in households where the "
          "respondent reports the problem) [7]. (8) Eurostat flags kept (EU-27 2010–2020 estimated; Germany 2023 low "
          "reliability); Figure 1 no longer bridges 2021–22; Figure 2 labels to one decimal; table note kept with its "
          "table; cover status “draft · no right of reply needed”. Verdict and confidence unchanged.")

# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("Amphora Media’s <i>2026 Election Guidebook: The Environment</i> (12 May 2026) says: <b>“35% of people in Malta "
        "reported exposure to pollution in 2023 — the highest share in the EU.”</b> In the body it adds that this is "
        "“nearly three times the EU average of 12%”. Amphora does not name its source. We tested both statements "
        "against Eurostat’s EU-SILC survey indicator on pollution, grime and other environmental problems.", lead)]
S.append(key_points([
    ("The numbers are right.",
     "Eurostat gives 34.7% for Malta and 12.2% for the EU-27 in 2023. Rounded, that is 35% and 12%; the ratio is 2.84."),
    ("Malta is first in the EU, by a wide margin.",
     "Greece is second at 20.5%. Malta has been first in every survey year with data since 2005 (17 of 17), and in "
     "2023 it was also above every non-EU country in the table (the highest, Türkiye, 19.8%)."),
    ("“Reported exposure” is Eurostat’s own wording.",
     "The survey asks whether the household has a problem with pollution, grime or other environmental problems in "
     "its area. Eurostat describes the result as people “reporting exposure to pollution, grime or other environmental "
     "problems”; Amphora’s intro line shortens that. It records what people report, not measured air quality."),
    ("Up since 2017, below the 2010–14 peak.",
     "The share was 41.4% in 2011 and 26.5% in 2017. At 34.7%, 2023 is 8.2 points above that low and the highest "
     "since 2014 (37.4%)."),
    ("Verdict: supported (high confidence).",
     "The statistic, the rank, the comparison and the wording all match Eurostat. A secondary sentence, that "
     "high earners were more affected, holds for 2023 but is loosely worded (sub-claim E)."),
]))
S += [Spacer(1, 4 * mm), VerdictMeter(0), Spacer(1, 3 * mm),
      tiles([("34.7%", GREEN, "Malta, 2023: reporting pollution, grime or other environmental problems"),
             ("12.2%", GREY, "EU-27 average, 2023"),
             ("1st", GREEN, "Malta’s rank among 27 Member States; Greece second at 20.5%"),
             ("17 of 17", GREEN, "Survey years since 2005 with Malta ranked first")]),
      Spacer(1, 4 * mm),
      up_down("None: Supported is the top of the scale.",
              "A revision of Eurostat’s 2023 figures that removed Malta’s lead, or evidence that the Maltese result "
              "comes from a question, translation or sampling artefact rather than from what residents report."),
      Spacer(1, 5 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the indicator measures"),
          ("4", "What the data show"), ("5", "Where the evidence points different ways"),
          ("6", "Testing the claim"), ("7", "Verdict and requests for evidence"), ("8", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The claim is Amphora Media’s own text, read in full on 5 October 2026 [1]. Amphora is a news outlet; we "
           "assess its wording, not any authority’s. The guidebook names no source for the figures and links none. Only "
           "the income sentence is attributed, to “the report”, which is not named. We identified the Eurostat data "
           "that reproduce the figures [2] and the Eurostat publications that report them in the same terms [5, 6]."))
S.append(std_table([
    [C("What Amphora says", cellh), C("Where", cellh), C("Access", cellh)],
    [C("“35% of people in Malta reported exposure to pollution in 2023 — the highest share in the EU.”"),
     C("Introduction [1]"), C("Read in full; no source given")],
    [C("“In 2023, more than a third of people (35%) in Malta reported exposure to pollution, grime, and other "
       "environmental problems. This is the highest share in the EU and nearly three times the EU average of 12%.”"),
     C("Section “Is Malta becoming cleaner?” [1]"), C("Read in full; no source given")],
    [C("“According to the report, high-earning households were more affected than low-earning ones.”"),
     C("Same section [1]"), C("Read in full; “the report” not named")],
], [104 * mm, 36 * mm, 30 * mm]))
S.append(P("<b>Likely source.</b> Eurostat’s <i>Statistics Explained</i> article on the natural and living environment "
           "(last edited 14 August 2025) says Malta recorded “by far the highest share” (34.7%) of people reporting "
           "exposure to pollution, grime or other environmental problems, and names Malta among nine Member States where "
           "people at risk of poverty reported less (5.5 points lower) [5]. Eurostat’s news release of 1 September 2025 "
           "is headed “12% of EU population reported pollution in their area” [6]. Together they carry all three of "
           "Amphora’s statements. We cannot confirm that Amphora used them."))
S += [Spacer(1, 2 * mm),
      callout([P("SCOPE NOTE", tag),
               P("This check tests the figures and the wording “reported exposure to pollution”. It does not assess "
                 "Malta’s actual air or environmental quality, which is covered by other checks. Amphora’s guidebook "
                 "contains other statements that we did not test here.", small)],
              bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Question.</b> Are the 35%, the “highest in the EU” ranking and the comparison with a 12% EU average "
           "accurate, does “reported exposure to pollution” describe what was measured, and is the income statement "
           "right?"))
S.append(P("<b>Evidence.</b> This claim is statistical. We downloaded Eurostat’s <i>ilc_mddw02</i> (updated 13 August "
           "2026) and the at-risk-of-poverty rate <i>ilc_li02</i> through the dissemination API on 5 October 2026 [2, 11], "
           "kept all Member States, years and Eurostat’s flags, and recomputed rank, ratios, trend and the income split "
           "with <i>tools/cc-037-report/calc.py</i> from <i>data/cc-037/</i>. We read Eurostat’s methodology note for "
           "the indicator [7], its 2025 article and news release [5, 6], and the EU legal acts that set how often the "
           "question is asked [8–10], all on 5 October 2026. Peer-reviewed literature was searched (Crossref, OpenAlex) "
           "for work comparing self-reported pollution with measurements."))
S.append(P("<b>Grades.</b> Official statistics are grade C under our scale. <b>Verdicts</b> follow the five-point scale in "
           "Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(45 * mm))
S.append(SectionHeading(3, "What the indicator measures"))
S.append(P("The indicator comes from the EU Statistics on Income and Living Conditions (EU-SILC), a household survey run by "
           "national statistics offices. One respondent answers for the household: does it have a problem with "
           "“pollution, grime or other environmental problems” in the local area, such as smoke, dust, unpleasant smells "
           "or polluted water? Eurostat then counts every person living in a household where the answer was yes, weighted "
           "to the population of private households; the indicator is that share [7]. It records whether the respondent "
           "considers this a problem for the household, and Eurostat sets no common standard for what counts as one [7]."))
S.append(P("Eurostat’s own publications describe the result as people “reporting exposure to pollution, grime or other "
           "environmental problems” [5] and speak of “self-reported exposure” [5]. Amphora’s wording follows that usage."))
S.append(P("Self-reports and measurement overlap but do not coincide. In one Spanish cohort of 504 pregnant women, "
           "self-reported air-pollution annoyance was associated with modelled NO<sub>2</sub> and VOC levels, but "
           "category-by-category agreement was low to moderate (11–72%) [3]. That is a conference abstract from another "
           "country and is context only."))
S.append(P("Why there are no figures for 2021 and 2022", h2))
S.append(P("Until 2020 the question was asked, and the indicator published, every year. Since 2021 EU-SILC has run "
           "under Regulation (EU) 2019/1700, which collects some items every year and others every three or six years "
           "[8]. The pollution question (variable HS180) is now part of the three-yearly module “Labour market and "
           "housing” [9], which the Commission’s rolling plan schedules for 2023 and 2026 [10]. Eurostat’s release says "
           "the same: the data come from a module “collected every 3 years” [6]. So 2023 is the first year of the new "
           "cycle, and the next figures will be for 2026."))

# ================================================================== 4
S.append(CondPageBreak(100 * mm))
S.append(SectionHeading(4, "What the data show"))
S.append(KeepTogether([fig(FIG / "fig1_trend.png"), P("Figure 1. Population reporting pollution, grime or other environmental problems, Malta and EU-27. Malta’s series "
           "peaked at 41.4% in 2011, fell to 26.5% in 2017 and has risen since; 2023 is the highest since 2014 (37.4%). "
           "The question was not asked in 2021–22. EU-27 values for 2010–2020 are Eurostat estimates (flag e, hollow "
           "markers); Malta’s values carry no flags.", cap)]))
S.append(KeepTogether([fig(FIG / "fig2_rank.png"), P("Figure 2. The same indicator for all 27 Member States, 2023. Malta ranks first. Germany’s value (16.8%) is "
           "flagged by Eurostat as of low reliability.", cap)]))
S.append(KeepTogether([
    std_table([
        [C("Indicator", cellh), C("Malta", cellh), C("EU / comparison", cellh), C("Source", cellh), C("Grade", cellh)],
        [C("Reporting pollution, grime or other problems, 2023"), C("<b>34.7%</b>"), C("12.2% (EU-27)"), C("Eurostat [2]"),
         grade_tag("C")],
        [C("Ratio to EU-27 average, 2023"), C("2.84×"), C("2.92× on the rounded 35% and 12%"), C("calculated"),
         grade_tag("C")],
        [C("Rank among 27 Member States, 2023"), C("1st"), C("Greece 20.5%, Germany 16.8% (low reliability), "
                                                          "France 16.0%"), C("calculated"), grade_tag("C")],
        [C("Years ranked first, 2005–2023"), C("17 of 17"), C("25–27 Member States with data each year"),
         C("calculated"), grade_tag("C")],
        [C("Change since the 2017 low"), C("+8.2 points"), C("26.5% → 34.7%; highest since 2014 (37.4%)"),
         C("calculated"), grade_tag("C")],
        [C("Above / below 60% of median income, 2023"), C("35.6% / 30.1%"), C("11.8% / 14.0% (EU-27)"), C("Eurostat [2]"),
         grade_tag("C")],
        [C("People above 60% of median income, 2023"), C("83.4%"), C("at-risk-of-poverty rate 16.6% (EU-27 16.2%)"),
         C("Eurostat [11]"), grade_tag("C")],
    ], [62 * mm, 26 * mm, 40 * mm, 26 * mm, 16 * mm]),
    P("All values in <i>data/cc-037/checks.csv</i>. Member States with data: 25 in 2005–06 (none for Croatia and "
      "Romania), 26 in 2007–09 (none for Croatia) and in 2020 (none for Poland), 27 in the other years. No data for "
      "2021 and 2022 (section 3).", cap)]))

# ================================================================== 5
S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(5, "Where the evidence points different ways"))
S.append(contested(
    "Q1  Is “reported exposure to pollution” an accurate description?", "ACCURATE; EUROSTAT’S WORDING", GREEN,
    "Eurostat itself describes the indicator as people “reporting exposure to pollution, grime or other environmental "
    "problems” [5]. Amphora’s body text uses the full wording, and “reported” makes clear that this is what people said.",
    "Read alone, “exposure to pollution” could be taken as measured exposure, which the survey does not provide, and "
    "“grime” covers dirt that is not pollution in the regulatory sense.",
    "<b>For this claim:</b> Amphora shortened Eurostat’s wording; it did not change its meaning. Holding a news outlet "
    "to stricter wording than the statistics office uses would not be an even standard, so we give this as context "
    "for readers, not as a flaw in the claim."))
S.append(contested(
    "Q2  Does the ranking reflect real conditions or a survey effect?", "UNCERTAIN; RANKING IS ROBUST", GREEN,
    "Malta has led the EU in all 17 survey years with data, and in 2023 by 14.2 points, so a single year’s sampling "
    "noise does not explain it.",
    "Self-reports can reflect expectations as well as conditions (general context; one study found only partial agreement with measurements [3]), and Eurostat sets no common standard for what counts as a problem [7]. We "
    "found no study that separates these effects for Malta.",
    "<b>For this claim:</b> the rank is accurate as a statement about reports. Causes are outside this check."))

# ================================================================== 6
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(6, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> 35% of people in Malta reported pollution in 2023"),
     C("Eurostat: 34.7% [2]."), verd("ACCURATE", GREENC)],
    [C("<b>B.</b> The highest share in the EU"),
     C("First of 27; Greece second at 20.5%; first in all 17 years with data [2]."), verd("ACCURATE", GREENC)],
    [C("<b>C.</b> Nearly three times the EU average of 12%"),
     C("12.2% EU-27; ratio 2.84 (2.9 on the rounded figures) [2]."), verd("ACCURATE", GREENC)],
    [C("<b>D.</b> “Exposure to pollution” (intro wording)"),
     C("Eurostat’s own wording, shortened: it describes the indicator as people “reporting exposure to pollution, "
       "grime or other environmental problems” [5]. The survey records reported problems, not measured exposure [7]."),
     verd("ACCURATE (OFFICIAL WORDING)", GREENC)],
    [C("<b>E.</b> High earners more affected than low earners"),
     C("2023: 35.6% above vs 30.1% below 60% of median income [2]. But the “above” group is 83.4% of people, not "
       "high earners [11]; the gap reversed in 6 of 17 years; EU-wide it runs the other way."),
     verd("LARGELY ACCURATE", LG)],
], [62 * mm, 78 * mm, 30 * mm], valign="MIDDLE"))
S.append(Spacer(1, 3 * mm))
S.append(P("<b>The income sentence (E).</b> Eurostat splits the indicator at 60% of median equivalised income, the "
           "at-risk-of-poverty line, not by earnings bands [7]. In Malta in 2023, 16.6% of people were below that line "
           "[11], so the “above” group is 83.4% of the population; most of it is not “high-earning”. For 2023 the "
           "direction Amphora gives is right, and Eurostat notes it: Malta is one of nine Member States where people at "
           "risk of poverty reported less (5.5 points lower) [5]. It is not a stable pattern: in 6 of the 17 survey years "
           "(2006, 2007, 2009, 2010, 2016 and 2018) people below the line reported more. Across the EU-27 the pattern runs "
           "the other way (14.0% below, 11.8% above, 2023) [2]. Eurostat’s article gave 14.1% and 11.9% from an earlier "
           "extraction [5]."))

# ================================================================== 7
S += [CondPageBreak(80 * mm), Spacer(1, 6 * mm), SectionHeading(7, "Verdict and requests for evidence"),
      verdict_box("Supported", "The figures, rank, comparison and wording match Eurostat’s data and Eurostat’s own "
                  "description of them. Confidence: high."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) The 35%, the first place in the EU and the comparison with the EU average all reproduce from "
           "Eurostat’s own data. (2) The result is stable across 17 survey years. (3) “Reported exposure to pollution” "
           "is Eurostat’s own description of the indicator, shortened; it is context for readers, not a flaw in the "
           "statement. (4) Confidence is high because the data, Eurostat’s methodology note and its own publications "
           "agree. The verdict applies to the claim under review, the intro line and its restatement in the body. The "
           "income sentence is a separate statement, rated on its own (E)."))
S.append(P("<b>What this verdict does not say.</b> It does not say that Malta’s measured pollution is the highest "
           "in the EU, that any particular source is to blame, or that any authority has failed. It addresses only "
           "whether Amphora’s statement is accurate."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "The source Amphora refers to as “the report” for the income split, and the source of the 35% (neither is named "
    "in the guidebook).",
    "Measured exposure data (EEA air quality, noise maps) that could be set beside this perception indicator in a future check.",
]))

# ================================================================== 8
S += [Spacer(1, 6 * mm), SectionHeading(8, "Limitations")]
for l in ["The indicator is self-reported and cannot be read as measured exposure.",
          "We did not compare it with measured concentrations in Malta; no such comparison was part of the claim.",
          "The question was not asked in 2021–2022 (three-yearly module since 2021); 2023 is the latest year and the "
          "next is 2026.",
          "Amphora names no source; the match to Eurostat’s data and publications is ours, through the figures (35%, "
          "12%, the income split).",
          "Eurostat flags the EU-27 values for 2010–2020 as estimates and Germany’s 2023 value as of low reliability; "
          "Malta’s values carry no flags.",
          "The Aguilera abstract [3] is a conference abstract from Spain; it was read as an abstract only and is context."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Amphora Media (12 May 2026). 2026 Election Guidebook: The Environment. (Read in full, 5 Oct 2026; no "
          "source named.)", "https://www.amphora.media/2026/05/2026-election-guidebook-the-environment"),
    ("2", "Eurostat. ilc_mddw02 Pollution, grime or other environmental problems (EU-SILC); updated 13 Aug 2026, "
          "retrieved 5 Oct 2026, with flags. doi:10.2908/ILC_MDDW02.",
     "https://ec.europa.eu/eurostat/databrowser/view/ilc_mddw02/default/table"),
    ("3", "Aguilera I., Sunyer J., Fernández-Patier R., Jacquemin B., Aguirre A., Bomboi T. (2007). Self-reported traffic, air "
          "pollution annoyance, and GIS-modeled exposure to air pollutants in pregnant women. <i>Epidemiology</i> "
          "18(5):S43. doi:10.1097/01.ede.0000276553.96485.21. (Conference abstract read.)",
     "https://doi.org/10.1097/01.ede.0000276553.96485.21"),
    ("4", "Miżien. Data and calculations: data/cc-037/; tools/cc-037-report/calc.py.", ""),
    ("5", "Eurostat. Quality of life indicators – natural and living environment. Statistics Explained; last edited "
          "14 Aug 2025 (data from March 2025). Read 5 Oct 2026.",
     "https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Quality_of_life_indicators_-_natural_and_living_environment"),
    ("6", "Eurostat (1 Sep 2025). 12% of EU population reported pollution in their area. Eurostat news. Read 5 Oct 2026.",
     "https://ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-20250901-1"),
    ("7", "Eurostat. EU statistics on income and living conditions (EU-SILC) methodology – environment of the dwelling. "
          "Statistics Explained; last edited 10 Aug 2023. Read 5 Oct 2026.",
     "https://ec.europa.eu/eurostat/statistics-explained/index.php?title=EU_statistics_on_income_and_living_conditions_(EU-SILC)_methodology_-_environment_of_the_dwelling"),
    ("8", "Regulation (EU) 2019/1700 of the European Parliament and of the Council of 10 October 2019 (IESS framework "
          "regulation), Annex IV point 2. OJ L 261I, 14.10.2019, p. 1. Read via the EU Publications Office, 5 Oct 2026.",
     "https://data.europa.eu/eli/reg/2019/1700/oj"),
    ("9", "Commission Delegated Regulation (EU) 2022/29 of 28 October 2021 (variables on labour market and housing), "
          "Annex: HS180. OJ L 7, 12.1.2022, p. 1. Read via the EU Publications Office, 5 Oct 2026.",
     "https://data.europa.eu/eli/reg_del/2022/29/oj"),
    ("10", "Commission Delegated Regulation (EU) 2020/256 of 16 December 2019 (multiannual rolling planning), Annex I. "
           "OJ L 54, 26.2.2020, p. 1. Read via the EU Publications Office, 5 Oct 2026.",
     "https://data.europa.eu/eli/reg_del/2020/256/oj"),
    ("11", "Eurostat. ilc_li02 At-risk-of-poverty rate by poverty threshold, age and sex (EU-SILC); updated 17 Sep 2026, "
           "retrieved 5 Oct 2026.", "https://ec.europa.eu/eurostat/databrowser/view/ilc_li02/default/table"),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "5 Oct 2026", "First issue. No right of reply needed for a Supported verdict."),
                   ("1.1", "5 Oct 2026", REV_11),
                   ("1.2", "6 Oct 2026", "Clarification after the 6 Oct 2026 audit: an unsourced sentence on perception reworded as general context, tied to the cited study [3]. Verdict unchanged; no right of reply needed.")])

build_report(Report(
    number="037", out=str(FIG / "report.pdf"), kicker="Statistics and EU surveys",
    title_lines=["Is Malta first", "in the EU for", "reported pollution?"],
    subtitle_lines=["Testing a media claim about Malta’s share of people", "reporting pollution against Eurostat data"],
    quote_lines=["“35% of people in Malta reported exposure to pollution", "in 2023 — the highest share in the EU.”"],
    quote_size=14,
    attribution="Amphora Media, 2026 Election Guidebook: The Environment, 12 May 2026.",
    context="Source not named; the figures match Eurostat’s EU-SILC data.",
    verdict="Supported", verdict_note="Accurate; reported problems, in Eurostat’s own words",
    footer_lines=["Version 1.2  ·  6 October 2026", "Status:",
                  "Prepared from public sources and Eurostat data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Reported pollution in Malta and the EU", version="1.2", date="6 October 2026",
    pdf_title="Is Malta first in the EU for reported pollution? Claim Check 037",
    pdf_subject="Tests Amphora Media's statement that 35% of people in Malta reported pollution in 2023, the highest share in the EU",
    story=S))
