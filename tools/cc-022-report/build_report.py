"""Claim Check 022 report. Run fetch_data.py, calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []
LG = colors.HexColor("#8DB36B")

S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("On 6 May 2025 the Energy Ministry said that <b>“Malta has the lowest electricity prices for domestic consumers "
        "in the European Union when measured in terms of purchasing power standards”</b>, and that “the burden on Maltese "
        "families is the lowest in the EU”. Every figure matches Eurostat, but burden is measured by price "
        "alone. <b>Measured against income, a typical Maltese bill is 2.2% of median income against 4.7% in the EU: "
        "the second lowest, after Luxembourg. On households’ actual use it is the fifth lowest.</b> Prices are held "
        "down by public subsidies that the release does not mention.", lead)]
S.append(key_points([
    ("Every figure checks out.",
     "For a typical household (2,500–4,999 kWh a year), Malta’s 14.35 PPS per 100 kWh in 2024-S2 is the lowest of "
     "27 and EUR 0.130 the third lowest in euros. In other consumption bands Malta ranks 2nd to 23rd (Figure 2)."),
    ("Against income, second.",
     "A typical bill (3,750 kWh) takes 2.2% of median income (EU 4.7%) and 3.5% of a low income at the 20th "
     "percentile (EU 7.3%): second lowest both times, after Luxembourg (Figure 4)."),
    ("On actual use, fifth.",
     "Maltese homes use more electricity than most (4,617 kWh a year, 21st of 27), a fifth of it for cooling. The "
     "average household’s bill is 1.3% of its disposable income (EU 1.9%), fifth lowest of 26."),
    ("The price is held down with public money.",
     "Malta’s price was cut from EUR 0.169 to 0.125 per kWh in 2014 and has barely moved since; the EU average "
     "rose 35% after 2020. The IMF puts energy subsidies (electricity and fuel) at about EUR 1 billion in 2022–2025."),
    ("Fewer struggle than the EU average, but not the fewest.",
     "4.5% of people are in arrears on utility bills (EU 7.0%; 9th of 27) and 7.6% cannot keep the home adequately "
     "warm (EU 8.8%; 17th of 27)."),
    ("Verdict: largely supported (moderate confidence).",
     "The price comparison is accurate, and Malta’s burden is among the EU’s lowest on every measure we tried, but "
     "the lowest only on price. The cost of keeping prices low, borne by public finances, is left out."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("1st", GREEN, "Lowest price in purchasing power, typical household (2,500–4,999 kWh), 2024-S2"),
             ("2nd", GREEN, "Typical bill as a share of median income, 2.2% (EU 4.7%); Luxembourg is lower"),
             ("5th", ORANGE, "Average household’s actual bill as a share of its income, 1.3% (EU 1.9%)"),
             ("€1.0bn", RED, "Energy subsidies 2022–2025, electricity and fuel together (IMF; 2025 projected)")]),
      Spacer(1, 4 * mm),
      up_down("Household Budget Survey results after 2022 showing the lowest share of spending on electricity in the "
              "EU, with the subsidy cost shown alongside.",
              "Evidence that subsidy costs fall on households through other bills, or newer data placing Malta lower "
              "on the income-based measures."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim"), ("2", "Method"), ("3", "What the data show"),
          ("4", "What “burden” means: price, income and use"), ("5", "Where the evidence points different ways"),
          ("6", "Testing the claim"), ("7", "Verdict and requests for evidence"), ("8", "Limitations")])
S.append(PageBreak())

S.append(SectionHeading(1, "The claim"))
S.append(P("The press release by the Ministry for the Environment, Energy and Public Cleanliness was read in full [1]."))
S.append(std_table([
    [C("What was said", cellh), C("Access", cellh)],
    [C("“Malta has the lowest electricity prices for domestic consumers in the European Union when measured in terms of "
       "purchasing power standards (PPS)… for the second half of 2024.”"), C("Read in full")],
    [C("“…third-lowest nominal electricity price… at €0.131 per unit… the burden on Maltese families is the lowest in the "
       "EU, at 14.33 PPS per 100kWh.” Czech Republic 41.00, Cyprus 35.70, Germany 35.23 PPS."), C("Read in full")],
    [C("“This is clear confirmation that our policy is working for the benefit of the people.” (Minister Miriam Dalli)"),
     C("Read in full")],
], [140 * mm, 30 * mm]))

S += [Spacer(1, 4 * mm), SectionHeading(2, "Method")]
S.append(P("Eurostat household electricity prices (band DC, 2,500–4,999 kWh a year, all taxes) for all EU countries, "
           "2019–2025, in euros and purchasing power standards, with the other consumption bands and Malta’s price "
           "since 2012 for comparison [2]; Eurostat energy-poverty indicators [3]; energy subsidies from the IMF’s "
           "2025 Article IV report [4], converted to euros with Eurostat GDP. To test “burden” against income and use "
           "(Section 4) we added Eurostat income distribution (EU-SILC) [6], household electricity use and consumption "
           "by band [7], household numbers [8], household disposable income [9] and the 2020 Household Budget Survey "
           "[10], all retrieved on 5 October 2026 with their status flags. Numbers are recomputed by "
           "<i>tools/cc-022-report/calc.py</i> and <i>burden.py</i>. Official statistics and assessments are grade C."))

S.append(CondPageBreak(150 * mm))
S.append(SectionHeading(3, "What the data show"))
S.append(fig(FIG / "fig1_ranking.png"))
S.append(P("Figure 1. Household electricity prices in the EU, second half of 2024, typical household (2,500–4,999 "
           "kWh). Malta is third cheapest in euros and cheapest once prices are adjusted for purchasing power.", cap))
S.append(P("Malta is cheapest only in this standard band, which the release uses (Figure 2). In 2024-S2 it ranked "
           "3rd in the band below (1,000–2,499 kWh) and 2nd in the band above (5,000–14,999 kWh), but 16th for the "
           "smallest users (under 1,000 kWh) and 23rd of 27 for the largest (15,000 kWh or more), and 4th of 26 on "
           "Eurostat’s all-band average. In 2025-S2 the pattern is the same: 9th, 2nd, 1st, 2nd and 24th, and 3rd of "
           "27 on the average [2]. For the largest users Malta’s price per unit is more than double the typical one "
           "(31.9 against 14.35 PPS per 100 kWh in 2024-S2); in 19 of the 27 states it is lower for them."))
S.append(KeepTogether([fig(FIG / "fig3_bands.png"),
                       P("Figure 2. Malta’s price and rank in each household consumption band, in purchasing power "
                         "standards, second half of 2024 and of 2025. Grey dots are the other Member States; the blue "
                         "line is the EU average.", cap)]))
S.append(fig(FIG / "fig2_price_subsidy.png"))
S.append(P("Figure 3. Left: Malta’s price was cut in 2014 and has stayed flat since, while the EU average rose. Right: "
           "energy subsidies as the IMF reports them, covering fuel as well as electricity (2025 is a projection); the "
           "electricity share is not published separately.", cap))
S.append(std_table([
    [C("Indicator", cellh), C("Claim", cellh), C("Eurostat / IMF", cellh), C("Grade", cellh)],
    [C("Malta, PPS per 100 kWh, 2024-S2, band 2,500–4,999 kWh"), C("14.33, lowest"), C("<b>14.35, lowest of 27</b>"), grade_tag("C")],
    [C("Malta, nominal price, 2024-S2"), C("EUR 0.131, third lowest"), C("EUR 0.1303, third lowest"), grade_tag("C")],
    [C("Czechia / Cyprus / Germany, PPS"), C("41.00 / 35.70 / 35.23"), C("41.00 / 35.70 / 35.23"), grade_tag("C")],
    [C("Price change 2020-S1 → 2025-S2"), C("“remained stable”"), C("Malta −0.2%; EU +35.4%"), grade_tag("C")],
    [C("Energy subsidies (electricity and fuel), 2022–2025"), C("not mentioned"), C("EUR 325m, 293m, 208m, 197m (2025 projected)"), grade_tag("C")],
    [C("Unable to keep home warm, 2025"), C("–"), C("7.6% (EU 8.8%); 17th of 27"), grade_tag("C")],
    [C("Arrears on utility bills, 2025"), C("–"), C("4.5% (EU 7.0%); 9th of 27"), grade_tag("C")],
], [60 * mm, 40 * mm, 56 * mm, 14 * mm]))
S.append(P("All values in <i>data/cc-022/checks.csv</i>.", cap))

S.append(CondPageBreak(60 * mm))
S.append(SectionHeading(4, "What “burden” means: price, income and use"))
S.append(P("The release is titled “Maltese households with lowest burden”, and the minister calls the result “clear "
           "confirmation that our policy is working” [1]. A price in purchasing power standards corrects for how "
           "expensive a country is in general. It does not take account of what households earn, or of how much "
           "electricity they use: a cheap unit can still add up to a heavy bill for a household that uses a lot or "
           "earns little. We therefore measured burden four more ways, all from Eurostat, and ranked the 27 Member "
           "States on each (1 = lowest burden):"))
for t in ["• <b>Typical bill against median income:</b> 3,750 kWh a year (the middle of the typical band) at the 2024 "
          "band price, all taxes, as a share of median equivalised net income from EU-SILC 2025, which measures 2024 "
          "income [2, 6].",
          "• <b>The same bill against a low income:</b> the 20th percentile, the top of the poorest fifth [6].",
          "• <b>The average household’s actual bill:</b> household electricity use divided by the number of households, "
          "priced at the average of the band prices weighted by consumption, as a share of households’ gross "
          "disposable income per household [7–9]. Income comes from the national accounts here because EU-SILC "
          "publishes income per adult-equivalent, not per household.",
          "• <b>Electricity’s share of household spending</b> in the 2020 Household Budget Survey, the latest, which "
          "predates the 2022 price shock [10]."]:
    S.append(P(t, bul))
S.append(KeepTogether([fig(FIG / "fig4_burden.png"),
                       P("Figure 4. Malta’s rank among the EU Member States on each measure of burden (1 = lowest), with "
                         "Malta’s value and the EU-27 value. Grey dots are the other Member States.", cap)]))
S.append(std_table([
    [C("Measure", cellh), C("Malta", cellh), C("EU-27", cellh), C("Malta’s rank", cellh), C("Grade", cellh)],
    [C("Price in PPS per 100 kWh, typical household, 2024-S2 (the release’s measure)"), C("14.35"), C("28.38"),
     C("<b>1st of 27</b>"), grade_tag("C")],
    [C("Bill for 3,750 kWh as a share of median income, 2024"), C("2.2%"), C("4.7%"),
     C("<b>2nd of 27</b> (Luxembourg 1.5%)"), grade_tag("C")],
    [C("Same bill as a share of the 20th-percentile income, 2024"), C("3.5%"), C("7.3%"), C("<b>2nd of 27</b>"),
     grade_tag("C")],
    [C("Electricity use per household, 2024"), C("4,617 kWh"), C("3,524 kWh"), C("21st of 27"), grade_tag("C")],
    [C("Average household’s annual bill, 2024"), C("€689"), C("€1,041"), C("12th of 27"), grade_tag("C")],
    [C("Average bill as a share of disposable income per household, 2024"), C("1.26% (p)"), C("1.91%"),
     C("<b>5th of 26</b>"), grade_tag("C")],
    [C("Electricity’s share of household spending, 2020"), C("2.3% (e)"), C("2.8% (median of 24)"),
     C("joint 7th of 24"), grade_tag("C")],
    [C("Arrears on utility bills, 2025: all / below 60% of median income"), C("4.5% / 9.2%"), C("7.0% / 16.8%"),
     C("9th / 7th of 27"), grade_tag("C")],
    [C("Unable to keep the home adequately warm, 2025: all / below 60% of median income"), C("7.6% / 10.9%"),
     C("8.8% / 19.6%"), C("17th / 9th of 27"), grade_tag("C")],
    [C("Home not comfortably cool in summer, 2012 (latest)"), C("35.4%"), C("21.4%"), C("25th of 27"),
     grade_tag("C")],
], [70 * mm, 24 * mm, 26 * mm, 38 * mm, 12 * mm]))
S.append(P("Ranks: 1 = lowest burden or fewest people affected. (p) provisional; (e) estimated (Eurostat flags). The "
           "average bill is household use per household times the consumption-weighted price; Bulgaria has no "
           "household income in the national accounts, hence 26. All inputs and results: "
           "<i>data/cc-022/eurostat_burden_inputs.csv</i> and <i>burden_measures.csv</i>.", cap))
S.append(P("Does “lowest burden” hold?", h2))
S.append(P("On the release’s own measure, yes. Against income, Malta comes second, after Luxembourg, for a typical "
           "household and for a low-income one; the result is the same at 2,500 or 5,000 kWh, with 2023 incomes and "
           "with 2025 prices. For the average household’s actual bill Malta is fifth of 26, level with Slovakia. "
           "Before the 2022 shock, six other states spent a smaller share of household budgets on electricity "
           "(Malta joint seventh of 24, with Belgium). On every measure Malta’s burden is well below the EU average "
           "and among the lowest in the EU. It is the lowest only on the price measure the release used."))
S.append(P("<b>Use matters.</b> Maltese households use more electricity than most: 4,617 kWh a year, 21st of 27 (EU "
           "3,524). In 2024 a fifth of it went on space cooling (19.5%; EU 3.1%) and a quarter on water heating "
           "(25.8%; EU 11.4%) [7]. A low price per unit therefore adds up to a larger bill than the price ranking "
           "suggests: €689 a year for the average household, 12th lowest of 27, against €1,041 in the EU."))
S.append(P("<b>Who struggles.</b> Fewer people in Malta than in the EU as a whole are behind on utility bills (4.5% "
           "against 7.0%) or unable to keep the home warm (7.6% against 8.8%), but these rates place Malta 9th and "
           "17th of 27, not first [3]. Among people below 60% of median income the rates are about half the EU’s. "
           "Summer comfort was last measured in 2012, when 35.4% of people in Malta said their home was not "
           "comfortably cool, against 21.4% in the EU (25th of 27) [11]; Eurostat publishes no later figure."))
S += [Spacer(1, 2 * mm),
      callout([P("FAIRNESS NOTE", tag),
               P("The tariff freeze is the policy the minister credits, and the income measures bear out its effect: "
                 "since 2020, while the EU average price rose by about a third, Maltese bills stayed among the lightest "
                 "in the EU relative to income. The other side is the cost. Energy subsidies for electricity and fuel "
                 "together came to about €1 billion in 2022–2025 (IMF; 2025 projected) [4], paid through public "
                 "finances and so, in the end, by taxpayers. No household-bill measure captures that.", small)],
              bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(5, "Where the evidence points different ways"))
S.append(contested(
    "Q1  Is the burden on families the lowest in the EU?", "ON PRICE YES; ON INCOME 2ND", AMBER,
    "For a typical household (2,500–4,999 kWh), price adjusted for purchasing power is the lowest in the EU. Against "
    "income a typical bill is the second lowest (2.2% of median income; EU 4.7%), and fewer Maltese than average "
    "struggle to pay bills or heat their homes.",
    "PPS adjusts for general price levels, not for income or use. Against income Luxembourg is lower; on households’ "
    "actual bills Malta is fifth of 26, because Maltese homes use more electricity than most; on keeping warm it is "
    "17th of 27 (Section 4).",
    "<b>For this claim:</b> as a statement about price for a typical household it is accurate. As a statement about "
    "burden, Malta is among the lowest in the EU on every measure, but the lowest only on price."))
S.append(contested(
    "Q2  Is it confirmation that the policy works?", "INCOMPLETE", AMBER,
    "Prices stayed flat through the 2022 energy shock, protecting households.",
    "The stability is paid for through public finances: the IMF puts energy subsidies, for electricity and fuel "
    "together, at about EUR 1 billion in 2022–2025, with 2025 projected [4]; the IMF recommends replacing untargeted subsidies with cost-recovery tariffs and targeted support.",
    "<b>For this claim:</b> the release presents the benefit without its cost."))

S.append(CondPageBreak(90 * mm))
S.append(SectionHeading(6, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> Lowest price in PPS, 2024-S2"), C("Confirmed by Eurostat for the standard household band "
       "(2,500–4,999 kWh), the one the release uses; not the lowest in other bands [2]."), verd("SUPPORTED", GREENC)],
    [C("<b>B.</b> Third-lowest nominal price; comparison figures"), C("Confirmed [2]."), verd("SUPPORTED", GREENC)],
    [C("<b>C.</b> Prices stable since 2020"), C("−0.2% vs EU +35% [2]."), verd("SUPPORTED", GREENC)],
    [C("<b>D.</b> Lowest “burden” on families"), C("True for price. Against income, 2nd of 27 for a typical and a "
       "low-income household; on actual bills, 5th of 26 (Section 4). The subsidy cost is not counted [4]."),
     verd("LARGELY SUPPORTED", LG)],
], [52 * mm, 88 * mm, 30 * mm], valign="MIDDLE"))

S += [Spacer(1, 6 * mm), SectionHeading(7, "Verdict and requests for evidence"),
      verdict_box("Largely supported", "Every figure is accurate; the cost of keeping prices low is left out. "
                  "Confidence: moderate."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> The statistical claims match Eurostat exactly. The word “burden” and the minister’s conclusion "
           "rest on price alone. Measured against income, Malta’s burden is the second lowest in the EU, after "
           "Luxembourg, and the fifth lowest on households’ actual bills: among the lowest on every measure, but the "
           "lowest only on the price the release used. Fixed electricity and fuel prices are financed by public "
           "subsidies the IMF puts at about EUR 1 billion over 2022–2025 (electricity and fuel together; 2025 "
           "projected). These qualify the claim without contradicting it. Confidence is moderate because the "
           "income comparisons combine survey income (EU-SILC), national-accounts income and labour-force household "
           "counts, and several inputs are provisional."))
S.append(CondPageBreak(30 * mm))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "The electricity-only subsidy to Enemalta by year, separate from fuel.",
    "Household spending on electricity as a share of income, by income group, after 2022 (the latest EU "
    "Household Budget Survey is from 2020).",
]))
S += [Spacer(1, 6 * mm), SectionHeading(8, "Limitations")]
for l in ["The IMF subsidy series covers electricity and fuel; 2025 is a staff projection.",
          "The income measures combine sources with different bases: EU-SILC income is per adult-equivalent while a "
          "bill is per household; national-accounts income includes non-profit institutions and imputed items and "
          "is higher than survey income; household numbers come from the Labour Force Survey. They rank countries "
          "under stated assumptions rather than give exact burdens. Malta’s 2024 household income is provisional, "
          "and Malta and Slovakia are 0.003 points apart on the actual-bill measure.",
          "The 2024 bill is matched to EU-SILC 2025, which measures 2024 income; with EU-SILC 2024 (2023 income) "
          "Malta’s ranks are unchanged.",
          "The spending share is from 2020, before the 2022 price shock; summer comfort was last measured in 2012.",
          "The comparison uses band DC (2,500–4,999 kWh), a typical household; Malta is not the cheapest in the other "
          "bands (Section 3).",
          "The release gives 14.33 PPS; Eurostat’s current figure is 14.35. We did not keep the data as published in "
          "May 2025, so we cannot say whether this reflects a revision; the ranking is the same."]:
    S.append(P("• " + l, bul))
S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Ministry for the Environment, Energy and Public Cleanliness (6 May 2025). Electricity prices in the EU: "
          "Maltese households with lowest burden. PR250746en.",
     "https://www.gov.mt/en/Government/DOI/Press%20Releases/Pages/2025/05/06/pr250746en.aspx"),
    ("2", "Eurostat. nrg_pc_204, electricity prices for household consumers; retrieved 4 Oct 2026 (other "
          "consumption bands and Malta’s series since 2012 retrieved 5 Oct 2026).",
     "https://ec.europa.eu/eurostat/databrowser/view/nrg_pc_204/default/table"),
    ("3", "Eurostat. ilc_mdes01, ilc_mdes07; retrieved 4 Oct 2026.", "https://ec.europa.eu/eurostat/databrowser/view/ilc_mdes01/default/table"),
    ("4", "International Monetary Fund (2026). Malta: 2025 Article IV Consultation. Country Report 26/29, Table 2 and "
          "para. on energy subsidies. doi:10.5089/9798229038249.002.", "https://www.imf.org/-/media/files/publications/cr/2026/english/1mltea2026001-source-pdf.pdf"),
    ("5", "MiŻien. Data and calculations: data/cc-022/; tools/cc-022-report/.", ""),
    ("6", "Eurostat. ilc_di03 (mean and median equivalised net income) and ilc_di01 (distribution of income by "
          "quantiles), EU-SILC 2024 and 2025; retrieved 5 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/ilc_di03/default/table"),
    ("7", "Eurostat. nrg_d_hhq (household energy consumption by end use) and nrg_pc_204_v (household electricity "
          "consumption by band), 2024; retrieved 5 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/nrg_d_hhq/default/table"),
    ("8", "Eurostat. lfst_hhnhtych (private households, Labour Force Survey), 2024; retrieved 5 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/lfst_hhnhtych/default/table"),
    ("9", "Eurostat. nasa_10_nf_tr (gross disposable income, households and NPISH, S14_S15), 2024; retrieved "
          "5 Oct 2026.", "https://ec.europa.eu/eurostat/databrowser/view/nasa_10_nf_tr/default/table"),
    ("10", "Eurostat. hbs_str_t211 (structure of consumption expenditure, Household Budget Survey 2020); retrieved "
           "5 Oct 2026.", "https://ec.europa.eu/eurostat/databrowser/view/hbs_str_t211/default/table"),
    ("11", "Eurostat. ilc_hcmp03 (dwelling not comfortably cool during summer, EU-SILC 2012 module) and ilc_mdes07 "
           "(arrears on utility bills by poverty status); retrieved 5 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/ilc_hcmp03/default/table"),
])
S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or official "
                "statistics · D assertion or anecdote.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "4 Oct 2026", "First issue. Right of reply to the Energy Ministry not yet sent."),
                   ("1.1", "5 Oct 2026",
                    "Corrections. (1) “Lowest in the EU” now says it holds for the standard household band "
                    "(2,500–4,999 kWh) (TL;DR, tile, Figure 1 caption, table, Q1, sub-claim A, flyer, thumbnail); "
                    "added one sentence on the other bands (2024-S2: 3rd, 2nd, 16th, 23rd of 27; 4th of 26 on the "
                    "all-band average). (2) “Tariffs have been frozen since 2014” (no source) → Eurostat’s series: "
                    "EUR 0.169 (2013-S2) to 0.125 per kWh (2014-S2), then 0.125–0.133 to 2025-S2. (3) The IMF’s "
                    "EUR 1 billion is now described as energy subsidies for electricity and fuel together, with "
                    "2025 projected: Figure 2 caption “what that stability cost” → “energy subsidies as the IMF "
                    "reports them”; “tariff freeze is financed by” → “fixed electricity and fuel prices are "
                    "financed by” (TL;DR, Q2, Why, table, tile, flyer). (4) “Eurostat revised 14.33 to 14.35” → "
                    "difference noted without asserting a revision. (5) IMF reference: DOI added. Verdict and "
                    "confidence unchanged."),
                   ("1.2", "5 Oct 2026",
                    "Upgrade: (1) New Section 4 tests “burden” against income and use (Eurostat; Figure 4 and a "
                    "table): typical bill 2.2% of median income (EU 4.7%), 2nd of 27 after Luxembourg; 3.5% of a "
                    "20th-percentile income, 2nd; average household’s actual bill 1.26% of disposable income, 5th of "
                    "26; spending share 2.3% in 2020, joint 7th of 24; arrears 9th and keeping warm 17th of 27; "
                    "summer comfort 2012 (25th). (2) New Figure 2: Malta’s price and rank in every consumption band, "
                    "2024-S2 and 2025-S2. (3) Figure 3 (was 2) now starts in 2012 and shows the 2014 tariff cut. "
                    "(4) TL;DR, key points, tiles, Q1, sub-claim D text, Why, Limitations, references and flyer "
                    "updated; fairness note added. Verdict, confidence and sub-claim ratings unchanged."),
                   ("1.2", "5 Oct 2026",
                    "Maintainer decision (5 Oct 2026): verdict kept as Largely supported; confidence lowered from "
                    "High to Moderate, because the income-based measures in Section 4 mix survey and "
                    "national-accounts sources and some inputs are provisional."),
                   ("1.2", "5 Oct 2026", "Maintainer decision (5 Oct 2026): a right of reply is sought only where a check finds a claim Not substantiated, Misleading or Contradicted, so this check needs none; cover, page footer and flyer now say “no right of reply needed”.")])

build_report(Report(
    number="022", out=str(FIG / "report.pdf"), kicker="Climate and energy",
    title_lines=["The lowest", "electricity", "burden in the EU?"],
    subtitle_lines=["Testing a ministry claim about household electricity prices",
                    "against Eurostat and the IMF"],
    quote_lines=["“…the burden on Maltese families is the", "lowest in the EU, at 14.33 PPS per 100kWh.”"],
    quote_size=16,
    attribution="Ministry for the Environment, Energy and Public Cleanliness, 6 May 2025.",
    context="Based on Eurostat figures for the second half of 2024.",
    verdict="Largely supported", verdict_note="Lowest on price, second against income; subsidy cost left out",
    footer_lines=["Version 1.2  ·  5 October 2026", "Status: draft · no right of reply needed",
                  "Prepared from Eurostat data and the IMF report.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Electricity prices – Malta", version="1.2", date="5 October 2026",
    status_note="no right of reply needed",
    pdf_title="The lowest electricity burden in the EU? Claim Check 022",
    pdf_subject="Tests the Energy Ministry's claim that Maltese households have the EU's lowest electricity burden",
    story=S))
