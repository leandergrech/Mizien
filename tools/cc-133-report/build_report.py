"""Claim Check 133 report. Run fetch.py, calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
verd = lambda t, c: chip(t, c, w=29 * mm)
LG = colors.HexColor("#8DB36B")
S = []
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("In its 2026 Country Report for Malta, published on 3 June 2026, the European Commission wrote that sustained "
        "demand “continues to drive nominal property prices, which have risen steadily since 2014 and consistently "
        "outpace EU average growth. <b>However, with income growth exceeding these gains, the price-to-income ratio has "
        "actually declined, tempering the impact on overall affordability</b>.” We tested each part against Eurostat’s "
        "house price index, its standardised price-to-income ratio (the indicator the Commission’s own annex reproduces), "
        "household income in the national accounts, and median household income from EU-SILC.", lead)]
S.append(key_points([
    ("The ratio has declined, on the Commission’s indicator.",
     "Eurostat’s standardised ratio for Malta fell 11.5% in 2014–2024 and 23.1% since 2007 (EU-27: +5.8% since 2014). "
     "We recomputed Malta’s 2024 value exactly."),
    ("Prices rose every year since 2014, but not faster than the EU every year.",
     "Malta’s prices rose 83.6% in 2014–2025 (EU-27: 65.6%), by 3.4% to 6.7% a year; but EU-27 prices rose faster in "
     "2020, 2021 and 2022."),
    ("“Income growth exceeding these gains” depends on which income.",
     "Household income per head in the national accounts rose 95.7% in 2014–2024, faster than prices (73.3%); median "
     "household income (EU-SILC) rose 62.6%, slower. Since 2007 both measures show a decline in the ratio."),
    ("Verdict: largely supported (moderate confidence).",
     "Right on the indicator the Commission names; “consistently” is too strong, the decline since 2014 rests on an "
     "aggregate income measure, and the ratio says nothing about renters."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("−11.5%", GREEN, "Malta’s price-to-income ratio, 2014–2024 (EU-27: +5.8%)"),
             ("+83.6%", GREEN, "Malta’s nominal house prices, 2014–2025 (EU-27: +65.6%)"),
             ("3 of 11", AMBER, "years since 2014 in which EU-27 prices rose faster (2020–2022)"),
             ("+6.6%", AMBER, "the ratio 2014–2024 if median household income (EU-SILC) is used instead")]),
      Spacer(1, 4 * mm),
      up_down("A ‘Supported’ verdict would need the decline to hold on household-level income as well (for example "
              "median or lower-quartile income from EU-SILC, or a Commission borrowing-capacity series for Malta), and "
              "the word “consistently” to be read as cumulative growth.",
              "Revisions to Malta’s provisional household income for 2021–2024 large enough to remove the decline since "
              "2014, or evidence that the Commission meant the ratio for typical households, for which the median-income "
              "measure points the other way."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "Nominal house prices since 2014"),
          ("4", "The price-to-income ratio"), ("5", "Which income? Two measures disagree"),
          ("6", "What the ratio does and does not show"), ("7", "Testing the claim"),
          ("8", "Verdict and requests for evidence"), ("9", "Limitations")])
S.append(PageBreak())

S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The claim is in the Commission’s 2026 Country Report for Malta (staff working document SWD(2026) 218 final), "
           "in the summary section on housing [1]. We read the document in full from the Council’s register copy (document "
           "10135/26 ADD 1) on 25 and 26 October 2026. The passage (PDF p. 8) reads:"))
S.append(P("“Sustained demand is accelerating price growth in Malta’s property and rental markets. Residential property "
           "transactions reached new highs in 2025 (see Annex 16), continuing a long-term upward trend. This continues to "
           "drive nominal property prices, which have risen steadily since 2014 and consistently outpace EU average growth. "
           "However, with income growth exceeding these gains, the price-to-income ratio has actually declined, tempering "
           "the impact on overall affordability (see Annex 16). Meanwhile, rental prices continue to climb, boosted by high "
           "demand from foreign workers and tourists.”", bul))
S.append(P("Annex 16 (housing, PDF pp. 113–116) adds the period and the source. It says that “the price-to-income ratio in "
           "Malta has declined since 2007” and that “slightly higher overall income growth has offset the increase in house "
           "prices”; it plots nominal prices, rents and the price-to-income ratio for Malta and the EU-27 with “Source: "
           "Eurostat” (Graph A16.1), and its Graph A16.3 tabulates the ratio for Malta as 96.9 in 2023 and 92.7 in 2024 "
           "(2000–25 average = 100), down 2.2% and 4.3% on the year [1]. The same annex says house prices and rents rose 5.9% "
           "and 1.7% between 2024 and 2025."))
S.append(std_table([
    [C("What was said", cellh), C("Where", cellh), C("Access", cellh)],
    [C("Nominal property prices have risen steadily since 2014"), C("Summary, PDF p. 8 [1]"), C("Read in full")],
    [C("…and consistently outpace EU average growth"), C("Summary, PDF p. 8 [1]"), C("Read in full")],
    [C("With income growth exceeding these gains, the price-to-income ratio has actually declined"),
     C("Summary, p. 8; Annex 16, p. 113 (“since 2007”) [1]"), C("Read in full")],
    [C("…tempering the impact on overall affordability"), C("Summary, PDF p. 8 [1]"), C("Read in full")],
], [94 * mm, 46 * mm, 30 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("SCOPE NOTE", tag),
               P("This check tests the figures and what the price-to-income ratio does and does not show. It does not "
                 "assess whether housing in Malta is affordable for any particular group, or the Commission’s policy "
                 "points on social housing and rent caps. Other checks cover house prices and planning permits (CC-013, "
                 "CC-018, CC-123). The rental sentence that follows the claim is context here, not a rated sub-claim.",
                 small)], bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

S.append(SectionHeading(2, "Method"))
S.append(P("<b>Question.</b> Did Malta’s nominal house prices rise steadily and faster than the EU’s since 2014, did income "
           "grow faster than those prices, and has the price-to-income ratio declined? <b>Evidence.</b> From Eurostat, all "
           "downloaded on 26 October 2026 with status flags: the house price index (prc_hpi_a, total purchases) [3]; the "
           "standardised house price-to-income ratio (tipsho60), a Macroeconomic Imbalance Procedure (MIP) auxiliary "
           "indicator [2]; household adjusted and unadjusted gross disposable income (nasa_10_nf_tr, B7G and B6G, households "
           "and NPISH) and population (nama_10_pe) [4]; median equivalised net income from EU-SILC (ilc_di03) [5]; and the "
           "HICP index of actual rentals (prc_hicp_aind, CP041) [6]. Eurostat defines the ratio’s income as adjusted "
           "household gross disposable income per head of population [7]. We compared Eurostat’s values with the "
           "Commission’s Graph A16.3, recomputed the ratio from its parts, and repeated it with median household income "
           "(<i>tools/cc-133-report/calc.py</i>; inputs in <i>data/cc-133/</i>; results in <i>checks.csv</i>). The "
           "Commission’s 2025 housing discussion paper [8] is read for how DG ECFIN uses the ratio. <b>Grades.</b> Official "
           "statistics and Commission analysis are grade C; peer-reviewed work on affordability measures is cited as "
           "context (grade C, a review and a measurement study, abstracts read) [9, 10]. Verdicts follow the scale in "
           "Appendix A."))

S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(3, "Nominal house prices since 2014"))
S.append(P("Eurostat’s house price index covers all purchases of new and existing dwellings by households, at market "
           "prices, including land [7]; for Malta it is compiled from the national statistics office’s data. Malta’s "
           "index rose every year from 2015 to 2025, by between 3.4% (2020) and 6.7% (2022 and 2024), and by 83.6% in all "
           "from 2014 to 2025; the EU-27 index rose 65.6% [3]. On a 2005 base, Malta’s index stands at 297 in 2025 and the "
           "EU-27’s at 189, the two end-points of the Commission’s Graph A16.1 [1, 3]. “Risen steadily since 2014” is "
           "therefore accurate."))
S.append(fig(FIG / "fig2_growth.png"))
S.append(P("Figure 1. Annual change in nominal house prices, Malta and the EU-27, 2015–2025. In the shaded years "
           "(2020–2022) EU-27 prices rose faster than Malta’s.", cap))
S.append(P("“Consistently outpace EU average growth” is not accurate year by year. Malta’s annual growth was above the "
           "EU-27’s in 8 of the 11 years, but below it in 2020 (3.4% against 5.6%), 2021 (5.1% against 8.4%) and 2022 (6.7% "
           "against 8.0%) [3]. Measured cumulatively from 2014, Malta stayed ahead in every year, but only just in 2022 "
           "(52.8% against 52.3%). The Commission’s annex uses the cumulative reading (“over the past decade… clearly "
           "outpacing developments in the EU”) [1]; the summary’s “consistently” overstates it."))

S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(4, "The price-to-income ratio"))
S.append(P("The standardised price-to-income ratio divides the nominal house price index by adjusted household gross "
           "disposable income per head, both as indices, so it shows how prices have moved relative to average income, "
           "not how many years of income a home costs [2, 7]. Eurostat’s ratio for Malta peaked in 2008 and has fallen "
           "since: by 23.1% from 2007 to 2024 and by 11.5% from 2014 to 2024. Over 2015–2020 it hardly moved (−1.3%); most "
           "of the fall since 2014 came in 2021 and in 2023–2024. Over the same decade the EU-27 ratio rose 5.8% [2]."))
S.append(fig(FIG / "fig1_index.png"))
S.append(P("Figure 2. Nominal house prices and the price-to-income ratio, Malta and the EU-27, 2005 = 100. Malta’s prices "
           "almost trebled while its ratio ended slightly below its 2005 level.", cap))
S.append(P("The Commission’s figures match Eurostat’s closely. For 2023 and 2024 Graph A16.3 gives Malta 96.9 and 92.7 "
           "(2000–25 average = 100) and annual changes of −2.2% and −4.3%; Eurostat’s published ratio relative to its "
           "long-term average gives 97.1 and 92.9, and −2.2% and −4.4% [1, 2]. The small differences are consistent with a "
           "different averaging period or data vintage; the report does not say which it used. We recomputed Eurostat’s "
           "2024 value for Malta (89.29, 2015 = 100) exactly from the house price index, household adjusted disposable "
           "income and population [3, 4]. DG ECFIN’s own quarterly ratio, shown in its 2025 discussion paper, also puts "
           "Malta’s ratio at the end of 2024 below its 2014 level and well below 2007 [8, Graph 9 and Annex V; read from "
           "the chart, no values given]."))

S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(5, "Which income? Two measures disagree"))
S.append(P("The ratio’s income is a national-accounts aggregate: the adjusted gross disposable income of households and "
           "non-profit institutions serving households, divided by the whole population [4, 7]. “Adjusted” means it "
           "includes social transfers in kind such as public health and education. EU-SILC’s median equivalised net "
           "income instead describes the household in the middle of the distribution, adjusted for household size, and "
           "refers to the year before the survey [5]. These are definitions, not explanations of the gap below."))
S.append(fig(FIG / "fig3_income.png"))
S.append(P("Figure 3. Malta, 2014 = 100: nominal house prices, household adjusted disposable income per head, and median "
           "equivalised household income (EU-SILC, plotted at the income year).", cap))
S.append(contested(
    "Did income grow faster than house prices since 2014?", "DEPENDS ON MEASURE", AMBER,
    "Adjusted household disposable income per head rose 95.7% in 2014–2024, against 73.3% for house prices; the ratio "
    "fell 11.5%. Unadjusted disposable income per head gives the same result (+95.5%; ratio −11.4%) [3, 4]. This is the "
    "income in the indicator the Commission cites.",
    "Median equivalised household income (EU-SILC) rose 62.6% over income years 2014–2024, less than house prices; on "
    "that measure the ratio rose 6.6% (8.2% over 2013–2023). Malta’s population grew 31.2% in 2014–2024 against 2.1% "
    "for the EU-27, so per-head aggregates and the typical household can diverge [3, 4, 5].",
    "Since 2007 both measures agree that incomes outgrew prices (median income +120.1%, prices +93.1%; ratio −12.3%). "
    "Since 2014, the period the summary sentence names, only the aggregate measure supports “income growth exceeding "
    "these gains”. Malta’s household income for 2021–2024 is flagged provisional by Eurostat [4]. The Commission’s "
    "sentence names the ratio, and on that indicator it is right; but for the typical household the decline since 2014 "
    "is not shown."))
S.append(P("The EU-27 comparison is less sensitive to the choice: there both measures show prices outgrowing income since "
           "2014 (aggregate ratio +5.8%; median-income ratio +5.5%) [2, 5]."))

S.append(CondPageBreak(90 * mm))
S.append(SectionHeading(6, "What the ratio does and does not show"))
S.append(P("<b>It is a relative, average measure.</b> An index ratio shows change against its own past, not a level of "
           "affordability, and an average or median ratio can hide what happens to lower-income buyers. Gan and Hill argue "
           "that median-based measures can understate affordability problems and distinguish the ability to buy from the "
           "burden of repayments [9]; Stone argues for measuring what households have left after housing costs [10]. We "
           "read both abstracts only; they support caution about reading “overall affordability” from one ratio, not a "
           "conclusion about Malta."))
S.append(P("<b>Interest rates and credit matter.</b> The Commission’s 2025 discussion paper notes that, with the exception "
           "of Bulgaria, Romania and Malta, house price growth exceeded the change in households’ borrowing capacity "
           "between 2019 and 2024 [8, p. 23]; the Country Report says the same of Malta (“did not exceed the change in the "
           "borrowing capacity of the population”) and cites stable, low mortgage rates [1]. This supports the "
           "Commission’s reading for buyers who borrow."))
S.append(P("<b>It says nothing about renters.</b> The sentence after the claim says rents “continue to climb”. Eurostat’s "
           "HICP for actual rentals rose 15.2% in 2023 and 8.9% in 2024, far above the EU-27’s 3.0% and 3.1%, then 1.7% in "
           "2025 [6], the figure the annex gives for 2024–2025. The Commission’s own Graph A16.3 shows Malta’s rent-to-income "
           "ratio falling (83.0, 81.0 and 79.4 in 2023–2025, 2000–25 average = 100) and the housing-cost overburden rate "
           "for tenants at market rent at 25.5% in 2023 and 19.7% in 2024 [1]. “Tempering the impact on overall "
           "affordability” is a fair reading of an average; the annex itself stresses the pressure on vulnerable groups."))

S.append(CondPageBreak(95 * mm))
S.append(SectionHeading(7, "Testing the claim"))
S.append(std_table([
    [C("Sub-claim", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> Nominal property prices have risen steadily since 2014"),
     C("Up every year 2015–2025, by 3.4% to 6.7%; +83.6% in all [3]."), verd("ACCURATE", GREENC)],
    [C("<b>B.</b> …and consistently outpace EU average growth"),
     C("Cumulatively ahead every year (+83.6% vs +65.6% by 2025), but EU-27 annual growth was higher in 2020, 2021 and "
       "2022 [3]."), verd("OVERSTATED", AMBER)],
    [C("<b>C.</b> Income growth exceeding these gains"),
     C("Yes for household adjusted disposable income per head (+95.7% vs prices +73.3%, 2014–2024); no for median "
       "household income (+62.6%) [3, 4, 5]."), verd("DEPENDS ON MEASURE", AMBER)],
    [C("<b>D.</b> The price-to-income ratio has actually declined"),
     C("Eurostat ratio −11.5% since 2014 and −23.1% since 2007; recomputed; matches the Commission’s Graph A16.3 [1, 2]."),
     verd("ACCURATE", GREENC)],
    [C("<b>E.</b> …tempering the impact on overall affordability"),
     C("A fair reading of an average ratio and of borrowing capacity [8]; it does not cover renters or lower-income "
       "households [1, 6, 9]."), verd("FAIR, LIMITED", LG)],
], [52 * mm, 88 * mm, 30 * mm], valign="MIDDLE"))
S.append(P("The rental sentence and the Commission’s policy points are not rated.", cap))

S += [Spacer(1, 6 * mm), SectionHeading(8, "Verdict and requests for evidence"),
      verdict_box("Largely supported", "The ratio has declined on the indicator named; the caveats are the word "
                  "“consistently” and the choice of income. Confidence: moderate."),
      Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) The central claim, that Malta’s price-to-income ratio has declined, holds on Eurostat’s "
           "standardised indicator over any start year from 2007 to 2014, recomputes exactly, and matches the Commission’s "
           "annex. (2) Prices have risen every year since 2014. (3) “Consistently outpace EU average growth” is true "
           "cumulatively but not in 2020–2022. (4) The decline rests on an aggregate income measure; median household income "
           "grew more slowly than prices after 2014, so for the typical household the ratio did not fall over that decade. "
           "These caveats qualify, but do not reverse, a statement about a named indicator, which is why the verdict is "
           "‘largely supported’ and not ‘supported’. Confidence is moderate, not high, because two income measures disagree "
           "since 2014 and Malta’s 2021–2024 household income is provisional. <b>What this verdict does not say.</b> It does "
           "not say housing in Malta is affordable, or that it is not, for any group."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "European Commission: the data vintage and averaging period behind Graph A16.3, and whether the summary’s "
    "“since 2014” and the annex’s “since 2007” refer to the same series.",
    "National Statistics Office: an explanation of the gap between household disposable income per head in the national "
    "accounts and median equivalised income in EU-SILC since 2014.",
    "Central Bank of Malta: any published price-to-income or borrowing-capacity series for Malta based on household-level "
    "income.",
]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag), P("Not needed for this verdict (maintainer rule of 5 October 2026).", small)],
              bg=AMBER_PALE, bar=AMBER)]
S += [Spacer(1, 6 * mm), SectionHeading(9, "Limitations")]
for l in ["Eurostat revises its series. The values here are those released by 16 April 2026 (price-to-income ratio), "
          "1 October 2026 (house prices; Malta 2025 provisional), 14 October 2026 (household income; Malta 2021–2024 "
          "provisional), 21 October 2026 (population) and 20 October 2026 (EU-SILC). We did not test earlier vintages.",
          "The Commission’s 2025 discussion paper gives Malta’s quarterly ratio only as charts; we read its direction from the "
          "charts and do not use any value from them.",
          "EU-SILC refers to the year before the survey and has its own sampling error; we did not test whether the gap "
          "between the two income measures is statistically significant or explain its causes.",
          "We used Eurostat’s house price index, which for Malta comes from the national statistics office. We did not test "
          "the Central Bank of Malta’s advertised-price index or any regional series.",
          "The peer-reviewed works cited are read as abstracts only (Gan and Hill via the SSRN working-paper record) and "
          "concern other countries."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), CondPageBreak(95 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "European Commission (3 Jun 2026; transmitted to the Council 8 Jun 2026). 2026 Country Report – Malta, "
          "SWD(2026) 218 final, Annexes (Council document 10135/26 ADD 1), PDF pp. 8 (summary) and 113–116 (Annex 16, "
          "housing; Graphs A16.1 and A16.3).", "https://data.consilium.europa.eu/doc/document/ST-10135-2026-ADD-1/en/pdf"),
    ("2", "Eurostat. Standardised house price-to-income ratio – annual data (tipsho60), Malta and EU-27, 2000–2024, "
          "dataset updated 16 Apr 2026; downloaded 26 Oct 2026. doi:10.2908/TIPSHO60.",
     "https://ec.europa.eu/eurostat/databrowser/view/tipsho60"),
    ("3", "Eurostat. House price index – annual data (prc_hpi_a), total purchases, Malta and EU-27, 2004–2025, updated "
          "1 Oct 2026; downloaded 26 Oct 2026.", "https://ec.europa.eu/eurostat/databrowser/view/prc_hpi_a"),
    ("4", "Eurostat. Non-financial transactions (nasa_10_nf_tr: B6G and B7G, households and NPISH, current prices) and "
          "population (nama_10_pe, POP_NC), downloaded 26 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/nasa_10_nf_tr"),
    ("5", "Eurostat. Mean and median income by age and sex – EU-SILC (ilc_di03, median equivalised net income, EUR), "
          "updated 20 Oct 2026; downloaded 26 Oct 2026.", "https://ec.europa.eu/eurostat/databrowser/view/ilc_di03"),
    ("6", "Eurostat. HICP – annual data (prc_hicp_aind, CP041 actual rentals for housing), downloaded 26 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/prc_hicp_aind"),
    ("7", "Eurostat. House price index (MIP indicators), reference metadata (tipsho20_esms): definitions, including the "
          "income used in the standardised price-to-income ratio.",
     "https://ec.europa.eu/eurostat/cache/metadata/en/tipsho20_esms.htm"),
    ("8", "Cousin G., Frayne C., Martins V., Vašíček B. (2025). Housing in the European Union: Market Developments, "
          "Underlying Drivers, and Policies. European Economy Discussion Paper 228, European Commission (DG ECFIN), "
          "14 Oct 2025. doi:10.2765/3521352 (resolves to the Publications Office; not in Crossref). Read in full, "
          "pp. 20–23 and Annex V (p. 82); CC BY 4.0.",
     "https://economy-finance.ec.europa.eu/publications/housing-european-union-market-developments-underlying-drivers-and-policies_en"),
    ("9", "Gan Q., Hill R. J. (2009). Measuring housing affordability: Looking beyond the median. <i>Journal of Housing "
          "Economics</i> 18(2):115–125. doi:10.1016/j.jhe.2009.04.003. (Abstract read, SSRN version 1310294.)",
     "https://doi.org/10.1016/j.jhe.2009.04.003"),
    ("10", "Stone M. E. (2006). What is housing affordability? The case for the residual income approach. <i>Housing "
           "Policy Debate</i> 17(1):151–184. doi:10.1080/10511482.2006.9521564. (Abstract read.)",
     "https://doi.org/10.1080/10511482.2006.9521564"),
    ("11", "Miżien. Data and calculations: data/cc-133/; tools/cc-133-report/calc.py (checks.csv).", ""),
])
S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or official "
                "statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "26 Oct 2026", "First issue. Verdict Largely supported (moderate confidence); no right of reply needed.")])

build_report(Report(
    number="133", out=str(FIG / "report.pdf"), kicker="Housing and affordability",
    title_lines=["House prices against", "incomes: has the", "ratio fallen?"],
    subtitle_lines=["Testing the Commission’s 2026 Country Report", "against Eurostat’s price and income series"],
    quote_lines=["“With income growth exceeding these gains,", "the price-to-income ratio has actually declined.”"],
    quote_size=14.5,
    attribution="European Commission, 2026 Country Report – Malta, 3 June 2026.",
    context="Summary on housing, after ‘nominal property prices… risen steadily since 2014’.",
    verdict="Largely supported", verdict_note="True on the named indicator; not for median income since 2014",
    footer_lines=["Version 1.0  ·  26 October 2026", "Status:",
                  "Prepared from public sources and Eurostat data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Price-to-income ratio – European Commission", version="1.0", date="26 October 2026",
    pdf_title="House prices against incomes: has the ratio fallen? Claim Check 133",
    pdf_subject="Tests the Commission's 2026 Country Report statement on Malta's house prices and price-to-income ratio",
    story=S))
