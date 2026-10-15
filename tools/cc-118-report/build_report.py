"""Claim Check 118 report. Run fetch.py, calc.py and figures.py first. Output: out/report.pdf"""
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
      P("The Council of the European Union’s draft Recommendation on Malta (3 July 2026, recital 30) says that Malta’s "
        "seasonal <b>Water Exploitation Index Plus (WEI+) “reached 66.7% in the third quarter of 2023, the second-highest level "
        "among EU Member States”</b>, and, citing Malta’s Third River Basin Management Plan, that only 58% of surface water bodies "
        "(by number) reached good or high ecological status, 45% good chemical status, and that 82% of groundwater bodies "
        "(by area) failed good quantitative status and 100% failed good chemical status [1]. We reproduced each figure from the "
        "European Environment Agency (EEA) and Eurostat.", lead)]
S.append(key_points([
    ("The water-stress figure is the EEA’s, and the ranking holds.",
     "The EEA’s 2023 chart gives Malta 66.7% in Q3; only Cyprus (92.1%) is higher, and Greece is next at 37.4% [2]. "
     "Only Cyprus and Malta reach Eurostat’s 40% line for severe scarcity [3]."),
    ("Surface water: the percentages reproduce, but ‘by number’ matters.",
     "11 of 19 bodies are good or high (58%) [4]. Nine coastal bodies hold 99.96% of the area; by area the figure is 97%."),
    ("The 45% for chemical status counts the territorial waters.",
     "9 of 20 bodies are good (45%); the 20th is the territorial sea, whose status is ‘Unknown’. Without it, 9 of 19 is 47%."),
    ("Groundwater: 82% and 100% reproduce.",
     "292.5 of 356.9 km² is in poor quantitative status (82%); 4 of 15 bodies by number. All 15 are in poor chemical status [4]."),
    ("Verdict: largely supported (high confidence).",
     "Caveats: the ranking depends on the series, the 45% basis is unstated, and we did not read the plan itself."),
]))
S += [Spacer(1, 4 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("66.7%", RED, "Malta’s worst-quarter WEI+ in 2023 (Q3); EU second-highest after Cyprus (92.1%)"),
             ("58%", GREEN, "of 19 surface water bodies at good or high ecological status (11); 97% by area"),
             ("82%", RED, "of groundwater area in poor quantitative status (4 of 15 bodies)"),
             ("100%", RED, "of groundwater bodies in poor chemical status (15 of 15)")]),
      Spacer(1, 4 * mm),
      up_down("The plan’s own tables showing the same counts and bases, and an explanation of the EEA–Eurostat gap for Romania.",
              "A plan version with different counts, or a corrected series that moves Malta out of the top two.",
              heads=("What would make it ‘Supported’", "What would lower it")),
      Spacer(1, 5 * mm)]
S += toc([("1", "The claim and its source"), ("2", "Method"), ("3", "Water scarcity: the WEI+ figure"),
          ("4", "Water bodies: status counts"), ("5", "Where the evidence points different ways"),
          ("6", "Testing the claim"), ("7", "Verdict and requests for evidence"), ("8", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and its source"))
S.append(P("The wording is recital (30) of the draft Council Recommendation on Malta’s economic, social, employment, structural and "
           "budgetary policies, document 11130/26 of 3 July 2026 (PDF p. 16 of 22), a General Secretariat note to the Council "
           "committees [1]. It is a draft; we did not find the adopted text. The Council relays figures from the Commission’s 2026 "
           "country report and from Malta’s Third River Basin Management Plan (RBMP), neither of which we read."))
S.append(std_table([
    [C("Council’s words (recital 30)", cellh), C("Basis given", cellh)],
    [C("“the seasonal Water Exploitation Index Plus (WEI+), which reached 66.7% in the third quarter of 2023, the second-highest "
       "level among EU Member States, indicating severe water scarcity”"), C("None named")],
    [C("“only 58% of surface water bodies (by number) attained good or high ecological status, while just 45% met good chemical status”"),
     C("Third RBMP; ‘by number’ stated for the first figure only")],
    [C("“82% of groundwater bodies (by area) failed to achieve good quantitative status, and 100% did not meet good chemical status”"),
     C("Third RBMP; ‘by area’ stated for the first figure only")],
], [120 * mm, 50 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("SCOPE NOTE", tag),
               P("We test the numbers in the sentences above. The recital’s other sentences (pressures, wastewater agglomerations, "
                 "policy recommendations) are not rated. The Council is relaying other bodies’ data, so a difference from the "
                 "Commission’s or Malta’s own documents would not be an error by Malta. The check concerns the statement, not any person.",
                 small)], bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Question.</b> Do the cited figures match the official data, and do the stated bases (‘seasonal’, ‘by number’, ‘by area’) "
           "change what they mean?"))
S.append(P("<b>Evidence.</b> The EEA’s indicator chart of each country’s worst seasonal WEI+ in 2023 [2]; Eurostat’s annual WEI+ "
           "(sdg_06_60) and its metadata [3]; the EEA’s WISE database of Malta’s 2022 Water Framework Directive reporting, which "
           "holds each water body’s status and area [4]; and the Energy and Water Agency’s 2024 technical document on groundwater levels [5]. "
           "We recomputed every share in <i>tools/cc-118-report/calc.py</i> from <i>data/cc-118/</i> (source URLs and retrieval date "
           "in each file). Because the plan itself was refused to scripts, we use the WISE copy of Malta’s reporting as the stand-in; "
           "that the Council’s percentages come out exactly is the evidence they share a source."))
S.append(P("<b>Grades.</b> All sources are official statistics or regulator data (grade C). Water-body status is self-reported by Malta to "
           "the EEA. No peer-reviewed paper is needed to reproduce the counts; two reviews give context [6, 7]."))

# ================================================================== 3
S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(3, "Water scarcity: the WEI+ figure"))
S.append(P("WEI+ is water consumption (abstraction less return flows) as a percentage of renewable freshwater resources. Eurostat’s "
           "metadata treats values above 20% as a sign of scarcity and 40% or more as severe scarcity, and warns that annual national "
           "values “may therefore mask water stress, which occurs on a seasonal or regional basis” [3]."))
S.append(fig(FIG / "fig1_wei.png"))
S.append(P("Figure 1. Highest seasonal WEI+ in 2023 for the 27 EU Member States, with the quarter in which it occurs. Source: EEA indicator "
           "‘Worst seasonal water scarcity conditions’ (chart data, modified 28 Nov 2025) [2]; thresholds from Eurostat metadata [3].", cap))
S.append(std_table([
    [C("Measure (2023)", cellh), C("Malta", cellh), C("Comparison", cellh), C("Source", cellh)],
    [C("Worst seasonal WEI+ (EEA chart)"), C("<b>66.7%</b> (Q3), rank 2 of 27"), C("Cyprus 92.1%; Greece 37.4%; Romania 33.9%"), C("EEA [2]")],
    [C("Annual WEI+ (Eurostat VAL_A)"), C("30.1%, rank 3"), C("Cyprus 75.3%; Romania 47.4%"), C("Eurostat [3]")],
    [C("Four-year average (Eurostat AVG_4Y)"), C("33.4%, rank 2"), C("Cyprus 72.2%; Romania 27.9%"), C("Eurostat [3]")],
], [52 * mm, 38 * mm, 52 * mm, 28 * mm]))
S.append(P("The Council’s number is the EEA’s, and Malta is second. Eurostat’s annual 2023 series ranks Malta third because it gives Romania "
           "47.4%, higher than the 33.9% worst quarter in the EEA chart, which cannot both hold under one method; the series differ in "
           "vintage (Eurostat updated 28 April 2026, EEA chart November 2025) and we could not explain the difference. Ranking Malta second "
           "is therefore right on the indicator the Council names (seasonal) and on the four-year average, not on the 2023 annual value.", small))

# ================================================================== 4
S.append(CondPageBreak(150 * mm))
S.append(SectionHeading(4, "Water bodies: status counts"))
S.append(P("Malta reported 19 surface water bodies (9 coastal, 5 transitional, 3 river, 2 lake) plus its territorial sea, and 15 groundwater "
           "bodies [4]. Territorial waters carry only a chemical status, which is ‘Unknown’ in the data."))
S.append(std_table([
    [C("Council figure", cellh), C("What the data give", cellh), C("Result", cellh)],
    [C("58% of surface water bodies good or high ecological status (by number)"),
     C("11 of 19: coastal 8 of 9, transitional 3 of 5, river 0 of 3, lake 0 of 2. Assessed 2017–2022."), C("<b>58%</b>, reproduced")],
    [C("45% good chemical status"),
     C("9 of 20 including the territorial sea (status ‘Unknown’); 9 of 19 without it (47%). The 9 are the coastal bodies; all 10 river, lake "
       "and transitional bodies fail."), C("<b>45%</b>, reproduced with 20")],
    [C("82% of groundwater bodies (by area) failed quantitative status"),
     C("292.5 of 356.9 km² (Malta, Marfa, Pwales and Gozo bodies). By number 4 of 15 (27%). Assessed 2021."), C("<b>82%</b>, reproduced")],
    [C("100% failed chemical status"), C("15 of 15 bodies, all poor."), C("<b>100%</b>, reproduced")],
], [58 * mm, 82 * mm, 30 * mm]))
S.append(fig(FIG / "fig2_denominators.png"))
S.append(P("Figure 2. The same bodies counted by number and by area [4]. Surface area excludes the three rivers (3.4 km in all) and the "
           "territorial sea.", cap))
S.append(P("The groundwater picture is corroborated by the Energy and Water Agency’s monitoring: 21 of 35 boreholes show a significant "
           "negative water-level trend over 2000–2021 in its Table 1 (the text says 62.9%, or 22) [5]. The EEA data show the chemical-status "
           "variant that excludes ubiquitous persistent substances is identical to the headline for every Maltese surface body, so that "
           "exclusion does not explain the failures [4]."))

# ================================================================== 5
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(5, "Where the evidence points different ways"))
S.append(contested(
    "Q1  Is ‘severe water scarcity’ right?", "YES AT THE PEAK, NOT ANNUALLY", AMBER,
    "The seasonal peak of 66.7% is far above Eurostat’s 40% line for severe scarcity, and only Cyprus and Malta are above it [2, 3].",
    "Eurostat’s annual 2023 value for Malta is 30.1%, in the 20–40% band of ‘scarcity’, and Eurostat warns annual values can mask seasonal stress [3].",
    "<b>For this claim:</b> the Council says ‘seasonal’ and the severe label fits that figure; it does not describe Malta’s annual average."))
S.append(contested(
    "Q2  Is surface water quality ‘poor’?", "DEPENDS ON THE COUNT", AMBER,
    "By number only 58% reach good or high ecological status and 45% good chemical status, so almost half the bodies fall short.",
    "By area 97% of surface water is at good or high ecological status, because nine coastal bodies hold 99.96% of it; the failing "
    "bodies are ten small lagoons, saltpans, lakes and wadis.",
    "<b>For this claim:</b> the Council states ‘by number’ for the ecological figure, so it is accurate; the 45% basis is not stated."))

# ================================================================== 6
S.append(CondPageBreak(100 * mm))
S.append(SectionHeading(6, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> Seasonal WEI+ reached 66.7% in Q3 2023, indicating severe water scarcity"),
     C("Exact match to the EEA chart [2]; above Eurostat’s 40% severe line [3]. An annual figure would be 30.1%."),
     verd("SUPPORTED", GREENC)],
    [C("<b>B.</b> That is the second-highest among EU Member States"),
     C("Second after Cyprus on the EEA chart and the four-year average; third on Eurostat’s annual 2023 value (Romania higher)."),
     verd("LARGELY SUPPORTED", LG)],
    [C("<b>C.</b> 58% of surface water bodies (by number) at good or high ecological status"),
     C("11 of 19 [4]; 97% by area."), verd("SUPPORTED", GREENC)],
    [C("<b>D.</b> 45% of surface water bodies at good chemical status"),
     C("9 of 20 [4]; needs the territorial sea in the denominator; 47% without. Basis not stated."), verd("LARGELY SUPPORTED", LG)],
    [C("<b>E.</b> 82% of groundwater bodies (by area) failed quantitative status"),
     C("81.96% by area [4]; 27% by number. Corroborated by borehole trends [5]."), verd("SUPPORTED", GREENC)],
    [C("<b>F.</b> 100% of groundwater bodies failed chemical status"), C("15 of 15 [4]."), verd("SUPPORTED", GREENC)],
], [56 * mm, 84 * mm, 30 * mm], valign="MIDDLE"))

# ================================================================== 7
S += [Spacer(1, 6 * mm), SectionHeading(7, "Verdict and requests for evidence"),
      verdict_box("Largely supported", "Every figure reproduces from EEA and Eurostat data; the ranking and the 45% depend on the dataset "
                  "and the denominator. Confidence: high. No right of reply needed."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) Five of the six figures reproduce exactly and the sixth (45%) reproduces with a defensible denominator. "
           "(2) The caveats are minor: the ranking depends on the series, and ‘by number’ gives a harsher picture of surface waters than "
           "area does, as the Council’s own wording signals. Our scale calls that <i>Largely supported</i>."))
S.append(P("<b>What this verdict does not say.</b> It does not say Malta’s water is well managed or that the status classes are the right "
           "yardstick; it says the Council’s numbers match the official data."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "From the Energy and Water Agency or ERA: the Third RBMP’s status tables, to confirm the counts and the basis of the 45%.",
    "From the EEA and Eurostat: why Romania’s 2023 annual WEI+ (47.4%) exceeds its worst-quarter value in the EEA chart (33.9%).",
    "From the Council: the adopted text of the Recommendation and the document in which the WEI+ sentence first appears.",
]))

# ================================================================== 8
S += [Spacer(1, 6 * mm), SectionHeading(8, "Limitations")]
for l in ["We did not read the Third RBMP (era.org.mt returned 403), the Commission’s 2026 country report or the adopted Recommendation. "
          "The WISE data are Malta’s 2022 reporting; the plan is dated March 2024 and could differ.",
          "Status classes use the WISE legends (codes read from the services’ own legend); the Water Framework Directive was not re-read.",
          "The EEA chart was read from the page’s embedded data; we have no independent copy of its underlying dataset.",
          "The EWA borehole table has 35 rows; its text reports one more negative trend than the rows show. We cite both.",
          "Only the two WEI+ series and one plan year were tested; later 2024–2026 values were not available."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Council of the European Union (3 Jul 2026). Draft Council Recommendation on Malta’s economic, social, employment, structural and "
          "budgetary policies, 11130/26, recital (30). (Read in full; draft.)",
     "https://data.consilium.europa.eu/doc/document/ST-11130-2026-INIT/en/pdf"),
    ("2", "European Environment Agency. Worst seasonal water scarcity conditions for European countries in 2023, measured by WEI+ "
          "(indicator page, modified 28 Nov 2025; chart data read 15 Oct 2026).",
     "https://www.eea.europa.eu/en/analysis/indicators/use-of-freshwater-resources-in-europe-1/worst-seasonal-water-scarcity-conditions"),
    ("3", "Eurostat. Water exploitation index, plus (WEI+), sdg_06_60, and reference metadata (updated 28 Apr 2026; retrieved 15 Oct 2026).",
     "https://ec.europa.eu/eurostat/cache/metadata/en/sdg_06_60_esmsip2.htm"),
    ("4", "European Environment Agency. WISE Water Framework Directive database, Malta, 2022 reporting (surface and groundwater bodies); "
          "queried 15 Oct 2026.",
     "https://water.discomap.eea.europa.eu/arcgis/rest/services/WISE_WFD/"),
    ("5", "Energy and Water Agency (May 2024). Technical Document in support of the 3rd RBMP: Monitoring Results for the Groundwater "
          "Quantitative Status Assessment, Table 1.",
     "https://energywateragency.gov.mt/wp-content/uploads/2024/05/Technical-Document-Status-of-the-Quantitative-monitoring-network_Final.pdf"),
    ("6", "Hartfiel L., Soupir M., Kanwar R. (2020). Malta’s Water Scarcity Challenges: Past, Present, and Future Mitigation Strategies for "
          "Sustainable Water Supplies. <i>Sustainability</i> 12(23). doi:10.3390/su12239835 (Crossref-verified; abstract read.)",
     "https://doi.org/10.3390/su12239835"),
    ("7", "Casadei S., Peppoloni F., Pierleoni A. (2020). A New Approach to Calculate the Water Exploitation Index (WEI+). <i>Water</i> 12(11). "
          "doi:10.3390/w12113227 (Crossref-verified; abstract read.)", "https://doi.org/10.3390/w12113227"),
    ("8", "Miżien. Data and calculations: data/cc-118/; tools/cc-118-report/.", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "15 Oct 2026", "First issue. Verdict Largely supported. No right of reply needed.")])

build_report(Report(
    number="118", out=str(FIG / "report.pdf"), kicker="Water, checked",
    title_lines=["Second-highest", "water stress,", "groundwater failing?"],
    subtitle_lines=["Testing the Council’s figures on Malta’s water", "against the EEA and Eurostat"],
    quote_lines=["“…the seasonal Water Exploitation Index Plus (WEI+), which", "reached 66.7% in the third quarter of 2023…”"],
    quote_size=14,
    attribution="Council of the European Union, draft Recommendation on Malta, 3 July 2026, recital (30).",
    context="“…the second-highest level among EU Member States.”",
    verdict="Largely supported", verdict_note="All figures reproduce; ranking and one basis are caveated",
    footer_lines=["Version 1.0  ·  15 October 2026", "Status:",
                  "Prepared from public sources, EEA and Eurostat data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Malta water stress and water-body status", version="1.0", date="15 October 2026",
    pdf_title="Second-highest water stress, groundwater failing? Claim Check 118",
    pdf_subject="Tests the Council's recital on Malta's WEI+ and water-body status against EEA and Eurostat data",
    story=S))
