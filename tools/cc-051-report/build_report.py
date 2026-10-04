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
        "We mapped every marine Natura 2000 site from EEA boundaries and laid it over each zone Malta’s waters are "
        "measured by. The maps show that all of the protected sea lies within 25 nautical miles of the coast, and that "
        "beyond that line, in 85% of the waters Malta reports to the EU, there is no marine protected site at all.", lead)]
S.append(key_points([
    ("The protected area is as stated.",
     "EEA boundaries give 18 marine Natura 2000 sites covering 4,138 km² of sea once overlaps are counted once, "
     "matching ERA’s “over 4,100 km²”."),
    ("All of it lies within 25 nautical miles.",
     "No site reaches beyond the Fisheries Management Zone. Outside it lie about 64,000 km² of the 75,715 km² Malta "
     "reports to the EU, none of them in a marine protected site (Figures 1 and 2)."),
    ("So the percentage depends on what you divide by.",
     "4,138 km² is 36% of the Fisheries Management Zone, 7.8% of the exclusive economic zone as mapped internationally "
     "and 5.5% of the waters reported to the EU (Figure 3). Even if every square kilometre within 25 nm were protected, "
     "the share of the waters reported to the EU would be 15%."),
    ("The deep sea is almost unprotected.",
     "A quarter of the waters reported to the EU are deeper than 1,000 m; 0.6% of that deep sea is protected, against "
     "14% of the shallow shelf (Figure 4)."),
    ("ERA says which zone it means; the minister did not.",
     "“Maritime zone” suggests all of Malta’s waters. Reaching 30% on the EU basis would need about 18,600 km² more. "
     "The EU’s 30% is a target for the EU as a whole, so 5.5% breaks no rule, but it is not “more than 30%”."),
    ("Verdict: misleading (moderate confidence).",
     "Accurate for the 25-nm zone only; unqualified, it overstates protection about sixfold. The minister’s words are "
     "known through a news report, and this check covers designation, not management."),
]))
S += [Spacer(1, 4 * mm), VerdictMeter(3), Spacer(1, 3 * mm),
      tiles([("4,138", GREEN, "km² of sea in 18 marine Natura 2000 sites (EEA)"),
             ("36%", GREEN, "of the 25-nm Fisheries Management Zone"),
             ("5.5%", RED, "of the marine waters Malta reports to the EU"),
             ("0 km²", RED, "protected beyond 25 nm, where 85% of those waters lie")]),
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
           "dissolved and land removed with OpenStreetMap coastlines; areas in UTM 33N. Reference areas and their "
           "outlines: the Fisheries Management Zone, 11,480 km² as stated by the government, rebuilt as 25 nm from "
           "Malta’s baselines using the Marine Regions 12-nm limit (11,492 km²) [6]; the exclusive economic zone as "
           "mapped by Marine Regions (52,923 km²) [5]; and the 75,715 km² of marine waters Malta reports to the EU "
           "[2, 4], drawn from the EEA’s map of the waters reported under the Marine Strategy Framework Directive [7]. "
           "Percentages use the official totals; the outlines show where the protected sea lies. Depth from the EMODnet "
           "grid [8], grouped into shelf (0–200 m), slope (200–1,000 m) and deep sea (over 1,000 m). Data and scripts: "
           "<i>data/cc-051/</i>, <i>tools/cc-051-report/</i> [11]."))
S.append(CondPageBreak(150 * mm))
S.append(SectionHeading(3, "What the data show"))
S.append(P("Close up, the network looks extensive: the 18 sites cover much of the sea around Malta and Gozo, and fill "
           "36% of the 25-nm Fisheries Management Zone (Figure 1). Every site stops at or inside the 25-nm line."))
S.append(fig(FIG / "fig1_map.png", width=CW * 0.95))
S.append(P("Figure 1. The 18 marine sites, the 12-nm territorial sea and the 25-nm Fisheries Management Zone.", cap))
S.append(P("The waters Malta reports to the EU reach much further, up to about 350 km to the south-east, over an area "
           "more than six times the size of the fisheries zone (Figure 2). In the EEA’s map of these "
           "waters, Malta’s area is labelled “area designated for hydrocarbon exploration and exploitation” [7]. "
           "Beyond 25 nm, about 64,000 km² (85% of the 75,715 km²) contains no marine protected site."))
S.append(fig(FIG / "fig2_wide_map.png"))
S.append(P("Figure 2. All of the waters Malta reports to the EU: protected sites in green, everything else in red.", cap))
S.append(P("Measured against each area in turn, the same protected sea gives three very different percentages "
           "(Figure 3). Only the smallest area, the fisheries zone, takes the figure above 30%."))
S.append(fig(FIG / "fig3_three_areas.png"))
S.append(P("Figure 3. One protected area, three percentages. Same scale in each panel; the amber mark is 30%.", cap))
S.append(std_table([
    [C("Measure", cellh), C("Value", cellh), C("Source", cellh), C("Grade", cellh)],
    [C("Protected sea, 18 sites (overlaps once)"), C("<b>4,138 km²</b>"), C("EEA [3]; ERA: over 4,100 [1]"), grade_tag("C")],
    [C("Share of Fisheries Management Zone (11,480 km²)"), C("36.0%"), C("calculated"), grade_tag("C")],
    [C("Share of EEZ as mapped internationally (~52,900 km²)"), C("7.8%"), C("calculated; Protected Planet 7.83%"), grade_tag("C")],
    [C("Share of marine waters reported to the EU (75,715 km²)"), C("5.5%"), C("calculated; BISE 5.5% [4]"), grade_tag("C")],
    [C("Protected sea more than 25 nm from the baselines"), C("<b>0 km²</b>"), C("calculated [3, 6]"), grade_tag("C")],
    [C("Reported waters beyond 25 nm, none protected"), C("~64,200 km² (85%)"), C("calculated"), grade_tag("C")],
    [C("Whole 25-nm zone as a share of the reported waters"), C("15.2%"), C("calculated"), grade_tag("C")],
    [C("Extra area for 30% on the EU basis"), C("~18,600 km²"), C("calculated"), grade_tag("C")],
], [72 * mm, 32 * mm, 54 * mm, 12 * mm]))
S.append(Spacer(1, 4 * mm))
S.append(P("<b>Which kinds of sea are protected.</b> The global 30% target asks for protected areas that are "
           "“ecologically representative” [10]. Depth is a coarse guide to the kinds of seabed and sea life an area "
           "holds. Within 25 nm the sites cover about a third of both the shelf and the slope. Across all the waters "
           "reported to the EU the picture changes: 14% of the shelf, 5.3% of the slope and 0.6% of the deep sea are "
           "protected (Figure 4). The deep sea, over 1,000 m, makes up a quarter of those waters; 97% of the protected "
           "sea is shallower than that."))
S.append(fig(FIG / "fig4_depth.png"))
S.append(P("Figure 4. Depth bands across the waters Malta reports to the EU, with the protected sites hatched, and the "
           "share of each band that is protected.", cap))
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(4, "Where the evidence points different ways"))
S.append(contested(
    "Q1  Which area is the right one?", "DEPENDS ON THE PURPOSE", AMBER,
    "Malta manages the FMZ and its national biodiversity target is written for it; a University of Malta geologist told "
    "Amphora the FMZ reflects Malta’s practical mandate [2].",
    "For EU accounting Malta itself reports 75,715 km², and the EU’s 30% target is tracked on that basis [2, 4]. No "
    "other Mediterranean EU state was found using a fisheries zone as the denominator [2]. All of the protected sea "
    "lies inside the fisheries zone, so dividing by that zone leaves out every unprotected square kilometre beyond it.",
    "<b>For this claim:</b> both percentages are arithmetic; only one is how Malta is measured against the EU target. "
    "The 30% is a target for the EU as a whole, with each state doing its “fair share” [9], so 5.5% breaks no rule; "
    "it is not “more than 30%” either."))
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
    [C("<b>B.</b> Over 35% of the Fisheries Management Zone"),
     C("36.0% as ERA divides it (34–35% if internal waters are treated alike; see Limitations)."), verd("SUPPORTED", GREENC)],
    [C("<b>C.</b> Over 30% of Malta’s “maritime zone” / waters"),
     C("5.5% of the waters reported to the EU; no protected site beyond 25 nm, where 85% of them lie."),
     verd("MISLEADING", RED)],
], [52 * mm, 88 * mm, 30 * mm], valign="MIDDLE"))
S += [Spacer(1, 6 * mm), SectionHeading(6, "Verdict and requests for evidence"),
      verdict_box("Misleading", "“Over 30%” holds only for the 25-nm fisheries zone. Of the 75,715 km² Malta reports "
                  "to the EU, 5.5% is protected, and nothing beyond 25 nm. Confidence: moderate."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> The arithmetic behind “over 30%” is correct for one reference area, the 25-nm fisheries zone, "
           "and that zone contains all of the protected sea. Stated as a share of Malta’s “maritime zone” or “waters” "
           "without naming that area, it gives the impression that Malta has met the EU’s 30% target. On the basis "
           "Malta itself reports to the EU the coverage is 5.5%: the 64,000 km² beyond 25 nm, including nearly all of "
           "the deep sea, has no marine protected site. Confidence is moderate because the minister’s words are known "
           "through a news report."))
S.append(CondPageBreak(40 * mm))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list(["The minister’s statement in full, with event and date.",
                        "Which reference area Malta will use to report against the EU 2030 target.",
                        "Management plans and monitoring results for the offshore sites.",
                        "Any plans for protected areas beyond 25 nm, including deep-sea habitats."]))
S += [Spacer(1, 6 * mm), SectionHeading(7, "Limitations")]
for l in ["Areas computed in UTM 33N with OSM coastlines; small differences from official GIS are expected.",
          "Percentages use the published EEZ and EU-reported areas. The outlines agree within 0.5%: 52,891 km² "
          "(Marine Regions) and 75,484 km² (the EEA’s simplified web outline).",
          "About 183 km² of the protected sea lies in internal waters, landward of the baselines, which the 11,480 km² "
          "zone excludes. Treated alike in both numerator and denominator, the fisheries-zone share is 34–35%, still "
          "over 30%.",
          "Depth bands come from a grid of about 200 m and are a proxy for habitat types, not a habitat map.",
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
    ("5", "Flanders Marine Institute (2023). Maritime Boundaries Geodatabase: Maritime Boundaries and Exclusive Economic "
          "Zones (200NM), version 12. doi:10.14284/632.", "https://doi.org/10.14284/632"),
    ("6", "Flanders Marine Institute (2023). Maritime Boundaries Geodatabase: Territorial Seas (12NM), version 4. "
          "doi:10.14284/633.", "https://doi.org/10.14284/633"),
    ("7", "European Environment Agency (2020). Marine waters used in Marine Strategy Framework Directive (MSFD), "
          "version 1.0; map service queried 4 Oct 2026.",
     "https://water.discomap.eea.europa.eu/arcgis/rest/services/Marine/Marine_waters_EU/MapServer"),
    ("8", "EMODnet Bathymetry digital terrain model, via the EEA Bathymetry image service; queried 4 Oct 2026.",
     "https://water.discomap.eea.europa.eu/arcgis/rest/services/Marine/Bathymetry/ImageServer"),
    ("9", "European Commission (2020). EU Biodiversity Strategy for 2030: Bringing nature back into our lives. "
          "COM(2020) 380 final, section 2.1.", "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52020DC0380"),
    ("10", "Convention on Biological Diversity (2022). Kunming-Montreal Global Biodiversity Framework, Decision 15/4, "
           "Target 3.", "https://www.cbd.int/gbf/targets/3"),
    ("11", "MiŻien. Data and calculations: data/cc-051/; tools/cc-051-report/.", ""),
])
S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or official "
                "statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "4 Oct 2026", "First issue. Right of reply to the Environment Ministry and ERA not yet sent."),
                   ("1.1", "4 Oct 2026", "Maps of all the waters Malta reports to the EU, the three reference areas and "
                    "depth bands; areas measured from boundary files; clearer summary. Verdict unchanged.")])
build_report(Report(
    number="051", out=str(FIG / "report.pdf"), kicker="Nature and the sea",
    title_lines=["Over 30% of", "our seas", "protected?"],
    subtitle_lines=["Testing a government claim about marine protected areas",
                    "against EEA boundaries and EU reporting"],
    quote_lines=["“Malta protects more than 30% of", "its maritime zone…”"], quote_size=16,
    attribution="Environment Minister Miriam Dalli, 2025 (as quoted by Amphora Media).",
    context="ERA: more than 35% of the Fisheries Management Zone.",
    verdict="Misleading", verdict_note="36% of the 25-nm fisheries zone; 5.5% of the waters reported to the EU",
    footer_lines=["Version 1.1  ·  4 October 2026", "Status: draft (right of reply: Environment Ministry, ERA)",
                  "Prepared from EEA data and public sources.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Marine protected areas – Malta", version="1.1", date="4 October 2026",
    pdf_title="Over 30% of our seas protected? Claim Check 051",
    pdf_subject="Tests the claim that Malta protects more than 30% of its maritime zone", story=S))
