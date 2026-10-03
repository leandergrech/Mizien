"""Claim Check 012 report. Run fetch_s2.py, calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []
LG = colors.HexColor("#8DB36B")
CON = colors.HexColor("#8E2F25")

# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("In June 2025 the picnic area at Ta’ Qali National Park was covered in imported sand and gravel. The Public "
        "Works Ministry said the material would keep the soil moist so that <b>“the natural grass grows at a much "
        "faster rate well before the rainfall of the winter season”</b>. In January 2026 the Prime Minister said the "
        "area would be dealt with <b>“after the concerts are done”</b>. Momentum and the Nationalist Party said the "
        "gravel was choking the grass and could leave the area permanently barren. We tested what can be tested "
        "with three and a half years of Sentinel-2 satellite images.", lead)]
S.append(key_points([
    ("The grass did not come back.",
     "Before the gravel, the picnic area greened every winter as much as the rest of the park (winter NDVI 0.37–0.47). In "
     "winter 2025–26 it stayed brown (0.11) while the rest of the park greened as usual."),
    ("The summer dust problem was real.",
     "In summer the area was already bare before the gravel (NDVI about 0.11 in 2023 and 2024), as the park "
     "management said. The gravel solved a summer problem by removing the winter grass."),
    ("No intervention is visible yet.",
     "Summer Daze took place in August 2026. In the last clear image (27 September 2026) the gravel is still in "
     "place and the area is still bare."),
    ("“Permanently barren” cannot be tested.",
     "Satellite greenness shows what grows, not the state of the soil. Whether the damage is permanent depends on "
     "whether the gravel is removed and the soil treated."),
    ("Verdict: contradicted.",
     "The assurance that grass would regrow through the material is contradicted by the satellite record. The "
     "opposition’s description of the present state is supported; its “permanent” warning is not shown."),
]))
S += [Spacer(1, 4 * mm), VerdictMeter(4), Spacer(1, 3 * mm),
      tiles([("2.8 ha", GREEN, "Gravel zone found in the images (Momentum: about 2.2 ha)"),
             ("0.37–0.47", SAGE, "Winter greenness before the gravel (NDVI, 2023–2025)"),
             ("0.11", RED, "Winter greenness after the gravel (2025–26)"),
             ("27 Sep", GREY, "Last clear image: gravel still in place, 2026")]),
      Spacer(1, 4 * mm),
      up_down("Ground evidence that grass grew under or through the gravel in winter 2025–26 but is invisible to "
              "10 m satellite pixels; or works after 27 September 2026 that restore the grass.",
              "Soil tests showing the original soil can no longer support grass even after the gravel is removed."),
      Spacer(1, 5 * mm)]
S += toc([("1", "The claims and what we could verify"), ("2", "Method"), ("3", "What the science says"),
          ("4", "What the satellite record shows"), ("5", "Where the evidence points different ways"),
          ("6", "Testing the claims"), ("7", "Verdict and requests for evidence"), ("8", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claims and what we could verify"))
S.append(P("Both sides made checkable statements. We quote each from the fullest text we could read; no primary "
           "government press release or broadcast recording was found, so the government wording is as relayed by "
           "news outlets that quote it."))
S.append(std_table([
    [C("Claim", cellh), C("Speaker, date", cellh), C("Our access", cellh)],
    [C("The material retains moisture, so “the natural grass grows at a much faster rate well before the rainfall "
       "of the winter season”."), C("Public Works Ministry, Sept 2025 [1]"), C("Statement as relayed by MaltaToday")],
    [C("The gravel would curb summer dust while letting the grass grow back with the winter rains."),
     C("Jason Micallef, park unit head, Sept 2025 [2, 3]"), C("Paraphrase relayed by two outlets")],
    [C("“We will not be making this intervention now, as from April, the area will be hosting concerts … after the "
       "concerts are done, the intervention will happen.”"), C("Prime Minister, Jan 2026 [4]"),
     C("Verbatim, relayed by The Shift")],
    [C("The gravel is “choking the grass” and could “permanently transform” the area into a barren zone."),
     C("Partit Nazzjonalista, Feb 2026 [5]"), C("Statement as reported")],
    [C("Compacted gravel under sand prevents germination; the soil is “unsuitable for natural vegetation”."),
     C("Momentum, expert inspection, Feb 2026 [6]"), C("Reported; report not seen")],
], [80 * mm, 48 * mm, 42 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("SCOPE NOTE", tag),
               P("Momentum also said the works were “deliberately designed” to suppress grass, and both opposition "
                 "parties raised procurement and permit questions. Those are claims about intent and process, which "
                 "satellite data cannot test; we do not assess them.", small)], bg=AMBER_PALE, bar=AMBER),
      Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Where.</b> OpenStreetMap does not map the picnic area itself, so we located it from the images. Inside "
           "the mapped park polygon east of the National Stadium, we selected the pixels whose surface brightened most "
           "between late summer 2024 and late summer 2025 (above the 95th percentile of brightening outside the park), "
           "when the gravel was laid. This gives a 2.8 ha zone; Momentum’s inspection independently measured about "
           "2.2 ha. Choosing the zone by <i>brightness</i> rather than greenness keeps the greenness test independent."))
S.append(P("<b>What.</b> NDVI, a standard index of green vegetation from red and near-infrared reflectance, from every "
           "Sentinel-2 scene with less than 10% cloud from January 2023 to September 2026, using clear pixels only. The "
           "rest of the park polygon (excluding a 20 m buffer) is the control: same soil, same rain. Scripts: "
           "<i>tools/cc-012-report/fetch_s2.py</i> and <i>calc.py</i>; data in <i>data/cc-012/</i>."))
S.append(P("<b>Grades.</b> Direct satellite measurement against a control area is grade B; soil-science reviews are "
           "grade C. <b>Verdicts</b> follow the five-point scale in Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(80 * mm))
S.append(SectionHeading(3, "What the science says"))
S.append(P("Soil compaction from traffic and trampling, including amenity use, is a well-documented form of soil "
           "degradation: it limits water and air infiltration and root penetration [8, 9]. Controlled experiments find "
           "that seedling emergence falls as compaction increases [10]. That fits the arborist Jonathan Henwood’s "
           "diagnosis that years of mass events had already compacted the picnic area [1], and Momentum’s finding of a "
           "compacted gravel layer [6]."))
S.append(P("The Ministry’s rationale also has a basis: gravel–sand mulch is an established technique for conserving "
           "soil water in dry regions [11]. But conserving water under a surface layer is not the same as letting grass "
           "grow through it. Whether it does is an empirical question, which the satellite record can answer."))

# ================================================================== 4
S.append(PageBreak())
S.append(SectionHeading(4, "What the satellite record shows"))
S.append(fig(FIG / "fig1_map.png"))
S.append(P("Figure 1. The picnic area in February 2025 (green) and February 2026 (bare), with the gravel zone in amber.",
           cap))
S.append(fig(FIG / "fig2_timeseries.png"))
S.append(P("Figure 2. Greenness of the gravel zone and of the rest of the park, January 2023 to September 2026. Before "
           "June 2025 the zone greened every winter like the rest of the park; after it, it did not.", cap))
S.append(P("Reading across the data", h2))
for t in ["• <b>Two normal winters, then none.</b> Winter medians in the zone were 0.37, 0.47 and 0.38 in "
          "2023–2025, level with the rest of the park (0.39–0.40). In winter 2025–26 the median was 0.11 while the "
          "rest of the park was at 0.38.",
          "• <b>No early start either.</b> The Ministry said grass would grow “well before the rainfall”. In autumn "
          "and early winter 2025 the zone was browner than in the same months of 2023, before the gravel.",
          "• <b>The summer problem was real.</b> In July–August 2023 and 2024 the zone was already bare (about 0.11), "
          "browner than the rest of the park, consistent with a compacted events ground that turned to dust.",
          "• <b>No change after the concerts so far.</b> The surface has stayed bright since June 2025 and was still bare "
          "in the last clear images (5, 8, 10 and 27 September 2026)."]:
    S.append(P(t, bul))

# ================================================================== 5
S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(5, "Where the evidence points different ways"))
S.append(contested(
    "Q1  Was the area already in poor condition?", "YES, IN SUMMER", AMBER,
    "Summer NDVI was already very low in 2023 and 2024 and the park management’s dust complaint is borne out. Mass "
    "events had compacted the soil, as the arborist said [1].",
    "In winter the same ground greened normally until 2025. The gravel removed the winter grass without restoring the "
    "summer cover.",
    "<b>For the claims:</b> the gravel addressed summer dust, but at the cost of the grass the area had in winter."))
S.append(contested(
    "Q2  Could grass be growing that the satellite cannot see?", "UNLIKELY AT THIS SCALE", AMBER,
    "Ten-metre pixels average over small patches; a local mayor reported isolated Bermuda grass where no gravel was "
    "laid [3].",
    "Across 2.8 ha the zone was as green as the rest of the park in two winters and far below it in the third; a "
    "change of that size would show if grass had returned.",
    "<b>For the claims:</b> small patches are possible; a recovered lawn is not."))
S.append(contested(
    "Q3  Is the damage permanent?", "NOT SHOWN", GREY,
    "Momentum’s inspection describes a compacted layer that seeds in the soil cannot penetrate [6]; compaction "
    "is slow to reverse [8, 9].",
    "Compaction can be alleviated by removing the surface layer and loosening the soil [9]; the government says an "
    "expert is advising on restoration [4].",
    "<b>For the claims:</b> “permanently” is a prediction, and depends on what is done next."))

# ================================================================== 6
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(6, "Testing the claims"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Claim", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> Grass would grow faster, before the winter rains (Ministry)"),
     C("Zone stayed bare through winter 2025–26 (median NDVI 0.11) while the rest of the park greened."), verd("CONTRADICTED", CON)],
    [C("<b>B.</b> Grass would grow back with the winter rains (park unit head)"), C("As above."), verd("CONTRADICTED", CON)],
    [C("<b>C.</b> Intervention after the concerts (Prime Minister)"),
     C("No change visible to 27 Sep 2026, after Summer Daze. Not yet due if “after” means autumn."), verd("NOT YET DELIVERED", GREY)],
    [C("<b>D.</b> Gravel is choking the grass (PN, Momentum)"), C("Consistent with the satellite record."),
     verd("SUPPORTED", GREENC)],
    [C("<b>E.</b> Could become permanently barren (PN)"), C("A prediction; soil condition not measurable from space."),
     verd("NOT SUBSTANTIATED", ORANGE)],
], [52 * mm, 88 * mm, 30 * mm], valign="MIDDLE"))

# ================================================================== 7
S += [Spacer(1, 6 * mm), SectionHeading(7, "Verdict and requests for evidence"),
      verdict_box("Contradicted", "The assurance that grass would regrow through the material is contradicted by "
                  "Sentinel-2 data against a control area. Confidence: high."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> The zone greened normally in the two winters before the gravel and did not green in the winter "
           "after it, while the surrounding park did. The Ministry’s claim that grass would grow faster, and the park "
           "unit’s that it would return with the rains, are therefore contradicted. The opposition’s description of "
           "the current state is supported; its warning of permanent damage is not shown either way."))
S.append(P("<b>What this verdict does not say.</b> It does not say why the gravel was chosen, whether procurement rules "
           "were followed, or that the area cannot be restored."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "The landscaping consultant’s report and the restoration plan, with dates.",
    "The specification of the material laid and the advice on which it was chosen.",
    "Momentum’s inspection report in full, including sampling locations.",
    "The 2026 events calendar for the picnic area.",
]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag),
               P("Before wider circulation this draft should go to the Public Works / Infrastructure Ministry, the Ta’ "
                 "Qali National Park unit, the Office of the Prime Minister, the Partit Nazzjonalista and Momentum, "
                 "with a fixed deadline. A <i>Contradicted</i> verdict is not published before that deadline passes.",
                 small)], bg=AMBER_PALE, bar=AMBER)]

# ================================================================== 8
S += [Spacer(1, 6 * mm), SectionHeading(8, "Limitations")]
for l in ["NDVI measures green vegetation, not soil health; it cannot show whether the soil is “sterilised”.",
          "Sentinel-2 pixels are 10 m; patches smaller than a pixel are invisible.",
          "The zone was located from the images because the picnic area is not mapped; its edges are approximate.",
          "Government wording is relayed by news outlets; no primary statement or broadcast recording was found.",
          "Works after 27 September 2026 are not covered."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "MaltaToday (Sept 2025). Use of gravel at Ta’ Qali ‘sterilises’ soil, expert says (updated with Public Works "
          "Ministry statement).",
     "https://www.maltatoday.com.mt/news/national/136863/use_of_gravel_at_ta_qali_sterilises_soil_expert_says_"),
    ("2", "The Malta Independent (5 Feb 2026). Momentum inspection on Ta’ Qali gravel shows soil rendered unsuitable "
          "for natural vegetation. (Also reports Micallef’s earlier assurance.)",
     "https://www.independent.com.mt/articles/2026-02-05/local-news/Momentum-inspection-on-Ta-Qali-gravel-shows-soil-rendered-unsuitable-for-natural-vegetation-6736286987"),
    ("3", "MaltaToday (Nov 2025). Ta’ Qali gravel under scrutiny again.",
     "https://www.maltatoday.com.mt/environment/nature/137956/ta_qali_gravel_under_scrutiny_again_"),
    ("4", "The Shift News (15 Jan 2026). PM contradicted over Ta’ Qali concerts and green grass.",
     "https://theshiftnews.com/2026/01/15/pm-contradicted-over-ta-qali-concerts-and-green-grass/"),
    ("5", "The Malta Independent (6 Feb 2026). Gravel used to cover Ta’ Qali suppressing grass growth, PN says.",
     "https://www.independent.com.mt/articles/2026-02-06/local-news/Gravel-used-to-cover-Ta-Qali-suppressing-grass-growth-PN-says-6736287029"),
    ("6", "Momentum expert inspection, as reported in [2] ◆. Report not seen.", ""),
    ("7", "Copernicus Sentinel-2 L2A, tile 33SVV, 2023–2026, via Microsoft Planetary Computer; retrieved 3 Oct 2026.",
     "https://planetarycomputer.microsoft.com/dataset/sentinel-2-l2a"),
    ("8", "Nawaz M.F., Bourrié G., Trolard F. (2013). Soil compaction impact and modelling. A review. <i>Agronomy for "
          "Sustainable Development</i> 33(2):291–309. doi:10.1007/s13593-011-0071-8. (Abstract read.)",
     "https://doi.org/10.1007/s13593-011-0071-8"),
    ("9", "Batey T. (2009). Soil compaction and soil management – a review. <i>Soil Use and Management</i> 25(4):335–345. "
          "doi:10.1111/j.1475-2743.2009.00236.x. (Abstract read.)", "https://doi.org/10.1111/j.1475-2743.2009.00236.x"),
    ("10", "Hyatt J., Wendroth O., Egli D.B. (2007). Soil compaction and soybean seedling emergence. <i>Crop Science</i> "
           "47(6):2495–2503. doi:10.2135/cropsci2007.03.0171. (Abstract read.)", "https://doi.org/10.2135/cropsci2007.03.0171"),
    ("11", "Li X.-Y. (2003). Gravel–sand mulch for soil and water conservation in the semiarid loess region of northwest "
           "China. <i>Catena</i> 52(2):105–127. doi:10.1016/S0341-8162(02)00181-9. (Metadata only.)",
     "https://doi.org/10.1016/S0341-8162(02)00181-9"),
    ("12", "MiŻien. Data and scripts: data/cc-012/; tools/cc-012-report/.", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "3 Oct 2026", "First issue. Draft pending right of reply.")])

build_report(Report(
    number="012", out=str(FIG / "report.pdf"), kicker="Parks and open space",
    title_lines=["Will the grass", "come back at", "Ta’ Qali?"],
    subtitle_lines=["Testing claims by the government and the opposition",
                    "against three and a half years of satellite images"],
    quote_lines=["“The natural grass grows at a much faster", "rate well before the rainfall of the winter season.”"],
    quote_size=15,
    attribution="Public Works Ministry statement, September 2025, as reported by MaltaToday.",
    context="On the sand and gravel laid on the Ta’ Qali picnic area in June 2025.",
    verdict="Contradicted", verdict_note="The grass did not return; the gravel is still there",
    footer_lines=["Version 1.0  ·  3 October 2026", "Status: draft for right of reply",
                  "Prepared from public sources and Copernicus Sentinel-2 data.",
                  "Repository: github.com/leandergrech/Mizien"],
    running_head="Ta’ Qali gravel and grass – Malta", version="1.0", date="3 October 2026",
    pdf_title="Will the grass come back at Ta' Qali? Claim Check 012",
    pdf_subject="Tests government and opposition claims about grass regrowth at the Ta' Qali picnic area with Sentinel-2",
    story=S))
