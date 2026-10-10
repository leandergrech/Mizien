"""Claim Check 095 report. Run fetch.py, calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []
LG = colors.HexColor("#8DB36B")
NYD = PLEDGE_COLS[1]          # "Not yet due" in the site's pledge palette
ON_HOLD = "right of reply on hold until the Pre-Budget Document 2027 is read"

# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("Launching the Pre-Budget Document 2027 on 30 September 2026, Finance Minister Clyde Caruana said that energy "
        "subsidies would cost about EUR 400 million this year (EUR 391.7 million in the figures he presented) and that "
        "<b>“I expect those numbers to remain at the same level next year”</b>; that <b>“in our country, the prices of fuel, "
        "electricity and gas have not changed”</b>; and that “what there is in the energy sector, come what may, will "
        "remain” [1, 2]. We tested the prices, the cost and the comparison with other countries.", lead)]
S.append(key_points([
    ("The prices have not changed.",
     "Petrol EUR 1.34 and diesel EUR 1.21 a litre in every weekly EU Oil Bulletin since 15 June 2020; electricity "
     "unchanged since 2014. In the year to August 2026 energy prices rose 13.0% in the EU and 0.0% in Malta [8, 9]."),
    ("The EUR 400 million is an estimate, not spending.",
     "No 2026 spending figure for energy subsidies has been published. Official forecasts rose, but no independent source gives the "
     "amount, and the Pre-Budget Document that holds it could not be read [14, 15, 17]."),
    ("Past figures fit; past forecasts missed.",
     "The minister’s EUR 242.5 million for 2023 fits Eurostat and the IMF [11, 20], but EUR 595 million had been planned "
     "for that year in October 2022 [13]."),
    ("“The only country” holds for prices, not for support.",
     "No other EU country kept energy prices flat, but several subsidise as much relative to GDP [8, 11]."),
    ("Verdict: not substantiated (moderate); pledge: not yet due.",
     "The price statement is accurate; the central figure, about EUR 400 million in 2026 and 2027, cannot yet be "
     "tested. Keeping prices fixed in 2027 is a commitment."),
]))
S += [Spacer(1, 1 * mm), VerdictMeter(2), Spacer(1, 2 * mm),
      tiles([("0.0%", GREEN, "Malta’s energy prices, year to Aug 2026 (EU-27 +13.0%)"),
             ("EUR 1.21", GREEN, "Diesel a litre in Malta every week since 15 Jun 2020; EU average 2.15"),
             ("391.7m", ORANGE, "EUR: the minister’s 2026 figure (energy and food), an estimate with no outturn yet"),
             ("41%", ORANGE, "Government’s 2023 figure (242.5m) as a share of the 595m planned in Oct 2022")]),
      Spacer(1, 3 * mm),
      up_down("The Pre-Budget Document’s breakdown of the EUR 391.7 million by measure, with its price assumptions; "
              "or 2026 spending data (the Financial Estimates 2027 or the National Statistics Office) close to that "
              "figure.",
              "2026 spending data well away from EUR 391.7 million, or a breakdown showing that most of it is not "
              "energy price support. Evidence that retail energy prices changed in 2026 would also count against."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "How the prices are held"),
          ("4", "What the data show"), ("5", "Where the evidence points different ways"), ("6", "Testing the claim"),
          ("7", "Verdict, pledge and requests for evidence"), ("8", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("Our record came from a news headline, “Malta Spends EUR 400 Million to Keep Energy Bills Low Through 2027” "
           "(The Malta Post, 2 October 2026, not 2025 as first recorded) [6]. That article quotes no one. The words are the "
           "Finance Minister’s, at the launch of the Pre-Budget Document 2027 in Rabat on 30 September 2026, reported the "
           "same day by five outlets [1–5]. He spoke partly in Maltese; the English quotations are the outlets’ "
           "renderings. We rate only words inside quotation marks; figures in the reporters’ own text are labelled so."))
S.append(std_table([
    [C("What was said", cellh), C("Where (30 Sep 2026)", cellh), C("Form", cellh)],
    [C("“The numbers already clearly show that they are higher than when Russia invaded the Ukraine, and I expect those "
       "numbers to remain at the same level next year. If things worsen ... that bill will continue to rise”"),
     C("BusinessNow [1]"), C("Quotation")],
    [C("Energy and fuel subsidies “for this year are expected to cost Government EUR 400 million”; next year “the cost "
       "to remain the same”; EUR 500 million next year with energy infrastructure"),
     C("BusinessNow [1]; TVM [3]"), C("Reporters’ text")],
    [C("Figures “presented by the minister”: energy and food subsidies EUR 242.5m (2023), 188.1m (2025), 391.7m (2026), "
       "about 400m (2027); EUR 75m for energy infrastructure; EUR 1.35bn over five years"),
     C("Lovin Malta [2]; also TVM, Italpress/MNA [3, 5]"), C("Reporters’ text")],
    [C("“In just a few months, energy prices have risen very significantly. However, in our country, the prices of fuel, "
       "electricity and gas have not changed”"), C("Lovin Malta [2]"), C("Quotation")],
    [C("“Malta is the only country that has continued to protect families and businesses from these substantial "
       "burdens”; “No other European country is doing what we are doing.”"), C("Lovin Malta [2]; TVM [3]"),
     C("Quotation")],
    [C("“what there is in the energy sector, come what may, will remain”; “What we are doing right now, we will "
       "sustain” (Maltese: “Dak li qed nagħmlu bħalissa se nsostnuh”)"), C("BusinessNow [1]; Newsbook [4]"),
     C("Quotation")],
    [C("The Pre-Budget Document 2027, <i>Bis-Saħħa Tiegħek</i> (150 pages), which carries the figures"),
     C("Ministry for Finance [7]"), C("<b>Not read</b> (403)")],
], [100 * mm, 40 * mm, 30 * mm]))
S.append(P("<b>What we rate.</b> “Through 2027” is the headline’s phrase; the minister spoke of this year and next. We "
           "therefore test: the price statement; the cost this year (EUR 391.7 million, presented as an expected figure); the "
           "past figures in the same series; and “the only country”. The 2027 cost is the minister’s forecast, which he made "
           "conditional on prices, and keeping the support in 2027 is a commitment: we label it as a pledge."))
S += [Spacer(1, 2 * mm),
      callout([P("SCOPE AND FAIRNESS", tag),
               P("This check does not test the minister’s estimates of what removing the subsidies would do (a fall in GDP of "
                 "about EUR 630 million over three years, 3,000 jobs), nor whether the policy is right. Both main parties "
                 "promised stable energy prices or tariffs at the May 2026 election: Labour to keep “the policy of price "
                 "stability” in the coming years [26], the Nationalist Party that electricity and water tariffs would not rise "
                 "[27]. The Green Party (ADPD) and the economist Marisa Xuereb argued on 30 September and 1 October for targeted "
                 "rather than blanket support [29]. We assess the statements, not the people who made them.", small)],
              bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Questions.</b> Have Malta’s fuel, electricity and gas prices stayed unchanged while prices elsewhere rose? "
           "Is about EUR 400 million a credible cost for 2026, and do the minister’s earlier figures agree with independent "
           "data? Is Malta the only EU country to shield its consumers?"))
S.append(P("<b>Evidence.</b> On 10 October 2026 we downloaded Eurostat’s harmonised consumer prices (HICP, monthly to "
           "August 2026, September flash for energy) for every EU country [8], the Commission’s Weekly Oil Bulletin from 2019 "
           "to 5 October 2026 [9], Eurostat’s half-yearly electricity prices for households and businesses [10], its "
           "government spending by function (COFOG 04.3, “fuel and energy”, 2015–2024) [11] and GDP [12]. We read the Malta "
           "Fiscal Advisory Council’s assessments of the Government’s forecasts [13–16, 22] and the Commission’s spring 2026 "
           "forecast [17, 18], and reused, without copying, the draft budgetary plans, IMF and Commission subsidy figures "
           "gathered for CC-113 [19–21]. <i>tools/cc-095-report/calc.py</i> recomputes every number from "
           "<i>data/cc-095/</i> into <i>checks.csv</i>. Crossref was searched for peer-reviewed work; none on Malta’s "
           "policy was found (search log in <i>literature/CC-095/notes.md</i>)."))
S.append(P("<b>Grades.</b> Official statistics, fiscal-council assessments and forecasts are grade C; one peer-reviewed "
           "panel study with a comparison group is grade B. <b>Verdicts</b> and <b>pledge labels</b> follow Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(70 * mm))
S.append(SectionHeading(3, "How the prices are held"))
S.append(P("Malta’s retail prices for electricity, fuel and LPG are set by the Government, not by the market. When the cost "
           "of supply rises above the fixed price, the state pays the difference: the Commission’s subsidy database describes "
           "Malta’s largest measure as energy prices “frozen to their pre-COVID levels as the Governement [sic] is compensating "
           "Enemalta for the losses” [21]. The cost therefore depends on international oil, gas and electricity prices, which "
           "is why the minister tied next year’s bill to the Strait of Hormuz, diesel exports and the winter [1]. In 2022 the "
           "Government’s own model put the price rises avoided at 130.2% for electricity, 47.9% for diesel, 33.6% for petrol "
           "and 55.3% for gas [22]."))
S.append(KeepTogether([std_table([
    [C("Study", cellh), C("Design", cellh), C("Finding relevant here", cellh), C("Grade", cellh)],
    [C("Rapa (2025), Central Bank of Malta paper on SSRN [23]"), C("Structural model of Malta’s economy; not "
       "peer-reviewed; abstract read"),
     C("Fixed prices supported activity, cut inflation and protected low-income households in 2022–23, and raised the "
       "debt ratio by about 4 points of GDP by 2024; abrupt removal would be contractionary, gradual tapering less so."),
     grade_tag("C")],
    [C("Tutar &amp; Erden (2026), <i>Int. J. Sociology and Social Policy</i> [24]"),
     C("EU-27 panel, 2015–2024, difference-in-differences; abstract read"),
     C("Effects imprecise on average; targeted cash transfers gave more lasting gains against energy poverty, and better "
       "value, than universal price subsidies."), grade_tag("B")],
    [C("Arze del Granado, Coady &amp; Gillingham (2012), <i>World Development</i> [25]"),
     C("Review of fuel-subsidy studies in developing countries; abstract read"),
     C("Untargeted fuel subsidies leak to richer households: the top fifth receives six times what the bottom fifth "
       "receives."), grade_tag("C")],
    [C("European Commission, spring 2026 forecast [18]"), C("Review of 2026 measures across the EU"),
     C("New 2026 measures cost EUR 14.5 billion; three-quarters untargeted; price measures blunt the incentive to cut "
       "demand."), grade_tag("C")],
], [44 * mm, 38 * mm, 76 * mm, 12 * mm]), P(
    "Table 1. What the literature says about price subsidies. None tests the size of Malta’s subsidy; they explain why "
    "its cost moves with world prices and why its design is debated.", cap)]))

# ================================================================== 4
S.append(CondPageBreak(90 * mm))
S.append(SectionHeading(4, "What the data show"))
S.append(P("Prices", h2))
S.append(KeepTogether([fig(FIG / "fig1_prices.png"), P(
    "Figure 1. (a) Energy in the harmonised index of consumer prices, Malta and the EU-27, January 2019 to August 2026 "
    "(Malta to September, flash estimate) [8]. Malta’s index fell when fuel prices were cut in June 2020 and has been flat "
    "since. (b) Diesel pump prices with taxes, weekly, 2019 to 5 October 2026: Malta, Italy and the EU weighted average [9].",
    cap)]))
S.append(KeepTogether([std_table([
    [C("Measure", cellh), C("Malta", cellh), C("EU", cellh), C("Source", cellh)],
    [C("Electricity index (HICP): unchanged since"), C("Apr 2014"), C("+2.3% in year to Aug 2026"), C("[8]")],
    [C("Gas (LPG in Malta), diesel, petrol (HICP): unchanged since"), C("Apr 2020; Jul 2020; Jul 2020"),
     C("gas +7.2%, diesel +31.2%, petrol +20.5% since Dec 2025"), C("[8]")],
    [C("All energy (HICP), Jan 2020 to Aug 2026"), C("−3.5%"), C("+55.4%"), C("[8]")],
    [C("Petrol and diesel at the pump, 5 Oct 2026 (EUR per litre)"), C("1.34 and 1.21 (cheapest of 26)"),
     C("2.01 and 2.15 (weighted average)"), C("[9]")],
    [C("Diesel before taxes, 5 Oct 2026 (EUR per litre)"), C("0.553"), C("1.324 (Italy 1.241)"), C("[9]")],
    [C("Household electricity, 2,500–4,999 kWh, all taxes (EUR per kWh)"), C("0.126–0.132, 2019 to 2026-S1"),
     C("0.290 (2025-S2)"), C("[10]")],
    [C("Business electricity, 500–1,999 MWh, excluding VAT (EUR per kWh)"), C("0.134–0.141, 2019 to 2026-S1"),
     C("0.184 (2025-S2); peak 0.215 (2023-S1)"), C("[10]")],
], [66 * mm, 40 * mm, 49 * mm, 15 * mm]), P(
    "Table 2. Malta’s energy prices against the EU. 2026-S1 electricity prices are provisional. Malta’s price before taxes "
    "is 41.8% of the EU average: the gap is what the state covers. The minister compared Malta with one Sicilian pump "
    "(EUR 2.34 for diesel, quoted by Newsbook [4]); the Oil Bulletin’s Italian average was EUR 2.35 on 28 September.",
    cap)]))
S.append(KeepTogether([fig(FIG / "fig2_energy_inflation.png"), P(
    "Figure 2. Annual change in energy prices (HICP), August 2026, every EU country [8]. Malta 0.0%; the next lowest are "
    "Hungary (1.6%) and Czechia (2.2%). For diesel alone Malta is 0.0% and the next lowest Hungary 11.1%.", cap)]))
S.append(CondPageBreak(95 * mm))
S.append(P("What it costs", h2))
S.append(KeepTogether([fig(FIG / "fig3_costs.png"), P(
    "Figure 3. Malta’s energy support by source, EUR million. Bars: Eurostat’s general-government subsidies for fuel and "
    "energy (COFOG 04.3), which include a pre-crisis base of EUR 31–46 million a year in 2015–2019 [11]. Circles: the minister’s "
    "figures (energy and food), as reported [2]. Triangles: the IMF’s shares of GDP in euros [20]. Square and diamond: "
    "the October 2022 plan for 2023 [13] and the Commission database’s 2023 entry used in CC-113 [21].", cap)]))
S.append(KeepTogether([std_table([
    [C("Year", cellh), C("Minister (energy and food) [2]", cellh), C("Eurostat COFOG 04.3 subsidies [11]", cellh),
     C("Other official estimates", cellh)],
    [C("2023"), C("<b>242.5</b> (1.16% of GDP)"), C("295.9; 258.5 above 2019"),
     C("IMF 292.8 [20]; Government (Oct 2023, expected, other commodities included) 355.5 [19]; planned Oct 2022: 595 "
       "[13]; Commission database 604.7 [21]")],
    [C("2025"), C("<b>188.1</b> (0.76% of GDP)"), C("not yet published"),
     C("Government plan (Oct 2024) 177.6 [19]; IMF projection 197.3 [20]")],
    [C("2026"), C("<b>391.7</b> (projection)"), C("not yet published"),
     C("All subsidies: 493.3 forecast in Oct 2025, 560.0 in Apr 2026, with energy about 0.3% of GDP (78.3) higher [14, "
       "15]; first quarter 119.0 [16]")],
    [C("2027"), C("<b>about 400</b> (forecast)"), C("–"), C("Commission: subsidies to fall as a share of GDP [17]")],
    [C("2022–26"), C("<b>1,350</b> in five years"), C("2022 + 2024: 630.3 (555.5 above the 2019 level)"),
     C("The minister’s total implies 527.7 for 2022 and 2024 together")],
], [16 * mm, 38 * mm, 42 * mm, 74 * mm]), P(
    "Table 3. EUR million. Shares of GDP converted with Eurostat GDP [12]. The minister’s series includes food subsidies "
    "(Lovin Malta’s report [2]; BusinessNow says “energy and fuel” [1]); COFOG 04.3 has no food. ◆ A news report of the "
    "2025 Budget gives 2023 as EUR 580 million allocated and “just over EUR 227 million” spent [28].", cap)]))

# ================================================================== 5
S.append(CondPageBreak(80 * mm))
S.append(SectionHeading(5, "Where the evidence points different ways"))
S.append(contested(
    "Q1  Is about EUR 400 million the right size for 2026?", "PLAUSIBLE, NOT YET SHOWN", ORANGE,
    "The Government’s forecasts rose through the year: in October 2025 it expected subsidies to fall in 2026 on lower oil "
    "prices; in April 2026 it added energy subsidies worth about 0.3% of GDP [14, 15]. The Commission expects spending to "
    "rise in 2026 “as a result of the higher cost of energy subsidies” [17]. In the EU, diesel before taxes cost 2.4 times "
    "Malta’s regulated pre-tax price on 5 October [9]. The minister’s past figures agree with Eurostat and the IMF.",
    "No 2026 spending figure for energy subsidies exists yet (only all subsidies, first quarter: EUR 119.0 million "
    "[16]), and no independent source gives an amount. The September figure is EUR 125 "
    "million above the April energy uplift (indicative: the bases differ) [15]. Forecasts of this spending have missed "
    "widely: EUR 595 million was planned for 2023 in October 2022 and EUR 262 million in spring 2023 [13]; the Government "
    "now gives EUR 242.5 million [2]. The figure also includes food subsidies.",
    "<b>For this claim:</b> the direction is supported; the amount rests on the Ministry’s own projection, whose "
    "breakdown is in a document we could not read. It can be tested when 2026 spending is published.",
    label_a="EVIDENCE FOR THE FIGURE", label_b="EVIDENCE THAT IT IS NOT YET SHOWN"))
S.append(contested(
    "Q2  Is Malta “the only country” still shielding consumers?", "TRUE FOR PRICES, NOT FOR SUPPORT", LG,
    "In the year to August 2026 Malta is the only EU country whose energy prices did not rise at all (Figure 2); its "
    "diesel and petrol are the cheapest of 26 countries reporting to the Oil Bulletin [8, 9]. The Commission notes the "
    "measures “keep retail energy prices unchanged” [17].",
    "Other governments subsidise too: in 2024 Hungary spent 1.3% of GDP on fuel and energy subsidies and Bulgaria and "
    "Slovakia 1.1%, the same as Malta (EU-27 0.4%) [11]. EU countries adopted EUR 14.5 billion of new measures in spring "
    "2026 [18]; Hungary’s energy prices rose only 1.6%.",
    "<b>For this claim:</b> as a statement about keeping prices completely fixed, it holds on the data; as a statement "
    "that no other country protects families and businesses, it is too strong.",
    label_a="EVIDENCE FOR THE CLAIM", label_b="EVIDENCE AGAINST"))
S.append(contested(
    "Q3  Will about EUR 400 million hold in 2027?", "A FORECAST; NOT RATED", GREY,
    "The minister expects costs “to remain at the same level next year” and EUR 75 million of energy investment on top "
    "[1, 2]. The policy has been kept since 2020 and both main parties promised stable prices [26, 27].",
    "The minister himself said that if things worsen “that bill will continue to rise” [1]. The Commission expects "
    "subsidies to fall as a share of GDP in 2027 [17]. The cost depends on world prices that no one can forecast with "
    "confidence, and past forecasts have missed by more than half [13].",
    "<b>For this claim:</b> the 2027 amount is a conditional forecast and is not rated. Whether prices stay fixed in "
    "2027 is labelled as a pledge (Section 7).",
    label_a="WHAT POINTS TO ABOUT EUR 400 MILLION", label_b="WHAT COULD CHANGE IT"))

# ================================================================== 6
S.append(CondPageBreak(60 * mm))
S.append(SectionHeading(6, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> “in our country, the prices of fuel, electricity and gas have not changed”"),
     C("Pump prices fixed since 15 Jun 2020 (325 weekly reports); electricity index unchanged since Apr 2014, LPG since Apr "
       "2020; energy 0.0% in the year to Aug 2026 against EU +13.0% [8, 9, 10]."), verd("ACCURATE", GREENC)],
    [C("<b>B.</b> Energy subsidies of about EUR 400 million this year (EUR 391.7 million presented)"),
     C("A projection for a year not yet over; no energy-subsidy spending figure yet. Official forecasts rose during 2026 and the Commission "
       "expects a higher cost, but no independent source gives the amount; it includes food; the Pre-Budget Document "
       "was not read [14, 15, 17]."), verd("PLAUSIBLE, NOT SHOWN", AMBER)],
    [C("<b>C.</b> Past figures: EUR 242.5m (2023), 188.1m (2025), 1,350m over five years"),
     C("2023 close to Eurostat’s crisis rise (258.5) and the IMF (292.8); 2025 between the Government’s plan (177.6) "
       "and the IMF (197.3); the five-year total fits Eurostat’s 2022 and 2024 [11, 19, 20]."),
     verd("CONSISTENT", GREENC)],
    [C("<b>D.</b> “I expect those numbers to remain at the same level next year”"),
     C("A forecast the minister made conditional on prices; past forecasts of this spending missed widely [1, 13]."),
     verd("NOT RATED (FORECAST)", GREY)],
    [C("<b>E.</b> “Malta is the only country that has continued to protect families and businesses ...”"),
     C("Only EU country with no rise in energy prices (Hungary +1.6%); cheapest fuel of 26. But Hungary, Bulgaria and "
       "Slovakia spent as much or more on fuel and energy subsidies relative to GDP in 2024 [8, 9, 11]."),
     verd("LARGELY ACCURATE", LG)],
    [C("<b>F.</b> “what there is in the energy sector, come what may, will remain” (in 2027)"),
     C("A commitment for 2027; prices are measurable; the year has not begun [1, 4]."),
     verd("NOT YET DUE (PLEDGE)", NYD)],
], [56 * mm, 84 * mm, 30 * mm], valign="MIDDLE"))

# ================================================================== 7
S += [CondPageBreak(60 * mm), Spacer(1, 4 * mm), SectionHeading(7, "Verdict, pledge and requests for evidence"),
      verdict_box("Not substantiated", "Prices held, as stated; the central figure, about EUR 400 million a year, is an "
                  "estimate and a forecast that cannot yet be tested. Confidence: moderate."),
      Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) The statement that fuel, electricity and gas prices have not changed is accurate on every "
           "measure we used. (2) The claim’s central figure is the cost: about EUR 400 million in 2026 and the same in "
           "2027. For 2026 it is the Ministry’s projection for a year still in progress; for 2027 a forecast the minister "
           "made conditional on world prices. Independent sources support the direction (a higher cost in 2026) but not the "
           "amount, and earlier projections of the same spending were revised by large margins. Under our scale, a central "
           "figure that cannot yet be tested is <i>Not substantiated</i>; this says the figure has not been shown, not that "
           "it is wrong. (3) “The only country” holds for fixed prices, not for support in general. (4) Confidence is "
           "moderate: the Pre-Budget Document, which may explain the figure, could not be read."))
S.append(callout([P("PLEDGE LABEL: NOT YET DUE (AS OF 10 OCT 2026)", tag),
                  P("The commitment that the support, and with it fixed retail prices for fuel, electricity and LPG, will remain "
                    "in 2027 is measurable (the Oil Bulletin and Eurostat price data) and its term has not begun. It carries "
                    "forward Labour’s 2026 manifesto promise to keep the price-stability policy [26]. Revisit when 2027 "
                    "price data are published.", small)], bg=BLUE_PALE, bar=BLUE))
S.append(P("<b>What this does not say.</b> It does not say the EUR 391.7 million is wrong or that the policy is right or "
           "wrong. A fully supported version would read: <i>“Fuel, electricity and gas prices have not changed. We estimate "
           "that energy and food subsidies will cost about EUR 390 million this year; next year depends on world prices.”</i>"))
S.append(KeepTogether([P("Evidence we are asking for", h2), requests_list([
    "Ministry for Finance: the Pre-Budget Document 2027’s breakdown of EUR 391.7 million (2026) and about EUR 400 "
    "million (2027) by measure (Enemalta compensation, fuel, LPG, cereals and feed) and the price assumptions behind them.",
    "Ministry for Finance: the yearly outturn of the same series from 2022, so that the EUR 1,350 million can be checked "
    "year by year.",
    "National Statistics Office / Eurostat: 2026 government finance data for fuel and energy subsidies when published.",
    "DG ENER: whether Malta’s 2023 entries in the subsidy database (EUR 580m and 15m) are the October 2022 allocations, "
    "which they equal, rather than spending (see CC-113).",
])]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag),
               P("Right of reply on hold until the Pre-Budget Document 2027 is read. The verdict rests partly on a document "
                 "we could not open; the maintainer will read it and decide whether to seek a reply from the Ministry for "
                 "Finance. A <i>Not substantiated</i> verdict is not circulated beyond this site before then.", small)],
              bg=AMBER_PALE, bar=AMBER)]

# ================================================================== 8
S += [Spacer(1, 5 * mm), SectionHeading(8, "Limitations")]
for l in ["The Pre-Budget Document 2027 [7], the Government’s press release and the Financial Estimates could not be read "
          "(finance.gov.mt and gov.mt refused our requests; the Wayback Machine was unreachable). The figures are as five "
          "outlets reported them; they agree with each other.",
          "The minister spoke partly in Maltese; English quotations are the outlets’ renderings, checked against the "
          "Maltese versions where TVM and Newsbook printed them.",
          "The HICP measures household prices. Business electricity prices were checked [10]; fuel bought by firms was not "
          "tested separately. Malta’s August 2026 HICP is the latest final month; September energy is a flash estimate.",
          "Eurostat’s COFOG subsidies run to 2024 and include non-crisis items; the minister’s series includes food. The "
          "comparison in Table 3 is of orders of magnitude, not a reconciliation.",
          "The IMF and draft-budgetary-plan figures were read for CC-113 and CC-022 and not re-opened. Literature was read "
          "as abstracts only.",
          "The Commission’s 2026 measures box shows Malta’s cost only in a chart, which we did not measure."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Schembri Orland, K. (30 Sep 2026). Subsidies expected to hit EUR 400 million, minister warns of ‘economic "
          "catastrophe’ if stopped. BusinessNow. Read in full 10 Oct 2026.",
     "https://businessnow.mt/subsidies-expected-to-hit-e400-million-minister-warns-of-economic-catastrophe-if-stopped/"),
    ("2", "Falzon, G. (30 Sep 2026). Malta To Spend Around EUR 400 Million On Energy Subsidies Again In 2027. Lovin "
          "Malta. Read in full 10 Oct 2026.",
     "https://lovinmalta.com/news/local/malta-to-spend-around-e400-million-on-energy-subsidies-again-in-2027/"),
    ("3", "TVM News (30 Sep 2026). Finance Minister warns that without energy subsidies, the country will face “an "
          "economic catastrophe” (and Maltese version by A. Rossitto). Read in full 10 Oct 2026.",
     "https://tvmnews.mt/en/news/finance-minister-warns-that-without-energy-subsidies-the-country-will-face-an-economic-catastrophe/"),
    ("4", "Camilleri, N. and Muscat, C. (30 Sep 2026). Caruana jgħid li s-sussidji se jkomplu, imma jispjega x’jiġri "
          "kieku jieqfu / Caruana says subsidies will continue. Newsbook. Read in full 10 Oct 2026.",
     "https://newsbook.com.mt/caruana-jghid-li-s-sussidji-se-jkomplu-imma-jispjega-xjigri-kieku-jieqfu/"),
    ("5", "Italpress / Malta News Agency (30 Sep 2026). Malta, Finance Minister warns removal of energy subsidies poses "
          "a risk. Read 10 Oct 2026.", "https://www.italpress.com/?p=753654"),
    ("6", "Camilleri, S. (2 Oct 2026). Malta Spends EUR 400 Million to Keep Energy Bills Low Through 2027. The Malta "
          "Post. Read 10 Oct 2026 (the claim record’s locator).",
     "https://themaltapost.com/posts/malta-spends-400-million-to-keep-energy-bills-low-through-2027"),
    ("7", "Ministry for Finance (30 Sep 2026). Pre-Budget Document 2027: Bis-Saħħa Tiegħek. Not read (403).",
     "https://finance.gov.mt/"),
    ("8", "Eurostat. prc_hicp_minr, HICP (ECOICOP ver.2), monthly; updated 2 Oct 2026, retrieved 10 Oct 2026. "
          "doi:10.2908/PRC_HICP_MINR.", "https://ec.europa.eu/eurostat/databrowser/view/prc_hicp_minr/default/table"),
    ("9", "European Commission, DG ENER. Weekly Oil Bulletin, price history with and without taxes, to 5 Oct 2026. "
          "Retrieved 10 Oct 2026.", "https://energy.ec.europa.eu/data-and-analysis/weekly-oil-bulletin_en"),
    ("10", "Eurostat. nrg_pc_204 (households, band DC) and nrg_pc_205 (non-households, band ID); updated 9 Oct 2026, "
           "retrieved 10 Oct 2026. doi:10.2908/NRG_PC_204.",
     "https://ec.europa.eu/eurostat/databrowser/view/nrg_pc_204/default/table"),
    ("11", "Eurostat. gov_10a_exp, government expenditure by function, COFOG 04.3 fuel and energy; updated 16 Sep 2026, "
           "retrieved 10 Oct 2026. doi:10.2908/GOV_10A_EXP.",
     "https://ec.europa.eu/eurostat/databrowser/view/gov_10a_exp/default/table"),
    ("12", "Eurostat. nama_10_gdp, GDP at current prices, Malta; retrieved 10 Oct 2026. doi:10.2908/NAMA_10_GDP.",
     "https://ec.europa.eu/eurostat/databrowser/view/nama_10_gdp/default/table"),
    ("13", "Malta Fiscal Advisory Council (2023). Assessment of the Update of Stability Programme 2023–2026, Box C: "
           "Energy subsidies – revisions across forecast rounds, Table 5.11, p. 89. Read 10 Oct 2026.",
     "https://mfac.org.mt/wp-content/uploads/2024/07/Box-C-Energy-subsidies-Revisions-across-forecast-rounds-Assessment-of-USP-2023-2026.pdf"),
    ("14", "Malta Fiscal Advisory Council (Dec 2025). Assessment of the Fiscal Forecasts within the Draft Budgetary Plan "
           "2026, pp. 8, 24–25. Read 10 Oct 2026.",
     "https://mfac.org.mt/wp-content/uploads/2025/12/Assessment-of-the-Fiscal-Forecasts-within-the-DBP26.pdf"),
    ("15", "Malta Fiscal Advisory Council (Jun 2026). Assessment of the Fiscal Forecasts within the Annual Progress "
           "Report 2026, pp. 8, 28–29. Read 10 Oct 2026.",
     "https://mfac.org.mt/wp-content/uploads/2026/06/MFAC-Assessment-of-the-Fiscal-Forecasts-within-the-Annual-Progress-Report-2026.pdf"),
    ("16", "Malta Fiscal Advisory Council (1 Sep 2026). Economic and Fiscal Developments over the First Half of 2026, "
           "Council Note 03/2026, p. 7. Read 10 Oct 2026.",
     "https://mfac.org.mt/wp-content/uploads/2026/09/Council-note_Economic-and-Fiscal-Developments-During-the-First-Half-of-2026.pdf"),
    ("17", "European Commission (21 May 2026). European Economic Forecast, Spring 2026, Institutional Paper 341, Malta, "
           "pp. 136–137. Read 10 Oct 2026.",
     "https://economy-finance.ec.europa.eu/document/download/3360898c-cd40-46c0-b170-7adfcb993add_en?filename=ip341_en.pdf"),
    ("18", "European Commission (21 May 2026). Policy measures in EU Member States to address the 2026 energy price "
           "shock (spring 2026 forecast box). Read 10 Oct 2026.",
     "https://economy-finance.ec.europa.eu/economic-forecast-and-surveys/economic-forecasts/spring-2026-economic-forecast-slowdown-growth-energy-shock-drives-inflation/policy-measures-eu-member-states-address-2026-energy-price-shock_en"),
    ("19", "Government of Malta. Draft Budgetary Plans 2024 (Oct 2023, PDF p.34) and 2025 (Oct 2024, PDF p.40). Read for "
           "CC-113, 6 Oct 2026 (data/cc-113/other_estimates_transcribed.csv).",
     "https://economy-finance.ec.europa.eu/document/download/4edb4e16-f5c7-4443-ba70-dc3c0dc4099b_en?filename=2024_dbp_mt_en.pdf"),
    ("20", "International Monetary Fund (Feb 2026). Malta: 2025 Article IV Consultation, Country Report 26/29, Table 2. "
           "doi:10.5089/9798229038249.002. Read for CC-022, 5 Oct 2026.",
     "https://www.imf.org/-/media/files/publications/cr/2026/english/1mltea2026001-source-pdf.pdf"),
    ("21", "European Commission, DG ENER, with Enerdata and Trinomics. Inventory of energy subsidies in the EU27, 2024 "
           "edition; Malta’s 2023 entries as recorded for CC-113 (data/cc-113/ec_inventory_malta_facts.csv).",
     "https://circabc.europa.eu/ui/group/8f5f9424-a7ef-4dbf-b914-1af1d12ff5d2/library/4e6f2b2c-702b-429b-bb19-7aeb48f28f58/details"),
    ("22", "Malta Fiscal Advisory Council (2022). Assessment of the Draft Budgetary Plan 2023, Box A: Energy and "
           "food-related support measures. Read 10 Oct 2026.",
     "https://mfac.org.mt/wp-content/uploads/2024/07/Box-A-Energy-and-Food-related-support-measures-Assessment-of-DBP-2023.pdf"),
    ("23", "Rapa, N. (2025). Energy Subsidies in Malta: Estimating the Effects of Current Policies and Hypothetical Exit "
           "Strategies. SSRN. doi:10.2139/ssrn.5353671. Not peer-reviewed; abstract read.",
     "https://doi.org/10.2139/ssrn.5353671"),
    ("24", "Tutar, H. and Erden, C. (2026). Targeted cash transfers vs universal price subsidies: policy persistence and "
           "cost-effectiveness in EU energy poverty (2015–2024). <i>International Journal of Sociology and Social "
           "Policy</i>, 1–22. doi:10.1108/IJSSP-01-2026-0043. Abstract read.",
     "https://doi.org/10.1108/IJSSP-01-2026-0043"),
    ("25", "Arze del Granado, F. J., Coady, D. and Gillingham, R. (2012). The Unequal Benefits of Fuel Subsidies: A "
           "Review of Evidence for Developing Countries. <i>World Development</i> 40(11):2234–2248. "
           "doi:10.1016/j.worlddev.2012.05.005. Abstract read.", "https://doi.org/10.1016/j.worlddev.2012.05.005"),
    ("26", "Partit Laburista (2026). Int Malta: Manifest Elettorali 2026, chapter 16, item 11, PDF p. 187. Read 10 Oct "
           "2026.", "https://partitlaburista.org/wp-content/uploads/2026/08/Manifest_Elettorali_INT_MALTA_2026.pdf"),
    ("27", "Partit Nazzjonalista (2026). Nifs Ġdid, chapter Enerġija u Ilma, pledge 1, as summarised in Miżien’s "
           "manifesto list (data/manifesto_pledges.csv, MP-PN-2026-ENI-01).", "https://pn.org.mt/nifsgdid/energija-u-ilma/kontijiet-orhos-u-tariffi-gusti/"),
    ("28", "◆ Cachia, A. (1 Nov 2024). Energy subsidies for 2025 are set to cost half the amount set aside for 2024. "
           "BusinessNow (reporting the 2025 Budget; budget documents not opened).",
     "https://businessnow.mt/energy-subsidies-for-2025-are-set-to-cost-half-the-amount-set-aside-for-2024/"),
    ("29", "Newsbook (30 Sep and 1 Oct 2026). Green Party calls for targeted energy subsidies instead of blanket support; "
           "Sussidji: “Il-Ministru tal-Finanzi qed jipprova jbeżża’ bil-babaw” – Marisa Xuereb. Read 10 Oct 2026.",
     "https://newsbook.com.mt/en/green-party-calls-for-targeted-energy-subsidies-instead-of-blanket-support/"),
    ("30", "Miżien. Data and calculations: data/cc-095/; tools/cc-095-report/calc.py (checks.csv).", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or official "
                "statistics · D assertion or anecdote. ◆ marks a source known only second-hand (used for context only, "
                "never for a deciding figure).", pledges=True)
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "10 Oct 2026", "First issue. Verdict Not substantiated (moderate); pledge label Not yet due. "
                    "Right of reply on hold until the Pre-Budget Document 2027 is read.")])

build_report(Report(
    number="095", out=str(FIG / "report.pdf"), kicker="Energy subsidies and prices",
    title_lines=["EUR 400 million a year", "to keep energy", "prices fixed?"],
    subtitle_lines=["Testing the Finance Minister’s pre-budget figures against", "Eurostat, the Oil Bulletin and the "
                    "Government’s own forecasts"],
    quote_lines=["“I expect those numbers to remain at the same", "level next year.”  “… in our country, the prices",
                 "of fuel, electricity and gas have not changed.”"],
    quote_size=13.5, title_size=34,
    attribution="Clyde Caruana, Minister for Finance, launching the Pre-Budget Document 2027, 30 Sep 2026.",
    context="Quoted by BusinessNow and Lovin Malta; the cost this year was given as about EUR 400 million (391.7m).",
    verdict="Not substantiated", verdict_note="Prices held; the EUR 400m is an estimate not yet testable",
    footer_lines=["Version 1.0  ·  10 October 2026", "Status:",
                  "Prepared from public sources, Eurostat and Commission data and MFAC reports.",
                  "Pledge label: not yet due (as of 10 Oct 2026).  Repository: github.com/leandergrech/Mizien"],
    running_head="Energy subsidies and fixed prices", version="1.0", date="10 October 2026",
    pdf_title="EUR 400 million a year to keep energy prices fixed? Claim Check 095",
    pdf_subject="Tests the Finance Minister's statements of 30 Sep 2026 on the cost of energy subsidies and unchanged "
                "fuel, electricity and gas prices",
    status_note=ON_HOLD, pledge_label="Not yet due",
    story=S))
