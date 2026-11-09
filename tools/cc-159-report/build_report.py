"""Claim Check 159 report. Run fetch.py, calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("In its 2025 Article IV staff report on Malta (Country Report No. 26/29, February 2026), the International "
        "Monetary Fund wrote: <b>“With a population density fifteen times greater than the EU average, straining "
        "infrastructure, housing and public services, Malta cannot rely indefinitely on population growth to "
        "maintain momentum.”</b> We tested the density ratio against Eurostat and the World Bank on several "
        "definitions of the “EU average”, and the report’s population table against Eurostat.", lead)]
S.append(key_points([
    ("The ratio is right in substance, and slightly low.",
     "Eurostat gives Malta 1,817 people per km² in 2024 against 110 for the EU-27, a ratio of 16.6. The ratio passed "
     "15 in 2021 (15.1) and has risen every year since."),
    ("The answer depends on what “EU average” means.",
     "Against the EU-27 aggregate the ratio is 16.6; against the median of the other 26 states 17.2; against their "
     "unweighted mean 13.9. The staff report states no year or definition. Fifteen sits inside the 13.5–17.2 range "
     "on every basis we tried."),
    ("The population table is close to Eurostat’s, but lower.",
     "IMF 2022 and 2023 values equal Eurostat’s 1 January figures; the 2024 and 2025 values (553,000; 563,000) are "
     "about 2% below Eurostat’s (563,443; 574,250), and the 2026 projection (573,000) is 2.6% below Eurostat’s "
     "588,254."),
    ("The strain on services is a judgement, not tested here.",
     "The sentence ties density to pressure on infrastructure, housing and services and to a limit on growth. "
     "That is the staff’s assessment; it is not a statistic, and we do not rate it."),
    ("Verdict: largely supported (high confidence).",
     "The density comparison holds, with a ratio a little above the one stated; the caveats do not change the "
     "substance."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("16.6×", GREEN, "Malta’s density relative to the EU-27, 2024 (Eurostat)"),
             ("13.5–17.2×", AMBER, "range across the definitions of “EU average” we tested"),
             ("1,817", AMBER, "people per km² in Malta, 2024 (total area basis)"),
             ("−2%", AMBER, "IMF population for 2024–25 against Eurostat 1 January")]),
      Spacer(1, 4 * mm),
      up_down("Nothing: Supported is the top of the scale. A statement of the year and definition behind “fifteen "
              "times” would settle the one caveat but could not raise the verdict.",
              "A definition of “EU average” under which Malta’s density is well below 13 or above 18 times it, or "
              "evidence that the staff compared a different quantity (for example, density of built-up land)."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the data show"),
          ("4", "Where the evidence points different ways"), ("5", "Testing the claim"),
          ("6", "Verdict and requests for evidence"), ("7", "Limitations")])
S.append(PageBreak())

S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The sentence is in the IMF staff’s own voice in the Overview of the 2025 Article IV staff report on Malta, "
           "published as IMF Country Report No. 26/29 in February 2026 [1]. The Executive Board considered the report "
           "on 4 February 2026. We extracted the text of the PDF and read the sentence and the population table on "
           "9 November 2026 (page 8 and Table 1, page 32 of the PDF). The staff give no year, source or definition for "
           "the density comparison. Table 1 is sourced to “Authorities’ data, Eurostat, and IMF staff estimates and "
           "projections”."))
S.append(std_table([
    [C("Source", cellh), C("What it says", cellh), C("Our access", cellh), C("Status", cellh)],
    [C("<b>IMF</b>, Country Report 26/29, Feb 2026 [1]"),
     C("“With a population density fifteen times greater than the EU average, straining infrastructure, housing and "
       "public services, Malta cannot rely indefinitely on population growth to maintain momentum.” Table 1: "
       "population (1,000) 553 (2024), 563 (2025), 573 (2026), 584 (2027)."),
     C("PDF text read in full for these passages (imf.org refuses scripts; copy fetched through a reader)."),
     C("<b>The claim</b>")],
    [C("<b>Eurostat</b>, demo_r_d3dens [2], demo_gind [3], reg_area3 [4]"),
     C("National density; population on 1 January; area of each state."), C("Downloaded 9 Nov 2026 (data/cc-159/)."),
     C("<b>Primary data</b>")],
    [C("<b>World Bank</b>, EN.POP.DNST [5]"), C("People per km² of land area, EU states."),
     C("Downloaded 9 Nov 2026."), C("<b>Primary data</b>")],
], [38 * mm, 66 * mm, 40 * mm, 26 * mm]))

S += [Spacer(1, 4 * mm), SectionHeading(2, "Method")]
S.append(P("<b>Questions.</b> (A) Is Malta’s population density about fifteen times the EU average? (B) Is the IMF’s "
           "population path consistent with the official figures? The sentence’s link between density and strain on "
           "infrastructure, housing and services is a judgement and is not rated."))
S.append(P("<b>Evidence.</b> The ratio was recomputed from Eurostat’s national density (people per km² of total area) "
           "for Malta and the EU-27 aggregate for 2015–2024; for the EU-27 excluding Malta from population and area; "
           "for the median and unweighted mean of the other 26 states; and, as a cross-check on land area, from the "
           "World Bank series. The IMF’s population values were compared with Eurostat’s population on 1 January "
           "(<i>tools/cc-159-report/calc.py</i>; outputs in <i>data/cc-159/checks.csv</i>)."))
S.append(P("<b>Grades.</b> Official statistics, grade C. No literature is needed to test these figures. "
           "<b>Verdicts</b> follow the five-point scale in Appendix A."))

S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(3, "What the data show"))
S.append(fig(FIG / "fig1_ratio_years.png", width=CW * 0.98))
S.append(P("Figure 1. Malta’s density as a multiple of the EU-27 aggregate, 2015–2024. The ratio crossed fifteen in "
           "2021 and was 16.6 in the latest year.", cap))
S.append(P("In 2024 Malta had 1,817 people per km² and the EU-27 110 (Eurostat flag: provisional) [2]. Malta is the "
           "densest country in the EU by a wide margin: the next, the Netherlands, has 530. Malta’s density rose by "
           "29% between 2015 and 2024 while the EU’s rose by 1.5%, which is why the ratio keeps climbing; the "
           "staff’s “fifteen” is the right order and describes roughly 2021–22."))
S.append(fig(FIG / "fig2_ratio_bases.png", width=CW * 0.98))
S.append(P("Figure 2. Malta’s density divided by different versions of “the EU average”. The EU-27 aggregate, which "
           "weights states by area and population, is the usual meaning of an EU average.", cap))
S.append(P("The unweighted mean of national densities is pulled up by a few dense states (the Netherlands, Belgium) "
           "and gives a lower ratio, 13.9. The median gives 17.2. The World Bank, which divides by land area, "
           "gives similar results (Malta 1,805; 16.6 times the median state; 13.5 times the mean) [5]."))
S.append(CondPageBreak(75 * mm))
S.append(fig(FIG / "fig3_population.png", width=CW * 0.95))
S.append(P("Figure 3. The IMF’s population values (Table 1) and Eurostat’s population on 1 January. The IMF’s 2022 "
           "and 2023 values match Eurostat’s; later values are 2–3% lower.", cap))
S.append(P("The IMF values for 2022 and 2023 (520,000 and 542,000) equal Eurostat’s 1 January figures (520,174 and "
           "542,051) [3]. For 2024 and 2025 the staff figures are staff estimates and projections and are 1.9% and "
           "2.0% below Eurostat’s 1 January values; the 2026 value is 2.6% below. We do not know whether the gap "
           "reflects timing, a revision, or a different definition of the population. If the IMF’s 2025 population "
           "is used in the density, the ratio is 16.2 rather than 16.6 (calc.py)."))

S.append(CondPageBreak(80 * mm))
S.append(SectionHeading(4, "Where the evidence points different ways"))
S.append(contested("Is Malta’s density “fifteen times” the EU average?", "ABOUT RIGHT; LATEST DATA GIVE 16–17", AMBER,
                   "On Eurostat’s 2024 data Malta’s density is 16.6 times the EU-27’s, and on the 2021 data 15.1 times: "
                   "fifteen is within the range of defensible figures and is the ratio of the early 2020s [2].",
                   "On the latest year the ratio is above sixteen on the aggregate, the median and the EU "
                   "excluding Malta, so “fifteen” understates it by about a tenth. Against an unweighted mean "
                   "of national densities it is 13.9, a tenth below fifteen.",
                   "A rounded “fifteen times” is a fair summary of a ratio between 14 and 17 on every common "
                   "definition. The report does not say which year it used, so we cannot say which side its "
                   "figure is closer to.",
                   label_a="FOR THE CLAIM", label_b="AGAINST"))

S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(5, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> Malta’s population density is fifteen times the EU average"), C("IMF [1]"),
     C("16.6× the EU-27 aggregate in 2024 (1,817 vs 110 per km²); 15.1× in 2021; 13.9–17.2× on other definitions "
       "of the average. No year or definition stated."), verd("LARGELY ACCURATE", GREENC)],
    [C("<b>B.</b> Population (Table 1): 553,000 (2024), 563,000 (2025), 573,000 (2026), 584,000 (2027)"), C("IMF [1]"),
     C("IMF 2022–23 equal Eurostat; 2024 and 2025 are 1.9% and 2.0% below Eurostat’s 1 January values, 2026 is "
       "2.6% below. 2027 has no outturn."), verd("CLOSE; SLIGHTLY LOW", GREENC)],
    [C("<b>C.</b> Density strains infrastructure, housing and services, so Malta cannot rely indefinitely on "
       "population growth"), C("IMF [1]"),
     C("A policy judgement, not a measurement. Not rated."), verd("NOT RATED", GREY)],
], [42 * mm, 18 * mm, 76 * mm, 34 * mm], valign="MIDDLE"))

S += [Spacer(1, 6 * mm), SectionHeading(6, "Verdict and requests for evidence"),
      verdict_box("Largely supported", "The density comparison holds, at a ratio slightly above the one stated "
                  "(16.6 on 2024 data). Confidence: high."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> Malta’s density is between 14 and 17 times the EU average on every common definition, "
           "and 16.6 times the EU-27 aggregate in the latest year. “Fifteen times” is a little low for 2024 but "
           "matches the ratio in 2021–22, and the staff’s population figures follow Eurostat’s within about "
           "2–3%. These caveats do not change the substance. "
           "<b>What this verdict does not say.</b> It does not assess whether density strains infrastructure, "
           "housing or public services, or whether the growth model can continue: those are the staff’s "
           "judgements."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list(["From the IMF: the year and the definition of “EU average” behind “fifteen times”.",
                        "From the IMF: the basis of the 2024–2027 population values in Table 1 and why they sit about "
                        "2% below Eurostat’s."]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag),
               P("Not needed for this verdict (maintainer rule of 5 October 2026).", small)], bg=AMBER_PALE, bar=AMBER)]
S += [Spacer(1, 6 * mm), SectionHeading(7, "Limitations")]
for l in ["The IMF PDF was refused to scripts (HTTP 403) and the Internet Archive was unreachable on 9 November 2026; "
          "we read the text through a reader and checked the sentence and table by extracting the PDF locally. "
          "The page was not archived by our tool and needs archiving by hand.",
          "Eurostat divides by total area and the World Bank by land area; the two differ for Malta by about "
          "12 people per km² and do not change the conclusion.",
          "The Eurostat EU-27 density for 2024 carries the flag ‘provisional’ (and earlier years ‘estimated’ or "
          "‘break’); Malta’s values carry no flag.",
          "We do not know which year the staff used. The report was written in 2025–26, so 2024 or 2025 data are "
          "the likely basis, but that is our inference."]:
    S.append(P("• " + l, bul))
S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "International Monetary Fund. Malta: 2025 Article IV Consultation – Press Release and Staff Report, IMF Country "
          "Report No. 26/29, February 2026 (PDF read 9 Nov 2026).",
     "https://www.imf.org/-/media/files/publications/cr/2026/english/1mltea2026001-source-pdf.pdf"),
    ("2", "Eurostat. Population density by NUTS 3 region (demo_r_d3dens), national level, updated 25 Feb 2026, retrieved "
          "9 Nov 2026.", "https://ec.europa.eu/eurostat/databrowser/view/demo_r_d3dens/default/table"),
    ("3", "Eurostat. Population change – demographic balance (demo_gind), updated 27 Oct 2026, retrieved 9 Nov 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/demo_gind/default/table"),
    ("4", "Eurostat. Area by NUTS 3 region (reg_area3), updated 22 Jan 2026, retrieved 9 Nov 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/reg_area3/default/table"),
    ("5", "World Bank. Population density (people per sq. km of land area), EN.POP.DNST, last updated 8 Oct 2026, "
          "retrieved 9 Nov 2026.", "https://data.worldbank.org/indicator/EN.POP.DNST"),
    ("6", "MiŻien. Calculation script and outputs: tools/cc-159-report/calc.py; data/cc-159/checks.csv.", ""),
])
S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "9 Nov 2026", "First issue. Verdict Largely supported (high confidence); no right of reply needed.")])

build_report(Report(
    number="159", out=str(FIG / "report.pdf"), kicker="Statistics and international reports",
    title_lines=["Fifteen times", "the EU", "average?"],
    subtitle_lines=["Testing an IMF staff statement on Malta’s", "population density against Eurostat and the World Bank"],
    quote_lines=["“With a population density fifteen times", "greater than the EU average …”"], quote_size=15,
    attribution="International Monetary Fund staff, Country Report No. 26/29, February 2026.",
    context="Overview of the 2025 Article IV staff report on Malta.",
    verdict="Largely supported", verdict_note="The ratio is 16.6 on 2024 data; fifteen is slightly low",
    footer_lines=["Version 1.0  ·  9 November 2026", "Status: no right of reply needed",
                  "Prepared from public sources and open data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Population density – IMF, February 2026", version="1.0", date="9 November 2026",
    pdf_title="Fifteen times the EU average? Claim Check 159",
    pdf_subject="Tests the IMF staff's statement on Malta's population density",
    story=S))
