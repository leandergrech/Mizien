"""Claim Check 063 report. Run fetch.py, calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("On 2 June 2021 the Malta Developers Association (MDA) warned that unless an “imminent and enduring” solution "
        "was found to the dumping of construction waste, development would come to an <b>“almost complete "
        "standstill”</b>. We checked the warning against Eurostat’s construction output and waste data.", lead)]
S.append(key_points([
    ("Disposal space was a real problem.",
     "Road works were halted in 2020 for lack of dumping space, government fixed a €12 a tonne gate fee, and in June "
     "2021 contractors said that fee strained their tenders (MaltaToday, BusinessToday)."),
    ("No standstill appears in the data.",
     "Malta’s construction output (volume) rose 5.8% in 2021 and 5.5% in 2022, to 162.5 (2015 = 100). It is the "
     "latest year Eurostat publishes for Malta."),
    ("But the warning was conditional, and the condition changed.",
     "Government announced a construction and demolition waste strategy of 15 measures in October 2021. We cannot "
     "say what would have happened with no solution, so the data neither confirm nor refute the warning."),
    ("Verdict: not substantiated (moderate confidence).",
     "The MDA published no analysis behind “almost complete standstill”, and none exists in the sources we could "
     "read. The concern is real; the degree is unshown."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(2), Spacer(1, 3 * mm),
      tiles([("+5.8%", GREEN, "Construction output volume, 2021 (+5.5% in 2022)"),
             ("2.1 Mt", AMBER, "Waste from construction, 2022 (3.0 Mt in 2020)"),
             ("78%", GREY, "Construction’s share of all waste generated in Malta, 2022"),
             ("€12/t", GREY, "Fixed fee for construction waste at Wied Incita since 2020")]),
      Spacer(1, 4 * mm),
      up_down("Evidence of what stalled after June 2021 because of disposal limits (stopped projects, tenders, "
              "quarry capacity), or the MDA’s own analysis behind its warning.",
              "Evidence that output kept growing through the period for reasons unrelated to disposal, or an MDA "
              "analysis that showed the warning was a forecast with a method."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the data show"),
          ("4", "Where the evidence points different ways"), ("5", "Testing the claim"),
          ("6", "Verdict and requests for evidence"), ("7", "Limitations")])
S.append(PageBreak())

S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("MaltaToday reported the Association’s statement on 2 June 2021 [1]. Only the words inside quotation marks "
           "are the Association’s own in that report: the “almost complete standstill” warning, its remark that "
           "there “has been a patchwork of attempted solutions along the years”, and its description of the situation "
           "as “untenable” (attributed to director-general Deborah Schembri). The conditional framing (“unless a "
           "solution is found”) is the outlet’s paraphrase of the statement. We could not reach the Association’s "
           "own text; the page was read from an Internet Archive copy, because the live site returns 403. BusinessToday "
           "(17 June 2021) repeats the warning and quotes MDA president Sandro Chetcuti on the cost of dumping [2]."))
S.append(std_table([
    [C("Source", cellh), C("What it says", cellh), C("Our access", cellh), C("Status", cellh)],
    [C("<b>MaltaToday</b>, 2 Jun 2021 [1]"),
     C("MDA warns “unless an imminent and enduring solution” is found, development will come to an “almost complete "
       "standstill”; “intense discussions” with government under way."), C("Read, Internet Archive copy."),
     C("<b>The claim</b> (outlet’s report of the statement)")],
    [C("<b>BusinessToday</b>, 17 Jun 2021 [2]"),
     C("Contractors’ tenders assumed €5–8 a tonne; quarry owners charge €12; MDA proposes land for recycling and "
       "exporting waste."), C("Read, Internet Archive copy."), C("Context")],
    [C("<b>MaltaToday</b>, 9 Oct 2021 [3]"),
     C("Environment Minister announces a construction and demolition waste strategy of 15 measures in four areas."),
     C("Read, Internet Archive copy."), C("Context")],
    [C("<b>Eurostat</b> [4–6]"), C("Construction output (volume); waste generated and treated, Malta."),
     C("Downloaded 5 Oct 2026."), C("<b>Primary data</b>")],
], [38 * mm, 74 * mm, 36 * mm, 22 * mm]))

S += [Spacer(1, 4 * mm), SectionHeading(2, "Method")]
S.append(P("<b>Question.</b> Is the warning that development would almost completely stop, absent a solution to "
           "construction-waste dumping, supported?"))
S.append(P("<b>Evidence.</b> We located the statement and its context, then downloaded three Eurostat series for Malta "
           "(<i>data/cc-063/</i>): production in construction (sts_copr_a, volume index), waste generated by the "
           "construction sector (env_wasgen) and treatment of mineral construction and demolition waste (env_wastrt). "
           "Calculations are in <i>tools/cc-063-report/calc.py</i> with outputs in <i>data/cc-063/checks.csv</i>."))
S.append(P("<b>Limits of the test.</b> A warning of the form “unless X, then Y” can only be tested directly if X "
           "did not happen. Here, government acted (a fee in 2020, a strategy in October 2021), so the data can show "
           "whether the feared outcome occurred, not whether it would have without action. <b>Grades:</b> Eurostat "
           "statistics are grade C; the MDA statement is an assertion (D). <b>Verdicts</b> follow Appendix A."))

S.append(CondPageBreak(85 * mm))
S.append(SectionHeading(3, "What the data show"))
S.append(fig(FIG / "fig1_output_waste.png", width=CW * 0.98))
S.append(P("Figure 1. Left: Malta’s construction output, volume index (2015 = 100). Right: waste from the construction "
           "sector, all waste, millions of tonnes (biennial).", cap))
S.append(P("Construction output rose from 145.5 in 2020 to 154.0 in 2021 (+5.8%) and 162.5 in 2022 (+5.5%, provisional), "
           "11.7% above 2020. Eurostat has no later year for Malta, so the data say nothing about 2023 onwards. Waste "
           "from the construction sector was 3.0 million tonnes in 2020 and 2.1 million in 2022 (−31%), but 4.7% "
           "above 2018. It is 78% of all waste generated in Malta in 2022 (84% in 2020). Of the mineral construction "
           "and demolition waste treated in 2022, 67% was recycled and 33% used for backfilling, with landfill "
           "negligible; Eurostat classes backfilling as recovery, so this does not show how much went to quarries "
           "for disposal."))

S.append(CondPageBreak(80 * mm))
S.append(SectionHeading(4, "Where the evidence points different ways"))
S.append(contested("Did the disposal bottleneck threaten to stop development?", "UNSETTLED", AMBER,
                   "In 2020 Infrastructure Malta ordered road works to stop for lack of dumping space and the high price "
                   "asked by the few quarries accepting waste; government then imposed a €12 a tonne fee [1]. In June "
                   "2021 contractors said road works had again largely halted over costs [2]. Construction waste has "
                   "grown with the pace of development [3].",
                   "Output kept growing in 2021 and 2022. The Environment Minister said in 2020 that there was ample "
                   "quarry space, but not all quarries accepted debris [1]. A strategy followed in October 2021 [3]. "
                   "We found no published data on the number of stalled projects.",
                   "A real bottleneck existed and affected road works. An “almost complete standstill” of "
                   "development is a far stronger statement; it has no published analysis and did not show in "
                   "national output through 2022.",
                   label_a="FOR", label_b="AGAINST"))

S.append(CondPageBreak(70 * mm))
S.append(SectionHeading(5, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> Dumping of construction waste had no enduring solution in June 2021"), C("MDA [1]"),
     C("Road works halted in 2020 and strain reported again in 2021; the MDA calls past fixes a “patchwork”."),
     verd("SUPPORTED", GREENC)],
    [C("<b>B.</b> Without one, development would come to an almost complete standstill"), C("MDA [1]"),
     C("No analysis published. Output grew 5.8% (2021) and 5.5% (2022), but government acted, so the "
       "counterfactual is untestable."),
     verd("NOT SUBSTANTIATED", AMBER)],
], [42 * mm, 18 * mm, 76 * mm, 34 * mm], valign="MIDDLE"))

S += [Spacer(1, 6 * mm), SectionHeading(6, "Verdict and requests for evidence"),
      verdict_box("Not substantiated", "The disposal problem was real, but “almost complete standstill” has no "
                  "published basis and did not appear in national output. Confidence: moderate."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> Our scale rates a claim <i>Not substantiated</i> when it is stated more strongly than the evidence "
           "available allows. The shortage of disposal capacity is documented; the degree of harm forecast is not. "
           "Confidence is moderate because output data stop at 2022 and say little about specific projects."))
S.append(P("<b>What this verdict does not say.</b> It does not say the developers were wrong to raise the problem, or "
           "that nothing stalled: road works did. It treats a negotiating warning as the kind of statement it is, "
           "and asks what evidence backs its strength. A fuller sentence would read: <i>“Without more disposal "
           "capacity, construction, and road works in particular, faces delays and higher costs.”</i>"))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "From the MDA: the analysis or member survey behind “almost complete standstill”.",
    "From ERA and the Planning Authority: quarry intake and remaining capacity by year since 2020.",
    "From Infrastructure Malta: projects suspended for lack of dumping space in 2020–21.",
]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag),
               P("Pending. Under the maintainer’s rule of 5 October 2026 a reply is sought for <i>Not substantiated</i> "
                 "verdicts. The maintainer will contact the MDA; this report will be updated with any response.", small)],
              bg=AMBER_PALE, bar=AMBER)]
S += [Spacer(1, 6 * mm), SectionHeading(7, "Limitations")]
for l in ["We did not reach the MDA’s own statement; wording is from MaltaToday’s report, read from an Internet Archive copy.",
          "Eurostat output data end in 2022 (provisional) and waste data in 2022; later years are untested.",
          "Eurostat’s waste data count backfilling as recovery, so they do not separate quarry disposal from recycling.",
          "National output could hide local stoppages; we have no project-level data."]:
    S.append(P("• " + l, bul))
S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Calleja, L. (2 Jun 2021). Developers again call for enduring solution to dumping of construction waste. MaltaToday.",
     "https://www.maltatoday.com.mt/news/national/110023/developers_again_call_for_enduring_solution_to_dumping_of_construction_waste"),
    ("2", "Cocks, P. (17 Jun 2021). Crippling construction waste dumping costs behind road works standstill, MDA says. BusinessToday.",
     "https://www.businesstoday.com.mt/business/business/1503/crippling_construction_waste_dumping_costs_behind_road_works_standstill_mda_says"),
    ("3", "Vella, L. (9 Oct 2021). Construction drive produced unprecedented levels of construction waste, Farrugia says. MaltaToday.",
     "https://www.maltatoday.com.mt/news/national/112566/construction_drive_produced_unprecedented_levels_of_construction_waste_farrugia_says"),
    ("4", "Eurostat. Production in construction, annual data (sts_copr_a), updated 2 Oct 2026, retrieved 5 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/sts_copr_a/default/table"),
    ("5", "Eurostat. Generation of waste by waste category, hazardousness and NACE Rev. 2 activity (env_wasgen), updated Sep 2025.",
     "https://ec.europa.eu/eurostat/databrowser/view/env_wasgen/default/table"),
    ("6", "Eurostat. Treatment of waste by waste category, hazardousness and waste management operations (env_wastrt), updated Sep 2025.",
     "https://ec.europa.eu/eurostat/databrowser/view/env_wastrt/default/table"),
    ("7", "MiŻien. Calculation script and outputs: tools/cc-063-report/calc.py; data/cc-063/.", ""),
])
S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "5 Oct 2026", "First issue. Verdict Not substantiated (moderate confidence); pending right of reply.")])

build_report(Report(
    number="063", out=str(FIG / "report.pdf"), kicker="Waste and construction",
    title_lines=["Development at an", "“almost complete", "standstill”?"],
    subtitle_lines=["Testing the Malta Developers Association’s 2021 warning", "about construction-waste dumping"],
    quote_lines=["“…development will come to an", "‘almost complete standstill.’”"], quote_size=14,
    attribution="Malta Developers Association, statement of 2 June 2021, as reported by MaltaToday.",
    context="The conditional framing is the outlet’s; only the words in quotation marks are the Association’s.",
    verdict="Not substantiated", verdict_note="Real bottleneck; the scale of the warning is unshown",
    footer_lines=["Version 1.0  ·  5 October 2026", "Status: draft, pending right of reply",
                  "Prepared from public sources and Eurostat data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Construction waste – MDA standstill warning 2021", version="1.0", date="5 October 2026",
    status_note="pending right of reply",
    pdf_title="Development at an almost complete standstill? Claim Check 063",
    pdf_subject="Tests the MDA's 2021 warning about construction-waste dumping",
    story=S))
