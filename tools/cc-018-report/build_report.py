"""Claim Check 018 report. Run fetch_data.py, fetch_more.py, fetch_cycles.py, calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []
LG = colors.HexColor("#8DB36B")
CON = colors.HexColor("#8E2F25")

# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("In February 2026 the Malta Developers Association (MDA) welcomed the IMF’s annual assessment of Malta, saying: "
        "<b>“The IMF’s assessment of the Maltese housing market confirms what the Malta Developers Association has "
        "been saying for several years.”</b> MaltaToday summarised the statement as the IMF confirming the “strength "
        "and stability” of the property sector. We tested it against the IMF report and Eurostat data and, in version "
        "1.2, checked the release’s other statements.", lead)]
S.append(key_points([
    ("The IMF does say the market is sound.",
     "House prices “remained aligned with fundamentals”, price-to-income and price-to-rent ratios “have been "
     "stable”, and the likelihood of a weakening is “currently low”."),
    ("Independent data agree.",
     "Eurostat’s price-to-income ratio for Malta fell 10.7% in 2015–2024 and is below its long-term average: "
     "incomes grew faster than house prices."),
    ("The IMF also flagged risks the statement leaves out.",
     "Banks’ exposure to real estate (72% of private loans) is “a vulnerability”; the Board urged vigilance and "
     "staff asked for closer monitoring “in view of rapid house price growth”."),
    ("Stability is not affordability.",
     "The IMF did not assess affordability. Housing-cost overburden rose from 1.1% to 2.9% in 2015–2022 on "
     "Eurostat’s comparable series; after a 2023 series break it was 6.0%, flat since."),
    ("The release’s other claims are mixed.",
     "The IMF did move Malta to a two-year cycle; Malta is the only EU member on it, but not the first (Luxembourg, "
     "2000–2002). GDP per head “nearly doubled” is the IMF’s phrase; “far higher than the EU average” overstates it."),
    ("Verdict: largely supported (high confidence).",
     "The IMF and Eurostat back the strength and stability claim; the omitted risks are caveats, not a "
     "contradiction. The side claims do not change the verdict."),
]))
S += [Spacer(1, 3 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("−10.7%", GREEN, "Malta house price-to-income ratio, 2015–2024 (Eurostat)"),
             ("72%", ORANGE, "Bank private loans tied to real estate and construction (IMF)"),
             ("110", ORANGE, "GDP per head in purchasing power, EU = 100, 2025: above average, not “far higher”"),
             ("2000", RED, "Luxembourg was on the IMF’s 24-month cycle: Malta is not the first EU economy")]),
      Spacer(1, 3 * mm),
      up_down("A statement by the MDA acknowledging the IMF’s warnings on bank exposure, which its release omits.",
              "Evidence that the IMF found overvaluation or instability, or a reading of the statement as a claim about "
              "affordability."),
      Spacer(1, 4 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the IMF report says"),
          ("4", "What the data show"), ("5", "The release’s other statements"),
          ("6", "Where the evidence points different ways"), ("7", "Testing the claim"),
          ("8", "Verdict and requests for evidence"), ("9", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The MDA published the statement on its website on 8 February 2026 [5]; the page was modified on 17 June "
           "2026, and we read that version. Its opening sentence matches the words MaltaToday quoted the same day [1], "
           "which abbreviate the association’s name to “the MDA”. The release quotes the IMF’s positive findings on "
           "valuation, banks and growth, and does not mention the IMF calling banks’ exposures to real estate “a "
           "vulnerability”. The IMF report it refers to is the 2025 Article IV consultation, published as Country "
           "Report 26/29 [2], which we read in full."))
S.append(P("Two IMF phrases the release quotes, “current data do not suggest overvaluation” and “price increases "
           "have been in line with income growth in recent years”, are not in that report. They match an IMF Selected "
           "Issues paper on Malta’s growth-at-risk [6], which the IMF published on 13 March 2026, five weeks after the "
           "release’s date. The paper also says a sharp fall in prices, though unlikely, could strain banks. Because "
           "the release was modified in June, we cannot tell whether these phrases were in the original text."))
S.append(std_table([
    [C("What was said", cellh), C("Who", cellh), C("Access", cellh)],
    [C("“The IMF’s assessment of the Maltese housing market confirms what the Malta Developers Association has been "
       "saying for several years.”"),
     C("MDA release [5]; quoted by MaltaToday [1]"), C("Read in full")],
    [C("The assessment confirms the “strength and stability” of the property sector"), C("MaltaToday summary [1]"),
     C("Read in full")],
    [C("The IMF “will be doing it every two years. Malta is the first EU economy to be given such a certificate of "
       "economic governance”"), C("MDA release [5]"), C("Read in full")],
    [C("“Since 2013, GDP per capita in Malta has nearly doubled and now is far higher than the EU average.”"),
     C("MDA release [5]"), C("Read in full")],
    [C("MDA-commissioned study: prices +59% since 2017; price-to-income 14.0 → 14.5 (2024–25)"),
     C("MaltaToday [1] ◆"), C("Study not seen")],
], [104 * mm, 38 * mm, 28 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("SCOPE NOTE", tag),
               P("This check asks whether the IMF report supports the statement. It does not assess whether more "
                 "building is desirable (see Claim Check 013 on permits and prices) or the environmental cost of "
                 "development.", small)], bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Question.</b> Does the IMF’s 2025 assessment confirm that Malta’s property sector is strong and stable, "
           "and does independent data agree? Are the release’s statements about the IMF’s consultation cycle and "
           "GDP per head accurate?"))
S.append(P("<b>Evidence.</b> The MDA’s release [5]; the IMF report, with page references [2]; Eurostat’s standardised house price-to-income "
           "ratio [3]; Eurostat real house prices and housing-cost overburden [4]; Eurostat GDP per head, house price "
           "index and household income [10]. For the consultation cycle: the IMF’s surveillance guidance [7], the latest "
           "staff report of each of the 27 EU members on the IMF eLibrary [8] and Luxembourg’s reports of 2000 and "
           "2002 [9]. Numbers are recomputed by <i>tools/cc-018-report/calc.py</i>."))
S.append(P("<b>Grades.</b> Official assessments and statistics are grade C. ◆ marks a source known second-hand."))

# ================================================================== 3
S.append(CondPageBreak(80 * mm))
S.append(SectionHeading(3, "What the IMF report says"))
S.append(std_table([
    [C("IMF wording (PDF page)", cellh), C("Supports the statement?", cellh)],
    [C("House prices “remained aligned with fundamentals and price-to-income and price-to-rent ratios have been "
       "stable” (p.19)"), C("Yes")],
    [C("“The likelihood of weakening of property and housing markets is currently low, it is a prospective risk” "
       "(p.12)"), C("Yes, with a caveat")],
    [C("Prices +6.7% in 2024; growth moderated in early 2025 “while the house price-to-income ratio remained stable” "
       "(p.11)"), C("Yes")],
    [C("“Significant exposures of banks to real estate are a vulnerability”: 72% of private loans, from 61% (p.19)"),
     C("Omitted risk")],
    [C("“In view of rapid house price growth, staff recommend enhanced monitoring” (p.20)"), C("Omitted risk")],
    [C("Directors “urged vigilance on vulnerabilities from rising exposures to real estate” (p.3)"), C("Omitted risk")],
    [C("Population density fifteen times the EU’s, “straining infrastructure, housing and public services” (p.8)"),
     C("Context")],
    [C("“It is recommended that the next Article IV consultation be held on the 24-month cycle” (p.26); “Malta has "
       "moved to the 24-month consultation cycle” (p.66)"), C("Yes, on the two-year cycle (Section 5)")],
    [C("“Per capita income has nearly doubled since 2013” (p.25); “By 2024, per capita income reached US$45 "
       "thousand, higher than the EU average, up from US$25 thousand in 2013” (p.8)"),
     C("Yes on “nearly doubled”; the IMF says “higher”, not “far higher”")],
], [130 * mm, 40 * mm]))

# ================================================================== 4
S.append(CondPageBreak(150 * mm))
S.append(SectionHeading(4, "What the data show"))
S.append(fig(FIG / "fig1_price_income.png"))
S.append(P("Figure 1. Left: Malta’s house price-to-income ratio fell below its long-term average after 2020, while the "
           "EU’s rose and then fell back. Right: Malta’s housing-cost overburden rate rose from 1.1% to 2.9% in 2015–2022; "
           "Eurostat flags a break in Malta’s series in 2023, so the step to 6.0% is not a like-for-like change.", cap))
S.append(fig(FIG / "fig2_bank_exposure.png"))
S.append(P("Figure 2. Banks’ lending tied to property, about 2015 and mid-2025 [2].", cap))
S.append(std_table([
    [C("Indicator", cellh), C("Malta", cellh), C("EU-27", cellh), C("Source", cellh), C("Grade", cellh)],
    [C("Price-to-income ratio, change 2015–2024"), C("<b>−10.7%</b>"), C("+5.7%"), C("Eurostat tipsho60 [3]"), grade_tag("C")],
    [C("Price-to-income vs long-term average, 2024"), C("92.9"), C("98.9"), C("Eurostat tipsho60 [3]"), grade_tag("C")],
    [C("Real house prices 2015–2025"), C("+34%"), C("+25%"), C("Eurostat tipsho10 [4]"), grade_tag("C")],
    [C("Housing-cost overburden, 2015 → 2022; 2023 → 2025 (break in Malta’s series in 2023)"),
     C("1.1% → 2.9%; 6.0% → 6.0%"), C("11.2% → 8.7%; 8.8% → 7.7%"), C("Eurostat ilc_lvho07a [4]"), grade_tag("C")],
    [C("Real estate share of bank private loans"), C("61% → 72%"), C("–"), C("IMF [2]"), grade_tag("C")],
    [C("House prices, annual change, 2026 Q1 and Q2 (provisional)"), C("+6.8%; +6.9%"), C("–"),
     C("Eurostat prc_hpi_q [10]"), grade_tag("C")],
], [62 * mm, 30 * mm, 30 * mm, 36 * mm, 12 * mm]))
S.append(P("All values in <i>data/cc-018/checks.csv</i>.", cap))
S.append(P("The slowdown the IMF saw in early 2025 was brief: Eurostat’s house price index rose 6.4–7.0% a year in "
           "each quarter of 2024, 5.9% and 5.6% in the first two quarters of 2025, 6.0% over 2025 as a whole, and "
           "6.8% and 6.9% in the first two quarters of 2026 (figures from mid-2025 are provisional) [10]."))
S.append(CondPageBreak(95 * mm))
S.append(fig(FIG / "fig3_prices_incomes.png"))
S.append(P("Figure 3. House prices against incomes per head, 2015 = 100. To 2024, households’ disposable income per head "
           "rose faster than house prices (index 183 against 164), which is what Eurostat’s price-to-income ratio "
           "shows. Household income for Malta is published only to 2024; house prices have kept rising about 6–7% a "
           "year since, and by mid-2026 had reached the level income per head had in 2024 [10].", cap))

# ================================================================== 5
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(5, "The release’s other statements"))
S.append(P("The release goes beyond housing. It says the IMF decided that the Maltese economy is “so strong” that its "
           "comprehensive assessment will now take place “every two years”, and that “Malta is the first EU economy "
           "to be given such a certificate of economic governance”. It also says that since 2013 GDP per capita “has "
           "nearly doubled and now is far higher than the EU average” [5]."))
S.append(P("A two-year cycle, but not the first", h2))
S.append(P("The cycle is real. The IMF staff report recommends that the next consultation “be held on the 24-month "
           "cycle”, and its annex records that “Malta has moved to the 24-month consultation cycle” [2]. The standard "
           "cycle is 12 months. The IMF’s guidance allows up to 24 months only with the member’s consent, and only if "
           "it is not of systemic or regional importance, is not perceived to be at risk from policy imbalances or "
           "facing pressing policy issues, and owes the IMF little [7]. The move therefore reflects low perceived "
           "risk and Malta’s size; the IMF does not describe it as a certificate."))
S.append(P("Malta is the only EU member on the 24-month cycle today: the latest staff reports of the other 26, "
           "published in 2025 and 2026, all name the standard 12-month cycle [8]. It is not the first. In 2000 the IMF "
           "wrote that its next consultation with Luxembourg, then as now an EU member, “is expected to be held on the "
           "24-month cycle”; the next one followed in 2002, two years later, and again proposed the following one "
           "“within 24 months” [9]."))
S.append(std_table([
    [C("IMF document", cellh), C("Member", cellh), C("Cycle", cellh), C("Grade", cellh)],
    [C("Country Report 26/29 (Feb 2026), para. 40 and Informational Annex [2]"), C("Malta"), C("<b>24 months</b>"),
     grade_tag("C")],
    [C("Latest staff reports, 2025–2026 [8]"), C("The other 26 EU members"), C("12 months"), grade_tag("C")],
    [C("Staff Country Report 00/65 (May 2000), para. 45; Country Report 02/118 (June 2002), para. 34 [9]"),
     C("Luxembourg"), C("<b>24 months</b>"), grade_tag("C")],
], [92 * mm, 40 * mm, 26 * mm, 12 * mm]))
S.append(P("Each statement in <i>data/cc-018/imf_consultation_cycles.csv</i>, with its link.", cap))
S.append(CondPageBreak(70 * mm))
S.append(P("GDP per head", h2))
S.append(P("“Nearly doubled” is the IMF’s own phrase, and in US dollars per capita income rose from about $25,000 "
           "in 2013 to $45,000 in 2024 [2]. On Eurostat’s figures in euros, it more than doubled, from €19,120 in 2013 to "
           "€42,390 in 2025. After inflation, GDP per head rose by about half. “Far higher than the EU average” is the "
           "release’s own addition: the IMF says “higher”. At market prices Malta’s GDP per head was 1.7% above the EU "
           "average in 2025; adjusted for price levels it was 10% above [10]. GDP per head measures output, not the "
           "income of residents."))
S.append(std_table([
    [C("Measure", cellh), C("2013", cellh), C("Latest", cellh), C("Change", cellh), C("Source", cellh)],
    [C("Per capita income, US dollars"), C("$25,000"), C("$45,000 (2024)"), C("×1.8"), C("IMF [2]")],
    [C("GDP per head, current prices"), C("€19,120"), C("€42,390 (2025)"), C("<b>×2.2</b>"),
     C("Eurostat nama_10_pc [10]")],
    [C("GDP per head, 2020 prices (real)"), C("€22,600"), C("€34,360 (2025)"), C("<b>×1.5</b>"),
     C("Eurostat nama_10_pc [10]")],
    [C("GDP per head vs EU-27, market prices"), C("72.8%"), C("101.7% (2025)"), C("+1.7% above"),
     C("Eurostat nama_10_pc [10]")],
    [C("GDP per head vs EU-27, purchasing power"), C("91"), C("110 (2025)"), C("+10% above"),
     C("Eurostat nama_10_pc [10]")],
], [52 * mm, 22 * mm, 30 * mm, 24 * mm, 42 * mm]))

# ================================================================== 6
S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(6, "Where the evidence points different ways"))
S.append(contested(
    "Q1  Is the market strong and stable?", "YES, ON VALUATION", GREENC,
    "The IMF finds prices in line with fundamentals and ratios stable; Eurostat’s price-to-income ratio fell 10.7% "
    "since 2015 and is below its long-term average.",
    "The IMF calls weakening a “prospective risk” and wants closer monitoring because prices are rising fast.",
    "<b>For this claim:</b> the core of the statement matches the report."))
S.append(contested(
    "Q2  Does the report confirm everything the MDA has said?", "NOT SHOWN", AMBER,
    "The MDA has long argued that prices reflect demand and incomes; the IMF and Eurostat agree on that.",
    "The MDA’s own commissioned study, as reported, said prices outpaced incomes and the price-to-income ratio was "
    "rising, the opposite of the IMF and Eurostat finding. The IMF also warns about banks’ exposure to property.",
    "<b>For this claim:</b> “what the MDA has been saying” is broad; the IMF confirms part of it."))
S.append(contested(
    "Q3  Is the market working for residents?", "OUTSIDE THE IMF’S SCOPE", GREY,
    "Overcrowding and overburden remain below the EU average (Claim Check 013).",
    "Overburden rose from 1.1% to 2.9% in 2015–2022 (about 6% since a 2023 series break), and the IMF notes housing "
    "is strained by population density.",
    "<b>For this claim:</b> stability for banks and investors is not the same as affordability."))

# ================================================================== 7
S.append(CondPageBreak(130 * mm))
S.append(SectionHeading(7, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> The IMF found the housing market sound (prices aligned with fundamentals, stable ratios)"),
     C("Stated in the report [2]; confirmed by Eurostat [3]."), verd("SUPPORTED", GREENC)],
    [C("<b>B.</b> The assessment confirms the sector’s “strength and stability”"),
     C("Yes on valuation; the IMF also lists bank exposure as a vulnerability."), verd("LARGELY SUPPORTED", LG)],
    [C("<b>C.</b> It confirms what the MDA has said for years"),
     C("Partly; the MDA’s own study pointed the other way on price-to-income."), verd("PARTLY", AMBER)],
    [C("<b>D.</b> The IMF will now assess Malta “every two years”"),
     C("The staff report recommends the 24-month cycle, and the annex says Malta “has moved” to it [2]."),
     verd("SUPPORTED", GREENC)],
    [C("<b>E.</b> Malta is “the first EU economy to be given such a certificate of economic governance”"),
     C("Not the first: Luxembourg was on the 24-month cycle in 2000–2002 [9]. Malta is the only EU member on it "
       "today [8]. The IMF’s criteria are size, low perceived risk and consent, not a certificate [7]."),
     verd("CONTRADICTED", CON)],
    [C("<b>F.</b> Since 2013 GDP per capita “has nearly doubled”"),
     C("The IMF’s own words (US$25,000 → 45,000, 2013–2024) [2]. In euros it more than doubled (×2.2 to 2025); "
       "after inflation it rose by about half (×1.5) [10]."), verd("LARGELY SUPPORTED", LG)],
    [C("<b>G.</b> GDP per capita is now “far higher than the EU average”"),
     C("The IMF says “higher”. Eurostat, 2025: 1.7% above the EU average at market prices, 10% above in purchasing "
       "power [10]."), verd("NOT SUBSTANTIATED", ORANGE)],
], [52 * mm, 88 * mm, 30 * mm], valign="MIDDLE"))
S.append(P("Sub-claims A to C concern the housing statement on which the verdict rests. D to G, added in version 1.2, "
           "are the release’s statements about the wider economy; they are rated separately and do not change the "
           "verdict.", cap))

# ================================================================== 8
S += [Spacer(1, 6 * mm), SectionHeading(8, "Verdict and requests for evidence"),
      verdict_box("Largely supported", "The IMF and Eurostat back the strength and stability claim; the statement "
                  "leaves out the IMF’s warnings on bank exposure. Confidence: high."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) The IMF report says what the MDA says it says about valuation and stability. (2) Eurostat’s "
           "independent ratio agrees. (3) The statement does not mention the IMF’s concern about banks’ growing "
           "exposure to property or its call for closer monitoring, and the IMF did not assess affordability. These "
           "omissions qualify the claim without reversing it. (4) The release’s statements about the wider economy "
           "are mixed: the two-year cycle is real, but Malta is not the first EU economy on it, and GDP per head is "
           "above the EU average rather than far above it. They are not part of the housing claim."))
S.append(P("<b>Confidence is high.</b> The MDA’s own release has been read and matches the quoted wording, and the IMF "
           "report and Eurostat’s independent data agree on the housing findings. One caveat remains: the release was "
           "modified on 17 June 2026, after publication, and the original text was not seen."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "The text of the MDA’s release as first published on 8 February 2026, and what was changed on 17 June 2026.",
    "The MDA-commissioned study (November 2025) and how its price-to-income ratio is defined.",
    "The basis for calling Malta “the first EU economy” on the IMF’s two-year cycle.",
]))

# ================================================================== 9
S += [Spacer(1, 6 * mm), SectionHeading(9, "Limitations")]
for l in ["The MDA’s release was modified on 17 June 2026, after publication; we read the modified version and "
          "could not see the original.",
          "Eurostat’s price-to-income ratio uses national-accounts income per head; it can differ from wage-based "
          "measures such as the MDA study’s.",
          "National averages hide differences between first-time buyers, renters and owners.",
          "Eurostat flags a break in Malta’s housing-cost overburden series in 2023; values before and after it are "
          "not comparable.",
          "House prices from mid-2025 and household income for 2021–2024 are provisional; Malta’s household income "
          "is not yet published for 2025 or 2026.",
          "The comparison of consultation cycles uses each EU member’s latest staff report (2025–2026); earlier "
          "years were checked only for Luxembourg, so other earlier cases may exist."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Zammit J. (8 Feb 2026). Malta Development Association welcomes IMF assessment of housing market. "
          "<i>MaltaToday</i>.",
     "https://www.maltatoday.com.mt/news/national/139634/malta_development_association_welcomes_imf_assessment_housing_market"),
    ("2", "International Monetary Fund (2026). Malta: 2025 Article IV Consultation. IMF Country Report No. 26/29. "
          "doi:10.5089/9798229038249.002.",
     "https://www.imf.org/-/media/files/publications/cr/2026/english/1mltea2026001-source-pdf.pdf"),
    ("3", "Eurostat. tipsho60, standardised house price-to-income ratio; retrieved 4 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/tipsho60/default/table"),
    ("4", "Eurostat. tipsho10 (real house prices), retrieved 3 Oct 2026; ilc_lvho07a (housing-cost overburden, with "
          "status flags), retrieved 5 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/"),
    ("5", "Malta Developers Association (8 Feb 2026; modified 17 Jun 2026). A strong housing market supported by "
          "excellent fundamentals. Read 5 Oct 2026.",
     "https://mda.com.mt/a-strong-housing-market-supported-by-excellent-fundamentals/"),
    ("6", "Hasanov F. (13 Mar 2026). Malta’s growth-at-risk: exploring the effects of macro-financial factors on "
          "growth. IMF Selected Issues Paper 2026/022. doi:10.5089/9798229041652.018.",
     "https://doi.org/10.5089/9798229041652.018"),
    ("7", "International Monetary Fund (2022). Guidance note for surveillance under Article IV consultations. Policy "
          "Paper 2022/029, para. 123. doi:10.5089/9798400211522.007.",
     "https://doi.org/10.5089/9798400211522.007"),
    ("8", "International Monetary Fund. Latest Article IV staff reports of the 27 EU members, 2025–2026, on the IMF "
          "eLibrary; read 5 Oct 2026. Statements and links in data/cc-018/imf_consultation_cycles.csv.",
     "https://www.elibrary.imf.org/"),
    ("9", "International Monetary Fund. Luxembourg: Staff Report for the 2000 Article IV Consultation, Staff Country "
          "Report 00/65, para. 45, doi:10.5089/9781451824254.002; Staff Report for the 2002 Article IV "
          "Consultation, Country Report 02/118, para. 34 and Appendix I, doi:10.5089/9781451824339.002.",
     "https://doi.org/10.5089/9781451824254.002"),
    ("10", "Eurostat. nama_10_pc (GDP per head), prc_hpi_q and prc_hpi_a (house price index), nasa_10_nf_tr "
           "(household gross disposable income) and nama_10_pe (population), with status flags; retrieved 5 Oct "
           "2026.",
     "https://ec.europa.eu/eurostat/databrowser/"),
    ("11", "MiŻien. Data and calculations: data/cc-018/; tools/cc-018-report/.", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "4 Oct 2026", "First issue. Right of reply to the MDA not yet sent."),
                   ("1.1", "5 Oct 2026", "Corrections: (1) “The MDA’s own release was not found” → found and read "
                    "[5] (published 8 Feb 2026, modified 17 Jun 2026); the quote now uses its wording (“the Malta "
                    "Developers Association” where MaltaToday wrote “the MDA”) and is no longer second-hand; Section 1 "
                    "notes that the release does not mention the IMF’s “vulnerability” warning. (2) “Incomes have kept "
                    "pace with prices” → “incomes grew faster than house prices” (price-to-income −10.7%); flyer "
                    "“Prices kept pace with incomes” → “Incomes grew faster than prices”. (3) Flyer “IMF: no sign of a "
                    "bubble” → “IMF: ratios “stable””; sub-claim A “no overvaluation” → “prices aligned with "
                    "fundamentals”. (4) Housing-cost overburden: Eurostat flags a break in Malta’s series in 2023, so "
                    "“1.1% → 6.0% (2015–2025)” and “fivefold” → like-for-like runs 1.1% → 2.9% (2015–2022) and 6.0% "
                    "/ 5.9% / 6.0% (2023–2025), in the TL;DR, tile, Figure 1 caption, table, Q3, Limitations and flyer. "
                    "(5) DOI of the IMF report added to the literature record. Verdict and confidence unchanged."),
                   ("1.2", "5 Oct 2026", "Upgrade: (1) New Section 5 and sub-claims D–G test the release’s other "
                    "statements: the IMF’s two-year cycle (supported [2]); “the first EU economy” on it (contradicted: "
                    "Luxembourg was on the 24-month cycle in 2000–2002 [9]; Malta is the only EU member on it in the "
                    "2025–2026 reports [8]; IMF criteria [7]); GDP per head “nearly doubled” (largely supported) and "
                    "“far higher than the EU average” (not substantiated) [10]. (2) Section 1: the IMF phrases the "
                    "release quotes on overvaluation and income growth, not in Country Report 26/29, traced to an IMF "
                    "Selected Issues paper of 13 March 2026 [6]. (3) Section 4: house prices to the second quarter of "
                    "2026 (provisional) and Figure 3, house prices against incomes per head, 2015 = 100. (4) TL;DR, key "
                    "points, tiles, Section 3 table, Why, requests, limitations and flyer updated; sections renumbered. "
                    "Verdict unchanged."),
                   ("1.2", "5 Oct 2026", "Maintainer decision (5 Oct 2026): confidence raised from Moderate to High, "
                    "because the MDA’s own release is now verified.")])

build_report(Report(
    number="018", out=str(FIG / "report.pdf"), kicker="Housing and planning",
    title_lines=["Did the IMF", "confirm the", "developers?"],
    subtitle_lines=["Testing a developers’ claim about the IMF’s view of Malta’s housing market",
                    "against the IMF report and Eurostat"],
    quote_lines=["“The IMF’s assessment of the Maltese housing", "market confirms what the Malta Developers",
                 "Association has been saying for several years.”"], quote_size=14.5,
    attribution="Malta Developers Association, release on its website, 8 February 2026.",
    context="On the IMF’s 2025 Article IV consultation with Malta.",
    verdict="Largely supported", verdict_note="Sound on valuation; the IMF’s bank-exposure warnings omitted",
    footer_lines=["Version 1.2  ·  5 October 2026", "Status: draft (right of reply: MDA)",
                  "Prepared from the IMF report and Eurostat data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="The IMF and the developers – Malta", version="1.2", date="5 October 2026",
    pdf_title="Did the IMF confirm the developers? Claim Check 018",
    pdf_subject="Tests the MDA's claim that the IMF's assessment confirms what it has been saying about housing",
    story=S))
