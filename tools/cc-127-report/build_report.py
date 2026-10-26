"""Claim Check 127 report. Run fetch_data.py, calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

LG = colors.HexColor("#8DB36B")
FIG = HERE / "out"
S = []
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("The European Commission’s assessment of Malta’s third river basin management plan, dated 2 October 2026, says: "
        "<b>“Malta has the lowest proportion of organic farming in the EU.”</b> Later it adds that “only 66 hectares (less "
        "than 1%)” of Malta’s 10 700 hectares of agricultural area “was managed organically in 2022, well below the EU "
        "average”. We tested the ranking, the 66 hectares and the comparison with the EU average against Eurostat’s "
        "organic-farming statistics.", lead)]
S.append(key_points([
    ("The ranking holds in every year we could test.",
     "In Eurostat’s series (share of farmland under organic farming) Malta is the lowest reporting Member State in each "
     "year from 2012 to 2024. In 2022 it was 0.62%; the next lowest, Bulgaria and Ireland, were at 2.2%."),
    ("The 66 hectares is Eurostat’s figure for 2022.",
     "Eurostat gives 66 ha of organic land in Malta in 2022 (65 ha fully converted, 1 ha in conversion), and 80 ha in 2023 "
     "and 2024. The Commission’s own two numbers give 66 / 10 700 = 0.62%."),
    ("“Well below the EU average” holds.",
     "Eurostat’s last published EU-27 estimate is 9.1% of farmland (2020); Malta was at 0.62% that year, about one fifteenth."),
    ("Two minor caveats.",
     "Austria (from 2021) and Greece (from 2022) are missing from Eurostat’s latest release, though both were far above Malta "
     "when last published. And the 10 700 ha denominator is not named in the document; farm-structure surveys give 9 800 ha "
     "(2020) and 8 880 ha (2023). The share stays below 1% on either."),
    ("Verdict: supported (high confidence).",
     "The statements reproduce from Eurostat’s published data, by year and by country."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(0), Spacer(1, 3 * mm),
      tiles([("0.62%", RED, "of Malta’s farmland was organic in 2022 (Eurostat)"),
             ("66 ha", AMBER, "organic area in 2022, as the Commission says"),
             ("2.2%", BLUE, "the next lowest Member States in 2022 (Bulgaria, Ireland)"),
             ("9.1%", GREY, "EU-27 average, 2020 (last published estimate)")]),
      Spacer(1, 4 * mm),
      up_down("Supported is the top of the scale: nothing moves the verdict up.",
              "Eurostat revisions that put another Member State below Malta, or a published organic area for Malta "
              "well above 66 ha in 2022 (for example from the national register)."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the data show"),
          ("4", "Where the evidence points different ways"), ("5", "Testing the claim"),
          ("6", "Verdict and requests for evidence"), ("7", "Limitations")])
S.append(PageBreak())

S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The claim is in the European Commission’s staff working document SWD(2026) 702 final, “Third River Basin "
           "Management Plans, Second Flood Hazard and Risk Maps and Second Flood Risk Management Plans, Member State: "
           "Malta”, dated Brussels, 2 October 2026 [1]. We read it in full on 18 October 2026 from the copy on the Austrian "
           "Parliament’s website; we did not find the Commission’s own copy. Two passages matter. In the description of "
           "the country (PDF p. 5): “Malta has the lowest proportion of organic farming in the EU.” In the section on "
           "pressures (PDF p. 11): “The total agricultural area of Malta is 10 700 hectares, representing 34% of the total "
           "land area. Only 66 hectares (less than 1%) of this agricultural area was managed organically in 2022, well "
           "below the EU average.” The document does not name the source of these figures in the passage; a footnote on "
           "p. 29 repeats the 66 hectares and cites a Publications Office report on CAP strategic plans, which we did not "
           "open ◆."))
S.append(std_table([
    [C("Source", cellh), C("What it says", cellh), C("Our access", cellh), C("Status", cellh)],
    [C("<b>European Commission</b>, SWD(2026) 702 [1]"),
     C("Lowest organic share in the EU; 66 ha of 10 700 ha organic in 2022."), C("Read in full (PDF)."), C("<b>The claim</b>")],
    [C("<b>Eurostat</b>, sdg_02_40 [2]"),
     C("Share of utilised agricultural area under organic farming, by country, 2000–2024."), C("API, all Member States."),
     C("Independent")],
    [C("<b>Eurostat</b>, org_cropar [3]"),
     C("Organic area in hectares by production method (fully converted, in conversion)."), C("API, all Member States."),
     C("Independent")],
    [C("<b>Eurostat</b>, ef_lus_main; demo_r_d3area [4]"),
     C("Utilised agricultural area from farm-structure surveys; land area (316 km²)."), C("API."), C("Independent")],
], [40 * mm, 72 * mm, 32 * mm, 26 * mm]))

S += [Spacer(1, 4 * mm), SectionHeading(2, "Method")]
S.append(P("<b>Question.</b> Is Malta the lowest in the EU in organic share of farmland, is the 66 hectares right, and is "
           "this well below the EU average?"))
S.append(P("<b>Evidence.</b> We downloaded the Eurostat series through its API on 21 October 2026, saved filtered copies "
           "in <i>data/cc-127/</i> and ran <i>tools/cc-127-report/calc.py</i>. It ranks Malta against every Member State for "
           "each year from 2012 to 2024, compares Malta’s organic area with the Commission’s 66 ha, recomputes 66 / 10 700, "
           "and tests the 10 700 ha and 34% against survey and land-area data."))
S.append(P("<b>Grades.</b> Eurostat statistics from national reporting: C. Commission document: C. <b>Verdicts</b> follow "
           "the scale in Appendix A."))

S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(3, "What the data show"))
S.append(KeepTogether([fig(FIG / "fig1_ranking.png", width=CW * 0.98),
                       P("Figure 1. Organic share of farmland by Member State, 2022 (Eurostat). Austria and Greece are "
                         "missing from the 2022 release; their last published values are hatched.", cap)]))
S.append(P("Malta is at 0.62% in 2022, the lowest of the 25 Member States that report. Austria (25.7% in 2020) and Greece "
           "(12.2% in 2021) are absent from the 2022 release, but their last values are far above Malta’s. The same holds "
           "in 2023 and 2024 (0.78% and 0.77%), with Bulgaria the next lowest (2.95% and 3.95%). In absolute terms Malta’s "
           "66 ha compares with 7 749 ha in Cyprus and 8 255 ha in Luxembourg, the next smallest areas."))
S.append(KeepTogether([fig(FIG / "fig2_series.png", width=CW * 0.98),
                       P("Figure 2. Malta against the lowest of the other Member States, 2012–2024 (Eurostat).", cap)]))
S.append(P("The gap is persistent: in every year from 2012 to 2024 Malta is below every other reporting Member State. "
           "Malta’s share has risen from 0.21% in 2016 to 0.77% in 2024, but the next lowest has risen faster since 2021. "
           "Eurostat’s 2022 hectares are 65 fully converted plus 1 in conversion: the Commission’s 66 ha is the total."))

S.append(CondPageBreak(95 * mm))
S.append(SectionHeading(4, "Where the evidence points different ways"))
S.append(contested("What is the denominator: 10 700 ha, or less?", "NO MATERIAL CONFLICT", GREENC,
                   "Eurostat’s share (0.62%) with 66 ha implies about 10 645 ha of farmland, close to the Commission’s "
                   "10 700 ha. 10 700 ha is 33.9% of Malta’s 316 km², as the Commission says.",
                   "Farm-structure surveys give lower utilised agricultural area: 9 800 ha in 2020 and 8 880 ha in 2023. "
                   "On these, organic land would be 0.68% (66–67 ha in 2020) and 0.90% (80 ha in 2023).",
                   "The denominator differs between sources, but the organic share is below 1% on every one tested. The "
                   "ranking does not depend on it: the next lowest Member State is at 2.2% or more in 2022.", label_a="CONSISTENT", label_b="CAVEAT"))

S.append(CondPageBreak(90 * mm))
S.append(SectionHeading(5, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> Malta has the lowest proportion of organic farming in the EU"), C("European Commission [1]"),
     C("Lowest of all reporting Member States in each year 2012–2024; 0.62% in 2022 against 2.2% for the next [2]."),
     verd("CONFIRMED", GREENC)],
    [C("<b>B.</b> Only 66 hectares (less than 1%) were organic in 2022"), C("European Commission [1]"),
     C("Eurostat: 66 ha (65 + 1 in conversion), 0.62% of farmland [2][3]."), verd("CONFIRMED", GREENC)],
    [C("<b>C.</b> That is well below the EU average"), C("European Commission [1]"),
     C("EU-27 estimate 9.1% in 2020, the last published; Malta 0.62% that year [2]. No EU aggregate for 2022 was found."),
     verd("CONFIRMED", GREENC)],
    [C("<b>D.</b> Agricultural area is 10 700 ha, 34% of the land area"), C("European Commission [1]"),
     C("10 700 / 31 600 ha = 33.9%. Eurostat’s implied area is 10 645 ha; surveys give 8 880–9 800 ha [4]."),
     verd("CONSISTENT", LG)],
], [42 * mm, 26 * mm, 68 * mm, 34 * mm], valign="MIDDLE"))

S += [Spacer(1, 6 * mm), SectionHeading(6, "Verdict and requests for evidence"),
      verdict_box("Supported", "Every statement reproduces from Eurostat’s published data. Confidence: high."),
      Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> Malta is lowest in each year tested, the 66 hectares is Eurostat’s own figure, and the share is "
           "far below the last published EU average. <b>Caveats that do not change the substance.</b> The 10 700 ha "
           "denominator is not sourced in the document and surveys give a smaller area; Austria and Greece are missing from "
           "the latest release; and the EU average we cite is for 2020, not 2022. <b>What this verdict does not say.</b> "
           "It does not say anything about the quality of Malta’s farming or about the causes of the low share, and it does "
           "not test the document’s statements on water."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list(["From the Commission: the source and year of the 10 700 ha and the EU average in the passage.",
                        "From Malta’s Agriculture Directorate: the organic register area for 2022–2025, to compare with "
                        "Eurostat’s 66–80 ha."]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag), P("Not needed for this verdict (maintainer rule of 5 October 2026).", small)],
              bg=AMBER_PALE, bar=AMBER)]
S += [CondPageBreak(60 * mm), Spacer(1, 6 * mm), SectionHeading(7, "Limitations")]
for l in ["We read the Commission document in the Austrian Parliament’s copy; the Commission’s own copy was not located.",
          "Eurostat’s organic-share series has no EU-27 aggregate after 2020 in the release we used, and lacks Austria "
          "from 2021 and Greece from 2022. We compared against those countries’ last published values.",
          "The Commission’s 10 700 ha and 34% are not traced to a named source; we only tested them for consistency.",
          "We did not read the Publications Office report cited in the footnote on p. 29 ◆, and did not check Malta’s "
          "national organic register.",
          "The wider document, including its statements on water quality and flood risk, is not tested here."]:
    S.append(P("• " + l, bul))
S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "European Commission (2 October 2026). Commission Staff Working Document: Third River Basin Management Plans, Second "
          "Flood Hazard and Risk Maps and Second Flood Risk Management Plans, Member State: Malta. SWD(2026) 702 final "
          "(copy on the Austrian Parliament website).", "https://www.parlament.gv.at/dokument/XXVIII/EU/94981/imfname_11680004.pdf"),
    ("2", "Eurostat. Area under organic farming (share of utilised agricultural area), dataset sdg_02_40. Retrieved 21 October 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/sdg_02_40"),
    ("3", "Eurostat. Organic crop area by agricultural production methods and crops, dataset org_cropar. Retrieved 21 October 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/org_cropar"),
    ("4", "Eurostat. Farm structure survey: utilised agricultural area (ef_lus_main); area by NUTS 3 region (demo_r_d3area). "
          "Retrieved 21 October 2026.", "https://ec.europa.eu/eurostat/databrowser/view/ef_lus_main"),
    ("5", "MiŻien. Data and calculation: data/cc-127/; tools/cc-127-report/calc.py.", ""),
])
S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "21 Oct 2026", "First issue. Verdict Supported (high confidence); no right of reply needed.")])

build_report(Report(
    number="127", out=str(FIG / "report.pdf"), kicker="Land and agriculture",
    title_lines=["Malta’s organic", "farming: lowest", "in the EU?"],
    subtitle_lines=["Testing the Commission’s statement on Malta’s", "share of organic farmland"],
    quote_lines=["“Malta has the lowest proportion of organic farming", "in the EU.”"],
    quote_size=15,
    attribution="European Commission, SWD(2026) 702 final, Malta, 2 October 2026.",
    context="“Only 66 hectares (less than 1%) … was managed organically in 2022, well below the EU average.”",
    verdict="Supported", verdict_note="Reproduces from Eurostat in every year tested",
    footer_lines=["Version 1.0  ·  21 October 2026", "Status: no right of reply needed",
                  "Prepared from published statistics.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Organic farming in Malta", version="1.0", date="21 October 2026",
    pdf_title="Malta’s organic farming: lowest in the EU? Claim Check 127",
    pdf_subject="Tests the Commission’s statement that Malta has the lowest proportion of organic farming in the EU",
    story=S))
