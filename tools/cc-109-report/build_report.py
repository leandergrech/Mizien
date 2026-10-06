"""Claim Check 109 report. Run fetch.py, read_graph.py, calc.py and figures.py first. Output: out/report.pdf"""
import csv
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
CHK = {r["check"]: r for r in csv.DictReader(open(HERE.parents[1] / "data" / "cc-109" / "checks.csv"))}


def v(check, fmt="{:.1f}"):
    """A figure from data/cc-109/checks.csv, so the text and the calculations cannot drift apart."""
    return fmt.format(float(CHK[check]["value"]))


SH_PX = v("Transport share of ESR emissions 2024, approximated inventory")                       # 53.3
SH_G = v("Transport share of ESR emissions 2024, the report's own Graph 3.1")                    # 53.3
SH_FIN = v("Transport share of ESR emissions 2024, 2026 inventory (our estimate)")               # 54.8
SH_ROAD = v("Road transport only (1.A.3.b), 2026 inventory, as share of the approximated ESR total, 2024")  # 48.0
SH_ROAD23 = v("Road transport only, share of the reviewed ESR total, 2023")                     # 47.5
CH_G = v("Transport change 2005-2024, the report's own Graph 3.1")                              # 45.0
CH_PX = v("Transport change 2005-2024, inventory 2005 and approximated 2024")                    # 45.0
ROAD_RANGE = CHK["Range of road-transport-only ratios that round to 48%"]["value"].replace("-", "–")  # 47.5–48.3
GAP = v("Gap: approximated-inventory share minus the report's 48%")                              # 5.3
CH_FIN = v("Transport change 2005-2024, 2026 inventory (final submission)")                      # 48.4
CH_ROAD = v("Road transport only (1.A.3.b) change 2005-2024")                                    # 39.4
CH_NAV = v("Domestic navigation (1.A.3.d) change 2005-2024", "{:.0f}")                           # 184
CH_CARS = v("Cars (1.A.3.b.i) change 2005-2024", "{:.0f}")                                       # 34
ROAD_SH = v("Road share of ESR transport, 2024")                                                 # 88.1
NAV_SH = CHK["Domestic navigation share of ESR transport, 2005 and 2024"]["value"].split(" / ")   # 6.2, 11.9
INC_ROAD = v("Share of the 2005-2024 transport increase from road", "{:.0f}")                    # 76
T_PX = v("ESR transport 2024, approximated inventory (1.A.3 total minus 1.A.3.a CO2)", "{:.3f}")  # 0.766
ESR_PX = v("ESR total 2024, approximated inventory", "{:.3f}")                                   # 1.437
REV = v("ESR transport 2024: approximated vs final inventory")                                   # 2.3
SH05 = CHK["Transport share of ESR emissions 2005"]["value"].split(" ")[0]                        # 52.0
SMALL = v("ESR sector share 2024 (approximated): Small industry (residual)", "{:.0f}")            # 19
EU_CH = v("EU-27: ESR transport (1.A.3 - aviation CO2) change 2005-2024")                        # -5.0
A81_T = v("Table A8.1 row vs ESR transport series, 2018-2023: largest difference")               # 0.0
A81_R = v("Table A8.1 row vs road-only series, 2018-2023: largest difference")                   # 6.2
S = []
LG = colors.HexColor("#8DB36B")

# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("In its 2026 Country Report on Malta (3 June 2026), the European Commission wrote: <b>“Transport is the "
        "dominant source of Malta’s effort sharing emissions. It has generated 48% of these emissions in 2024, up by "
        "45% since 2005.”</b> Effort-sharing emissions are those outside the EU’s emissions trading system that count "
        "towards Malta’s binding national target. We recomputed both numbers from the EEA and Eurostat data the report "
        "draws on.", lead)]
S.append(key_points([
    ("Transport is the dominant source.",
     f"On the effort-sharing definition (all domestic transport, with aviation CO<sub>2</sub> excluded) transport was "
     f"{SH_PX}% of Malta’s effort-sharing emissions in 2024; the next sector, small industry, was {SMALL}%. Transport "
     "has been the largest sector in every year since 2005."),
    ("“Up by 45% since 2005” reproduces.",
     f"Transport emissions rose from 0.528 Mt in 2005 to {T_PX} Mt in 2024 on the approximated data the report "
     f"uses: +{CH_PX}%, exactly its figure. That is the rise in emissions; the share barely moved ({SH05}% to "
     f"{SH_G}%). The final 2026 inventory gives +{CH_FIN}%."),
    ("The 48% does not reproduce; the share is 53%.",
     f"The same definition gives {SH_PX}% in the EEA’s approximated inventory and the report’s own Graph 3.1, and 53% "
     f"in the Commission’s climate profile of Malta. Only road transport alone ({ROAD_RANGE}%) gives 48% (our "
     "identification; the report does not say). The 48% understates transport’s share."),
    ("The labels are narrower than the data.",
     "A footnote calls the sector “road transport” and the annex table labels its series “domestic road transport”, "
     f"but the series includes domestic shipping ({NAV_SH[1]}% in 2024). 2024 figures are approximated; final data come "
     "in 2027."),
    ("Verdict: largely supported (high confidence).",
     "The substance holds, and on the report’s own definition transport’s share is larger than stated, not smaller."),
]))
S += [Spacer(1, 3.5 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([(f"{float(SH_PX):.0f}%", GREEN, f"transport’s share of effort-sharing emissions, 2024 (report: 48%)"),
             (f"+{float(CH_G):.0f}%", GREEN, f"transport emissions 2005–2024, approximated data (final inventory +{CH_FIN}%)"),
             ("20 of 20", GREEN, "years since 2005 with transport the largest effort-sharing sector"),
             ("48%", GREY, f"only from road transport alone ({ROAD_RANGE}% of a total; our identification)")]),
      Spacer(1, 4 * mm),
      up_down("A published Commission or EEA series in which transport, as the Effort Sharing Regulation defines it, "
              "is 48% of Malta’s 2024 effort-sharing emissions.",
              "Final, reviewed data (due 2027) showing that transport is not the largest effort-sharing sector, or that "
              f"its emissions rose well under 45% since 2005. The final 2026 inventory points the other way: "
              f"{float(SH_FIN):.0f}% and +{float(CH_FIN):.0f}%."),
      Spacer(1, 4 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What counts as transport, and which data"),
          ("4", "What the data show"), ("5", "Where the evidence points different ways"), ("6", "Testing the claim"),
          ("7", "Verdict and requests for evidence"), ("8", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The claim is the Commission’s own text in a staff working document that accompanies its 2026 recommendation "
           "to the Council on Malta’s economic policies [1]. We read the Commission’s copy and the copy the Council "
           "registered as document 10135/26 ADD 1 in full on 6 October 2026; the wording is the same in both, only the "
           "page numbers differ (Commission copy pages are given here). The quoted sentence carries a footnote mark, "
           "(141), omitted on the cover; the footnote reads “See Table A8.1 at the end of this Annex.”"))
S.append(std_table([
    [C("Where in the report [1]", cellh), C("What it says", cellh), C("Access", cellh)],
    [C("Annex 8, “Sustainable transport”, p. 66 (Council copy p. 72)"),
     C("“Transport is the dominant source of Malta’s effort sharing emissions. It has generated 48% of these emissions "
       "in 2024 (141), up by 45% since 2005.”"), C("Read in full; <b>the claim</b>")],
    [C("Chapter 3, p. 14 (Council p. 15)"),
     C("“In terms of Malta’s effort sharing emissions, transport had a share of 48% in 2024, with emissions up by 45% "
       "since 2005 (see Graph 3.1 and Annex 8).”"), C("Read in full")],
    [C("Summary, p. 6 (Council p. 6)"),
     C("“The transport sector remains the biggest source of Effort Sharing Regulation emissions in 2024 (48%)”"),
     C("Read in full")],
    [C("Graph 3.1, p. 14 (Council p. 16)"),
     C("Effort-sharing emissions by sector, 2005, 2023 and 2024; “Domestic transport (excl. aviation)”; source: "
       "European Environment Agency."), C("Read; values taken from the PDF’s vector paths")],
    [C("Footnote (140) and Table A8.1, pp. 66 and 71 (Council pp. 72, 77)"),
     C("Effort sharing covers “buildings (heating and cooling), road transport, agriculture, waste and small "
       "industry”; 2024 values “are based on approximated inventory data”. Table row “domestic road transport”: "
       "+45.0% in 2024. The table gives no share."), C("Read in full")],
], [42 * mm, 98 * mm, 30 * mm]))
S += [Spacer(1, 2 * mm),
      callout([P("FAIRNESS NOTE", tag),
               P("An EU institution’s assessment of Malta is held to the same standard as a local statement. This check "
                 "covers one sentence and its two figures. The 2030 projection in the same annex (+29.7% with additional "
                 "measures, +42.1% with existing measures, against a −19% target; Table A8.1) is outside this check; "
                 "Claim Checks 003 and 094 cover the Commission’s projections.",
                 small)], bg=AMBER_PALE, bar=AMBER), Spacer(1, 3 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Question.</b> On the effort-sharing definition, was transport the largest source of Malta’s effort-sharing "
           "emissions in 2024, was it 48% of them, and had its emissions risen by 45% since 2005?"))
S.append(P("<b>Evidence.</b> The claim is statistical, so the evidence is the emissions data behind it: the EEA’s "
           "effort-sharing totals for 2005–2024 [4]; the EEA’s approximated (preliminary) inventory for 2024 [5], which "
           "the report uses for 2024; Malta’s final inventory for 2005–2024 as compiled by the EEA in April 2026 [7] and "
           "republished by Eurostat in June 2026 [6]; and the report’s own Graph 3.1, whose bar heights we read from the "
           "PDF’s drawing instructions [1]. We also read the Commission’s climate-progress profiles of Malta [8, 9], its "
           "2025 Country Report [10] and the legal scope of effort sharing [2, 3]. Data were downloaded on 6 October "
           "2026 (<i>tools/cc-109-report/fetch.py</i>, <i>read_graph.py</i>) and every figure is recomputed in "
           "<i>calc.py</i>, with results in <i>data/cc-109/checks.csv</i>. Eurostat sets no flags on the Malta rows "
           "used. A peer-reviewed study of Malta’s transport emissions [11] gives context."))
S.append(P("<b>Grades.</b> Official statistics and legal texts are grade C under our scale. <b>Verdicts</b> follow the "
           "five-point scale in Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(60 * mm))
S.append(SectionHeading(3, "What counts as transport, and which data"))
S.append(P("<b>The legal definition.</b> The Effort Sharing Regulation covers emissions from energy, industrial processes, "
           "agriculture and waste, minus the activities in the EU emissions trading system (ETS), except maritime "
           "transport, which stays in effort sharing [2, 3]. CO<sub>2</sub> from civil aviation (inventory category "
           "1.A.3.a) is “treated as zero” [2]. So effort-sharing transport is all domestic transport (road, domestic "
           "shipping, rail and other) minus domestic-aviation CO<sub>2</sub>. That is what Graph 3.1 calls “Domestic "
           "transport (excl. aviation)” and what the Commission’s climate profiles of Malta use [8, 9]."))
S.append(std_table([
    [C("Inventory category", cellh), C("In effort sharing?", cellh), C("Malta 2005", cellh), C("Malta 2024", cellh),
     C("Change", cellh)],
    [C("1.A.3.b Road transport"), C("Yes"), C("0.495 Mt"), C("0.690 Mt"), C(f"+{CH_ROAD}%")],
    [C("1.A.3.d Domestic navigation"), C("Yes (maritime stays in effort sharing)"), C("0.033 Mt"), C("0.093 Mt"),
     C(f"+{CH_NAV}%")],
    [C("1.A.3.c Rail, 1.A.3.e Other"), C("Yes"), C("not occurring"), C("not occurring"), C("–")],
    [C("1.A.3.a Domestic aviation, CO<sub>2</sub>"), C("No (treated as zero)"), C("0.002 Mt"), C("0.004 Mt"), C("–")],
    [C("<b>Effort-sharing transport</b>"), C(""), C("<b>0.528 Mt</b>"), C("<b>0.784 Mt</b>"), C(f"<b>+{CH_FIN}%</b>")],
], [52 * mm, 50 * mm, 22 * mm, 22 * mm, 24 * mm]))
S.append(P("Malta’s final inventory, 2026 submission (Eurostat env_air_gge, updated 2 June 2026 [6]; identical to the EEA "
           "compilation of 15 March 2026 [7]). Greenhouse gases in CO<sub>2</sub> equivalent; rail and other transport "
           "carry the inventory notation “not occurring”.", cap))
S.append(P(f"Road transport is {ROAD_SH}% of effort-sharing transport in 2024. A peer-reviewed study of Malta’s transport "
           "policy reports, from Malta’s Fourth Biennial Report, a similar split: road transport 87% of transport "
           "CO<sub>2</sub> [11 ◆]. The report’s footnote (140) shortens the sector to “road transport”, and Table A8.1 "
           "labels its series “domestic road transport”; section 4 shows that the series itself includes domestic "
           "shipping."))
S.append(P(f"<b>Approximated and final data.</b> Member States report an approximated inventory for the previous year by 31 "
           "July; the EEA describes it as a preliminary indicator, with the full inventory a year later [5]. The report "
           "uses approximated data for 2024 (footnote 140) and says final effort-sharing figures will be set after a "
           "review in 2027 [1]. Malta’s final inventory for 2024 already exists: due by 15 March 2026 and compiled by the EEA in April [3, 7], it puts "
           f"effort-sharing transport {REV}% above the approximated value [6, 7]. Approximations have moved further "
           "before: for 2023 the 2025 report gave transport +32.2% since 2005 [10], the 2026 report +44.8% [1]."))

# ================================================================== 4
S.append(CondPageBreak(95 * mm))
S.append(SectionHeading(4, "What the data show"))
S.append(KeepTogether([fig(FIG / "fig1_graph31.png", width=CW * 0.8), P(
    "Figure 1. The report’s own Graph 3.1, redrawn from the values in the PDF’s drawing instructions [1]. Transport is "
    f"the largest sector in all three years. In 2024 it is 0.765 of 1.437 Mt, or {SH_G}%; the amber line marks where "
    "48% would fall. The 2024 bars equal the EEA’s approximated inventory [4, 5].", cap)]))
S.append(P(f"<b>The share.</b> The EEA’s approximated inventory gives transport {T_PX} Mt (all transport, 0.767 Mt, minus "
           f"0.9 kt of domestic-aviation CO<sub>2</sub>) of an effort-sharing total of {ESR_PX} Mt: {SH_PX}% [5]. The "
           "EEA builds its total with the same aviation figure, so numerator and denominator match. The report’s Graph "
           f"3.1, which the chapter-3 sentence cites, shows the same {SH_G}%, and the Commission’s own climate-progress "
           "profile of Malta, published in January 2026, prints 53% for the same year and definition, against 39% for "
           "the EU-27 [8]. Its 2024 profile gave 52% for 2023 [9]. With the final 2026 inventory, and our estimate of "
           f"the effort-sharing total, the share is {SH_FIN}% [6]. Small industry is second, at {SMALL}% (Figure 1)."))
S.append(KeepTogether([fig(FIG / "fig2_shares.png"), P(
    "Figure 2. Transport’s 2024 share of Malta’s effort-sharing emissions by source and definition. Every source on the "
    "effort-sharing definition gives 53–55%. Only road transport alone, divided by an effort-sharing total, gives 48%.",
    cap)]))
S.append(P(f"<b>Where could 48% come from?</b> The report does not say. Footnote (141) points to Table A8.1, which gives "
           f"no share. Of the combinations we tried, only ratios of road transport alone ({ROAD_RANGE}%) give 48%: road "
           f"(1.A.3.b, 0.690 Mt) over the approximated effort-sharing total is {SH_ROAD}%, road CO<sub>2</sub> alone "
           f"{v('Road transport only, CO2 only, as share of the approximated ESR total, 2024')}%, road over our "
           f"final-inventory total {v('Road transport only, share of the final-inventory ESR estimate, 2024')}%, and "
           f"road in 2023 {SH_ROAD23}%. The {SH_ROAD}% mixes a final-inventory numerator with an approximated "
           "denominator, because the approximated inventory has no road row. A road-only figure would fit footnote "
           "(140)’s wording (“road transport”), but this is our identification, not a stated method. If it is the "
           f"source, the sentence mixes two scopes: road alone rose +{CH_ROAD}% since 2005, not 45%."))
S.append(KeepTogether([fig(FIG / "fig3_change.png"), P(
    f"Figure 3. Change since 2005 in effort-sharing transport (green) and road transport alone (grey). Table A8.1’s "
    f"“domestic road transport” values (amber) sit on the green line for 2018–2023 (to the table’s one-decimal precision) "
    f"and up to {A81_R} points off the road-only line; its 2024 value, +45.0%, equals our recomputation from the "
    "approximated inventory. The red marker is 2023 as approximated a year earlier.", cap)]))
S.append(P(f"<b>The rise.</b> Effort-sharing transport emitted 0.528 Mt in 2005. On the approximated 2024 data the report "
           f"uses it was {T_PX} Mt: +{CH_PX}% [1, 5], the same as Table A8.1 and Graph 3.1 (+{CH_G}%). The report’s "
           "“45%” is that rise: the chapter-3 sentence says “with emissions up by 45%”, and transport’s share moved only from "
           f"{SH05}% to {SH_G}%. On the final 2026 inventory the rise is +{CH_FIN}% [6], close to the +48.6% Claim Check "
           f"003 found for all domestic transport. Road transport rose +{CH_ROAD}% (cars +{CH_CARS}%) and domestic "
           f"navigation +{CH_NAV}%: road gave {INC_ROAD}% of the increase, shipping the rest, and shipping’s part of "
           f"transport grew from {NAV_SH[0]}% to {NAV_SH[1]}%. Across the EU-27, effort-sharing transport fell "
           f"{EU_CH[1:]}% over the same years [6]."))
S.append(P(f"<b>The 2005 baseline.</b> The approximated 2024 total, {ESR_PX} Mt, is "
           f"{v('ESR total 2024 (approximated) vs the legal 2005 base')}% above Malta’s legal 2005 level of 1,020,601 t "
           "set in Commission Implementing Decision (EU) 2020/2126 [13]: the report’s “40.8% above 2005 levels” [1]. "
           "The EEA’s own 2005 estimate (1.007 Mt [4]) and Graph 3.1’s 2005 bar (1.016 Mt) differ slightly. The "
           "transport growth rate compares transport with itself, so it does not depend on which 2005 total is used."))
S.append(KeepTogether([
    std_table([
        [C("Measure, Malta", cellh), C("Value", cellh), C("Source", cellh), C("Grade", cellh)],
        [C("Transport share of effort-sharing emissions, 2024: report’s text"), C("<b>48%</b>"), C("[1] pp. 6, 14, 66"),
         grade_tag("C")],
        [C("Same, approximated inventory / Graph 3.1 / climate profile"), C(f"{SH_PX}% / {SH_G}% / 53%"),
         C("[5] / [1] / [8]"), grade_tag("C")],
        [C("Same, final 2026 inventory (our estimate of the total)"), C(f"{SH_FIN}%"), C("[6, 5]"), grade_tag("C")],
        [C("Road transport only ÷ an effort-sharing total, 2023–2024"), C(f"{ROAD_RANGE}%"), C("[4–6]"),
         grade_tag("C")],
        [C("Transport emissions change 2005–2024: report’s text"), C("<b>+45%</b>"), C("[1] pp. 14, 66"), grade_tag("C")],
        [C("Same, approximated 2024 (= Graph 3.1, Table A8.1) / final inventory"), C(f"+{CH_PX}% / +{CH_FIN}%"),
         C("[5, 6, 1] / [6]"), grade_tag("C")],
        [C("Years 2005–2024 with transport the largest sector"), C("20 of 20"), C("[6]"), grade_tag("C")],
        [C("EU-27: transport share 2024; transport change 2005–2024"), C(f"39%; {EU_CH}%"), C("[8]; [6]"),
         grade_tag("C")],
    ], [80 * mm, 44 * mm, 30 * mm, 16 * mm]),
    P("All values in <i>data/cc-109/checks.csv</i>. Effort-sharing transport = greenhouse gases from domestic transport "
      "minus aviation CO<sub>2</sub>. The largest-sector count compares transport with buildings, agriculture, waste "
      "and industry plus F-gases in the inventory; Malta’s ETS emissions are power generation plus 0.0003 Mt [5].", cap)]))

# ================================================================== 5
S.append(CondPageBreak(95 * mm))
S.append(SectionHeading(5, "Where the evidence points different ways"))
S.append(contested(
    "Q1  Is transport 48% or 53% of Malta’s effort-sharing emissions?", "53% ON THE REPORT’S DEFINITION", ORANGE,
    f"Road transport alone is {ROAD_RANGE}% of an effort-sharing total, and footnote (140) names the sector “road "
    "transport”. Read that way, the 48% is a correct number for a narrower category.",
    f"The EEA’s approximated inventory and the report’s own Graph 3.1 ({SH_PX}%) and the Commission’s climate profile "
    "of Malta (53%) all use all domestic transport except aviation CO<sub>2</sub>, the legal definition [2]. On that "
    f"definition 48% is {GAP} points low.",
    "<b>For this claim:</b> the sentence says “transport” and “these emissions”, and the report’s graph uses the wider "
    "definition, so 53% is the figure that matches the sentence. The 48% understates transport’s weight; it does not "
    "exaggerate it, and transport is the dominant source either way."))
S.append(contested(
    "Q2  Does “up by 45% since 2005” hold, given that 2024 is approximated?", "HOLDS; FINAL DATA GIVE +48%", GREEN,
    f"On the approximated 2024 data the report uses, the rise is +{CH_PX}%, and the report’s Table A8.1 reproduces "
    "exactly from the inventory for 2018–2023 and from the approximated inventory for 2024.",
    "Approximations can be revised a long way: the 2025 report put 2023 at +32.2%, the final inventory at +44.8%. "
    "The final effort-sharing figures for 2024 will only be set after the 2027 review.",
    f"<b>For this claim:</b> the final 2026 inventory already gives +{CH_FIN}%, so the revision so far has raised the "
    "figure. “Up by 45%” is accurate on the data the report used and conservative on the newer data."))

# ================================================================== 6
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(6, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    # plain strings (no f-strings) so scripts/subclaims.py can read the table; numbers checked against checks.csv below
    [C("<b>A.</b> Transport is the dominant source of Malta’s effort sharing emissions"), C("Commission [1]"),
     C("53.3% in 2024 on the approximated data; the next sector, small industry, 19%. The largest sector in "
       "every year 2005–2024 [5, 6]."), verd("ACCURATE", GREENC)],
    [C("<b>B.</b> It has generated 48% of these emissions in 2024"), C("Commission [1]"),
     C("53% on the report’s own definition: EEA approximated inventory and Graph 3.1 53.3%, Commission climate "
       "profile 53% [1, 5, 8]. Only road-transport-only ratios (47.5–48.3%) give 48% (our identification)."),
     verd("UNDERSTATED", AMBER)],
    [C("<b>C.</b> … up by 45% since 2005"), C("Commission [1]"),
     C("The rise in emissions, not in the share: +45.0% on approximated 2024 data (0.528 to 0.766 Mt); +48.4% on "
       "the final 2026 inventory [1, 5, 6]. The share moved from 52.0% to 53.3%."), verd("ACCURATE", GREENC)],
    [C("<b>D.</b> Effort sharing covers “road transport”; Table A8.1 row “domestic road transport”"),
     C("Commission [1], footnote (140), Table A8.1"),
     C("Effort sharing covers all domestic transport except aviation CO<sub>2</sub> [2, 3]. The table row matches that "
       "wider series to 0.1 points in 2018–2023 and exactly in 2024 (45.0%); road alone is up to 6.2 points off "
       "(2024: +39.4%). Shipping is 11.9% of it [6]."), verd("LOOSELY WORDED", AMBER)],
], [46 * mm, 22 * mm, 72 * mm, 30 * mm], valign="MIDDLE"))
for got, want in ((SH_PX, "53.3"), (SH_G, "53.3"), (ROAD_RANGE, "47.5–48.3"), (CH_PX, "45.0"), (CH_G, "45.0"),
                  (CH_FIN, "48.4"), (SH05, "52.0"), (A81_R, "6.2"), (NAV_SH[1], "11.9"), (SMALL, "19"),
                  (T_PX, "0.766"), (CH_ROAD, "39.4")):
    assert got == want, (got, want)   # the sub-claim table's typed numbers must match data/cc-109/checks.csv
S.append(Spacer(1, 3 * mm))
S.append(P("<b>Reading the sentence.</b> “Up by 45% since 2005” could in principle mean that transport’s share rose by "
           "45%. The chapter-3 version of the same sentence says “with emissions up by 45%”, and the share moved only "
           f"from {SH05}% to {SH_G}%, so we rate the reading the report itself gives."))

# ================================================================== 7
S += [CondPageBreak(85 * mm), Spacer(1, 4 * mm), SectionHeading(7, "Verdict and requests for evidence"),
      verdict_box("Largely supported", "Transport is the dominant source and its emissions rose about 45% since 2005. "
                  "On the report’s own definition its share is 53%, not 48%. Confidence: high."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) Transport is the largest effort-sharing sector by a wide margin, in 2024 and in every year "
           "since 2005. (2) The 45% rise reproduces from the approximated data the report uses, and the final inventory "
           f"gives more (+{CH_FIN}%). (3) The 48% does not reproduce on the definition the report uses in its own graph; "
           "that definition gives 53%, as does the Commission’s climate profile of Malta. Because 48% understates "
           "transport’s share, and the sentence’s message (transport dominates and is growing) holds more strongly on "
           "the correct figure, this is a minor caveat, not a change of substance. (4) Confidence is high because the "
           "EEA’s datasets, Malta’s inventory and two Commission documents agree. No right of reply is needed for this "
           "verdict."))
S.append(P("<b>What this verdict does not say.</b> It does not assess the Commission’s 2030 projection, its policy "
           "recommendations or the causes of the rise in transport emissions."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "From the Commission: the series and calculation behind the 48% (Table A8.1, which footnote (141) cites, gives no "
    "share), and whether it is road transport alone.",
    "From the Commission: confirmation that Table A8.1’s “domestic road transport” row includes domestic navigation, as "
    "its values imply.",
    "From the EEA or the Commission: final effort-sharing figures for 2024 by sector after the 2027 review.",
]))

# ================================================================== 8
S += [Spacer(1, 5 * mm), SectionHeading(8, "Limitations")]
for l in ["The 2024 effort-sharing total is approximated; the final, reviewed figure will be set in 2027.",
          "Graph 3.1 was read from the PDF’s drawing instructions, not from a data table; the 2024 total read this way "
          "(1.437 Mt) matches the EEA’s figure to 0.001 Mt.",
          "Our effort-sharing total on the final 2026 inventory is an estimate (total excluding land use, minus ETS "
          "emissions from the approximated inventory, minus aviation CO<sub>2</sub>).",
          "We could not see how the Commission computed 48%; the road-only route is our identification only.",
          "The EEA greenhouse gas data viewer named in Table A8.1 draws its charts in JavaScript; we used the EEA "
          "datasets behind it. Malta’s UNFCCC reporting tables were not opened; the EEA’s compilation of the same "
          "submission was used.",
          "The study cited for road’s share of transport CO<sub>2</sub> [11] takes it from Malta’s Fourth Biennial "
          "Report, which we did not read (marked ◆)."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 5 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "European Commission (3 Jun 2026). 2026 Country Report – Malta. SWD(2026) 218 final; Council document 10135/26 "
          "ADD 1 (8 Jun 2026). Read in full 6 Oct 2026; Commission-copy pages 6, 14, 66, 71 (Council copy 6, 15–16, 72, "
          "77).",
     "https://economy-finance.ec.europa.eu/document/download/b0bb0c3b-1b52-4ac5-8090-ee21edf1e039_en?filename=MT_SWD_2026_218_1_EN_autre_document_travail_service_part1_v1.pdf"),
    ("2", "Regulation (EU) 2018/842 (Effort Sharing Regulation), Article 2. OJ L 156, 19.6.2018, p. 26. Read via the EU "
          "Publications Office, 6 Oct 2026.", "http://data.europa.eu/eli/reg/2018/842/oj"),
    ("3", "Regulation (EU) 2023/857 amending Regulation (EU) 2018/842, Article 1(2) (scope) and Article 2(1) (final inventories by 15 March). OJ L 111, 26.4.2023, p. 1. Read via "
          "the EU Publications Office, 6 Oct 2026.", "http://data.europa.eu/eli/reg/2023/857/oj"),
    ("4", "European Environment Agency (6 Nov 2025). Greenhouse gas emissions under the Effort Sharing Legislation, "
          "2005–2024. Dataset, doi:10.2909/f80bebef-447e-4882-b3e9-c4a91cbae4f5. Retrieved 6 Oct 2026.",
     "https://doi.org/10.2909/f80bebef-447e-4882-b3e9-c4a91cbae4f5"),
    ("5", "European Environment Agency (5 Nov 2025). GovReg: Approximated estimates for greenhouse gas emissions, 2024 "
          "(with statistical metadata). Dataset, doi:10.2909/cd572015-4d0d-408a-abf8-290ed2057bf7. Retrieved 6 Oct 2026.",
     "https://doi.org/10.2909/cd572015-4d0d-408a-abf8-290ed2057bf7"),
    ("6", "Eurostat. Greenhouse gas emissions by source sector (env_air_gge), updated 2 Jun 2026, "
          "doi:10.2908/ENV_AIR_GGE. Retrieved 6 Oct 2026; no flags on the Malta rows used.",
     "https://ec.europa.eu/eurostat/databrowser/view/env_air_gge/default/table"),
    ("7", "European Environment Agency (17 Apr 2026). GovReg: National emissions reported to the UNFCCC and to the EU "
          "under the Governance Regulation, 2026 ver. 1.0 (data of 15 Mar 2026). Dataset, "
          "doi:10.2909/83ee8f8c-1422-4e3f-af63-ba88146811e5. Retrieved 6 Oct 2026.",
     "https://doi.org/10.2909/83ee8f8c-1422-4e3f-af63-ba88146811e5"),
    ("8", "European Commission, DG Climate Action (Jan 2026). Climate Action Progress Report 2025: country profile "
          "Malta, pp. 9–10 (Figure 11). Read in full 6 Oct 2026.",
     "https://climate.ec.europa.eu/document/download/acb92e05-4220-44c3-9483-b3524c326f59_en?filename=mt_2025_factsheet_en.pdf"),
    ("9", "European Commission, DG Climate Action. Climate Action Progress Report 2024: country profile Malta (2023 data), "
          "pp. 5–6. Read 6 Oct 2026.",
     "https://climate.ec.europa.eu/document/download/4c335e40-6961-4473-9cc0-5b6367f75a6e_en?filename=mt_2024_factsheet_en.pdf"),
    ("10", "European Commission (4 Jun 2025). 2025 Country Report – Malta. SWD(2025) 218 final, pp. 67, 69. Read 6 Oct "
           "2026.",
     "https://economy-finance.ec.europa.eu/document/download/be493fbf-cb70-432c-a68a-13067176ff38_en?filename=MT_CR_SWD_2025_218_1_EN_autre_document_travail_service_part1_v5.pdf"),
    ("11", "Camilleri R., Attard M., Hickman R. (2024). Participatory policy packaging for transport backcasting: a pathway "
           "for reducing CO<sub>2</sub> emissions from transport in Malta. <i>Sustainability</i> 16(1):430. "
           "doi:10.3390/su16010430. Full text read (CC BY 4.0); its road share comes from Malta’s Fourth Biennial "
           "Report ◆.", "https://doi.org/10.3390/su16010430"),
    ("12", "Miżien. Data and calculations: data/cc-109/; tools/cc-109-report/ (fetch.py, read_graph.py, calc.py). Claim "
           "Check 003 for the earlier figures (data/cc-003/).", ""),
    ("13", "Commission Implementing Decision (EU) 2020/2126 of 16 December 2020 setting out the annual emission "
           "allocations of the Member States for 2021–2030, Annex I (Malta, 2005: 1 020 601 t CO<sub>2</sub>e). OJ L 426, "
           "17.12.2020, p. 58. Read via the EU Publications Office, 6 Oct 2026.",
     "https://data.europa.eu/eli/dec_impl/2020/2126/oj"),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "6 Oct 2026", "First issue. Largely supported (high confidence); no right of reply needed.")])

build_report(Report(
    number="109", out=str(FIG / "report.pdf"), kicker="EU statistics and climate targets",
    title_lines=["Is transport 48%", "of Malta’s effort-", "sharing emissions?"],
    subtitle_lines=["Testing a European Commission statement against", "EEA and Eurostat emissions data"],
    quote_lines=["“Transport is the dominant source of Malta’s effort sharing",
                 "emissions. It has generated 48% of these emissions in 2024,", "up by 45% since 2005.”"],
    quote_size=13,
    attribution="European Commission, 2026 Country Report – Malta, SWD(2026) 218 final, 3 June 2026, p. 66.",
    context="The same figures appear on pp. 6 and 14. Footnote mark (141) omitted.",
    verdict="Largely supported", verdict_note="Dominant and up 45%; the share is 53%, not 48%",
    footer_lines=["Version 1.0  ·  6 October 2026", "Status:",
                  "Prepared from public sources, EEA and Eurostat data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Transport and Malta’s effort-sharing emissions", version="1.0", date="6 October 2026",
    pdf_title="Is transport 48% of Malta's effort-sharing emissions? Claim Check 109",
    pdf_subject="Tests the European Commission's statement that transport generated 48% of Malta's effort-sharing "
                "emissions in 2024, up 45% since 2005",
    story=S))
