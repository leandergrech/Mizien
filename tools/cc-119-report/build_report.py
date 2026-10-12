"""Claim Check 119 report. Run fetch.py, calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

LG = colors.HexColor("#8DB36B")
FIG = HERE / "out"
S = []

# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("The Council’s draft Recommendation on Malta says Malta’s renewables share is “very low and well below the EU average”: "
        "<b>17.2% of gross final energy consumption in 2024</b> and <b>16.7% in the electricity mix in 2025</b>, with generation "
        "“almost exclusively” from solar and “no wind or hydropower generation recorded”. <b>Eurostat’s data bear all of it "
        "out.</b> The 17.2% is Eurostat’s published figure (EU-27: 25.2%; only three Member States are lower). The 16.7% is "
        "<b>not</b> Eurostat’s renewable-electricity indicator (11.2%, provisional); it matches the share of renewables in "
        "Malta’s <i>domestic net generation</i> (363.3 of 2,176.3 GWh), which leaves out imports. The text does not say which "
        "measure it uses.", lead)]
S.append(key_points([
    ("17.2% in 2024 is exact.", "Eurostat nrg_ind_ren: 17.21%, against 25.24% for the EU-27; Malta is fourth lowest of 27 (Belgium, Luxembourg and Ireland are lower)."),
    ("16.7% in 2025 reproduces, on generation.",
     "Renewables were 16.69% of Malta’s 2025 net electricity generation (Eurostat early estimate). Against consumption, which includes imports "
     "(about a third of supply), Eurostat’s indicator gives 11.2% (provisional)."),
    ("“Well below the EU average” holds on every measure.", "EU-27 renewables in net generation: 47.3% (2025); Eurostat’s indicator: 49.9% (provisional)."),
    ("Solar is 97% of Malta’s renewable electricity.", "PV 326.7 of 336.0 GWh in 2024; the rest is biogas (2.8%). 2025: 96.8% PV, 3.2% combustible renewables."),
    ("No hydro; wind is a trace.", "Hydro: zero in every year 2013–2024. Wind: 0.033 GWh in 2024 (0.01% of renewable generation), so “none recorded” is true to rounding."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("17.2%", GREEN, "Renewables, share of gross final energy consumption, Malta 2024 (EU-27: 25.2%)"),
             ("16.7%", GREEN, "Renewables in Malta’s 2025 net generation (Eurostat early estimate; Eurostat’s consumption-based indicator: 11.2%, provisional)"),
             ("97%", ORANGE, "Solar PV share of Malta’s renewable electricity, 2024"),
             ("0", GREEN, "Hydropower generated in Malta, any year 2013–2024")]),
      Spacer(1, 4 * mm),
      up_down("Naming the measure behind 16.7% (domestic net generation) and its source would remove the one caveat and make it Supported.",
              "A final adopted text that changes the figures, or Eurostat revising Malta’s 2025 generation or 2024 share materially."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the data show"),
          ("4", "Where the evidence points different ways"), ("5", "Testing the claim"),
          ("6", "Verdict and requests for evidence"), ("7", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The words are paragraph (25) of the General Secretariat’s note of 3 July 2026 transmitting the draft Council Recommendation on "
           "Malta’s economic, social, employment, structural and budgetary policies (document 11130/26, p. 13) [1]. We read the whole "
           "text:"))
S.append(callout([P("THE COUNCIL’S WORDS (DRAFT RECOMMENDATION, PARAGRAPH 25)", tag),
                  P("“Malta’s share of renewables in gross final energy consumption (17.2% in 2024) and in the electricity mix (16.7% in "
                    "2025) remains very low and well below the EU average. The renewable energy generation is almost exclusively "
                    "coming from solar energy, with a very small part of biomass/combustible renewable fuels, and with no wind or "
                    "hydropower generation recorded.”", small)], bg=PALE, bar=GREEN))
S += [Spacer(1, 3 * mm), P("The paragraph goes on to note that Malta has announced a floating offshore wind farm expected by 2033 and that "
        "“there is scope to leverage further the potential of offshore solar and wind projects”. Those are plans and a recommendation, not "
        "statistics, and we do not rate them (the wind farm is the subject of CC-029).")]
S.append(std_table([
    [C("Source", cellh), C("What it gives", cellh), C("Our access", cellh), C("Status", cellh)],
    [C("<b>Council of the EU</b>, 11130/26, para. (25), p. 13 [1]"), C("The four statements above."),
     C("Read in full (22 pp.). A draft submitted for adoption."), C("<b>The claim</b>")],
    [C("<b>Eurostat</b> nrg_ind_ren; nrg_bal_peh; nrg_cb_pem; nrg_cb_e [2–5]"),
     C("Shares, generation by source and electricity supply for Malta, the EU-27 and every Member State."),
     C("Downloaded by API with status flags (12 Oct 2026)."), C("<b>Primary evidence</b>")],
    [C("The source of 16.7% and of “17.2%”"), C("The paragraph names no source."),
     C("We did not find the document that first states 16.7%; we tested which published series reproduces it."), C("Gap")],
], [44 * mm, 52 * mm, 50 * mm, 24 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("FAIRNESS NOTE", tag),
               P("A Council note summarises the Commission’s analysis and cannot define every measure in a recital. This check asks whether the "
                 "figures are right and whether the picture is fair, not whether the recommendation is wise. Government and opposition "
                 "statements on renewables are held to the same data (CC-024, CC-114).", small)], bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Question.</b> Are the four statements in the paragraph correct on published statistics, and is “very low and well below the "
           "EU average” a fair description?"))
S.append(P("<b>Evidence.</b> We downloaded from Eurostat’s API on 12 October 2026: nrg_ind_ren (shares; updated 15 Sep 2026), nrg_cb_pem "
           "(monthly net generation by fuel; updated 7 Oct 2026), nrg_cb_e (electricity supply; 9 Oct 2026) and nrg_bal_peh (generation by "
           "type of fuel; 2 Jun 2026), for Malta, the EU-27 and each Member State, keeping status flags. Every figure was recomputed "
           "by script (<i>tools/cc-119-report/calc.py</i>; outputs in <i>data/cc-119/</i>). Because “the electricity mix” is not "
           "defined in the text, we tested three readings and report all three. No peer-reviewed paper is needed to read a statistic "
           "against its source table; we rely on official statistics (grade C)."))

# ================================================================== 3
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(3, "What the data show"))
S.append(std_table([
    [C("Indicator", cellh), C("Malta", cellh), C("Comparator", cellh), C("Source", cellh), C("Grade", cellh)],
    [C("Renewables, share of gross final energy consumption, 2024"), C("<b>17.21%</b>"), C("EU-27 25.24%; Malta fourth lowest of 27"), C("Eurostat [2]"), grade_tag("C")],
    [C("Same, 2025 (early estimate, flag p)"), C("18.8%"), C("EU-27 26.2% (p)"), C("Eurostat [2]"), grade_tag("C")],
    [C("Renewables in <b>net generation</b>, 2025"), C("<b>16.69%</b>"), C("EU-27 47.3%; Malta second lowest of 27"), C("Eurostat [4]"), grade_tag("C")],
    [C("Same, 2024"), C("15.71%"), C("EU-27 47.2%"), C("Eurostat [4]"), grade_tag("C")],
    [C("Eurostat indicator: renewable electricity, share of gross electricity consumption, 2024 / 2025 (p)"), C("<b>10.65% / 11.2%</b>"), C("EU-27 47.5% / 49.9% (p)"), C("Eurostat [2]"), grade_tag("C")],
    [C("Imports as a share of final electricity consumption, 2024 / 2025 (p)"), C("33.8% / 34.7%"), C("—"), C("Eurostat [5]"), grade_tag("C")],
    [C("Solar PV share of renewable generation, 2024 / 2025"), C("<b>97.2% / 96.8%</b>"), C("PV 326.7 and 351.5 GWh"), C("Eurostat [3, 4]"), grade_tag("C")],
    [C("Biogas / combustible renewables share, 2024 / 2025"), C("2.8% / 3.2%"), C("9.3 and 11.7 GWh (flag e)"), C("Eurostat [3, 4]"), grade_tag("C")],
    [C("Wind generation, 2024 (annual balance)"), C("0.033 GWh"), C("0.01% of renewable generation; 0.058 to 0.085 GWh in 2013–2022"), C("Eurostat [3]"), grade_tag("C")],
    [C("Hydro generation, 2013–2024"), C("<b>0</b>"), C("—"), C("Eurostat [3]"), grade_tag("C")],
], [58 * mm, 26 * mm, 42 * mm, 30 * mm, 14 * mm]))
S.append(P("Values in <i>data/cc-119/checks.csv</i>. Eurostat’s 2025 generation and consumption values are early estimates (flags e, p) and the "
           "series are revised.", cap))
S.append(fig(FIG / "fig_rank.png"))
S.append(P("Figure 1. Renewables as a share of gross final energy consumption, 2024, all 27 Member States. Malta is fourth lowest; only Belgium, "
           "Luxembourg and Ireland are lower.", cap))
S.append(P("Which “electricity mix” is 16.7%?", h2))
S.append(P("Eurostat’s own renewable-electricity indicator, the share of renewables in gross electricity consumption, gives Malta 10.65% in 2024 "
           "and 11.2% (provisional) in 2025, not 16.7%. The Council’s figure matches a different quantity: renewable electricity divided by "
           "Malta’s <i>domestic</i> net generation, 363.3 GWh of 2,176.3 GWh in 2025 (16.69%). This excludes imports over the "
           "interconnector, which supplied about a third of final consumption. We cannot say the Council used this series, because the paragraph "
           "names none; but it is the only one of the three that reproduces the number, and it is a fair reading of “the electricity mix” "
           "of Malta’s power stations and panels. Read against the electricity Malta consumes, the share is lower, not higher."))
S.append(KeepTogether([fig(FIG / "fig_measures.png"),
                       P("Figure 2. Malta’s 2025 renewable-electricity share on three bases against the Council’s 16.7%, with the EU-27 where Eurostat or "
                         "the same series allows. The EU-27 comparison is far above Malta on both bases we could compute.", cap)]))
S.append(KeepTogether([fig(FIG / "fig_sources.png"),
                       P("Figure 3. Malta’s renewable electricity by source, 2013–2024. Solar PV is almost all of it; biogas is the rest; wind is below "
                         "0.1 GWh in every year and hydro is zero.", cap)]))

# ================================================================== 4
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(4, "Where the evidence points different ways"))
S.append(contested(
    "Q1  What does “16.7% in the electricity mix” measure?", "REPRODUCED ON GENERATION", AMBER,
    "Renewables are 16.69% of Malta’s 2025 net generation (363.3 of 2,176.3 GWh), which equals the Council’s 16.7% [4].",
    "Eurostat’s consumption-based indicator for the same year is 11.2% (provisional), and the simple ratio of renewable generation to final "
    "consumption is 12.2% [2, 5].",
    "<b>For this claim:</b> the figure is right on generation but is the more favourable of the readings; the paragraph does not say which it is. "
    "Every reading is far below the EU’s.",
    label_a="WHERE 16.7% COMES FROM", label_b="OTHER READINGS"))
S.append(contested(
    "Q2  “No wind or hydropower generation recorded”", "TRUE TO ROUNDING", GREENC,
    "Hydro is zero in every year 2013–2024, and monthly net generation by fuel shows 0.0 GWh of wind in 2024 and 2025 [3, 4].",
    "Eurostat’s annual generation balance records a trace of wind, 0.033 GWh in 2024 (0.058 GWh in 2022), in every year since 2013 [3].",
    "<b>For this claim:</b> the trace is about 33 MWh, 0.01% of renewable generation. “None recorded” is accurate in any practical sense but not "
    "literally zero in the annual table.",
    label_a="NO WIND OR HYDRO", label_b="A TRACE OF WIND"))

# ================================================================== 5
S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(5, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> Renewables are 17.2% of gross final energy consumption in 2024, “very low and well below the EU average”"), C("Council, para. (25) [1]"),
     C("Eurostat: 17.21%; EU-27 25.24%; fourth lowest of 27 [2]."), verd("ACCURATE", GREENC)],
    [C("<b>B.</b> Renewables are 16.7% of the electricity mix in 2025, “very low and well below the EU average”"), C("Council, para. (25) [1]"),
     C("Reproduces as the share of domestic net generation (16.69%); Eurostat’s consumption-based indicator gives 11.2% (provisional). EU-27: 47.3% on generation, "
       "49.9% on the indicator [2, 4]. The measure is not named."), verd("ACCURATE, MEASURE UNNAMED", LG)],
    [C("<b>C.</b> Renewable generation is “almost exclusively” solar, with “a very small part of biomass/combustible renewable fuels”"), C("Council, para. (25) [1]"),
     C("PV 97.2% (2024) and 96.8% (2025) of renewable generation; biogas 2.8% and 3.2% [3, 4]."), verd("ACCURATE", GREENC)],
    [C("<b>D.</b> “No wind or hydropower generation recorded”"), C("Council, para. (25) [1]"),
     C("Hydro zero throughout; wind 0.033 GWh in 2024 in the annual balance, 0.0 in monthly net generation [3, 4]."), verd("ACCURATE, TRACE OF WIND", LG)],
], [44 * mm, 24 * mm, 66 * mm, 36 * mm], valign="MIDDLE"))

# ================================================================== 6
S += [Spacer(1, 6 * mm), SectionHeading(6, "Verdict and requests for evidence"),
      verdict_box("Largely supported", "Every figure reproduces from Eurostat; the 2025 electricity figure is on generation, a basis the text does not name. Confidence: high."),
      Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> The 2024 share and the “well below the EU average” description are exact. The 2025 electricity figure, 16.7%, matches Eurostat’s "
           "generation data to the decimal. The description of solar, biomass and the absence of hydro is right and wind is a rounding-level trace. "
           "The one caveat is that “the electricity mix” is not defined and the 16.7% is the highest of three readings: this does not change the "
           "substance, which is that Malta is among the lowest in the EU on every one. Our scale gives <i>Supported</i> only when the evidence backs "
           "the claim as stated, so an unnamed measure keeps this at <i>Largely supported</i>."))
S.append(P("<b>What this does not say.</b> It does not assess the recommendation, the 2033 offshore wind farm, or Malta’s 2030 target (see CC-024 and CC-029). "
           "It does not say the Commission or the Council chose the measure to flatter; the text names no source and we have not found one."))
S.append(KeepTogether([P("Evidence we are asking for", h2), requests_list([
    "The source and the measure behind “16.7% in 2025”, if it is not Eurostat’s monthly net generation (nrg_cb_pem).",
    "Confirmation whether the adopted Council Recommendation keeps paragraph (25) unchanged.",
])]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag),
               P("No right of reply needed: the verdict is <i>Largely supported</i>. A correction or comment from the Council Secretariat or the Commission "
                 "would be appended if received.", small)], bg=PALE, bar=GREEN)]

# ================================================================== 7
S += [Spacer(1, 6 * mm), SectionHeading(7, "Limitations")]
for l in ["The paragraph is from a <b>draft</b> note of 3 July 2026. We have not found the adopted text, so it may differ.",
          "The 2025 values (18.8%, 11.2%, and the 2025 net generation and consumption) are Eurostat early estimates (flags p, e); the monthly "
          "net generation series carries flag e. A revision could change the second decimal of 16.7%.",
          "We did not locate the source document of 16.7% or of the Council’s figures (a Commission staff document is likely but unverified); "
          "our attribution of 16.7% to the generation share is a reproduction, not a confirmed source.",
          "“No wind recorded” is tested against Eurostat. We did not check small installations that do not report to Eurostat.",
          "Eurostat’s EU-27 renewable share of net generation is our own sum of monthly national values; the SHARES indicator is Eurostat’s own.",
          "We did not compare Eurostat’s figures with Enemalta’s or the National Statistics Office’s own releases (the NSO site is refused to scripts); Eurostat takes Malta’s data from the NSO."]:
    S.append(P("• " + l, bul))

S += [CondPageBreak(70 * mm), Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Council of the European Union, General Secretariat (3 Jul 2026). Council Recommendation on the economic, social, employment, structural and "
          "budgetary policies of Malta (draft), document 11130/26, para. (25), p. 13.",
     "https://data.consilium.europa.eu/doc/document/ST-11130-2026-INIT/en/pdf"),
    ("2", "Eurostat. Share of energy from renewable sources (nrg_ind_ren), updated 15 Sep 2026, retrieved 12 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/nrg_ind_ren/default/table"),
    ("3", "Eurostat. Production of electricity and derived heat by type of fuel (nrg_bal_peh), updated 2 Jun 2026, retrieved 12 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/nrg_bal_peh/default/table"),
    ("4", "Eurostat. Net electricity generation by type of fuel, monthly data (nrg_cb_pem), updated 7 Oct 2026, retrieved 12 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/nrg_cb_pem/default/table"),
    ("5", "Eurostat. Electricity supply, transformation and consumption, annual data (nrg_cb_e), updated 9 Oct 2026, retrieved 12 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/nrg_cb_e/default/table"),
    ("6", "Miżien. Calculation script and outputs: tools/cc-119-report/calc.py; data/cc-119/checks.csv.", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "12 Oct 2026", "First issue. No right of reply needed.")])

build_report(Report(
    number="119", out=str(FIG / "report.pdf"), kicker="Climate and energy",
    title_lines=["Council on Malta’s", "renewables:", "the numbers"],
    subtitle_lines=["Testing the Council’s draft Recommendation", "against Eurostat data"],
    quote_lines=["“Malta’s share of renewables … (17.2% in 2024) and in the", "electricity mix (16.7% in 2025) remains very low …”"], quote_size=15,
    attribution="Council of the European Union, draft Recommendation on Malta, para. (25), 3 July 2026.",
    context="Almost exclusively solar, “with no wind or hydropower generation recorded”.",
    verdict="Largely supported", verdict_note="Figures reproduce; one measure unnamed",
    footer_lines=["Version 1.0  ·  12 October 2026", "Status: no right of reply needed",
                  "Prepared from public sources and Eurostat data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Council on Malta’s renewables", version="1.0", date="12 October 2026",
    pdf_title="Council on Malta's renewables: the numbers. Claim Check 119",
    pdf_subject="Tests the Council's draft Recommendation statement on Malta's renewables against Eurostat data",
    story=S))
