"""Claim Check 019 report. Run fetch_data.py, calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []
LG = colors.HexColor("#8DB36B")

# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("In September 2026 Amphora Media, an investigative newsroom, reported that <b>“nearly 830,000 square metres of "
        "nature and cropland have been built up in Malta between 2018 and 2023”</b>, and that in “nearly 95% of the "
        "take-up, farmland rather than natural area was affected”. The press is held to the same standard as everyone "
        "else here. We checked the arithmetic and repeated the measurement with a different satellite land-cover "
        "product.", lead)]
S.append(key_points([
    ("The arithmetic holds.",
     "830,000 m² is 0.26% of Malta’s land, 116 football pitches and about 0.3 of Comino, as stated. Adding the EEA "
     "figures quoted gives the “at least 1.94 km²” since 2006."),
    ("An independent measurement finds more, not less.",
     "Using Impact Observatory’s 10 m land-cover maps and counting only land that changed consistently, about 1.4 km² "
     "net became built up between 2018 and 2023. Amphora’s figure is lower, consistent with its own description as "
     "“a conservative estimate”."),
    ("The 95% farmland share was not reproduced.",
     "In the independent data, 65% of the new built-up land was cropland and 31% shrub or grassland. Abandoned fields "
     "can fall in either class, and Amphora does not say how it measured the 95% or for which period."),
    ("Some parts could not be checked.",
     "The EEA figures are quoted second-hand, Amphora’s map polygons were not downloaded, and the “top 5 in Europe” "
     "ranking rests on the wider Green to Grey network’s data."),
    ("Verdict: largely supported (moderate confidence).",
     "The headline figure stands up and is, if anything, low. The farmland share is not shown, and the headline’s "
     "“over” 830,000 sits oddly with the text’s “nearly”."),
]))
S += [Spacer(1, 4 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("0.83", ORANGE, "km² built up 2018–2023, Amphora (Dynamic World, checked by hand)"),
             ("1.41", GREEN, "km² net, independent estimate (IO land cover, 3-year rule)"),
             ("65%", AMBER, "of new built-up land was cropland (IO); Amphora: nearly 95%"),
             ("0.26%", GREY, "of Malta’s land, as stated")]),
      Spacer(1, 4 * mm),
      up_down("Amphora’s polygons and the basis of the 95% share, or the EEA land-take table for Malta.",
              "Evidence that many flagged areas were already built before 2018 or are not built up."),
      Spacer(1, 5 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "How the satellite data work"),
          ("4", "What the data show"), ("5", "Where the evidence points different ways"),
          ("6", "Testing the claim"), ("7", "Verdict and requests for evidence"), ("8", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("Amphora Media published the investigation on 11 September 2026 [1] with a companion piece on agricultural "
           "land the next day [2], in collaboration with Arena for Journalism in Europe and supported by The Malta "
           "Environment Foundation. We read both in full."))
S.append(std_table([
    [C("What was said", cellh), C("Where", cellh), C("Access", cellh)],
    [C("“nearly 830,000 square metres of nature and cropland have been built up in Malta between 2018 and 2023” "
       "(headline: “over 830,000”)"), C("Amphora [1]"), C("Read in full")],
    [C("Total land loss 0.26%, “among the top 5 countries”; “a conservative estimate”"), C("Amphora [1]"),
     C("Read in full")],
    [C("EEA: 920,000 m² (2012–2018) and 190,000 m² (2006–2012); “at least 1.94 square kilometres” since 2006"),
     C("Amphora [1] ◆"), C("EEA data not seen")],
    [C("“in nearly 95% of the take-up, farmland rather than natural area was affected”"), C("Amphora [2]"),
     C("Read in full")],
], [104 * mm, 34 * mm, 32 * mm]))

# ================================================================== 2
S.append(Spacer(1, 4 * mm))
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Questions.</b> Is the 830,000 m² figure plausible, are the comparisons right, and was the land mostly "
           "farmland?"))
S.append(P("<b>Evidence.</b> Amphora’s method [1] uses Google and WRI’s Dynamic World [3]. For an independent "
           "estimate we used a different model, Impact Observatory and Esri’s 10 m annual land cover for 2017–2023 [4, 5], "
           "through Microsoft Planetary Computer. Island areas are from OpenStreetMap. Scripts and data: "
           "<i>tools/cc-019-report/</i> and <i>data/cc-019/</i>."))
S.append(P("<b>Grades.</b> Satellite land cover is a direct, model-classified measurement (grade B). ◆ marks a source "
           "known second-hand."))

# ================================================================== 3
S.append(CondPageBreak(70 * mm))
S.append(SectionHeading(3, "How the satellite data work"))
S.append(P("Both products classify every 10 m pixel with a deep-learning model trained on Sentinel-2 imagery [3, 4]. "
           "Single-year maps are noisy: in the Impact Observatory data Malta’s built-up area swings by more than 15 km² "
           "from one year to the next, twenty times the change being measured. A simple 2018-versus-2023 comparison "
           "would give 24 km², which is not credible. We therefore counted only pixels that were not built up in each "
           "of 2017, 2018 and 2019 and built up in each of 2021, 2022 and 2023, and subtracted the reverse change as a "
           "gauge of noise. Amphora handled the same problem by checking each flagged area by eye, which removes false "
           "alarms but can miss developments, as it notes."))

# ================================================================== 4
S.append(CondPageBreak(150 * mm))
S.append(SectionHeading(4, "What the data show"))
S.append(fig(FIG / "fig1_map.png", width=CW * 0.92))
S.append(P("Figure 1. Land that became consistently built up between 2017–19 and 2021–23 in the Impact Observatory "
           "data. The changes are small and scattered, as Amphora describes.", cap))
S.append(fig(FIG / "fig2_estimates.png"))
S.append(P("Figure 2. Left: Amphora’s figure against two independent estimates. Right: what the newly built land "
           "was before.", cap))
S.append(std_table([
    [C("Check", cellh), C("Result", cellh), C("Amphora", cellh), C("Grade", cellh)],
    [C("830,000 m² as a share of Malta’s land (314 km²)"), C("0.264%"), C("0.26%"), grade_tag("C")],
    [C("In FIFA pitches; vs Comino; vs Manoel Island"), C("116; 0.30; 2.7"), C("116; a quarter; two"), grade_tag("C")],
    [C("EEA 2006–12 + 2012–18 + Amphora 2018–23"), C("1.94 km²"), C("at least 1.94 km²"), grade_tag("C")],
    [C("New built-up 2018–23, IO, 3-year rule (net)"), C("<b>1.41 km²</b> (gross 1.91)"), C("0.83 km²"), grade_tag("B")],
    [C("New built-up 2018–23, IO, 2-year rule (net)"), C("2.96 km² (gross 4.98)"), C("–"), grade_tag("B")],
    [C("Previously cropland / shrub and grass / bare"), C("65% / 31% / 4%"), C("nearly 95% farmland"), grade_tag("B")],
], [70 * mm, 40 * mm, 46 * mm, 14 * mm]))
S.append(P("All values in <i>data/cc-019/checks.csv</i>.", cap))

# ================================================================== 5
S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(5, "Where the evidence points different ways"))
S.append(contested(
    "Q1  Is 830,000 m² right?", "PLAUSIBLE, PROBABLY LOW", GREENC,
    "An independent model finds 1.4 to 3.0 km² net under strict rules: more than Amphora’s figure, which it calls "
    "conservative.",
    "The independent estimates include classification noise that Amphora removed by hand; the true figure could be "
    "nearer Amphora’s.",
    "<b>For this claim:</b> the scale is right, and the figure is unlikely to be an overstatement."))
S.append(contested(
    "Q2  Was 95% of it farmland?", "NOT SHOWN", AMBER,
    "Two thirds of the new built-up land was cropland in the independent data, and much Maltese shrubland is "
    "abandoned farmland.",
    "A third was classed as shrub or grassland, which includes semi-natural garrigue. Amphora gives no basis or period "
    "for the 95%.",
    "<b>For this claim:</b> “mostly farmland” is supported; “nearly 95%” is not reproduced."))
S.append(contested(
    "Q3  Over or nearly 830,000?", "INCONSISTENT WORDING", GREY,
    "The text says “nearly”, the headline “over”.",
    "A headline should not round up a figure the text rounds down.",
    "<b>For this claim:</b> a minor point that does not change the finding."))

# ================================================================== 6
S.append(CondPageBreak(100 * mm))
S.append(SectionHeading(6, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> About 830,000 m² of green land built up 2018–2023"),
     C("Independent estimate 1.4–3.0 km² net; Amphora’s figure plausible and conservative."), verd("SUPPORTED", GREENC)],
    [C("<b>B.</b> 0.26% of land; comparisons (pitches, Comino, Manoel)"), C("Arithmetic checks out (Manoel: 2.7, "
       "not two)."), verd("SUPPORTED", GREENC)],
    [C("<b>C.</b> Nearly 95% of take-up was farmland"), C("Independent data: 65% cropland, 31% shrub or grass."),
     verd("NOT SHOWN", GREY)],
    [C("<b>D.</b> EEA figures and the 1.94 km² total"), C("Sum correct; EEA values not seen."), verd("NOT CHECKED", GREY)],
], [52 * mm, 88 * mm, 30 * mm], valign="MIDDLE"))

# ================================================================== 7
S += [Spacer(1, 6 * mm), SectionHeading(7, "Verdict and requests for evidence"),
      verdict_box("Largely supported", "The headline figure stands up and is probably low; the 95% farmland share is "
                  "not shown. Confidence: moderate."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) The figure is consistent with an independent satellite estimate, which finds as much or "
           "more. (2) The arithmetic and comparisons are right. (3) The farmland share and the EEA figures could not be "
           "verified, and the headline rounds up a number the text rounds down. These are caveats on details, not on "
           "the substance."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "Amphora’s polygons (the map layer) and the basis and period of the 95% farmland figure.",
    "The EEA land-take values for Malta, 2006–2012 and 2012–2018.",
]))

# ================================================================== 8
S += [Spacer(1, 6 * mm), SectionHeading(8, "Limitations")]
for l in ["Land-cover models misclassify pixels; our rules reduce but do not remove this.",
          "Built-up land includes roads, car parks and quarries as well as buildings; so does Amphora’s.",
          "Neither estimate says whether development was inside or outside the development zone.",
          "Class names differ between the two models; ‘rangeland’ in IO is not the same as ‘natural’."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Amphora Media (11 Sep 2026). Green To Grey: Malta lost over 830,000 square metres of land to development in "
          "five years.", "https://www.amphora.media/2026/09/green-to-grey-malta-land-loss-development-construction"),
    ("2", "Amphora Media (12 Sep 2026). Green to Grey: when development creeps up on agricultural land.",
     "https://www.amphora.media/2026/09/green-to-grey-development-agricutlural-land"),
    ("3", "Brown C.F. et al. (2022). Dynamic World, near real-time global 10 m land use land cover mapping. "
          "<i>Scientific Data</i> 9:251. doi:10.1038/s41597-022-01307-4.", "https://doi.org/10.1038/s41597-022-01307-4"),
    ("4", "Karra K. et al. (2021). Global land use / land cover with Sentinel 2 and deep learning. <i>IGARSS 2021</i>, "
          "4704–4707. doi:10.1109/IGARSS47720.2021.9553499.", "https://doi.org/10.1109/IGARSS47720.2021.9553499"),
    ("5", "Impact Observatory and Esri. 10 m Annual Land Use Land Cover (9-class) V2, 2017–2023; Microsoft Planetary "
          "Computer; retrieved 4 Oct 2026.", "https://planetarycomputer.microsoft.com/dataset/io-lulc-annual-v02"),
    ("6", "MiŻien. Data and calculations: data/cc-019/; tools/cc-019-report/.", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient, or direct measurement · C review, "
                "guidance or official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "4 Oct 2026", "First issue. Right of reply to Amphora Media not yet sent.")])

build_report(Report(
    number="019", out=str(FIG / "report.pdf"), kicker="Land and trees",
    title_lines=["830,000 m² of", "green land", "built over?"],
    subtitle_lines=["Testing a newsroom’s satellite estimate of land lost to development in Malta",
                    "against an independent land-cover model"],
    quote_lines=["“Nearly 830,000 square metres of nature", "and cropland have been built up in Malta",
                 "between 2018 and 2023.”"], quote_size=15,
    attribution="Amphora Media, Green to Grey, 11 September 2026.",
    context="Companion piece: nearly 95% of the take-up was farmland.",
    verdict="Largely supported", verdict_note="Figure stands up, probably low; the 95% farmland share is not shown",
    footer_lines=["Version 1.0  ·  4 October 2026", "Status: draft (right of reply: Amphora Media)",
                  "Prepared from public sources and satellite land cover.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Green to grey – Malta", version="1.0", date="4 October 2026",
    pdf_title="830,000 m2 of green land built over? Claim Check 019",
    pdf_subject="Tests Amphora Media's estimate of green land built up in Malta, 2018-2023",
    story=S))
