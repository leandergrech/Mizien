"""Claim Check 071 report. Run calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []

# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("On 26 February 2026 The Shift News (Ivan Camilleri) headlined an article “‘Free’ public transport reaches €100 million a year in "
        "subsidies as traffic gridlock worsens”. Its first sentence says that Malta’s “‘free’ public transport system cost taxpayers almost "
        "€100 million in 2025, according to figures tabled in Parliament” [1]. The speaker is the newspaper, so its article is the wording we "
        "test. We checked the money, the congestion claim and the link the article draws between them.", lead)]
S.append(key_points([(a, b.replace("◆", DIAM)) for a, b in [
    ("The headline rounds up its own figures.",
     "The article gives three 2025 payments: €59 million, €31.2 million and €3.2 million [1]. They sum to €93.4 million, 6.6% under €100 "
     "million, and €3.2 million of it is for buying buses. The body says “almost”; the headline says “reaches”."),
    ("We could not read the parliamentary reply behind the money.",
     "The figures come from replies by the Transport Minister to the PN’s Chris Said. Newsbook reports the same document in Maltese [2 ◆]. "
     "The reply itself, the Financial Estimates and the operator’s accounts were not available to us, so every euro figure is second-hand ◆."),
    ("Congestion is up a little; the evidence for “gridlock” is thin.",
     "TomTom’s index puts the Valletta area’s congestion level at 50.3% in 2025, 1.1 points above 2024, with mean speed down 0.5 km/h [5]. "
     "Eurostat counts 1.6% more passenger cars in 2025 and 5.8% more than in 2022, but cars per 1,000 residents fell from 610 to 585 [3, 4]."),
    ("The article’s link between the two is not tested.",
     "Nothing in the data we could read shows what congestion would have been without free buses. The comparison is a juxtaposition, not a finding."),
]]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(2), Spacer(1, 3 * mm),
      tiles([("3", GREY, "payments in the article (€59m, €31.2m, €3.2m) add to less than its €100 million headline ◆".replace("◆", DIAM)),
             ("+1.1 pt", ORANGE, "Valletta-area congestion level, 2025 against 2024 (TomTom)"),
             ("+5.8%", ORANGE, "More passenger cars, 2022 to 2025 (Eurostat); population grew 10.4%"),
             ("0", ORANGE, "Parliamentary replies, budget estimates or operator accounts we could read")]),
      Spacer(1, 4 * mm),
      up_down("A move up to Largely supported would need the parliamentary reply (or the Financial Estimates or the operator’s accounts) "
              "confirming a 2025 total close to €100 million, and a congestion series of more than two years that rises.",
              "A reply showing a total well under €93 million, or a longer congestion series that is flat or falling, would lower it. "
              "A source showing the figure includes items outside the scheme would also count."),
      Spacer(1, 3 * mm)]
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The claim record summarised the article as “‘free’ public transport now costs about EUR 100 million a year in subsidies while "
           "traffic gridlock worsens”. We rate the article’s own words. Quoted words below are the Shift’s, as printed; the Shift’s account "
           "of the Minister’s replies is the Shift’s paraphrase and is not in quotation marks."))
S.append(std_table([
    [C("Source", cellh), C("What it says", cellh), C("Our access", cellh), C("Status", cellh)],
    [C("<b>The Shift News</b>, Ivan Camilleri, 26 Feb 2026 [1]"),
     C("“‘Free’ public transport reaches €100 million a year in subsidies as traffic gridlock worsens” (headline). Body: the system “cost taxpayers "
       "almost €100 million in 2025, according to figures tabled in Parliament”; components €59 million (PSO concession), €31.2 million (Tallinja "
       "card) and €3.2 million (new buses); €84 million in 2024; “traffic congestion continues to worsen”."),
     C("Read in full, 10 Oct 2026."), C("<b>The claim</b> (quoted words)")],
    [C("<b>Newsbook</b>, Christine Mamo, 27 Feb 2026 (Maltese) [2]"),
     C("Reports the same document and the same figures (“kważi €100 miljun”, “almost €100 million”); adds that on average 35 vehicles a day are added to the roads."),
     C("Read in full."), C("Outlet report ◆".replace("◆", DIAM))],
    [C("<b>Business Now</b>, 18 Apr 2024 [6]; <b>The Shift</b>, 10 Feb 2024 [7]"),
     C("Payments to Malta Public Transport: €36.3 million (2021), €42.8 million (2022), €69.4 million (2023, from information tabled in Parliament); "
       "Budget 2024 allocation €49 million (PSO) + €25 million (free-ride scheme)."),
     C("Read in full."), C("Outlet reports ◆".replace("◆", DIAM))],
    [C("<b>Eurostat</b> road_eqs_carmot, demo_gind [3, 4]"),
     C("Passenger cars at 31 December and population on 1 January for Malta, 2019–2025."),
     C("Downloaded 10 Oct 2026 (data/cc-071/)."), C("<b>Primary</b> (official statistics)")],
    [C("<b>TomTom Traffic Index</b>, Valletta [5]"),
     C("Annual congestion level and mean speed for the Valletta metro area, 2025 and the previous year."),
     C("Page data read 10 Oct 2026."), C("<b>Primary</b> (commercial dataset)")],
], [40 * mm, 72 * mm, 32 * mm, 26 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("WHAT WE COULD NOT READ", tag),
               P("The Minister’s replies to the Parliamentary Questions (parlament.mt returns 403 to scripts), the Financial Estimates 2026 and Budget "
                 "Speech 2026 (finance.gov.mt returns 403), Transport Malta’s pages (403) and Malta Public Transport’s accounts. The Wayback Machine "
                 "reset our connections. Routes tried are in <i>literature/CC-071/README.md</i>.", small)],
              bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Questions.</b> (A) Is the 2025 figure close to €100 million? (B) Has the payment risen year on year since free travel began? "
           "(C) Is traffic congestion worsening? (D) Have car numbers and car use gone on increasing? (E) Does the data show that the spending has "
           "failed to ease congestion, as the article’s framing implies?"))
S.append(P("<b>Evidence.</b> For A and B we added the components the Shift reports and compared them with the earlier payments reported by Business Now and the "
           "Shift (<i>calc.py</i>; <i>data/cc-071/checks.csv</i>, <i>subsidy_series.csv</i>). For C we read TomTom’s annual congestion level for the "
           "Valletta metro area. For D we took Eurostat’s count of passenger cars and the population on 1 January, and computed cars per 1,000 residents "
           "with both on the same year (Eurostat’s own rate uses the next 1 January; ours is like for like across years)."))
S.append(P("<b>Limits.</b> The euro figures rest on outlet reports of a document we did not read. TomTom’s index measures one metropolitan area, in two years "
           "that we could read, and is a commercial product; its “congestion level” is the extra travel time against free-flow conditions. Eurostat counts "
           "the stock of cars, not how much they are driven."))
S.append(P("<b>Grades.</b> Eurostat counts are grade C (official statistics); TomTom is grade C (a documented commercial dataset, not audited); outlet reports "
           "of tabled figures are grade D. <b>Verdicts</b> follow Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(3, "What the evidence shows"))
S.append(P("<b>The money.</b> The article’s three 2025 payments sum to €93.4 million (59.0 + 31.2 + 3.2). Operating payments alone, the concession fee and the "
           "Tallinja card, come to €90.2 million; the €3.2 million for buses is investment. The sum is 6.6% under €100 million and 11.2% above the €84 million "
           "the article gives for 2024 (<i>calc.py</i>). The earlier payments reported by Business Now were €36.3 million (2021), €42.8 million (2022) and "
           "€69.4 million (2023). If those series are on the same basis, payments have risen every year, and the 2025 sum is 34.6% above 2023. They may not be on "
           "the same basis: the 2023 figure is described as payments to the operator, the 2025 total as subsidies. The Shift’s “highest annual subsidy yet” "
           f"is consistent with these numbers {DIAM}."))
S.append(fig(FIG / "fig1_payments.png", width=CW * 0.98))
S.append(P(f"Figure 1. Payments for public transport, as reported {DIAM}. 2021–2023: payments to Malta Public Transport (Business Now [6]); 2024 and 2025: the "
           "Shift [1]; 2025 is the sum of three components. Sources: <i>data/cc-071/subsidy_series.csv</i>.", cap))
S.append(P("<b>Congestion.</b> TomTom’s index for the Valletta metro area gives an annual average congestion level of 50.3% in 2025 against 49.2% in 2024, a "
           "rise of 1.1 percentage points, with mean speed of 27.6 km/h against 28.1 km/h [5]. That is a small, one-year rise in a single area. We read only "
           "those two years on TomTom’s page, so we cannot say whether it extends a longer trend. The article itself gives no congestion figure; its basis is "
           "“transport experts” and the rise in car numbers."))
S.append(P("<b>Cars.</b> Eurostat counts 335,693 passenger cars at the end of 2025, 1.6% more than a year earlier and 5.8% more than at the end of 2022, the year free "
           "travel began [3]. Over 2019–2022 the stock grew 3.3% in three years. Population grew faster, by 10.4% from 1 January 2022 to 1 January 2025 [4], "
           "so cars per 1,000 residents fell from 610 to 585 on our like-for-like ratio. More cars on the roads, yes; more cars per person, no. "
           "Eurostat does not measure vehicle-kilometres, so “private car use” is not something we could test."))
S.append(CondPageBreak(75 * mm))
S.append(fig(FIG / "fig2_cars.png", width=CW * 0.98))
S.append(P("Figure 2. Passenger cars and population in Malta, index 2019 = 100. Sources: Eurostat road_eqs_carmot (stock at 31 December) and demo_gind (1 January) "
           "[3, 4]; <i>data/cc-071/cars_population.csv</i>.", cap))
S.append(callout([P("WHAT THIS DOES AND DOES NOT SHOW", tag),
                  P("It shows that the article’s figures add up to about €93 million, not €100 million, that car numbers and one congestion index have edged up, and "
                    "that population has grown faster than cars. It does not show what congestion would have been without free buses, whether the money is "
                    "well spent, or the reply the figures come from.", small)],
                 bg=BLUE_PALE, bar=BLUE))

# ================================================================== 4
S.append(Spacer(1, 4 * mm))
S.append(SectionHeading(4, "Where the evidence points different ways"))
S.append(contested("Has free travel failed to ease congestion?", "NOT SETTLED", AMBER,
                   "The article says that “vehicle imports and private car use have continued to increase” and that experts saw “no measurable reduction in "
                   "congestion” [1]. In our data the car stock is up 5.8% since 2022 and TomTom’s congestion level is up 1.1 points in 2025 [3, 5].",
                   f"Business Now reports bus passengers rose from 49.6 million in 2022 to 67.3 million in 2023, from a Transport Malta release we did not read "
                   f"{DIAM} [6]. Population grew 10.4% since 2022 and cars per 1,000 residents fell [3, 4]. More people using buses and fewer cars per person are "
                   "compatible with congestion that is still rising, because the population is larger.",
                   "Without a counterfactual (congestion in a comparable country or period without free buses) the data cannot say whether congestion would have been "
                   "worse. We did not rate that inference; we rated the facts stated.",
                   label_a="THE ARTICLE’S FRAMING", label_b="WHAT ELSE THE DATA SHOW"))

# ================================================================== 5
S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(5, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> The system cost “almost €100 million in 2025” (headline: “reaches €100 million a year”)"),
     C("The Shift [1]"),
     C(f"The article’s own components sum to €93.4 million, 6.6% under €100 million; €3.2 million is bus investment. The parliamentary reply was not read; "
       f"Newsbook reports the same document {DIAM} [2].", cell),
     verd("UNVERIFIED", AMBER)],
    [C("<b>B.</b> Payments are the highest yet and still rising"),
     C("The Shift [1]"),
     C(f"€36.3m, €42.8m, €69.4m, €84m, €93.4m for 2021–2025 as reported {DIAM} [1, 6]; bases may differ. Consistent with the article; not verified at source.", cell),
     verd("CONSISTENT", AMBER)],
    [C("<b>C.</b> “Traffic congestion continues to worsen”"),
     C("The Shift [1]"),
     C("TomTom Valletta-area congestion level 49.2% to 50.3% (+1.1 points), speed down 0.5 km/h; two years only, one area [5].", cell),
     verd("PARTLY SUPPORTED", AMBER)],
    [C("<b>D.</b> “Vehicle imports and private car use have continued to increase”"),
     C("The Shift [1]"),
     C("Passenger cars +1.6% in 2025, +5.8% since 2022 [3]; but cars per 1,000 residents fell 610 to 585 [3, 4]. Imports and car use not measured by us.", cell),
     verd("NEEDS CONTEXT", AMBER)],
    [C("<b>E.</b> The spending has brought “no measurable reduction in congestion” (the article’s framing)"),
     C("The Shift’s experts [1]"),
     C("No counterfactual and no congestion series that straddles October 2022 in the sources we could read. Not tested.", cell),
     verd("NOT TESTED", GREY)],
], [42 * mm, 24 * mm, 70 * mm, 34 * mm], valign="MIDDLE"))

# ================================================================== 6
S += [Spacer(1, 6 * mm), SectionHeading(6, "Verdict and requests for evidence"),
      verdict_box("Not substantiated", "The figure is close to €93 million on the article’s own numbers, not €100 million, and we could not read the reply behind "
                  "it; congestion is only slightly up and the link to free travel is not tested. Confidence: low."),
      Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) The headline figure is stronger than the components under it, and the body’s “almost” is the more defensible wording. (2) Every euro "
           "figure rests on outlet reports of tabled replies, which we could not check at source. (3) Cars and one congestion index have edged up, but "
           "population grew faster, and the data in hand contain no counterfactual for the implied failure of the scheme. The rating applies to the claim as "
           "worded, which joins a spending figure to a trend in a single headline. It says nothing about the journalists’ motives, and the direction of the "
           "payments, upward each year, is consistent with every source we read. Confidence is low because the central figure is second-hand."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "From the Ministry (or Parliament): the text of the replies to Chris Said’s questions on payments to Malta Public Transport for 2024 and 2025, itemised.",
    "From the Ministry for Finance: the 2025 outturn and 2026 estimate for the public service obligation and free-travel lines.",
    "From Malta Public Transport or Transport Malta: payments received by year, with passenger numbers, on one consistent basis.",
    "From Transport Malta: vehicle-kilometre or traffic-count series for 2019–2025 on the main corridors.",
]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag),
               P("The verdict is Not substantiated, so a right of reply applies (maintainer rule of 5 October 2026). It is pending; the maintainer sends it. "
                 "Nothing has been sent to anyone.", small)],
              bg=BLUE_PALE, bar=BLUE)]

# ================================================================== 7
S += [Spacer(1, 6 * mm), SectionHeading(7, "Limitations")]
for l in ["The 2025 and 2024 payments, and the 2021–2023 series, are known only through the Shift, Newsbook and Business Now ◆. We did not read any "
          "parliamentary reply, budget document or account.".replace("◆", DIAM),
          "The series in Figure 1 may mix bases (payments to the operator against subsidies as the Shift defines them). We did not verify what the Minister’s "
          "reply counts as a subsidy.",
          "TomTom’s index is for the Valletta metro area, not for Malta as a whole; we read its 2025 and previous-year values only. Sources conflict on earlier "
          "years in search summaries, which we do not use.",
          "Eurostat’s car count is a stock at 31 December; it does not measure how far cars are driven, so “car use” is untested. The 2025 values are the latest "
          "Eurostat release (6 Oct 2026) and may be revised.",
          "The Shift says there were 542,000 valid Tallinja cards “by the end of 2024” in 2026, and its 10 Feb 2024 article gave the same number for the end of the "
          "year before. We did not rate this.",
          "Newsbook’s figure of 35 vehicles a day (all vehicle types) was not tested; our passenger-car figure is 14 a day net in 2025.",
          "We rate the Shift’s wording. We did not rate its statements that few Maltese nationals are believed to use the buses or that experts questioned value for money."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Camilleri I. (26 Feb 2026). ‘Free’ public transport reaches €100 million a year in subsidies as traffic gridlock worsens. The Shift News.",
     "https://theshiftnews.com/2026/02/26/free-public-transport-reaches-e100-million-a-year-in-subsidies-as-traffic-gridlock-worsens/"),
    ("2", "Mamo C. (27 Feb 2026). Nefqa ta’ €100 miljun fis-sena għal trasport pubbliku b’xejn. Newsbook ◆ (outlet’s report of the parliamentary reply).",
     "https://newsbook.com.mt/nefqa-ta-e100-miljun-fis-sena-ghal-trasport-pubbliku-bxejn/"),
    ("3", "Eurostat. Passenger cars, by type of motor energy and size of engine (road_eqs_carmot), Malta, total. Retrieved 10 Oct 2026.",
     "https://doi.org/10.2908/ROAD_EQS_CARMOT"),
    ("4", "Eurostat. Population change – demographic balance and crude rates at national level (demo_gind), Malta, population on 1 January. Retrieved 10 Oct 2026.",
     "https://doi.org/10.2908/DEMO_GIND"),
    ("5", "TomTom. Traffic Index: Valletta traffic report, annual congestion level and mean speed, Valletta metro area. Read 10 Oct 2026.",
     "https://www.tomtom.com/traffic-index/city/valletta/"),
    ("6", "Fenech R. (18 Apr 2024). Government shells out close to €70 million to national bus operator Malta Public Transport in 2023. Business Now ◆.",
     "https://businessnow.mt/government-shells-out-close-to-e70-million-to-national-bus-operator-malta-public-transport-in-2023/"),
    ("7", "The Shift Team (10 Feb 2024). Tal-linja costing taxpayers €250 each in subsidies. The Shift News.",
     "https://theshiftnews.com/2024/02/10/tal-linja-costing-taxpayers-e250-each-in-subsidies/"),
    ("8", "Miżien. Calculation script and outputs: tools/cc-071-report/calc.py; data/cc-071/checks.csv, subsidy_series.csv, cars_population.csv, tomtom_valletta.csv.", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance, statute text or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "10 Oct 2026", "First issue. Verdict Not substantiated (low confidence); pending right of reply.")])

build_report(Report(
    number="071", out=str(FIG / "report.pdf"), kicker="Transport",
    title_lines=["‘Free’ buses:", "€100 million", "a year?"],
    subtitle_lines=["Testing The Shift’s figure for public-transport", "subsidies and its claim that gridlock is worsening"],
    quote_lines=["“‘Free’ public transport reaches €100 million a year", "in subsidies as traffic gridlock worsens”"],
    quote_size=13,
    attribution="The Shift News (Ivan Camilleri), 26 February 2026, headline.",
    context="Body text: the system “cost taxpayers almost €100 million in 2025, according to figures tabled in Parliament”.",
    verdict="Not substantiated", verdict_note="Reply not read; link to congestion untested",
    footer_lines=["Version 1.0  ·  10 October 2026", "Status:",
                  "Prepared from public sources.", "Repository: github.com/leandergrech/Mizien"],
    running_head="‘Free’ buses – €100 million a year", version="1.0", date="10 October 2026",
    pdf_title="‘Free’ buses: €100 million a year? Claim Check 071",
    pdf_subject="Tests The Shift's statement that free public transport costs almost EUR 100 million a year while congestion worsens",
    story=S))
