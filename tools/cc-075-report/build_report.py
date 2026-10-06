"""Claim Check 075 report. Run fetch.py, fetch_vintage.py, read_charts.py, calc.py and figures.py first.
Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []
LG = colors.HexColor("#8DB36B")
REPLY = "pending right of reply (Lovin Malta)"   # maintainer session, 6 Oct 2026: name the body in the status

# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("On 21 September 2024 Lovin Malta wrote that Eurostat had “shared a dataset … as of 2023” on passenger cars per "
        "1,000 inhabitants, and that <b>“according to the statistics Malta is ranked number seven, just between Germany "
        "and Poland respectively, with 585 cars per 1,000 inhabitants.”</b> We tested the figure and the rank against "
        "Eurostat’s data, and against what Eurostat had published by the date of the article.", lead)]
S.append(key_points([
    ("The figure is right for 2022, in revised data.",
     "Eurostat’s current data give Malta 585 in 2022, seventh of 27, between Germany (587) and Poland (584) [2]. "
     "Eurostat’s own release of January 2024 had Malta’s 2022 value at about 602, sixth [6, 14]; it was revised later."),
    ("Eurostat’s newer figures put Malta 12th.",
     "By 25 July 2024, about two months before the article, Eurostat had published 2023 figures for all 27 Member "
     "States: Malta about 575, 12th; EU 571. That version of Eurostat’s article was online on the day the article "
     "appeared [13]."),
    ("The article presents the old rank as current.",
     "It calls Eurostat’s dataset “as of 2023” and says Malta “is ranked number seven”, while dating its graphic “up "
     "to the year 2022”. It never says the 585 is a 2022 figure, and does not mention the 2023 figures."),
    ("Lower since.",
     "In today’s revised data Malta is 11th for 2023 and 14th for 2025 (571, below the EU-27’s 584) [2]: its "
     "population has grown faster than its car stock [3, 4]. Side remarks: 585 per 1,000 is one car per 1.7 people, "
     "not per two; 246 km² is Malta island."),
    ("Verdict: misleading (high confidence).",
     "The 2022 figure is defensible, but leaving out that Eurostat’s latest figures put Malta 12th gives an inaccurate "
     "picture of where Malta stood."),
]))
S += [Spacer(1, 4 * mm), VerdictMeter(3), Spacer(1, 3 * mm),
      tiles([("585", GREEN, "Malta, 2022, in Eurostat’s revised data: seventh of 27, the figure the article reports"),
             ("12th", RED, "Malta’s rank in Eurostat’s 2023 figures (about 575), published by 25 July 2024"),
             ("≈602", GREY, "Malta’s 2022 value as Eurostat first released it (January 2024): sixth"),
             ("14th", ORANGE, "Malta’s rank in 2025 (571), now below the EU-27’s 584")]),
      Spacer(1, 4 * mm),
      up_down("Evidence that Eurostat’s 2023 figures were not public on 21 September 2024 (its article history shows "
              "they were from 23 July), or that the article told readers the rank was for 2022 and that newer figures "
              "existed.",
              "Evidence that the graphic the article relied on showed 2023 data, so that seventh and 585 were misread "
              "rather than out of date."),
      Spacer(1, 5 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the indicator measures"),
          ("4", "What Eurostat had published by 21 September 2024"), ("5", "What the data show now"),
          ("6", "Population growth and car density"), ("7", "Where the evidence points different ways"),
          ("8", "Testing the claim"), ("9", "Verdict and requests for evidence"), ("10", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The claim is Lovin Malta’s own text, read in full on 6 October 2026 on the page and through the site’s "
           "WordPress interface (post dated 21 September 2024) [1]. Lovin Malta is a news outlet and is the speaker "
           "here; the sentences below are its words, not quotations of anyone else. The article names Eurostat as the "
           "source of the dataset and a graphic by Paula Lago via The European Correspondent as the source of the "
           "rankings. We could not find the graphic (section 10)."))
S.append(std_table([
    [C("What Lovin Malta says", cellh), C("Where", cellh), C("Access", cellh)],
    [C("Eurostat “shared a dataset detailing the unit of cars per thousand residents in each European country as of "
       "2023”; a graphic “better illustrated these rankings up to the year 2022”"), C("Paragraphs 1–2 [1]"),
     C("Read in full; graphic not found")],
    [C("“according to the statistics Malta is ranked number seven, just between Germany and Poland respectively, "
       "with 585 cars per 1,000 inhabitants”"), C("Paragraph 3 [1]"), C("Read in full")],
    [C("Italy the “top-ranker … at a whopping 682”; Latvia lowest “with only 409 per 1,000”"), C("Paragraph 2 [1]"),
     C("Read in full")],
    [C("“approximately 1 car for every 2 people”; “with just 246 square kilometres of land, Malta is also up there "
       "among the countries with the highest car density in Europe”"), C("Paragraph 4 [1]"), C("Read in full")],
], [104 * mm, 36 * mm, 30 * mm]))
S.append(P("The headline is “Malta Ranked Number Seven On Eurostat’s ‘Passenger Cars Per 1,000 Inhabitants’ "
           "Dataset”. The claim record’s summary (seventh in the EU, 585 per 1,000) matches the article; we rate the "
           "article’s own sentences, which add the neighbours (Germany, Poland), describe the dataset as “as of 2023” "
           "and give no year for the 585."))
S += [Spacer(1, 2 * mm),
      callout([P("SCOPE NOTE", tag),
               P("This check tests the statistics the article reports and how it presents them. It does not assess "
                 "traffic, congestion, pollution or transport policy, which the article mentions in passing, nor the "
                 "readers’ comments it summarises. Claim Check 003 covers Malta’s per-capita greenhouse gas emissions.",
                 small)],
              bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Question.</b> Was Malta seventh in the EU with 585 passenger cars per 1,000 inhabitants, between Germany "
           "and Poland; for which year; was that Malta’s latest rank when the article appeared; and are the article’s "
           "other figures right?"))
S.append(P("<b>Evidence.</b> This claim is statistical. On 6 October 2026 we downloaded through Eurostat’s API the rate "
           "(<i>road_eqs_carhab</i>, updated 30 July 2026) [2], the stock of passenger cars (<i>road_eqs_carmot</i>) [3], "
           "the population on 1 January (<i>demo_gind</i>) [4] and land area (<i>reg_area3</i>) [5], for every country "
           "and year, keeping Eurostat’s flags. The API serves only current data, so for what Eurostat had published "
           "before the article we used Eurostat’s own publications: its release of 17 January 2024 with its chart [6], "
           "and the revision history of its article “Passenger cars in the EU”, read through the site’s MediaWiki "
           "interface, with the charts each version showed [13, 14]. Eurostat’s charts were read by pixel measurement, "
           "calibrated on their gridlines and checked against the values Eurostat prints in the text (all within 1.2 "
           "cars per 1,000). Everything is recomputed by <i>tools/cc-075-report/</i> from <i>data/cc-075/</i> [12]. "
           "Crossref and OpenAlex were searched for peer-reviewed work on car ownership in Malta; one comparative study "
           "was read in full [9]. Malta’s National Statistics Office (NSO) and Transport Malta refused scripted access, "
           "so their figures are second-hand (◆) [10, 11]."))
S.append(P("<b>Grades.</b> Official statistics and reviews are grade C under our scale. <b>Verdicts</b> follow the "
           "five-point scale in Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(60 * mm))
S.append(SectionHeading(3, "What the indicator measures"))
S.append(P("Eurostat’s “motorisation rate” is the number of passenger cars per 1,000 inhabitants [7]. A passenger car "
           "is a road motor vehicle designed to seat no more than nine people including the driver (category M1). "
           "Privately owned and company cars, taxis, private hire cars, shared cars and rented cars are included; light "
           "utility vehicles, buses and minibuses are not [7]."))
S.append(P("<b>How the rate is built.</b> We could not open Eurostat’s methodology page for this dataset (section 10), "
           "so we rebuilt the rate. Dividing each country’s car stock at 31 December [3] by its population on 1 January "
           "of the following year [4] reproduces Eurostat’s 2022 value for all 27 Member States, within one car per "
           "1,000 [12]. For Malta: 317,234 cars at the end of 2022 and 542,051 people on 1 January 2023 give 585.2."))
S.append(P("<b>Registered or licensed?</b> Eurostat collects these figures from national authorities through a "
           "questionnaire shared with the ITF and UNECE; collection methods are “not harmonised at EU level”, and "
           "vehicle registers “may include very old vehicles without signs of life” [7, 8]. For Malta, NSO publishes the "
           "stock of <i>licensed</i> motor vehicles. Its release for the end of 2022 is reported to give 424,904 licensed "
           "vehicles, 74.7% of them passenger cars, about 317,400 ◆ [10]; Eurostat’s 317,234 lies within the rounding "
           "range (317,191–317,616). NSO’s quarterly figures also count vehicles “taken off the road” (garaged, resold "
           "or scrapped) ◆ [11]. This suggests that Malta’s Eurostat figure is the licensed stock; we could not read "
           "NSO’s release to confirm it. Rented cars are in the numerator and residents only in the denominator [4, 7]; "
           "we found no readable count of rented cars in Malta’s stock."))

# ================================================================== 4
S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(4, "What Eurostat had published by 21 September 2024"))
S.append(P("Eurostat released the 2022 figures on 17 January 2024. Its chart in that release, and the chart in its "
           "article “Passenger cars in the EU” at the time, put Malta sixth at about 602 [6, 14]. In July 2024 Eurostat "
           "updated the article with data extracted that month: from 23 July its text gives 2023 values (Italy 694, EU "
           "571), and from 25 July its Figure 3 charts 2023 for all 27 Member States [13]. That version (revision "
           "647912, saved 19 August 2024) stayed online until 5 November 2024, so it was Eurostat’s published picture on "
           "21 September 2024 [13]. In it Malta is 12th, at about 575, behind France (about 578) and ahead of Austria "
           "(about 566) (Figure 1). The same version’s Table 2 gives Malta’s car stock as 317,234 for 2022 and 323,852 "
           "for 2023, the same as today’s data [3, 13]."))
S.append(KeepTogether([std_table([
    [C("Eurostat publication", cellh), C("Date", cellh), C("Year shown", cellh), C("Malta", cellh), C("Rank (EU-27)", cellh),
     C("Source", cellh)],
    [C("News release and chart; article Figure 3"), C("16–17 Jan 2024"), C("2022"), C("about 602"), C("6th"),
     C("[6, 14]")],
    [C("Article “Passenger cars in the EU”, revision 647912 (live 19 Aug – 5 Nov 2024)"), C("text 23 Jul, chart "
                                                                                             "25 Jul 2024"),
     C("2023"), C("about 575"), C("<b>12th</b>"), C("[13]")],
    [C("<i>Lovin Malta article</i>"), C("<i>21 Sep 2024</i>"), C("<i>not stated</i>"), C("<i>585</i>"),
     C("<i>“number seven”</i>"), C("[1]")],
    [C("Database today (updated 30 Jul 2026)"), C("—"), C("2022 / 2023 / 2025"), C("585 / 575 / 571"),
     C("7th / 11th / 14th"), C("[2]")],
], [60 * mm, 26 * mm, 22 * mm, 22 * mm, 22 * mm, 18 * mm]),
    P("“About” values are read from Eurostat’s charts by pixel measurement (data/cc-075/chart_reads.csv); they match "
      "every value Eurostat prints in the accompanying text within 1.2 cars per 1,000. Malta’s gap to its neighbours "
      "in the 2023 chart (about 3 and 8) is larger than that error.", cap)]))
S.append(KeepTogether([fig(FIG / "fig5_published2023.png"), P(
    "Figure 1. Passenger cars per 1,000 inhabitants in 2023, as Eurostat published them by 25 July 2024 and as they "
    "stood on 21 September 2024. Malta is 12th [13].", cap)]))
S.append(P("So the article’s 585 and seventh place are the 2022 column of data revised after January 2024: the 2022 "
           "value Eurostat first released was about 602 (sixth), and when the article appeared Eurostat’s published "
           "2023 figures put Malta 12th. The article does not say which year its figures are for."))

# ================================================================== 5
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(5, "What the data show now"))
S.append(KeepTogether([fig(FIG / "fig2_rank2022.png"), P(
    "Figure 2. Passenger cars per 1,000 inhabitants, 2022, all 27 Member States, in today’s data. Malta (585) is "
    "seventh, between Germany (587, break in series) and Poland (584, imputed); Czechia (582) is three cars behind. "
    "In Eurostat’s January 2024 release Malta was sixth (about 602) and Poland about 571 [2, 6].", cap)]))
S.append(KeepTogether([
    std_table([
        [C("Indicator", cellh), C("Malta", cellh), C("Comparison", cellh), C("Source", cellh), C("Grade", cellh)],
        [C("Passenger cars per 1,000 inhabitants, 2022 (today’s data)"), C("<b>585</b> (no flag)"), C("EU-27 564"),
         C("Eurostat [2]"), grade_tag("C")],
        [C("Rank among the EU-27, 2022 (today’s data)"), C("<b>7th of 27</b>"), C("Germany 587 (b), Poland 584 (i)"),
         C("Eurostat [2]"), grade_tag("C")],
        [C("Rank among all 41 countries in the dataset, 2022"), C("9th"), C("Liechtenstein 773, Iceland 611 (i) higher"),
         C("Eurostat [2]"), grade_tag("C")],
        [C("Rank, 2024 / 2025 (today’s data)"), C("13th / 14th"), C("Malta 576 / 571; EU-27 577 / 584"),
         C("Eurostat [2]"), grade_tag("C")],
        [C("Car stock at 31 Dec 2022 vs NSO licensed passenger cars"), C("317,234"), C("about 317,400 ◆"),
         C("Eurostat [3]; NSO [10]"), grade_tag("C")],
    ], [56 * mm, 32 * mm, 44 * mm, 24 * mm, 14 * mm]),
    P("Flags: b = break in time series, i = imputed. All values in <i>data/cc-075/checks.csv</i> [12]. Malta’s values "
      "carry no flag in any year. Earlier published versions: section 4.", cap)]))
S.append(P("Malta’s rank over time", h2))
S.append(P("In today’s data Malta’s rate rose from 302 in 1990 to a peak of 616 in 2016, and has drifted down since. Its "
           "rank in the EU-27 was third in eleven years (1995, 1997, 2007–2012 and 2014–2016), seventh in 2022 and 14th "
           "in 2025, when it fell 13 cars per 1,000 below the EU-27 value (Figure 3) [2]. A 2010 comparative study of "
           "four island states described Malta’s car ownership as then “the highest in the European Union” [9]; it used "
           "a different measure and earlier data, and in Eurostat’s current series Malta was third in those years."))
S.append(KeepTogether([fig(FIG / "fig1_trend.png"), P(
    "Figure 3. Top: passenger cars per 1,000 inhabitants, Malta and EU-27, 1990–2025, in today’s data. Bottom: Malta’s "
    "rank among the EU-27 countries with a value each year. The shaded band marks 2022, the year the article’s figures "
    "match. No Malta value for 2003–2004 [2].", cap)]))

# ================================================================== 6
S.append(CondPageBreak(30 * mm))
S.append(SectionHeading(6, "Population growth and car density"))
S.append(P("The fall in the rate is a population effect. Malta’s passenger car stock grew every year from 2006 to 2025 "
           "[3]: by 6,618 in 2023, 6,632 in 2024 and 5,209 in 2025. Its population grew faster: from the end of 2012 to "
           "the end of 2025 the car stock rose 34.5% (249,612 to 335,693) and the population 39.6% (421,464 to 588,254) "
           "[3, 4]. In 2022 alone the stock rose 1.3% and the population 4.2%, which is why the rate dropped from 602 to "
           "585 in today’s data; from 2022 to 2025 the population grew 8.5% and the car stock 5.8% [3, 4]."))
S.append(P("Measured per km² of land instead of per person, Malta is far ahead of every other Member State: 1,014 "
           "passenger cars per km² in 2022 against 261 in the Netherlands, the next highest, and 1,073 in 2025 [3, 5]. "
           "The article’s 246 km² is Malta island (245 km² of land in Eurostat’s data); the whole country, including "
           "Gozo and Comino, has 313 km² [5]. The article’s sentence (Malta “up there among the countries with the "
           "highest car density”) holds on either area."))

# ================================================================== 7
S.append(CondPageBreak(75 * mm))
S.append(SectionHeading(7, "Where the evidence points different ways"))
S.append(contested(
    "Q1  Was “seventh” Malta’s standing when the article appeared?", "NO: 2023 FIGURES PUT MALTA 12TH", RED,
    "585 and seventh place are right for 2022 in Eurostat’s revised data [2], and the article dates its graphic “up to "
    "the year 2022”.",
    "Eurostat’s article, in the version online from 19 August to 5 November 2024, gave 2023 figures for all 27 Member "
    "States, with Malta 12th at about 575 [13]. The Lovin Malta article calls the dataset “as of 2023”, states the "
    "rank in the present tense and never gives a year for the 585.",
    "<b>For this claim:</b> the 2022 figure is defensible, but presenting seventh as Malta’s standing, without saying "
    "it was 2022 or that Eurostat’s newer figures put Malta 12th, leaves out a material fact and gives an inaccurate "
    "picture."))
S.append(P("<b>Comparability.</b> Eurostat publishes and ranks these rates side by side [6, 7], and Malta’s values carry "
           "no flag, but collection methods are “not harmonised at EU level” and registers may hold cars with no "
           "“signs of life” [7]. Revisions also move places: after January 2024 Malta’s 2022 value went from about 602 to "
           "585 and Poland’s from about 571 to 584 [2, 6]. Places 6 to 9 in 2022 are within five cars per 1,000 "
           "(Germany 587, Malta 585, Poland 584, Czechia 582). Exact positions are fragile, a further reason to give "
           "the year and the version of the data with a rank."))

# ================================================================== 8
S.append(CondPageBreak(60 * mm))
S.append(SectionHeading(8, "Testing the claim"))
S.append(P("Each statement in the article, rated on its own; the verdict (section 9) weighs them together."))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> Malta has 585 cars per 1,000 inhabitants"),
     C("Right for 2022 in data revised after January 2024: 585, no flag; rebuilt from 317,234 cars and 542,051 people "
       "[2–4]. Eurostat’s January 2024 release had about 602 [6]."),
     verd("ACCURATE (2022, REVISED DATA)", GREENC)],
    [C("<b>B.</b> Ranked number seven, between Germany and Poland"),
     C("Seventh of 27 for 2022 in today’s data, between Germany 587 (b) and Poland 584 (i) [2]. In the January 2024 "
       "release Malta was sixth and Poland 11th [6]."),
     verd("ACCURATE (2022, REVISED DATA)", GREENC)],
    [C("<b>C.</b> Presented as current: dataset “as of 2023”, Malta “is ranked” seventh"),
     C("The article dates its graphic “up to the year 2022” but calls the dataset “as of 2023” and gives the rank in "
       "the present tense. Eurostat had published 2023 figures by 25 Jul 2024: Malta about 575, 12th [13]. Separately, "
       "in today’s revised data Malta is 11th for 2023 [2]."),
     verd("OUT OF DATE WHEN PUBLISHED", RED)],
    [C("<b>D.</b> Italy top at 682, Latvia lowest at 409"),
     C("Italy 682 matches today’s 2022 data (684 in January 2024); Latvia is lowest in every version (406 now, 414 "
       "then) [2, 6]."),
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
S.append(P("<b>The figure and rank (A, B)</b> reproduce from Eurostat’s data for 2022, but only from the version revised "
           "after January 2024. <b>How they are presented (C)</b> is the problem: the article reports them as Malta’s "
           "current standing when Eurostat’s published 2023 figures put Malta 12th. <b>The side remarks (D–F)</b> are "
           "right in direction: Latvia’s figure differs by data version, “1 car for every 2 people” understates Malta’s "
           "rate, and 246 km² is the main island, though Malta leads the EU on car density on either area."))

# ================================================================== 9
S += [CondPageBreak(55 * mm), Spacer(1, 3 * mm), SectionHeading(9, "Verdict and requests for evidence"),
      verdict_box("Misleading", "The 2022 figure is right in revised data, but the article presents seventh as current "
                  "when Eurostat’s 2023 figures, published two months earlier, put Malta 12th. Confidence: high."),
      Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) Malta’s 585 and seventh place, between Germany and Poland, match Eurostat’s 2022 data as "
           "revised after January 2024; Eurostat’s January 2024 release had Malta sixth at about 602 [2, 6]. (2) By 23–25 "
           "July 2024 Eurostat had published 2023 figures for all 27 Member States, and the version of its article that "
           "showed them was online from 19 August to 5 November 2024: Malta about 575, 12th [13]. (3) The article calls "
           "the dataset “as of 2023” and says “Malta is ranked number seven” without giving a year or mentioning the "
           "2023 figures. Readers would take seventh as Malta’s latest standing; on Eurostat’s published figures it "
           "was not. Individual statements are defensible, but the omission makes the overall impression inaccurate, "
           "which is the scale’s definition of Misleading. (4) Confidence is high because Eurostat’s dated revision "
           "history, the chart file with its upload time and checksum, the values in Eurostat’s text and our pixel "
           "reading all agree [12, 13]. The documents are listed in the claim record (evidence shown)."))
S.append(P("<b>What this verdict does not say.</b> It does not say the 585 figure is wrong (it is right for 2022 in "
           "today’s data), and it says nothing about intent: the graphic the article used may itself have been built "
           "from 2022 data. It assesses the article as published. It also says nothing about congestion, pollution or "
           "transport policy."))
S.append(KeepTogether([P("Evidence we are asking for", h2), requests_list([
    "From Lovin Malta: the graphic it used (Paula Lago, The European Correspondent), the data year and Eurostat "
    "release behind the 585 and the seventh place, and whether the article was checked against Eurostat’s 2023 figures.",
    "From NSO or Transport Malta: the stock of licensed passenger cars by year, the number of rented cars in it, and "
    "the number of registered but unlicensed (garaged) cars.",
])]))
S.append(P("<b>Right of reply.</b> Under the project’s rule a reply is sought for a Misleading verdict. A letter to "
           "Lovin Malta has been drafted for the maintainer; any response will be appended and the verdict revisited. "
           "Until the reply deadline has passed, this draft verdict is shown only on Miżien’s own site."))

# ================================================================== 10
S += [Spacer(1, 6 * mm), CondPageBreak(60 * mm), SectionHeading(10, "Limitations")]
for l in ["Eurostat’s database serves only current data. What Eurostat had published earlier is shown through its "
          "Statistics Explained revisions and charts [13, 14] and its January 2024 release [6], not through a copy of "
          "the database itself. The article’s own data date is unknown.",
          "The earlier values are read from Eurostat’s charts by pixel measurement; they match every value Eurostat "
          "prints within 1.2 cars per 1,000, and Malta’s 12th place in 2023 rests on gaps of about 3 and 8.",
          "The graphic the article used (Paula Lago, The European Correspondent) was not found (the embedded Instagram "
          "post needs a login; web.archive.org reset every connection). Eurostat’s methodology page for road "
          "equipment returned “not found”, so the denominator was established by recomputation.",
          "NSO and Transport Malta refused scripted access. The licensed-vehicle figures [10, 11] are second-hand (◆); "
          "Newsbook’s passenger-car counts are internally inconsistent and are not used. No readable count of rented "
          "cars in Malta’s stock was found.",
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
    ("6", "Eurostat (17 Jan 2024). Passenger cars per 1 000 inhabitants reached 560 in 2022. Eurostat news, with the chart "
          "“Motorisation rate of passenger cars in the EU, 2012 and 2022” (sha1 236d4565…). Read 6 Oct 2026.",
     "https://ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-20240117-1"),
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
    ("12", "Miżien. Data and calculations: data/cc-075/; tools/cc-075-report/ (calc.py, read_charts.py).", ""),
    ("13", "Eurostat. Passenger cars in the EU. Statistics Explained, revision 647912 (saved 19 Aug 2024, replaced "
           "5 Nov 2024; “Data extracted in July 2024”), with Figure 3 “Motorisation rate, 2023” (file uploaded 25 Jul "
           "2024, sha1 7dd8b8d6…) and Table 2. Read through the MediaWiki API, 6 Oct 2026.",
     "https://ec.europa.eu/eurostat/statistics-explained/api.php?action=query&prop=revisions&revids=647912"
     "&rvprop=content|timestamp&rvslots=main&format=json"),
    ("14", "Eurostat. Passenger cars in the EU. Statistics Explained, revision 627098 (31 Jan 2024; “Data extracted in "
           "December 2023”), with Figure 3 “Motorisation rate, 2022” (file uploaded 16 Jan 2024, sha1 2eb4c04f…). Read "
           "through the MediaWiki API, 6 Oct 2026.",
     "https://ec.europa.eu/eurostat/statistics-explained/api.php?action=query&prop=revisions&revids=627098"
     "&rvprop=content|timestamp&rvslots=main&format=json"),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "6 Oct 2026", "First issue. Draft verdict Misleading (high confidence); pending right of "
                                         "reply (Lovin Malta).")])

build_report(Report(
    number="075", out=str(FIG / "report.pdf"), kicker="Statistics and EU data",
    title_lines=["Is Malta seventh", "in the EU for", "cars per person?"],
    subtitle_lines=["Testing a media report of Eurostat’s passenger-car", "figures against the data and its dates"],
    quote_lines=["“Malta is ranked number seven, just between", "Germany and Poland … with 585 cars",
                 "per 1,000 inhabitants.”"],
    quote_size=14,
    attribution="Lovin Malta (J. Darmanin), 21 September 2024.",
    context="The outlet’s own text, citing Eurostat; no year given for the figure.",
    verdict="Misleading", verdict_note="A 2022 rank presented as current; 2023 figures put Malta 12th",
    footer_lines=["Version 1.0 (draft)  ·  6 October 2026", "Status:",
                  "Prepared from public sources and Eurostat data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Passenger cars per person: Malta and the EU", version="1.0", date="6 October 2026",
    status_note=REPLY,
    pdf_title="Is Malta seventh in the EU for cars per person? Claim Check 075",
    pdf_subject="Tests Lovin Malta's report that Malta ranks seventh in the EU with 585 passenger cars per 1,000 inhabitants",
    story=S))
