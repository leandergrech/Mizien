"""Claim Check 105 report. Run calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
LG = colors.HexColor("#8DB36B")
S = []
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("At a press conference in Birżebbuġa on 26 May 2026 ADPD – The Green Party said: <b>“This country has yet to "
        "acknowledge that noise pollution is having an effect on the health of those who live near the Freeport or the "
        "airport”</b> and that “there is a need to study the impact of noise from the Freeport operations and the airport "
        "on the surrounding residential community”. We looked for the studies and official documents that would "
        "confirm or contradict this.", lead)]
S.append(key_points([
    ("Freeport noise is absent from the national noise framework.",
     "The word “Freeport” does not appear in any of five Environment and Resources Authority (ERA) noise documents we "
     "read in full (round 4 mapping report, two Noise Action Plans, the consultation responses, the airport report). "
     "The industrial sites mapped are seven to eight licensed facilities, none of them the Freeport."),
    ("Airport noise is mapped, but only as exposure.",
     "ERA has published modelled aircraft noise maps since 2011. In 2016 about 9,700 people lived in dwellings with "
     "modelled aircraft noise of 55 dB Lden or more, and about 830 at 50 dB Lnight or more. No health outcome was studied."),
    ("Some local noise research exists, which the statement does not mention.",
     "A Freeport-commissioned year-long study (2014–2015, reported by TVM; report not seen ◆) and a University of Malta "
     "paper (2022, 477 residents, 329 measurements) found noise above the EU reporting thresholds in Birżebbuġa and "
     "residents reporting annoyance, sleep problems and stress."),
    ("Verdict: largely supported (moderate confidence).",
     "We found no study of health outcomes (illness, medication, sleep measured objectively) among residents near the "
     "Freeport or the airport, and the official framework does not cover the Freeport. But the airport’s noise has "
     "been acknowledged and mapped, and Freeport-area noise has been measured, so “yet to acknowledge” is too strong."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("0 of 5", RED, "ERA noise documents that mention the Freeport"),
             ("≈9,700", AMBER, "People in modelled aircraft noise above 55 dB Lden, 2016 (MIA)"),
             ("5 of 5", AMBER, "Birżebbuġa monitoring points with daytime averages at 55 dBA or more (2020–21)"),
             ("0", GREY, "Health-outcome studies of residents found")]),
      Spacer(1, 4 * mm),
      up_down("Evidence that Maltese authorities have published a health assessment (not only noise levels) for residents "
              "near the Freeport or the airport; or that the Freeport noise has been formally assessed and acted on in the "
              "national action plan.",
              "A published health-outcome study of these residents, or a Freeport noise assessment inside the national "
              "framework; the statement would then be wrong on its main point."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the evidence shows"),
          ("4", "Where the evidence points different ways"), ("5", "Testing the claim"),
          ("6", "Verdict and requests for evidence"), ("7", "Limitations")])
S.append(PageBreak())

S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("ADPD published the statement on its website on 26 May 2026, in Maltese with an English version [1]; "
           "Newsbook reported it the same day [2]. It was issued by the party’s deputy chairpersons Carmel Cacopardo and "
           "Melissa Bagley during the general election campaign. The party names the Freeport Terminal, Malta International "
           "Airport and the entertainment industry as noise sources. It also says: “It is essential that we do not rely on "
           "international studies alone.” This check covers the Freeport and the airport; entertainment noise is a "
           "separate topic. The check is of the statement, not of anyone’s motives."))
S.append(std_table([
    [C("Source", cellh), C("What it says", cellh), C("Our access", cellh), C("Status", cellh)],
    [C("<b>ADPD</b> press statement, 26 May 2026 [1]"),
     C("“This country has yet to acknowledge that noise pollution is having an effect on the health of those who live "
       "near the Freeport or the airport, including its points of access.”"), C("Read in full, 5 Oct 2026 (English version)."),
     C("<b>The claim</b>")],
    [C("<b>ERA</b> Round 4 mapping report [3], Noise Action Plans [4,5], MIA round 3 report [6]"),
     C("Strategic noise maps of roads, industry and aircraft; action plan for the agglomeration and major roads."),
     C("Read in full (Internet Archive copies; era.org.mt returns 403 to scripts)."), C("<b>Regulator</b>")],
    [C("<b>Falzon et al.</b> (2022) [7]"), C("Five-point noise survey in Birżebbuġa, 329 measurements, 477 questionnaires."),
     C("Full text read (open access)."), C("<b>Journal</b>")],
    [C("<b>TVM news</b>, 29 Dec 2015 [8]"), C("A year-long study commissioned by Malta Freeport Terminals found noise above WHO levels."),
     C("Article read; the study itself not seen ◆."), C("News (second-hand)")],
], [38 * mm, 74 * mm, 36 * mm, 22 * mm]))

S += [Spacer(1, 4 * mm), SectionHeading(2, "Method")]
S.append(P("<b>Question.</b> Is it true that Malta has yet to acknowledge noise effects on people near the Freeport and the airport, "
           "and that such effects have not been studied?"))
S.append(P("<b>Evidence.</b> We read the ERA noise documents named above in full text and searched them for “Freeport”, "
           "“Birżebbuġa” and “Kalafrana” (<i>data/cc-105/doc_search.csv</i>). We tabulated the airport exposure figures and the "
           "Birżebbuġa monitoring ranges (<i>tools/cc-105-report/calc.py</i>), then searched OpenAlex, Crossref and the web for "
           "other local studies. The European Parliament study PE 783.089 (Hjerp & Coffey 2026) [9] gives the legal context. "
           "The Birżebbuġa measurements are LAeq averages, not Lden or Lnight, so comparison with the Noise Directive "
           "thresholds is only indicative."))
S.append(P("<b>Grades.</b> ERA documents: C (official, modelled). Falzon et al.: B (observational, survey plus measurements, no "
           "control). TVM report: D, second-hand. <b>Verdicts</b> follow the five-point scale in Appendix A."))

S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(3, "What the evidence shows"))
S.append(P("<b>The Freeport.</b> None of the five ERA documents mentions it. ERA’s round 3 mapping covered eight licensed "
           "industrial sites in or next to the Malta agglomeration (for example the Marsa power station and the Sant’Antnin "
           "waste plant); round 4 covered seven. The Freeport is not among them [3]. The European Parliament study notes that "
           "the Noise Directive covers only major roads, railways, airports and large agglomerations [9], so a port can fall "
           "outside the mandatory scope. That explains the gap but does not fill it."))
S.append(P("<b>Local Freeport-area noise research does exist.</b> A study commissioned by Malta Freeport Terminals at the request "
           "of the Birżebbuġa monitoring board (2014–2015, by Adi Associates Environmental Consultants) was reported by TVM "
           "as finding day and night noise above WHO levels ◆ [8]. A University of Malta team measured five residential "
           "points between December 2020 and August 2021 [7] (Figure 1). Daytime averages were 55 dBA or higher "
           "at all five points, and night averages reached above 50 dBA at four of five. The Freeport’s container handling, "
           "alarms and engine hum were named among the predominant sources at four points [7]. In the questionnaire, 98% of 477 "
           "respondents said noise was a problem, and 61.6% said annoyance was the main effect on health and well-being, "
           "followed by sleep disorders, fatigue and stress [7]. These are self-reported effects, not clinical findings."))
S.append(KeepTogether([fig(FIG / "fig1_birzebbuga.png", width=CW * 0.98),
    P("Figure 1. Range of average noise levels at five Birżebbuġa monitoring points, December 2020 to August 2021.", cap)]))
S.append(P("<b>The airport.</b> The airport is not a “major airport” under the directive (fewer than 50,000 movements a year; "
           "49,214 in 2021), but ERA has modelled its noise in each mapping round because flight paths cross the agglomeration "
           "[3,6]. In round 3 (base year 2016), 9,666 people lived in dwellings with modelled aircraft noise of 55 dB Lden or "
           "more (8,054 inside the agglomeration, 1,612 outside), almost all in the 55–59 band, and 827 at 50 dB Lnight or more "
           "[6]. The Noise Action Plan states WHO’s 2018 levels for aircraft noise (45 dB Lden, 40 dB Lnight) [4]. The "
           "published results are not broken down by locality, so we cannot say how many of these people live in "
           "Birżebbuġa."))
S.append(P("<b>Health outcomes.</b> We found no Maltese study linking measured exposure to illness, medication use, sleep "
           "recordings or other outcomes in residents near either site. Falzon et al. themselves write that “minimal research” "
           "exists on exposure–effect studies of community noise in Malta [7]. Our search was of public sources only (see "
           "Limitations)."))

S.append(CondPageBreak(80 * mm))
S.append(SectionHeading(4, "Where the evidence points different ways"))
S.append(contested("Has Malta “yet to acknowledge” the effect?", "PARTLY", AMBER,
                   "No ERA noise document mentions the Freeport, the airport’s results are exposure counts without a health "
                   "assessment, and the 2022 paper itself says exposure–effect research is minimal.",
                   "Aircraft noise has been mapped since 2011 and the Noise Action Plan sets out the health effects and WHO "
                   "levels. A Freeport-funded study and a university study of Birżebbuġa exist, and the mayor said in 2015 the "
                   "council had “enough information to start addressing the problem”.",
                   "Noise exposure near both sites has been acknowledged and measured, and general health effects are stated "
                   "in the action plan. What is missing is a health assessment of these residents, and any treatment of the "
                   "Freeport in the national framework. The statement’s call for a study is reasonable; its premise is overstated.",
                   label_a="FOR THE CLAIM", label_b="AGAINST"))

S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(5, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> Malta has yet to acknowledge the effect of Freeport noise on nearby residents' health"), C("ADPD [1]"),
     C("The Freeport is not mentioned in any ERA noise document and not among the mapped industrial sites, but a Freeport-"
       "commissioned study (2014–15 ◆) and a university study (2022) exist."),
     verd("LARGELY SUPPORTED", LG)],
    [C("<b>B.</b> Malta has yet to acknowledge the effect of airport noise on nearby residents' health"), C("ADPD [1]"),
     C("Aircraft noise exposure is modelled, mapped and published in three rounds, with WHO levels stated; "
       "no health assessment of residents."),
     verd("OVERSTATED", AMBER)],
    [C("<b>C.</b> A study of the impact of noise from the Freeport and airport on nearby residents is needed"), C("ADPD [1]"),
     C("No health-outcome study found; local work is exposure, annoyance and self-reported symptoms."),
     verd("LARGELY SUPPORTED", LG)],
], [42 * mm, 18 * mm, 76 * mm, 34 * mm], valign="MIDDLE"))

S += [Spacer(1, 6 * mm), SectionHeading(6, "Verdict and requests for evidence"),
      verdict_box("Largely supported", "No health study or Freeport coverage in the national framework; but noise near both "
                  "sites has been mapped or measured. Confidence: moderate."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> The substance, that nobody has studied the health of residents near the Freeport and the airport, is "
           "consistent with what we found, and the Freeport is missing from the national noise maps and action plans. "
           "The words “yet to acknowledge” overstate the case because airport noise is mapped and published, and Freeport-area noise "
           "has been measured twice. Confidence is moderate because absence of a study is hard to prove from public sources. "
           "<b>What this verdict does not say.</b> It does not say that residents are or are not harmed; it tests only "
           "whether the studies and official acknowledgement exist."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "From ERA: whether the Freeport and Kalafrana port activity are covered by any noise mapping, permit or monitoring requirement.",
    "From Malta Freeport Terminals: the 2014–2015 Adi Associates report and any later monitoring.",
    "From the Superintendence of Public Health: any health assessment of noise near the airport or the Freeport.",
]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag), P("Not needed for this verdict (maintainer rule of 5 October 2026).", small)],
              bg=AMBER_PALE, bar=AMBER)]
S += [Spacer(1, 6 * mm), SectionHeading(7, "Limitations")]
for l in ["The 2014–2015 Freeport study is known only through a TVM news report and a citation in Falzon et al. (◆).",
          "We could not search ERA’s site, the MEPS portal or the Superintendence of Public Health for unpublished studies; "
          "absence of a health study means none found in public sources.",
          "Birżebbuġa measurements are LAeq averages, not Lden or Lnight; comparison with thresholds is indicative. "
          "The paper’s monitoring figures were read as printed ranges, not digitised.",
          "Airport exposure is a model of aircraft noise only, from 2016 data; the round 4 (2021) results were not tabulated.",
          "ERA documents were read from Internet Archive copies because the live site refuses scripts."]:
    S.append(P("• " + l, bul))
S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "ADPD – The Green Party (26 May 2026). It-tniġġis qiegħed iħassrilna saħħitna / Pollution is negatively affecting our "
          "health. Read 5 Oct 2026.", "https://adpd.mt/it-tniggis-qieghed-ihassrilna-sahhitna-adpd/"),
    ("2", "Newsbook (26 May 2026). Air and noise pollution are harming our health – ADPD. (Locator.)",
     "https://newsbook.com.mt/en/air-and-noise-pollution-are-harming-our-health-adpd/"),
    ("3", "Lemitor for ERA (Nov 2024). Round 4 Final Project Report, Strategic Noise Mapping in Malta (SPD8/2022/011).",
     "https://era.org.mt/wp-content/uploads/2024/12/R4_Noise_Maps_Malta_Final_Report_compressed.pdf"),
    ("4", "ERA (2023). Noise Action Plan, Malta Agglomeration, 2019–2024.",
     "https://era.org.mt/wp-content/uploads/2023/12/Noise-Action-Plan-Agglomeration-Interactive.pdf"),
    ("5", "ERA (2023). Noise Action Plan for Major Roads in Malta, 2019–2024.",
     "https://era.org.mt/wp-content/uploads/2023/12/Noise-Action-Plan-Major-Roads.pdf"),
    ("6", "Acustica for ERA (March 2019). Malta International Airport Noise Modelling, Final Report 593-14-2/3 (round 3).",
     "https://era.org.mt/wp-content/uploads/2019/10/593-14-2v3-1_Malta-International-Airport-R3-Final-Report.pdf"),
    ("7", "Falzon J., Dalli Gonzi R.E., Camilleri M. & Grima S. (2022). Effects of noise pollution on residents living in Birzebbuga "
          "and the introduction of effective mitigation measures. <i>Int. J. Sustainable Development and Planning</i> 17(7): "
          "2309–2318. doi:10.18280/ijsdp.170732.", "https://doi.org/10.18280/ijsdp.170732"),
    ("8", "Galea O. (29 Dec 2015). Level of noise disturbance at Birżebbuġa is higher than that established by WHO. TVM news. ◆",
     "https://tvmnews.mt/en/news/level-of-noise-disturbance-at-birzebbuga-is-higher-than-that-established-by-who/"),
    ("9", "Hjerp P. & Coffey (2026). Analysing Malta’s implementation of Directive 2002/49/EC. European Parliament PE 783.089. "
          "doi:10.2861/6278624.", "https://doi.org/10.2861/6278624"),
    ("10", "MiŻien. Data and calculation: data/cc-105/; tools/cc-105-report/calc.py.", ""),
])
S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "5 Oct 2026", "First issue. Verdict Largely supported (moderate confidence); no right of reply needed.")])

build_report(Report(
    number="105", out=str(FIG / "report.pdf"), kicker="Noise",
    title_lines=["Noise near the", "Freeport and airport:", "never studied?"],
    subtitle_lines=["Testing ADPD’s call for a study of noise and health", "in Birżebbuġa and around the airport"],
    quote_lines=["“This country has yet to acknowledge that noise", "pollution is having an effect on the health of those",
                 "who live near the Freeport or the airport.”"], quote_size=14,
    attribution="ADPD – The Green Party, press statement, Birżebbuġa, 26 May 2026.",
    context="Deputy chairpersons Carmel Cacopardo and Melissa Bagley.",
    verdict="Largely supported", verdict_note="No health study found; but noise has been mapped and measured",
    footer_lines=["Version 1.0  ·  5 October 2026", "Status: no right of reply needed",
                  "Prepared from public sources and published literature.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Freeport and airport noise – ADPD", version="1.0", date="5 October 2026",
    status_note="no right of reply needed",
    pdf_title="Noise near the Freeport and airport: never studied? Claim Check 105",
    pdf_subject="Tests ADPD's statement that Malta has yet to acknowledge or study noise effects near the Freeport and airport",
    story=S))
