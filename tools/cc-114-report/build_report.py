"""Claim Check 114 report. Run fetch.py, calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
BRICK = VERDICT_COLS[3]     # the Misleading colour
MAROON = VERDICT_COLS[4]    # the Contradicted colour
S = []

# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("On 26 January 2026 a Nationalist Party (PN) release signed by Eve Borg Bonello said that <b>“Malta is the "
        "only EU Member State which, instead of reducing, increased the intensity of greenhouse gas emissions from "
        "2013 to date”</b> (+17%, EU −34%), that Malta now pollutes more for every euro of its economy, and that this "
        "is “the direct result” of the Government’s lack of ambition, above all on renewables [1] (our translation). "
        "We tested it against Eurostat’s own tables.", lead)]
S.append(key_points([
    ("The headline figure is Eurostat’s, quoted correctly.",
     "Eurostat: “Only Malta (+17%) saw its emissions intensity increase since 2013”, EU −34% [3, 4]. Revised data "
     "(August 2026) give +14.3%, still the only rise of the 27 [6]."),
    ("72% of the emissions in Malta’s 2024 figure are airline fuel bought abroad.",
     "The indicator counts Malta-resident firms’ emissions wherever they occur [7]. Air transport rose from 0.30 to "
     "4.73 Mt CO₂e, 2013–2024, almost all of it fuel bought abroad [6, 8]."),
    ("Without air transport, or on the territorial inventory, intensity fell sharply.",
     "−64% and −61%: both the EU’s second-largest fall (EU −35% and −36%) [6, 9]."),
    ("The cause the release gives does not fit the data.",
     "Electricity-supply emissions, where renewables act, fell 56% [6]. The 10.7% is Malta’s renewable share of "
     "electricity, set against the EU’s overall share; Estonia, Ireland and Finland cut intensity, not emissions [6, 10]."),
    ("Verdict: misleading (high confidence).",
     "The statistic is right, but without its driver the release gives an inaccurate impression: that Malta’s economy "
     "pollutes more per euro because of weak renewables policy. Pending right of reply."),
]))
S += [Spacer(1, 4 * mm), VerdictMeter(3), Spacer(1, 3 * mm),
      tiles([("+14%", RED, "Eurostat’s indicator for Malta, 2013–2024 (+17% in January; EU −34%)"),
             ("72%", RED, "of Malta’s 2024 figure is airline fuel bought abroad (11% in 2013)"),
             ("−64%", GREEN, "the same without air transport: the EU’s second-largest fall"),
             ("−56%", GREEN, "emissions from electricity supply, 2013–2024")]),
      Spacer(1, 4 * mm),
      up_down("Revised data or a source showing that the rise comes from activities in Malta that renewable energy "
              "could reduce (for example emissions reallocated from air transport to electricity or other domestic "
              "activities): <i>Largely supported</i>.",
              "Reported 2024 data replacing Eurostat’s estimate and showing no rise since 2013 (to 2023 the "
              "indicator fell 8.3%): the headline itself would then be wrong, <i>Contradicted</i>."),
      Spacer(1, 5 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What Eurostat’s indicator counts"),
          ("4", "What the data show"), ("5", "Where the evidence points different ways"), ("6", "Testing the claim"),
          ("7", "Verdict and requests for evidence"), ("8", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The statement is a PN press release in Maltese, published on the party’s website on 26 January 2026 and "
           "signed by Eve Borg Bonello as Shadow Minister for Climate Change and Public Cleanliness [1]. Newsbook "
           "reported it in English the same day, with some sentences in quotation marks and the figures in its own "
           "words [2]. We rate the release. Quotations below are our translation of the Maltese, checked against "
           "Newsbook’s English where it has one; the original sentences are in <i>literature/CC-114/primary-source.md</i>."))
S.append(std_table([
    [C("What was said (our translation)", cellh), C("Where", cellh), C("Our access", cellh)],
    [C("“Malta is the only EU Member State which, instead of reducing, increased the intensity of greenhouse gas "
       "emissions from 2013 to date. Malta in fact increased these emissions by 17%, when the average intensity of "
       "these emissions in all EU Member States fell by 34%.”"), C("Release [1]; Newsbook quotes the first sentence "
                                                                    "and paraphrases the figures [2]"),
     C("Read in full")],
    [C("Eurostat’s figures, “published in recent days”, show other countries succeeding “in the fight against air "
       "pollution”, among them “Estonia, which reduced emissions by 64%, Ireland by 50% and Finland by 44%”."),
     C("Release [1]"), C("Read in full")],
    [C("“In simple words, we are not polluting more simply because the economy grew; today, for every euro we put "
       "into our economy, we are polluting more than we were polluting in 2013.”"), C("Release [1]; quoted in "
                                                                                     "English by Newsbook [2]"),
     C("Read in full")],
    [C("“This is the direct result of a lack of ambition on the part of the Maltese Government on several fronts. "
       "Among them, the clear lack of ambition to seriously increase the use of renewable energy.”"),
     C("Release [1]; subtitle says the same of renewables"), C("Read in full")],
    [C("“In 2024 our country generated only 10.7% of its energy from renewable sources … the European average is a "
       "little over 25% … third from last.”"), C("Release [1]"), C("Read in full")],
    [C("The release’s image: Eurostat’s map of the change in emissions intensity of gross value added, 2013–2024 "
       "(Malta 16.6)."), C("Release [1]; Eurostat [3, 4]"), C("Read in full")],
], [96 * mm, 46 * mm, 28 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("FAIRNESS NOTE", tag),
               P("The PN reproduced Eurostat’s headline and definition accurately, and Eurostat’s own news item "
                 "gives no explanation of Malta’s figure either [3]. The questions are what the figure measures and "
                 "whether the release’s reading of it holds. This is an opposition statement, held to the same "
                 "standard and the same data as the Government’s statement on the same theme (Claim Check 025: "
                 "emissions per unit of GDP down more than 80% since 2005) [13]. Newsbook added, in its own words, "
                 "that Malta leads the EU on cutting emissions per unit of GDP since 2005; that is not the PN’s "
                 "statement and is not rated here.", small)],
              bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Questions.</b> (A) Does Eurostat show Malta as the only EU Member State whose emissions intensity rose "
           "since 2013, by 17% against −34%? (B) Does that hold in the latest data and for other start and end years? "
           "(C) What drives Malta’s figure? (D) Do other measures of emissions per unit of output agree? (E) Does the "
           "cause the release gives fit the data? (F) Are the release’s other figures right?"))
S.append(P("<b>Evidence.</b> Eurostat’s news item and its map [3, 4]; its Statistics Explained article on greenhouse "
           "gas emission accounts [5]; the air emissions accounts by activity, the intensity table and the table "
           "bridging the accounts to the national inventory [6]; Eurostat’s and the National Statistics Office’s "
           "(NSO) metadata [7, 8]; the territorial inventory, GDP, gross value added and population [9]; renewable "
           "shares [10]; and two peer-reviewed papers on accounting principles and decoupling [11, 12]. All data "
           "were retrieved on 6 October 2026 into <i>data/cc-114/</i> with Eurostat’s status flags, and every figure "
           "here is recomputed by <i>tools/cc-114-report/calc.py</i> (<i>data/cc-114/checks.csv</i>)."))
S.append(P("<b>Grades.</b> Eurostat’s and the NSO’s statistics and metadata are official statistics, grade C. The two "
           "papers are a methodological analysis and a systematic review, read as abstracts, grade C. The release "
           "and the news report are the claim, not evidence. <b>Verdicts</b> follow the five-point scale in "
           "Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(80 * mm))
S.append(SectionHeading(3, "What Eurostat’s indicator counts"))
S.append(P("Eurostat’s greenhouse gas emissions intensity is the emissions of an economy’s production units, in CO₂ "
           "equivalents, per euro of gross value added in chain-linked 2020 prices; households are left out because "
           "they produce no value added [3, 5]. The emissions come from the <b>air emissions accounts</b>, which follow "
           "the national accounts and so the <b>residence principle</b>: they record “emissions arising from the "
           "activities of all resident units … regardless of where these emissions actually occur geographically” "
           "[7]. The national inventory under the UN climate convention, on which EU targets are set, counts what is "
           "emitted on the territory and keeps international aviation and shipping as memo items [9]; Eurostat "
           "bridges the two in a separate table [6]. A peer-reviewed comparison finds the gap between the two "
           "principles “high for many countries” and growing [11]."))
S.append(P("An airline resident in Malta is counted in Malta’s accounts for the fuel it burns on any route, and its "
           "value added is part of Malta’s GDP: the indicator is consistent, but it does not measure emissions in "
           "Malta. Eurostat’s article notes that in Denmark, Luxembourg and Malta transport is the key emitting "
           "activity in these accounts, as transport companies’ emissions “are allocated to the country of "
           "residence” [5]."))
S.append(P("<b>Malta’s air transport.</b> Eurostat’s bridging table puts emissions from fuel bought abroad by "
           "Malta-resident air transport firms at 0.30 Mt CO₂e in 2013, 0.91 Mt in 2019, 1.59 Mt in 2022, 3.11 Mt in "
           "2023 and 4.73 Mt in 2024 [6]: from 0.4% to 4.4% of all such emissions by EU residents, for an economy "
           "with 0.13% of the EU’s value added. The NSO attributes the 2023 jump to “an increase in international "
           "aviation activity, primarily due to the activity of airlines which started operating during 2023”; its "
           "source is the OECD’s residence-based aviation data, with charter flights for 2013–2018 estimated by the "
           "NSO and revised in February 2026 [8]. Neither names the airlines, and we do not."))
S.append(P("<b>What 2024 is.</b> Eurostat estimates the latest year itself [7]: Malta’s 2024 values carry the flag "
           "“i”, imputed. Eurostat also warns that “a multitude of factors may drive greenhouse gas emissions "
           "intensity, with improving environmental performance and decarbonisation policies being only one of "
           "them” [5]. A falling intensity alongside growth is what the literature calls relative decoupling [12]."))

# ================================================================== 4
S.append(KeepTogether([SectionHeading(4, "What the data show"),
    P("The same economy gives opposite signs depending on what is counted, from when, and at which prices. Figure 1 "
      "sets the two main measures side by side for the 27; Figure 2 shows what lies inside Malta’s figure."),
    std_table([
    [C("Measure", cellh), C("Counts", cellh), C("Period", cellh), C("Malta", cellh), C("EU-27", cellh),
     C("Malta among 27", cellh)],
    [C("Eurostat’s indicator, January release"), C("Residents / GVA"), C("2013–24"), C("<b>+16.6%</b>"),
     C("−34.0%"), C("only rise")],
    [C("Same, data of August 2026"), C("Residents / GVA"), C("2013–24"), C("<b>+14.3%</b> (est.)"),
     C("−34.0%"), C("only rise")],
    [C("Same, ending 2023"), C("Residents / GVA"), C("2013–23"), C("−8.3%"), C("−32.4%"), C("no rise")],
    [C("Same, current prices"), C("Residents / GVA"), C("2013–24"), C("−20.3%"), C("−49.3%"), C("no rise")],
    [C("Same, without air transport"), C("Residents / GVA"), C("2013–24"), C("<b>−64.0%</b>"), C("−35.2%"),
     C("2nd-largest fall")],
    [C("Territorial inventory per € of GDP"), C("Territory / GDP"), C("2013–24"), C("<b>−61.3%</b>"), C("−35.5%"),
     C("2nd-largest fall")],
    [C("Same, from 2005 (CC-025)"), C("Territory / GDP"), C("2005–24"), C("−72.2%"), C("−47.9%"),
     C("")],
    [C("Same, current prices (CC-025’s “80%”)"), C("Territory / GDP"), C("2005–24"),
     C("−83.8%"), C("−64.7%"), C("")],
    [C("Territorial inventory per person"), C("Territory / person"), C("2013–24"), C("−42.6%"), C("−24.2%"),
     C("3rd-largest fall")],
    [C("Residents incl. households, per person"), C("Residents / person"), C("2013–24"), C("+69.2%"), C("−21.2%"),
     C("largest of 5 rises")],
], [62 * mm, 28 * mm, 15 * mm, 23 * mm, 16 * mm, 26 * mm]),
    P("Sources [4, 6, 9, 13]; values in <i>data/cc-114/checks.csv</i>, ranks in <i>ranking_2013_2024.csv</i>. "
      "“Without air transport” removes its emissions only; removing transport from both sides gives −66.3%.", cap)]))
S.append(KeepTogether([fig(FIG / "fig1_ranking.png", width=CW * 0.92),
                       P("Figure 1. Change in emissions per euro of output, 2013–2024, for the 27 Member States, on "
                         "Eurostat’s published indicator (filled; resident production units per euro of gross value "
                         "added) and on the territorial inventory per euro of GDP (hollow; excluding land use and "
                         "international bunkers), both in chain-linked volumes [6, 9]. Sorted by Eurostat’s indicator. "
                         "Malta’s 2024 value in the accounts is a Eurostat estimate.", cap)]))
S.append(KeepTogether([fig(FIG / "fig2_malta.png"),
                       P("Figure 2. Malta. Panel A: emissions of resident production units by activity, with the "
                         "territorial inventory for comparison (Mt CO₂e). Panel B: Eurostat’s indicator, the same "
                         "without air-transport emissions, and the territorial inventory per euro of GDP, all indexed "
                         "to 2013 = 100. 2024 is a Eurostat estimate (hatched, shaded) [6, 9].", cap)]))
RA = [P("Reading across the data", h2)]
for t in ["• <b>Both parties’ figures are real; they count different things.</b> The Government’s COP30 statement "
          "(Claim Check 025) used the territorial inventory since 2005 and found a fall of more than 80% at current "
          "prices (−72% in volumes); the PN used Eurostat’s residence-based indicator since 2013 and found a rise. "
          "On the territorial basis Malta’s fall since 2013 is the EU’s second largest, after Estonia’s.",
          "• <b>One activity explains the whole rise.</b> Emissions of Malta’s resident production units went from "
          "2.78 to 6.59 Mt CO₂e while real value added rose 108.5%. Air transport added 4.43 Mt, 116% of the net "
          "increase: everything else fell, taken together. Electricity, gas and steam fell from 1.70 to 0.74 Mt "
          "(−56%); the remaining activities rose from 0.59 to 0.86 Mt, less than half as fast as output.",
          "• <b>The rise is recent.</b> The indicator fell 40% from 2013 to 2016 and was still 39% below 2013 in "
          "2021. It rose 63% from 2022 to 2024, the years of the airline growth the NSO describes [8].",
          "• <b>“Only Malta” rests on the 2024 estimate.</b> With 2013 as the base, Malta is the only riser for the "
          "end year 2024 and for no other; to 2023, the last year Malta reported, it fell 8.3% and no Member State "
          "rose. With 2024 as the end year, Malta is the only riser for every base year from 2013 to 2019, but fell "
          "from 2008–2012 (−9.0% since 2008).",
          "• <b>The January and August figures differ only for Malta.</b> Malta moved from +16.6% to +14.3%; no other "
          "country moved by more than 0.7 points. This coincides with the NSO’s February 2026 revision of 2013–2018 "
          "air transport [8]."]:
    RA.append(P(t, bul))
S += [KeepTogether(RA[:2])] + RA[2:]

# ================================================================== 5
S.append(CondPageBreak(85 * mm))
S.append(SectionHeading(5, "Where the evidence points different ways"))
S.append(contested(
    "Q1  Is Malta the only Member State whose intensity rose since 2013?", "YES, ON EUROSTAT’S INDICATOR", GREEN,
    "Eurostat’s news item and map say so: +16.6%, the only rise, EU −34.0% [3, 4]. The revised data of August 2026 "
    "give +14.3%, still the only rise [6].",
    "Only with 2024 as the end year, and Malta’s 2024 value is a Eurostat estimate. To 2023 the indicator fell 8.3% "
    "and no Member State rose. On the territorial inventory Malta’s fall is the EU’s second largest [6, 9].",
    "<b>For this claim:</b> accurate as Eurostat’s published statistic; the release rightly says it is Eurostat’s."))
S.append(contested(
    "Q2  Does Malta now pollute more per euro than in 2013?", "ONLY BY COUNTING AIRLINES ABROAD", ORANGE,
    "Malta-resident firms emit 14% more per euro of value added than in 2013 [6]. Their value added is in Malta’s "
    "GDP, so counting their emissions is consistent, as Eurostat’s accounts intend [5, 7].",
    "72% of the 2024 figure is fuel bought abroad by resident air transport firms [6]. Without air "
    "transport the indicator fell 64%; the territorial inventory per euro of GDP fell 61% [6, 9].",
    "<b>For this claim:</b> true of resident firms as the accounts count them, not of emissions in Malta; the "
    "release presents it as the second without saying it is the first."))
S.append(contested(
    "Q3  Is the rise the result of weak renewables ambition?", "NOT BORNE OUT", RED,
    "Malta’s renewable shares are among the lowest in the EU: 10.7% of electricity in 2024, the lowest of the 27, and "
    "17.2% of all energy, fourth from last [10].",
    "Emissions from electricity, gas and steam supply fell 56% since 2013 [6]. The whole net rise is air transport, "
    "fuel bought abroad, which renewable power in Malta does not displace. Eurostat cautions that many factors "
    "besides policy drive intensity [5].",
    "<b>For this claim:</b> the release names a cause the sector data do not show. It speaks of “several fronts” but "
    "names only renewables; unnamed causes cannot be tested."))

# ================================================================== 6
S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(6, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> Malta is the only EU Member State whose greenhouse gas emissions intensity rose since 2013"),
     C("Eurostat’s news item and map say so [3, 4]; still true in the August 2026 data, but only with 2024, a Eurostat "
       "estimate, as end year (to 2023: −8.3%, no riser) [6]."), verd("ACCURATE", GREENC)],
    [C("<b>B.</b> Malta +17%, EU average −34%"),
     C("Matches the January release (+16.6%, −34.0%); revised to +14.3% in August 2026. The release’s “these emissions” "
       "means the intensity; the −34% is the EU aggregate, not a mean of countries (−32.4%) [3, 4, 6]."), verd("ACCURATE", GREENC)],
    [C("<b>C.</b> Estonia reduced emissions by 64%, Ireland by 50%, Finland by 44%"),
     C("These are the intensity changes. Their emissions changed by −55%, +14% (Ireland’s rose) and −38% [5, 6]."),
     verd("MISLABELLED", AMBER)],
    [C("<b>D.</b> For every euro put into the economy, Malta pollutes more than in 2013"),
     C("True only as the accounts count resident firms: 72% of Malta’s 2024 figure is airline fuel bought abroad; "
       "without it −64%; territorial inventory per € of GDP −61%, the EU’s second-largest fall [6, 9]."),
     verd("MISLEADING", BRICK)],
    [C("<b>E.</b> The rise is the direct result of a lack of ambition, notably on renewable energy"),
     C("Electricity-supply emissions fell 56% since 2013; the net rise is all air-transport fuel bought abroad, which "
       "renewable power in Malta does not displace. No other cause is named [1, 6]."), verd("CONTRADICTED", MAROON)],
    [C("<b>F.</b> 10.7% renewables in 2024 against an EU average of just over 25%, third from last"),
     C("10.7% is Malta’s electricity share (lowest in the EU; EU 47.5%); 25.2% is the EU’s overall share. Malta’s "
       "overall share is 17.2%, fourth from last [10]. Malta is near the bottom either way."),
     verd("MIXED MEASURES", AMBER)],
], [50 * mm, 90 * mm, 30 * mm], valign="MIDDLE"))

# ================================================================== 7
S += [Spacer(1, 6 * mm), CondPageBreak(90 * mm), SectionHeading(7, "Verdict and requests for evidence"),
      verdict_box("Misleading", "Eurostat’s figure is quoted correctly, but the release omits that the whole rise is "
                  "airline fuel bought abroad and blames a cause the data do not show. Confidence: high."),
      Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) The central statistic is Eurostat’s and is quoted correctly: Malta is the only Member "
           "State whose indicator rose from 2013 to 2024. (2) The release then reads it as Malta polluting more for "
           "every euro of its economy, as the direct result of the Government’s lack of ambition on renewable energy. "
           "(3) Eurostat’s own tables, which the release does not mention, show that the rise is entirely air transport, "
           "almost all of it fuel bought abroad by airlines resident in Malta; that without it the indicator fell "
           "64%; that the territorial inventory per euro of GDP fell 61%, the EU’s second-largest fall; and that "
           "emissions from electricity supply fell 56%. These omitted facts are material: they reverse the sign of "
           "the trend and contradict the cause given. The individual figures are defensible but the overall "
           "impression is inaccurate, which is the scale’s definition of <i>Misleading</i>. The evidence that can "
           "be shown is listed in the claim record (Eurostat tables [6, 9, 10] and the NSO’s metadata [8])."))
S.append(P("<b>Why not Contradicted or Largely supported.</b> The headline statistic is true, so the claim is not "
           "contradicted. The omission is not a minor caveat: it changes what the figure means and undercuts the "
           "cause the release draws from it. <b>Why high confidence.</b> Four independent lines agree: emissions by "
           "activity, the bridging table, the NSO’s description of its data, and the territorial inventory. The one "
           "soft point, the 2024 estimate, bears on the headline, which we rate accurate, not on the omission."))
S.append(P("<b>Consistency with other checks.</b> Claim Check 026 rated a news report of a figure from the same "
           "accounts (Malta’s emissions up an estimated 169% since 2015, the EU’s largest rise) <i>Largely "
           "supported</i>: it gave Eurostat’s estimate as such and drew no conclusion from it [15]. This release goes "
           "further, reading the figure as more pollution per euro and naming a cause the data contradict. Claim "
           "Check 025 rated the Government’s “more than 80%” per unit of GDP <i>Largely supported</i>, its omission "
           "(−72% in volumes) being one of degree; Claim Check 003 rated a per-person figure <i>Misleading</i> for "
           "leaving out a projection that changed the picture [13, 14]."))
S.append(P("<b>What this verdict does not say.</b> It does not say Malta’s renewable shares are adequate (its "
           "electricity share is the EU’s lowest), that aviation emissions do not matter, or that anyone acted in "
           "bad faith. A statement the data support would read: <i>“On Eurostat’s residence-based measure Malta’s "
           "emissions intensity rose 17% since 2013 (14% in revised data), the only rise in the EU, because emissions of airlines based in "
           "Malta, mostly from fuel bought abroad, rose fifteen-fold; Malta’s territorial emissions per euro fell "
           "61%.”</i>"))
S.append(KeepTogether([P("Evidence we are asking for", h2), requests_list([
    "From the PN: whether the release took account of Eurostat’s breakdown by activity and its bridging table, and "
    "which other “fronts” it had in mind besides renewable energy.",
    "From the PN: the source of the 10.7% and of “third from last” (Eurostat gives 10.7% for electricity; Malta is "
    "fourth from last overall).",
    "From the NSO: which resident airline operations drive the air-transport series from 2019, and how fuel bought "
    "abroad is estimated from the OECD data.",
    "From the NSO and Eurostat: when Malta’s reported 2024 accounts will replace Eurostat’s estimate.",
])]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag),
               P("A right of reply will be sought from the Nationalist Party before this check is circulated beyond "
                 "Miżien’s site, with a fixed deadline (suggested 14 days). Its response will be appended and the "
                 "verdict revisited.", small)],
              bg=AMBER_PALE, bar=AMBER)]

# ================================================================== 8
S += [Spacer(1, 6 * mm), CondPageBreak(70 * mm), SectionHeading(8, "Limitations")]
for l in ["Malta’s 2024 values in the air emissions accounts are Eurostat estimates (flag i); Malta reported to 2023. "
          "The rise since 2013 depends on that estimate and may be revised.",
          "Malta’s air-transport series comes from the OECD’s residence-based aviation data with NSO additions for "
          "charter flights before 2019 [8]; a change of source between years could affect comparisons with 2013.",
          "We did not identify the airlines or read company filings. The value added of air transport is not "
          "published for 2013 and is negative in volumes for 2022–2024, so “without air transport” removes "
          "emissions only; removing the whole transport section from both sides gives a similar result (−66.3%).",
          "The translation of the Maltese release is ours. The page was modified on 24 April 2026 (its image is filed "
          "under that month); we found no January copy, but Newsbook’s quotes of 26 January match the text.",
          "The two papers were read as abstracts. MaltaToday’s report of the statement was not readable from our "
          "network and was not used."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Partit Nazzjonalista (26 January 2026, modified 24 April 2026). Malta l-uniku Stat Membru tal-UE li żied "
          "l-intensità tal-emissjonijiet tiegħu mill-2013 ’l hawn. Press release signed by Eve Borg Bonello, Shadow "
          "Minister for Climate Change and Public Cleanliness (Maltese).",
     "https://pn.org.mt/press-releases/malta-l-uniku-stat-membru-tal-ue-li-zied-l-intenstita-tal-emissjonijiet-tieghu-mill-2013-l-hawn/"),
    ("2", "Balzan J. (26 January 2026). PN accuses government of climate ‘apathy’ as emissions intensity rises. "
          "Newsbook.",
     "https://newsbook.com.mt/en/pn-accuses-government-of-climate-apathy-as-emissions-intensity-rises/"),
    ("3", "Eurostat (23 January 2026). 2024 EU greenhouse gas emissions: -20% since 2013. News item. Its being the "
          "release’s source is our identification (dates, figures, map and definition match).",
     "https://ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-20260123-1"),
    ("4", "Eurostat (January 2026). Greenhouse gas emissions intensity of gross value added, 2013–2024 (map in [3]; "
          "data block dated 20 January 2026, transcribed by script to data/cc-114/eurostat_map_jan2026.csv).",
     "https://ec.europa.eu/eurostat/documents/4187653/22762673/greenhouse-gas-emissions-intensity-2013-2024.html/98651795-bcd1-3b5a-b273-7da9727ee5f3"),
    ("5", "Eurostat (June 2026). Greenhouse gas emission accounts. Statistics Explained (data extracted June 2026). "
          "Open access, CC BY 4.0; copy in literature/CC-114/open-access/.",
     "https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Greenhouse_gas_emission_accounts"),
    ("6", "Eurostat. Air emissions accounts: intensities (env_ac_aeint_r2), emissions by NACE activity "
          "(env_ac_ainah_r2) and bridging to inventory totals (env_ac_aibrid_r2); updated 7 August 2026, retrieved "
          "6 October 2026.", "https://ec.europa.eu/eurostat/databrowser/view/env_ac_aeint_r2/default/table"),
    ("7", "Eurostat. Air emissions accounts by NACE Rev. 2 activity: reference metadata (ESMS).",
     "https://ec.europa.eu/eurostat/cache/metadata/en/env_ac_ainah_r2_sims.htm"),
    ("8", "National Statistics Office, Malta (11 February 2026). Air emissions accounts: national reference "
          "metadata, sections 17.2, 18.3 and 18.5.2.",
     "https://ec.europa.eu/eurostat/cache/metadata/en/env_ac_ainah_r2_simsae_mt.htm"),
    ("9", "Eurostat. Greenhouse gas emissions by source sector (env_air_gge, updated 2 June 2026); GDP (nama_10_gdp) "
          "and gross value added by activity (nama_10_a64), updated 6 October 2026; population (nama_10_pe). "
          "Retrieved 6 October 2026.", "https://ec.europa.eu/eurostat/databrowser/view/env_air_gge/default/table"),
    ("10", "Eurostat. Share of energy from renewable sources (nrg_ind_ren), overall and electricity; updated "
           "15 September 2026, retrieved 6 October 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/nrg_ind_ren/default/table"),
    ("11", "Usubiaga A., Acosta-Fernández J. (2015). Carbon emission accounting in MRIO models: the territory vs. the "
           "residence principle. <i>Economic Systems Research</i> 27(4):458–477. doi:10.1080/09535314.2015.1049126. "
           "Abstract read.", "https://doi.org/10.1080/09535314.2015.1049126"),
    ("12", "Haberl H. et al. (2020). A systematic review of the evidence on decoupling of GDP, resource use and GHG "
           "emissions, part II: synthesizing the insights. <i>Environmental Research Letters</i> 15:065003. "
           "doi:10.1088/1748-9326/ab842a. Abstract read.", "https://doi.org/10.1088/1748-9326/ab842a"),
    ("13", "Miżien. Claim Check 025: per-capita and per-GDP emissions (COP30 statement), v1.1.",
     "https://github.com/leandergrech/Mizien/tree/main/claims/CC-025"),
    ("14", "Miżien. Claim Check 003: per-capita emissions vs the 2030 projection, v1.2.",
     "https://github.com/leandergrech/Mizien/tree/main/claims/CC-003"),
    ("15", "Miżien. Claim Check 026: the EU’s largest rise in emissions, v1.0 (same accounts; air transport 444 to "
           "4,730 kt CO₂e, 2015–2024).", "https://github.com/leandergrech/Mizien/tree/main/claims/CC-026"),
    ("16", "Miżien. Data and calculations: data/cc-114/; tools/cc-114-report/fetch.py and calc.py.", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 2 * mm)]
S += revision_log([
    ("1.0", "6 Oct 2026", "First issue. Pending right of reply (Nationalist Party)."),
])

build_report(Report(
    number="114", out=str(FIG / "report.pdf"), kicker="Emissions intensity",
    title_lines=["Rising intensity,", "and what", "drives it"],
    subtitle_lines=["Testing the PN’s reading of Eurostat’s greenhouse gas", "intensity figures for Malta, 2013–2024"],
    quote_lines=["“Malta is the only EU Member State which, instead", "of reducing, increased the intensity of",
                 "greenhouse gas emissions from 2013 to date.”"], quote_size=13.5,
    attribution="Partit Nazzjonalista press release, signed by Eve Borg Bonello, 26 Jan 2026 (our translation).",
    context="It cites Eurostat (Malta +17%, EU −34%) and calls the rise the result of weak renewables ambition.",
    verdict="Misleading", verdict_note="Eurostat’s figure is right; the rise is airline fuel bought abroad",
    footer_lines=["Version 1.0  ·  6 October 2026", "Status: draft, pending right of reply (Nationalist Party)",
                  "Prepared from public sources and Eurostat data.",
                  "Repository: github.com/leandergrech/Mizien"],
    running_head="Emissions intensity – Malta", version="1.0", date="6 October 2026",
    pdf_title="Rising intensity, and what drives it. Claim Check 114",
    pdf_subject="Tests the PN's statement that Malta is the only EU state whose emissions intensity rose since 2013",
    story=S))
