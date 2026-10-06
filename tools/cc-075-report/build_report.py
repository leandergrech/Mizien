"""Claim Check 075 report. Run fetch.py, calc.py and figures.py first. Output: out/report.pdf"""
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
      P("On 21 September 2024 Lovin Malta reported a Eurostat dataset on passenger cars per 1,000 inhabitants: "
        "<b>“according to the statistics Malta is ranked number seven, just between Germany and Poland respectively, "
        "with 585 cars per 1,000 inhabitants.”</b> The article says its rankings come from a graphic that runs “up to "
        "the year 2022”. We tested the figure, the rank and the article’s other numbers against Eurostat’s data.", lead)]
S.append(key_points([
    ("The figure and the rank are right, for 2022.",
     "Eurostat gives Malta 585 passenger cars per 1,000 inhabitants in 2022, seventh of the 27 Member States, between "
     "Germany (587) and Poland (584). All 27 have a 2022 value; Malta’s carries no flag [2]."),
    ("The article does not say which year.",
     "It calls the dataset “as of 2023”, but its figures are 2022’s. In the 2023 figures as now published Malta is "
     "11th (575); by 2025 it is 14th (571), below the EU-27 (584) [2]."),
    ("Fewer cars per person, but more cars.",
     "From the end of 2012 to the end of 2025 Malta’s passenger car stock rose 34.5% and its population 39.6%, so the "
     "rate fell while the number of cars rose every year [3, 4]."),
    ("The side remarks are loose.",
     "585 per 1,000 is one car for every 1.7 people, not “1 car for every 2 people”. 246 km² is about the area of "
     "Malta island alone; the country has 313 km² of land. On either area Malta has by far the most cars per km² in the EU [3, 5]."),
    ("Verdict: largely supported (high confidence).",
     "The reported figure and rank reproduce exactly from Eurostat. The caveats (no year, and two loosely worded side "
     "remarks) do not change the substance."),
]))
S += [Spacer(1, 4 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("585", GREEN, "Malta, 2022: passenger cars per 1,000 inhabitants (Eurostat, no flag)"),
             ("7th of 27", GREEN, "Malta’s rank in 2022; all 27 Member States report"),
             ("14th", ORANGE, "Malta’s rank in 2025 (571), now below the EU-27’s 584"),
             ("1,014", GREEN, "Passenger cars per km² of land in Malta, 2022: first in the EU")]),
      Spacer(1, 4 * mm),
      up_down("A copy of Eurostat’s dataset as it stood on 21 September 2024 showing 2022 as the latest year, with "
              "Malta seventh. The missing year would then be the only caveat on the central statement.",
              "Evidence that Eurostat had already published Malta’s 2023 figure (11th) before the article appeared, so "
              "that a superseded rank was reported as current; or a revision of the 2022 data that moves Malta from "
              "seventh."),
      Spacer(1, 5 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the indicator measures"),
          ("4", "What the data show"), ("5", "Population growth and car density"),
          ("6", "Where the evidence points different ways"), ("7", "Testing the claim"),
          ("8", "Verdict and requests for evidence"), ("9", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The claim is Lovin Malta’s own text, read in full on 6 October 2026 on the page and through the site’s "
           "WordPress interface (post dated 21 September 2024) [1]. Lovin Malta is a news outlet and is the speaker "
           "here; the sentences below are its words, not quotations of anyone else. The article names Eurostat as the "
           "source of the dataset and a graphic by Paula Lago via The European Correspondent as the source of the "
           "rankings. We could not find the graphic (section 9)."))
S.append(std_table([
    [C("What Lovin Malta says", cellh), C("Where", cellh), C("Access", cellh)],
    [C("“according to the statistics Malta is ranked number seven, just between Germany and Poland respectively, "
       "with 585 cars per 1,000 inhabitants”"), C("Body, paragraph 3 [1]"), C("Read in full")],
    [C("Eurostat “shared a dataset detailing the unit of cars per thousand residents in each European country as of "
       "2023”; a graphic “better illustrated these rankings up to the year 2022”"), C("Paragraphs 1–2 [1]"),
     C("Read in full; graphic not found")],
    [C("Italy the “top-ranker … at a whopping 682”; Latvia lowest “with only 409 per 1,000”"), C("Paragraph 2 [1]"),
     C("Read in full")],
    [C("“approximately 1 car for every 2 people”; “with just 246 square kilometres of land, Malta is also up there "
       "among the countries with the highest car density in Europe”"), C("Paragraph 4 [1]"), C("Read in full")],
], [104 * mm, 36 * mm, 30 * mm]))
S.append(P("The headline is “Malta Ranked Number Seven On Eurostat’s ‘Passenger Cars Per 1,000 Inhabitants’ "
           "Dataset”. The claim record’s summary (seventh in the EU, 585 per 1,000) matches the article; we rate the "
           "article’s own sentences, which add the neighbours (Germany, Poland) and give no year."))
S += [Spacer(1, 2 * mm),
      callout([P("SCOPE NOTE", tag),
               P("This check tests the statistics the article reports. It does not assess traffic, congestion, "
                 "pollution or transport policy, which the article mentions in passing, nor the readers’ comments it "
                 "summarises. Claim Check 003 covers Malta’s per-capita greenhouse gas emissions.", small)],
              bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Question.</b> Was Malta seventh in the EU with 585 passenger cars per 1,000 inhabitants, between Germany "
           "and Poland; for which year; and are the article’s other figures (Italy and Latvia, one car for every two "
           "people, 246 km², car density) right?"))
S.append(P("<b>Evidence.</b> This claim is statistical. On 6 October 2026 we downloaded through Eurostat’s API the rate "
           "itself (<i>road_eqs_carhab</i>, updated 30 July 2026) [2], the stock of passenger cars (<i>road_eqs_carmot</i>) "
           "[3], the population on 1 January (<i>demo_gind</i>) [4] and land area (<i>reg_area3</i>) [5], for every "
           "country and year, keeping Eurostat’s flags. Rank, denominator, growth and density are recomputed by "
           "<i>tools/cc-075-report/calc.py</i> from <i>data/cc-075/</i> [12]. We read Eurostat’s release of the 2022 "
           "figures (17 January 2024) [6], its two Statistics Explained articles on passenger cars and transport equipment "
           "[7, 8] and its regional releases [13]. Crossref and OpenAlex were searched for peer-reviewed work on car "
           "ownership in Malta; one comparative study was read in full [9]. Malta’s National Statistics Office (NSO) "
           "and Transport Malta refused scripted access, so their figures are second-hand (◆) [10, 11]."))
S.append(P("<b>Grades.</b> Official statistics and reviews are grade C under our scale. <b>Verdicts</b> follow the "
           "five-point scale in Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(60 * mm))
S.append(SectionHeading(3, "What the indicator measures"))
S.append(P("Eurostat’s “motorisation rate” is the number of passenger cars per 1,000 inhabitants [7]. A passenger car "
           "is a road motor vehicle designed to seat no more than nine people including the driver (category M1). "
           "Privately owned and company cars, taxis, private hire cars, shared cars and rented cars are included; light "
           "utility vehicles, buses and minibuses are not [7]."))
S.append(P("<b>How the rate is built.</b> We could not open Eurostat’s methodology page for this dataset (section 9), so "
           "we rebuilt the rate. Dividing each country’s car stock at 31 December [3] by its population on 1 January of "
           "the following year [4] reproduces Eurostat’s 2022 value for all 27 Member States, within one car per 1,000 "
           "[12]. For Malta: 317,234 cars at the end of 2022 and 542,051 people on 1 January 2023 give 585.2. Divided by "
           "the population at the start of 2022 (520,174), the same stock would give 610. The denominator therefore "
           "matters in a country whose population rose 4.2% in one year."))
S.append(P("<b>Registered or licensed?</b> Eurostat collects these figures from national authorities through a "
           "questionnaire shared with the ITF and UNECE; collection methods are “not harmonised at EU level”, and "
           "vehicle registers “may include very old vehicles without signs of life” [7, 8]. For Malta, NSO publishes the "
           "stock of <i>licensed</i> motor vehicles. Its release for the end of 2022 is reported to give 424,904 licensed "
           "vehicles, 74.7% of them passenger cars, about 317,400 ◆ [10]; Eurostat’s 317,234 lies within the rounding "
           "range (317,191–317,616). NSO’s quarterly figures also count vehicles “taken off the road” (garaged, resold "
           "or scrapped) ◆ [11]. This suggests that Malta’s Eurostat figure is the licensed stock and leaves out "
           "garaged cars; we could not read NSO’s release to confirm it."))
S.append(P("<b>Who is counted.</b> The denominator is the resident population [4]. Rented cars are in the numerator [7]; "
           "we found no readable source for how many of Malta’s licensed cars are rented cars."))

# ================================================================== 4
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(4, "What the data show"))
S.append(KeepTogether([fig(FIG / "fig2_rank2022.png"), P(
    "Figure 1. Passenger cars per 1,000 inhabitants, 2022, all 27 Member States. Malta (585) is seventh, between Germany "
    "(587, break in series) and Poland (584, imputed by Eurostat); Czechia (582) is three cars behind. The EU-27 value "
    "is 564 [2].", cap)]))
S.append(KeepTogether([
    std_table([
        [C("Indicator", cellh), C("Malta", cellh), C("Comparison", cellh), C("Source", cellh), C("Grade", cellh)],
        [C("Passenger cars per 1,000 inhabitants, 2022"), C("<b>585</b> (no flag)"), C("EU-27 564"), C("Eurostat [2]"),
         grade_tag("C")],
        [C("Rank among the EU-27, 2022"), C("<b>7th of 27</b>"), C("Germany 587 (b), Poland 584 (i)"), C("Eurostat [2]"),
         grade_tag("C")],
        [C("Rank among all 41 countries in the dataset, 2022"), C("9th"), C("Liechtenstein 773, Iceland 611 (i) higher"),
         C("Eurostat [2]"), grade_tag("C")],
        [C("Highest and lowest in the EU-27, 2022"), C("–"), C("Italy 682; Latvia 406 (b)"), C("Eurostat [2]"),
         grade_tag("C")],
        [C("Same, in Eurostat’s release of 17 Jan 2024"), C("not given"), C("Italy 684; Latvia 414; EU 560"),
         C("Eurostat [6]"), grade_tag("C")],
        [C("Rank, 2023 / 2024 / 2025"), C("11th / 13th / 14th"), C("Malta 575 / 576 / 571; EU-27 570 / 577 / 584"),
         C("Eurostat [2]"), grade_tag("C")],
        [C("Car stock at 31 Dec 2022 vs NSO licensed passenger cars"), C("317,234"), C("about 317,400 ◆"),
         C("Eurostat [3]; NSO [10]"), grade_tag("C")],
    ], [58 * mm, 28 * mm, 46 * mm, 24 * mm, 14 * mm]),
    P("Flags: b = break in time series, i = imputed by Eurostat or other receiving agencies. All values in "
      "<i>data/cc-075/checks.csv</i> [12]. In 2025, eleven countries’ values are flagged (provisional, estimated, "
      "imputed or break); Malta’s values carry no flag in any year.", cap)]))
S.append(P("Malta’s rank over time", h2))
S.append(P("Malta’s rate rose from 302 in 1990 to a peak of 616 in 2016, and has drifted down since. Its rank in the "
           "EU-27 was third in eleven years (1995, 1997, 2007–2012 and 2014–2016), seventh in 2022, and 14th in 2025, "
           "when it fell 13 cars per 1,000 below the EU-27 value (Figure 2) [2]. The EU-27 value meanwhile rose from 487 "
           "in 2010 to 584 in 2025 [2]. A 2010 comparative study of four island states described Malta’s car ownership as "
           "then “the highest in the European Union” [9]; it used a different measure and earlier data, and in "
           "Eurostat’s current series Malta was third in those years."))
S.append(KeepTogether([fig(FIG / "fig1_trend.png"), P(
    "Figure 2. Top: passenger cars per 1,000 inhabitants, Malta and EU-27, 1990–2025. Bottom: Malta’s rank among the "
    "EU-27 countries with a value each year. The shaded band marks 2022, the year the article’s figures match. No Malta "
    "value for 2003–2004 [2].", cap)]))

# ================================================================== 5
S.append(CondPageBreak(90 * mm))
S.append(SectionHeading(5, "Population growth and car density"))
S.append(P("The fall in the rate is a population effect. Malta’s passenger car stock grew every year from 2006 to 2025 "
           "[3]: by 6,618 in 2023, 6,632 in 2024 and 5,209 in 2025. Its population grew faster: from the end of 2012 to "
           "the end of 2025 the car stock rose 34.5% (249,612 to 335,693) and the population 39.6% (421,464 to 588,254) "
           "[3, 4]. In 2022 alone the stock rose 1.3% and the population 4.2%, which is why the rate dropped from 602 to "
           "585 in the year the article reports (Figure 3)."))
S.append(KeepTogether([fig(FIG / "fig3_growth.png"), P(
    "Figure 3. Malta’s passenger car stock and population, indexed to the end of 2012. The population index passes "
    "the car-stock index in 2022, the year of the article’s figures; from 2022 to 2025 the population grew 8.5% and the "
    "car stock 5.8% [3, 4].", cap)]))
S.append(P("Measured per km² of land instead of per person, Malta is far ahead of every other Member State: 1,014 "
           "passenger cars per km² in 2022 against 261 in the Netherlands, the next highest, and 1,073 in 2025 [3, 5]. "
           "The article’s 246 km² is Malta island (245 km² of land in Eurostat’s data); the whole country, including "
           "Gozo and Comino, has 313 km² [5]. Using Malta island alone with the national car stock would give 1,295 cars "
           "per km², an overstatement, but the article did not compute a density, and its sentence (Malta “up there "
           "among the countries with the highest car density”) holds on either area."))
S.append(KeepTogether([fig(FIG / "fig4_density.png"), P(
    "Figure 4. Passenger cars per km² of land, 2022, the ten highest of the EU-27 [3, 5].", cap)]))

# ================================================================== 6
S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(6, "Where the evidence points different ways"))
S.append(contested(
    "Q1  Was “seventh” the current picture when the article appeared?", "TRUE FOR 2022; LATER DATA DIFFER", AMBER,
    "2022 is the year of the graphic the article used and of Eurostat’s own release of 17 January 2024 [6]. Eurostat’s "
    "regional releases came on 6 May 2024 (for 2022) and 21 May 2025 (for 2023) [13]. The article’s Italy figure (682) "
    "matches the 2022 data.",
    "The article gives no year for the 585 and describes the dataset as “as of 2023”. In the 2023 figures as now "
    "published Malta is 11th (575); by 2025 it is 14th, below the EU-27 [2]. A reader in September 2024 could take "
    "seventh as the current position.",
    "<b>For this claim:</b> we could not establish whether any 2023 values were in Eurostat’s dataset on 21 September "
    "2024 (section 9). On the evidence we have, the article reported a correct 2022 figure without saying it was "
    "2022. That is a caveat, not an error in the figure."))
S.append(contested(
    "Q2  Are the national figures comparable enough to rank?", "RANK HOLDS; MARGINS ARE SMALL", AMBER,
    "Eurostat publishes the rates side by side and ranks them in its own releases [6, 7]. Malta’s values carry no flag, "
    "and its car stock matches NSO’s licensed passenger cars ◆ [3, 10].",
    "Collection methods are “not harmonised at EU level” and registers may hold cars with no “signs of life” [7]. If "
    "Malta counts only licensed cars while some countries’ registers hold inactive ones, Malta’s rate is understated "
    "relative to theirs; we cannot measure by how much. Germany’s 2022 value has a break in series and Poland’s is "
    "imputed [2].",
    "<b>For this claim:</b> the article reports Eurostat’s published ranking accurately. Places 6 to 9 are within five "
    "cars per 1,000 (Germany 587, Malta 585, Poland 584, Czechia 582), so the exact position is less robust than the "
    "broad picture of Malta among the EU’s higher rates in 2022."))

# ================================================================== 7
S.append(CondPageBreak(95 * mm))
S.append(SectionHeading(7, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> Malta has 585 cars per 1,000 inhabitants"),
     C("Eurostat 2022: 585, no flag; reproduced from 317,234 cars and 542,051 people on 1 Jan 2023 [2–4]."),
     verd("ACCURATE (2022)", GREENC)],
    [C("<b>B.</b> Ranked number seven, between Germany and Poland"),
     C("Seventh of 27, all reporting; Germany 587 (break in series), Poland 584 (imputed) [2]. An EU ranking: among "
       "all 41 countries in the dataset Malta is ninth."),
     verd("ACCURATE (2022)", GREENC)],
    [C("<b>C.</b> The year: a dataset “as of 2023”, a graphic “up to the year 2022”"),
     C("The figures are 2022’s; the article never says so. In the 2023 figures as now published Malta is 11th (575) "
       "[2]; whether they were out by 21 Sep 2024 could not be established."),
     verd("YEAR NOT STATED", AMBER)],
    [C("<b>D.</b> Italy top at 682, Latvia lowest at 409"),
     C("Italy 682 and Latvia lowest match [2]. Latvia is 406 (break in series) now and was 414 in Eurostat’s January "
       "2024 release [6]."),
     verd("LARGELY ACCURATE", LG)],
    [C("<b>E.</b> “Approximately 1 car for every 2 people”"),
     C("585 per 1,000 is one car for every 1.71 people [2]; the rounding understates the rate."),
     verd("LOOSELY WORDED", LG)],
    [C("<b>F.</b> 246 km² of land; among the highest car density in Europe"),
     C("246 km² is Malta island; the country has 313 km² of land [5]. With 1,014 cars per km² of land Malta is first in "
       "the EU, 3.9 times the Netherlands [3, 5]."),
     verd("LARGELY ACCURATE", LG)],
], [55 * mm, 85 * mm, 30 * mm], valign="MIDDLE"))
S.append(Spacer(1, 3 * mm))
S.append(P("<b>The central statement (A, B)</b> reproduces exactly from Eurostat’s current data for 2022, the year of "
           "the graphic the article used. <b>The year (C)</b> is the main caveat: “as of 2023” describes the dataset, "
           "while the figures are 2022’s, and the article never ties the 585 to a year. <b>The side remarks (D–F)</b> "
           "are right in direction: Latvia’s figure differs by data vintage; “1 car for every 2 people” understates "
           "Malta’s rate; and 246 km² is the main island, though Malta leads the EU on car density on either area."))

# ================================================================== 8
S += [CondPageBreak(80 * mm), Spacer(1, 6 * mm), SectionHeading(8, "Verdict and requests for evidence"),
      verdict_box("Largely supported", "The figure and the rank reproduce exactly from Eurostat for 2022; the article "
                  "gives no year and two side remarks are loose. Confidence: high."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) Malta’s 585 passenger cars per 1,000 inhabitants and its seventh place among the 27 Member "
           "States, between Germany and Poland, match Eurostat’s data for 2022, in which all 27 report and Malta’s "
           "value carries no flag. (2) The article does not say the figures are for 2022 and calls the dataset “as of "
           "2023”; in the 2023 figures as now published Malta is 11th. (3) Its Italy and Latvia figures, its “1 car "
           "for every 2 people” and its 246 km² are approximately right, and its car-density sentence is accurate. "
           "These caveats do not change the substance. (4) Confidence is high because the rate rebuilds from Eurostat’s "
           "stock and population data for all 27 countries, and Eurostat’s own release gives the same picture for 2022."))
S.append(P("<b>What this verdict does not say.</b> It does not say Malta is seventh today (it was 14th in 2025), that "
           "Malta has more cars than before (the stock has grown every year), or anything about congestion, pollution or "
           "transport policy. It assesses only whether Lovin Malta reported Eurostat’s figures accurately."))
S.append(KeepTogether([P("Evidence we are asking for", h2), requests_list([
    "From Lovin Malta: the graphic it used (Paula Lago, The European Correspondent) and the date of the data in it.",
    "From Eurostat: the date on which 2023 values were first published in <i>road_eqs_carhab</i>, and its methodology "
    "note on how national stocks are counted.",
    "From NSO or Transport Malta: the stock of licensed passenger cars by year, the number of rented cars in it, and "
    "the number of registered but unlicensed (garaged) cars.",
])]))
S.append(P("<b>Right of reply.</b> Not needed: under the project’s rule a reply is sought only for Not substantiated, "
           "Misleading or Contradicted verdicts."))

# ================================================================== 9
S += [Spacer(1, 6 * mm), CondPageBreak(60 * mm), SectionHeading(9, "Limitations")]
for l in ["Eurostat serves only its current data. We could not see the dataset as it stood on 21 September 2024: the "
          "Internet Archive lists a February 2024 copy of Eurostat’s passenger-car article, but web.archive.org reset "
          "every connection from our network. Several 2022 values have been revised since January 2024 (Cyprus 658 to "
          "633, Luxembourg 678 to 673) [2, 6].",
          "The graphic the article used (Paula Lago, The European Correspondent) was not found; the Instagram post "
          "embedded in the article needs a login.",
          "Eurostat’s methodology (ESMS) page for road equipment returned “not found” at every address we tried; the "
          "denominator was established by recomputation instead.",
          "NSO and Transport Malta refused scripted access. The licensed-vehicle figures [10, 11] are second-hand (◆); "
          "Newsbook’s passenger-car counts are internally inconsistent and are not used.",
          "We found no readable count of rented cars in Malta’s licensed stock, so their effect on a per-resident rate "
          "is not quantified.",
          "Warren and Enoch [9] is a comparative study with data from the 2000s and a different measure; it is "
          "context only."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Darmanin J. (21 Sep 2024). Malta Ranked Number Seven On Eurostat’s ‘Passenger Cars Per 1,000 Inhabitants’ "
          "Dataset. Lovin Malta. (Read in full, 6 Oct 2026.)",
     "https://lovinmalta.com/malta/malta-ranked-number-seven-on-eurostats-passenger-cars-per-1000-inhabitants-dataset/"),
    ("2", "Eurostat. road_eqs_carhab Passenger cars – per thousand inhabitants; updated 30 Jul 2026, retrieved 6 Oct "
          "2026, with flags. doi:10.2908/ROAD_EQS_CARHAB.",
     "https://ec.europa.eu/eurostat/databrowser/view/road_eqs_carhab/default/table?lang=en"),
    ("3", "Eurostat. road_eqs_carmot Passenger cars, by type of motor energy and size of engine (total); updated 1 Sep "
          "2026, retrieved 6 Oct 2026, with flags. doi:10.2908/ROAD_EQS_CARMOT.",
     "https://ec.europa.eu/eurostat/databrowser/view/road_eqs_carmot/default/table?lang=en"),
    ("4", "Eurostat. demo_gind Population change – demographic balance and crude rates at national level (population "
          "on 1 January); updated 30 Sep 2026, retrieved 6 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/demo_gind/default/table?lang=en"),
    ("5", "Eurostat. reg_area3 Area by NUTS 3 region (land area); updated 22 Jan 2026, retrieved 6 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/reg_area3/default/table?lang=en"),
    ("6", "Eurostat (17 Jan 2024). Passenger cars per 1 000 inhabitants reached 560 in 2022. Eurostat news. Read 6 Oct "
          "2026.", "https://ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-20240117-1"),
    ("7", "Eurostat. Passenger cars in the EU. Statistics Explained; data extracted July 2026. Read 6 Oct 2026 (PDF).",
     "https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Passenger_cars_in_the_EU"),
    ("8", "Eurostat. Transport equipment statistics. Statistics Explained; data extracted December 2025. Read 6 Oct "
          "2026 (PDF).", "https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Transport_equipment_statistics"),
    ("9", "Warren J.P., Enoch M.P. (2010). Island transport, car ownership and use: a focus on practices in Cuba, Malta, "
          "Mauritius and Singapore. <i>Island Studies Journal</i> 5(2):193–216. doi:10.24043/isj.244. (Full text read.)",
     "https://doi.org/10.24043/isj.244"),
    ("10", "◆ National Statistics Office Malta (15 Feb 2023). Motor Vehicles: Q4/2022, News Release 023/2023. Not "
           "read (403); figures from a search summary.", "https://nso.gov.mt/wp-content/uploads/News2023_023.pdf"),
    ("11", "◆ Balzan J. (30 Jul 2025). Over 450,000 licensed vehicles on Malta’s roads, NSO confirms. Newsbook (a "
           "report of NSO’s Q2/2025 release). Read 6 Oct 2026.",
     "https://newsbook.com.mt/en/over-450000-licensed-vehicles-on-maltas-roads-nso-confirms/"),
    ("12", "Miżien. Data and calculations: data/cc-075/; tools/cc-075-report/calc.py.", ""),
    ("13", "Eurostat (6 May 2024; 21 May 2025). Passenger cars per inhabitant remain stable in 2022; Passenger cars per "
           "inhabitant stable in 2023. Eurostat news (regional data). Read 6 Oct 2026.",
     "https://ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-20250521-1"),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "6 Oct 2026", "First issue. No right of reply needed for a Largely supported verdict.")])

build_report(Report(
    number="075", out=str(FIG / "report.pdf"), kicker="Statistics and EU data",
    title_lines=["Is Malta seventh", "in the EU for", "cars per person?"],
    subtitle_lines=["Testing a media report of Eurostat’s passenger-car", "figures against the data"],
    quote_lines=["“according to the statistics Malta is ranked number", "seven, just between Germany and Poland",
                 "respectively, with 585 cars per 1,000 inhabitants.”"],
    quote_size=14,
    attribution="Lovin Malta (J. Darmanin), 21 September 2024.",
    context="The outlet’s own text, citing Eurostat; no year given for the figure.",
    verdict="Largely supported", verdict_note="Right for 2022; the year is not stated",
    footer_lines=["Version 1.0  ·  6 October 2026", "Status:",
                  "Prepared from public sources and Eurostat data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Passenger cars per person: Malta and the EU", version="1.0", date="6 October 2026",
    pdf_title="Is Malta seventh in the EU for cars per person? Claim Check 075",
    pdf_subject="Tests Lovin Malta's report that Malta ranks seventh in the EU with 585 passenger cars per 1,000 inhabitants",
    story=S))
