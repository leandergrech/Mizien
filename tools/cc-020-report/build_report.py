"""Claim Check 020 report. Run calc.py and figures.py first. Output: out/report.pdf"""
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
      P("A study for the European Parliament’s Committee on Petitions (February 2026) examined Malta’s implementation "
        "of the Environmental Noise Directive (END). It concluded: <b>“The transposition and implementation of the END "
        "evidently is not the cause of the noise problems in Malta.”</b> It found only two meaningful non-conformities, "
        "no infringement proceedings in 2015–2025, and that most complaints concern noise the Directive does not cover. "
        "We read the full study and tested its reasoning against Eurostat survey data and the WHO guideline levels it "
        "reports.", lead)]
S.append(key_points([
    ("The study’s reasoning holds together.",
     "The Directive sets reporting thresholds, not limits, and covers only major roads, railways, airports and large "
     "agglomerations. Construction, entertainment and neighbourhood noise are outside it, so legal conformity cannot "
     "explain complaints about them."),
    ("The noise problem itself is real.",
     "31.3% of people in Malta reported noise from neighbours or the street in 2023, the highest share in the EU "
     "(EU-27 18.1%), and Malta has been above the EU average in every available year since 2010."),
    ("‘Compliant’ is not ‘quiet’.",
     "The Directive’s 55 dB (day-evening-night) and 50 dB (night) thresholds are above the WHO 2018 guideline levels "
     "(53 and 45 dB for roads; 45 and 40 dB for aircraft). The study says so itself, and says health effects occur below the "
     "END thresholds."),
    ("Some parts could not be checked independently.",
     "We did not re-read the Maltese regulation or search the Commission’s infringement register. The 21% vs 9% survey "
     "figure is in ERA’s consultation annex, but the annex names no survey and the figure is not in the Marmarà survey summary, so its origin is unidentified."),
    ("Verdict: largely supported (moderate confidence).",
     "The conclusion follows from the evidence the study presents. Caveats: delays in action plans are an END "
     "implementation issue, and the verdict covers legal conformity only, not whether Malta is quiet."),
]))
S += [Spacer(1, 4 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("2", GREEN, "Meaningful non-conformities in the study’s transposition table (of about 219 rows)"),
             ("0", GREEN, "END infringement proceedings against Malta, 2015–2025 (per the study)"),
             ("31.3%", RED, "People reporting street or neighbour noise, 2023: highest in the EU (EU 18.1%)"),
             ("13%", ORANGE, "People above the END 55 dB threshold (study, citing EEA); underestimates")]),
      Spacer(1, 4 * mm),
      up_down("Maltese regulation or Commission records showing non-conformity that the study missed, or evidence that "
              "END-covered exposure (roads, airport) drives complaints more than the study allows.",
              "A cause for the complaints that does lie in END implementation, for example evidence that delayed "
              "action plans left residents unprotected from road noise."),
      Spacer(1, 5 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the study and the research say"),
          ("4", "What the data show"), ("5", "Where the evidence points different ways"),
          ("6", "Testing the claim"), ("7", "Verdict and requests for evidence"), ("8", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The claim is the study by Peter Hjerp and Clare Coffey (Ecocentric Consulting), commissioned by the European "
           "Parliament’s Committee on Petitions in response to Maltese petitions, PE 783.089, February 2026 [1]. We read the "
           "full text from the EU Publications Office. The opinions are the authors’, not the Parliament’s official position."))
S.append(std_table([
    [C("What the study says", cellh), C("Where", cellh), C("Access", cellh)],
    [C("“Legal transposition of the END into national legislation is not considered to be the cause of the noise "
       "problems in Malta.”"), C("Ch. 3 key findings [1]"), C("Read in full")],
    [C("Transposition has “just two issues of non-conformity that are meaningful” (Art. 8(3); Annex V limit values)."),
     C("Ch. 3 [1]"), C("Read in full")],
    [C("“There have been no END infringement proceedings against Malta between 2015 and 2025.”"), C("Ch. 4 [1]"),
     C("Read; register not searched")],
    [C("21% of participants in a 2019 Maltese survey ranked noise among their four most important environmental "
       "issues, against an EU28 average of 9%."), C("Ch. 6 [1], citing ERA 2023c [7]"), C("Annex read; origin unidentified")],
    [C("Complaints concern sources “largely” outside the END, so they do not “significantly reflect a failure in the "
       "implementation or enforcement of the END”."), C("Ch. 6 [1]"), C("Read in full (authors’ reading)")],
], [104 * mm, 34 * mm, 32 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("SCOPE NOTE", tag),
               P("This check tests the study’s conclusion and figures. It does not assess any person, authority or "
                 "enforcement decision, and it is read alongside a separate petition-based claim (CC-104). The study itself "
                 "names one implementation problem: long delays in publishing action plans.", small)],
              bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Question.</b> Does the evidence support the conclusion that how Malta transposed and implements the END is "
           "not what causes Malta’s noise problems?"))
S.append(P("<b>Evidence.</b> The study’s own text and tables [1]; Eurostat’s EU-SILC indicator on noise from neighbours or "
           "the street [2] for Malta, the EU and all Member States, as a measure of the size of the problem; the WHO guideline levels as reported in the study [1, 5]; "
           "and peer-reviewed reviews behind the WHO guidelines [3–4], verified by DOI in Crossref. Numbers are recomputed by "
           "<i>tools/cc-020-report/calc.py</i> from <i>data/cc-020/</i>."))
S.append(P("<b>Grades.</b> Peer-reviewed reviews are grade C–B by design; official statistics grade C; the study is a "
           "commissioned expert report (grade C). <b>Verdicts</b> follow the five-point scale in Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(90 * mm))
S.append(SectionHeading(3, "What the study and the research say"))
S.append(P("The study compares the Directive with Malta’s 2004 Regulations (as amended in 2007, 2018 and 2022) article by "
           "article. By our rough count about 14 of some 219 rows in its table are marked as not transposed; the authors "
           "judge only two to matter: the duty to inform the Commission of other criteria used in action plans (Art. 8(3)) and "
           "the absence of a reference to limit values under Article 5 [1]. That judgement of relevance is theirs, and we "
           "did not repeat the legal comparison."))
S.append(P("The Directive itself sets no limit values or reduction targets. It requires noise maps and action plans for major "
           "roads, railways, airports and agglomerations above 100,000 inhabitants, with reporting thresholds of 55 dB "
           "(Lden) and 50 dB (Lnight) [1]. Malta has no railways. The study, citing the EEA, says the exposure figures reported under "
           "it “are likely to be a considerable underestimation” for this reason [1]."))
S.append(P("The WHO’s 2018 guidelines recommend lower levels than these thresholds, built on systematic reviews of the "
           "evidence on annoyance [4] and cardiovascular and metabolic effects [3]; the process is described in [6]. "
           "The study itself states that “health impacts already occur at noise levels below the END reporting thresholds”."))
S.append(fig(FIG / "fig3_thresholds.png"))
S.append(P("Figure 1. Directive reporting thresholds against WHO 2018 guideline levels, as reported in the study [1] "
           "(second-hand for the WHO values).", cap))

# ================================================================== 4
S.append(CondPageBreak(150 * mm))
S.append(SectionHeading(4, "What the data show"))
S.append(P("Eurostat’s EU-SILC survey asks households whether they are bothered by noise from neighbours or from the "
           "street. It is self-reported and covers all sources, including road traffic, which the Directive does cover. It therefore shows the size of the problem, not what causes it or whether the law is at fault."))
S.append(fig(FIG / "fig1_noise_trend.png"))
S.append(P("Figure 2. Population reporting noise from neighbours or the street, Malta and EU-27. The orange line is the "
           "share of Maltese people modelled above the Directive’s 55 dB threshold (a different measure: modelled exposure "
           "to road and air noise only).", cap))
S.append(fig(FIG / "fig2_noise_rank.png"))
S.append(P("Figure 3. The same indicator for all 27 Member States, 2023. Malta ranks first.", cap))
DT = []
DT.append(std_table([
    [C("Indicator", cellh), C("Malta", cellh), C("EU / comparison", cellh), C("Source", cellh), C("Grade", cellh)],
    [C("Noise from neighbours or street, 2023"), C("<b>31.3%</b>"), C("18.1% (EU-27)"), C("Eurostat ilc_mddw01"), grade_tag("C")],
    [C("Years since 2010 with Malta above EU"), C("12 of 12"), C("–"), C("calculated"), grade_tag("C")],
    [C("Rank among 27 Member States, 2023"), C("1st"), C("next: Luxembourg 30.2%"), C("calculated"), grade_tag("C")],
    [C("People above Lden 55 dB (END)"), C("65,100 (13%)"), C("–"), C("Study, citing EEA [1]"), grade_tag("C")],
    [C("Transposition rows marked ‘No’"), C("~14 of ~219"), C("2 judged meaningful"), C("Study Annex 1 [1]"), grade_tag("C")],
    [C("Noise ranked top-4 environmental issue, 2019"), C("21%"), C("9% (EU28)"), C("Study, citing ERA [1, 7]"), grade_tag("D")],
], [60 * mm, 28 * mm, 34 * mm, 32 * mm, 16 * mm]))
DT.append(P("All values in <i>data/cc-020/checks.csv</i>. The 21% vs 9% row is as stated in ERA’s annex [7], which names no survey; it is not traced to one.", cap))
S.append(KeepTogether(DT))

# ================================================================== 5
S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(5, "Where the evidence points different ways"))
S.append(contested(
    "Q1  Is legal transposition the cause?", "SUPPORTED", GREEN,
    "Only two of the non-conformities the study lists are judged meaningful, the Commission has opened no END case "
    "against Malta in 2015–2025 (per the study), and the study reads the consultation responses and petition as concerning "
    "mostly sources outside the Directive.",
    "We did not verify the transposition table against the Maltese regulation or search the infringement register; "
    "the relevance judgement and the reading of the complaints are the authors’ own, and we did not re-code the responses.",
    "<b>For this claim:</b> the conclusion follows from the study’s evidence; independent legal verification is outstanding."))
S.append(contested(
    "Q2  Is the noise problem therefore small?", "NOT WHAT THE STUDY SAYS", AMBER,
    "The study separates two questions: whether the law is the cause, and whether people are exposed. It reports "
    "considerable exposure and, citing the EEA, says the END figures are likely an underestimate.",
    "Eurostat shows Malta first in the EU for reported noise, 13 points above the average. Directive thresholds sit above "
    "WHO levels (2 dB for road Lden, 5 dB for road Lnight, 10 dB for aircraft Lden).",
    "<b>For this claim:</b> “not the cause” must not be read as “not a problem”. The study does not read it that way."))
S.append(contested(
    "Q3  Are action-plan delays part of END implementation?", "A GAP IN THE HEADLINE", AMBER,
    "The study says the delays are the only implementation issue of concern and recommends faster publication.",
    "The conclusion says implementation “evidently is not the cause”, but the Action Plan due in January 2025 had not been "
    "published as of January 2026 [1].",
    "<b>For this claim:</b> the headline is slightly stronger than the study’s own detail; the body states the exception."))

# ================================================================== 6
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(6, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> Only two meaningful non-conformities in the transposition"),
     C("Per the study’s table [1]; legal comparison not repeated."), verd("SUPPORTED (study)", LG)],
    [C("<b>B.</b> No END infringement proceedings, 2015–2025"),
     C("Per the study [1]; register not searched."), verd("NOT CHECKED", GREY)],
    [C("<b>C.</b> Complaints concern sources outside the END"),
     C("The study’s own reading of the 2022 consultation responses and the 2024 petition (ch. 6) [1]: the authors’ "
       "judgement, which we did not re-code."),
     verd("SUPPORTED (study)", LG)],
    [C("<b>D.</b> 21% vs 9% survey figure"), C("In ERA’s annex [7] (a comment, no survey named); not in the Marmarà summary [8]; origin unidentified."),
     verd("NOT VERIFIED", GREY)],
], [52 * mm, 88 * mm, 30 * mm], valign="MIDDLE"))

# ================================================================== 7
S += [Spacer(1, 6 * mm), SectionHeading(7, "Verdict and requests for evidence"),
      verdict_box("Largely supported", "The conclusion follows from the evidence presented; legal conformity does not "
                  "mean low noise. Confidence: moderate."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) The Directive’s scope explains why complaints about construction, entertainment and "
           "neighbourhood noise are not a transposition failure. (2) Independent data confirm that the problem is large. "
           "(3) The caveats are that we could not verify the legal table or the infringement record independently, the "
           "survey figure’s origin is unidentified, and action-plan delays are a genuine implementation issue. They do not change "
           "the substance, which our scale calls <i>Largely supported</i>."))
S.append(P("<b>What this verdict does not say.</b> It does not say that Malta’s noise is acceptable, that thresholds "
           "protect health, or that authorities have enforced other noise laws adequately. It addresses only whether "
           "the study’s conclusion on the Directive is supported."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "The name of the survey behind the 21% vs 9% figure in ERA’s consultation annex (2023c), with the EU28 comparison source.",
    "Complaint and enforcement data for construction and entertainment noise.",
    "The date the Action Plan due in January 2025 will be published.",
]))

# ================================================================== 8
S += [Spacer(1, 6 * mm), SectionHeading(8, "Limitations")]
for l in ["We did not compare the Maltese regulation with the Directive ourselves, nor search the Commission’s infringement register.",
          "WHO guideline values and EEA exposure counts are taken from the study (second-hand); the EEA fact sheet and "
          "WHO document were not opened.",
          "The 21% vs 9% figure is in ERA’s annex [7] (pp. 5–6), in a comment from the Office of the Superintendent of Public "
          "Health, which names no survey. It is not in the summary of the Marmarà survey of October 2019 [8], which gives only a "
          "mean worry score for noise (3.90 out of 5). We do not know its source and have not assumed one.",
          "Eurostat’s indicator is self-reported, has no 2021–2022 values for Malta, and shows a dip in 2015 we did not investigate.",
          "Self-reported noise and modelled END exposure are different measures and are not directly comparable.",
          "Reviews [3, 4, 6] were read as abstracts, or as metadata only where no abstract was available."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Hjerp P., Coffey C. (2026). Analysing Malta’s implementation of Directive 2002/49/EC on the Assessment and "
          "Management of Environmental Noise. European Parliament, PE 783.089. doi:10.2861/6278624. (Read in full.)",
     "https://doi.org/10.2861/6278624"),
    ("2", "Eurostat. ilc_mddw01 Noise from neighbours or from the street (EU-SILC); retrieved 5 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/ilc_mddw01"),
    ("3", "van Kempen E. et al. (2018). WHO Environmental Noise Guidelines for the European Region: a systematic review on "
          "environmental noise and cardiovascular and metabolic effects. <i>IJERPH</i> 15(2):379. doi:10.3390/ijerph15020379. (Abstract read.)",
     "https://doi.org/10.3390/ijerph15020379"),
    ("4", "Guski R., Schreckenberg D., Schuemer R. (2017). WHO Environmental Noise Guidelines for the European Region: a "
          "systematic review on environmental noise and annoyance. <i>IJERPH</i> 14(12):1539. doi:10.3390/ijerph14121539. (Abstract read.)",
     "https://doi.org/10.3390/ijerph14121539"),
    ("5", "World Health Organization Regional Office for Europe (2018). Environmental Noise Guidelines for the European "
          "Region. (Second-hand via [1].)", ""),
    ("6", "Jarosińska D. et al. (2018). Development of the WHO Environmental Noise Guidelines for the European Region: an "
          "introduction. <i>IJERPH</i> 15(4):813. doi:10.3390/ijerph15040813. (Metadata verified.)",
     "https://doi.org/10.3390/ijerph15040813"),
    ("7", "Environment and Resources Authority (2023). Public consultation submissions and responses, Noise Action Plan "
          "for Malta (Annex I). Read in a Wayback copy on 6 Oct 2026, pp. 5–6.",
     "https://web.archive.org/web/2026/https://era.org.mt/wp-content/uploads/2023/12/Annex-I_Noise-Action-Plan-submissions-and-responses_Final.pdf"),
    ("8", "Marmarà V. (2019). Environment in Malta: Today and the Future, summary report, October 2019. Environment and "
          "Resources Authority. (Read; contains no 21% figure.)",
     "https://era.org.mt/wp-content/uploads/2020/07/Citizen-Survey-Environment-in-Malta-Today-and-the-Future.pdf"),
    ("9", "Miżien. Data and calculations: data/cc-020/; tools/cc-020-report/calc.py.", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "5 Oct 2026", "First issue. No right of reply needed."),
                   ("1.1", "6 Oct 2026", "Corrections after audit: sub-claim C rated on the study’s own analysis (the Eurostat "
                    "indicator no longer cited as support); the 21% vs 9% figure traced to ERA’s annex, origin still unidentified; "
                    "EEA underestimate attributed to the EEA; status and layout wording fixed. Verdict unchanged.")])

build_report(Report(
    number="020", out=str(FIG / "report.pdf"), kicker="Noise",
    title_lines=["Is the noise law", "the cause of", "Malta’s noise?"],
    subtitle_lines=["Testing a European Parliament study on Malta’s implementation",
                    "of the Environmental Noise Directive"],
    quote_lines=["“The transposition and implementation of the END", "evidently is not the cause of the noise problems in Malta.”"],
    quote_size=14,
    attribution="Hjerp and Coffey (Ecocentric Consulting), study for the European Parliament’s Committee on Petitions, February 2026.",
    context="Key findings, chapter 6 (PE 783.089).",
    verdict="Largely supported", verdict_note="Legal conformity is not the cause; that does not mean Malta is quiet",
    footer_lines=["Version 1.1  ·  6 October 2026", "Status:",
                  "Prepared from public sources and Eurostat data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Noise law and noise in Malta", version="1.1", date="6 October 2026",
    pdf_title="Is the noise law the cause of Malta's noise? Claim Check 020",
    pdf_subject="Tests the EP Petitions Committee study's conclusion on Malta's implementation of the Environmental Noise Directive",
    story=S))
