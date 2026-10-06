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
G_ALL = V("G-eea-winter-peaks").split(";")[0].replace("all days ", "").split(" → ")   # winter peak, all days: 2014-17, 2018-19
S = []
LG = colors.HexColor("#8DB36B")
FW = 0.88 * CW   # figure width


capS = ParagraphStyle("capS", parent=cap, spaceAfter=4)   # figure captions: tighter than the default


def SH(num, title, need=22 * mm):
    """Section heading that stays with the first lines after it (no keep-together of a long paragraph)."""
    h = SectionHeading(num, title)
    h.keepWithNext = False
    return [CondPageBreak(need), h]


def H2(text, need=19 * mm):
    return [CondPageBreak(need), P(text, h2)]



# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("The Environment and Resources Authority (ERA) says its Air Quality Plan “outlines actions that have already "
        "yielded positive results for Malta’s air quality” [1]. The plan names six, from “the reform in the power "
        "generation sector” to “free public transport for all” [2], and we rate the claim as applying to those six. We "
        "tested it against validated measurements from every ERA station (2006–2025), ERA’s reports to the European "
        "Environment Agency (EEA) and Malta’s emissions inventory.", lead)]
S.append(key_points([
    ("The power-sector reform did clean the air.",
     "Sulphur oxides from power stations fell 99.8% between 2014 and 2018, the reform years [5] (99.9% since 2008, "
     "though 55% of that fall came before 2015); sulphur dioxide in the air fell 83% at Żejtun [3]."),
    ("NO₂ and PM2.5 at the Msida roadside are lower than in 2015–17",
     f"({T('B-NO2-msida')} and {T('B-PM2.5-msida')} µg/m³, 2015–17 to 2021–23) [3], in step with a cleaner vehicle "
     "fleet [5]. The data cannot tie this to any named measure."),
    ("PM10, the reason for the plan, did not improve.",
     "After ERA deducts dust and sea salt, Msida had 52 days over the daily limit in 2023 (35 allowed), the most of "
     "2015–2023 at the old monitor, with the transport measures in place [4]. The monitor moved in 2024, so later "
     "counts are not comparable."),
    ("The transport measures come with uptake figures, not results.",
     "The plan’s one test, of free school transport, does not reproduce in the EEA data; in the year after free "
     "public transport began, 10 of 11 station readings rose [3]."),
    ("Verdict: not substantiated (moderate confidence).",
     "Missing evidence, not proof that the measures did nothing. Pending right of reply from ERA."),
]))
S += [Spacer(1, 4 * mm), VerdictMeter(2), Spacer(1, 3 * mm),
      tiles([("−99.8%", GREEN, "Sulphur oxides from power stations, 2014 to 2018 (the reform years) [5]"),
             ("−22%", GREEN, "NO₂ at the Msida roadside, 2015–17 to 2021–23; cause not isolated [3]"),
             ("52 days", RED, "Msida PM10 over the daily limit in 2023 after natural deductions; 35 allowed (one site, one year) [4]"),
             ("+8.1", ORANGE, "µg/m³ PM10 at Msida in the year after free public transport began (one site, one year) [3]")]),
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
S += SH(1, "The claim and what we could verify")
S.append(P("The statement is on ERA’s web page for the plan, dated 12 March 2025 in the page’s metadata [1]. The page "
           "says “actions” without listing them; the plan’s executive summary names them [2]. The claim record combines "
           "the two documents, so each is quoted with its own source below. The plan was approved under Article 51 of "
           "the Environment Protection Act (Cap. 549) [1]. <b>What we rate.</b> Read alone, “actions that have already "
           "yielded positive results” is met by any one action that worked, and the power-sector reform did. We read "
           "“actions” as the six measures in the plan’s executive summary [2]; that reading is ours, and the verdict "
           "applies to it."))
S.append(std_table([
    [C("What was said", cellh), C("Where", cellh), C("Our access", cellh)],
    [C("“The plan outlines actions that have already yielded positive results for Malta’s air quality, measures "
       "committed to by the Government for imminent implementation, and additional proposed measures …”"),
     C("ERA web page, Air Quality Plan for Malta 2025 [1]"), C("Read in full (Wayback capture of 15 Aug 2025)")],
    [C("“…measures from other policy documents that have already contributed to improvements in air quality in Malta, "
       "such as the reform in the power generation sector, grants for more sustainable transport, free school "
       "transport, improvement of ferry landing places, a fast ferry link between the main islands and free public "
       "transport for all.”"),
     C("Plan, executive summary, p. 3 [2]"), C("Pages 3, 21–67, 91, 95 read; the rest skimmed (section 9)")],
    [C("The Msida station “exceeded the allowed number of exceedances for the daily limit value of particulate matter "
       "(PM10)”, on ERA’s assessment of 2018 and 2023 data."),
     C("ERA web page [1]; plan, p. 25 [2]"), C("Page read in full; p. 25 read")],
], [92 * mm, 44 * mm, 34 * mm]))
S += [Spacer(1, 3 * mm),
      callout([P("FAIRNESS NOTE", tag),
               P("The plan is candid about the limits of past action: most 2010-plan measures were carried out, yet the "
                 "exceedances returned because of population growth, traffic flows and vehicle registrations (p. 28), "
                 "and cleaner vehicles are “masked by the rising number of vehicles” (p. 54) [2]. This check does not "
                 "assess the plan’s future measures.", small)],
              bg=AMBER_PALE, bar=AMBER), Spacer(1, 3 * mm)]

# ================================================================== 2
S += SH(2, "Method")
S.append(P("<b>Evidence.</b> All validated measurements Malta reported to the EEA for PM10, PM2.5, nitrogen dioxide (NO₂), "
           "sulphur dioxide (SO₂) and carbon monoxide (CO), from every ERA station, 2006–2025 (85 files, retrieved "
           "6 October 2026) [3]; ERA’s attainment reports for 2015–2025 (PM10 exceedances before and after deduction of "
           "natural sources) [4]; the emissions inventory [5]; car numbers [6]. Every figure is recomputed by "
           "<i>tools/cc-034-report/calc.py</i> from <i>data/cc-034/</i> (see <i>checks.csv</i>). "
           "<b>Attribution.</b> Three controls: (1) background stations (the plan notes that natural sources affect “the "
           "entire monitoring network in a similar manner”, p. 25 [2], so Msida’s excess over rural Għarb or urban Żejtun "
           "and Attard removes shared dust, sea salt and weather); (2) ERA’s own deduction of Saharan dust and sea salt "
           "[4]; (3) before-and-after windows at the traffic site and the controls. We did not normalise for weather "
           "station by station [12] (section 9)."))
S.append(P("<b>Time stamps.</b> The EEA’s hourly values carry a <i>Start</i> time, the beginning of the hour on a fixed "
           "clock without daylight saving: all 22 days on which Malta’s clocks changed in 2013–2023 have 24 values, "
           "and Msida’s NO₂ peaks at Start 06 in summer and (but for 2014) 07 in winter, as traffic following local time "
           "gives on a fixed clock [3]; the EEA documents hourly times as UTC+1 [16] ◆. The plan states no convention for its hours; "
           "section 5.3 tests which its curves follow. <b>Grades:</b> official statistics C; the plan’s statements of "
           "effect without data D; peer-reviewed observational studies B. <b>Verdicts</b> follow Appendix A."))

# ================================================================== 3
S += SH(3, "What moves Malta’s air")
S.append(P("<b>PM10 at Msida is mostly not exhaust.</b> A source apportionment of 209 samples taken at the Msida "
           "traffic site in 2018 attributes 3.4% of PM10 to vehicle exhaust, 17% to tyre and brake wear and 18% to road "
           "dust and crustal material [7]; the plan’s account of the study adds sea salt (23%) and Saharan dust (21%) "
           "[2]. The authors found “no discernible trend” in Msida’s PM10 over the preceding decade and concluded that "
           "traffic policies will have “a minimal effect unless the non-exhaust emissions are adequately controlled” "
           "[7]. The inventory agrees: road exhaust PM10 fell from 82 t (2015) to 33 t (2023) while tyre, brake and road "
           "wear stayed at about 100 t [5]. So cleaner engines barely touch PM10; fewer vehicle-kilometres can. At rural "
           "Għarb, natural and regional sources make up most of the PM10 (the plan’s summary of [8] ◆). <b>NO₂ is the "
           "clearest traffic signal:</b> during the 2020 lockdowns monthly NO₂ at Msida was up to 54% below business as "
           "usual [9]. <b>SO₂ and nickel</b> trace the heavy fuel oil burned to 2015–17 [2]."))

# ================================================================== 4
S += SH(4, "What the data show")
S.append(KeepTogether([fig(FIG / "fig1_pm10_days.png", FW), P(
    "Figure 1. Days with PM10 above 50 µg/m³ at Msida (bars and Għarb: our counts from EEA daily values; red line: "
    "ERA’s count after deduction, dataflow G). Before the deduction of natural sources every year of 2013–2023 was "
    "over the 35 allowed [14]; after it, 2018 (41 days) and 2023 (52) were [4]. Għarb had fewer such days in 2023 (8) "
    "than in 2018 (12), so 2023 was not a dust year. The monitor moved about 300 m in January 2024 [13]: ERA’s "
    "2024–25 counts (hollow) are zone counts from other stations, not comparable. Markers: start of each measure "
    "(plan, sections 10.11, 11); one gas-oil unit stayed on standby at Marsa (plan, p. 57).", capS)]))
S.append(KeepTogether([std_table([
    [C("Indicator, Msida unless stated", cellh), C("2015–17", cellh), C("2021–23", cellh), C("Change", cellh),
     C("Grade", cellh)],
    [C("PM10, annual mean (µg/m³)"), C(V("B-PM10-msida").split(" → ")[0]), C(V("B-PM10-msida").split(" → ")[1]),
     C("+0.1"), grade_tag("C")],
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
], [78 * mm, 22 * mm, 22 * mm, 30 * mm, 18 * mm]),
    P("Means of the three annual means per period, without 2020 (lockdowns); NO₂ at Msida had 83% valid data in 2015; "
      f"with 2022–23 alone, {V('B-NO2-msida-2223').split(' → ')[0]} to {V('B-NO2-msida-2223').split(' → ')[1]} µg/m³ "
      "(−20%). Sources: EEA [3], ERA [4]; <i>checks.csv</i> [15].", capS)]))
S.append(KeepTogether([fig(FIG / "fig2_annual.png", FW), P(
    "Figure 2. Annual means: roadside NO₂ and PM2.5 at Msida fell while the background stations changed little; PM10 "
    "did not fall. Hollow: under 85% of the year valid. Attard has PM10 only from 2024; the Msida monitor moved in "
    "January 2024 (dashed). Dashed verticals: Sept 2018 and Oct 2022 (see Figure 1). Source: EEA [3].", capS)]))

# ================================================================== 5
S += SH(5, "Measure by measure")
S += H2("5.1 Power-sector reform (2015–2017)")
_e = lambda k: V(k).replace(",", "").split(" → ")   # emissions: 2008, 2014, 2018, 2024 (tonnes)
S.append(P("The interconnector to Sicily opened in April 2015, the Marsa power station was decommissioned in 2015 (one "
           "gas-oil unit stayed on standby) and from 2017 Delimara ran wholly on natural gas (plan, p. 57) [2]. The plan "
           "also credits an earlier shift to low-sulphur fuel for part of the fall in sulphur dioxide (pp. 41–42, 58). "
           "In 2008 the power sector produced 97% of Malta’s sulphur oxides and 58% of its nitrogen oxides. Its sulphur "
           f"oxides fell from {int(_e('C-emis-SOx')[0]):,} t (2008) to {int(_e('C-emis-SOx')[1]):,} t (2014), before the "
           f"reform, and to {int(_e('C-emis-SOx')[2]):,} t (2018): −99.8% from 2014, −99.9% from 2008, 55% of which came "
           "before 2015; nitrogen oxides fell 90% from 2014 (95% from 2008) and PM2.5 97% [5]. In the air, SO₂ at Żejtun, "
           f"nearest Delimara, fell from {T('C-so2-MT00004').split(' to ')[0]} µg/m³ (2008–12, without 2011, when only "
           f"28.5% of the year was measured) to {T('C-so2-MT00004').split(' to ')[1]} (2018–23): −83%, or −68% from the 2013–16 mean. "
           "Since 1 January 2020 ships outside emission control areas have had to burn fuel with 0.5% sulphur, down from "
           "3.5% [17]; the data cannot separate that from the reform [3]. SO₂ at Kordin, downwind of Marsa, was already "
           f"{T('C-so2-kordin').split(' to ')[0]} µg/m³ in 2014 (98% of the year measured) and "
           f"{T('C-so2-kordin').split(' to ')[1]} in 2015, so it shows no step at the reform; its higher 2010–13 values "
           "rest on 10–62% of the year, and the monitor closed in 2016 [3]. The plan shows the fall in its diffusion-tube "
           "maps and in nickel, a fuel-oil marker, at Kordin (pp. 57–58) [2]. NO₂, PM2.5 and PM10 at Żejtun did not "
           "change measurably (NO₂ 14.1 to 13.9 µg/m³) [3]. <b>This measure is shown to have improved air quality,</b> "
           "through sulphur dioxide and fuel-oil metals, though part of the fall came before it."))
S.append(KeepTogether([fig(FIG / "fig3_power.png", FW), P(
    "Figure 3. Power-station emissions (A: Eurostat, NFR 1A1a [5]) and sulphur dioxide in the air (B: EEA validated "
    "data, AirBase before 2013 [3]; hollow markers: under 85% of hours valid, as at Kordin 2010–13). Lines: "
    "interconnector and Marsa’s decommissioning (2015), Delimara on gas (2017) [2].", capS)]))
S += H2("5.2 Grants for more sustainable transport (from 2010)")
S.append(P("The plan lists the scrappage scheme and grants for electric, LPG and other vehicles and reports uptake, such "
           "as vehicles scrapped each year in 2017–21 (pp. 47–51) [2]; it gives no measured air effect and says the "
           "scheme “does not address the problem of the increasing number of vehicles on the road” (p. 47). NO₂ at "
           "Msida fell 22%, in line with the modelled inventory’s 23% fall in road-transport exhaust NOx (2,546 t in 2015 to "
           "1,950 t in 2022) from a newer fleet [3, 5]. Grants are one reason a fleet renews; EU emission standards for "
           "new vehicles are another, and the data cannot separate them, while passenger cars rose 31% (256,096 in 2013 "
           "to 335,693 in 2025) [6]. <b>Plausible, not shown.</b>"))
S += H2("5.3 Free school transport (from September 2018)")
S.append(P("This is the only transport measure for which the plan offers air data: Msida’s average daily cycles of CO and "
           "NO₂ in October–December and June–August, 2014–17 against 2018–19. It reports the winter CO peak falling from "
           "about 1,200 to about 860 µg/m³ and NO₂ by “around 10 µg/m³” at rush hour, and that the falls “can also be "
           "attributed to other reasons” (pp. 59–60) [2]. We repeated the comparison with the EEA’s hourly data [3] and "
           "read the plan’s Figure 26 off the PDF (±1 µg/m³ at the peaks) [15]. <b>Peaks.</b> CO reproduces peak to peak "
           "(1.15 to 0.86 mg/m³), though its highest hour moves from Start 07 to 06 (06 in 2017–18, 07 in the other "
           f"years). NO₂ does not: the EEA’s winter profile peaks at Start 07 in both periods, {G_ALL[0]} then {G_ALL[1]} "
           "µg/m³ (−1.0), whatever shift is applied to both periods; on weekdays only, 68.0 then 68.7 (+0.7)."))
S.append(P("<b>The plan’s curves.</b> Its peaks are about 70 (label 07, 2014–17) and 61 (label 08, 2018–19), a fall of "
           "about 8. The 2018–19 curves match the EEA data (RMSE 0.2 µg/m³, winter and summer) only if the "
           "plan’s label is the EEA’s Start plus one hour (hour-ending); with the EEA’s labels the error is 7.0 and 5.3. "
           "The 2014–17 curves match under neither (best RMSE 5.0 winter, 2.7 summer; no subset of years 2013–2019 does "
           "better than 3.9 for winter): the plan’s peak of about 70 compares with 62.3 in the EEA’s all-days profile and "
           "68.0 on weekdays only. So the plan’s gap sits in its 2014–17 baseline, whose hour convention and data basis "
           "we cannot establish; a one-hour offset between the periods alone gives a fall of this size (62.3 at Start 07 "
           "in 2014–17 against 54.8 an hour earlier in 2018–19: −7.5)."))
S.append(P("<b>Further tests.</b> (1) Sustained fall: Msida’s weekday-morning NO₂ in October–December averaged 60.4 µg/m³ "
           "in 2013–17 and 48.9 in 2019–23, a fall of 11.5, similar to the plan’s “around 10” [3]. But the step came in "
           "2019: October–December 2018, the first term with the measure, was the highest of 2013–2023 (70.3, against 54.3 "
           "in 2017) (Figure 4); the later window includes the 2020–21 lockdown years, and there is no control for fleet "
           "renewal. (2) CO was falling from 2014, before the measure, and rose slightly in 2018. (3) Term against summer "
           "holidays, morning NO₂ fell 2.5 µg/m³ more in term time at Msida and 2.7 more at Attard, which we use as a "
           "control for city-wide change, and rose 2.8 at Żejtun [3]. <b>Not shown.</b>"))
S.append(KeepTogether([fig(FIG / "fig4_school.png", FW), P(
    "Figure 4. Weekday mornings (07:00–09:59 Start) in October–December [3]; a step down from autumn 2018 would be "
    "expected if free school transport had cut the school run past Msida. Hollow markers: under 85% of the mornings’ "
    "hours valid (Msida NO₂ 2014: 57%, 2015: 73%, 2017: 84%). Dotted: Msida means 2013–17 and 2019–23. The fixed "
    "window is shaky for CO, whose peak hour moves between 06 and 07; no CO at Attard or Żejtun; 2016 CO has no valid "
    "hours.", capS)]))
S += H2("5.4 Ferry landing places and the fast ferry (2021)")
S.append(P("The plan reports passengers, 1.6 million on the harbour ferries in 2018 and about 42,000 on the two fast "
           "ferries in their first month (pp. 62, 65), and expects fewer car journeys [2]. It gives no air-quality data "
           "for either. PM10 at Msida after June 2021 was no lower than before (Figure 1). <b>No evidence offered.</b>"))
S += H2("5.5 Free public transport for all (from 1 October 2022)")
S.append(P("The plan describes the measure and says it “should further encourage the public to use such modes” "
           "(p. 65) [2]; it offers no measured effect. In the 12 months after it began, PM10 at Msida averaged "
           f"{V('F-PM10-MT00005').split(' → ')[1]} µg/m³ against {V('F-PM10-MT00005').split(' → ')[0]} in the 12 "
           f"months before, with {V('F-days-MT00005').split(' → ')[1]} days over 50 µg/m³ against "
           f"{V('F-days-MT00005').split(' → ')[0]}; NO₂ was flat ({T('F-NO2-MT00005')} µg/m³). Of 11 station and "
           "pollutant pairs with a full year on both sides, 10 were higher and one (PM10 at Għarb) 0.1 µg/m³ lower [3]. "
           "One year at one site, unadjusted for weather, is a weak test, and local sources the measures do not target "
           "also moved: inventory PM10 from construction and demolition rose from 80 t (2013) to 370 t (2023) [5], and "
           "the Msida Creek works lie 112 m from the old monitor [13] (we could not verify when work near it began). "
           "Elsewhere the evidence is mixed: Luxembourg’s free public transport (March 2020) cut road-transport CO₂ by an "
           "estimated 5.9%, with larger effects for nitrogen oxides [10], while Spain’s large fare discounts of 2022 "
           "produced “no evidence” of better air quality [11]. In Malta the measure has not shown up in any station’s "
           "data (daily values; St Paul’s Bay is left out because "
           "monitoring began in 2022, and Attard had no PM10 monitor before 2024; no weather adjustment). "
           "<b>Not shown.</b>"))

# ================================================================== 6
S += SH(6, "Where the evidence points different ways", 80 * mm)
S.append(contested(
    "Did the named transport measures lower NO₂ at Msida?", "POSSIBLE; NOT ATTRIBUTABLE", AMBER,
    "NO₂ at the Msida roadside fell 22% between 2015–17 and 2021–23 and its excess over the background 30%, in a "
    "period with free school transport, the grants and the fast ferry; weekday-morning NO₂ in October–December fell "
    "11.5 µg/m³ between 2013–17 and 2019–23, close to the plan’s “around 10” [3].",
    "The fall matches the inventory’s −23% in road-transport exhaust NOx from fleet renewal under EU standards [5]; "
    "the first school term with free transport was the highest since 2013 and the step down came in 2019; no traffic "
    "counts or surveys tie the fall to any measure; cars +31% [6].",
    "<b>For this claim:</b> roadside NO₂ improved, which counts in ERA’s favour, but the plan does not show that its "
    "named measures caused it."))

# ================================================================== 7
verd = lambda t, c: chip(t, c, w=29 * mm)
S += SH(7, "Testing the claim", 62 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> The reform in the power generation sector has contributed to improvements in air quality"),
     C("Power-station sulphur oxides −99.8% and nitrogen oxides −90%, 2014 to 2018 (−99.9% and −95% from 2008; 55% of "
       "the sulphur fall came before 2015) [5]; SO₂ in the air −83% at Żejtun (2008–12 to 2018–23); Kordin already "
       "2.6 µg/m³ in 2014 [3]; nickel down at Kordin (plan) [2]."),
     verd("SUPPORTED", GREENC)],
    [C("<b>B.</b> Grants for more sustainable transport have contributed"),
     C("The plan gives uptake, not effect [2]. NO₂ at Msida −22%, matching the modelled −23% in road exhaust NOx "
       "from a newer fleet, which grants are one cause of [3, 5]; cars +31% [6]."),
     verd("PLAUSIBLE, NOT SHOWN", AMBER)],
    [C("<b>C.</b> Free school transport (from 2018) has contributed"),
     C("The plan’s NO₂ fall of “around 10 µg/m³” at rush hour does not reproduce: peak to peak −1.0 in the EEA "
       "data, and its 2014–17 baseline cannot be matched; autumn 2018 had the highest morning NO₂ of 2013–2023; a "
       "sustained fall of 11.5 came from 2019 and cannot be tied to the measure; the term-time change matches the "
       "Attard background [2, 3]."),
     verd("NOT SHOWN", ORANGE)],
    [C("<b>D.</b> Better ferry landing places and the fast ferry (2021) have contributed"),
     C("The plan reports passengers only (1.6 million in 2018; about 42,000 in the fast ferries’ first month) "
       "[2]. No air data offered."),
     verd("NO EVIDENCE OFFERED", ORANGE)],
    [C("<b>E.</b> Free public transport for all (from October 2022) has contributed"),
     C("The plan offers no measured effect [2]. In the year after it began, 10 of 11 station readings were higher; "
       "Msida PM10 +8.1 µg/m³, 90 days over 50 against 48 (one site, one year, no weather adjustment) [3]."),
     verd("NOT SHOWN", ORANGE)],
    [C("<b>F.</b> Msida exceeded the PM10 daily limit in 2018 and 2023 (the plan’s reason)"),
     C("ERA’s reports: 41 and 52 days after natural deduction, 86 and 84 before; 35 allowed [4]. 2023 is the "
       "highest of 2015–2023 at the old Msida point; ERA’s 2024–25 counts (20, 23) are zone counts from other "
       "stations."),
     verd("ACCURATE", GREENC)],
], [52 * mm, 88 * mm, 30 * mm], valign="MIDDLE"))
S.append(Spacer(1, 3 * mm))
S.append(P("<b>The speaker’s own reasoning.</b> For five of the six measures the plan counts what was done (grants paid, "
           "passengers carried) as the result, yet for new measures its Annex I says “all efforts will be made to "
           "quantify the improvement in air quality” (p. 95) [2]; past measures have not been held to that standard."))

# ================================================================== 8
S += [Spacer(1, 2 * mm)] + SH(8, "Verdict and requests for evidence", 60 * mm)
S += [verdict_box("Not substantiated", "Power-sector reform is shown to have improved the air; the five transport "
                  "measures named have not been. Confidence: moderate. Missing evidence, not evidence against."),
      Spacer(1, 3 * mm)]
S.append(P("<b>Why.</b> (1) For the power-sector reform the plan and independent data agree. (2) For the five transport "
           "measures the plan offers uptake figures or nothing, and its one test does not reproduce. (3) NO₂ and PM2.5 at "
           "the roadside improved, but in step with fleet renewal as much as with any named measure, and PM10, the "
           "pollutant the plan exists to address, did not: 2023, with the transport measures in place, was the worst year "
           "of 2015–2023 at the old monitor after natural deductions. Read as the plan’s list of six, the claim is stated "
           "more strongly than the evidence allows: <i>Not substantiated</i>."))
S.append(P("<b>Why not Largely supported.</b> One of the six measures has effect evidence (the power-sector reform); for "
           "the other five there is none, and the one test among them, free school transport, does not reproduce. That "
           "is most of the list, not a minor caveat. <b>Why not Misleading or Contradicted.</b> ERA’s page states the "
           "2018 and 2023 exceedances as the reason for the plan, and the plan says traffic growth offset gains; and flat "
           "or worse PM10 does not prove the measures did nothing, with 31% more cars. <b>Why moderate confidence.</b> "
           "The data are extensive and validated, but there is no weather normalisation or traffic data to settle "
           "attribution."))
S.append(P("<b>What this verdict does not say:</b> that the measures were poor policy, that Malta’s air has not improved "
           "(SO₂, NO₂ and PM2.5 have), or anything about the plan’s future measures. A supportable statement: "
           "<i>Power-sector reform has cut sulphur dioxide sharply; roadside NO₂ and PM2.5 are lower than in the "
           "mid-2010s, but we have not measured how much is due to transport measures, and PM10 at Msida has not "
           "improved.</i>"))
S.append(KeepTogether([P("Evidence we are asking for", h2), requests_list([
    "For each of the six measures, the data or study behind “already yielded positive results”.",
    "The data behind the plan’s Figures 25–26: the hour convention and the days and years used for each period’s "
    "curves (we cannot reproduce its 2014–17 NO₂ curve), and how “around 10 µg/m³” was derived.",
    "Transport Malta traffic counts near Msida (for example Blata l-Bajda) and bus ridership, before and after "
    "September 2018 and October 2022.",
    "ERA’s analysis of the local sources of the 2023 PM10 excess at Msida, and a comparison of the old and new "
    "Msida sampling points.",
])]))
S += [Spacer(1, 3 * mm),
      callout([P("RIGHT OF REPLY", tag),
               P("A right of reply will be sought from the Environment and Resources Authority before this check is "
                 "circulated beyond Miżien’s site, with a fixed deadline (suggested 14 days). Its response will be "
                 "appended and the verdict revisited.", small)],
              bg=AMBER_PALE, bar=AMBER)]

# ================================================================== 9
S += [Spacer(1, 3 * mm)] + SH(9, "Limitations", 50 * mm)
for l in ["<b>Wording rated:</b> the six measures the plan names (section 1); read as <i>any action that worked</i>, the "
          "power-sector reform alone would meet the claim. <b>Weather and traffic:</b> no weather normalisation [12] and "
          "no traffic data; the 2023 count (52 days) and the +8.1 µg/m³ after free public transport are single-site, "
          "single-year comparisons.",
          "<b>Monitor and works:</b> the Msida monitor moved about 300 m in January 2024 [13] with no overlapping valid "
          "data, so 2024–25 are not compared with earlier years; the Msida Creek works lie 112 m from the old monitor "
          "[13] (when work near it began is not verified). Our PM10 day counts differ from ERA’s by −1 to +4 a year; "
          "findings use ERA’s counts where they exist.",
          "<b>Time labels:</b> the plan states no hour convention; our tests are in section 5.3. The plan’s curves were "
          "read off the PDF (±1 µg/m³ at the peaks).",
          "<b>Access:</b> ERA’s page and plan were read from Wayback copies saved on 5 October 2026 (archive unreachable "
          "on 6 October). Plan pages 3, 21–67, 91 and 95 were read; pp. 4–20, 68–90 and 96–104 were skimmed for effect "
          "estimates of the six measures and none was found, so <i>the plan gives no measured effect</i> means in the pages "
          "read and skimmed. ERA’s consultation report was not read; two papers were read as abstracts; [8] is "
          "second-hand " + DIAM + "."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Environment and Resources Authority. Air Quality Plan for Malta 2025 (web page; dated 12 Mar 2025 in the page "
          "metadata). Wayback capture of 15 Aug 2025.",
     "https://web.archive.org/web/20250815211515/https://era.org.mt/air-quality-plan-for-malta-2024/"),
    ("2", "Environment and Resources Authority (2025). Air Quality Plan for Malta (approved policy), 104 pp. Pages 3, "
          "21–67, 91, 95 read; pp. 4–20, 68–90, 96–104 skimmed for effect estimates; printed page numbers.",
     "https://era.org.mt/wp-content/uploads/2025/02/DIGITAL-Air-Quality-Plan.pdf"),
    ("3", "European Environment Agency. Air Quality download service: Malta, PM10, PM2.5, NO₂, SO₂, CO, all sampling "
          "points (AirBase; E1a validated, to 2025). Retrieved 6 Oct 2026; SHA-256 in data/cc-034/eea_files.csv.",
     "https://eeadmz1-downloads-api-appservice.azurewebsites.net/"),
    ("4", "Environment and Resources Authority. Air Quality e-Reporting, dataflow G (attainment), Malta, 2015–2025 "
          "(Eionet CDR). Retrieved 6 Oct 2026.", "https://cdr.eionet.europa.eu/mt/eu/aqd/g/"),
    ("5", "Eurostat. env_air_emis, Air pollutants by source sector, Malta; updated 7 Sep 2026, retrieved 6 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/env_air_emis/default/table"),
    ("6", "Eurostat. road_eqs_carpda and road_eqs_carhab, passenger cars. Retrieved 6 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/road_eqs_carpda/default/table"),
    ("7", "Scerri M.M., Weinbruch S., Delmaire G., Mercieca N., Nolle M., Prati P., Massabò D. (2023). Exhaust and "
          "non-exhaust contributions from road transport to PM10 at a Southern European traffic site. "
          "<i>Environmental Pollution</i> 316:120569. (Abstract read.)",
     "https://doi.org/10.1016/j.envpol.2022.120569"),
    ("8", "Scerri M.M., Kandler K., Weinbruch S. (2016). Disentangling the contribution of Saharan dust and marine "
          "aerosol to PM10 levels in the Central Mediterranean. <i>Atmospheric Environment</i> 147:395–408. ◆ (Known "
          "from the plan’s summary.)", "https://doi.org/10.1016/j.atmosenv.2016.10.028"),
    ("9", "Fenech S., Aquilina N.J., Vella R. (2021). COVID-19-related changes in NO₂ and O₃ concentrations and "
          "associated health effects in Malta. <i>Frontiers in Sustainable Cities</i> 3:631280. (Full text read, CC BY.)",
     "https://doi.org/10.3389/frsc.2021.631280"),
    ("10", "Eibinger T., Fernando S. (2026). Zero fare, cleaner air? The causal effect of Luxembourg’s free public "
           "transportation policy on transport emissions. <i>Environmental and Resource Economics</i> 89:45. (Authors’ "
           "copy read, CC BY.)", "https://doi.org/10.1007/s10640-026-01090-5"),
    ("11", "Albalate D., Borsati M., Gragera A. (2024). Free rides to cleaner air? Examining the impact of massive "
           "public transport fare discounts on air quality. <i>Economics of Transportation</i> 40:100380. (Abstract "
           "read.)", "https://doi.org/10.1016/j.ecotra.2024.100380"),
    ("12", "Grange S.K., Carslaw D.C., Lewis A.C., Boleti E., Hueglin C. (2018). Random forest meteorological "
           "normalisation models for Swiss PM10 trend analysis. <i>Atmospheric Chemistry and Physics</i> 18:6223–6239. "
           "(Abstract read.)", "https://doi.org/10.5194/acp-18-6223-2018"),
    ("13", "Miżien, Claim Check 008: Msida sampling points from ERA’s dataset D 2025 (data/cc-008/aq_stations.csv); "
           "old to new point 301 m, old point to the nearest flyover vertex 112 m (data/cc-008/checks.csv).", ""),
    ("14", "European Environment Agency. Particulate matter (PM10): annual limit value for the protection of human "
           "health (Directive 2008/50/EC). Read 6 Oct 2026.",
     "https://www.eea.europa.eu/en/analysis/maps-and-charts/particulate-matter-pm10-annual-limit-value-for-the-protection-of-human-health-3"),
    ("15", "Miżien. Data and calculations: data/cc-034/, tools/cc-034-report/calc.py. The plan’s Figure 26 (p. 60) was "
           "read off the PDF by tools/cc-034-report/digitise_fig26.py.", ""),
    ("16", "European Environment Agency. Data dictionary, Air Quality e-Reporting time series (E1a, E2a): hourly "
           "date-time begin in UTC+1. ◆ (Seen in a web-search summary on 6 Oct 2026; page not opened.)", ""),
    ("17", "International Maritime Organization. IMO 2020 – cutting sulphur oxide emissions (0.50% m/m limit on ships’ "
           "fuel oil outside emission control areas from 1 Jan 2020, down from 3.50%). Read 6 Oct 2026.",
     "https://www.imo.org/en/MediaCentre/HotTopics/Pages/Sulphur-2020.aspx"),
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
    attribution="Environment and Resources Authority, Air Quality Plan for Malta 2025 web page, 12 March 2025 (page metadata).",
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
