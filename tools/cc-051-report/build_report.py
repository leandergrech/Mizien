"""Claim Check 051 report. Run fetch_data.py, calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []
LG = colors.HexColor("#8DB36B")
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("Environment Minister Miriam Dalli said in 2025 that <b>“Malta protects more than 30% of its maritime zone”</b>; "
        "ERA says its marine Natura 2000 network covers “more than 35% of Malta’s Fisheries Management Zone”. "
        "International databases put Malta under 10%. We measured the protected area ourselves and divided it by each "
        "reference area in use.", lead)]
S.append(key_points([
    ("The protected area is as stated.",
     "EEA boundaries give 18 marine Natura 2000 sites covering 4,138 km² of sea once overlaps are counted once, "
     "matching ERA’s “over 4,100 km²”."),
    ("The percentage depends on what you divide by.",
     "4,138 km² is 36% of the 25-nautical-mile Fisheries Management Zone, 7.8% of the exclusive economic zone as mapped "
     "internationally and 5.5% of the 75,715 km² of marine waters Malta reports to the EU."),
    ("ERA says which zone it means; the minister did not.",
     "“Maritime zone” suggests all of Malta’s waters. The figure Malta reports for the EU’s 30% target is 5.5%, one of "
     "the lowest in the EU; reaching 30% on that basis would need about 18,600 km² more."),
    ("Protected on paper.",
     "Natura 2000 designation allows fishing and other uses if species are kept in good condition; this check does not "
     "assess management."),
    ("Verdict: misleading (moderate confidence).",
     "Accurate for the Fisheries Management Zone, but presented without that qualifier it gives an inaccurate impression "
     "of Malta’s standing against the EU target. The minister’s words are known through a news report."),
]))
S += [Spacer(1, 4 * mm), VerdictMeter(3), Spacer(1, 3 * mm),
      tiles([("4,138", GREEN, "km² of sea in 18 marine Natura 2000 sites (EEA)"),
             ("36%", GREEN, "of the 25-nm Fisheries Management Zone"),
             ("5.5%", RED, "of the marine waters Malta reports to the EU"),
             ("18,600", ORANGE, "km² more needed for 30% on the EU basis")]),
      Spacer(1, 4 * mm),
      up_down("The minister’s full statement showing the Fisheries Management Zone was named, or EU acceptance of the "
              "FMZ as Malta’s reference area.",
              "Evidence that Malta reports the 36% figure to the EU, or that sites are not managed."),
      Spacer(1, 5 * mm)]
S += toc([("1", "The claim"), ("2", "Method"), ("3", "What the data show"), ("4", "Where the evidence points different ways"),
          ("5", "Testing the claim"), ("6", "Verdict and requests for evidence"), ("7", "Limitations")])
S.append(PageBreak())
S.append(SectionHeading(1, "The claim"))
S.append(std_table([
    [C("What was said", cellh), C("Who", cellh), C("Access", cellh)],
    [C("“Malta protects more than 30% of its maritime zone, through Natura 2000 sites, scientific monitoring, and a €2 "
       "million conservation programme.”"), C("Minister Miriam Dalli, 2025 [2]"), C("Second-hand ◆")],
    [C("“Malta’s marine Natura 2000 network encompasses 18 sites and covers over 4100 km2, equivalent to more than 35% "
       "of Malta’s Fisheries Management Zone”"), C("ERA [1]"), C("Read in full")],
    [C("“designated over 35% of Malta’s waters as Marine Protected Areas” (2021)"), C("ERA [2]"), C("Second-hand ◆")],
], [104 * mm, 38 * mm, 28 * mm]))
S += [Spacer(1, 3 * mm), P("Amphora Media published a fact-check of the same statements in August 2025 [2]. We repeated the "
                           "measurement independently from the EEA boundaries.")]
S += [Spacer(1, 3 * mm), SectionHeading(2, "Method")]
S.append(P("Boundaries of all Maltese Natura 2000 sites from the EEA (2024 release) [3]; overlapping marine sites "
           "dissolved and land removed with OpenStreetMap coastlines; areas in UTM 33N. Reference areas: the Fisheries "
           "Management Zone as stated by the government (checked against a 25-nm buffer, about 11,650 km²), the "
           "exclusive economic zone used by Protected Planet and Marine Regions, and the area reported to the EU [4]. "
           "Scripts: <i>tools/cc-051-report/</i>."))
S.append(CondPageBreak(150 * mm))
S.append(SectionHeading(3, "What the data show"))
S.append(fig(FIG / "fig1_map.png", width=CW * 0.95))
S.append(P("Figure 1. The 18 marine sites, the 12-nm territorial sea and the 25-nm Fisheries Management Zone.", cap))
S.append(fig(FIG / "fig2_denominators.png"))
S.append(P("Figure 2. One protected area, three percentages.", cap))
S.append(std_table([
    [C("Measure", cellh), C("Value", cellh), C("Source", cellh), C("Grade", cellh)],
    [C("Protected sea, 18 sites (overlaps once)"), C("<b>4,138 km²</b>"), C("EEA [3]; ERA: over 4,100 [1]"), grade_tag("C")],
    [C("Share of Fisheries Management Zone (11,480 km²)"), C("36.0%"), C("calculated"), grade_tag("C")],
    [C("Share of EEZ as mapped internationally (~52,900 km²)"), C("7.8%"), C("calculated; Protected Planet 7.83%"), grade_tag("C")],
    [C("Share of marine waters reported to the EU (75,715 km²)"), C("5.5%"), C("calculated; BISE 5.5% [4]"), grade_tag("C")],
    [C("Extra area for 30% on the EU basis"), C("~18,600 km²"), C("calculated"), grade_tag("C")],
], [72 * mm, 32 * mm, 54 * mm, 12 * mm]))
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(4, "Where the evidence points different ways"))
S.append(contested(
    "Q1  Which area is the right one?", "DEPENDS ON THE PURPOSE", AMBER,
    "Malta manages the FMZ and its national biodiversity target is written for it; a University of Malta geologist told "
    "Amphora the FMZ reflects Malta’s practical mandate [2].",
    "For EU accounting Malta itself reports 75,715 km², and the EU’s 30% target is tracked on that basis [2, 4]. No "
    "other Mediterranean EU state was found using a fisheries zone as the denominator [2].",
    "<b>For this claim:</b> both percentages are arithmetic; only one is how Malta is measured against the EU target."))
S.append(contested(
    "Q2  Does “maritime zone” tell the reader which?", "NO", RED,
    "ERA’s own page names the Fisheries Management Zone [1].",
    "The minister’s statement does not, and “maritime zone” reads as all of Malta’s waters.",
    "<b>For this claim:</b> dropping the qualifier is what makes it misleading."))
S.append(CondPageBreak(90 * mm))
S.append(SectionHeading(5, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> 18 marine sites, over 4,100 km²"), C("4,138 km² [3]."), verd("SUPPORTED", GREENC)],
    [C("<b>B.</b> Over 35% of the Fisheries Management Zone"), C("36.0%."), verd("SUPPORTED", GREENC)],
    [C("<b>C.</b> Over 30% of Malta’s “maritime zone” / waters"), C("5.5% of the waters reported to the EU."),
     verd("MISLEADING", RED)],
], [52 * mm, 88 * mm, 30 * mm], valign="MIDDLE"))
S += [Spacer(1, 6 * mm), SectionHeading(6, "Verdict and requests for evidence"),
      verdict_box("Misleading", "True for the Fisheries Management Zone; presented as Malta’s seas it overstates "
                  "protection about sixfold. Confidence: moderate."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> The arithmetic behind “over 30%” is correct for one reference area. Stated as a share of Malta’s "
           "“maritime zone” or “waters” without naming that area, it gives the impression that Malta has met the EU’s "
           "30% target, while on the basis Malta itself reports to the EU the coverage is 5.5%. Confidence is moderate "
           "because the minister’s words are known through a news report."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list(["The minister’s statement in full, with event and date.",
                        "Which reference area Malta will use to report against the EU 2030 target.",
                        "Management plans and monitoring results for the offshore sites."]))
S += [Spacer(1, 6 * mm), SectionHeading(7, "Limitations")]
for l in ["Areas computed in UTM 33N with OSM coastlines; small differences from official GIS are expected.",
          "The EEZ and EU-reported areas are as published, not recomputed from boundary files.",
          "This check covers designation, not the effectiveness of protection."]:
    S.append(P("• " + l, bul))
S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Environment and Resources Authority. Marine Protected Areas (topic page); read 4 Oct 2026.",
     "https://era.org.mt/topic/marine-protected-areas-2/"),
    ("2", "Amphora Media (Aug 2025). FATTI: Does Malta protect about one-third of its seas? ◆ for quoted statements.",
     "https://www.amphora.media/2025/08/fatti-malta-protect-sea-marine-environment"),
    ("3", "European Environment Agency. Natura 2000 sites, 2024 release; queried 4 Oct 2026.",
     "https://bio.discomap.eea.europa.eu/arcgis/rest/services/ProtectedSites/Natura2000Sites/MapServer"),
    ("4", "Biodiversity Information System for Europe. Malta country page.", "https://biodiversity.europa.eu/countries/malta"),
    ("5", "MiŻien. Data and calculations: data/cc-051/; tools/cc-051-report/.", ""),
])
S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or official "
                "statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "4 Oct 2026", "First issue. Right of reply to the Environment Ministry and ERA not yet sent.")])
build_report(Report(
    number="051", out=str(FIG / "report.pdf"), kicker="Nature and the sea",
    title_lines=["Over 30% of", "our seas", "protected?"],
    subtitle_lines=["Testing a government claim about marine protected areas",
                    "against EEA boundaries and EU reporting"],
    quote_lines=["“Malta protects more than 30% of", "its maritime zone…”"], quote_size=16,
    attribution="Environment Minister Miriam Dalli, 2025 (as quoted by Amphora Media).",
    context="ERA: more than 35% of the Fisheries Management Zone.",
    verdict="Misleading", verdict_note="36% of the fisheries zone; 5.5% of the waters reported to the EU",
    footer_lines=["Version 1.0  ·  4 October 2026", "Status: draft (right of reply: Environment Ministry, ERA)",
                  "Prepared from EEA data and public sources.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Marine protected areas – Malta", version="1.0", date="4 October 2026",
    pdf_title="Over 30% of our seas protected? Claim Check 051",
    pdf_subject="Tests the claim that Malta protects more than 30% of its maritime zone", story=S))
