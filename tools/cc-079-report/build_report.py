"""Claim Check 079 report. Run fetch.py, calc.py and figures.py first. Output: out/report.pdf"""
import csv
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
ROOT = HERE.parents[1]
CHK = {r["check"]: r for r in csv.DictReader(open(ROOT / "data/cc-079/checks.csv"))}
S = []


def den(check):
    return float(CHK[check]["value"])


def share(num, check):
    """num GWh as a share of a saved denominator, to one decimal (computed from the denominator, not re-rounded)."""
    return f"{100 * num / den(check):.1f}%"


E, FUEL = 126.0, den("Energy content of 192,000 t at that value (fuel input)")

# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("In June 2023 WasteServ wrote that the waste-to-energy plant it plans at "
        "Magħtab <b>“will be treating around 192,000 tonnes of non-recyclable waste generated locally”</b> and <b>“is "
        "expected to meet around 4.5% of Malta’s total energy needs”</b>. It had used the same 4.5% in 2020, “as green "
        "energy”. We tested both figures against WasteServ’s own output figure, the plant design in Malta’s National "
        "Energy and Climate Plan (NECP) and Eurostat’s energy and waste statistics.", lead)]
S.append(key_points([
    ("The tonnage matches the design.",
     "192,000 tonnes a year is two lines of 12 tonnes an hour running 8,000 hours, as in the NECP; the Commission "
     "cites 190,000 t. Malta landfilled 255,000 t of municipal waste in 2024, so there is enough residual waste today."),
    ("The plant would make about 126 GWh of electricity a year.",
     "That is WasteServ’s own figure. The NECP’s 14–16 MW net and the efficiencies published for plants of this size "
     "(20–24%) agree with it."),
    ("4.5% fits electricity, not total energy.",
     "126 GWh was 4.4–4.7% of Malta’s electricity use in 2022, but 1.5% of its final energy consumption and 1.2% of its "
     "primary energy. Electricity is only about a third of the final energy Malta uses."),
    ("Only one other reading comes near 4.5%.",
     "The energy in the waste itself (about 533 GWh a year) is 5.0–5.2% of primary energy. But the plant would deliver "
     "under a quarter of it, as electricity; WasteServ names no user for the heat."),
    ("“Green” needs a qualifier.",
     "EU law counts only the biodegradable part of waste as renewable, and the NECP says the plant “is not expected "
     "to contribute to Malta’s RES share”."),
    ("Verdict: misleading (moderate confidence).",
     "A share of electricity is presented as a share of all energy, about three times too high. Even for electricity the "
     "share falls to 3.2% by 2030 on the NECP’s projection. WasteServ published no method."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(3), Spacer(1, 3 * mm),
      tiles([("4.5%", RED, "WasteServ: share of “Malta’s total energy needs” the plant would meet"),
             ("1.5%", ORANGE, "126 GWh as a share of Malta’s final energy consumption, 2022 (1.2% of primary energy)"),
             ("4.4–4.7%", GREEN, "126 GWh as a share of Malta’s electricity use, 2022: where 4.5% fits"),
             ("3.2%", GREY, "Share of electricity supply in 2030, on the NECP’s own projection")]),
      Spacer(1, 4 * mm),
      up_down("WasteServ’s calculation showing which energy measure and year the 4.5% uses; or design documents (the EIA, "
              "the contract) showing the plant will also supply heat, enough to bring the energy it delivers near 4.5% "
              "of Malta’s total.",
              "A design or contract output well below 126 GWh a year, which would leave the 4.5% without a basis even "
              "as a share of electricity."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "How the plant would make energy"),
          ("4", "What the studies and data show"), ("5", "Where the evidence points different ways"),
          ("6", "Testing the claim"), ("7", "Verdict and requests for evidence"), ("8", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("ECOHIVE is WasteServ’s project for new waste plants at the Magħtab waste complex, among them a waste-to-energy "
           "facility, a material recovery facility, an organic processing plant, a skip management facility and a "
           "thermal treatment facility for hazardous waste [3]. The news item of 26 June 2023 on WasteServ’s ECOHIVE website "
           "reported a procurement milestone for the waste-to-energy plant and ended with the two sentences quoted on "
           "the cover [1]. WasteServ’s releases of 23 October and 2 November 2020 had given the 4.5% as “green energy” "
           "added to “Malta’s total energy demand” [2]. The undated project page gives the plant’s output, 126 GWh a "
           "year, and says it will treat 40% of Malta’s non-recyclable waste [3]. We read all of them in full on "
           "10 October 2026."))
S.append(P("The figures reached us through Amphora Media (June 2025), which reported in its own words that in a January "
           "2025 parliamentary answer the Environment Minister said the plant would process 40% of non-recyclable "
           "waste and provide 4.5% of the country’s energy needs [4]. We could not read that answer (the parliament’s "
           "websites refuse automated access), so we rate WasteServ’s published wording only."))
S.append(std_table([
    [C("Source", cellh), C("What it says", cellh), C("Our access", cellh), C("Status", cellh)],
    [C("<b>WasteServ</b>, ECOHIVE news, 26 Jun 2023 [1]"),
     C("“This plant will be treating around 192,000 tonnes of non-recyclable waste generated locally … It is expected "
       "to meet around 4.5% of Malta’s total energy needs.”"), C("Read in full, 10 Oct 2026."), C("<b>The claim</b>")],
    [C("<b>WasteServ</b>, releases of 23 Oct and 2 Nov 2020 [2]"),
     C("“… adding an impressive 4.5% as green energy to Malta’s total energy demand.”"),
     C("Read in full (also the Malta Business Weekly reprint)."), C("Earlier wording")],
    [C("<b>WasteServ</b>, ECOHIVE project page, undated [3]"),
     C("“the plant will generate 126GWh annually to the grid”; “40% of non-recyclable waste generated in Malta”; "
       "capacity 192,000 t; commissioning December 2026."), C("Read in full (English and Maltese)."),
     C("Speaker’s own figures")],
    [C("<b>Amphora Media</b>, 6 Jun 2025 [4]"), C("The Minister’s parliamentary answer, in the outlet’s words."),
     C("Read; the answer itself returned 403."), C("Locator; not rated")],
    [C("<b>Government of Malta</b>, NECP, Dec 2024 [5]"),
     C("Plant design; 2030 projections; the plant and the renewable share."), C("Read the relevant sections."),
     C("Official plan")],
    [C("<b>Eurostat</b> [6, 7]"), C("Energy balances, electricity and waste statistics for Malta."),
     C("Downloaded 10 Oct 2026 (data/cc-079/)."), C("<b>Primary data</b>")],
], [36 * mm, 74 * mm, 38 * mm, 22 * mm]))
S.append(Spacer(1, 3 * mm))
S.append(callout([P("FAIRNESS NOTE", tag),
                  P("WasteServ’s statements describe a plant that has not been built. In March 2026 The Shift News "
                    "reported, from a parliamentary answer, that the latest procurement had been abandoned and no funds "
                    "set aside for 2026 [13]. We test the figures as stated, not the project, its procurement or its "
                    "environmental effects, and nothing here concerns anyone’s motives.", small)], bg=PALE, bar=GREEN))

# ================================================================== 2
S += [Spacer(1, 4 * mm), SectionHeading(2, "Method")]
S.append(P("<b>Question.</b> What could “4.5% of Malta’s total energy needs” mean, and do the plant’s expected output "
           "and Malta’s energy statistics support it on that reading? Are the tonnage and the other figures WasteServ "
           "gives for the plant consistent?"))
S.append(P("<b>Readings.</b> WasteServ gives no method, so we tested each plausible one. The <i>numerator</i> is the "
           "energy the plant delivers (126 GWh of electricity a year, WasteServ’s figure) or, as an upper bound that is "
           "not delivered, the energy content of the waste burnt. The <i>denominator</i> is Malta’s electricity (final "
           "consumption; inland demand) or its total energy: final energy consumption as reported for the Energy "
           "Efficiency Directive (which includes international aviation), final energy use without it, primary energy "
           "consumption, gross inland consumption and gross available energy (which also counts fuel sold to ships). "
           "Years: 2019 and 2022, the last years before the 2020 and 2023 statements, 2024 (latest) and the NECP’s 2030 "
           "projection."))
S.append(P("<b>Evidence.</b> Eurostat datasets nrg_bal_c, nrg_cb_e, env_wasmun, env_wastrt and env_wasgen, downloaded "
           "with a script on 10 October 2026 (<i>tools/cc-079-report/fetch.py</i>); the NECP’s design figures and "
           "projections; peer-reviewed studies of electrical efficiency and of the biogenic share of burnt waste "
           "(abstracts only); EU law. Every figure is recomputed in <i>calc.py</i> (outputs in "
           "<i>data/cc-079/checks.csv</i>). <b>Grades</b> and the <b>verdict scale</b> are in Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(90 * mm))
S.append(SectionHeading(3, "How the plant would make energy"))
S.append(P("In a moving-grate plant, mixed waste burns on a sloping grate; the hot gases raise steam in a boiler and "
           "the steam drives a turbine. Only part of the waste’s energy becomes electricity. A review of thermal "
           "treatment puts the net electric efficiency of small and medium plants that make only electricity at around "
           "20–24%, and up to 30–31% for the largest [9]; the rest leaves as heat. Selling heat as well (co-generation) is the main way to recover more [9], and "
           "differences between European plants relate mainly to their size and to whether a heat market exists [10]."))
S.append(P("The NECP describes the Magħtab design: two moving-grate lines on one turbine, each taking 12 tonnes an hour, "
           "with a net electricity generation of 14–16 MW and a heat input to the boiler “between 20MWth and 33.33MWth” "
           "[5, p. 132]. 192,000 tonnes a year at 24 tonnes an hour is 8,000 full-load hours, 91% of the year. Reading "
           "33.33 MWth as the heat input of each line, the design calorific value is 10.0 GJ a tonne and the waste’s "
           "energy content 533 GWh a year; 126 GWh is then a net efficiency of 23.6%, inside the range for plants of "
           "this size. Read as the total for both lines, 33.33 MWth would imply 42–48%, well above the 30–31% the review "
           "gives for the largest plants [9], so we reject that reading."))
S.append(fig(FIG / "fig1_energy.png", width=CW * 0.98))
S.append(P("Figure 1. Where the energy in 192,000 tonnes of waste would go, on the NECP design figures and WasteServ’s "
           "126 GWh. The plant’s other heat is not described as delivered to any user.", cap))

# ================================================================== 4
S.append(CondPageBreak(60 * mm))
S.append(SectionHeading(4, "What the studies and data show"))
S.append(P("Against Malta’s electricity, 126 GWh a year is close to WasteServ’s 4.5%: 4.4–4.7% in 2022, the year before "
           "the June 2023 statement. Against Malta’s total energy it is 1.1–1.8% (Figure 2, Table 1), and less if fuel sold "
           "to ships is counted. Total energy also covers transport fuels, among them aviation fuel [6], and electricity "
           "is about a third of the final energy Malta uses (33% in 2022 and 2024). 126 GWh would be exactly 4.5% of "
           "2,800 GWh (241 ktoe); Malta’s gross inland consumption in 2024 was 964 ktoe."))
S.append(std_table([
    [C("Evidence", cellh), C("Finding", cellh), C("Source", cellh), C("Grade", cellh)],
    [C("Electrical efficiency of waste incineration"), C("Net 20–24% for small-medium plants making only "
       "electricity; up to 30–31% for large plants."), C("Lombardi et al. 2015, review [9]"), grade_tag("C")],
    [C("Why plants differ"), C("Mainly plant size and whether a heat market (district heating) exists."),
     C("Grosso et al. 2010 [10]"), grade_tag("B")],
    [C("Biogenic share of burnt mixed waste"), C("CO2 slightly above 50% biogenic at three Swiss plants; fossil share "
       "43–55% (mean 48%) at five plants over a year."), C("Mohn et al. 2008, 2012 [11, 12]"), grade_tag("B")],
    [C("Plant design"), C("2 lines × 12 t/h; 14–16 MW net; 20–33.33 MWth heat input."), C("NECP, p. 132 [5]"),
     grade_tag("C")],
    [C("Plant output"), C("126 GWh a year to the grid (no calculation given)."), C("WasteServ [3]"), grade_tag("D")],
    [C("Malta’s electricity, 2022"), C("Final consumption 2,698 GWh; inland demand 2,880 GWh (2024: 2,868 and "
       "3,106 GWh)."), C("Eurostat nrg_cb_e [6]"), grade_tag("C")],
    [C("Malta’s total energy, 2022"), C("Final energy consumption 8,136 GWh (700 ktoe); primary energy consumption "
       "10,318 GWh (887 ktoe), as in the NECP’s Table 27."), C("Eurostat nrg_bal_c [6]; NECP [5]"), grade_tag("C")],
    [C("Projections for 2030"), C("Electricity supply 3,951 GWh (all sources in Figure 120); primary energy 964 ktoe; "
       "final energy 803 ktoe."), C("NECP, pp. 94, 344 [5]"), grade_tag("C")],
    [C("Malta’s municipal waste, 2024"), C("354,000 t generated, 255,000 t landfilled, 8,000 t burnt with energy "
       "recovery."), C("Eurostat env_wasmun [7]"), grade_tag("C")],
], [36 * mm, 82 * mm, 40 * mm, 12 * mm], valign="MIDDLE"))
S.append(Spacer(1, 4 * mm))
S.append(CondPageBreak(95 * mm))
S.append(fig(FIG / "fig2_shares.png", width=CW * 0.98))
S.append(P("Figure 2. The plant’s 126 GWh a year as a share of Malta’s electricity (blue) and of its total energy (green). "
           "The 2030 marker on the inland-demand row is the NECP’s total electricity supply from all sources.", cap))

rows = [[C("126 GWh compared with", cellh), C("2019", cellh), C("2022", cellh), C("2024", cellh), C("2030 (NECP)", cellh)]]
spec = [("Electricity: final consumption", "Electricity: final consumption (nrg_cb_e FC)", None),
        ("Electricity: inland demand (2030: all supply)", "Electricity: inland demand (nrg_cb_e ID)",
         "2030 NECP electricity generation, all sources (sum of Figure 120)"),
        ("Final energy consumption (with international aviation)",
         "Total energy: final energy consumption (nrg_bal_c FEC_EED)", "2030 NECP final energy consumption (803 ktoe)"),
        ("Final energy use (without international aviation)",
         "Total energy: final energy use excl. international aviation (nrg_bal_c FC_E)", None),
        ("Primary energy consumption", "Total energy: primary energy consumption (nrg_bal_c PEC_EED)",
         "2030 NECP primary energy consumption (964 ktoe)"),
        ("Gross inland consumption", "Total energy: gross inland consumption (nrg_bal_c GIC)", None),
        ("Gross available energy (with fuel sold to ships)",
         "Total energy: gross available energy incl. marine bunkers (nrg_bal_c GAE)", None)]
for lab, key, k30 in spec:
    rows.append([C(lab)] + [C(share(E, f"{y} {key}")) for y in (2019, 2022, 2024)] +
                [C(share(E, k30) if k30 else "–")])
rows.append([C("<i>Upper bound: energy in the waste ({:.0f} GWh) vs primary energy consumption</i>".format(FUEL))] +
            [C("<i>" + share(FUEL, f"{y} Total energy: primary energy consumption (nrg_bal_c PEC_EED)") + "</i>")
             for y in (2019, 2022, 2024)] + [C("<i>" + share(FUEL, "2030 NECP primary energy consumption (964 ktoe)") + "</i>")])
S.append(KeepTogether([P("Table 1. The plant’s 126 GWh a year as a share of Malta’s totals", h2),
                       std_table(rows, [76 * mm, 22 * mm, 22 * mm, 22 * mm, 28 * mm], valign="MIDDLE"),
                       P("Eurostat nrg_cb_e and nrg_bal_c (retrieved 10 Oct 2026); NECP Dec 2024, p. 94 and Figure 120. "
                         "The last row is not energy the plant delivers: it counts all the energy in the waste.", cap)]))

# ================================================================== 5
S.append(CondPageBreak(80 * mm))
S.append(SectionHeading(5, "Where the evidence points different ways"))
S.append(contested(
    "What is the 4.5% a share of?", "ELECTRICITY, NOT ALL ENERGY", RED,
    "126 GWh is 4.4–4.7% of Malta’s electricity use in 2022 and 4.8–5.1% in 2019, so 4.5% is a fair figure for "
    "<i>electricity</i> at the time of both statements. Counting all the energy in the waste (533 GWh), the share of "
    "primary energy consumption is 5.0–5.2% (2022–2024).",
    "WasteServ wrote “total energy needs” and “total energy demand”. Against Malta’s total energy, 126 GWh is "
    "1.1–1.8% (2022–2024), and less if fuel sold to ships is counted. The energy-content reading counts the three-quarters of the waste’s energy that the plant "
    "would not deliver; WasteServ names no user for its heat.",
    "The 4.5% most likely is a share of electricity described as a share of all energy; WasteServ has not published "
    "its method. Read as worded, the statement overstates the plant’s contribution about threefold (4.5% against 1.5% "
    "of final energy consumption in 2022). Even for electricity the share shrinks as demand grows: 3.2% of the NECP’s "
    "2030 supply.", label_a="EVIDENCE FOR A 4.5% FIGURE", label_b="EVIDENCE AGAINST “TOTAL ENERGY”"))
S.append(contested(
    "Is it “green energy”?", "PARTLY", AMBER,
    "EU law counts the biodegradable fraction of municipal waste as biomass, a renewable source [14]. Radiocarbon "
    "measurements at Swiss plants found about half the carbon in burnt mixed waste to be biogenic [11, 12]. The NECP "
    "expects the waste sector to lead future cuts in Malta’s methane emissions, mainly because waste would go to the "
    "plant instead of landfill [5, p. 60].",
    "Only the biodegradable part counts; the rest, mainly plastics, is fossil. Malta’s own plan shows only solar PV "
    "and biogas in its renewable-electricity trajectory and says the new thermal treatment plant “is not expected to "
    "contribute to Malta’s RES share” [5, pp. 84, 144].",
    "“Green energy” is true at most for part of the output, and the Government’s own plan does not count the plant "
    "towards Malta’s renewable share. The Swiss carbon shares are context, not a measurement of Malta’s waste.",
    label_a="FOR", label_b="AGAINST"))
S.append(contested(
    "Will there be 192,000 tonnes of non-recyclable waste to burn?", "TODAY YES; AT 2035 TARGETS, NO", AMBER,
    "Malta landfilled 255,000 t of municipal waste in 2024 and 286,500 t of non-mineral waste of all kinds in 2022 [7]; "
    "192,000 t is 75% and 67% of these. Only 1.3% of municipal waste was incinerated in 2022 [8].",
    "Malta has kept the EU target of recycling 65% of municipal waste by 2035, renouncing a postponement in November "
    "2024 [8, 15]. At the 2024 level of waste, meeting it would leave at most 124,000 t for burning or landfill, "
    "68,000 t less than the plant’s capacity; waste would have to grow by 55% for 35% of it to fill the plant. The "
    "NECP plans to pre-sort mixed waste to take out recyclables before it reaches the plant [5, p. 132].",
    "The tonnage is consistent with today’s landfilling, which is far from EU targets (16.7% recycled in 2024; see "
    "CC-004). Whether the plant could run full once recycling rises depends on waste growth or on other waste streams; "
    "the sources we read do not list the plant’s feedstock. ◆ MaltaToday reported that a smaller design was dropped "
    "because recycling rates were low (not read: 403).", label_a="ENOUGH WASTE NOW", label_b="IF RECYCLING TARGETS ARE MET"))
S.append(CondPageBreak(85 * mm))
S.append(fig(FIG / "fig3_waste.png", width=CW * 0.98))
S.append(P("Figure 3. Malta’s municipal waste generated and landfilled, 2010–2024, against the plant’s capacity and the "
           "most that would be left for burning or landfill in 2035 if the recycling target were met at the 2024 "
           "level of waste.", cap))

# ================================================================== 6
S.append(CondPageBreak(105 * mm))
S.append(SectionHeading(6, "Testing the claim"))
S.append(P("WasteServ’s two sentences of 26 June 2023 are sub-claims A and B; its 2020 wording adds C; the project page "
           "supplies D, the output on which every reading of the 4.5% depends, and E. WasteServ gave no reasoning for "
           "the 4.5% that we could check."))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> The plant will treat around 192,000 tonnes of non-recyclable waste generated locally a year"),
     C("WasteServ [1]"),
     C("Matches the NECP design (24 t/h for 8,000 hours) and the Commission’s 190,000 t. Malta landfilled 255,000 t of "
       "municipal waste in 2024, but meeting the 2035 recycling target would leave at most 124,000 t."),
     verd("CONSISTENT", GREENC)],
    [C("<b>B.</b> It is expected to meet around 4.5% of Malta’s total energy needs"), C("WasteServ [1, 2]"),
     C("126 GWh is 1.5% of final and 1.2% of primary energy consumption (2022), but 4.4–4.7% of electricity use. "
       "3.2% of the NECP’s 2030 electricity supply."),
     verd("MISLEADING", RED)],
    [C("<b>C.</b> The waste is converted into green energy"), C("WasteServ [1, 2]"),
     C("Only the biodegradable fraction counts as renewable under EU law; the NECP says the plant is not expected to "
       "contribute to Malta’s renewable share."),
     verd("PARTLY", AMBER)],
    [C("<b>D.</b> The plant will generate 126 GWh a year to the grid"), C("WasteServ [3]"),
     C("Consistent with the NECP’s 14–16 MW net (112–128 GWh) and a net efficiency of 23.6%, within the 20–24% "
       "reported for plants of this size."),
     verd("PLAUSIBLE", GREENC)],
    [C("<b>E.</b> The plant will treat 40% of the non-recyclable waste generated in Malta"), C("WasteServ [3]"),
     C("With 192,000 t this implies 480,000 t of non-recyclable waste. 192,000 t is 67–75% of the waste Malta "
       "landfills and 32% of all non-mineral waste it generates; no basis is given."),
     verd("UNCLEAR BASIS", AMBER)],
], [42 * mm, 18 * mm, 76 * mm, 34 * mm], valign="MIDDLE"))

# ================================================================== 7
S += [Spacer(1, 5 * mm), SectionHeading(7, "Verdict and requests for evidence"),
      verdict_box("Misleading", "The 4.5% fits the plant’s expected electricity as a share of Malta’s electricity, not "
                  "of its total energy needs, where it is about 1.1–1.8%. Confidence: moderate."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> The tonnage and the output WasteServ gives are consistent with the plant design in the "
           "Government’s own energy plan. The share is not: “total energy needs” and “total energy demand” name all of "
           "Malta’s energy, of which the plant’s 126 GWh would be about 1.1% (gross inland consumption, 2024) to 1.8% (final "
           "energy use without aviation). The figure of 4.5% matches the plant’s output as a share of Malta’s <i>electricity</i> in the "
           "years before the statements, or the whole energy content of the waste, most of which the plant would not "
           "deliver. Either way the overall impression, that burning Malta’s residual waste would meet 4.5% of all the "
           "country’s energy needs, is inaccurate. The “green energy” label adds to it: the "
           "NECP does not count the plant towards Malta’s renewable share."))
S.append(P("<b>Why moderate confidence.</b> WasteServ published no method, the plant’s final design is not settled, "
           "and we could not read its EIA. A plant that also delivered most of its heat would supply more energy than "
           "the electricity alone; no heat user is described in any source we read."))
S.append(P("<b>What this verdict does not say.</b> It does not judge whether Malta should build a waste-to-energy plant, "
           "the procurement or the plant’s emissions. The tonnage and the electricity output are consistent with the "
           "design."))
S.append(KeepTogether([P("Evidence we are asking for", h2), requests_list([
    "From WasteServ: the calculation behind the 4.5%: which energy measure, which year and which output figure.",
    "From WasteServ: whether the plant will supply heat, to whom and how much, and its expected net electricity in the "
    "current design.",
    "From WasteServ or ERA: the Environmental Impact Assessment’s design calorific value, feedstock list and energy "
    "balance (we found no readable copy).",
    "From the Ministry for the Environment, Energy and Public Cleanliness: the text of the January 2025 parliamentary "
    "answer reported by Amphora Media.",
    "From the Energy and Water Agency: whether any of the plant’s output will count towards Malta’s renewable share, "
    "given the NECP’s statement that it is not expected to.",
])]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag),
               P("Before wider circulation this draft should be sent to WasteServ, with a fixed deadline. Responses "
                 "will be appended and the verdict revisited. Under the project’s rules a <i>Misleading</i> verdict is "
                 "not circulated beyond this site before the reply deadline has passed.", small)],
              bg=AMBER_PALE, bar=AMBER)]

# ================================================================== 8
S += [Spacer(1, 6 * mm), SectionHeading(8, "Limitations")]
for l in ["WasteServ published no method for the 4.5%. We tested every reading we could think of; there may be another.",
          "The design may change. The figures are from the NECP (December 2024) and WasteServ’s pages; the latest "
          "procurement was abandoned, as The Shift News reported [13] from a parliamentary answer we did not read.",
          "We could not read the plant’s EIA; its calorific value, heat use and net output are taken from the NECP. "
          "The heat-input figure does not say whether it is per line; we tested both readings.",
          "The NECP’s Figure 120 (2030 electricity by source) has a legend whose colours do not clearly match its slices; "
          "we used only the total of the slices as a denominator.",
          "The journal studies were read as abstracts. The Swiss biogenic shares are context, not measurements of "
          "Malta’s waste. No peer-reviewed study of this plant was found in Crossref; an OpenAlex search was refused "
          "(rate limit).",
          "Eurostat revises energy balances; the 2024 values are the latest published on 10 October 2026.",
          "Amphora’s account of the Minister’s parliamentary answer is the outlet’s paraphrase and is not rated."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "WasteServ (26 June 2023). Malta’s Waste-to-Energy Project Procurement Reaches its Final Stage. ECOHIVE news. "
          "Read 10 Oct 2026.", "https://www.ecohive.com.mt/en/article?id=872332ec-b93b-4e6d-8746-732b1c175bb5"),
    ("2", "WasteServ (23 October 2020). Three world leading giants shortlisted to design, build & operate the ECOHIVE "
          "Waste to Energy Plant; and (2 November 2020) Waste to Energy Procurement Process to Move to Next Stage. "
          "ECOHIVE news; the first reprinted by The Malta Business Weekly, 23 Oct 2020.",
     "https://www.ecohive.com.mt/en/article?id=b688333c-9004-403c-8643-cb92837b7143"),
    ("3", "WasteServ. ECOHIVE: The Project, Waste-to-Energy Facility (undated web page, English and Maltese). Read "
          "10 Oct 2026.", "https://www.ecohive.com.mt/"),
    ("4", "Repečkaitė, D. (6 June 2025). Analysis: Is Burning Waste At Magħtab The Only Way Out Of Malta’s Waste "
          "Crisis? Amphora Media. Locator only.", "https://www.amphora.media/2025/06/waste-energy-maghtab-recycling-sustainable"),
    ("5", "Government of Malta (December 2024). Malta’s National Energy and Climate Plan (updated), 2021–2030. Pp. 60, "
          "84, 94, 132, 144, 286 (Table 27), 344 (Figure 120); printed page numbers.",
     "https://clean-energy-islands.ec.europa.eu/system/files/2025-03/MT%20FINAL%20UPDATED%20NECP%202021-%202030%20%28English%29.pdf"),
    ("6", "Eurostat. Complete energy balances (nrg_bal_c, updated 27 Aug 2026); Supply, transformation and consumption "
          "of electricity (nrg_cb_e, updated 9 Oct 2026). Retrieved 10 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/nrg_bal_c/default/table"),
    ("7", "Eurostat. Municipal waste by waste management operations (env_wasmun, updated 30 Mar 2026); Treatment of "
          "waste (env_wastrt) and Generation of waste (env_wasgen), updated Sep 2025. Retrieved 10 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/env_wasmun/default/table"),
    ("8", "European Commission (2025). 2025 Environmental Implementation Review: Malta. SWD(2025) 318 final, pp. 8–9.",
     "http://publications.europa.eu/resource/celex/52025SC0318"),
    ("9", "Lombardi, L., Carnevale, E. and Corti, A. (2015). A review of technologies and performances of thermal "
          "treatment systems for energy recovery from waste. Waste Management 37, 26–44. Abstract read.",
     "https://doi.org/10.1016/j.wasman.2014.11.010"),
    ("10", "Grosso, M., Motta, A. and Rigamonti, L. (2010). Efficiency of energy recovery from waste incineration, in "
           "the light of the new Waste Framework Directive. Waste Management 30(7), 1238–1243. Abstract read.",
     "https://doi.org/10.1016/j.wasman.2010.02.036"),
    ("11", "Mohn, J., Szidat, S., Fellner, J. et al. (2008). Determination of biogenic and fossil CO2 emitted by waste "
           "incineration based on 14CO2 and mass balances. Bioresource Technology 99(14), 6471–6479. Abstract read.",
     "https://doi.org/10.1016/j.biortech.2007.11.042"),
    ("12", "Mohn, J., Szidat, S., Zeyer, K. and Emmenegger, L. (2012). Fossil and biogenic CO2 from waste incineration "
           "based on a yearlong radiocarbon study. Waste Management 32(8), 1516–1520. Abstract read.",
     "https://doi.org/10.1016/j.wasman.2012.04.002"),
    ("13", "The Shift News (3 March 2026). No funds for Magħtab waste-to-energy plant project promised in 2017. Context only.",
     "https://theshiftnews.com/2026/03/03/no-funds-for-maghtab-waste-to-energy-plant-project-promised-in-2017/"),
    ("14", "Directive (EU) 2018/2001 on the promotion of the use of energy from renewable sources (recast), Art. 2(1) "
           "and 2(24).", "http://publications.europa.eu/resource/celex/32018L2001"),
    ("15", "Directive (EU) 2018/851 amending Directive 2008/98/EC on waste, Art. 11(2)(e) as amended; Directive (EU) "
           "2018/850 amending Directive 1999/31/EC on landfill, Art. 5(5) as amended.",
     "http://publications.europa.eu/resource/celex/32018L0851"),
    ("16", "Miżien. Calculation scripts and outputs: tools/cc-079-report/calc.py; data/cc-079/checks.csv. Related "
           "checks: CC-004 (recycling), CC-111 (landfill), CC-080 (organic plant).", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand. A speaker’s "
                "figure given without data or method (here WasteServ’s 126 GWh and 4.5%) is graded D.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "10 Oct 2026", "First issue. Verdict Misleading (moderate confidence); pending right of reply.")])

build_report(Report(
    number="079", out=str(FIG / "report.pdf"), kicker="Energy and waste statistics",
    title_lines=["4.5% of Malta’s", "energy from", "burning waste?"],
    subtitle_lines=["Testing WasteServ’s figures for the Magħtab waste-to-energy", "plant against Eurostat and Malta’s energy plan"],
    quote_lines=["“This plant will be treating around 192,000 tonnes of",
                 "non-recyclable waste … It is expected to meet around",
                 "4.5% of Malta’s total energy needs.”"], quote_size=13.5,
    attribution="WasteServ, ECOHIVE news, 26 June 2023.",
    context="In 2020: “adding an impressive 4.5% as green energy to Malta’s total energy demand”.",
    verdict="Misleading", verdict_note="4.5% fits electricity; of total energy it is about 1.1–1.8%",
    footer_lines=["Version 1.0  ·  10 October 2026", "Status: derived", "Prepared from public sources, Eurostat data "
                  "and Malta’s National Energy and Climate Plan.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Magħtab waste-to-energy plant – WasteServ’s 4.5%", version="1.0", date="10 October 2026",
    pdf_title="4.5% of Malta’s energy from burning waste? Claim Check 079",
    pdf_subject="Tests WasteServ's statement that the Magħtab waste-to-energy plant would meet about 4.5% of Malta's "
                "total energy needs",
    story=S))
