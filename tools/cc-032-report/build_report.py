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
        "Xħajma. Its statement, as TVM News reported it, called them “the first of its kind in Europe”, and Gozo "
        "Minister Clint Camilleri spoke of <b>“these first solar flowers in Europe”</b> [1, 2]. The energy, he said, "
        "would supply the electric buses that shuttle passengers to Mġarr. We checked both claims against earlier "
        "installations, the manufacturer’s records, a European Commission solar model and the public record on the "
        "buses and the cost.", lead)]
S.append(key_points([
    ("Europe had solar flowers before Gozo.",
     "The fifteen units are SmartFlowers [5], an Austrian product. Dated reports show them in Spain in 2015, at an "
     "Austrian motorway rest area in 2016 and at Vodafone’s UK headquarters in 2021 [11–15]. The maker calls Gozo’s "
     "“one of the largest installations in Europe”, not the first [5, 6]."),
    ("The minister’s quote was narrower in one place.",
     "In the same statement he called it the first of its kind used in Malta and, by number at one site, the second "
     "in the world [1, 2]. Nothing we found contradicts the first; we did not test the second."),
    ("How much bus charging the flowers cover has not been shown.",
     "No capacity, metered output or bus consumption has been published, and Parliament was told no feasibility "
     "study was made [10] ◆. The modelled output, about 85 MWh a year [17], equals roughly 2–3 hours a day of the "
     "10-minute shuttle on consumption figures from other studies (indicative) [19, 23–25]."),
    ("The tracking gain and the cost hold up.",
     "A two-axis tracker at the site yields 36% more than fixed panels in the European Commission’s PVGIS model, "
     "against “up to 40%” claimed [17]. About €850,000 of EU recovery funds is consistent with the contract figures "
     "plus VAT [10, 26–28]."),
    ("Verdict: contradicted (high confidence).",
     "The headline claim, Europe’s first solar flowers, is contradicted by dated records; the bus-charging claim is "
     "not substantiated. Pending right of reply."),
]))
S += [Spacer(1, 4 * mm), VerdictMeter(4), Spacer(1, 3 * mm),
      tiles([("2016", RED, "a SmartFlower was already in service at an Austrian motorway rest area [13]"),
             ("15", GREEN, "SmartFlowers at Ta’ Xħajma; to the maker, “one of the largest installations in Europe”"),
             ("≈85 MWh", GREEN, "a year modelled for 15 units of 2.5 kWp with two-axis tracking; none metered or published"),
             ("2–3 h", ORANGE, "of the 10-minute shuttle a day is what that output equals (indicative); bus use unpublished")]),
      Spacer(1, 4 * mm),
      up_down("Documents from October 2025 showing that “of its kind” meant a feature no earlier European installation "
              "had (for example the number of units at one site, or offsetting bus charging), and that this was said: "
              "<i>Misleading</i>, since “these first solar flowers in Europe” would still mislead.",
              "Nothing: <i>Contradicted</i> is already the lowest rating. Metered output and charging data would settle "
              "the bus-charging part, not this verdict."),
      Spacer(1, 5 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What a solar flower is"),
          ("4", "Were they the first in Europe?"), ("5", "Do they power the buses?"),
          ("6", "Where the evidence points different ways"), ("7", "Testing the claim"),
          ("8", "Verdict and requests for evidence"), ("9", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The Government’s own press release (gov.mt) could not be read from our network. Three readable texts carry "
           "it, and the claim is assembled from them. Only words inside quotation marks in those texts are treated as the "
           "speakers’ own; the rest is the outlet’s report of the statement. The Maltese article is the fullest: its "
           "English version drops the words “first … in Europe” from the minister’s quote, while Lovin Malta’s "
           "English keeps them [1–3]."))
S.append(std_table([
    [C("What was said", cellh), C("Who, where", cellh), C("Our access", cellh)],
    [C("“Bl-installazzjoni ta’ dawn l-ewwel solar flowers fl-Ewropa, qed nuru kif Għawdex jista’ jkun ta’ eżempju "
       "fl-innovazzjoni sostenibbli.” In English: “With the installation of these first solar flowers in Europe, we "
       "are demonstrating how Gozo can be a model for sustainable innovation.”"),
     C("Camilleri, quoted; TVM News (Maltese) [1]; Lovin Malta’s English [2]"), C("Read in full")],
    [C("“… hija l-ewwel tax-xorta tagħha li qiegħda tintuża f’pajjiżna u li bħala ammont fl-istess żona hija t-tieni "
       "waħda fid-dinja …” (our translation: the first of its kind used in our country and, as a number in one "
       "place, the second in the world)."),
     C("Camilleri, quoted [1]; Lovin Malta renders it “first of its kind in Malta” [2]"), C("Read in full")],
    [C("“This energy will be used to supply electricity, electric buses which offer transport between Imġarr port "
       "and the Park &amp; Ride facility.”"), C("Camilleri, quoted; TVM News (English) [3]"), C("Read in full")],
    [C("The installation is “the first of its kind in Europe”; the energy will directly offset the electricity used "
       "to charge the Park and Ride bus fleet; each flower yields up to 40% more than traditional panels; about "
       "€850,000."), C("The statement, in the outlets’ words, not quoted [1–3]"), C("Read in full")],
    [C("“They are the first of their kind in Europe.” Funded through RRP C1-I5; €850,000."),
     C("European Commission project page, its own words [4]"), C("Read in full")],
    [C("Parliamentary Secretary Omar Farrugia: a solar system “unika fl-Ewropa” (“unique … in Europe”)."),
     C("Quoted [1, 2]"), C("Read in full")],
], [92 * mm, 50 * mm, 28 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("FAIRNESS NOTE", tag),
               P("The flowers exist, work and were paid for with EU recovery funds, as the Government said; Parliament "
                 "was told all fifteen were in working order [10] ◆. The minister’s own words also contain the narrower "
                 "and accurate-looking claim that this is a first for Malta. The Commission page repeats the "
                 "Government’s description; it does not test it. This check is about the words used, not about whether "
                 "the project was worth doing.", small)],
              bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Questions.</b> (A) Were these Europe’s first solar flowers, or the first installation of their kind, "
           "and what else could “first” mean? (B) How much electricity can fifteen flowers make, and how does that "
           "compare with what the Park and Ride buses use? (C) Is the stated tracking gain plausible? (D) What did the "
           "project cost and who paid?"))
S.append(P("<b>Evidence.</b> For (A), the manufacturer’s pages [5–8] and dated reports of earlier installations in "
           "Europe [11–16], with a search log in <i>literature/CC-032/notes.md</i>. For (B) and (C), the European "
           "Commission’s Photovoltaic Geographical Information System (PVGIS 5.3, satellite radiation 2005–2023) run for "
           "the site with two-axis tracking and with fixed panels [17]; the manufacturer’s data sheet [8, 9]; the "
           "Gozo Regional Development Authority (GRDA) and EU procurement records for the shuttle [19, 20]; road "
           "distances from OpenStreetMap [23]; and two peer-reviewed estimates of electric-bus consumption [24, 25] and "
           "one of tracking gains [18], read as abstracts. For (D), the reply to a parliamentary question as reported by "
           "Newsbook [10] ◆, the EU award notice we identify as this contract [26], the EU VAT table [27] and the "
           "Council decision on Malta’s recovery plan [28]. Inputs are in <i>data/cc-032/</i>; every figure is "
           "recomputed by <i>tools/cc-032-report/calc.py</i> (<i>checks.csv</i>)."))
S.append(P("<b>Grades.</b> Individual news reports and company pages are grade D, but the records of earlier "
           "installations are independent of one another, dated, and from three countries. PVGIS, EU procurement records, "
           "the Council decision and the GRDA are grade C. The tracker study [18] uses measured radiation across a "
           "latitude gradient (grade B); the bus-consumption figures are modelled for other routes and buses (grade C, "
           "indicative here). ◆ marks second-hand material. <b>Verdicts</b> follow the five-point scale in Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(70 * mm))
S.append(SectionHeading(3, "What a solar flower is"))
S.append(P("A SmartFlower is a free-standing photovoltaic unit with twelve petal-shaped panels that fan open at "
           "sunrise, follow the sun on two axes through the day and fold away at night or in strong wind [7–9]. The "
           "maker gives a nominal output of 2.5 kWp and 4,000–6,500 kWh a year per unit, depending on location, with "
           "an integrated inverter [8, 9]. It describes the product as manufactured in Austria; the company was founded "
           "there and bought by a Boston firm in 2018 [7]. The Commission page describes Gozo’s units in the same "
           "terms: they open at sunrise, follow the sun and close at sundown [4]."))
S.append(P("Tracking raises output because the panels face the sun for more of the day. A study of five tracker types "
           "at locations across Europe and Africa found dual-axis trackers collected 17.7% to 31.2% more solar energy "
           "than panels fixed at the best angle, the gain varying with latitude [18]. The maker and the Government both "
           "say “up to 40%” [3, 7]."))
S.append(P("The capacity of the Gozo units has not been published in anything we read. If they are the 2.5 kWp model "
           "the maker sells, the fifteen add up to 37.5 kWp; we use that figure below and say so each time."))

# ================================================================== 4
S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(4, "Were they the first in Europe?"))
S.append(KeepTogether([fig(FIG / "fig1_timeline.png"),
                       P("Figure 1. Dated records of SmartFlowers in Europe before the Gozo statement, and the maker’s "
                         "own description of Gozo’s installation afterwards [5, 11–13, 15]. Records listed in "
                         "<i>data/cc-032/european_records.csv</i>.", cap)]))
S.append(std_table([
    [C("Date", cellh), C("Where", cellh), C("What the record says", cellh), C("Source", cellh)],
    [C("Jun 2015"), C("Madrid, Spain"), C("Smartflower, “made in Austria”, presented and installed in Spain; 3,400–6,000 "
                                          "kWh a year depending on site"), C("energynews.es [11]")],
    [C("Jul 2016"), C("Vienna-based maker"), C("“Austria’s SmartFlower”; the company had sold over 1,000 units in Europe, "
                                               "Asia, the Middle East and elsewhere (its own figure)"), C("pv magazine [12]")],
    [C("Dec 2016"), C("Hinterbrühl rest area, A21, Austria"),
     C("Motorway operator ASFINAG puts a SmartFlower into service; it covers half of the rest area’s lighting "
       "electricity, about 3,550 of 7,000 kWh a year"), C("MeinBezirk.at [13]; IÖB [14]")],
    [C("Aug 2021"), C("Newbury, UK"), C("Vodafone erects a SmartFlower at its headquarters, made in Austria and installed "
                                        "by a UK distributor"), C("Newbury Today [15]")],
    [C("Undated"), C("UK, Jersey, Denmark, Spain"), C("Dealers list 17 UK and Jersey installations, some of two or three "
                                                      "units, and clients in Denmark, Spain and Scotland"), C("Dealer pages [16]")],
    [C("14 Nov 2025"), C("Ta’ Xħajma, Gozo"), C("Maker: the fifteen SmartFlowers are “one of the largest installations in "
                                                 "Europe”; its year review repeats this"), C("SmartFlower [5, 6]")],
], [20 * mm, 34 * mm, 84 * mm, 32 * mm]))
S.append(Spacer(1, 3 * mm))
S.append(P("Reading across the records", h2))
for t in ["• <b>As solar flowers, not the first.</b> The same product was in service in Austria nine years earlier, "
          "including at a motorway rest area run by the Austrian motorway operator ASFINAG, and in the UK four years "
          "earlier [13–15].",
          "• <b>As an installation of this size, not shown.</b> The maker calls it “one of the largest "
          "installations in Europe” [5]; it does not call it the largest. The "
          "maker’s English version of the minister’s quote reads “By installing these [SmartFlowers] in Europe”, with "
          "the word “first” replaced [5].",
          "• <b>As a first for Malta, plausible.</b> Parliament was told no other such installation exists in Malta "
          "[10] ◆, and our web search found none. The minister’s claim to be second in the world by number at one "
          "site was not tested.",
          "• <b>As a use, not unique.</b> Offsetting bus charging at a transport hub may be new; nothing we found shows "
          "an earlier European flower array charging buses. But the Government did not say that this was the "
          "novelty, and the 2016 Austrian unit already supplied part of a motorway rest area’s lighting."]:
    S.append(P(t, bul))

# ================================================================== 5
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(5, "Do they power the buses?"))
S.append(P("The minister said the energy “will be used to supply electricity, electric buses” running between Mġarr and "
           "the Park and Ride [3]; the statement said it would “directly offset” the electricity used to charge that "
           "fleet [2]. Neither gives an amount. Six electric buses owned by the Ministry for Gozo run the shuttle every "
           "10 minutes, operated by Malta Public Transport under negotiated contracts [19, 20]. The GRDA notes that "
           "uptake “remains very low” [19]. Since May 2026 the hub has also held a new depot where Gozo’s electric "
           "buses, now 29 in all, are charged during the night [21, 22]; Malta Public Transport says its electric buses "
           "charge “primarily overnight” [21]."))
S.append(KeepTogether([fig(FIG / "fig2_output.png"),
                       P("Figure 2. A: modelled output a day by month for 37.5 kWp at the Park and Ride, with two-axis "
                         "tracking and with fixed panels at the best angle (PVGIS 5.3, 14% system loss) [17]. B: the "
                         "hours of a 10-minute shuttle (8.5 km round trip [23]) that each month’s average day equals, "
                         "at 1.45–2.1 kWh per km, figures modelled for other buses and routes [24, 25]. Indicative "
                         "only: the Gozo buses’ consumption and hours are not published.", cap)]))
S.append(KeepTogether([std_table([
    [C("Indicator", cellh), C("Value", cellh), C("Source", cellh)],
    [C("Capacity of the 15 units"), C("Not published; <b>37.5 kWp</b> if 2.5 kWp each"), C("[8, 9]")],
    [C("Modelled output, two-axis tracking"), C("<b>85,121 kWh a year</b>; 5,675 per unit; 233 kWh a day on "
                                                "average (152 in December, 315 in July)"), C("[17], calculated")],
    [C("Maker’s range for 15 units"), C("60,000–97,500 kWh a year"), C("[8], calculated")],
    [C("Same capacity, fixed at the best angle (32°)"), C("62,341 kWh a year: tracking adds <b>36.5%</b>"),
     C("[17], calculated")],
    [C("Metered output of the flowers"), C("Not published"), C("Search log")],
    [C("Shuttle: buses, frequency, round trip"), C("6 buses, every 10 minutes, 8.5 km: about 51 km per hour of "
                                                   "service"), C("[19, 20, 23]")],
    [C("Shuttle buses’ model, battery, consumption, hours"), C("Not published"), C("Search log")],
    [C("Energy per hour of 10-minute service at 1.45–2.1 kWh/km"), C("74–107 kWh (indicative)"), C("[24, 25], calculated")],
    [C("Hours of that service the flowers’ average day equals"), C("<b>2.2–3.2 hours</b>; 1.4–2.1 in December "
                                                                   "(indicative)"), C("calculated")],
], [62 * mm, 82 * mm, 26 * mm]),
    P("All inputs in <i>data/cc-032/</i>; results in <i>checks.csv</i>.", cap)]))
S.append(P("Three things follow. First, the amount of charging the flowers cover cannot be calculated from public "
           "data: neither their output nor the buses’ consumption has been published, and Parliament was told that no "
           "technical report, feasibility study or value-for-money comparison was made [10] ◆. Second, on the only "
           "sourced figures we could find, the flowers’ average day matches roughly two to three hours of the 10-minute "
           "shuttle, less in winter; whether that is all or part of its charging depends on hours and consumption that "
           "are not public. Third, the flowers produce only in daylight. They can feed daytime charging or other loads "
           "at the hub directly, and offset night-time charging on a yearly balance through the grid, which is what the "
           "statement’s “offset” means; they cannot directly power buses charged overnight without storage, and none is "
           "mentioned. How they are wired is not published."))

# ================================================================== 6
S.append(CondPageBreak(85 * mm))
S.append(SectionHeading(6, "Where the evidence points different ways"))
S.append(contested(
    "Q1  Are they the first of their kind in Europe?", "NO, AS WORDED", MAROON,
    "Gozo’s array of fifteen is large: the maker calls it one of Europe’s largest [5]. Using flowers to offset bus "
    "charging at a transport hub may be new; we found no earlier European example. It is the first in Malta as far as "
    "we could find [10] ◆.",
    "The same product was installed in Spain (2015), Austria (2016) and the UK (2021), among others [11–16]. The maker "
    "does not call Gozo’s the first, or the largest [5, 6]. The minister said “these first solar flowers in Europe” "
    "[1, 2], and the Commission page repeats it [4].",
    "<b>For this claim:</b> as worded it is contradicted. A narrower claim (first in Malta, or among the largest in "
    "Europe) would have been supported by what we found."))
S.append(contested(
    "Q2  Do the flowers power the buses’ charging?", "NOT SHOWN", ORANGE,
    "Modelled output is about 85 MWh a year [17], of the same order as a few hours a day of the shuttle’s likely use "
    "[23–25]. The statement says “offset”, which a yearly balance through the grid can deliver.",
    "No capacity, metered output, bus consumption or wiring has been published, and no feasibility study was made "
    "[10] ◆. The new depot at the hub charges buses during the night [22], when the flowers are closed [4].",
    "<b>For this claim:</b> a part of the charging can be offset; how much has not been shown."))
S.append(contested(
    "Q3  Do they yield “up to 40%” more than fixed panels?", "PLAUSIBLE", LG,
    "PVGIS models 36.5% more for two-axis tracking than for fixed panels at the best angle at Ta’ Xħajma [17]. Against "
    "panels at a poorer angle the gain would be larger.",
    "Studies across Europe and Africa find 18–31% [18]. No measurements of these units are published, and the "
    "petal design may not behave like an ideal tracker.",
    "<b>For this claim:</b> close to the modelled gain at this site; “up to” is the maker’s figure.",
    label_a="EVIDENCE FOR THE CLAIM", label_b="EVIDENCE OF A SMALLER GAIN"))

# ================================================================== 7
S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(7, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> Fifteen solar flowers were installed at the Gozo Multi-Modal Hub, Ta’ Xħajma"),
     C("Statement [1–3]; Commission [4]"),
     C("The maker reports fifteen SmartFlowers at the hub [5]; Parliament was told all were working [10] ◆."),
     verd("ACCURATE", GREENC)],
    [C("<b>B.</b> “The first of its kind in Europe”; “these first solar flowers in Europe”"),
     C("Statement [1–3]; Camilleri, quoted [1, 2]; Commission [4]"),
     C("SmartFlowers, an Austrian product, were in service in Spain (2015), Austria (2016) and the UK (2021) [11–15]; "
       "the maker calls Gozo’s “one of the largest installations in Europe” [5]."), verd("CONTRADICTED", MAROON)],
    [C("<b>C.</b> The first of its kind used in Malta; second in the world by number at one site"),
     C("Camilleri, quoted [1, 2]"),
     C("First in Malta: consistent with the reply to Parliament [10] ◆ and our search. Second in the world: not "
       "tested."), verd("NOT CONTRADICTED", GREY)],
    [C("<b>D.</b> The energy will supply, or offset the charging of, the Park and Ride electric buses"),
     C("Camilleri, quoted [3]; statement [2]"),
     C("No capacity, metered output or bus use published; no feasibility study [10] ◆. Modelled output equals about "
       "2–3 hours a day of the shuttle (indicative) [17, 23–25]."), verd("NOT SUBSTANTIATED", ORANGE)],
    [C("<b>E.</b> Each flower yields up to 40% more energy than traditional panels"),
     C("Statement [3]; Commission [4]"),
     C("PVGIS: 36.5% more than fixed panels at the best angle at the site [17]; studies 18–31% elsewhere [18]. Not "
       "measured here."), verd("LARGELY ACCURATE", LG)],
    [C("<b>F.</b> About €850,000, funded by the EU recovery plan (C1-I5)"),
     C("Statement [1, 3]; Commission [4]"),
     C("Parliament was told €699,612 excluding VAT [10] ◆; the likely award, €718,830, is €848,219 with VAT [26, 27]; "
       "C1-I5 funds solar panels in public spaces [28]."), verd("CONSISTENT", GREENC)],
], [40 * mm, 30 * mm, 70 * mm, 30 * mm], valign="MIDDLE"))

# ================================================================== 8
S += [Spacer(1, 6 * mm), SectionHeading(8, "Verdict and requests for evidence"),
      verdict_box("Contradicted", "The claim that Gozo’s fifteen solar flowers are Europe’s first is contradicted by dated "
                  "records of the same product elsewhere in Europe since 2015. Confidence: high."),
      Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) The headline claim, made in the minister’s own words, in the statement and on the "
           "Commission’s page, is that these are the first solar flowers, or the first installation of their kind, in "
           "Europe. (2) The units are SmartFlowers, and independent, dated records show the same Austrian product in "
           "service in Spain, Austria and the UK years earlier, including a 2016 pilot by an Austrian motorway "
           "operator. (3) The manufacturer itself calls Gozo’s installation one of the largest in Europe, not the "
           "first. The evidence points against the claim as worded, so the verdict is <i>Contradicted</i>. The second "
           "claim, that the energy powers or offsets the buses’ charging, is <i>Not substantiated</i>: no figures were "
           "published to show how much."))
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
                 "days). The European Commission’s project page repeats the claim and may be offered the same. "
                 "Responses will be appended and the verdict revisited. A <i>Contradicted</i> verdict is not circulated "
                 "elsewhere before that deadline passes.", small)],
              bg=AMBER_PALE, bar=AMBER)]

# ================================================================== 9
S += [Spacer(1, 6 * mm), CondPageBreak(70 * mm), SectionHeading(9, "Limitations")]
for l in ["The Government’s press release on gov.mt and the parliamentary answers on parlament.mt could not be read "
          "from our network; we used TVM News, Lovin Malta and Newsbook’s report of the answers ◆.",
          "We did not establish which European SmartFlower was the first, only that several preceded Gozo’s. The "
          "records of earlier installations are news reports and dealer pages; we did not visit the sites.",
          "The capacity of the Gozo units is assumed from the maker’s current 2.5 kWp model. PVGIS models an ideal "
          "two-axis tracker with a default 14% loss; the petal design, shading at the hub and downtime are not modelled.",
          "The bus-consumption figures (1.45–2.1 kWh per km) were modelled for other buses and routes and read as "
          "abstracts; the route length comes from car routing on OpenStreetMap. Figure 2B is an order of magnitude, "
          "not an estimate of the share covered.",
          "We identify EU award notice 742398-2024 as this contract from its subject, buyer, date and value; the "
          "notice names no site or product."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "TVM News (21 October 2025). Installati l-ewwel solar flowers tax-xorta tagħhom fl-Ewropa fil-Gozo Multi-Modal "
          "Hub f’Ta’ Xħajma (Maltese).",
     "https://tvmnews.mt/news/installati-l-ewwel-solar-flowers-tax-xorta-taghhom-fl-ewropa-fil-gozo-multi-modal-hub-fta-xhajma/"),
    ("2", "Lovin Malta (21 October 2025). Gozo Leads The Way In Europe With First-Ever ‘Solar Flowers’ At Ta’ Xħajma "
          "Multi-Modal Hub.",
     "https://lovinmalta.com/malta/gozo-leads-the-way-in-europe-with-first-ever-solar-flowers-at-ta-xhajma-multi-modal-hub/"),
    ("3", "TVM News (21 October 2025). First solar flowers in Europe installed at the Gozo Multi-Modal Hub in Ta’ "
          "Xħajma (English).",
     "https://tvmnews.mt/en/news/first-solar-flowers-in-europe-installed-at-the-gozo-multi-modal-hub-in-ta-xhajma/"),
    ("4", "European Commission, Reforms and Investments. 15 solar flowers installed in Gozo for electricity generation, "
          "the first project of its kind in Europe (project page, RRP C1-I5; read 6 October 2026).",
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
    ("13", "MeinBezirk.at, Mödling (7 December 2016). Grüner Strom für den Rastplatz Hinterbrühl auf der A 21.",
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
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 2 * mm)]
S += revision_log([
    ("1.0", "6 Oct 2026", "First issue. Pending right of reply (Ministry for Gozo and Planning; Public Works Department)."),
])

build_report(Report(
    number="032", out=str(FIG / "report.pdf"), kicker="Renewables, Gozo",
    title_lines=["Europe’s first", "solar flowers?"],
    subtitle_lines=["Testing the Government’s claims about Gozo’s fifteen", "solar flowers against the record"],
    quote_lines=["“With the installation of these first solar flowers", "in Europe, we are demonstrating how Gozo can be",
                 "a model for sustainable innovation.”"], quote_size=15,
    attribution="Clint Camilleri, Minister for Gozo and Planning, 21 October 2025.",
    context="Lovin Malta’s English; the Maltese original is in TVM News. Fifteen units at Ta’ Xħajma, Gozo.",
    verdict="Contradicted", verdict_note="Solar flowers were in service elsewhere in Europe from 2015",
    footer_lines=["Version 1.0  ·  6 October 2026",
                  "Status: draft, pending right of reply (Ministry for Gozo and Planning)",
                  "Prepared from public sources, EU records and the PVGIS model.",
                  "Repository: github.com/leandergrech/Mizien"],
    running_head="Gozo’s solar flowers", version="1.0", date="6 October 2026",
    pdf_title="Europe's first solar flowers? Claim Check 032",
    pdf_subject="Tests the Government's claim that Gozo's 15 solar flowers are Europe's first and power its electric buses",
    story=S))
