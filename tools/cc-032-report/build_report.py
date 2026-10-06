"""Claim Check 032 report. Run fetch.py, calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
LG = colors.HexColor("#8DB36B")
MAROON = colors.HexColor("#8E2F25")
S = []

# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("On 21 October 2025 the Government announced fifteen “solar flowers” at the Gozo Multi-Modal Hub in Ta’ "
        "Xħajma as “the first installation of its kind in Europe” (Lovin Malta’s text, tagged “Press Release”); Minister "
        "Clint Camilleri spoke of <b>“these first solar flowers in Europe”</b> and said their energy would supply the "
        "Park and Ride buses [1–3]. We checked both claims against the record.", lead)]
S.append(key_points([
    ("Europe had solar flowers before Gozo.",
     "The units are SmartFlowers, an Austrian product [5]. Dated reports show two installed in Switzerland (2015), "
     "one in service at an Austrian motorway rest area (2016) and one at Vodafone’s UK headquarters (2021) [13–15, "
     "30]. The maker calls Gozo’s “one of the largest installations in Europe”, not the first [5]."),
    ("The minister’s quote was narrower in one place.",
     "He also called it the first of its kind in Malta and, by number at one site, second in the world [1, 2]. "
     "Nothing we found contradicts the first; we did not test the second."),
    ("How much bus charging the flowers cover has not been shown.",
     "No capacity, metered output or bus use is published, and Parliament was told no feasibility study was made "
     "[10] " + DIAM + ", so the share covered cannot be calculated. If each unit is 2.5 kWp, the Commission’s PVGIS "
     "model gives about 85 MWh a year [17]."),
    ("The tracking gain and the cost hold up.",
     "PVGIS gives 36.5% more than fixed panels at the site, against “up to 40%” claimed [17]. About €850,000 of EU "
     "recovery funds fits the figure given to Parliament [10] " + DIAM + " and the EU award notice we identify as this "
     "contract, plus VAT [26–28]."),
    ("Verdict: contradicted (high confidence).",
     "Europe’s first solar flowers: contradicted by dated records. Powering the buses: not substantiated. Pending "
     "right of reply."),
]))
S += [Spacer(1, 2 * mm), VerdictMeter(4), Spacer(1, 2 * mm),
      tiles([("2016", RED, "a SmartFlower was already in service at an Austrian motorway rest area [13, 14]"),
             ("15", GREEN, "SmartFlowers at Ta’ Xħajma; to the maker, “one of the largest installations in Europe”"),
             ("≈85 MWh", GREEN, "a year modelled if each unit is 2.5 kWp (two-axis tracking); nothing metered is published"),
             ("None", ORANGE, "published figures for the buses’ charging: the share the flowers cover cannot be calculated")]),
      Spacer(1, 3 * mm),
      up_down("Documents from October 2025 showing that “of its kind” meant a feature no earlier European installation "
              "had, and that this was said: <i>Misleading</i>, since “these first solar flowers in Europe” would still "
              "mislead. Only a use specific to buses, or the number at one site, might be new: the maker presented an "
              "electric-vehicle charging version, pitched at public bodies, in January 2016 [31].",
              "Nothing: <i>Contradicted</i> is already the lowest rating. Metered output and charging data would settle "
              "the bus-charging part, not this verdict."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What a solar flower is"),
          ("4", "Were they the first in Europe?"), ("5", "Do they power the buses?"),
          ("6", "Where the evidence points different ways"), ("7", "Testing the claim"),
          ("8", "Verdict and requests for evidence"), ("9", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The Government’s own press release (gov.mt) could not be read from our network. Three readable texts carry "
           "it, and the claim is assembled from them. Only words inside quotation marks in those texts are treated as the "
           "speakers’ own. Lovin Malta’s article is tagged “Press Release”, so its English is probably the Government’s "
           "own release. The Maltese article is the fullest: TVM’s English version drops the words “first … in Europe” "
           "from the minister’s quote, while Lovin Malta’s English keeps them [1–3]."))
S.append(std_table([
    [C("What was said", cellh), C("Who, where", cellh), C("Our access", cellh)],
    [C("“Bl-installazzjoni ta’ dawn l-ewwel solar flowers fl-Ewropa, qed nuru kif Għawdex jista’ jkun ta’ eżempju "
       "fl-innovazzjoni sostenibbli.” In English: “With the installation of these first solar flowers in Europe, we "
       "are demonstrating how Gozo can be a model for sustainable innovation.”"),
     C("Camilleri, quoted; TVM News (Maltese) [1]; Lovin Malta’s English (tagged “Press Release”) [2]"), C("Read in full")],
    [C("“… hija l-ewwel tax-xorta tagħha li qiegħda tintuża f’pajjiżna u li bħala ammont fl-istess żona hija t-tieni "
       "waħda fid-dinja …” (our translation: the first of its kind used in our country and, as a number in one "
       "place, the second in the world)."),
     C("Camilleri, quoted [1]; Lovin Malta’s English renders it “first of its kind in Malta” [2]"), C("Read in full")],
    [C("“This energy will be used to supply electricity, electric buses which offer transport between Imġarr port "
       "and the Park &amp; Ride facility.”"), C("Camilleri, quoted; TVM News (English) [3]"), C("Read in full")],
    [C("The installation is “the first installation of its kind in Europe” (Lovin Malta’s text) or “the first of its "
       "kind in Europe” (TVM’s indirect speech); the energy will directly offset the electricity used to charge the Park and "
       "Ride bus fleet; up to 40% more energy than traditional panels; about €850,000."),
     C("The statement as published, not in quotation marks: Lovin Malta’s text, tagged “Press Release” [2]; TVM News [1, 3]"), C("Read in full")],
    [C("Title: “… the first project of its kind in Europe”; text: “They are the first of their kind in Europe.” "
       "“Each ‘flower’ can generate 40% more power than traditional solar panels.” RRP C1-I5; €850,000."),
     C("European Commission project page (the “-0_en” page) [4]; not rated"), C("Read in full")],
    [C("Parliamentary Secretary Omar Farrugia: a solar system “unika fl-Ewropa” (“unique … in Europe”)."),
     C("Quoted [1, 2]"), C("Read; not rated separately")],
], [92 * mm, 50 * mm, 28 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("FAIRNESS NOTE", tag),
               P("The flowers exist, work and were paid for with EU recovery funds, as the Government said; Parliament "
                 "was told all fifteen were in working order [10] ◆. The minister’s own words also contain the narrower "
                 "and accurate-looking claim that this is a first for Malta. The Commission page’s wording matches the "
                 "Government statement; the claim is the Government’s, so the Commission’s own words are not rated. This "
                 "check is about the words used, not about whether the project was worth doing.", small)],
              bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Questions.</b> (A) Were these Europe’s first solar flowers, or the first installation of their kind, "
           "and what else could “first” mean? (B) How much electricity can fifteen flowers make, and how does that "
           "compare with what the Park and Ride buses use? (C) Is the stated tracking gain plausible? (D) What did the "
           "project cost and who paid?"))
S.append(P("<b>Evidence.</b> (A) The maker’s pages [5–8] and dated reports of earlier European installations "
           "[11–16, 30, 31]; search log in <i>literature/CC-032/notes.md</i>. (B, C) The European Commission’s PVGIS 5.3 model "
           "for the site [17], the data sheet [8, 9], GRDA and EU procurement records for the shuttle [19, 20], "
           "OpenStreetMap distances [23], and peer-reviewed estimates of bus consumption [24, 25] and tracking gains "
           "[18], read as abstracts. (D) Newsbook’s report of answers in Parliament [10] ◆, an EU award notice [26], "
           "the EU VAT table [27] and the Council decision on Malta’s recovery plan [28]. Inputs are in "
           "<i>data/cc-032/</i>; every figure is recomputed by <i>tools/cc-032-report/calc.py</i>."))
S.append(P("<b>Grades.</b> Individual news reports and company pages are grade D, but the records of earlier "
           "installations are independent of one another, dated, and from three countries. PVGIS, EU procurement records, "
           "the Council decision and the GRDA are grade C. The tracker study [18] uses measured radiation across a "
           "latitude gradient (grade B); the bus-consumption figures are modelled for other routes and buses (grade C, "
           "indicative here). ◆ marks second-hand material. <b>Verdicts</b> follow the five-point scale in Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(70 * mm))
S.append(SectionHeading(3, "What a solar flower is"))
S.append(P("A SmartFlower is a free-standing photovoltaic unit with twelve petal-shaped panels that fan open at "
           "sunrise, follow the sun on two axes and fold away at night or in strong wind [4, 7–9]. The maker gives "
           "2.5 kWp and 4,000–6,500 kWh a year per unit, depending on location [8, 9]. The product is manufactured in "
           "Austria, where the company was founded; a Boston firm bought it in 2018 [7]."))
S.append(P("Tracking raises output because the panels face the sun for more of the day. A study of five tracker types "
           "at locations across Europe and Africa found dual-axis trackers collected 17.7% to 31.2% more solar energy "
           "than panels fixed at the best angle, the gain varying with latitude [18]. The maker and the Government both "
           "say “up to 40%” [3, 7]; the PVGIS model gives 36.5% for this site (Section 5), but no measurements of these "
           "units are published, and the petal design may not behave like an ideal tracker."))
S.append(P("The capacity of the Gozo units has not been published in anything we read. If they are the 2.5 kWp model "
           "the maker sells, the fifteen add up to 37.5 kWp; we use that figure below and say so each time."))

# ================================================================== 4
S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(4, "Were they the first in Europe?"))
S.append(KeepTogether([fig(FIG / "fig1_timeline.png"),
                       P("Figure 1. Dated records of SmartFlowers in Europe before the Gozo statement, and the maker’s "
                         "own description of Gozo’s installation afterwards [1, 5, 13–15, 30, 31]. Records listed in "
                         "<i>data/cc-032/european_records.csv</i>.", cap)]))
S.append(P("Reading across the records (listed in the table below)", h2))
for t in ["• <b>As solar flowers, not the first.</b> Two were installed in Switzerland in May 2015 [30]; the same "
          "product was in service at an Austrian motorway rest area run by ASFINAG almost nine years before Gozo’s, and "
          "in the UK four years before [13–15].",
          "• <b>As an installation of this size, open.</b> The maker calls it “one of the largest installations in "
          "Europe” [5]; it does not call it the largest. The maker’s English version of the minister’s quote reads “By "
          "installing these [SmartFlowers] in Europe”, with “[SmartFlowers]” in place of “first solar flowers” [5].",
          "• <b>As a first for Malta, plausible.</b> Parliament was told no other such installation exists in Malta "
          "[10] ◆, and our web search found none. The minister’s claim to be second in the world by number at one "
          "site was not tested.",
          "• <b>As a use, only buses might be new.</b> The maker presented a version with an electric-vehicle charging "
          "station in Spain in January 2016, pitched at public administrations [31], and the 2016 Austrian unit "
          "supplied part of a motorway rest area’s lighting. Nothing we found shows an earlier European flower array "
          "charging buses, but the Government did not say that this was the novelty."]:
    S.append(P(t, bul))
S.append(Spacer(1, 2 * mm))
S.append(KeepTogether(std_table([
    [C("Date", cellh), C("Where", cellh), C("What the record says", cellh), C("Source", cellh)],
    [C("May 2015"), C("Umwelt Arena, Spreitenbach, Switzerland"),
     C("Two smartflowers newly installed at the arena and generating electricity (text credited to the arena)"),
     C("Moneycab [30]")],
    [C("Jun 2015"), C("Madrid, Spain"), C("Product launch: Smartflower, “made in Austria”, presented in Madrid and on sale "
                                          "in Spain from 3 June 2015"), C("energynews.es [11]")],
    [C("Jan 2016"), C("Spain (product)"), C("Smartflower presents “POP-e”, with an electric-vehicle charging station of up "
                                            "to 22 kW, as a “green business card” for public administrations and firms"),
     C("smartgridsinfo.es [31]")],
    [C("Jul 2016"), C("Vienna-based maker"), C("“Austria’s SmartFlower”; the company had sold over 1,000 units in Europe, "
                                               "Asia, the Middle East and elsewhere (its own figure)"), C("pv magazine [12]")],
    [C("Dec 2016"), C("Hinterbrühl rest area, A21, Austria"),
     C("Motorway operator ASFINAG puts a SmartFlower into service; it covers half of the rest area’s lighting "
       "electricity, about 3,550 of 7,000 kWh a year"), C("MeinBezirk.at community post [13]; IÖB [14]")],
    [C("Aug 2021"), C("Newbury, UK"), C("Vodafone erects a SmartFlower at its headquarters, made in Austria and installed "
                                        "by a UK distributor"), C("Newbury Today [15]")],
    [C("Undated"), C("UK, Jersey, Denmark, Spain"), C("Dealers list 17 UK and Jersey installations, some of two or three "
                                                      "units, and clients in Denmark, Spain and Scotland"), C("Dealer pages [16]")],
    [C("14 Nov 2025"), C("Ta’ Xħajma, Gozo"), C("Maker: the fifteen SmartFlowers are “one of the largest installations in "
                                                 "Europe”; its year review repeats this"), C("SmartFlower [5, 6]")],
], [20 * mm, 34 * mm, 84 * mm, 32 * mm])))

# ================================================================== 5
S.append(CondPageBreak(60 * mm))
S.append(SectionHeading(5, "Do they power the buses?"))
S.append(P("The minister said the energy “will be used to supply electricity, electric buses” running between Mġarr and "
           "the Park and Ride [3]; the statement said it would “directly offset” the electricity used to charge that "
           "fleet [2]. Neither gives an amount. Six electric buses owned by the Ministry for Gozo run the shuttle every "
           "10 minutes, operated by Malta Public Transport under negotiated contracts [19, 20]. The GRDA notes that "
           "uptake “remains very low” [19]. Where and when the six shuttle buses charge is not published. Since May "
           "2026, seven months after the statement, the hub has also held a new depot where Gozo’s route buses, now 29 "
           "electric buses in all, are charged during the night [21, 22]; Malta Public Transport describes its electric "
           "buses as “Primarily charging overnight”, with fast charging at its depot during the day [21]."))
S.append(KeepTogether([fig(FIG / "fig2_output.png", width=0.78 * CW),
                       P("Figure 2. A: modelled output a day by month at the Park and Ride if the fifteen units are "
                         "2.5 kWp each (37.5 kWp), with two-axis tracking and with fixed panels at the best angle "
                         "(PVGIS 5.3, 14% system loss) [17]. B: a conditional order of magnitude, not an estimate: the "
                         "hours of a 10-minute shuttle (8.5 km round trip [23]) that each month’s average day would "
                         "equal at 1.45–2.1 kWh per km, figures modelled for other buses and routes [24, 25]. The Gozo "
                         "units’ capacity and the buses’ consumption and hours are not published.", cap)]))
S.append(KeepTogether([std_table([
    [C("Indicator", cellh), C("Value", cellh), C("Source", cellh)],
    [C("Capacity of the 15 units"), C("Not published; <b>37.5 kWp</b> if 2.5 kWp each"), C("[8, 9]")],
    [C("Modelled output, two-axis tracking, if 2.5 kWp each"), C("<b>85,121 kWh a year</b>; 5,675 per unit; 233 kWh "
                                                "a day on average (152 in December, 315 in July)"), C("[17], calculated")],
    [C("Maker’s range for 15 units"), C("60,000–97,500 kWh a year"), C("[8], calculated")],
    [C("Same capacity, fixed at the best angle (32°)"), C("62,341 kWh a year: tracking adds <b>36.5%</b>"),
     C("[17], calculated")],
    [C("Metered output of the flowers"), C("Not published"), C("Search log")],
    [C("Shuttle: buses, frequency, round trip"), C("6 buses, every 10 minutes, 8.5 km: about 51 km per hour of "
                                                   "service"), C("[19, 20, 23]")],
    [C("Shuttle buses’ model, battery, consumption, hours"), C("Not published"), C("Search log")],
    [C("Energy per hour of 10-minute service, if 1.45–2.1 kWh/km"), C("74–107 kWh (conditional)"),
     C("[24, 25], calculated")],
    [C("Hours of that service the modelled average day would equal"), C("2.2–3.2 hours; 1.4–2.1 in December "
                                                                        "(conditional order of magnitude)"),
     C("calculated")],
], [62 * mm, 82 * mm, 26 * mm]),
    P("All inputs in <i>data/cc-032/</i>; results in <i>checks.csv</i>.", cap)]))
S.append(P("Three things follow. First, the amount of charging the flowers cover cannot be calculated from public "
           "data: neither their output nor the buses’ consumption has been published, and Parliament was told that no "
           "technical report, feasibility study or value-for-money comparison was made [10] ◆. Second, as a "
           "conditional order of magnitude only: if each unit is 2.5 kWp and the buses use 1.45–2.1 kWh per km, as "
           "modelled for other buses, the flowers’ average day would match roughly two to three hours of the 10-minute "
           "shuttle, less in winter; whether that is all or part of its charging depends on figures that are not "
           "public. Third, the flowers produce only in daylight. They can feed daytime charging or other loads "
           "at the hub directly, and offset night-time charging on a yearly balance through the grid, which is what the "
           "statement’s “offset” means; they cannot directly power buses charged overnight without storage, and none is "
           "mentioned. How they are wired is not published."))

# ================================================================== 6
S.append(CondPageBreak(85 * mm))
S.append(SectionHeading(6, "Where the evidence points different ways"))
S.append(contested(
    "Q1  Are they the first of their kind in Europe?", "NO, AS WORDED", MAROON,
    "Gozo’s array of fifteen is large: the maker calls it one of Europe’s largest [5]. Charging buses specifically "
    "may be new: we found no earlier European flower array doing so, though the maker presented an electric-vehicle "
    "charging version, pitched at public bodies, in January 2016 [31]. It is the first in Malta as far as we could find [10] ◆.",
    "Two units were installed in Switzerland (2015), and the product was in service in Austria (2016) and the UK "
    "(2021), among others [13–16, 30]. The maker does not call Gozo’s the first, or the largest [5, 6]. The minister "
    "said “these first solar flowers in Europe” [1, 2].",
    "<b>For this claim:</b> as worded it is contradicted. A narrower claim (first in Malta, or among the largest in "
    "Europe) would have been supported by what we found."))
S.append(contested(
    "Q2  Do the flowers power the buses’ charging?", "NOT SHOWN", ORANGE,
    "If each unit is 2.5 kWp, modelled output is about 85 MWh a year [17]. The statement says “offset”, which a "
    "yearly balance through the grid can deliver, and daytime charging could use the output directly.",
    "No capacity, metered output, bus consumption or wiring has been published, and no feasibility study was made "
    "[10] ◆. Where and when the six shuttle buses charge is not published; the hub’s night-charging depot opened "
    "seven months after the statement and serves the route fleet [22], and MPT also mentions daytime fast charging "
    "[21].",
    "<b>For this claim:</b> a part of the charging can be offset; how much has not been shown."))

# ================================================================== 7
S.append(CondPageBreak(70 * mm))
S.append(SectionHeading(7, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> Fifteen solar flowers were installed at the Gozo Multi-Modal Hub, Ta’ Xħajma"),
     C("Statement [1–3]"),
     C("The maker reports fifteen SmartFlowers at the hub [5]; Parliament was told all were working [10] ◆."),
     verd("ACCURATE", GREENC)],
    [C("<b>B.</b> “These first solar flowers in Europe”; “the first installation of its kind in Europe”"),
     C("Camilleri, quoted [1, 2]; Lovin Malta’s text [2] (TVM’s indirect speech [3]). Commission page not rated"),
     C("SmartFlowers, an Austrian product, were installed in Switzerland (2015) and in service in Austria (2016) and "
       "the UK (2021) [13–15, 30]; the maker calls Gozo’s “one of the largest installations in Europe” [5]."),
     verd("CONTRADICTED", MAROON)],
    [C("<b>C.</b> The first of its kind used in Malta; second in the world by number at one site"),
     C("Camilleri, quoted [1, 2]"),
     C("First in Malta: consistent with the reply to Parliament [10] ◆ and our search. Second in the world: not "
       "tested."), verd("NOT CONTRADICTED", GREY)],
    [C("<b>D.</b> The energy will supply, or offset the charging of, the Park and Ride electric buses"),
     C("Camilleri, quoted [3]; statement [2]"),
     C("No capacity, metered output or bus use published; no feasibility study [10] ◆. The share of charging covered "
       "cannot be calculated."), verd("NOT SUBSTANTIATED", ORANGE)],
    [C("<b>E.</b> Each flower yields up to 40% more energy than traditional panels"),
     C("Lovin Malta’s text [2]; TVM News [3]. Commission page [4] not rated"),
     C("PVGIS: 36.5% more than fixed panels at the best angle at the site [17]; one study: 18–31% elsewhere [18]. Not "
       "measured here. The Commission page’s flat “40% more power” has no “up to”, so it is stronger than the "
       "statement; it is not rated."), verd("LARGELY ACCURATE", LG)],
    [C("<b>F.</b> About €850,000, funded by the EU recovery plan (C1-I5)"),
     C("Statement [1, 3]"),
     C("Parliament was told €699,612 excluding VAT [10] ◆; the award we identify as this contract, €718,830, is "
       "€848,219 with VAT [26, 27]; C1-I5 funds solar panels in public spaces [28]."), verd("CONSISTENT", GREENC)],
], [40 * mm, 30 * mm, 70 * mm, 30 * mm], valign="MIDDLE"))

# ================================================================== 8
S += [Spacer(1, 3 * mm), SectionHeading(8, "Verdict and requests for evidence"),
      verdict_box("Contradicted", "The claim that Gozo’s fifteen solar flowers are Europe’s first is contradicted by dated "
                  "records of the same product installed elsewhere in Europe from 2015. Confidence: high."),
      Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) The headline claim, in the minister’s words and the statement, is that these are "
           "Europe’s first solar flowers, or its first installation of the kind. (2) The units are SmartFlowers, and "
           "independent, dated records show the same Austrian product installed in Switzerland in 2015 and in service "
           "in Austria from 2016 (a pilot by a motorway operator) and in the UK from 2021. (3) The maker calls "
           "Gozo’s installation one of the largest in Europe, not the first. The evidence points against the claim as "
           "worded: <i>Contradicted</i>. That the energy powers or offsets the buses’ charging is <i>Not "
           "substantiated</i>: no figures show how much."))
S.append(P("<b>Why high confidence.</b> Several independent lines agree: the maker’s own pages, local and trade "
           "reports in three countries, and an Austrian public-procurement record. <b>Why not Misleading.</b> The words "
           "are not a defensible statement that leaves a wrong impression; they state a fact that the records "
           "contradict."))
S.append(P("<b>What this verdict does not say.</b> It does not say the flowers do not work, that the money was wasted, "
           "that the energy is not used at the hub, or that anyone meant to mislead. A statement closer to the "
           "evidence: <i>“Malta’s first solar flowers, one of the largest such installations in Europe, will offset part "
           "of the electricity used to charge the Park and Ride buses.”</i>"))
S.append(KeepTogether([P("Evidence we are asking for", h2), requests_list([
    "What “first of its kind in Europe” referred to, and the source for “second in the world”.",
    "The installed capacity and model of the fifteen units, and their metered output since October 2025.",
    "The metered electricity used to charge the Park and Ride buses, their model and battery, the shuttle’s hours, "
    "and how the flowers are connected (to the chargers, the hub or the grid).",
    "The tender and contract documents (CT3013/2024, if that is this contract), and the reason the figure given to "
    "Parliament differs from the award notice.",
])]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag),
               P("A right of reply will be sought from the Ministry for Gozo and Planning, with the Public Works "
                 "Department, before this check circulates beyond Miżien’s site, with a fixed deadline (suggested 14 "
                 "days). Responses will be appended and the verdict revisited. A <i>Contradicted</i> verdict is not circulated "
                 "elsewhere before that deadline passes.", small)],
              bg=AMBER_PALE, bar=AMBER)]

# ================================================================== 9
S += [Spacer(1, 3 * mm), CondPageBreak(45 * mm), SectionHeading(9, "Limitations")]
for l in ["gov.mt and parlament.mt could not be read from our network; we used TVM News, Lovin Malta and Newsbook’s "
          "report of the answers in Parliament ◆.",
          "We did not establish which European SmartFlower was the first, only that several preceded Gozo’s, from news "
          "reports, a community post, a press release and dealer pages; the Swiss record is the arena’s own text.",
          "The capacity of the Gozo units is assumed from the maker’s current 2.5 kWp model. PVGIS models an ideal "
          "two-axis tracker with a default 14% loss; the petal design, shading at the hub and downtime are not modelled.",
          "The bus-consumption figures (1.45–2.1 kWh per km) were modelled for other buses and routes and read as "
          "abstracts; the route length comes from car routing on OpenStreetMap. Figure 2B is an order of magnitude, "
          "not an estimate of the share covered. EU award notice 742398-2024 is matched to this contract by its "
          "subject, buyer, date and value; it names no site."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 3 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "TVM News (21 October 2025). Installati l-ewwel solar flowers tax-xorta tagħhom fl-Ewropa fil-Gozo Multi-Modal "
          "Hub f’Ta’ Xħajma (Maltese).",
     "https://tvmnews.mt/news/installati-l-ewwel-solar-flowers-tax-xorta-taghhom-fl-ewropa-fil-gozo-multi-modal-hub-fta-xhajma/"),
    ("2", "Lovin Malta (21 October 2025). Gozo Leads The Way In Europe With First-Ever ‘Solar Flowers’ At Ta’ Xħajma "
          "Multi-Modal Hub (tagged “Press Release”: probably the Government’s English release).",
     "https://lovinmalta.com/malta/gozo-leads-the-way-in-europe-with-first-ever-solar-flowers-at-ta-xhajma-multi-modal-hub/"),
    ("3", "TVM News (21 October 2025). First solar flowers in Europe installed at the Gozo Multi-Modal Hub in Ta’ "
          "Xħajma (English).",
     "https://tvmnews.mt/en/news/first-solar-flowers-in-europe-installed-at-the-gozo-multi-modal-hub-in-ta-xhajma/"),
    ("4", "European Commission, Reforms and Investments. 15 solar flowers installed in Gozo for electricity generation, "
          "the first project of its kind in Europe (the page whose address ends “-0_en”, modified 2 February 2026, "
          "read 6 October 2026; the “-1_en” page has identical text, and the page with no suffix has a different "
          "body, without “first of their kind”).",
     "https://reforms-investments.ec.europa.eu/projects/15-solar-flowers-installed-gozo-electricity-generation-first-project-its-kind-europe-0_en"),
    ("5", "SmartFlower (14 November 2025). One of Europe’s Largest Installations Arrives with SmartFlowers.",
     "https://smartflower.com/news/one-of-europes-largest-installations-arrives-with-smartflowers/"),
    ("6", "SmartFlower (29 December 2025). A Year in Review: SmartFlower Growth, Impact and Inspiration for 2025.",
     "https://smartflower.com/news/2025-in-review-a-year-of-smartflower-growth-impact-and-inspiration/"),
    ("7", "SmartFlower. Frequently Asked Questions; Products; Company (web pages, read 6 October 2026).",
     "https://smartflower.com/frequently-asked-questions/"),
    ("8", "Smartflower (2019). The smart, simple &amp; stunning solar system: data sheet 150-0016 Rev G (dealer-hosted copy).",
     "https://www.worldofesf.com/docs/150-0016-SMARTFLOWER-DATA-SHEET-REV-G.pdf"),
    ("9", "pv magazine Australia (25 October 2024). Nature inspires 2.5 kW Smartflower mobile solar system.",
     "https://www.pv-magazine-australia.com/2024/10/25/nature-inspires-2-5-kw-smartflower-mobile-solar-system/"),
    ("10", "Newsbook (19 January 2026). Gozo’s solar flower installation cost €700,000 (report of parliamentary answers "
           "to Chris Said MP) ◆.",
     "https://newsbook.com.mt/en/gozos-solar-flower-installation-cost-e700000/"),
    ("11", "energynews.es (3 June 2015). Smartflower, una flor ‘made in Austria’, llega a España.",
     "https://www.energynews.es/smartflower-made-in-austria-llega-a-espana-para-hacer-posible-el-autoconsumo/"),
    ("12", "pv magazine (13 July 2016). Intersolar North America: SmartFlower unfurls its dual-axis tracker.",
     "https://www.pv-magazine.com/2016/07/13/intersolar-north-america-smartflower-unfurls-its-dual-axis-tracker_100025392/"),
    ("13", "Weber R. (7 December 2016). Grüner Strom für den Rastplatz Hinterbrühl auf der A 21. MeinBezirk.at, "
           "Mödling, Regionauten-Community post with an ASFINAG photo.",
     "https://www.meinbezirk.at/moedling/c-lokales/gruener-strom-fuer-den-rastplatz-hinterbruehl-auf-der-a-21_a1960598"),
    ("14", "IÖB, Innovationsfördernde Öffentliche Beschaffung (Austrian federal ministries). Asfinag: Photovoltaikanlage "
           "Solarblume (project page, undated).",
     "https://www.ioeb.at/erfolgreiche-projekte-detail/asfinag-photovoltaikanlage-solarblume"),
    ("15", "Newbury Today (12 August 2021). Vodafone installs ‘Smartflower’ solar sunflower on Newbury campus.",
     "https://www.newburytoday.co.uk/news/vodafone-installs-smartflower-solar-sunflower-on-newbury-c-9211498/"),
    ("16", "Green Mole Ltd. SmartFlower installations (UK); Smartflower Benelux. References (dealer pages, undated).",
     "https://smartflowersolar.co.uk/installations/"),
    ("17", "European Commission, Joint Research Centre. PVGIS 5.3 (PVGIS-SARAH3, 2005–2023), run 6 October 2026 for "
           "36.038 N, 14.272 E, 37.5 kWp, 14% loss (the user manual’s default).",
     "https://re.jrc.ec.europa.eu/api/v5_3/PVcalc"),
    ("18", "Bahrami A., Okoye C.O., Atikol U. (2016). The effect of latitude on the performance of different solar "
           "trackers in Europe and Africa. <i>Applied Energy</i> 177:896–906. doi:10.1016/j.apenergy.2016.05.103 "
           "(abstract read).", "https://doi.org/10.1016/j.apenergy.2016.05.103"),
    ("19", "Gozo Regional Development Authority (December 2025). National Transport Master Plan 2030: feedback by the "
           "GRDA.", "https://grda.mt/wp-content/uploads/2025/12/National-Transport-Master-Plan-2030.pdf"),
    ("20", "Tenders Electronic Daily: Ministry for Gozo and Planning, operation of the Park and Ride service with six "
           "MGP-owned electric buses, notices 142379-2025, 169742-2025, 155274-2026 and 183660-2026 (search API).",
     "https://ted.europa.eu/en/notice/-/detail/183660-2026"),
    ("21", "Malta Public Transport. Electric Buses (web page, read 6 October 2026).",
     "https://www.publictransport.com.mt/travel-information/electric-buses/"),
    ("22", "TVM News (28 May 2026). Public transport in Gozo is now being completely operated with electric buses.",
     "https://tvmnews.mt/en/news/public-transport-in-gozo-is-now-being-completely-operated-with-electric-buses/"),
    ("23", "OpenStreetMap contributors, routed with OSRM: Ta’ Xħajma Park and Ride to the Mġarr ferry terminal and back, "
           "4.35 and 4.15 km (retrieved 6 October 2026).", "https://router.project-osrm.org/"),
    ("24", "Czapla Z., Sierpiński G. (2023). Driving and energy profiles of urban bus routes predicted for operation with "
           "battery electric buses. <i>Energies</i> 16:5706. doi:10.3390/en16155706 (abstract read).",
     "https://doi.org/10.3390/en16155706"),
    ("25", "Li X., Horváth B., Winkler Á. (2025). Assessing the sustainability of electric and hybrid buses: a life cycle "
           "assessment approach to energy consumption in usage. <i>Energies</i> 18:1545. doi:10.3390/en18061545 "
           "(abstract read).", "https://doi.org/10.3390/en18061545"),
    ("26", "Tenders Electronic Daily, award notice 742398-2024: CT3013/2024, dual axis solar photovoltaic system for the "
           "Public Works Department, concluded 3 December 2024, €718,830.07 (our identification as this contract).",
     "https://ted.europa.eu/en/notice/-/detail/742398-2024"),
    ("27", "Baert P. (January 2026). Highs and lows: VAT rate-setting in the European Union. European Parliamentary "
           "Research Service, PE 782.613, Table 3.",
     "https://www.europarl.europa.eu/RegData/etudes/BRIE/2026/782613/EPRS_BRI(2026)782613_EN.pdf"),
    ("28", "Council of the European Union (17 July 2026). 11894/26 ADD 1: annex to the amended Council Implementing "
           "Decision on Malta’s recovery and resilience plan (C1-I5, target 1.27); and 15652/25 (19 November 2025).",
     "https://data.consilium.europa.eu/doc/document/ST-11894-2026-ADD-1/en/pdf"),
    ("29", "Miżien. Data and calculations: data/cc-032/; tools/cc-032-report/calc.py.", ""),
    ("30", "Moneycab (19 May 2015). In der Umwelt Arena erzeugen sogar Blumen Elektrizität (text credited to the Umwelt "
           "Arena, Spreitenbach).",
     "https://www.moneycab.com/dossiers/in-der-umwelt-arena-erzeugen-sogar-blumen-elektrizitaet/amp/"),
    ("31", "smartgridsinfo.es (28 January 2016). Nuevo sistema fotovoltaico para la recarga de vehículos eléctricos "
           "(smartflower POP-e).",
     "https://www.smartgridsinfo.es/2016/01/28/nuevo-sistema-fotovoltaico-para-la-recarga-de-vehiculos-electricos"),
])

S += [Spacer(1, 2 * mm), CondPageBreak(60 * mm)]
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 2 * mm)]
S += revision_log([
    ("1.0", "6 Oct 2026", "First issue. Pending right of reply (Ministry for "
                          "Gozo and Planning; Public Works Department)."),
])

build_report(Report(
    number="032", out=str(FIG / "report.pdf"), kicker="Renewables, Gozo",
    title_lines=["Europe’s first", "solar flowers?"],
    subtitle_lines=["Testing the Government’s claims about Gozo’s fifteen", "solar flowers against the record"],
    quote_lines=["“With the installation of these first solar flowers in Europe,", "we are demonstrating how Gozo can be a model",
                 "for sustainable innovation.”"], quote_size=13.5,
    attribution="Clint Camilleri, Minister for Gozo and Planning, 21 October 2025.",
    context="English as in Lovin Malta (tagged “Press Release”); Maltese original in TVM News.",
    verdict="Contradicted", verdict_note="Solar flowers were installed elsewhere in Europe from 2015",
    footer_lines=["Version 1.0  ·  6 October 2026",
                  "Status: draft, pending right of reply (Ministry for Gozo and Planning; Public Works Department)",
                  "Prepared from public sources, EU records and the PVGIS model.",
                  "Repository: github.com/leandergrech/Mizien"],
    running_head="Gozo’s solar flowers", version="1.0", date="6 October 2026",
    pdf_title="Europe's first solar flowers? Claim Check 032",
    pdf_subject="Tests the Government's claim that Gozo's 15 solar flowers are Europe's first and power its electric buses",
    story=S))
