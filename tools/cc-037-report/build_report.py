"""Claim Check 037 report. Run calc.py and figures.py first. Output: out/report.pdf"""
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
      P("Amphora Media’s <i>2026 Election Guidebook: The Environment</i> (12 May 2026) says: <b>“35% of people in Malta "
        "reported exposure to pollution in 2023 — the highest share in the EU.”</b> In the body it adds that this is "
        "“nearly three times the EU average of 12%”. Amphora does not name its source. We tested both statements "
        "against Eurostat’s EU-SILC survey indicator on pollution, grime and other environmental problems.", lead)]
S.append(key_points([
    ("The numbers are right.",
     "Eurostat gives 34.7% for Malta and 12.2% for the EU-27 in 2023. Rounded, that is 35% and 12%; the ratio is 2.8."),
    ("Malta is first in the EU, by a wide margin.",
     "Greece is second at 20.5%. Malta has been first in every survey year with data since 2005 (17 of 17)."),
    ("It measures what people report, not what is measured in the air.",
     "The survey asks whether the household has a problem with pollution, grime or other environmental problems in "
     "its area. Amphora’s body text says this (“pollution, grime, and other environmental problems”); the intro "
     "line says “exposure to pollution”, which reads as a stronger, measured claim."),
    ("Not a recent deterioration.",
     "The share peaked at 41.4% in 2011 and reached a low of 26.5% in 2017; 2023 is 8 points above that low."),
    ("Verdict: supported (high confidence).",
     "The statistic, the rank and the comparison are accurate. The caveat is the label: this is perceived, "
     "self-reported pollution."),
]))
S += [Spacer(1, 4 * mm), VerdictMeter(0), Spacer(1, 3 * mm),
      tiles([("34.7%", GREEN, "Malta, 2023: reporting pollution, grime or other environmental problems"),
             ("12.2%", GREY, "EU-27 average, 2023"),
             ("1st", GREEN, "Malta’s rank among 27 Member States; Greece second at 20.5%"),
             ("17 of 17", GREEN, "Survey years since 2005 with Malta ranked first")]),
      Spacer(1, 4 * mm),
      up_down("A correction of the Eurostat figures (revised data), or evidence that the Maltese result reflects "
              "a question or sampling difference rather than the experience of residents.",
              "Measured exposure data (EEA air-quality and noise maps) showing Malta’s exposure is not elevated, "
              "which would turn this into a perception-only statistic that the intro line overstates."),
      Spacer(1, 5 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the indicator measures"),
          ("4", "What the data show"), ("5", "Where the evidence points different ways"),
          ("6", "Testing the claim"), ("7", "Verdict and requests for evidence"), ("8", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The claim is Amphora Media’s own text, read in full on 5 October 2026 [1]. Amphora is a news outlet; we "
           "assess its wording, not any authority’s. It attributes the figure to “the report” without naming it, so we "
           "identified the Eurostat series that reproduces it [2]."))
S.append(std_table([
    [C("What Amphora says", cellh), C("Where", cellh), C("Access", cellh)],
    [C("“35% of people in Malta reported exposure to pollution in 2023 — the highest share in the EU.”"),
     C("Introduction [1]"), C("Read in full")],
    [C("“In 2023, more than a third of people (35%) in Malta reported exposure to pollution, grime, and other "
       "environmental problems. This is the highest share in the EU and nearly three times the EU average of 12%.”"),
     C("Section “Is Malta becoming cleaner?” [1]"), C("Read in full")],
    [C("“According to the report, high-earning households were more affected than low-earning ones.”"),
     C("Same section [1]"), C("Read in full; source report not named")],
], [104 * mm, 36 * mm, 30 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("SCOPE NOTE", tag),
               P("This check tests the figures and the wording “reported exposure to pollution”. It does not assess "
                 "Malta’s actual air or environmental quality, which is covered by other checks. Amphora’s guidebook "
                 "contains other statements that we did not test here.", small)],
              bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Question.</b> Are the 35%, the “highest in the EU” ranking and the comparison with a 12% EU average "
           "accurate, and does “reported exposure to pollution” describe what was measured?"))
S.append(P("<b>Evidence.</b> This claim is statistical. We downloaded Eurostat’s <i>ilc_mddw02</i> (updated 13 August "
           "2026) through the dissemination API on 5 October 2026 [2], kept all Member States and years, and recomputed rank, "
           "ratios and trend with <i>tools/cc-037-report/calc.py</i> from <i>data/cc-037/</i>. Peer-reviewed literature was "
           "searched (Crossref, OpenAlex) for work comparing self-reported pollution with measurements."))
S.append(P("<b>Grades.</b> Official statistics are grade C under our scale. <b>Verdicts</b> follow the five-point scale in "
           "Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(90 * mm))
S.append(SectionHeading(3, "What the indicator measures"))
S.append(P("The indicator comes from the EU Statistics on Income and Living Conditions (EU-SILC), a household survey run by "
           "national statistics offices. Respondents say whether their dwelling or its surroundings have a problem with "
           "“pollution, grime or other environmental problems”. The indicator is the percentage answering yes [2]. It "
           "records perceived problems, which depend on what people notice and tolerate as well as on the environment."))
S.append(P("Self-reports and measurement overlap but do not coincide. In one Spanish cohort of 504 pregnant women, "
           "self-reported air-pollution annoyance was associated with modelled NO<sub>2</sub> and VOC levels, but "
           "category-by-category agreement was low to moderate (11–72%) [3]. That is a conference abstract from another "
           "country and is context only. It supports the caution in the verdict, not the numbers."))

# ================================================================== 4
S.append(CondPageBreak(150 * mm))
S.append(SectionHeading(4, "What the data show"))
S.append(fig(FIG / "fig1_trend.png"))
S.append(P("Figure 1. Population reporting pollution, grime or other environmental problems, Malta and EU-27. Malta’s series "
           "peaked at 41.4% in 2011, fell to 26.5% in 2017 and has risen since.", cap))
S.append(fig(FIG / "fig2_rank.png"))
S.append(P("Figure 2. The same indicator for all 27 Member States, 2023. Malta ranks first.", cap))
S.append(std_table([
    [C("Indicator", cellh), C("Malta", cellh), C("EU / comparison", cellh), C("Source", cellh), C("Grade", cellh)],
    [C("Reporting pollution, grime or other problems, 2023"), C("<b>34.7%</b>"), C("12.2% (EU-27)"), C("Eurostat [2]"), grade_tag("C")],
    [C("Ratio to EU-27 average, 2023"), C("2.84×"), C("–"), C("calculated"), grade_tag("C")],
    [C("Rank among 27 Member States, 2023"), C("1st"), C("next: Greece 20.5%"), C("calculated"), grade_tag("C")],
    [C("Years ranked first, 2005–2023"), C("17 of 17"), C("–"), C("calculated"), grade_tag("C")],
    [C("Above / below 60% of median income, 2023"), C("35.6% / 30.1%"), C("11.8% / 14.0% (EU-27)"), C("Eurostat [2]"), grade_tag("C")],
], [62 * mm, 28 * mm, 36 * mm, 28 * mm, 16 * mm]))
S.append(P("All values in <i>data/cc-037/checks.csv</i>. No data exist for 2021 and 2022. Amphora’s statement that "
           "higher earners were more affected agrees with the income split.", cap))

# ================================================================== 5
S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(5, "Where the evidence points different ways"))
S.append(contested(
    "Q1  Is “reported exposure to pollution” an accurate description?", "ACCURATE IN THE BODY, LOOSER IN THE INTRO", AMBER,
    "The body text uses the survey’s wording: “pollution, grime, and other environmental problems”. “Reported” makes clear that "
    "this is what people said.",
    "The intro line shortens this to “exposure to pollution”. A reader could take that as measured exposure, which the "
    "survey does not provide, and “grime” covers dirt that is not pollution in the regulatory sense.",
    "<b>For this claim:</b> the statistic is accurate; the shorthand slightly widens its meaning."))
S.append(contested(
    "Q2  Does the ranking reflect real conditions or a survey effect?", "UNCERTAIN; RANKING IS ROBUST", GREEN,
    "Malta has led the EU for 17 survey years with a gap of 14 points in 2023, so a single year’s sampling noise does not "
    "explain it. Malta’s density and traffic are consistent with high reporting.",
    "Perception varies with expectations, and national survey practice differs. We found no study that separates "
    "these for Malta.",
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
     C("The survey records perceived problems, not measured exposure [2, 3]."), verd("LOOSE WORDING", LG)],
    [C("<b>E.</b> High earners more affected than low earners"),
     C("35.6% above vs 30.1% below 60% of median income [2]."), verd("ACCURATE", GREENC)],
], [62 * mm, 78 * mm, 30 * mm], valign="MIDDLE"))

# ================================================================== 7
S += [CondPageBreak(80 * mm), Spacer(1, 6 * mm), SectionHeading(7, "Verdict and requests for evidence"),
      verdict_box("Supported", "The figures, rank and comparison are accurate; they describe reported problems, not "
                  "measured exposure. Confidence: high."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) The 35%, the first place in the EU and the comparison with the EU average all reproduce from "
           "Eurostat’s own data. (2) The result is stable across 17 survey years. (3) The only caveat is that the "
           "indicator is self-reported; Amphora’s body text says “reported”, and our scale treats a caveat of that size as "
           "not altering the substance of a statement."))
S.append(P("<b>What this verdict does not say.</b> It does not say that Malta’s measured pollution is the highest "
           "in the EU, that any particular source is to blame, or that any authority has failed. It addresses only "
           "whether Amphora’s statement is accurate."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "The source Amphora refers to as “the report” for the 35% and the income split (not named in the guidebook).",
    "Measured exposure data (EEA air quality, noise maps) that could be set beside this perception indicator in a future check.",
]))

# ================================================================== 8
S += [Spacer(1, 6 * mm), SectionHeading(8, "Limitations")]
for l in ["The indicator is self-reported and cannot be read as measured exposure.",
          "We did not compare it with measured concentrations in Malta; no such comparison was part of the claim.",
          "No data exist for 2021–2022; 2023 is the latest year.",
          "We could not identify the report Amphora cites; the match to Eurostat <i>ilc_mddw02</i> is ours, through "
          "the figures (35%, 12%, income split).",
          "The Aguilera abstract [3] is a conference abstract from Spain; it was read as an abstract only and is context."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Amphora Media (12 May 2026). 2026 Election Guidebook: The Environment. (Read in full, 5 Oct 2026.)",
     "https://www.amphora.media/2026/05/2026-election-guidebook-the-environment"),
    ("2", "Eurostat. ilc_mddw02 Pollution, grime or other environmental problems (EU-SILC); updated 13 Aug 2026, "
          "retrieved 5 Oct 2026.", "https://ec.europa.eu/eurostat/databrowser/view/ilc_mddw02/default/table"),
    ("3", "Aguilera I., Sunyer J., Fernández-Patier R., Jacquemin B., Aguirre A., Bomboi T. (2007). Self-reported traffic, air "
          "pollution annoyance, and GIS-modeled exposure to air pollutants in pregnant women. <i>Epidemiology</i> 18:S43. "
          "doi:10.1097/01.ede.0000276553.96485.21. (Conference abstract read.)",
     "https://doi.org/10.1097/01.ede.0000276553.96485.21"),
    ("4", "Miżien. Data and calculations: data/cc-037/; tools/cc-037-report/calc.py.", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "5 Oct 2026", "First issue. No right of reply needed for a Supported verdict.")])

build_report(Report(
    number="037", out=str(FIG / "report.pdf"), kicker="Statistics and EU surveys",
    title_lines=["Is Malta first", "in the EU for", "reported pollution?"],
    subtitle_lines=["Testing a media claim about Malta’s share of people", "reporting pollution against Eurostat data"],
    quote_lines=["“35% of people in Malta reported exposure to pollution", "in 2023 — the highest share in the EU.”"],
    quote_size=14,
    attribution="Amphora Media, 2026 Election Guidebook: The Environment, 12 May 2026.",
    context="Citing Eurostat (series not named).",
    verdict="Supported", verdict_note="Accurate; it measures reported problems, not measured exposure",
    footer_lines=["Version 1.0  ·  5 October 2026", "Status: published, no right of reply needed (Supported)",
                  "Prepared from public sources and Eurostat data.", "Repository: github.com/leandergrech/Mizien"],
    status_note="no right of reply needed (Supported)",
    running_head="Reported pollution in Malta and the EU", version="1.0", date="5 October 2026",
    pdf_title="Is Malta first in the EU for reported pollution? Claim Check 037",
    pdf_subject="Tests Amphora Media's statement that 35% of people in Malta reported pollution in 2023, the highest share in the EU",
    story=S))
