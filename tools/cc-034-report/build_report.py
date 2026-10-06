"""Claim Check 034 report. Run fetch.py, calc.py and figures.py first. Output: out/report.pdf"""
import csv
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
K = {r["id"]: r for r in csv.DictReader(open(HERE.parents[1] / "data" / "cc-034" / "checks.csv", encoding="utf-8"))}
V = lambda k: K[k]["value"]   # every number below comes from data/cc-034/checks.csv
T = lambda k: V(k).replace(" → ", " to ")
S = []
LG = colors.HexColor("#8DB36B")
FW = 0.88 * CW   # figure width

# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("The Environment and Resources Authority (ERA) says its Air Quality Plan “outlines actions that have already "
        "yielded positive results for Malta’s air quality” [1]. The plan names six, from “the reform in the power "
        "generation sector” to “free public transport for all” [2]. We tested this against 13 years of validated data "
        "from every ERA station, ERA’s reports to the European Environment Agency (EEA) and Malta’s emissions "
        "inventory.", lead)]
S.append(key_points([
    ("The power-sector reform did clean the air.",
     "Sulphur oxides from power stations fell 99.9% between 2008 and 2018 [5]; sulphur dioxide in the air fell 82% "
     "at Żejtun [3]."),
    ("NO₂ and PM2.5 at the Msida roadside are lower than in 2015–17",
     f"({T('B-NO2-msida')} and {T('B-PM2.5-msida')} µg/m³, 2015–17 to 2021–23) [3], in step with a cleaner vehicle "
     "fleet [5]. The data cannot tie this to any named measure."),
    ("PM10, the reason for the plan, did not improve.",
     "After ERA deducts dust and sea salt, Msida had 52 days over the daily limit in 2023 (35 allowed), the most of "
     "2015–2025, with the transport measures in place [4]."),
    ("The transport measures come with uptake figures, not results.",
     "The plan’s one test, of free school transport, does not reproduce; in the year after free public transport "
     "began, 10 of 11 station readings rose [3]."),
    ("Verdict: not substantiated (moderate confidence).",
     "Missing evidence, not proof that the measures did nothing. Pending right of reply from ERA."),
]))
S += [Spacer(1, 4 * mm), VerdictMeter(2), Spacer(1, 3 * mm),
      tiles([("−99.9%", GREEN, "Sulphur oxides from power stations, 2008 to 2018 [5]"),
             ("−22%", GREEN, "NO₂ at the Msida roadside, 2015–17 to 2021–23; cause not isolated [3]"),
             ("52 days", RED, "Msida PM10 over the daily limit in 2023 after natural deductions; 35 allowed [4]"),
             ("+8.1", ORANGE, "µg/m³ PM10 at Msida in the year after free public transport began [3]")]),
      Spacer(1, 4 * mm),
      up_down("A published analysis that isolates the transport measures’ effect, for example traffic counts past "
              "Msida and meteorologically normalised trends against a control site, showing lower pollution after "
              "they began: <i>Largely supported</i>.",
              "Traffic or travel-survey data showing that the measures did not reduce car traffic in the harbour area, "
              "set beside the station data: <i>Contradicted</i> for those measures."),
      Spacer(1, 5 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What moves Malta’s air"),
          ("4", "What the data show"), ("5", "Measure by measure"), ("6", "Where the evidence points different ways"),
          ("7", "Testing the claim"), ("8", "Verdict and requests for evidence"), ("9", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The statement is on ERA’s web page for the plan, published on 12 March 2025 according to the page’s own "
           "metadata [1]. The page’s list stops at “actions”; the plan’s executive summary names them [2]. The claim "
           "record combines the two documents, so each is quoted with its own source below. The plan was approved "
           "under Article 51 of the Environment Protection Act (Cap. 549) [1]."))
S.append(std_table([
    [C("What was said", cellh), C("Where", cellh), C("Our access", cellh)],
    [C("“The plan outlines actions that have already yielded positive results for Malta’s air quality, measures "
       "committed to by the Government for imminent implementation, and additional proposed measures …”"),
     C("ERA web page, Air Quality Plan for Malta 2025 [1]"), C("Read in full (Wayback capture of 15 Aug 2025)")],
    [C("“…measures from other policy documents that have already contributed to improvements in air quality in Malta, "
       "such as the reform in the power generation sector, grants for more sustainable transport, free school "
       "transport, improvement of ferry landing places, a fast ferry link between the main islands and free public "
       "transport for all.”"),
     C("Plan, executive summary, p. 3 [2]"), C("Read in full (104 pages)")],
    [C("The Msida station “exceeded the allowed number of exceedances for the daily limit value of particulate matter "
       "(PM10)”, on ERA’s assessment of 2018 and 2023 data."),
     C("ERA web page [1]; plan, p. 25 [2]"), C("Read in full")],
], [96 * mm, 46 * mm, 28 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("FAIRNESS NOTE", tag),
               P("The plan is candid about the limits of past action. It says most measures of the 2010 plan were "
                 "carried out, yet the exceedances returned because of population growth, traffic flows and the number "
                 "of vehicles registered (p. 28), and that cleaner vehicles are “masked by the rising number of vehicles” "
                 "(p. 54) [2]. Its purpose is the measures still to come, which this check does not assess. The question "
                 "here is only whether the six named measures have been shown to have improved the air.", small)],
              bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Questions.</b> Did Malta’s measured air quality improve, and can the improvement be tied to the six "
           "named measures? What evidence of effect does the plan itself give for each?"))
S.append(P("<b>Evidence.</b> All the validated measurements Malta has reported to the EEA for PM10, PM2.5, nitrogen "
           "dioxide (NO₂), sulphur dioxide (SO₂) and carbon monoxide (CO), from every ERA station, 2006–2025 (85 files, "
           "retrieved 6 October 2026) [3]; ERA’s attainment reports for 2015–2025, which give each year’s PM10 "
           "exceedances before and after the deduction of natural sources [4]; Malta’s emissions inventory by sector "
           "[5]; car numbers [6]. Every figure is recomputed by <i>tools/cc-034-report/calc.py</i> from "
           "<i>data/cc-034/</i> and listed in <i>checks.csv</i>. Literature was searched in Crossref and OpenAlex; "
           "the search log is in <i>literature/CC-034/notes.md</i>."))
S.append(P("<b>Separating correlation from attribution.</b> Three controls. (1) Background stations: the plan notes "
           "that natural sources affect “the entire monitoring network in a similar manner” (p. 25) [2], so the excess "
           "of the Msida traffic site over the rural station at Għarb (Gozo) or the urban background at Żejtun and Attard "
           "removes most dust, sea salt and weather that all sites share. (2) ERA’s own deduction of Saharan dust and sea "
           "salt [4]. (3) Before-and-after windows around each dated measure, at the traffic site and at the controls. "
           "We did not normalise for weather station by station, the standard way of separating weather from emissions "
           "[12]; this is a limitation (section 9)."))
S.append(P("<b>Grades.</b> EEA and ERA data, Eurostat and the plan’s data are official statistics, grade C; the plan’s "
           "statements of effect without data are grade D. Peer-reviewed observational studies are grade B. "
           "<b>Verdicts</b> follow the five-point scale in Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(60 * mm))
S.append(SectionHeading(3, "What moves Malta’s air"))
S.append(P("<b>PM10 at Msida is mostly not exhaust.</b> A peer-reviewed source apportionment of 209 samples taken at "
           "the Msida traffic site in 2018 attributes 3.4% of PM10 to vehicle exhaust, 17% to tyre and brake wear and "
           "18% to road dust and crustal material [7]. The plan’s account of the same study adds sea salt (23%) and "
           "Saharan dust (21%) [2]. The authors found “no discernible trend” in Msida’s PM10 over the preceding decade "
           "and concluded that traffic policies will have “a minimal effect unless the non-exhaust emissions are "
           "adequately controlled” [7]. So cleaner engines barely touch PM10; fewer vehicle-kilometres can. At the "
           "rural station at Għarb, natural and regional sources make up most of the PM10 (the plan’s summary of [8] "
           + DIAM + ")."))
S.append(P("<b>NO₂ is the clearest traffic signal.</b> When traffic fell during the 2020 lockdowns, monthly NO₂ at "
           "Msida was up to 54% below what a machine-learning model of business as usual predicted [9]. If a measure "
           "took many cars off the roads past Msida, NO₂ there should show it."))
S.append(P("<b>Sulphur dioxide and nickel trace heavy fuel oil,</b> which the power stations burned until 2015–17 "
           "(plan, pp. 41, 57) [2]."))

# ================================================================== 4
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(4, "What the data show"))
S.append(KeepTogether([fig(FIG / "fig1_pm10_days.png", FW), P(
    "Figure 1. Days with PM10 above 50 µg/m³ at Msida. Before ERA’s deduction of natural sources, every year from "
    "2013 to 2023 was over the 35 days allowed [14]. After the deduction, 2018 (41 days) and 2023 (52) were over [4]. The "
    "rural Għarb station had only 8 such days in 2023, fewer than in 2018 (12), so 2023’s excess at Msida was not a "
    "dust year. 2024–25 come from a new sampling point about 300 m away [13] and are not comparable.", cap)]))
S.append(KeepTogether([fig(FIG / "fig2_annual.png", FW), P(
    "Figure 2. Annual means. NO₂ and PM2.5 at the Msida roadside fell while the background stations changed little; "
    "PM10 at Msida did not fall. Hollow markers: under 85% of the year’s data valid [3].", cap)]))
S.append(KeepTogether([std_table([
    [C("Indicator, Msida unless stated", cellh), C("2015–17", cellh), C("2021–23", cellh), C("Change", cellh),
     C("Grade", cellh)],
    [C("PM10, annual mean (µg/m³)"), C(V("B-PM10-msida").split(" → ")[0]), C(V("B-PM10-msida").split(" → ")[1]),
     C("+0.1"), grade_tag("C")],
    [C("PM10, Msida minus Għarb (µg/m³)"), C("21.7"), C("20.6"), C("−1.1"), grade_tag("C")],
    [C("PM10, days over 50 after natural deduction (ERA), mean a year"),
     C(V("B-msida-days-final-1517-2123").split(" → ")[0]), C(V("B-msida-days-final-1517-2123").split(" → ")[1]),
     C("+8.0"), grade_tag("C")],
    [C("PM2.5, annual mean (µg/m³)"), C(V("B-PM2.5-msida").split(" → ")[0]), C(V("B-PM2.5-msida").split(" → ")[1]),
     C("−17%"), grade_tag("C")],
    [C("NO₂, annual mean (µg/m³)"), C(V("B-NO2-msida").split(" → ")[0]), C(V("B-NO2-msida").split(" → ")[1]),
     C("−22%"), grade_tag("C")],
    [C("NO₂, Msida minus Attard (µg/m³)"), C("24.7"), C("17.2"), C("−30%"), grade_tag("C")],
    [C("NO₂ at Attard / Żejtun (urban background)"), C("11.8 / 14.2"), C("11.4 / 13.7"), C("−0.5 / −0.5"),
     grade_tag("C")],
    [C("Road-transport exhaust NOx, inventory (t), 2015 → 2022"), C("2,546"), C("1,950"), C("−23%"), grade_tag("C")],
    [C("Passenger cars licensed, 2013 → 2025"), C("256,096"), C("335,693"), C("+31%"), grade_tag("C")],
], [78 * mm, 22 * mm, 22 * mm, 30 * mm, 18 * mm]),
    P("Means of the three annual means in each period; neither includes 2020 (lockdowns). NO₂ at Msida had 83% "
      "valid data in 2015. Sources: EEA [3], ERA [4], Eurostat [5, 6]. All values in <i>data/cc-034/checks.csv</i> [15].",
      cap)]))

# ================================================================== 5
S.append(CondPageBreak(50 * mm))
S.append(SectionHeading(5, "Measure by measure"))
S.append(P("5.1 Power-sector reform (2015–2017)", h2))
S.append(P("The interconnector to Sicily opened in April 2015, the Marsa power station closed in 2015 and from 2017 "
           "all generation at Delimara ran on natural gas (plan, p. 57) [2]. In 2008 the power sector produced 97% of "
           "Malta’s sulphur oxides and 58% of its nitrogen oxides; by 2018 its sulphur oxides were down 99.9%, its "
           "nitrogen oxides 95% and its PM2.5 98.5% [5]. The air followed: SO₂ at Kordin, downwind of Marsa, fell "
           f"from {T('C-so2-kordin')} µg/m³ between 2012 and 2015, and at Żejtun, the station nearest Delimara, from "
           f"{T('C-so2-MT00004')} µg/m³ between 2010–12 and 2018–23 (−82%) [3]. The plan shows the same in its own "
           "diffusion-tube maps and in nickel, a marker of fuel oil, at Kordin (pp. 57–58) [2]. NO₂, PM2.5 and PM10 at "
           "Żejtun did not change measurably (for example NO₂ 14.1 to 13.9 µg/m³, 2013–16 to 2018–23) [3]. "
           "<b>This measure is shown to have improved air quality,</b> through sulphur dioxide and fuel-oil metals."))
S.append(KeepTogether([fig(FIG / "fig3_power.png", FW), P(
    "Figure 3. Power-station emissions [5] and sulphur dioxide in the air [3]. The 2015 and 2017 lines mark the "
    "interconnector and Marsa’s closure, and Delimara’s switch to gas [2].", cap)]))
S.append(P("5.2 Grants for more sustainable transport (from 2010)", h2))
S.append(P("The plan lists the scrappage scheme and grants for electric, LPG and other vehicles, and reports uptake, "
           "for example the number of vehicles scrapped each year from 2017 to 2021 (pp. 47–51) [2]. It gives no "
           "measured effect on air quality and says the scrappage scheme “does not address the problem of the "
           "increasing number of vehicles on the road” (p. 47). NO₂ at Msida did fall by 22%, in line with the "
           "inventory’s 23% fall in road-transport exhaust NOx, which reflects a newer fleet [3, 5]. Grants are one "
           "reason a fleet renews; EU emission standards for every new vehicle are another, and the data cannot "
           "separate them. Meanwhile the number of cars rose by 31% between 2013 and 2025 [6]. <b>Plausible, not "
           "shown.</b>"))
S.append(CondPageBreak(60 * mm))
S.append(P("5.3 Free school transport (from September 2018)", h2))
S.append(P("This is the only transport measure for which the plan offers air data. It compares Msida’s average daily "
           "cycle of CO and NO₂ in October–December and June–August, 2014–17 against 2018–19, and reports that the "
           "winter CO peak fell from about 1,200 to about 860 µg/m³ and NO₂ by “around 10 µg/m³” at rush hour, adding "
           "that the falls “can also be attributed to other reasons” (pp. 59–60) [2]. We repeated the comparison with "
           "the EEA’s validated hourly data [3]. The CO figures reproduce: the highest winter hour fell from 1.15 to "
           "0.86 mg/m³. The NO₂ figure does not: at the 07:00 morning peak NO₂ went from "
           f"{float(V('E-NO2-07').split(' → ')[0]):.1f} to {float(V('E-NO2-07').split(' → ')[1]):.1f} µg/m³ (−1.0), "
           "the largest morning fall was 5.0 µg/m³ (10:00–12:00), and the largest falls, 5–7 µg/m³, were in the "
           "evening, when there is no school run."))
S.append(P("Three further tests point away from a school-run effect. (1) The first term with the measure, "
           "October–December 2018, had the highest weekday morning NO₂ at Msida of any year from 2013 to 2023 "
           "(70.3 µg/m³, against 54.3 in 2017) (Figure 4). (2) CO had been falling since 2014, before the measure, and "
           "rose slightly in 2018. (3) Comparing school term with summer holidays, morning NO₂ at Msida fell by "
           "2.5 µg/m³ more in term time between the two periods, but at the Attard background station, away from "
           "the school-run traffic the measure targets, it fell by 2.7 µg/m³ more; at Żejtun it rose by 2.8 [3]. "
           "<b>Not shown.</b>"))
S.append(KeepTogether([fig(FIG / "fig4_school.png", FW), P(
    "Figure 4. Weekday morning rush hour (07:00–09:59) in October–December, each year [3]. A step down from "
    "autumn 2018 would be expected if free school transport had cut the morning school run past Msida.", cap)]))
S.append(P("5.4 Ferry landing places and the fast ferry (2021)", h2))
S.append(P("The plan reports passengers, 1.6 million on the harbour ferries in 2018 and about 42,000 on the two fast "
           "ferries in their first month (pp. 62, 65), and expects fewer car journeys [2]. It gives no air-quality "
           "data for either. PM10 at Msida after June 2021 was no lower than before (Figure 1). <b>No evidence "
           "offered.</b>"))
S.append(CondPageBreak(50 * mm))
S.append(P("5.5 Free public transport for all (from 1 October 2022)", h2))
S.append(P("The plan describes the measure and says it “should further encourage the public to use such modes” "
           "(p. 65) [2]; it offers no measured effect. In the 12 months after it began, PM10 at Msida averaged "
           f"{V('F-PM10-MT00005').split(' → ')[1]} µg/m³ against {V('F-PM10-MT00005').split(' → ')[0]} in the 12 "
           f"months before, with {V('F-days-MT00005').split(' → ')[1]} days over 50 µg/m³ against "
           f"{V('F-days-MT00005').split(' → ')[0]}; NO₂ at Msida was flat ({T('F-NO2-MT00005')} µg/m³). Of 11 "
           "station and pollutant pairs with a full year on both sides, 10 were higher and one (PM10 at Għarb) "
           "0.1 µg/m³ lower [3]. A year is short and weather varies, but the measure has not yet shown up in any "
           "station’s data. <b>Not shown.</b>"))
S.append(KeepTogether([fig(FIG / "fig5_free_pt.png", FW), P(
    "Figure 5. Twelve months before and after free public transport for all began [3]. St Paul’s Bay is left out "
    "(monitoring began in 2022, so the earlier window is incomplete).", cap)]))

# ================================================================== 6
S.append(CondPageBreak(75 * mm))
S.append(SectionHeading(6, "Where the evidence points different ways"))
S.append(contested(
    "Q1  Can free public transport improve air quality?", "MIXED; NOT SHOWN IN MALTA", AMBER,
    "In Luxembourg, the first country to make all public transport free (March 2020), a synthetic "
    "difference-in-differences study estimates a 5.9% fall in road-transport CO₂, with larger effects for nitrogen "
    "oxides, corroborated by traffic counters and air-quality stations [10]. Transport Malta has reported rising "
    "ridership (" + DIAM + " news report, not read).",
    "Spain’s large fare discounts from September 2022 produced “no evidence” of better air quality [11]. In Malta, "
    "no station improved in the year after October 2022, and PM10 at Msida worsened [3].",
    "<b>For this claim:</b> the measure can plausibly help, as Luxembourg shows, but whether it has in Malta is "
    "untested. A ridership rise is an input; the claim is about the outcome."))
S.append(contested(
    "Q2  Did the named transport measures lower NO₂ at Msida?", "POSSIBLE; NOT ATTRIBUTABLE", AMBER,
    "NO₂ at the Msida roadside fell by 22% between 2015–17 and 2021–23, and its excess over the background by 30%, "
    "a period that includes free school transport, the grants and the fast ferry [3].",
    "The fall matches the inventory’s fall in road-transport exhaust NOx (−23%), which follows fleet renewal under EU "
    "standards [5]; the first school term with free transport had the highest morning NO₂ since 2013; no traffic "
    "counts or travel surveys tie the fall to any measure; car numbers rose 31% [6].",
    "<b>For this claim:</b> the air at the roadside improved for NO₂, which counts in ERA’s favour, but the plan does "
    "not show that its named measures caused it."))

# ================================================================== 7
S.append(CondPageBreak(95 * mm))
S.append(SectionHeading(7, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> The reform in the power generation sector has contributed to improvements in air quality"),
     C("Power-station sulphur oxides −99.9% and nitrogen oxides −95%, 2008 to 2018 [5]; SO₂ in the air 16.0 to "
       "1.5 µg/m³ at Kordin (2012 to 2015) and −82% at Żejtun [3]; nickel down at Kordin (plan) [2]."),
     verd("SUPPORTED", GREENC)],
    [C("<b>B.</b> Grants for more sustainable transport have contributed"),
     C("The plan gives uptake, not effect [2]. NO₂ at Msida −22%, matching the modelled −23% in road exhaust NOx "
       "from a newer fleet, which grants are one cause of [3, 5]; cars +31% [6]."),
     verd("PLAUSIBLE, NOT SHOWN", AMBER)],
    [C("<b>C.</b> Free school transport (from 2018) has contributed"),
     C("The plan’s NO₂ fall of “around 10 µg/m³” at rush hour does not reproduce (−1.0 at 07:00); autumn 2018 had "
       "the highest morning NO₂ of 2013–2023; the term-time change matches the Attard background [2, 3]."),
     verd("NOT SHOWN", ORANGE)],
    [C("<b>D.</b> Better ferry landing places and the fast ferry (2021) have contributed"),
     C("The plan reports passengers only (1.6 million in 2018; about 42,000 in the fast ferries’ first month) "
       "[2]. No air data offered."),
     verd("NO EVIDENCE OFFERED", ORANGE)],
    [C("<b>E.</b> Free public transport for all (from October 2022) has contributed"),
     C("The plan offers no measured effect [2]. In the year after it began, 10 of 11 station readings were higher; "
       "Msida PM10 +8.1 µg/m³, 90 days over 50 against 48 [3]."),
     verd("NOT SHOWN", ORANGE)],
    [C("<b>F.</b> Msida exceeded the PM10 daily limit in 2018 and 2023 (the plan’s reason)"),
     C("ERA’s reports: 41 and 52 days after natural deduction, 86 and 84 before; 35 allowed [4]. 2023 is the "
       "highest of 2015–2025."),
     verd("ACCURATE", GREENC)],
], [52 * mm, 88 * mm, 30 * mm], valign="MIDDLE"))
S.append(Spacer(1, 3 * mm))
S.append(P("<b>The speaker’s own reasoning.</b> For five of the six measures the plan counts what was done (grants paid, "
           "passengers carried, students served) as the result. Its Annex I sets a different standard for the new "
           "measures: for core measures “all efforts will be made to quantify the improvement in air quality” (p. 95) "
           "[2]. The statement that past measures “have already contributed” has not been held to that standard."))

# ================================================================== 8
S += [CondPageBreak(95 * mm), Spacer(1, 4 * mm), SectionHeading(8, "Verdict and requests for evidence"),
      verdict_box("Not substantiated", "Power-sector reform is shown to have improved the air; the five transport "
                  "measures named have not been. Confidence: moderate. Missing evidence, not evidence against."),
      Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) For the power-sector reform the plan and independent data agree: sulphur dioxide "
           "collapsed as the power stations stopped burning fuel oil. (2) For the five transport measures the plan "
           "offers uptake figures or nothing, and its one test does not reproduce. (3) NO₂ and PM2.5 at the roadside "
           "did improve, but in step with fleet renewal as much as with any named measure, and PM10, the pollutant "
           "the plan exists to address, did not: 2023, with the transport measures in place, was the worst year after "
           "natural deductions. The claim is stated more strongly than the evidence allows: <i>Not substantiated</i>."))
S.append(P("<b>Why not Misleading or Contradicted.</b> ERA does not hide the 2018 and 2023 exceedances; it gives them "
           "as the reason for the plan, and the plan says traffic growth has offset gains. And flat or worse PM10 does "
           "not prove the measures did nothing: with 31% more cars, the air might have been worse without them. "
           "<b>Why moderate confidence.</b> The data are extensive and validated, but no weather normalisation or "
           "traffic data were available to settle attribution either way."))
S.append(P("<b>What this verdict does not say.</b> Not that the measures were poor policy, nor that Malta’s air has "
           "not improved (sulphur dioxide, NO₂ and PM2.5 have), nor anything about the plan’s future measures. A "
           "statement the evidence would support: <i>“Power-sector reform has cut sulphur dioxide sharply; NO₂ and "
           "PM2.5 at the roadside are lower than in the mid-2010s, but we have not measured how much is due to our "
           "transport measures, and PM10 at Msida has not improved.”</i>"))
S.append(KeepTogether([P("Evidence we are asking for", h2), requests_list([
    "For each of the six measures, the data or study behind “already yielded positive results”.",
    "The data behind the plan’s Figures 25–26 (hours, time convention, validation status) and how “around "
    "10 µg/m³” was derived.",
    "Transport Malta traffic counts near Msida (for example Blata l-Bajda) and bus ridership, before and after "
    "September 2018 and October 2022.",
    "ERA’s analysis of the local sources of the 2023 PM10 excess at Msida, and a comparison of the old and new "
    "Msida sampling points.",
])]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag),
               P("A right of reply will be sought from the Environment and Resources Authority before this check is "
                 "circulated beyond Miżien’s site, with a fixed deadline (suggested 14 days). Its response will be "
                 "appended and the verdict revisited.", small)],
              bg=AMBER_PALE, bar=AMBER)]

# ================================================================== 9
S += [Spacer(1, 6 * mm), CondPageBreak(70 * mm), SectionHeading(9, "Limitations")]
for l in ["No station-by-station weather normalisation [12]; background stations and ERA’s natural-source deductions "
          "control for shared weather and dust, not for local wind or traffic changes. No traffic data were used.",
          "The Msida monitor moved about 300 m in January 2024 [13]; with no overlapping validated data, 2024–25 are "
          "not compared with earlier years.",
          "Our PM10 day counts from EEA data differ from ERA’s by −1 to +4 a year (2019: 65 against 61); findings use "
          "ERA’s counts where they exist. Inventory road emissions are modelled, not measured.",
          "Hours are as reported to the EEA; a one-hour shift would not produce a 10 µg/m³ morning fall in these data.",
          "ERA’s page and plan were read from Wayback copies saved on 5 October 2026 (the archive was unreachable on "
          "6 October); ERA’s consultation report was not read. Two papers were read as abstracts; [8] is "
          "second-hand " + DIAM + "."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Environment and Resources Authority. Air Quality Plan for Malta 2025 (web page; published 12 Mar 2025 per "
          "page metadata). Read through the Wayback Machine capture of 15 Aug 2025.",
     "https://web.archive.org/web/20250815211515/https://era.org.mt/air-quality-plan-for-malta-2024/"),
    ("2", "Environment and Resources Authority (2025). Air Quality Plan for Malta (approved policy), 104 pp., ISBN "
          "978-9918-628-10-0. Read in full; page numbers are the printed pages.",
     "https://era.org.mt/wp-content/uploads/2025/02/DIGITAL-Air-Quality-Plan.pdf"),
    ("3", "European Environment Agency. Air Quality download service: Malta, PM10, PM2.5, NO₂, SO₂ and CO, all "
          "sampling points (AirBase; E1a validated, 2013–2025). Retrieved 6 Oct 2026; file list and SHA-256 in "
          "data/cc-034/eea_files.csv.", "https://eeadmz1-downloads-api-appservice.azurewebsites.net/"),
    ("4", "Environment and Resources Authority. Air Quality e-Reporting, dataflow G (attainment), Malta, 2015–2025. "
          "Eionet Central Data Repository. Retrieved 6 Oct 2026.", "https://cdr.eionet.europa.eu/mt/eu/aqd/g/"),
    ("5", "Eurostat. env_air_emis, Air pollutants by source sector (source: EEA), Malta; updated 7 Sep 2026, "
          "retrieved 6 Oct 2026.", "https://ec.europa.eu/eurostat/databrowser/view/env_air_emis/default/table"),
    ("6", "Eurostat. road_eqs_carpda, Passenger cars by type of motor energy; road_eqs_carhab, per 1,000 "
          "inhabitants. Retrieved 6 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/road_eqs_carpda/default/table"),
    ("7", "Scerri M.M., Weinbruch S., Delmaire G., Mercieca N., Nolle M., Prati P., Massabò D. (2023). Exhaust and "
          "non-exhaust contributions from road transport to PM10 at a Southern European traffic site. "
          "<i>Environmental Pollution</i> 316:120569. doi:10.1016/j.envpol.2022.120569. (Abstract read.)",
     "https://doi.org/10.1016/j.envpol.2022.120569"),
    ("8", "Scerri M.M., Kandler K., Weinbruch S. (2016). Disentangling the contribution of Saharan dust and marine "
          "aerosol to PM10 levels in the Central Mediterranean. <i>Atmospheric Environment</i> 147:395–408. "
          "doi:10.1016/j.atmosenv.2016.10.028. ◆ (Known from the plan’s summary.)",
     "https://doi.org/10.1016/j.atmosenv.2016.10.028"),
    ("9", "Fenech S., Aquilina N.J., Vella R. (2021). COVID-19-related changes in NO₂ and O₃ concentrations and "
          "associated health effects in Malta. <i>Frontiers in Sustainable Cities</i> 3:631280. "
          "doi:10.3389/frsc.2021.631280. (Full text read, CC BY.)", "https://doi.org/10.3389/frsc.2021.631280"),
    ("10", "Eibinger T., Fernando S. (2026). Zero fare, cleaner air? The causal effect of Luxembourg’s free public "
           "transportation policy on transport emissions. <i>Environmental and Resource Economics</i> 89:45. "
           "doi:10.1007/s10640-026-01090-5. (Authors’ copy read, CC BY.)",
     "https://doi.org/10.1007/s10640-026-01090-5"),
    ("11", "Albalate D., Borsati M., Gragera A. (2024). Free rides to cleaner air? Examining the impact of massive "
           "public transport fare discounts on air quality. <i>Economics of Transportation</i> 40:100380. "
           "doi:10.1016/j.ecotra.2024.100380. (Abstract read.)", "https://doi.org/10.1016/j.ecotra.2024.100380"),
    ("12", "Grange S.K., Carslaw D.C., Lewis A.C., Boleti E., Hueglin C. (2018). Random forest meteorological "
           "normalisation models for Swiss PM10 trend analysis. <i>Atmospheric Chemistry and Physics</i> "
           "18:6223–6239. doi:10.5194/acp-18-6223-2018. (Abstract read.)", "https://doi.org/10.5194/acp-18-6223-2018"),
    ("13", "Miżien, Claim Check 008: Msida sampling points from ERA’s dataset D 2025 (data/cc-008/aq_stations.csv); "
           "distance between the old and new points 301 m (data/cc-008/checks.csv).", ""),
    ("14", "European Environment Agency. Particulate matter (PM10): annual limit value for the protection of human "
           "health (limit values of Directive 2008/50/EC). Read 6 Oct 2026.",
     "https://www.eea.europa.eu/en/analysis/maps-and-charts/particulate-matter-pm10-annual-limit-value-for-the-protection-of-human-health-3"),
    ("15", "Miżien. Data and calculations: data/cc-034/; tools/cc-034-report/calc.py.", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "6 Oct 2026", "First issue. Draft verdict Not substantiated (moderate); pending right of "
                    "reply from the Environment and Resources Authority.")])

build_report(Report(
    number="034", out=str(FIG / "report.pdf"), kicker="Air quality",
    title_lines=["Cleaner air,", "already?"],
    subtitle_lines=["Testing ERA’s statement that measures in the Air Quality", "Plan have already improved Malta’s air"],
    quote_lines=["“The plan outlines actions that have already", "yielded positive results for Malta’s air quality…”"],
    quote_size=15,
    attribution="Environment and Resources Authority, Air Quality Plan for Malta 2025 web page, 12 March 2025.",
    context="The plan names six measures, from power-sector reform to free public transport for all.",
    verdict="Not substantiated", verdict_note="Power reform shown to help; transport measures not shown",
    footer_lines=["Version 1.0  ·  6 October 2026", "Status:",
                  "Prepared from public sources, EEA and ERA monitoring data and Eurostat.",
                  "Repository: github.com/leandergrech/Mizien"],
    running_head="Air Quality Plan: results already? – Malta", version="1.0", date="6 October 2026",
    pdf_title="Cleaner air, already? Claim Check 034",
    pdf_subject="Tests ERA's statement that measures named in the Air Quality Plan for Malta have already improved air "
                "quality, against EEA station data, ERA's attainment reports and Eurostat",
    story=S))
