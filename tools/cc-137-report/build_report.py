"""Claim Check 137 report. Run calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []

# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("On 21 July 2026 the Malta Chamber of Commerce, Enterprise and Industry said of the July power cuts that "
        "<b>“this increase was predictable – given the trends in increase in population”</b> and that <b>“It is "
        "evident that the investment carried out was not enough”</b>. The Chamber gave no figures. We tested what "
        "can be tested from public data: whether the rise in demand was foreseeable, and how much of it population "
        "explains. The sufficiency of investment could not be tested from documents we could open.", lead)]
S.append(key_points([
    ("The rise in peak demand was visible in the trend.",
     "A straight line fitted to the NSO’s annual peaks for 2017–2022 gives 631 MW for 2025; the actual peak "
     "was 637 MW. Peaks rose in 5 of the 8 years from 2018 to 2025."),
    ("Population explains about a third of it, not most.",
     "Peak demand rose 42.6% from 2018 to 2023 (465 to 663 MW); residents plus peak-month tourists rose 13.4%. "
     "Had peak demand per person present stayed at the 2018 level, the 2023 peak would have been about 527 MW, "
     "so people present account for about 31% of the 198 MW rise."),
    ("The Chamber also names tourists and climate.",
     "Its statement, as we could read it, lists population, tourist numbers and rising temperatures; the "
     "quoted phrase singles out population. The hottest month at Luqa was 2.5 °C warmer in 2023 than in 2018."),
    ("‘Investment was not enough’ has no yardstick.",
     "Neither the Chamber nor any document we could open gives the investment needed. The National Audit Office’s "
     "2024 review is reported to find high-voltage capital spending falling from about EUR 15 million a year to "
     "EUR 5.7 million in 2023 ◆ (second-hand; we could not open it). The Government says EUR 161 million was invested "
     "since 2022 ◆. Neither settles ‘enough’."),
    ("Verdict: not substantiated (low confidence).",
     "The foreseeability limb holds up; the investment limb is a judgement we could not test first-hand."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(2), Spacer(1, 3 * mm),
      tiles([("+42.6%", ORANGE, "Peak demand 2018 to 2023 (465 to 663 MW), NSO"),
             ("+13.4%", GREEN, "Residents plus peak-month tourists, same years, Eurostat"),
             ("31%", ORANGE, "Share of the 2018–2023 rise in peak demand accounted for by more people present"),
             ("631 MW", GREEN, "2025 peak predicted by the 2017–2022 trend (actual: 637 MW)")]),
      Spacer(1, 4 * mm),
      up_down("The investment actually made in the distribution network, set against a stated need (a planning standard "
              "or Enemalta’s own load forecast), showing a shortfall; or the NAO review’s figures read in full.",
              "Evidence that spending matched the network’s planned needs and that the July 2026 faults had causes "
              "unrelated to capacity, such as the fault-cause analysis the Government has cited."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the data show"),
          ("4", "Where the evidence points different ways"), ("5", "Testing the claim"),
          ("6", "Verdict and requests for evidence"), ("7", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The statement is a press statement of the Malta Chamber, published by Business Now on 21 July 2026 [1], "
           "headed ‘Predictable strain, unacceptable disruption’. A fuller reader’s extract of the page (28 Oct 2026) "
           "confirmed the sentence on investment and the date; the other two phrases were read on 25 Oct 2026. Both "
           "were read through a web reader, not a saved copy, so the quoted words should be checked against the page. "
           "Where the Chamber’s words are not in quotation marks below, they are our paraphrase."))
S.append(std_table([
    [C("What was said", cellh), C("Who", cellh), C("Access", cellh)],
    [C("“this increase was predictable – given the trends in increase in population”"),
     C("Malta Chamber [1]"), C("Via web reader (intake, 25 Oct 2026)")],
    [C("“It is evident that the investment carried out was not enough”"), C("Malta Chamber [1]"),
     C("Via web reader, 25 and 28 Oct 2026")],
    [C("The cuts are “linked directly with the country’s economic growth model”"), C("Malta Chamber [1]"),
     C("Via web reader (intake, 25 Oct 2026)")],
    [C("Population, tourist numbers and rising temperatures “place additional and predictable pressures” on "
       "infrastructure (reader’s extract; not rated)"), C("Malta Chamber [1]"), C("Via web reader, 28 Oct 2026")],
], [88 * mm, 36 * mm, 46 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("SCOPE NOTE", tag),
               P("This check covers the measurable parts: whether the rise in demand was foreseeable and what population "
                 "explains, and what is known about investment. The Chamber’s view that the cuts follow from the "
                 "country’s growth model is a characterisation and is not rated. We do not test who caused the July "
                 "2026 faults (see CC-027).", small)], bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Question.</b> Was the rise in electricity demand foreseeable from past trends, how much of it do population "
           "and tourists account for, and is there evidence that investment was or was not enough?"))
S.append(P("<b>Evidence.</b> Annual peak demand (the highest monthly maximum) from the National Statistics Office’s "
           "Electricity Supply releases 2017–2025 [2]; Eurostat population (demo_gind), tourist nights (tour_occ_nim) and "
           "final electricity consumption (nrg_cb_e) [3]; NOAA GHCN-Daily temperatures at Luqa [4]. Tourists present are "
           "peak-month nights divided by 31, the method of the IMF’s paper in CC-135. These are the same inputs, "
           "copied to <i>data/cc-137/</i> with their retrieval dates, and all numbers are recomputed by "
           "<i>tools/cc-137-report/calc.py</i>. For investment we found only second-hand reports (◆) [5][6]."))
S.append(P("<b>Foreseeability test.</b> We fit a straight line to the annual peaks for 2017–2022 only, as a forecaster "
           "would have had them before the 2023 peak, and compare its extension with the actual peaks. This is a "
           "plausibility test of ‘predictable’, not a forecasting model."))
S.append(P("<b>Grades.</b> Official statistics are grade C; the Chamber’s statement and reports of documents we did "
           "not open are grade D. <b>Verdicts</b> follow the five-point scale in Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(150 * mm))
S.append(SectionHeading(3, "What the data show"))
S.append(fig(FIG / "fig1_peak.png"))
S.append(P("Figure 1. Annual peak electricity demand in Malta, 2017–2025 (NSO), with a trend line fitted to 2017–2022 only. "
           "The 2023 peak (orange) is above the line; 2024 fell back and 2025 is on it.", cap))
S.append(std_table([
    [C("Indicator", cellh), C("Value", cellh), C("Source", cellh), C("Grade", cellh)],
    [C("Peak demand 2018 → 2023"), C("465 → 663 MW (<b>+42.6%</b>)"), C("NSO [2]"), grade_tag("C")],
    [C("Residents plus peak-month tourists 2018 → 2023"), C("<b>+13.4%</b>"), C("Eurostat [3]"), grade_tag("C")],
    [C("Residents alone (annual average) 2018 → 2023"), C("+14.2%"), C("Eurostat [3]"), grade_tag("C")],
    [C("Final electricity consumption 2018 → 2023"), C("+13.4%"), C("Eurostat [3]"), grade_tag("C")],
    [C("Peak per person present, 2018 → 2023"), C("0.89 → 1.12 kW (+25.7%)"), C("NSO; Eurostat"), grade_tag("C")],
    [C("2023 peak if peak per person had stayed at the 2018 level"), C("527 MW; people present explain <b>31%</b> of the rise"),
     C("calculated"), grade_tag("C")],
    [C("Trend 2017–2022, extended to 2023 and 2025"), C("588 MW (actual 663) and 631 MW (actual 637)"),
     C("calculated from NSO"), grade_tag("C")],
    [C("Years with a higher peak than the year before, 2018–2025"), C("5 of 8"), C("NSO [2]"), grade_tag("C")],
    [C("Hottest-month mean temperature at Luqa"), C("26.9 °C (2018); 29.4 °C (2023); 28.1 °C (2025)"),
     C("NOAA [4]"), grade_tag("C")],
], [66 * mm, 60 * mm, 32 * mm, 12 * mm]))
S.append(P("All values are in <i>data/cc-137/checks.csv</i>. The NSO series was transcribed through a web reader because "
           "nso.gov.mt refuses scripts; the 2022–2025 values come from the releases’ text and may have been revised "
           "(see CC-135).", cap))
S.append(KeepTogether([fig(FIG / "fig2_growth.png"),
                       P("Figure 2. Growth 2018 to 2023: peak demand against the number of people present and energy used. "
                         "Energy and people grew together; the peak grew about three times as fast.", cap)]))
S.append(P("Two readings follow. First, a rising peak was not a surprise: it was the established direction. Second, "
           "population is not what drove most of the rise in the peak: energy use tracked population, while the peak "
           "per person present rose by about a quarter. CC-135 shows that the end years 2018 and 2023 are the coolest "
           "and hottest summers of the period, which makes 2018–2023 the steepest window; the IMF paper treated "
           "temperature as a possible part of the explanation."))

# ================================================================== 4
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(4, "Where the evidence points different ways"))
S.append(contested(
    "Q1  Was the rise in demand predictable?", "YES, AS A TREND", GREEN,
    "Peaks rose in 5 of 8 years; the 2017–2022 trend gave 631 MW for 2025 against an actual 637 MW. The IMF’s "
    "February 2025 paper already reported the 43% rise and a 30% further rise projected by 2040 (CC-135).",
    "A single hot summer is hard to foresee: the 2023 peak was 12.7% above the 2017–2022 trend, and 2024 fell "
    "below it. The July 2026 peak of 741 MW reported elsewhere (CC-027) is not verified.",
    "<b>For this claim:</b> ‘predictable’ holds as a direction and rough rate; it does not hold for the size of any "
    "one summer’s peak."))
S.append(contested(
    "Q2  Does population explain the increase?", "ONLY IN PART", AMBER,
    "People present grew 13.4% from 2018 to 2023, and energy use grew 13.4%. Population is a real driver of the base load.",
    "The peak grew 42.6%. At constant peak per person the 2023 peak would have been 527 MW, 136 MW short of the "
    "actual 663 MW. Temperature, air-conditioning use and the peak-month mix are not separated here.",
    "<b>For this claim:</b> ‘given the trends in increase in population’ is a partial explanation; the Chamber’s fuller "
    "text also names tourists and temperature."))
S.append(contested(
    "Q3  Was the investment carried out enough?", "NOT TESTABLE FROM WHAT WE COULD OPEN", AMBER,
    "The National Audit Office’s review of July 2024 is reported (The Shift, MaltaToday summaries ◆) to find high-voltage "
    "capital investment falling from an average of about EUR 15 million a year in 2014–2018 to EUR 5.7 million in 2023, "
    "and actual spending below budget, while demand rose.",
    "The Government says EUR 161 million was invested in distribution since 2022 and that the July 2026 problem was "
    "the distribution network under heat, not generation (CC-027, reported speech ◆). Enemalta disputed the NAO’s "
    "reading in 2024 (reported ◆). No source gives the investment the network needed.",
    "<b>For this claim:</b> the direction of the 2014–2023 reports is consistent with ‘not enough’, but ‘enough’ needs a "
    "benchmark, and the post-2023 spending is only the Government’s figure."))

# ================================================================== 5
S.append(CondPageBreak(90 * mm))
S.append(SectionHeading(5, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> “this increase was predictable”"),
     C("The 2017–2022 trend gave 631 MW for 2025 (actual 637); peaks rose in 5 of 8 years [2]."),
     verd("SUPPORTED", GREENC)],
    [C("<b>B.</b> “given the trends in increase in population”"),
     C("People present +13.4% against peak demand +42.6%; they account for about 31% of the 2018–2023 rise [2][3]."),
     verd("PARTLY", AMBER)],
    [C("<b>C.</b> “It is evident that the investment carried out was not enough”"),
     C("No figure for investment made or needed in the statement; NAO findings known second-hand only ◆ [5][6]."),
     verd("NOT SUBSTANTIATED", AMBER)],
    [C("<b>D.</b> Cuts “linked directly with the country’s economic growth model”"),
     C("A characterisation; not rated."), verd("NOT RATED", GREY)],
], [58 * mm, 82 * mm, 30 * mm], valign="MIDDLE"))

# ================================================================== 6
S += [Spacer(1, 6 * mm), SectionHeading(6, "Verdict and requests for evidence"),
      verdict_box("Not substantiated", "The rise was foreseeable; ‘investment was not enough’ is stated without a "
                  "yardstick. Confidence: low."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) The foreseeability limb is backed by NSO and Eurostat data. (2) Population alone explains only "
           "about a third of the rise in the peak, so ‘given the trends in population’ understates the other drivers "
           "the Chamber itself lists. (3) The sufficiency of investment, the most consequential part, is stated as "
           "evident but supported by no figure in the statement, and the documents that bear on it (the NAO review, "
           "Enemalta’s accounts) were not readable by us. A statement whose central judgement cannot be tested stays "
           "‘not substantiated’, not ‘contradicted’: the second-hand reports point the same way as the Chamber. "
           "Confidence is low because the key evidence is second-hand."))
S.append(P("<b>What this verdict does not say.</b> It does not say the Chamber is wrong, that investment was adequate, "
           "or who is responsible for the cuts. It says the sufficiency claim has not been shown on documents we could "
           "read. It is a draft pending right of reply."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "The Chamber’s basis for ‘investment was not enough’: the figures it relied on.",
    "The NAO’s ‘High-Level Review on Enemalta’s Planning and Investment in the Local Distribution Network’ (July 2024), "
    "in full, and Enemalta’s yearly distribution capital expenditure 2019–2026.",
    "Enemalta’s or the regulator’s load forecast and planning standard for the distribution network.",
]))

# ================================================================== 7
S += [Spacer(1, 6 * mm), SectionHeading(7, "Limitations")]
for l in ["The Chamber’s statement was read only through a web reader; its wording should be checked against the page "
          "(Business Now returns 403 to scripts). The sentence introducing ‘this increase’ was paraphrased by the reader "
          "as ‘an increased demand increases strain’, not quoted.",
          "The NAO review, MaltaToday and Malta Business Weekly returned 403 or 503; the NAO figures come from a Shift "
          "article and search summaries (◆), and the EUR 5.7 million and EUR 15 million figures are the outlets’ reports "
          "of the review, not the review’s text.",
          "Search log (28 Oct 2026): Enemalta or Government distribution investment for 2024–2026 was searched on the web "
          "(one query); no 2025–2026 figure was found beyond the Government’s EUR 161 million (CC-027). Enemalta’s annual "
          "accounts were not searched.",
          "The foreseeability test is a straight line on nine annual peaks; it does not separate temperature, air-"
          "conditioning, or the peak month’s tourists. Peak demand 2022–2025 was transcribed from release texts.",
          "Outage records and Enemalta reliability indices were not obtained, so the link between investment and the July "
          "2026 cuts is not tested."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Malta Chamber of Commerce, Enterprise and Industry (21 Jul 2026). Predictable strain, unacceptable disruption: "
          "Malta Chamber urges immediate action over power cuts. <i>Business Now</i>.",
     "https://businessnow.mt/predictable-strain-unacceptable-disruption-malta-chamber-urges-immediate-action-over-power-cuts/"),
    ("2", "National Statistics Office Malta. Electricity Supply, news releases 2022–2026 (maximum demand). Transcribed "
          "26 Oct 2026; see data/cc-137/nso_max_demand.csv.", "https://nso.gov.mt/"),
    ("3", "Eurostat. demo_gind, tour_occ_nim, nrg_cb_e; retrieved 26 Oct 2026.", "https://ec.europa.eu/eurostat/databrowser/"),
    ("4", "NOAA NCEI. GHCN-Daily, station MT000016597 (Luqa); retrieved 26 Oct 2026.",
     "https://www.ncei.noaa.gov/data/global-historical-climatology-network-daily/access/MT000016597.csv"),
    ("5", "◆ The Shift (16 Jul 2024). NAO confirmed 2023 electricity failure was result of lack of investment in grid. "
          "Reports the NAO review; read via web reader, review not opened.",
     "https://theshiftnews.com/2024/07/16/confirmed-2023-electricity-failure-was-result-of-lack-of-investment-in-grid/"),
    ("6", "◆ National Audit Office (15 Jul 2024). High-Level Review on Enemalta’s Planning and Investment in the Local "
          "Distribution Network. Page and PDF returned 403; known from search summaries only.",
     "https://nao.gov.mt/2024/07/15/high-level-review-on-enemaltas-planning-and-investment-in-the-local-distribution-network/"),
    ("7", "Miżien. CC-135 (IMF on peak demand) and CC-027 (Government account of the July 2026 cuts). Data and "
          "calculations: data/cc-137/; tools/cc-137-report/calc.py.", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "28 Oct 2026", "First issue.")])

build_report(Report(
    number="137", out=str(FIG / "report.pdf"), kicker="Climate and energy",
    title_lines=["Were Malta’s July", "power cuts", "predictable?"],
    subtitle_lines=["Testing the Malta Chamber’s statement on demand,",
                    "population and investment against NSO and Eurostat data"],
    quote_lines=["“It is evident that the investment", "carried out was not enough.”"], quote_size=16,
    attribution="Malta Chamber of Commerce, Enterprise and Industry, 21 July 2026.",
    context="A statement on the July 2026 power cuts, with no figures.",
    verdict="Not substantiated", verdict_note="Foreseeable rise; no yardstick for ‘enough’",
    footer_lines=["Version 1.0  ·  28 October 2026", "Status: draft",
                  "Prepared from public sources, NSO and Eurostat data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="July power cuts – Malta Chamber", version="1.0", date="28 October 2026",
    pdf_title="Were Malta's July power cuts predictable? Claim Check 137",
    pdf_subject="Tests the Malta Chamber's statement of 21 July 2026 on the power cuts",
    story=S))
