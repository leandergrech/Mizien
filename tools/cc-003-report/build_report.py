"""Claim Check 003 report. Run calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []

# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("Malta’s Climate Action Authority (CAA) said in November 2025 that <b>emissions per person have fallen "
        "44% since 2005, well above the EU average of 34%</b>, and that this shows Malta “reducing emissions both "
        "at household level and across the economy”. The figures come from the European Commission’s 2025 "
        "Climate Action Progress Report. <b>The same report projects that Malta will miss its binding 2030 target by "
        "the widest margin in the EU in percentage points.</b> The CAA release does not mention that projection.", lead)]
S.append(key_points([
    ("The numbers are right.",
     "Eurostat data reproduce a per-person fall of about 46% (2005–2023) for Malta against 34% for the EU."),
    ("About half of it is population growth.",
     "Malta’s population grew 41% since 2005. Total emissions fell 27%, less than the EU’s 33%. Measured in "
     "total tonnes, Malta cut less than the EU average, not more."),
    ("Nearly all of the cut came from one sector.",
     "Power generation fell 63% after the 2015 interconnector and the switch from heavy fuel oil to gas. "
     "Transport rose 49%, buildings 9% and refrigerant gases almost six-fold."),
    ("The binding target is going the wrong way.",
     "Emissions under the EU Effort Sharing Regulation (transport, buildings, waste, farming, F-gases) were 41% "
     "above 2005 in 2024. The target is −19% by 2030; even with planned measures the Commission projects +30%."),
    ("Verdict: misleading.",
     "Each figure is accurate, but citing the per-person result from the report while omitting its central finding "
     "on Malta leaves an inaccurate overall impression."),
]))
S += [Spacer(1, 4 * mm), VerdictMeter(3), Spacer(1, 3 * mm),
      tiles([("−44%", GREEN, "Per-person change since 2005, as stated by the CAA (EU −34%)"),
             ("+41%", GREY, "Malta population growth, 2005–2024 (EU +4%)"),
             ("−27%", ORANGE, "Total emissions change, 2005–2024 (EU −33%)"),
             ("49 pts", RED, "Projected 2030 gap to the effort-sharing target, with planned measures")]),
      Spacer(1, 4 * mm),
      up_down("A published path showing how effort-sharing emissions (transport, buildings, F-gases) will fall "
              "from +41% to −19% by 2030; evidence that the projections are out of date; or a statement "
              "that put the per-person figure next to the 2030 projection.",
              "Evidence that the per-person figure is used in place of the target metric in other official "
              "communications, or that Malta plans to rely mainly on buying allocations from other states."),
      Spacer(1, 5 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "Why per person and total differ"),
          ("4", "What the data show"), ("5", "Where the evidence points different ways"),
          ("6", "Testing the claim"), ("7", "Verdict and requests for evidence"), ("8", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The claim is the Climate Action Authority’s own press release of 13 November 2025 [1], read in full "
           "from an archived copy. MaltaToday reported it the same week, quoting the authority [2]. A news-agency "
           "report on the same EU publication led instead with Malta’s projected 2030 increase [3]. We assess "
           "the authority’s wording, not the headlines."))
S.append(std_table([
    [C("Source", cellh), C("What it says", cellh), C("Our access", cellh), C("Status", cellh)],
    [C("<b>Climate Action Authority</b>, press release, 13 Nov 2025 [1]"),
     C("“Emissions per capita have fallen by 44% since 2005, well above the EU average of 34%.” Emissions per "
       "unit of GDP down 81.6% (EU 61.9%). The figures “show that Malta is reducing emissions both at household "
       "level and across the economy, while continuing to grow.” Transport and buildings named as sectors "
       "“where challenges remain”. No mention of the 2030 projection."),
     C("Read in full (Wayback copy, 15 Apr 2026). Live site blocks automated access."), C("<b>The claim</b>")],
    [C("<b>MaltaToday</b>, Nov 2025 [2]"), C("Repeats the authority’s figures and quotes it."),
     C("Read in full (Wayback copy)."), C("Relay")],
    [C("<b>Italpress / MNA</b>, 17 Nov 2025 [3]"),
     C("Same EU report: Malta’s emissions to rise about 30% above 2005 by 2030 against a 19% cut, a gap of 49 "
       "points; per-person fall of 44% also reported."), C("Read in full."), C("Context")],
    [C("<b>European Commission</b>, CAPR 2025 staff working document [4] and chapter 3 [5]"),
     C("Malta’s effort-sharing emissions and projections; sector trends; Malta among the three Member States "
       "with the largest projected 2030 gaps."), C("Read: all Malta passages."), C("<b>Primary evidence</b>")],
    [C("<b>CAA factsheet</b>, June 2026"), C("Listed in our candidate file as the authority’s framing."),
     C("Not read: blocked, no archived copy."), C("Gap")],
], [36 * mm, 76 * mm, 36 * mm, 22 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("FAIRNESS NOTE", tag),
               P("Malta’s power-sector transformation is real and large: emissions from electricity generation "
                 "fell by almost two-thirds after the Malta–Sicily interconnector (2015) and the conversion of "
                 "Delimara to gas. Per-person and per-GDP indicators are legitimate and the Commission publishes "
                 "them. The release also says transport and buildings remain challenging. This check is about what "
                 "the release leaves out, not about whether the indicators are valid.", small)],
              bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Question.</b> Is the per-person comparison accurate, and does it give a fair picture of Malta’s "
           "progress on emissions as the same EU report assesses it?"))
S.append(P("<b>Evidence.</b> This claim is statistical, so independent datasets carry most of the weight. We "
           "downloaded Eurostat greenhouse-gas inventories (env_air_gge), population (nama_10_pe) and renewables "
           "shares (nrg_ind_ren) on 2 October 2026 and recomputed every percentage with a script "
           "(<i>tools/cc-003-report/calc.py</i>; outputs in <i>data/cc-003/</i>). We read every passage on Malta in "
           "the Commission’s staff working document. Peer-reviewed literature was searched for Malta-specific "
           "decompositions of emissions; none was found (Section 8)."))
S.append(P("<b>Grades.</b> Official statistics and EU assessments are grade C under our scale (official statistics "
           "summary). The two peer-reviewed papers on Maltese transport are context only. <b>Verdicts</b> follow "
           "the five-point scale in Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(3, "Why per person and total differ"))
S.append(P("Emissions per person are total emissions divided by population. If the population grows, the "
           "per-person figure falls even when total emissions do not change. This is the identity behind the "
           "“impact = population × impact per person” framing used in environmental science since the "
           "1970s [12 ◆]. Malta’s population grew 41% over the period, second only to Luxembourg (+46%) in the EU, "
           "so the two measures diverge more for Malta than for almost any other state."))
S.append(fig(FIG / "fig1_index.png"))
S.append(P("Figure 1. Malta’s total emissions, population and emissions per person, indexed to 2005, with EU-27 "
           "for comparison. Per-person emissions fell further than total emissions because the denominator rose 41%.",
           cap))
S.append(callout([P("THE ARITHMETIC", tag),
                  P("Total emissions: 2.99 Mt (2005) to 2.17 Mt (2024), −27%. Population: 404,000 to 569,000, "
                    "+41%. Per person: 7.4 t to 3.8 t, −48%. On a logarithmic split, <b>52% of the per-person "
                    "fall is explained by population growth</b> and 48% by lower total emissions. For the EU, "
                    "population grew 4% and per-person and total falls are nearly the same.", small)],
                 bg=BLUE_PALE, bar=BLUE))

# ================================================================== 4
S.append(PageBreak())
S.append(SectionHeading(4, "What the data show"))
S.append(fig(FIG / "fig2_sectors_esr.png"))
S.append(P("Figure 2. Left: emissions by sector, Malta, 2005–2024 (Eurostat). Power generation is covered by "
           "the EU Emissions Trading System (ETS); the other sectors count towards Malta’s national "
           "effort-sharing target. Right: effort-sharing emissions relative to 2005 and the 2030 target "
           "(Commission).", cap))
S.append(std_table([
    [C("Indicator", cellh), C("Malta", cellh), C("EU-27", cellh), C("Source", cellh), C("Grade", cellh)],
    [C("Per-person emissions, 2005–2023"), C("<b>−46%</b>"), C("−34%"), C("Eurostat [6, 7]; CAA cites −44% / −34% [1]"), grade_tag("C")],
    [C("Total emissions, 2005–2024"), C("<b>−27%</b>"), C("−33%"), C("Eurostat [6]"), grade_tag("C")],
    [C("Population, 2005–2024"), C("+41%"), C("+4%"), C("Eurostat [7]"), grade_tag("C")],
    [C("Power generation emissions, 2005–2024"), C("−63%"), C("−54%"), C("Eurostat [6]"), grade_tag("C")],
    [C("Domestic transport emissions, 2005–2024"), C("+49%"), C("−5%"), C("Eurostat [6]; Commission [4] pp. 51–52"), grade_tag("C")],
    [C("Industrial emissions (mainly refrigeration and air-conditioning gases), 2005–2023"), C("+293%"), C("−36%"),
     C("Commission [4] p. 44"), grade_tag("C")],
    [C("Buildings emissions since 2005"), C("+12%"), C("fell in every other state but Romania"), C("Commission [4] p. 59"), grade_tag("C")],
    [C("Effort-sharing emissions, 2024 vs 2005"), C("<b>+41%</b>"), C("−20%"), C("Commission [4] pp. 114–115"), grade_tag("C")],
    [C("2030 projection, existing measures / with planned measures"), C("<b>+42% / +30%</b>"), C("−31% / −38%"),
     C("Commission [4] pp. 114–115"), grade_tag("C")],
    [C("2030 effort-sharing target"), C("−19%"), C("−40% (EU)"), C("Commission [4] pp. 114–115"), grade_tag("C")],
    [C("Renewables share of electricity, 2024"), C("10.7%"), C("47.5%"), C("Eurostat [8]"), grade_tag("C")],
], [60 * mm, 26 * mm, 26 * mm, 46 * mm, 12 * mm]))
S.append(P("All values recomputed or transcribed in <i>data/cc-003/checks.csv</i>. The Commission’s per-person "
           "series uses net emissions and an earlier inventory; ours uses the 2026 inventory excluding land use, so "
           "small differences are expected.", cap))
S.append(P("Reading across the data", h2))
for t in ["• <b>The cut was concentrated in electricity</b>, which is regulated at EU level through the ETS and "
          "does not count towards Malta’s national 2030 target.",
          "• <b>The sectors closest to households rose</b>: cars, buildings and air-conditioning gases. The "
          "release’s phrase “reducing emissions both at household level” is not what the sector data "
          "show; a per-person ratio is not a measure of household emissions.",
          "• <b>Malta’s 2030 gap is the largest in the EU in percentage points</b>: 61 points with existing "
          "measures and 49 with planned measures. The next largest is Ireland (33 and 20) [4]. In tonnes, larger "
          "states’ gaps are bigger: Germany’s projected 2030 shortfall is 64 Mt CO<sub>2</sub>-eq, Malta’s "
          "0.5 Mt [4, pp. 118, 125]. The Commission names Germany, Ireland and Malta as having the largest "
          "projected gaps [5].",
          "• <b>International shipping and aviation bunkers</b>, which are outside both the national total and "
          "the target, tripled from 2.4 to 7.3 Mt, more than three times Malta’s national total. They are "
          "reported but not part of this claim."]:
    S.append(P(t, bul))

# ================================================================== 5
S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(5, "Where the evidence points different ways"))
S.append(P("Three questions decide how the per-person figure should be read. Each sets out the case for the "
           "authority’s framing beside the case against."))
S.append(contested(
    "Q1  Is per person a fair way to compare Malta with the EU?", "BOTH VALID, NOT INTERCHANGEABLE", AMBER,
    "Per-person emissions are a standard indicator, published by the Commission itself [4]. They allow small and "
    "large states to be compared and reflect equity arguments in climate policy.",
    "Malta’s binding EU obligation is expressed in total tonnes against 2005, not per person. With the "
    "second-fastest population growth in the EU, the per-person figure flatters Malta more than almost any other state.",
    "Per person and total answer different questions. <b>For this claim:</b> the release uses the per-person "
    "result as evidence that Malta’s efforts are “showing clear results” without saying that, in "
    "total tonnes, Malta cut less than the EU average."))
S.append(contested(
    "Q2  Do the results reflect policy, or one-off changes?", "MAINLY ONE STRUCTURAL CHANGE", AMBER,
    "The interconnector and the gas conversion were policy decisions, and they delivered a lasting 63% cut in "
    "power-sector emissions. Emissions per unit of GDP fell 82% [1, 4].",
    "Outside power generation, emissions grew. Effort-sharing sectors were 30% above 2005 already in 2021 and 41% "
    "above in 2024 [4]. Transport and car ownership growth on islands is a known structural problem [10, 11].",
    "<b>For this claim:</b> the headline result is real but comes from the sector that is not under the national "
    "target. The sectors that are under it have moved away from the target."))
S.append(contested(
    "Q3  Can the 2030 gap still be closed?", "UNCERTAIN; PROJECTIONS SAY NO", RED,
    "The CAA says Malta aims to cut emissions by 40% by 2030 [1]. The EU rules allow flexibilities (buying "
    "allocations from other states, ETS and land-use credits). Projections can be revised as measures are added.",
    "Even with planned measures the Commission projects +30% against −19% [4]. Malta’s cumulative "
    "allocation balance turns negative from 2025 and reaches −2.1 Mt by 2030 before flexibilities [4, p. 125]. "
    "Malta is among six states projected to have excess emissions in 2026–2030 [5].",
    "We did not test the 40% figure; it appears to refer to total emissions including power, while the binding "
    "target covers the sectors that are rising. <b>For this claim:</b> a reader of the release would not learn "
    "that the gap exists."))

# ================================================================== 6
S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(6, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> Emissions per capita have fallen 44% since 2005"), C("CAA [1]"),
     C("Reproduced from Eurostat (−46% to 2023, −48% to 2024). Commission source."), verd("ACCURATE", GREENC)],
    [C("<b>B.</b> …well above the EU average of 34%"), C("CAA [1]"),
     C("Reproduced (−34% to 2023). True per person; false in total tonnes (−27% vs −33%)."),
     verd("ACCURATE, PARTIAL", AMBER)],
    [C("<b>C.</b> Emissions per unit of GDP down 81.6% vs EU 61.9%"), C("CAA [1]"),
     C("Not recomputed (GDP series and price base not stated). Direction consistent with Commission data."),
     verd("NOT TESTED", GREY)],
    [C("<b>D.</b> Malta is reducing emissions at household level"), C("CAA [1]"),
     C("Sectors linked to households rose: transport +49%, buildings +9 to +12%, air-conditioning gases up "
       "almost six-fold. A per-person ratio is not a household measure."), verd("NOT SUPPORTED", RED)],
    [C("<b>E.</b> Malta’s efforts are showing clear results"), C("CAA [1]"),
     C("True for power generation. The same report projects the largest shortfall in the EU (in percentage "
       "points) against Malta’s "
       "binding 2030 target, which the release does not mention."), verd("MISLEADING BY OMISSION", colors.HexColor("#C85A3A"))],
    [C("<b>F.</b> Malta aims to reduce emissions by 40% by 2030"), C("CAA [1]"),
     C("A stated aim, not a result. Scope (total or effort-sharing) not given. Same figure appears in the 2026 "
       "Labour manifesto (see CC-011)."), verd("UNCLEAR SCOPE", GREY)],
], [42 * mm, 18 * mm, 76 * mm, 34 * mm], valign="MIDDLE"))
S += [Spacer(1, 4 * mm),
      callout([P("WHAT THE REPORT ITSELF SAYS ABOUT MALTA", tag),
               P("The CAA release cites the Commission’s November 2025 report as its source. In the staff working "
                 "document, Malta’s effort-sharing table (p. 114) shows +41% in 2024 and a projected 2030 gap of "
                 "61 points with existing measures and 49 with planned ones. The web chapter on effort sharing names "
                 "Malta among the three states with the largest projected gaps [5]. Choosing the per-person line from "
                 "that report, and leaving out the target line, is the pattern our methodology calls a "
                 "<i>selective metric</i>.", small)], bg=BLUE_PALE, bar=BLUE)]

# ================================================================== 7
S += [Spacer(1, 6 * mm), SectionHeading(7, "Verdict and requests for evidence"),
      verdict_box("Misleading", "Accurate figures, inaccurate overall impression. Confidence: high. Based on the "
                  "Commission’s own report and Eurostat data, both of which can be shown."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) The 44% and 34% figures are correct and reproducible. (2) About half of Malta’s "
           "per-person fall reflects population growth; in total tonnes Malta cut less than the EU average. "
           "(3) The cut came almost entirely from power generation, which is outside the national target, while "
           "transport, buildings and refrigerant gases rose. (4) The report the authority cites projects that Malta "
           "will miss its binding 2030 target by the widest margin in the EU in percentage points; the release omits "
           "this. Under our scale, "
           "a statement whose individual figures are defensible but which omits material facts so that the overall "
           "impression is inaccurate is <i>Misleading</i>."))
S.append(P("<b>What this verdict does not say.</b> It does not say the figures are false, that the power-sector "
           "transition was not an achievement, or that anyone acted in bad faith. A fuller statement would read: "
           "<i>“Emissions per person fell 44%, helped by strong population growth; total emissions fell 27%. "
           "Emissions in transport, buildings and other effort-sharing sectors are 41% above 2005, and the "
           "Commission projects we will miss our 2030 target unless we do more.”</i>"))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "The Climate Action Authority’s source for the 44% and 34% figures (table, year and emissions scope).",
    "The scope of the “40% by 2030” aim: total emissions, effort-sharing emissions, or another basis.",
    "The latest projection of effort-sharing emissions for 2030, and the measures and dates that close the gap to "
    "−19%.",
    "Whether Malta expects to use flexibilities (purchased allocations, ETS or land-use credits) to meet the "
    "target, and in what quantity.",
    "The June 2026 CAA emissions factsheet, which we could not access.",
]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag),
               P("Before wider circulation this draft should be sent to the Climate Action Authority and the Ministry "
                 "for the Environment, Energy and Public Cleanliness with a fixed deadline (suggested 14 days). "
                 "Under our standards a <i>Misleading</i> verdict is not published before that deadline passes. "
                 "Responses will be appended and the verdict revisited.", small)], bg=AMBER_PALE, bar=AMBER)]

# ================================================================== 8
S += [Spacer(1, 6 * mm), SectionHeading(8, "Limitations")]
for l in ["This is a statistical check. Peer-reviewed literature was searched (Crossref, OpenAlex) for Malta-specific "
          "decompositions of emissions; none was found, so the decomposition here is our own two-factor arithmetic.",
          "Eurostat’s 2026 inventory differs slightly from the 2025 inventory the Commission used; we reproduce "
          "the direction and size of the CAA’s figures, not the exact decimals.",
          "Projections are the Commission’s reading of Malta’s 2025 submissions; newer measures may change them.",
          "We read the transport papers [10, 11] as abstracts only; they are context, not evidence for the verdict.",
          "The CAA’s June 2026 factsheet could not be read. If it presents the 2030 gap, that would be relevant "
          "to how the authority communicates, though not to the November 2025 release assessed here."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Climate Action Authority (13 Nov 2025). Malta strengthens its contribution toward the EU’s climate "
          "goals. Press release. (Read from Wayback Machine copy of 15 Apr 2026.)",
     "https://climateaction.gov.mt/press/malta-strengthens-its-contribution-toward-the-eus-climate-goals/"),
    ("2", "Zammit J. (Nov 2025). Malta cuts emissions faster than EU average, report shows. <i>MaltaToday</i>.",
     "https://www.maltatoday.com.mt/news/national/138271/malta_cuts_emissions_faster_than_eu_average_report_shows"),
    ("3", "Italpress / MNA (17 Nov 2025). Malta set to increase emissions as EU cuts carbon output.",
     "https://www.italpress.com/?p=605399"),
    ("4", "European Commission (Nov 2025). Climate Action Progress Report 2025, Commission Staff Working Document. "
          "Pages cited (printed page numbers; the PDF page is one higher): 33, 44, 51–52, 59, 113–115, 118, 125.",
     "https://climate.ec.europa.eu/document/download/35f83a2d-f77d-4895-b616-d579069b23d3_en?filename=capr2025_swd_en.pdf"),
    ("5", "European Commission (2025). EU Climate Action Progress Report 2025, Chapter 3: Effort sharing emissions.",
     "https://climate.ec.europa.eu/eu-action/climate-strategies-targets/progress-climate-action/eu-climate-action-progress-report-2025/chapter-3-effort-sharing-emissions_en"),
    ("6", "Eurostat. Greenhouse gas emissions by source sector (env_air_gge), updated 2 Jun 2026, retrieved 2 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/env_air_gge/default/table"),
    ("7", "Eurostat. Population and employment (nama_10_pe), retrieved 2 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/nama_10_pe/default/table"),
    ("8", "Eurostat. Share of energy from renewable sources (nrg_ind_ren), retrieved 2 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/nrg_ind_ren/default/table"),
    ("9", "MiŻien. Calculation script and outputs: tools/cc-003-report/calc.py; data/cc-003/checks.csv.", ""),
    ("10", "Camilleri R., Attard M., Hickman R. (2024). Participatory policy packaging for transport backcasting: a "
           "pathway for reducing CO<sub>2</sub> emissions from transport in Malta. <i>Sustainability</i> 16(1):430. "
           "doi:10.3390/su16010430. (Abstract read.)", "https://doi.org/10.3390/su16010430"),
    ("11", "Warren J.P., Enoch M.P. (2010). Island transport, car ownership and use: a focus on practices in Cuba, "
           "Malta, Mauritius and Singapore. <i>Island Studies Journal</i> 5(2):193–216. doi:10.24043/isj.244. "
           "(Abstract read.)", "https://doi.org/10.24043/isj.244"),
    ("12", "Ehrlich P.R., Holdren J.P. (1971). Impact of population growth. <i>Science</i> 171(3977):1212–1217. "
           "doi:10.1126/science.171.3977.1212. (Cited for the identity only; not read.)", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "2 Oct 2026", "First issue. Draft pending right of reply from the Climate Action Authority "
                                         "and the Ministry for the Environment, Energy and Public Cleanliness."),
                   ("1.1", "5 Oct 2026",
                    "Corrections. (1) Section 4 table, EU 2030 effort-sharing projection: “−31% / …” → “−31% / −38%” "
                    "(existing / additional measures, Commission Table 25). (2) EU industrial emissions, 2005–2023: "
                    "“fell” → “−36%” (Commission p. 44). (3) “Widest margin in the EU” → “widest margin in the EU in "
                    "percentage points” (TL;DR, Sections 6 and 7, flyer); Section 4 adds that in tonnes Germany’s "
                    "projected 2030 shortfall (64 Mt) exceeds Malta’s (0.5 Mt). (4) Commission page numbers changed "
                    "from PDF to printed pages: p. 115 → pp. 114–115 (Figure 2 label → p. 114), p. 126 → 125, "
                    "p. 45 → 44, p. 52 → 51–52, p. 60 → 59. (5) Flyer title “Emissions down 44%” → “Emissions per "
                    "person down 44%”; the two “+41%” flyer cards retitled “Population growth since 2005” and "
                    "“Target-sector emissions, 2024”. (6) data/cc-003/checks.csv now also holds the EU-27 values shown "
                    "in the Section 4 table. Verdict and confidence unchanged.")])

build_report(Report(
    number="003", out=str(FIG / "report.pdf"), kicker="Statistics and EU reports",
    title_lines=["Down 44% per", "person, or off", "track for 2030?"],
    subtitle_lines=["Testing a public claim about Malta’s greenhouse-gas emissions", "against EU and Eurostat data"],
    quote_lines=["“Emissions per capita have fallen by 44% since", "2005, well above the EU average of 34%.”"], quote_size=15,
    attribution="Climate Action Authority, press release, 13 November 2025.",
    context="Citing the European Commission’s Climate Action Progress Report 2025.",
    verdict="Misleading", verdict_note="Accurate figures; the report’s main finding is left out",
    footer_lines=["Version 1.1  ·  5 October 2026", "Status: draft for right of reply (Climate Action Authority; "
                  "Ministry for the Environment)", "Prepared from public sources and Eurostat data.",
                  "Repository: github.com/leandergrech/Mizien"],
    running_head="Per-person emissions and the 2030 target – Malta", version="1.1", date="5 October 2026",
    pdf_title="Down 44% per person, or off track for 2030? Claim Check 003",
    pdf_subject="Tests the Climate Action Authority's per-capita emissions claim against the Commission's 2030 projection",
    story=S))
