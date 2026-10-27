"""Claim Check 143 report. Run calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

LG = colors.HexColor("#8DB36B")
FIG = HERE / "out"
S = []
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("On 2 October 2026 the European Commission published its assessment of Malta’s third river basin management plan. "
        "On groundwater it says: <b>“Since the second RBMP, the percentage of GWBs with a good quantitative status has "
        "decreased from 86.7% to 73.3% due to overabstraction”</b> and <b>“no GWBs had a good chemical status in 2021, "
        "while a fifth of GWBs had a good chemical status in 2015”</b> [1]. We recomputed the counts and checked them "
        "against the Commission’s 2019 assessment of the second plan and the EEA’s database.", lead)]
S.append(key_points([
    ("The counts are right.",
     "Malta has 15 groundwater bodies, so 86.7% is 13 bodies and 73.3% is 11: two bodies moved from good to poor "
     "quantitative status. The 2019 Commission document gives 13 good in the second plan [2]; the EEA’s database gives "
     "11 good and 15 in poor chemical status for the third [3]."),
    ("Chemical status: three good bodies in 2015, none in 2021.",
     "The 2019 document gives 3 of 15 (20%) in good chemical status in the second plan [2]; the EEA’s database shows "
     "all 15 in poor chemical status in the third [3]."),
    ("The third plan is back where the first was, not below it.",
     "Four bodies were in poor quantitative status in the first plan, two in the second and four in the third [1, 2]. "
     "The second-plan figure is the low point the claim starts from."),
    ("“Due to overabstraction” is the Commission’s attribution, which we could not test.",
     "Its document reports the water balance and lowering of the water table as the reason for the four poor bodies, "
     "and notes that monitoring changed and comparability between cycles “might be low” [1]. Eurostat’s "
     "abstraction estimates do not rise from 2015 to 2021 [4]."),
    ("Verdict: largely supported (moderate confidence).",
     "The statement is accurate as the Commission’s reading of the plans; whether the change is real deterioration "
     "or partly a change in assessment is not settled by the sources we could read."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("13 → 11", AMBER, "of 15 groundwater bodies in good quantitative status, 2nd to 3rd plan"),
             ("3 → 0", RED, "of 15 bodies in good chemical status, 2015 to 2021"),
             ("4 · 2 · 4", GREY, "bodies in poor quantitative status in the 1st, 2nd and 3rd plans"),
             ("−10%", GREY, "Eurostat’s estimate of groundwater abstraction, 2015 to 2021 (◆ estimated)")]),
      Spacer(1, 2 * mm),
      up_down("Nothing: Supported is the top of the scale. The counts are confirmed; the caveats are the attribution to "
              "overabstraction and the comparability of the cycles.",
              "A Commission or Maltese statement that the change in the number of poor bodies comes mainly from a new "
              "monitoring network or a new calculation of available resource, not from the water balance."),
      Spacer(1, 1 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the data show"),
          ("4", "Where the evidence points different ways"), ("5", "Testing the claim"),
          ("6", "Verdict and requests for evidence"), ("7", "Limitations")])
S.append(CondPageBreak(200 * mm))

S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The claim record quotes the Commission’s staff working document <i>Third River Basin Management Plans, Second "
           "Flood Hazard and Risk Maps and Second Flood Risk Management Plans: Member State Malta</i>, SWD(2026) 702 final, "
           "dated 2 October 2026 [1]. We read the document on 27 October 2026 from the copy on the Austrian Parliament’s "
           "website. In its summary table (pp. 8–9 of the PDF) it says: “Since the second RBMP, the percentage of GWBs with a "
           "good quantitative status has decreased from 86.7% to 73.3% due to overabstraction.” In the chemical-status "
           "row it says: “Overall, there has been a decrease in chemical status in the third RBMP compared with the second "
           "RBMP: no GWBs had a good chemical status in 2021, while a fifth of GWBs had a good chemical status in 2015.” "
           "It adds that “nitrates in 80% of GWBs, chloride in 73.3% and sodium in 53.3%” are the top three pollutants "
           "causing failure. GWB is the document’s abbreviation for a groundwater body: one of the 15 units into which Malta "
           "has divided its aquifers."))
S.append(std_table([
    [C("Source", cellh), C("What it says", cellh), C("Our access", cellh), C("Status", cellh)],
    [C("<b>Commission</b>, SWD(2026) 702, Malta [1]"),
     C("Third plan: 11 of 15 bodies good for quantity, none good for chemistry (assessment year 2021); 4 poor for quantity, "
       "8 not monitored for quantity."),
     C("Read pp. 8–9, 17–18, 21 and 28 of the PDF."), C("<b>The claim</b>")],
    [C("<b>Commission</b>, SWD(2019) 48, Malta [2]"),
     C("Second plan: 13 of 15 good for quantity, 2 poor (first plan: 4 poor); 3 of 15 good for chemistry (first plan: 2 good)."),
     C("Read the groundwater sections (Cellar PDF)."), C("Earlier, independent of the 2026 text")],
    [C("<b>EEA WISE</b>, WFD 2022 reporting [3]"),
     C("Status of each of the 15 bodies as reported by Malta (assessment year 2021): 11 good and 4 poor for quantity; "
       "all 15 poor for chemistry."),
     C("Downloaded 6 Oct 2026."), C("Data behind the third plan")],
    [C("<b>Eurostat</b>, env_wat_abs [4]"),
     C("Estimated fresh groundwater abstraction, 2010–2024."), C("Downloaded 6 Oct 2026."), C("Context for “overabstraction”")],
], [38 * mm, 74 * mm, 36 * mm, 22 * mm]))

S += [Spacer(1, 4 * mm), SectionHeading(2, "Method")]
S.append(P("<b>Question.</b> Are the Commission’s percentages and counts correct, are they supported by an independent "
           "source, and does the data show that overabstraction is what changed?"))
S.append(P("<b>Evidence.</b> We transcribed the figures into <i>data/cc-143/</i> with the page they came from, and ran "
           "<i>tools/cc-143-report/calc.py</i>: it converts each percentage back to a whole number of the 15 bodies, compares "
           "the 2026 document with the 2019 document and with the EEA’s database, and compares Eurostat’s abstraction "
           "estimates for 2015 and 2021. The EEA’s second-cycle database (2016 reporting) was in maintenance on 27 October "
           "2026, so we could not list which bodies changed."))
S.append(P("<b>Grades.</b> Commission staff working documents and the EEA’s reporting database: C (official reporting by "
           "the Member State, reviewed by the Commission). Eurostat abstraction: C, estimated. <b>Verdicts</b> follow the "
           "scale in Appendix A."))

S.append(CondPageBreak(75 * mm))
S.append(SectionHeading(3, "What the data show"))
S.append(KeepTogether([fig(FIG / "fig1_status.png", width=CW * 0.98),
                       P("Figure 1. Groundwater bodies in poor quantitative and poor chemical status in the three plans "
                         "(out of 15).", cap)]))
S.append(P("<b>Quantity.</b> 86.7% is 13 of 15 bodies and 73.3% is 11 of 15 (calculated). One body is worth 6.7 percentage "
           "points, so the change of 13.3 points is two bodies. The 2019 document gives 13 good and 2 poor in the second plan "
           "and 4 poor in the first [2]; the EEA’s database lists four poor bodies in 2021 [3]: Malta Mean Sea Level, Pwales "
           "Coastal, Marfa Coastal and Gozo Mean Sea Level. The third plan therefore has the same number of poor bodies as "
           "the first; the second plan had the fewest."))
S.append(P("<b>Chemistry.</b> The 2019 document counts 3 good and 12 poor bodies in the second plan [2]; the 2026 document "
           "says 12 of 15 were poor in 2015 and all 15 in 2021 [1], and the EEA’s database shows all 15 poor [3]. “A fifth” "
           "is 3 of 15 (20.0%). 80% is 12 of 15 bodies failing for nitrates (calculated); we did not test this per body, "
           "because the pollutant by body was not in the data we could read. Nitrate in groundwater is separately "
           "examined in Claim Check 047."))
S.append(KeepTogether([fig(FIG / "fig2_abstraction.png", width=CW * 0.98),
                       P("Figure 2. Eurostat’s estimate of fresh groundwater abstraction in Malta, 2010–2024 (◆ every year "
                         "is an estimate, not a metered total).", cap)]))
S.append(P("<b>Abstraction.</b> Eurostat’s estimates give 41.6 million m³ in 2015 and 37.3 million m³ in 2021 (−10.4%), and "
           "a mean of 42.7 million m³ for 2010–2015 against 40.1 million m³ for 2016–2021 (−6.0%) [4]. These are estimates "
           "and the series has a break flag in 2020; the 2016 plan’s assessment year is not in the documents we read. They "
           "do not show a rise in abstraction, but they also do not test the Commission’s statement, which rests on a "
           "comparison of abstraction with “available groundwater resource” [2] and on recharge, which has fallen with "
           "rainfall [1, p. 21]."))

S.append(CondPageBreak(95 * mm))
S.append(SectionHeading(4, "Where the evidence points different ways"))
S.append(contested("Did groundwater get worse between the second and third plans?", "YES ON THE COUNTS; CAUSE NOT SHOWN", AMBER,
                   "The counts are consistent in three sources. Chemical status went from 3 good bodies to none. Four "
                   "bodies are in poor quantitative status, twice the second plan’s two, and the Commission describes "
                   "“a systemic problem of overabstraction” in the monitored area (95.9% of it in poor status) [1].",
                   "The same document says that quantitative monitoring rose from 3 to 7 bodies and that 8 of 15 bodies "
                   "(85.5% of the area) are still not monitored [1]. For the protected-area comparison it warns that, “due to "
                   "the substantial changes in monitoring and assessment, comparability of data between the cycles might "
                   "be low” (p. 19), and for surface-water chemistry it judges the decline likely to be “methodological, "
                   "assessment or monitoring changes” (p. 7). It makes neither statement for groundwater. Eurostat’s "
                   "estimated abstraction fell [4].",
                   "The statement is an accurate report of Malta’s reported status. It would overstate if read as proof "
                   "that more water is being pumped, or that two aquifers deteriorated in five years: the sources do not "
                   "show which.", label_a="THE COUNTS AND THE COMMISSION’S READING", label_b="CAVEATS ON COMPARING CYCLES"))

S.append(CondPageBreak(90 * mm))
S.append(SectionHeading(5, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> The share of groundwater bodies in good quantitative status fell from 86.7% to 73.3%"),
     C("European Commission [1]"),
     C("13 of 15 to 11 of 15. The 2019 document gives 13 good in the second plan [2]; the EEA’s database gives 11 good in "
       "the third [3]. The first plan had 11 good (4 poor) [2]."),
     verd("ACCURATE", GREENC)],
    [C("<b>B.</b> The fall is due to overabstraction"), C("European Commission [1]"),
     C("The document reports water balance and lowering of the water table as the reason for the four poor bodies and "
       "describes “systemic” overabstraction [1]. We could not test it: abstraction is only estimated by Eurostat and fell "
       "2015–2021 [4]; the second-plan method (water-balance model) and the third-plan method were not compared; monitoring "
       "changed [1, 2]."),
     verd("NOT TESTED", GREY)],
    [C("<b>C.</b> No groundwater body had good chemical status in 2021, while a fifth did in 2015"),
     C("European Commission [1]"),
     C("All 15 bodies poor in the EEA’s database [3]; 3 of 15 good (20%) in the second plan [2]."),
     verd("ACCURATE", GREENC)],
    [C("<b>D.</b> Nitrates cause failure in 80% of the 15 groundwater bodies"), C("European Commission [1]"),
     C("80% is 12 of 15 (calculated). The document’s figure; we did not have the pollutant by body. Independent monitoring "
       "of nitrate is in Claim Check 047."),
     verd("CONSISTENT", LG)],
], [42 * mm, 24 * mm, 70 * mm, 34 * mm], valign="MIDDLE"))

S += [Spacer(1, 6 * mm), SectionHeading(6, "Verdict and requests for evidence"),
      verdict_box("Largely supported", "The counts and percentages are right and agree with the Commission’s 2019 assessment "
                                       "and the EEA’s database; the attribution to overabstraction is the Commission’s "
                                       "reading, which we could not test. Confidence: moderate."),
      Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> Every number in the claim is a whole number of 15 bodies, matches the documents we could compare "
           "it with, and is the Commission’s statement of Malta’s own reporting. <b>Why not Supported.</b> The words "
           "“due to overabstraction” give a cause that the data we could read do not test, and the same document says that "
           "monitoring changed and that comparability between cycles might be low. <b>What this verdict does not say.</b> It "
           "does not say that Malta’s aquifers did or did not deteriorate in physical terms; it says the Commission’s figures "
           "are accurate. The 2026 document is a Commission assessment of Malta’s plan, not a finding in a case."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list(["From the Energy and Water Agency or the Environment and Resources Authority: the status of each of "
                        "the 15 bodies in the second and third plans, with the method and the “available groundwater "
                        "resource” used for the water balance in each.",
                        "From the Agency: metered groundwater abstraction by body, 2013–2023.",
                        "From the Commission: the basis of the statement “due to overabstraction” and whether the change in "
                        "the number of monitored bodies affects it."]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag), P("Not needed for this verdict (maintainer rule of 5 October 2026).", small)],
              bg=AMBER_PALE, bar=AMBER)]
S += [CondPageBreak(60 * mm), Spacer(1, 6 * mm), SectionHeading(7, "Limitations")]
for l in ["The second plan’s status by body (EEA WISE, 2016 reporting) could not be downloaded on 27 October 2026 (server in "
          "maintenance), so we cannot say which two bodies changed from good to poor.",
          "We read the groundwater parts of the 2026 document (pp. 8–9, 17–18, 21 and 28) and searched its text for "
          "statements on methodology and comparability; we did not read the Maltese plans themselves (era.org.mt refuses scripts).",
          "The 2019 document is not consistent with itself on how many bodies were monitored for quantity in the second plan "
          "(two in section 5.1.1, three on p. 13); the 2026 document reports three. The 2026 document also gives 7 bodies "
          "failing for saline intrusion in its table and in section 3.3 and 5 in section 4.2. Neither affects the claim.",
          "Eurostat’s abstraction series is an estimate and is not matched to the plans’ assessment years.",
          "We did not test the 80% (nitrates) per body, nor whether the 2021 assessment reflects abstraction in 2021."]:
    S.append(P("• " + l, bul))
S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "European Commission (2 October 2026). Commission Staff Working Document: Third River Basin Management Plans, "
          "Second Flood Hazard and Risk Maps and Second Flood Risk Management Plans, Member State: Malta, SWD(2026) 702 final. "
          "Copy on the Austrian Parliament website, document XXVIII/EU/94981.",
     "https://www.parlament.gv.at/dokument/XXVIII/EU/94981/imfname_11680004.pdf"),
    ("2", "European Commission (26 February 2019). Commission Staff Working Document: Second River Basin Management Plans, "
          "Member State: Malta, SWD(2019) 48 final (groundwater: sections 5.1 and 6.1; summary, p. 13).",
     "http://publications.europa.eu/resource/celex/52019SC0048"),
    ("3", "European Environment Agency. WISE Water Framework Directive database, 2022 reporting (WFD2022_GroundWaterBody_WM), "
          "Malta, retrieved 6 October 2026.",
     "https://water.discomap.eea.europa.eu/arcgis/rest/services/WISE_WFD/WFD2022_GroundWaterBody_WM/MapServer/0"),
    ("4", "Eurostat. Water abstraction by source and sector (env_wat_abs), Malta, updated 16 September 2026, retrieved 6 October "
          "2026. ◆ estimated values.",
     "https://ec.europa.eu/eurostat/databrowser/view/env_wat_abs/default/table"),
    ("5", "MiŻien. Data and calculation: data/cc-143/; tools/cc-143-report/calc.py.", ""),
])
S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks an estimate or a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "27 Oct 2026", "First issue. Verdict Largely supported (moderate confidence); no right of reply needed.")])

build_report(Report(
    number="143", out=str(FIG / "report.pdf"), kicker="Water and groundwater",
    title_lines=["Malta’s", "groundwater:", "worse than", "the last plan?"],
    subtitle_lines=["Testing the Commission’s 2026 comparison of", "Malta’s second and third water plans"],
    quote_lines=["“…no GWBs had a good chemical status in 2021, while", "a fifth of GWBs had a good chemical status in 2015.”"],
    quote_size=14,
    attribution="European Commission, SWD(2026) 702 final, Malta, 2 October 2026, p. 9.",
    context="Also: good quantitative status “decreased from 86.7% to 73.3% due to overabstraction”.",
    verdict="Largely supported", verdict_note="Counts correct; cause not tested",
    footer_lines=["Version 1.0  ·  27 October 2026", "Status: no right of reply needed",
                  "Prepared from published documents and data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Malta’s groundwater status", version="1.0", date="27 October 2026",
    pdf_title="Malta’s groundwater: worse than the last plan? Claim Check 143",
    pdf_subject="Tests the Commission's comparison of groundwater status in Malta's second and third river basin management plans",
    story=S))
