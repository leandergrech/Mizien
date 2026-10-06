"""Claim Check 113 report. Run fetch.py, calc.py and figures.py first. Output: out/report.pdf"""
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
      P("The European Environment Agency’s indicator page <i>Fossil fuel subsidies in Europe</i> (29 January "
        "2025) says: <b>“In 2023, fossil fuel subsidies represented the highest shares of gross domestic product (GDP) "
        "in Malta, Poland, and Slovakia (all at or above 1.5%).”</b> We rebuilt the figures from the Commission’s "
        "subsidy database that the EEA used and compared other measures of Malta’s support.", lead)]
S.append(key_points([
    ("The EEA reports its data faithfully.",
     "Rebuilt from the Commission’s subsidy database, every share on the EEA’s chart reproduces to two decimals: Malta "
     "3.37% of GDP, Poland 2.09%, Slovakia 1.51%, then Croatia 1.15%; the EU-27 as a whole 0.66% (total over EU GDP, "
     "not an average). The Commission’s report of 28 January 2025 shows the same top four [19]. In euros "
     "Malta is 19th of 27."),
    ("The top three holds; the 1.5% line is a near thing.",
     "The same three lead with Eurostat’s GDP of 6 October 2026 (which the EEA could not have had) and, as a lower "
     "bound, with unconfirmed items set to zero. Slovakia then falls to 1.49% or 1.39%."),
    ("Malta went from near the bottom to the top.",
     "Its share was 0.08–0.10% of GDP in 2015–2020 (24th to 27th of 27). In 2023, 96% of its EUR 605 million was one "
     "measure, compensation to Enemalta for keeping prices at pre-COVID levels, booked as natural-gas price support."),
    ("Other yardsticks differ, and not in one direction.",
     "For 2022 the database is lower: 1.71% of GDP (Enemalta line EUR 247 million) against the Government’s 2.5% (about "
     "EUR 451 million) and the IMF’s 1.8% (about EUR 325 million). For 2023 it is higher: EUR 580 million against "
     "about EUR 356 million (Government, expected) and EUR 293 million (IMF). Over 2022–23 the line (EUR 827 "
     "million) is close to the Government’s expected cost (about EUR 806 million): timing or basis. For 2024 the "
     "gap persists (about 1.8% against 0.87%). The IMF’s price-gap data show no explicit subsidy."),
    ("Verdict: largely supported (moderate confidence).",
     "The ranking is right on the EEA’s data and in every variant tested. Slovakia’s “at or above 1.5%” rests on "
     "provisional data; Malta’s EUR 580 million line (booked as actual costs) is not reconciled with other sources."),
]))
S += [Spacer(1, 1 * mm), VerdictMeter(1), Spacer(1, 2 * mm),
      tiles([("3.37%", GREEN, "Malta, 2023, on the EEA’s basis; EU-27 as a whole 0.66%"),
             ("1st", GREEN, "Malta’s rank in all four versions we recomputed 2023"),
             ("1.49%", ORANGE, "Slovakia with Eurostat’s GDP of 6 Oct 2026 (EEA: 1.51%)"),
             ("2.1×", ORANGE, "Database 2023 amount against the IMF Article IV cost")]),
      Spacer(1, 3 * mm),
      up_down("Final 2023 figures from the Commission’s 2025-edition database that keep Slovakia at or above 1.5%, "
              "and a documented source for Malta’s EUR 580 million that reconciles it with the Government’s and the "
              "IMF’s figures.",
              "Final 2023 figures that take Malta, Poland or Slovakia below Croatia’s 1.15%. For Malta that is under "
              "about EUR 216 million (1.15% × EUR 18,797 million) on the EEA’s basis, below even the IMF-based "
              "EUR 293 million, for example if the EUR 580 million were misbooked or counted twice."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What counts as a fossil-fuel subsidy"),
          ("4", "What the data show"), ("5", "Where the evidence points different ways"), ("6", "Testing the claim"),
          ("7", "Verdict and requests for evidence"), ("8", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The claim is the EEA’s own text, on the indicator page that tracks the EU’s commitment to phase out "
           "fossil-fuel subsidies [1]. The EEA is an EU agency; we assess its statement, not any Maltese authority’s. "
           "Our claim record summarises the sentence; the quotation below is the EEA’s wording."))
S.append(std_table([
    [C("What the EEA says", cellh), C("Where", cellh), C("Access", cellh)],
    [C("“In 2023, fossil fuel subsidies represented the highest shares of gross domestic product (GDP) in Malta, "
       "Poland, and Slovakia (all at or above 1.5%). Countries with the lowest shares were Austria, Denmark, and Estonia "
       "(less than 0.2% of GDP).”"),
     C("Indicator page, “Disaggregate level assessment” [1]"), C("Read in full, 6 Oct 2026; same wording on 3 Feb 2025 "
                                                                 "and 26 Nov 2025 [2]")],
    [C("Linked chart: “Fossil fuel subsidies as a share of national GDP, 2023”, with a note that 2023 data are "
       "provisional and use 2022 values for about 7% of the total"), C("Chart page [3]"), C("Chart data downloaded")],
    [C("Data source: “DG ENER study on energy subsidies” (“direct link to the datasets is not available”)"),
     C("Indicator metadata [1]"), C("Found: the Commission’s subsidy database on CIRCABC [4, 21]")],
], [92 * mm, 40 * mm, 38 * mm]))
S.append(P("<b>Has the page changed?</b> It shows “Published 29 Jan 2025”; its metadata record an edit on 29 July 2025. "
           "We could not open archived copies (the Wayback Machine and archive.today refused connections from our "
           "network), but the EEA itself serves two fixed copies: a browser print made on 3 February 2025 and the PDF "
           "in its 8th EAP monitoring report 2025 (26 November 2025). Both carry the sentence word for word [2]. The "
           "only difference we found is the label of the linked chart: “2020” in February 2025, “2023” now; the chart "
           "itself is for 2023 [3]. Two smaller slips remain on the live page: its method note still says the data "
           "were “deflated to 2022 prices” (the figures are in 2023 prices), and it calls the Commission’s report "
           "“forthcoming”, although it was adopted on 28 January 2025 [19]."))
S += [Spacer(1, 2 * mm),
      callout([P("SCOPE NOTE", tag),
               P("This check tests the EEA’s ranking and threshold, and asks what Malta’s figure is made of. It does not "
                 "judge whether Malta’s energy price policy is right: it was a response to the energy price crisis, and "
                 "its benefits to households are outside this check. The claim is about shares of GDP; in euros "
                 "Malta’s EUR 0.63 billion in 2023 is 19th of 27, against Germany’s EUR 41 billion [4]. The related "
                 "claim that Malta spends about EUR 400 million to keep bills low to 2027 (CC-095) is not tested "
                 "here.", small)],
              bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Question.</b> In 2023, were fossil-fuel subsidies the highest share of GDP in Malta, Poland and Slovakia, "
           "were all three at or above 1.5%, and how robust is that to the GDP series, to the provisional items and to "
           "the definition of a fossil-fuel subsidy?"))
S.append(P("<b>Evidence.</b> On 6 October 2026 we downloaded the EEA’s chart data [3], the Commission’s <i>Inventory of "
           "energy subsidies in the EU27, 2024 edition</i>, which lists every measure by country and year [4], Eurostat "
           "GDP at current prices [5], Eurostat’s general-government subsidies for Malta [15] and its electricity "
           "supply [20]. <i>tools/cc-113-report/calc.py</i> rebuilds each country’s 2023 total from the measure rows (kept "
           "locally: the database is Enerdata’s copyright, so only country totals and five Malta figures are in "
           "<i>data/cc-113/</i>) and recomputes the shares four ways: with the 2022 stand-ins (A, B) or, as a lower "
           "bound, with the unconfirmed items set to zero (C, D); with the database’s GDP (A, C) or Eurostat’s of "
           "6 October 2026 (B, D). We compared the Government’s draft budgetary plans [10, 11], the IMF’s Article IV "
           "report [12], the IMF’s price-gap database [13] and the OECD/IISD tracker [14], and read the Commission’s "
           "2024 report, COM(2025) 17 [19], whose Figure 16 gives the 2023 shares as of 28 January 2025 (we measured "
           "its bars), its newest report (17 September 2026) [8] and a paper on definitions [9]. Crossref was "
           "searched for peer-reviewed work on Malta’s energy price policy; none was found."))
S.append(P("<b>Grades.</b> Official statistics, agency indicators and official reports are grade C under our scale. "
           "<b>Verdicts</b> follow the five-point scale in Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(60 * mm))
S.append(SectionHeading(3, "What counts as a fossil-fuel subsidy"))
S.append(P("There is no single definition. A Commission discussion paper sets out the main approaches: inventories "
           "list budget transfers, tax breaks and price supports measure by measure; price-gap methods compare what "
           "users pay with a reference price; the IMF adds unpriced environmental costs [9]. Differences in scope and "
           "method “can have a large impact on total estimated amounts and comparability between countries” [9]. "
           "A peer-reviewed review discusses the common definitions [17], and a peer-reviewed study argues that subsidy "
           "inventories should be read together with carbon pricing, as a “net carbon price” [18]."))
S.append(KeepTogether([std_table([
    [C("Measure", cellh), C("What it counts", cellh), C("Malta", cellh)],
    [C("<b>EU inventory</b> (EEA indicator; Commission subsidy reports under the Governance Regulation) [4, 8, 9]"),
     C("WTO categories: direct transfers, tax expenditures, income or price support, R&amp;D. Bottom-up, measure by "
       "measure. Electricity support counted as fossil by the share of fossil fuels in the power mix, but Malta’s "
       "main line is booked wholly to natural gas (below)."),
     C("2023: EUR 605m, or 633m with the 2022 stand-in; 3.37% of GDP on the EEA’s basis; first of 27")],
    [C("<b>Government of Malta</b>, draft budgetary plans [10, 11]"),
     C("Cost of energy support: lower indirect taxes on energy, and subsidies for the higher cost of imported fuels, "
       "electricity and other basic commodities"),
     C("2.5% of GDP (2022), 1.7% (2023, expected), 0.87% (2024)")],
    [C("<b>IMF Article IV</b> [12]"), C("Fiscal cost of untargeted electricity and fuel subsidies"),
     C("1.8% of GDP (2022), 1.4% (2023), 0.9% (2024)")],
    [C("<b>IMF price-gap database</b> [13]"),
     C("Explicit: supply cost above the retail price. Implicit: unpriced environmental costs and forgone VAT"),
     C("Explicit: zero in every year. Explicit plus implicit: 2.27% (2023), 15th of 27")],
    [C("<b>OECD inventory, IEA price gap</b> (via the OECD/IISD tracker) [9, 14]"),
     C("OECD: budget transfers and tax expenditures. IEA: price gap"),
     C("The tracker carries no OECD or IEA estimate for Malta, only the IMF’s zero")],
], [52 * mm, 66 * mm, 52 * mm]), P("Table 1. The same support, measured five ways. Shares of GDP as each source gives them.", cap)]))
S.append(P("Malta’s energy price stabilisation", h2))
S.append(P("Malta has kept retail energy prices fixed through the price crisis: the Commission’s 2024 country report "
           "notes that 2023 inflation reached 5.6% “with energy prices being kept at 2020 levels” [16]. The database "
           "describes its largest Maltese item, “Energy Support Measures”, as energy prices “frozen to their pre-COVID "
           "levels as the Governement [sic] is compensating Enemalta for the losses”, and classes it as natural-gas "
           "income or price support (a consumer price guarantee), created for the price crisis [4]. Under the EU method "
           "that is a fossil-fuel subsidy. The IMF’s price-gap database, which compares retail prices with supply costs "
           "fuel by fuel, records no explicit subsidy for Malta in any year [13]; we did not find why Malta’s frozen "
           "prices do not register in it."))
S.append(P("<b>Caveat on the power mix.</b> The database books the Enemalta line wholly to natural gas, so the "
           "pro-rating by the power mix described in Table 1 was not applied to it. In 2023 Malta imported 648 of the "
           "2,992 GWh of electricity it supplied from production plus imports (21.7%) [20]. Leaving out only that "
           "import share of the line would put Malta’s 2023 share at 2.70% on the EEA’s basis, still first of 27: a "
           "bound on one part of the question, not an estimate, since imports are not all non-fossil and we did not "
           "model the domestic mix."))

# ================================================================== 4
S.append(CondPageBreak(100 * mm))
S.append(SectionHeading(4, "What the data show"))
S.append(KeepTogether([fig(FIG / "fig1_rank.png"), P(
    "Figure 1. Fossil-fuel subsidies as a share of GDP, 2023. Bars: the EEA’s basis (the Commission database with the "
    "2022 stand-ins, divided by the database’s GDP), which reproduces every value on the EEA’s chart. Diamonds: the "
    "same subsidies over Eurostat’s GDP as of 6 October 2026, which the EEA could not have had. Dashes: a lower bound, "
    "with the unconfirmed items set to zero, over Eurostat’s GDP. Malta, Poland and Slovakia lead in every version; "
    "only on the EEA’s basis is Slovakia above the 1.5% line. Sources as Table 2; 2023 values are provisional; EL = "
    "Greece.", cap)]))
S.append(KeepTogether([std_table([
    [C("Version (2023)", cellh), C("Malta", cellh), C("Poland", cellh), C("Slovakia", cellh), C("Fourth", cellh),
     C("At or above 1.5%", cellh)],
    [C("A. EEA basis: with stand-ins, database GDP"), C("<b>3.37%</b>"), C("2.09%"), C("1.51%"), C("Croatia 1.15%"),
     C("Malta, Poland, Slovakia")],
    [C("B. With stand-ins, Eurostat GDP of 6 Oct 2026"), C("3.03%"), C("2.08%"), C("1.49%"), C("Bulgaria 1.08%"),
     C("Malta, Poland")],
    [C("C. Lower bound: unconfirmed items zero, database GDP"), C("3.22%"), C("1.89%"), C("1.39%"), C("Bulgaria 1.02%"),
     C("Malta, Poland")],
    [C("D. Lower bound: unconfirmed items zero, Eurostat GDP of 6 Oct 2026"), C("2.89%"), C("1.88%"), C("1.38%"), C("Bulgaria 1.00%"),
     C("Malta, Poland")],
], [52 * mm, 17 * mm, 17 * mm, 19 * mm, 27 * mm, 38 * mm]), P(
    "Table 2. Sources: Commission subsidy database, 2024 edition [4]; Eurostat nama_10_gdp, current prices, no flags "
    "for 2023 [5]. C and D set the “to be confirmed” items to zero: a lower bound, not an equally valid version of "
    "the data. B and D use Eurostat’s GDP as of 6 October 2026, which the EEA could not have had in January 2025. "
    "The database’s GDP comes from IMF and World Bank data via Enerdata: for Malta EUR 18.8 billion, "
    "against Eurostat’s EUR 20.9 billion (11.3% higher); for Slovakia the gap is 0.9%. The stand-ins are 7.4% of the EU "
    "total (EEA: “about 7%”); Slovakia’s are EUR 146 million. All values in <i>data/cc-113/checks.csv</i> and "
    "<i>shares_2023_variants.csv</i>.", cap)]))
S.append(KeepTogether([fig(FIG / "fig2_measures.png"), P(
    "Figure 2. Malta’s support by four measures, each over its own GDP (the inventory over the database’s GDP; over "
    "Eurostat’s the 2023 point would be 3.03%). Inventory line: the EEA’s Malta chart [7]; hollow 2024 point: the "
    "Commission’s 2026 report, read from its chart [8]. Other hollow markers are expected, projected or estimated "
    "values: Government 2023–25 (budget plans, other basic commodities included [10, 11]), IMF 2025 (projection "
    "[12]), IMF price-gap 2023–25 (estimated in August 2023 [13]).",
    cap)]))
S.append(KeepTogether([std_table([
    [C("Malta’s fossil-fuel subsidies in the database", cellh), C("2022", cellh), C("2023", cellh),
     C("Type", cellh)],
    [C("Energy Support Measures (compensation to Enemalta; crisis measure)"), C("246.6"), C("<b>580.0</b>"),
     C("Natural gas; price support")],
    [C("Gas Stabilisation Fund (crisis measure)"), C("17.2"), C("15.0"), C("Natural gas; price support")],
    [C("Cut in excise duty on petrol and diesel (crisis measure)"), C("28.2"), C("to be confirmed (28.2 used)"),
     C("Oil; tax expenditure")],
    [C("Excise exemptions: inland navigation, fishing, domestic flights"), C("9.5"), C("8.5"), C("Oil; tax expenditure")],
    [C("Melita TransGas pipeline (Malta–Sicily)"), C("1.4"), C("1.2"), C("Natural gas; grant")],
    [C("<b>Total</b> (with the stand-in)"), C("<b>302.8</b>"), C("<b>604.7</b> (632.9)"), C("")],
], [80 * mm, 20 * mm, 38 * mm, 32 * mm]), P(
    "Table 3. EUR million in 2023 prices [4]. The Enemalta line, the Gas Stabilisation Fund and the pipeline grant are "
    "flagged “Actual costs” in the database, the excise lines are estimates, and only the petrol-and-diesel excise cut "
    "is to be confirmed. In 2023, 96% of the total was the one line, and 98% was flagged as created "
    "for the price crisis. Before the crisis Malta’s fossil-fuel subsidies were EUR 10–15 million a year, 0.08–0.10% "
    "of GDP, 24th to 27th of 27 in 2015–2020; in 2021 the share was already 1.33%, first in the EU; in 2022, 1.71%, "
    "second to Croatia.", cap)]))

# ================================================================== 5
S.append(CondPageBreak(75 * mm))
S.append(SectionHeading(5, "Where the evidence points different ways"))
S.append(contested(
    "Q1  Is Slovakia “at or above 1.5%”?", "YES ON THE EEA’S DATA; BORDERLINE", LG,
    "On the EEA’s basis Slovakia is 1.507% of GDP, printed 1.51% [3, 4]; the Commission’s own chart of 28 January "
    "2025 reads about 1.51% [19]. The sentence describes the data the EEA used, and on those data it is right.",
    "With Eurostat’s GDP as of 6 October 2026, which the EEA could not have had, Slovakia is 1.494%; with the "
    "EUR 146 million of 2022 stand-ins set to zero (a lower bound) it is 1.39% [4, 5]. Malta and Poland clear 1.5% in "
    "every version.",
    "<b>For this claim:</b> the threshold depends on which GDP series is used and on provisional items. It is a "
    "minor caveat on a parenthesis; the Commission’s final 2023 figures would settle it.",
    label_a="EVIDENCE FOR THE CLAIM", label_b="EVIDENCE AGAINST"))
S.append(contested(
    "Q2  How large was Malta’s support in 2023?", "UNRESOLVED; THE RANK HOLDS", ORANGE,
    "The database records EUR 580 million for the Enemalta compensation in 2023, all of it crisis-related and flagged "
    "“Actual costs” [4]. That line alone is 3.09% of GDP; with the other items the total is 3.37% (3.03% with "
    "Eurostat’s GDP). In the Commission’s 2026 report Malta is again first, for 2024, at about 1.8% of GDP, with 80% "
    "of its energy subsidies on fossil fuels [8].",
    "For 2023 the Government expected energy support of 1.7% of GDP, other basic commodities included (about EUR 356 "
    "million with Eurostat’s GDP) [10], and the IMF gives 1.4% (about EUR 293 million) [12]. But in 2022 the database "
    "was the lower: 1.71% of GDP, the Enemalta line EUR 246.6 million, against the Government’s 2.5% (about EUR 451 "
    "million) and the IMF’s 1.8% (about EUR 325 million). Over 2022–23 the line (EUR 826.5 million) is close to the "
    "Government’s expected cost (about EUR 806 million). For 2024 the gap persists: about 1.8% against the "
    "Government’s 0.87% [8, 11]. Eurostat’s all-purpose subsidies fell from EUR 824 million (2022) to EUR 660 million "
    "(2023) [15].",
    "<b>For this claim:</b> the 2023 gap may be one of timing or accounting basis rather than size, since the two-year "
    "total is close to the Government’s; we could not establish which, and the 2024 gap is unexplained. Even at the "
    "IMF’s 1.4% Malta would rank third with the other countries on the EEA’s basis, and at the Government’s 1.7% "
    "second, so the claim that Malta is among the three highest holds; whether Malta’s share is more than twice the 1.5% line or just under it "
    "depends on which figure is right.",
    label_a="EVIDENCE FOR THE DATABASE’S SIZE", label_b="EVIDENCE FOR A DIFFERENT SIZE"))
S.append(contested(
    "Q3  Does Malta’s support count as a fossil-fuel subsidy?", "YES, UNDER THE EU METHOD", GREEN,
    "The EU’s reporting method, codified under the Governance Regulation, counts income and price supports such as "
    "consumer price guarantees; the database classes the Enemalta compensation as natural-gas price support, and the "
    "Commission’s own reports use the same data [4, 8, 9]. The EEA states this definition on its page [1].",
    "The IMF’s price-gap database records no explicit subsidy for Malta, and the OECD/IISD tracker carries no OECD or "
    "IEA estimate for Malta [13, 14]. On the IMF’s wider measure, which adds unpriced environmental costs, Malta is 15th of 27 [13].",
    "<b>For this claim:</b> the EEA uses the EU’s official reporting definition and says so. A reader should know "
    "that other respected measures rank Malta very differently. The database also books the Enemalta line wholly to "
    "natural gas, not pro-rated by the power mix as for other electricity support, although 21.7% of Malta’s 2023 "
    "electricity supply was imported [4, 20]; leaving out that share alone, Malta would still be first (2.70%).",
    label_a="EVIDENCE FOR THE CLAIM", label_b="EVIDENCE AGAINST"))

# ================================================================== 6
S.append(CondPageBreak(60 * mm))
S.append(SectionHeading(6, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> In 2023 the highest shares of GDP were in Malta, Poland and Slovakia"),
     C("Rebuilt from the Commission database: Malta 3.37%, Poland 2.09%, Slovakia 1.51%, then Croatia 1.15% [3, 4]; "
       "the Commission’s own chart of 28 Jan 2025 shows the same [19]. The same three lead with Eurostat’s GDP and, "
       "as a lower bound, with the unconfirmed items set to zero [5]."), verd("ACCURATE", GREENC)],
    [C("<b>B.</b> “all at or above 1.5%”"),
     C("True on the EEA’s basis (Slovakia 1.507%). With Eurostat’s GDP of 6 Oct 2026 (later than the EEA could have "
       "used) Slovakia is 1.49%; with the unconfirmed items set to zero (a lower bound), 1.39%. Malta and Poland "
       "clear the line in every version [4, 5]."), verd("LARGELY ACCURATE", LG)],
    [C("<b>C.</b> Malta’s share, 3.37% of GDP, the highest (the EEA’s linked chart)"),
     C("Reproduced exactly; 3.03% with Eurostat’s GDP of 6 Oct 2026; first in the Commission’s 2024 data too [8]. "
       "96% is one EUR 580m line; the total is 2.1 times the IMF Article IV estimate of the 2023 cost and 1.7 times the "
       "Government’s, though in 2022 the database was lower than both [10, 12]."),
     verd("LARGELY ACCURATE", LG)],
    [C("<b>D.</b> Malta’s support is a fossil-fuel subsidy"),
     C("Yes under the EU reporting method, which the EEA states; the IMF’s price-gap database records none, and the "
       "OECD/IISD tracker has no OECD or IEA estimate for Malta [9, 13, 14]. The database books Malta’s main line "
       "wholly to natural gas, although 21.7% of the 2023 electricity supply was imported [4, 20]; the rank does not "
       "change."), verd("ACCURATE (OFFICIAL METHOD)", GREENC)],
], [62 * mm, 78 * mm, 30 * mm], valign="MIDDLE"))
S.append(Spacer(1, 3 * mm))
S.append(P("<b>The lowest shares.</b> The sentence that follows the claim also holds: Austria 0.07%, Denmark 0.08% and "
           "Estonia 0.12% of GDP, all below 0.2% [3]."))

# ================================================================== 7
S += [CondPageBreak(50 * mm), Spacer(1, 4 * mm), SectionHeading(7, "Verdict and requests for evidence"),
      verdict_box("Largely supported", "The ranking reproduces exactly and holds in every variant; Slovakia’s 1.5% rests "
                  "on provisional data, and Malta’s 2023 line is not reconciled with other sources. Confidence: "
                  "moderate."),
      Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) Every figure behind the EEA’s sentence reproduces from the Commission database it used. "
           "(2) Malta, Poland and Slovakia are the top three with either GDP series and with or without the provisional "
           "items (the lower bound), so the ranking is robust. (3) The claim that all three are “at or above 1.5%” holds on the EEA’s basis but "
           "Slovakia sits at the line, falling just below it with Eurostat’s GDP of 6 October 2026 (which the EEA could "
           "not have had): a minor caveat. (4) Confidence is moderate, not high: all the EU-method figures come from one "
           "database; its 2023 values are provisional for the items still to be confirmed (about 7–8% of the EU total; "
           "in Malta only the EUR 28.2 million excise cut); and Malta’s 2023 amount, booked as actual costs, is 1.7 to "
           "2.1 times what the Government and the IMF report as the cost of energy support, a gap we could not explain "
           "(in 2022 the database was lower than both, and over 2022–23 the line is close to the Government’s figure, "
           "which suggests timing or basis)."))
S.append(P("<b>What this verdict does not say.</b> It does not say Malta’s energy price policy is right or wrong, that "
           "anyone misreported anything, or that other definitions are wrong. It says the EEA’s statement matches the "
           "EU’s official data as published, with the caveats above."))
S.append(CondPageBreak(45 * mm))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "DG ENER and its contractors: the budget source and accounting basis (outturn or allocation; cash or accrual; "
    "which year) of Malta’s “Energy Support Measures” line, EUR 246.6 million in 2022 and EUR 580 million in 2023, "
    "which the database flags “Actual costs”.",
    "DG ENER: the 2025-edition database, with final 2023 values by Member State, to show whether Slovakia stays at or "
    "above 1.5% and whether Malta’s 2023 amount was revised.",
    "Malta’s Ministry for Finance: the outturn cost of energy support measures for each year from 2021, separating "
    "electricity, fuels and other commodities.",
    "EEA: which GDP series its share chart uses (the Malta country page names Eurostat, but its values match the "
    "database’s IMF and World Bank series) and an update of the method note.",
    "DG ENER: whether Malta’s Enemalta line should be pro-rated by the power mix, as other electricity support is, "
    "given that 21.7% of Malta’s 2023 electricity supply was imported. The rank does not change on our test.",
]))

# ================================================================== 8
S += [Spacer(1, 5 * mm), SectionHeading(8, "Limitations")]
for l in ["The 2023 values are provisional; the Commission’s 2025-edition database (final 2023 values) was not found. "
          "Its 2026 report raises the EU’s 2023 total from EUR 111 billion (2023 prices) to EUR 121 billion (2024 "
          "prices) [8].",
          "The Commission’s 2024 subsidy report, COM(2025) 17 (28 January 2025), was read from the EU Publications "
          "Office (EUR-Lex refused our requests) [19]. It gives the 2023 shares only as a chart (Figure 16), which we "
          "measured by pixel: Malta 3.37%, Poland 2.09%, Slovakia 1.51%, Croatia 1.15% (±0.01 points), the same as "
          "the CIRCABC file we rebuilt from, which was modified on 9 April 2025, after the report [4]. We could not read "
          "the smaller bars, which the chart’s EU-27 line and 2015 markers cross. The news item of 29 January 2025 [6] "
          "was also read.",
          "The original 29 January 2025 page could not be opened; the earliest copy we read is the EEA’s print of "
          "3 February 2025.",
          "Malta’s 2024 value in the Commission’s 2026 report is read from a chart; no table is published.",
          "The IMF Article IV figures were read in full for earlier checks (CC-018 and CC-022, 5 October 2026) and not re-opened, as "
          "imf.org refused our requests. The IMF’s price-gap data are its 2023 update, published in August 2023, so "
          "their 2023 values were estimated before the year ended.",
          "The Government’s figures are expected costs written during the year and include other basic commodities.",
          "We found no peer-reviewed study of Malta’s energy price policy. A Central Bank of Malta discussion paper "
          "(Rapa 2025) was not read (403)."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "European Environment Agency (29 Jan 2025; modified 29 Jul 2025). Fossil fuel subsidies in Europe (8th EAP "
          "headline indicator). Read 6 Oct 2026.", "https://www.eea.europa.eu/en/analysis/indicators/fossil-fuel-subsidies"),
    ("2", "European Environment Agency. Fixed copies of the indicator: browser print of 3 Feb 2025 (8th EAP monitoring "
          "publication) and the 8th EAP monitoring report 2025 indicator PDF (26 Nov 2025). Read 6 Oct 2026.",
     "https://www.eea.europa.eu/en/analysis/publications/monitoring-progress-towards-8th-eap-objectives/indicators/19-fossil-fuel-subsidies/@@download/file"),
    ("3", "European Environment Agency. Chart data: Fossil fuel subsidies as a share of GDP 2023; Fossil fuel subsidies "
          "in EU Member States, 2015 and 2023; by energy vector (data packages). Retrieved 6 Oct 2026.",
     "https://www.eea.europa.eu/en/analysis/indicators/fossil-fuel-subsidies/fossil-fuel-subsidies-as"),
    ("4", "European Commission, DG ENER, with Enerdata and Trinomics. Inventory of energy subsidies in the EU27, 2024 "
          "edition (database, 6 Sep 2024), published with COM(2025) 17. Retrieved from CIRCABC 6 Oct 2026.",
     "https://circabc.europa.eu/ui/group/8f5f9424-a7ef-4dbf-b914-1af1d12ff5d2/library/4e6f2b2c-702b-429b-bb19-7aeb48f28f58/details"),
    ("5", "Eurostat. nama_10_gdp, GDP at current prices; updated and retrieved 6 Oct 2026. doi:10.2908/NAMA_10_GDP.",
     "https://ec.europa.eu/eurostat/databrowser/view/nama_10_gdp/default/table"),
    ("6", "European Commission, DG ENER (29 Jan 2025). Energy subsidies report shows progress in 2023. Read 6 Oct 2026.",
     "https://energy.ec.europa.eu/news/energy-subsidies-report-shows-progress-2023-2025-01-29_en"),
    ("7", "European Environment Agency (29 Sep 2025). Europe’s environment 2025, Malta: fossil fuel subsidies (chart). "
          "Retrieved 6 Oct 2026.", "https://www.eea.europa.eu/en/europe-environment-2025/countries/malta/fossil-fuel-subsidies"),
    ("8", "European Commission (17 Sep 2026). Report on energy subsidies in the EU, COM(2026) 472 final; Council document "
          "ST 13343/26. Read in full 6 Oct 2026.", "https://data.consilium.europa.eu/doc/document/ST-13343-2026-INIT/en/pdf"),
    ("9", "Nill, J. (2024). Fossil Fuel Subsidies in EU Member States – Trends and Analytical Challenges. European "
          "Economy Discussion Paper 214, DG ECFIN. doi:10.2765/28177. Read in full; pp. 6–8.",
     "https://economy-finance.ec.europa.eu/document/download/0ae8556a-14a3-4ac9-840f-7f86a5c58521_en?filename=dp214_en.pdf"),
    ("10", "Government of Malta (Oct 2023). Draft Budgetary Plan 2024, section 3.1 (PDF p.34). Read 6 Oct 2026.",
     "https://economy-finance.ec.europa.eu/document/download/4edb4e16-f5c7-4443-ba70-dc3c0dc4099b_en?filename=2024_dbp_mt_en.pdf"),
    ("11", "Government of Malta (Oct 2024). Draft Budgetary Plan 2025 (PDF p.40). Read 6 Oct 2026.",
     "https://economy-finance.ec.europa.eu/document/download/8d77183d-aad8-464a-9c97-8baded7f13a8_en?filename=2025_dbp_mt_en.pdf"),
    ("12", "International Monetary Fund (Feb 2026). Malta: 2025 Article IV Consultation, Country Report 26/29, Table 2 "
           "(PDF p.33). doi:10.5089/9798229038249.002. Read in full for CC-018/CC-022, 5 Oct 2026.",
     "https://www.imf.org/-/media/files/publications/cr/2026/english/1mltea2026001-source-pdf.pdf"),
    ("13", "Black, S., Liu, A., Parry, I. and Vernon-Lin, N. (2023). IMF Fossil Fuel Subsidies Data: 2023 Update. IMF "
           "Working Paper 23/169. doi:10.5089/9798400249006.001. Abstract read; data from the IMF Climate Data "
           "dashboard, retrieved 6 Oct 2026.", "https://climatedata.imf.org/datasets/d48cfd2124954fb0900cef95f2db2724_0"),
    ("14", "OECD and IISD. Fossil Fuel Subsidy Tracker, country data, 2024 update (file of Jan 2026). Retrieved 6 Oct "
           "2026.", "https://fossilfuelsubsidytracker.org/country/"),
    ("15", "Eurostat. gov_10a_main, general government subsidies (D.3), Malta; updated 21 Jul 2026, retrieved 6 Oct "
           "2026. doi:10.2908/GOV_10A_MAIN.", "https://ec.europa.eu/eurostat/databrowser/view/gov_10a_main/default/table"),
    ("16", "European Commission (19 Jun 2024). 2024 Country Report – Malta, SWD(2024) 618 final, PDF p.3. Read 6 Oct "
           "2026.",
     "https://economy-finance.ec.europa.eu/document/download/b8357ca1-e31e-4a3a-b7e4-25ebf8d01121_en?filename=SWD_2024_618_1_EN_Malta.pdf"),
    ("17", "Rentschler, J. and Bazilian, M. (2017). Reforming fossil fuel subsidies: drivers, barriers and the state of "
           "progress. <i>Climate Policy</i> 17(7):891–914. doi:10.1080/14693062.2016.1169393. Abstract read.",
     "https://doi.org/10.1080/14693062.2016.1169393"),
    ("18", "Böhm, J. and Peterson, S. (2024). Fossil Fuel Subsidy Inventories vs. Net Carbon Prices. <i>The Energy Journal</i> "
           "45(4):59–79. doi:10.1177/01956574241277304. Abstract read.",
     "https://doi.org/10.1177/01956574241277304"),
    ("19", "European Commission (28 Jan 2025). 2024 Report on Energy subsidies in the EU, COM(2025) 17 final, Figure 16 "
           "and footnote 6. Read 6 Oct 2026 from the EU Publications Office.",
     "http://publications.europa.eu/resource/cellar/7150e5a9-dd6f-11ef-be2a-01aa75ed71a1.0017.03/DOC_1"),
    ("20", "Eurostat. nrg_cb_e, electricity supply, transformation and consumption, Malta 2023 (gross production and "
           "imports); updated 11 Sep 2026, retrieved 6 Oct 2026. doi:10.2908/NRG_CB_E.",
     "https://ec.europa.eu/eurostat/databrowser/view/nrg_cb_e/default/table"),
    ("21", "European Commission, DG ENER (published 29 Jan 2025; modified 30 Jul 2026). 9th report on the state of the "
           "energy union (page listing the energy subsidies report COM/2025/17 and the subsidy database). Read 6 Oct "
           "2026.", "https://energy.ec.europa.eu/strategy/energy-union/ninth-report-state-energy-union_en"),
    ("22", "Miżien. Data and calculations: data/cc-113/; tools/cc-113-report/calc.py.", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand (none is used "
                "for a figure in this report).")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "6 Oct 2026", "First issue. No right of reply needed for a Largely supported verdict.")])

build_report(Report(
    number="113", out=str(FIG / "report.pdf"), kicker="EU data and energy subsidies",
    title_lines=["Malta among the EU’s", "highest fossil-fuel", "subsidies relative to GDP?"],
    subtitle_lines=["Testing an EEA ranking against the Commission’s subsidy", "database, Eurostat GDP and other measures"],
    quote_lines=["“In 2023, fossil fuel subsidies represented the highest", "shares of gross domestic product (GDP) in",
                 "Malta, Poland, and Slovakia (all at or above 1.5%).”"],
    quote_size=13.5, title_size=33,
    attribution="European Environment Agency, Fossil fuel subsidies in Europe (indicator), published 29 Jan 2025.",
    context="Wording unchanged in every copy we read, 3 Feb 2025 to 6 Oct 2026; data from the European Commission.",
    verdict="Largely supported", verdict_note="Ranking reproduced; Slovakia sits at the 1.5% line",
    footer_lines=["Version 1.0  ·  6 October 2026", "Status:",
                  "Prepared from public sources and EEA, Commission, Eurostat and IMF data.",
                  "Repository: github.com/leandergrech/Mizien"],
    running_head="Fossil-fuel subsidies: Malta and the EU", version="1.0", date="6 October 2026",
    pdf_title="Malta among the EU's highest fossil-fuel subsidies relative to GDP? Claim Check 113",
    pdf_subject="Tests the EEA statement that in 2023 fossil fuel subsidies were the highest shares of GDP in Malta, "
                "Poland and Slovakia, all at or above 1.5%",
    story=S))
