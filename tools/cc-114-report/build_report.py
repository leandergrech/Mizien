"""Claim Check 114 report. Run fetch.py, calc.py and figures.py first. Output: out/report.pdf"""
import csv
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
DATA = HERE.parents[1] / "data" / "cc-114"
BRICK = VERDICT_COLS[3]     # the Misleading colour
MAROON = VERDICT_COLS[4]    # the Contradicted colour
S = []
TIGHT = [("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]

# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("On 26 January 2026 a Nationalist Party (PN) release signed by Eve Borg Bonello said that <b>“Malta is the "
        "only EU Member State which, instead of reducing, increased the intensity of greenhouse gas emissions from "
        "2013 to date”</b> (+17%, EU −34%), that Malta now pollutes more for every euro of its economy, and that this "
        "is “the direct result” of a lack of ambition on several fronts, among them, renewables [1] (our "
        "translation).", lead)]
S.append(key_points([
    ("The headline figure is Eurostat’s, quoted correctly.",
     "Eurostat: “Only Malta (+17%) saw its emissions intensity increase since 2013”, EU −34% [3, 4]. Revised "
     "data: +14.3%, still the only rise, last of 27 from every base year [6]."),
    ("72% of Malta’s 2024 figure is airline fuel bought abroad (2024 estimate).",
     "The indicator counts Malta-resident firms’ emissions wherever they occur [7]. Air transport rose from 0.30 to "
     "4.73 Mt CO₂e, 2013–2024 (2024: Eurostat estimate, flag i), all of it fuel bought abroad: 116% of the net rise in "
     "resident-unit emissions (+3.81 Mt), not of the indicator. Air transport alone: about 36 g/EUR in 2013, 266 in "
     "2024 (estimate) [6, 8]."),
    ("Without air transport, the indicator fell from every base year.",
     "−8.5% to −72% for bases 2008–2023: −64% since 2013 (EU’s second largest fall), −29.5% since 2016 (17th of "
     "27), as power-sector emissions fell mostly in 2014–2016 [6]."),
    ("More renewable electricity, on its own, could not have removed the rise.",
     "Air transport accounts for the whole increase; electricity emissions fell about 56%. With none at all in "
     "2024 (the bound tests electricity only) the indicator would still be 1.4% above 2013 [6, 10]. “Lack of "
     "ambition” (E) is not rated."),
    ("Verdict: misleading (moderate confidence).",
     "The statistic is right, but the release never names the airline-fuel basis and links the rise to "
     "renewables, which alone could not have removed it. Moderate, not high: D and F rest on the same Eurostat "
     "accounts, including the imputed (flag i) 2024 air-transport value. Pending right of reply."),
]))
S += [Spacer(1, 1 * mm), VerdictMeter(3), Spacer(1, 1 * mm),
      tiles([("+14%", RED, "Eurostat’s indicator for Malta, 2013–2024 (+17% in January; EU −34%)"),
             ("72%", RED, "of Malta’s 2024 figure is airline fuel bought abroad (2024 estimate; 11% in 2013)"),
             ("116%", ORANGE, "of the rise in emissions (+3.81 Mt, not the indicator) is air transport (2024 est.)"),
             ("−64%", GREEN, "without air transport since 2013; a fall from every base year 2008–2023")]),
      Spacer(1, 2 * mm),
      up_down("Revised data or a source showing that the rise comes from activities in Malta that renewable energy "
              "could reduce (for example emissions reallocated to electricity): <i>Largely supported</i>.",
              "Reported 2024 data replacing Eurostat’s estimate and showing no rise since 2013 (to 2023 the "
              "indicator fell 8.3%): the headline itself would then be wrong, <i>Contradicted</i>."),
      Spacer(1, 2 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What Eurostat’s indicator counts"),
          ("4", "What the data show"), ("5", "Where the evidence points different ways"), ("6", "Testing the claim"),
          ("7", "Verdict and requests for evidence"), ("8", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The statement is a PN press release in Maltese, published on the party’s website on 26 January 2026 and "
           "signed by Eve Borg Bonello as Shadow Minister for Climate Change and Public Cleanliness [1]. Newsbook "
           "reported it in English the same day, quoting some sentences and giving the figures in its own words [2]. "
           "We rate the release. Quotations are our translation, checked against Newsbook’s English where it has one; "
           "the Maltese is in <i>literature/CC-114/primary-source.md</i>."))
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
    [C("“In simple words, it is not simply that we are polluting more because the economy grew, but today, for every "
       "euro we put into our economy, we are polluting more than we were polluting in 2013.”"),
     C("Release [1]; quoted in English by Newsbook [2]"), C("Read in full")],
    [C("“This is the direct result of a lack of ambition on the part of the Maltese Government on several fronts. "
       "Among them, the clear lack of ambition to seriously increase the use of renewable energy.” A later "
       "paragraph cites “the long hours stuck in traffic” as a problem on which the Government drags its feet."),
     C("Release [1]; its subtitle names renewables"), C("Read in full")],
    [C("“In 2024 our country generated only 10.7% of its energy from renewable sources … the European average is a "
       "little over 25% … third from last.”"), C("Release [1]"), C("Read in full")],
    [C("The release’s image: Eurostat’s map of the change in emissions intensity of gross value added, 2013–2024 "
       "(Malta 16.6)."), C("Release [1]; Eurostat [3, 4]"), C("Read in full")],
], [96 * mm, 46 * mm, 28 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("FAIRNESS NOTE", tag),
               P("The PN reproduced Eurostat’s headline and definition accurately, and Eurostat’s own news item "
                 "gives no explanation of Malta’s figure either [3]. This is an opposition statement, held to the same "
                 "standard and data as the Government’s statement on the same theme (Claim Check 025) [13]; we test our "
                 "own counter-figures from every base year, as we test the PN’s. Newsbook’s own additions (for example "
                 "Malta’s lead in emissions per unit of GDP since 2005) are not the PN’s and are not rated.", small)],
              bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Questions.</b> (i) Does Eurostat show Malta as the only EU Member State whose emissions intensity rose "
           "since 2013, by 17% against −34%? (ii) Does that hold in the latest data and for other start and end years? "
           "(iii) What drives Malta’s figure? (iv) Do other measures of emissions per unit of output agree, and from "
           "which base years? (v) Can the cause the release gives account for the rise? (vi) Are the release’s other "
           "figures right?"))
S.append(P("<b>Evidence.</b> Eurostat’s news item, map and Statistics Explained article [3–5]; its air emissions "
           "accounts (intensities, emissions by activity, bridging to the national inventory) [6]; Eurostat’s and the "
           "National Statistics Office’s (NSO) metadata [7, 8]; the territorial inventory, GDP, value added and "
           "population [9]; renewable shares [10, 16]; and two peer-reviewed papers [11, 12]. All data were retrieved "
           "on 6 October 2026 into <i>data/cc-114/</i> with Eurostat’s status flags; every figure is recomputed by "
           "<i>tools/cc-114-report/calc.py</i> (<i>data/cc-114/checks.csv</i>)."))
S.append(P("<b>Grades.</b> Eurostat’s and the NSO’s statistics and metadata are official statistics, grade C; the two "
           "papers, read as abstracts, are a methodological analysis and a systematic review, grade C. The release and "
           "the news report are the claim, not evidence. <b>Verdicts</b> follow the scale in Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(80 * mm))
S.append(SectionHeading(3, "What Eurostat’s indicator counts"))
S.append(P("Eurostat’s greenhouse gas emissions intensity is the emissions of an economy’s production units, in CO₂ "
           "equivalents, per euro of gross value added in chain-linked 2020 prices; households are left out because "
           "they produce no value added [5]. The emissions come from the <b>air emissions accounts</b>, which follow "
           "the national accounts and so the <b>residence principle</b>: they record “emissions arising from the "
           "activities of all resident units … regardless of where these emissions actually occur geographically” "
           "[7]. The inventory reported to the UN climate convention instead counts what is emitted on the territory "
           "(“territory principle”, in the label of Eurostat’s bridging table [6]) and keeps international aviation "
           "and shipping as memo items [9]. A peer-reviewed comparison finds the gap between the two principles "
           "“high for many countries” and growing [11]."))
S.append(P("An airline resident in Malta is counted in Malta’s accounts for the fuel it burns on any route [7], and "
           "its value added is part of Malta’s GDP (general national-accounts context): the indicator is consistent, "
           "but it does not measure emissions in Malta. Eurostat’s article notes that in Denmark, Luxembourg and Malta transport is the key emitting "
           "activity in these accounts, as transport companies’ emissions “are allocated to the country of "
           "residence” [5]."))
S.append(P("<b>Malta’s air transport.</b> Eurostat’s bridging table classes as fuel bought abroad 299 of the 304 kt "
           "of Malta’s air-transport emissions in 2013 and all 4.73 Mt in 2024 (an estimate), with 0.91 Mt in 2019, "
           "1.59 Mt in 2022 and 3.11 Mt in 2023 [6]: from 0.4% to 4.4% of all such emissions by EU residents, for "
           "an economy with 0.13% of the EU’s value added. The NSO attributes the 2023 jump to “an increase in "
           "international aviation activity, primarily due to the activity of airlines which started operating during "
           "2023”; its source is the OECD’s residence-based aviation data, with charter flights for 2013–2018 "
           "estimated by the NSO and revised in February 2026 [8]. Neither names the airlines, and we do not."))
S.append(P("<b>What 2024 is.</b> Eurostat estimates the latest year itself [7]: Malta’s 2024 values, and the EU-27’s, "
           "carry the flag “i”, imputed. Eurostat also warns that “a multitude of factors may drive greenhouse gas "
           "emissions intensity, with improving environmental performance and decarbonisation policies being only "
           "one of them” [5]. A falling intensity alongside growth is what the literature calls relative "
           "decoupling [12]."))

# ================================================================== 4
S += [CondPageBreak(70 * mm), SectionHeading(4, "What the data show"),
    P("The same economy gives opposite signs depending on what is counted, from when and at which prices. This table "
      "starts in 2013, the PN’s base year; the next one tests other base years, for our figures as for the PN’s."),
    std_table([
    [C("Measure", cellh), C("Counts", cellh), C("Period", cellh), C("Malta", cellh), C("EU-27", cellh),
     C("Rank, 1 = largest fall", cellh)],
    [C("Eurostat’s indicator, January release"), C("Residents / GVA"), C("2013–24"), C("<b>+16.6%</b>"),
     C("−34.0%"), C("27th, only rise")],
    [C("Same, data of August 2026"), C("Residents / GVA"), C("2013–24"), C("<b>+14.3%</b> (est.)"),
     C("−34.0%"), C("27th, only rise")],
    [C("Same, ending 2023"), C("Residents / GVA"), C("2013–23"), C("−8.3%"), C("−32.4%"), C("no rise")],
    [C("Same, current prices"), C("Residents / GVA"), C("2013–24"), C("−20.3%"), C("−49.3%"), C("no rise")],
    [C("Same, without air transport"), C("Residents / GVA"), C("2013–24"), C("<b>−64.0%</b>"), C("−35.2%"),
     C("2nd of 27")],
    [C("Territorial inventory per € of GDP"), C("Territory / GDP"), C("2013–24"), C("<b>−61.3%</b>"), C("−35.5%"),
     C("2nd of 27")],
    [C("Same, from 2005, volumes / current prices (CC-025’s “80%”)"), C("Territory / GDP"), C("2005–24"),
     C("−72.2% / −83.8%"), C("−47.9% / −64.7%"), C("")],
    [C("Territorial inventory per person"), C("Territory / person"), C("2013–24"), C("−42.6%"), C("−24.2%"),
     C("3rd of 27")],
    [C("Residents incl. households, per person"), C("Residents / person"), C("2013–24"), C("+69.2%"), C("−21.2%"),
     C("27th, 5 rises")],
], [50 * mm, 27 * mm, 15 * mm, 25 * mm, 25 * mm, 28 * mm],
              extra=TIGHT),
    P("Sources [4, 6, 9, 13]; values in <i>data/cc-114/checks.csv</i>, ranks in <i>ranking_2013_2024.csv</i>. "
      "“Without air transport” removes its emissions only; removing transport from both sides gives −66.3%.", cap)]
# base-year sensitivity, read from calc.py's output
BS = {int(r["base_year"]): r for r in csv.DictReader(open(DATA / "sensitivity_base_years.csv"))}
th = lambda n: f"{n}{'st' if n % 10 == 1 and n != 11 else 'nd' if n % 10 == 2 and n != 12 else 'rd' if n % 10 == 3 and n != 13 else 'th'}"
cell = lambda v, rk: C(f"{float(v):+.1f}% ({th(int(rk))})".replace("+-", "−").replace("-", "−"))
bs_rows = [[C("Base year", cellh), C("Eurostat’s indicator", cellh), C("Without air transport", cellh),
            C("Territorial per € of GDP", cellh), C("Electricity-sector emissions", cellh)]]
for b in (2008, 2010, 2012, 2013, 2014, 2015, 2016, 2019, 2023):
    r = BS[b]
    bs_rows.append([C(f"<b>{b}</b>" if b in (2013, 2016) else str(b)), cell(r["published_malta_pct"], r["published_rank"]),
                    cell(r["without_air_malta_pct"], r["without_air_rank"]),
                    cell(r["territorial_per_gdp_malta_pct"], r["territorial_rank"]),
                    C(f"{float(r['malta_electricity_D_pct']):+.0f}%".replace("-", "−"))])
S.append(KeepTogether([P("Every measure by base year, to 2024", h2), std_table(bs_rows, [24 * mm, 38 * mm, 38 * mm,
                                                                                          38 * mm, 32 * mm]),
    P("Malta’s change to 2024 and its rank of 27 (1st = largest fall; 27th = weakest). EU-27 from 2013: −34.0%, "
      "−35.2%, −35.5%; from 2016: −29.0%, −30.1%, −29.8%. All bases 2008–2023 in <i>sensitivity_base_years.csv</i> "
      "[6, 9].", cap)]))
RA = [P("Reading across the data", h2)]
for t in ["• <b>Both parties’ figures are real; they count different things.</b> The Government’s COP30 statement "
          "(Claim Check 025) gave no basis; its “more than 80%” per unit of GDP since 2005 holds on the territorial "
          "inventory only at current prices (−72% in volumes) [13]. The PN used Eurostat’s residence-based indicator.",
          "• <b>One activity explains the whole rise.</b> Malta’s resident production units went from 2.78 to "
          "6.59 Mt CO₂e while real value added rose 108.5%: air transport from 0.30 to 4.73 Mt (2024 estimate), electricity, gas and "
          "steam from 1.70 to 0.74 Mt, other transport from 0.18 to 0.26 Mt, and all other activities from 0.59 to "
          "0.86 Mt [6]. Air transport added 4.43 Mt, 116% of the net increase in these emissions (+3.81 Mt; a share of the "
          "rise in emissions, not of the intensity indicator); the rest fell, taken together. In intensity terms, air "
          "transport alone went from about 36 g/EUR of total value added in 2013 to about 266 g/EUR in 2024 "
          "(estimate), against an indicator of 325 and 372 g/EUR.",
          "• <b>Our counter-figures depend on the base year too.</b> Most of the fall without air transport, and of the "
          "territorial fall, came in 2014–2016, when electricity-sector emissions fell from 1.70 to 0.58 Mt; since "
          "2016 they have risen 28%. From 2016, Malta’s fall without air transport (−29.5%, 17th) and on the "
          "territorial inventory (−27.1%, 21st) is close to the EU’s. What holds from every base year is the "
          "direction: both fell, from every year from 2008 to 2023.",
          "• <b>The PN’s base year is not a convenient one.</b> Ending 2024, Malta’s rise from any base year 2014–2019 "
          "is larger, +19.5% to +97%, and Malta is last of the 27 from every base year from 2008, though it fell "
          "(by up to 9%) from bases 2008–2012.",
          "• <b>“Only Malta” rests on the 2024 estimate.</b> With 2013 as the base, Malta is the only riser for the "
          "end year 2024 and for no other; to 2023, the last year Malta reported, it fell 8.3% and no Member State "
          "rose.",
          "• <b>The rise is recent.</b> The indicator fell 40% from 2013 to 2016 and was still 39% below 2013 in 2021. "
          "It rose 63% from 2022 to 2024: the NSO links the 2023 jump to airlines that started operating that year "
          "[8]; the 2024 value is Eurostat’s estimate.",
          "• <b>The January and August figures differ only for Malta:</b> +16.6% to +14.3%; no other country moved "
          "by more than 0.7 points. The NSO revised 2013–2018 air transport in February 2026 [8]."]:
    RA.append(P(t, bul))
S += [KeepTogether(RA[:2])] + RA[2:]
S.append(KeepTogether([fig(FIG / "fig1_ranking.png", width=CW * 0.92),
                       P("Figure 1. Change in emissions per euro of output, 2013–2024, for the 27 Member States, on "
                         "Eurostat’s published indicator (filled; resident production units per euro of gross value "
                         "added) and on the territorial inventory per euro of GDP (hollow; excluding land use and "
                         "international bunkers), both in chain-linked volumes [6, 9]. Sorted by Eurostat’s indicator. "
                         "2024 values in the accounts are Eurostat estimates; ranks depend on the base year (see the base-year table).",
                         cap)]))
S.append(KeepTogether([fig(FIG / "fig2_malta.png"),
                       P("Figure 2. Malta. Panel A: emissions of resident production units by activity, with the "
                         "territorial inventory for comparison (Mt CO₂e). Panel B: Eurostat’s indicator, the same "
                         "without air-transport emissions, and the territorial inventory per euro of GDP, all indexed "
                         "to 2013 = 100. 2024 is a Eurostat estimate (hatched, shaded) [6, 9].", cap)]))


# ================================================================== 5
S.append(CondPageBreak(85 * mm))
S.append(SectionHeading(5, "Where the evidence points different ways"))
S.append(contested(
    "Q1  Is Malta the only Member State whose intensity rose since 2013?", "YES, ON EUROSTAT’S INDICATOR", GREEN,
    "Eurostat’s news item and map say so: +16.6%, the only rise, EU −34.0% [3, 4]. The revised data of August 2026 "
    "give +14.3%, still the only rise, and Malta ranks last from every base year [6].",
    "Only with 2024 as the end year, and Malta’s 2024 value is a Eurostat estimate. To 2023 the indicator fell 8.3% "
    "and no Member State rose [6].",
    "<b>For this claim:</b> accurate as Eurostat’s published statistic; the release rightly says it is Eurostat’s."))
S.append(contested(
    "Q2  Does Malta now pollute more per euro than in 2013?", "ONLY BY COUNTING AIRLINES ABROAD", ORANGE,
    "Malta-resident firms emit 14% more per euro of value added than in 2013 [6]. Their value added is in Malta’s "
    "GDP, so counting their emissions is consistent, as Eurostat’s accounts intend [5, 7].",
    "72% of the 2024 figure is fuel bought abroad by resident air transport firms. Without air transport the "
    "indicator fell from every base year (−64% since 2013, −29.5% since 2016) [6].",
    "<b>For this claim:</b> true of resident firms as the accounts count them. The release never names that basis, "
    "and its renewables explanation treats the figure as domestic."))
S.append(contested(
    "Q3  Could more renewable electricity, on its own, have removed the rise?", "CONTRADICTED", MAROON,
    "Malta’s renewable shares are among the EU’s lowest: 10.7% of electricity in 2024, the lowest of the 27, and "
    "17.2% of all energy, fourth from last [10].",
"Air transport accounts for the whole increase in resident-unit emissions (116% of +3.81 Mt), while "
    "electricity-sector emissions fell about 56% (1.70 to 0.74 Mt). Even with no electricity-sector emissions at all "
    "in 2024, the indicator would still be 1.4% above 2013 (329.8 against 325.2 g/EUR): zeroing electricity alone "
    "leaves 2024 above 2013. Renewable shares rose over the period: electricity 1.6% to 10.7%, overall 3.8% to "
    "17.2% [6, 10].",
    "<b>For this claim:</b> more renewable electricity, on its own, could not have removed the rise. The bound tests "
    "electricity-sector emissions only. This rates the release’s “direct result” link as applied to renewables; "
    "“a lack of ambition on several fronts” (E) is a political judgement we do not rate. The release also cites "
    "“the long hours stuck in traffic”, without tying it to the figure; households’ own car use is outside the "
    "indicator [5]."))

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
     C("Matches the January release (+16.6%, −34.0%); revised to +14.3% (EU values flagged i). “Increased these "
       "emissions” is the slip rated in C, but here the same sentence gives the EU’s “average intensity”, so we read "
       "the figures as intensity. The −34% is the EU aggregate (countries’ mean −32.4%) [3, 4, 6]."), verd("ACCURATE", GREENC)],
    [C("<b>C.</b> Estonia reduced emissions by 64%, Ireland by 50%, Finland by 44%"),
     C("These are intensity changes, given as emissions and “the fight against air pollution”. Amber because of "
       "Ireland, whose emissions rose while its intensity fell, not because of the emissions-for-intensity label as "
       "such: the same label in the Malta sentence was excused (B), as that sentence gives the EU’s “average "
       "intensity”. Emissions 2013–2024, residence accounts / territorial inventory: Estonia −55% / −53% and "
       "Finland −38% / −38% (both 2024 flagged i), Ireland +13.7% / −6.9% (2024 flagged e; 87% of its rise on the "
       "residence basis is air transport) [5, 6, 9]."),
     verd("MISLABELLED", AMBER)],
    [C("<b>D.</b> For every euro put into the economy, Malta pollutes more than in 2013"),
     C("True on the residence basis, which the release never names: 72% of Malta’s 2024 figure is air-transport fuel "
       "bought abroad; without it the indicator fell from every base year (−64% since 2013); territorial inventory per "
       "€ of GDP −61% since 2013 [6, 9]."), verd("NEEDS CONTEXT", AMBER)],
    [C("<b>E.</b> The rise is the direct result of a lack of ambition on several fronts"),
     C("A political judgement about the Government’s ambition, not a checkable statement of fact [1]."),
     verd("NOT RATED", GREY)],
    [C("<b>F.</b> Renewables as a cause of the rise: “among them, the clear lack of ambition to seriously increase "
       "the use of renewable energy”"),
     C("Rates the release’s “direct result” causal link as applied to renewables; the “lack of ambition” judgement "
       "(E) is not rated. Air transport accounts for the whole increase and electricity-sector emissions fell about "
       "56%; with zero electricity-sector emissions in 2024 the indicator would still be 1.4% above 2013, so more "
       "renewable electricity, on its own, could not have removed the rise (the bound tests electricity only); "
       "renewable shares rose (electricity 1.6% to 10.7%) [6, 10]."),
     verd("CONTRADICTED", MAROON)],
    [C("<b>G.</b> 10.7% renewables in 2024 against an EU average of just over 25%, third from last"),
     C("10.7% is Malta’s electricity share (lowest in the EU; EU 47.5%); 25.2% is the EU’s overall share. Malta’s "
       "overall share is 17.2%, fourth from last [10]. Eurostat’s release of 18 December 2025 named Belgium, Luxembourg "
       "and Ireland (14.3–16.1%) as the lowest three, so Malta was not third from last in the data published before "
       "the PN’s release [16]."), verd("MIXED MEASURES", AMBER)],
], [50 * mm, 90 * mm, 30 * mm], valign="MIDDLE"))

# ================================================================== 7
S += [Spacer(1, 6 * mm), CondPageBreak(90 * mm), SectionHeading(7, "Verdict and requests for evidence"),
      verdict_box("Misleading", "Eurostat’s figure is quoted correctly, but the release never says it counts airline "
                  "fuel bought abroad, and links the rise to renewables, which on their own could not have removed it. "
                  "Confidence: moderate."),
      Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) The central statistic is Eurostat’s, quoted correctly: Malta is the only Member "
           "State whose indicator rose from 2013 to 2024. (2) The release "
           "reads it as Malta polluting more for every euro of its economy, “the direct result” of a lack of ambition "
           "on several fronts, among them, renewables. (3) Eurostat’s own tables, which the release does not mention, "
           "show that air transport is 116% of the net rise, all of the rise being fuel bought abroad by air "
           "transport firms resident in Malta; that without it the indicator fell from every base year from 2008 to "
           "2023; and that even with no electricity-sector emissions in 2024 it would still be above 2013, so "
           "more renewable electricity, on its own, could not have removed the rise. These omitted facts change what the figure means: the individual "
           "figures are defensible but the overall impression is inaccurate, the scale’s definition of "
           "<i>Misleading</i>. The verdict rests on the omission (sub-claim D) together with the contradicted "
           "renewables link (F); the evidence shown is listed in the claim record."))
S.append(P("<b>Why not Contradicted or Largely supported.</b> The headline statistic is true, so the claim is not "
           "contradicted. The omission is not a minor caveat: it changes what the figure means and undercuts the "
           "cause drawn from it. <b>Why moderate, not high, confidence.</b> The decomposition and the bound are "
           "arithmetic on Eurostat’s own tables, and the OECD-based aviation series in the accounts [8] and the "
           "separately compiled territorial inventory [9] point the same way for the per-euro fall. But the deciding "
           "sub-claims D and F both rest on the same Eurostat air emissions accounts, including the imputed (flag i) "
           "2024 air-transport value, so they are not independent checks of each other; confidence was lowered from "
           "high to moderate in version 1.1 for that reason. Our own counter-figures also depend on the base year, so "
           "the verdict rests on their direction, not on Malta’s ranking."))
S.append(P("<b>Consistency with other checks.</b> Claim Check 026 rated a news report of a figure from the same "
           "accounts <i>Largely supported</i> because its body explained the difference between the residence and "
           "territorial measures; its headline read alone was rated “Needs context” (amber, 026D) [15]. This release "
           "never names the basis, so sub-claim D gets the same amber rating, and the overall <i>Misleading</i> rests "
           "on that omission together with the contradicted renewables link (F). Claim Check 025 rated the "
           "Government’s “more than 80%” per unit of GDP “True only at current prices” (amber, within a <i>Largely "
           "supported</i> statement): it gave no basis, and the figure holds on the territorial inventory at current "
           "prices, not in volumes (−72%) [13]. Claim Check 003 rated a per-person figure <i>Misleading</i> for "
           "leaving out a projection that changed the picture [14]. “Selective metric” tags a metric favourable to "
           "the speaker’s argument (not to Malta or to any party) cited while the inventory reported to the UN climate "
           "convention points the other way. On the residence basis the PN used, emissions per person (households "
           "included) rose 69.2% from 2013 to 2024, 27th of 27, against −21.2% for the EU-27 [6, 9]. The verdicts "
           "differ because this release adds a causal link the data contradict, whereas Claim Check 025 states the "
           "basis of the figure it rates and the statement it rates draws no causal inference."))
S.append(P("<b>What this verdict does not say.</b> It does not say Malta’s renewable shares are adequate (its "
           "electricity share is the EU’s lowest), that aviation emissions do not matter, or that anyone acted in "
           "bad faith. A statement the data support would read: <i>“On Eurostat’s residence-based measure Malta’s "
           "emissions intensity rose 17% since 2013 (14% in revised data), the only rise in the EU, because emissions "
           "of airlines resident in Malta, from fuel bought abroad, rose more than fifteen-fold; without them, and on the "
           "territorial inventory, Malta’s emissions per euro fell.”</i>"))
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
S += [Spacer(1, 4 * mm), CondPageBreak(60 * mm), SectionHeading(8, "Limitations")]
for l in ["Malta’s 2024 values in the air emissions accounts are Eurostat estimates (flag i; Malta reported to 2023), "
          "and the rise since 2013 depends on them. Our counter-figures hold in direction from every base year, but "
          "their size and rank do not: from 2016 they are close to the EU’s (section 4).",
          "Malta’s air-transport series comes from the OECD’s residence-based aviation data with NSO additions for "
          "charter flights before 2019 [8]; a change of source between years could affect comparisons with 2013.",
          "We did not identify the airlines or read company filings. The value added of air transport is not "
          "published for 2013 and is negative in volumes for 2022–2024, so “without air transport” removes "
          "emissions only (removing all transport from both sides: −66.3%).",
          "The translation of the Maltese release is ours. The page was modified on 24 April 2026 (its image is filed "
          "under that month); we found no January copy, but Newsbook’s quotes of 26 January match the text.",
          "The two papers were read as abstracts; MaltaToday’s report was not readable and not used."]:
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
    ("15", "Miżien. Claim Check 026: the EU’s largest rise in emissions, v1.1 (same accounts; air transport 444 to "
           "4,730 kt CO₂e, 2015–2024).", "https://github.com/leandergrech/Mizien/tree/main/claims/CC-026"),
    ("16", "Eurostat (18 December 2025). 25.2% of energy EU used in 2024 came from renewables. News item (lowest: "
           "Belgium 14.3%, Luxembourg 14.7%, Ireland 16.1%).",
     "https://ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-20251218-2"),
    ("17", "Miżien. Data and calculations: data/cc-114/; tools/cc-114-report/fetch.py and calc.py.", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 2 * mm)]
S += revision_log([
    ("1.0", "6 Oct 2026", "First issue. Pending right of reply (Nationalist Party)."),
    ("1.1", "6 Oct 2026", "Corrections after the audit of 6 Oct 2026. Sub-claim F and the bound narrowed to “more "
                          "renewable electricity, on its own, could not have removed the rise” (the bound tests "
                          "electricity-sector emissions only; “lack of ambition” not rated); confidence lowered from "
                          "high to moderate (D and F rest on the same Eurostat accounts, including the imputed 2024 "
                          "air-transport value); 116% labelled as a share of the rise in resident-unit emissions; "
                          "2024 values labelled as estimates; sub-claim C amber because of Ireland; land-transport "
                          "figure dropped; consistency sentence added on emissions per person (+69.2%, CC-025). "
                          "Pending right of reply (Nationalist Party)."),
])

build_report(Report(
    number="114", out=str(FIG / "report.pdf"), kicker="Emissions intensity",
    title_lines=["Rising intensity,", "and what", "drives it"],
    subtitle_lines=["Testing the PN’s reading of Eurostat’s greenhouse gas", "intensity figures for Malta, 2013–2024"],
    quote_lines=["“Malta is the only EU Member State which, instead", "of reducing, increased the intensity of",
                 "greenhouse gas emissions from 2013 to date.”"], quote_size=13.5,
    attribution="Partit Nazzjonalista press release, signed by Eve Borg Bonello, 26 Jan 2026 (our translation).",
    context="It cites Eurostat (Malta +17%, EU −34%) and blames a lack of ambition on “several fronts”, among them, "
            "renewables.",
    verdict="Misleading", verdict_note="Eurostat’s figure is right; since 2013 the rise is airline fuel (2024 estimate)",
    footer_lines=["Version 1.1  ·  6 October 2026", "Status: draft, pending right of reply (Nationalist Party)",
                  "Prepared from public sources and Eurostat data.",
                  "Repository: github.com/leandergrech/Mizien"],
    running_head="Emissions intensity – Malta", version="1.1", date="6 October 2026",
    pdf_title="Rising intensity, and what drives it. Claim Check 114",
    pdf_subject="Tests the PN's statement that Malta is the only EU state whose emissions intensity rose since 2013",
    story=S))
