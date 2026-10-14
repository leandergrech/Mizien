"""Claim Check 120 report. Run calc.py and figures.py first. Output: out/report.pdf"""
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
      P("A study for the European Parliament’s Committee on Petitions (February 2026) reports that "
        "<b>“An estimated 54 000 inhabitants of Malta are being exposed to road noise levels over 55dB (Lden), compared to "
        "11 100 in the case of aircraft noise levels.”</b> It adds that the road figure is likely a considerable underestimate and "
        "that Malta has the lowest number of noise-related premature deaths a year (not per capita) and among the lowest DALYs per "
        "capita in the EU. We traced each figure to the European Environment Agency (EEA) report the study relies on.", lead)]
S.append(key_points([
    ("The exposure figures are exactly the EEA’s.",
     "54,000 people on roads and 11,100 for aircraft above 55 dB Lden are in the EEA’s country table (Table 2.1). "
     "Roads affect about 5 times as many people as aircraft."),
    ("‘Underestimate’ is the EEA’s caution, applied to Malta.",
     "The EEA says its findings “likely represent a considerable underestimation” because the Directive covers only major "
     "infrastructure and large agglomerations. It does not quantify this for Malta, and neither do we."),
    ("The ‘lowest deaths’ claim holds, as an absolute count.",
     "30 premature deaths a year in the EEA’s current table (the study quotes 20; the EEA corrected its figures after the study), the lowest of 27; the next is Estonia with 80. "
     "Per head Malta is second-lowest (5.8 per 100,000)."),
    ("‘Among the lowest DALYs’ holds on the Directive’s thresholds only.",
     "Malta’s 150 DALYs per 100,000 is the 4th-lowest of 27 (tied). On the EEA’s WHO-level estimate it is 310, "
     "11th lowest and below the median."),
    ("Verdict: largely supported (moderate confidence).",
     "The figures trace to the EEA; the caveats are the study’s outdated health numbers, an unquantified underestimate and the "
     "dependence of the DALY ranking on the threshold used."),
]))
S += [Spacer(1, 4 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("54,000", GREEN, "People exposed to road noise above 55 dB Lden: matches the EEA table"),
             ("1st", GREEN, "Lowest number of premature deaths a year among 27 (30; Estonia next at 80)"),
             ("4th", ORANGE, "Lowest DALYs per 100,000 on END thresholds (tied); 11th on WHO levels"),
             ("30 vs 20", AMBER, "Deaths a year: EEA corrected table against the study’s figure")]),
      Spacer(1, 4 * mm),
      up_down("A study version using the corrected EEA health numbers and stating the WHO-basis result would make this ‘Supported’.",
              "Evidence that Malta’s END reporting is incomplete in a way that changes the ranking, or a corrected EEA table "
              "that moves Malta out of the lowest group."),
      Spacer(1, 5 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the sources say"),
          ("4", "What the data show"), ("5", "Where the evidence points different ways"),
          ("6", "Testing the claim"), ("7", "Verdict and requests for evidence"), ("8", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The statements are in the key findings of the study by Peter Hjerp and Clare Coffey (Ecocentric Consulting), "
           "commissioned by the European Parliament’s Committee on Petitions, PE 783.089, February 2026 [1]. We read the full "
           "text. The opinions are the authors’, not the Parliament’s official position. The study takes the numbers from the EEA "
           "report <i>Environmental noise in Europe 2025</i> [2], which we also read, so this check tests the study’s Malta figures "
           "against their source."))
S.append(std_table([
    [C("What the study says", cellh), C("Where", cellh), C("Access", cellh)],
    [C("“An estimated 54 000 inhabitants of Malta are being exposed to road noise levels over 55dB (Lden), compared to 11 100 "
       "in the case of aircraft noise levels.”"), C("Key findings, p. 14 [1]"), C("Read in full")],
    [C("The road number “is likely to be a considerable underestimation” because the Directive “only covers major road, rail and "
       "airport infrastructures and agglomerations of more than 100,000 inhabitants”."), C("Key findings; s. 2.3 [1]"),
     C("Read in full")],
    [C("“Malta has the lowest number of noise related premature deaths/year rate (not per capita).”"), C("Key findings [1]"),
     C("Read in full")],
    [C("“It has among the lowest noise related DALYs (per capita) of all EU Member States.”"), C("Key findings [1]"),
     C("Read in full")],
], [104 * mm, 34 * mm, 32 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("SCOPE NOTE", tag),
               P("This check tests the study’s numbers and rankings against the EEA’s tables. It is separate from CC-020, which "
                 "tests the same study’s conclusion on the Directive’s transposition, and does not assess any person or authority. "
                 "A DALY is a disability-adjusted life year: one year of healthy life lost, a measure combining illness and early death.",
                 small)], bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Question.</b> Are the study’s Malta figures and rankings correct, and what do they leave out?"))
S.append(P("<b>Evidence.</b> The EEA report’s country tables for people exposed (Table 2.1, p. 23–24), and for premature deaths and "
           "DALYs per 100,000 people based on the Directive’s thresholds (Table 3.7, p. 58) and on WHO levels (Table 3.12, p. 64) [2]; "
           "Eurostat population on 1 January 2022 [3] to put counts on a per-head basis; Eurostat’s survey indicator on street and "
           "neighbour noise for context [4]. Numbers are recomputed by <i>tools/cc-120-report/calc.py</i> from <i>data/cc-120/</i>. "
           "Ranks are among the 27 Member States; ties share the best rank."))
S.append(P("<b>Grades.</b> The EEA tables are modelled estimates from official country reports (grade C, regulator report); the study is a "
           "commissioned expert report (grade C). No peer-reviewed paper is needed to reproduce the figures, and we did not "
           "re-derive the EEA’s exposure–response model. <b>Verdicts</b> follow the five-point scale in Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(90 * mm))
S.append(SectionHeading(3, "What the sources say"))
S.append(P("The Environmental Noise Directive requires Member States to report how many people live above 55 dB Lden (day-evening-night "
           "average) and 50 dB Lnight for major roads, railways, airports and agglomerations above 100,000 inhabitants [1, 2]. It sets "
           "no limit values. The EEA states that its assessment “does not fully account for all urban areas, roads, railways, airports, or "
           "other noise sources” and that its findings “likely represent a considerable underestimation of the true impact” [2, s. 1.4, p. 20]. "
           "That sentence refers to Europe-wide findings; the study applies it to Malta’s road number."))
S.append(P("The EEA cautions that “results from various countries might not be directly comparable”, because countries differ in network "
           "coverage within urban areas and in modelling detail [2, s. 1.5]. This applies to every ranking below. The EEA’s health "
           "figures were corrected: the report’s page states that an error in several health estimates, found after publication in June 2025, "
           "was corrected in the online version on 27 March 2026 [2]. The study (February 2026) predates the correction."))
S.append(P("The study draws Malta’s health figures from the EEA’s June 2025 table and says the DALY figure “may suggest Malta is bucking a trend” of small, "
           "dense countries having higher health impacts [1, p. 18]. We did not open the June 2025 version; the difference between "
           "the study’s 20 deaths and 100 DALYs per 100,000 and the corrected 30 and 150 is consistent with the EEA’s correction, "
           "but we cannot confirm the cause."))
S.append(fig(FIG / "fig3_roadshare.png"))
S.append(P("Figure 1. People reported as exposed to road noise above 55 dB Lden as a share of population. Malta (10.4%) is 6th lowest of 27, "
           "above Slovakia (6.3%) and Portugal (6.8%). These are reported, not measured, exposures [2].", cap))

# ================================================================== 4
S.append(CondPageBreak(150 * mm))
S.append(SectionHeading(4, "What the data show"))
S.append(P("Malta’s road number is 54,000 and its aircraft number 11,100 in the EEA table, identical to the study. Together with "
           "no railways, 65,100 people (13% of the population) are above the Directive’s Lden threshold; for the night "
           "indicator the figure is 37,400 (7%) [2]. Absolute health burdens are small because the population is small."))
S.append(fig(FIG / "fig1_deaths.png"))
S.append(P("Figure 2. Estimated premature deaths a year from transport noise above the Directive’s thresholds, 27 Member States, lowest "
           "values labelled. Malta has 30, the lowest; the next are Estonia (80) and Slovenia (150).", cap))
S.append(fig(FIG / "fig2_dalys.png"))
S.append(P("Figure 3. DALYs per 100,000 people a year, on the Directive’s thresholds (the study’s basis) and on WHO 2018 recommended levels. "
           "Malta ranks 4th lowest on the first (tied with Greece and Slovenia) and 11th on the second.", cap))
DT = []
DT.append(std_table([
    [C("Indicator", cellh), C("Malta", cellh), C("Comparison", cellh), C("Source", cellh), C("Grade", cellh)],
    [C("Road, Lden ≥ 55 dB / aircraft"), C("<b>54,000 / 11,100</b>"), C("study: same"), C("EEA Table 2.1 [2]"), grade_tag("C")],
    [C("Premature deaths a year (END basis)"), C("<b>30</b> (rank 1)"), C("Study: 20; next: Estonia 80"), C("EEA Table 3.7 [2]"), grade_tag("C")],
    [C("Deaths per 100,000 (END basis)"), C("5.8 (rank 2)"), C("lowest: Slovakia 5.3"), C("calculated [2, 3]"), grade_tag("C")],
    [C("DALYs per 100,000 (END basis)"), C("<b>150</b> (rank 4, tied)"), C("Study: 100; lowest: Portugal 110"), C("EEA Table 3.7 [2]"), grade_tag("C")],
    [C("DALYs per 100,000 (WHO levels)"), C("310 (rank 11)"), C("EU median 350; lowest: Slovakia 140"), C("EEA Table 3.12 [2]"), grade_tag("C")],
    [C("Street or neighbour noise, 2023 (survey)"), C("31.3%"), C("EU-27 18.1%; Malta 1st"), C("Eurostat ilc_mddw01 [4]"), grade_tag("C")],
], [58 * mm, 30 * mm, 38 * mm, 32 * mm, 12 * mm]))
DT.append(P("All values in <i>data/cc-120/checks.csv</i>. Ranks use 27 Member States; 1 = lowest burden. The survey row measures perceived noise "
            "from all sources and is not part of the study’s claim.", cap))
S.append(KeepTogether(DT))

# ================================================================== 5
S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(5, "Where the evidence points different ways"))
S.append(contested(
    "Q1  Is Malta’s noise burden among the lowest in the EU?", "DEPENDS ON THE THRESHOLD", AMBER,
    "On the Directive’s reporting thresholds Malta has the fewest premature deaths, the second-lowest rate per head and the 4th-lowest "
    "DALY rate of 27.",
    "On WHO’s recommended levels, which the EEA also tabulates, Malta’s DALY rate is 310, 11th lowest and below the EU median of 350, and its "
    "death rate per head ranks 9th.",
    "<b>For this claim:</b> the study’s statement is correct on its stated (Directive) basis; it does not say that on WHO levels Malta is mid-table."))
S.append(contested(
    "Q2  Does low modelled exposure mean little noise?", "NOT WHAT THE DATA SAY", AMBER,
    "The Directive-based figures show Malta with a low share of people exposed to road noise (10.4%, 6th lowest) and the study notes "
    "Malta has the lowest share of urban inhabitants exposed.",
    "Eurostat’s household survey puts Malta first in the EU for noise from neighbours or the street (31.3% against 18.1%) [4], and the study "
    "itself says END-covered sources are not “necessarily the main focus or cause of Maltese noise complaints”.",
    "<b>For this claim:</b> the numbers describe Directive-covered noise only; they are not a measure of how noisy Malta is."))
S.append(contested(
    "Q3  Are the study’s health figures current?", "OUTDATED FIGURES, SAME RANKS", AMBER,
    "The study cites 20 deaths and 100 DALYs per 100,000 for Malta.",
    "The EEA’s corrected table now shows 30 and 150. Malta is still lowest for deaths and, using either set of values, 1st or 4th for DALYs "
    "(1st with 100; tied 4th with 150).",
    "<b>For this claim:</b> the claim’s direction survives, but the numbers need updating, and with 150 Malta no longer stands alone at the bottom."))

# ================================================================== 6
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(6, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> 54,000 exposed to road noise and 11,100 to aircraft noise above 55 dB Lden"),
     C("Both figures are in the EEA’s Table 2.1 for Malta [2]. Reported counts of exposed people, from Malta’s END reporting."),
     verd("SUPPORTED", GREENC)],
    [C("<b>B.</b> The road figure is likely a considerable underestimate"),
     C("The EEA says the Directive’s coverage limits mean its findings likely understate the true impact [2, s. 1.4]; the study applies "
       "this to Malta. The size for Malta is not quantified."),
     verd("LARGELY SUPPORTED", LG)],
    [C("<b>C.</b> Malta has the lowest number of premature deaths a year (not per capita)"),
     C("30 against Estonia 80, the lowest of 27 [2]; the study’s 20 is superseded. The study correctly says this is not per capita."),
     verd("SUPPORTED", GREENC)],
    [C("<b>D.</b> Malta has among the lowest DALYs per capita of the Member States"),
     C("4th lowest of 27 on END thresholds (tied); 11th lowest on WHO levels, below the median [2]. The study quotes 100, the EEA now shows 150."),
     verd("LARGELY SUPPORTED", LG)],
], [52 * mm, 88 * mm, 30 * mm], valign="MIDDLE"))

# ================================================================== 7
S += [Spacer(1, 6 * mm), SectionHeading(7, "Verdict and requests for evidence"),
      verdict_box("Largely supported", "The figures trace to the EEA and the rankings hold; the study’s health numbers are outdated "
                  "and the DALY ranking depends on the threshold. Confidence: moderate."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) The exposure numbers are the EEA’s own. (2) Malta is lowest for absolute premature deaths and among the "
           "lowest per head on the Directive’s basis, as the study says. (3) The caveats are that the study’s health figures predate the "
           "EEA’s correction, the underestimate for Malta is not quantified, and on WHO levels Malta is mid-table. These do not change "
           "the substance, which our scale calls <i>Largely supported</i>."))
S.append(P("<b>What this verdict does not say.</b> It does not say that Malta is quiet, that the Directive’s thresholds protect health, or that "
           "the modelled health burden is exact. It addresses only whether the study’s figures and rankings are what the EEA data show."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "The EEA’s June 2025 table, to confirm that the study’s 20 deaths and 100 DALYs come from it.",
    "Malta’s noise-mapping coverage under Round 4, to size the underestimate for roads.",
    "Health-impact estimates for Malta below the Directive’s thresholds, if the EEA publishes them by country.",
]))

# ================================================================== 8
S += [Spacer(1, 6 * mm), SectionHeading(8, "Limitations")]
for l in ["Health burdens are modelled by the EEA from exposure–response relationships; we did not re-derive them, and small countries’ values are rounded to the nearest 10.",
          "Countries differ in noise-mapping detail and coverage, so cross-country ranks are indicative [2, s. 1.5].",
          "Per-head deaths use Eurostat’s population on 1 January 2022 and the EEA’s counts; the EEA’s own reference population may differ slightly.",
          "We read the EEA report as published on 27 March 2026 (the corrected version). The June 2025 version was not opened, so why the study’s numbers differ is inferred.",
          "The ‘considerable underestimation’ wording is the EEA’s statement about its assessment as a whole; we did not find a Malta-specific estimate."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Hjerp P., Coffey C. (2026). Analysing Malta’s implementation of Directive 2002/49/EC on the Assessment and "
          "Management of Environmental Noise. European Parliament, PE 783.089. doi:10.2861/6278624. (Read in full.)",
     "https://doi.org/10.2861/6278624"),
    ("2", "European Environment Agency (2025; online version corrected 27 Mar 2026). Environmental noise in Europe 2025. EEA Report 05/2025. "
          "doi:10.2800/5134480 (resolves via doi.org; not in Crossref). Tables 2.1, 3.7, 3.12; sections 1.4–1.5. (Read; CC BY 4.0.)",
     "https://www.eea.europa.eu/en/analysis/publications/environmental-noise-in-europe-2025"),
    ("3", "Eurostat. demo_pjan Population on 1 January by age and sex; retrieved 14 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/demo_pjan"),
    ("4", "Eurostat. ilc_mddw01 Noise from neighbours or from the street (EU-SILC); retrieved 5 Oct 2026 (CC-020 data).",
     "https://ec.europa.eu/eurostat/databrowser/view/ilc_mddw01"),
    ("5", "Miżien. Data and calculations: data/cc-120/; tools/cc-120-report/calc.py.", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "14 Oct 2026", "First issue. No right of reply needed (verdict Largely supported).")])

build_report(Report(
    number="120", out=str(FIG / "report.pdf"), kicker="Noise",
    title_lines=["54,000 exposed", "to road noise:", "right, and too low?"],
    subtitle_lines=["Testing a European Parliament study’s Malta noise figures",
                    "against the European Environment Agency"],
    quote_lines=["“An estimated 54 000 inhabitants of Malta are being", "exposed to road noise levels over 55dB (Lden).”"],
    quote_size=14,
    attribution="Hjerp and Coffey (Ecocentric Consulting), study for the European Parliament’s Committee on Petitions, February 2026.",
    context="Key findings (PE 783.089).",
    verdict="Largely supported", verdict_note="Figures match the EEA; health numbers outdated",
    footer_lines=["Version 1.0  ·  14 October 2026", "Status:",
                  "Prepared from public sources, EEA and Eurostat data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Noise exposure and health burden in Malta", version="1.0", date="14 October 2026",
    pdf_title="Malta road noise exposure and health burden: Claim Check 120",
    pdf_subject="Tests the EP Petitions Committee study's Malta noise exposure and health figures against the EEA",
    story=S))
