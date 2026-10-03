"""Claim Check 017 report. Run fetch_data.py, calc.py and figures.py first. Output: out/report.pdf"""
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
      P("In the Budget 2026 speech on 27 October 2025, Finance Minister Clyde Caruana said: <b>“A reclamation project is "
        "already under way in the Freeport, and now it is time to take the next step. The Government is preparing to "
        "launch a large-scale land reclamation project outside the Freeport perimeter next year.”</b> The land would serve "
        "industry and maritime activity and let commercial activities move away from where families live. Earlier, the "
        "government said a seabed study had found sites where reclamation causes the least environmental damage. We "
        "tested what can be tested a year later.", lead)]
S.append(key_points([
    ("The existing reclamation is real.",
     "Sentinel-2 imagery shows about 3.7 hectares (±1) of new land at Freeport Terminal 2 between summer 2023 and "
     "summer 2026, matching the 30,000 m² the Freeport Corporation describes, built with about a million tonnes of "
     "inert construction material."),
    ("The large-scale project has no public detail.",
     "Neither the speech nor the Prime Minister gave a site, size, cost, fill source or timetable. We found no project "
     "description, environmental screening, planning application or call for it by 3 October 2026."),
    ("The environmental basis is unpublished.",
     "The EUR 11 million seabed study, said in 2019 to identify five or six “environmentally safe” sites and to go to "
     "public consultation, has not been published. Budget lines for reclamation fell from EUR 500,000 (2023) to "
     "EUR 10,000 (2025)."),
    ("The area is close to protected sites.",
     "Three Natura 2000 sites lie about 1 km from the Freeport, including a 256 km² marine bird area to the south. "
     "Research ties coastal development and dumping to the loss of Mediterranean seagrass meadows."),
    ("Verdict: not substantiated (moderate confidence).",
     "The statement is a plan, and its first sentence is accurate. But the claim that the chosen sites do least "
     "environmental damage, and the benefits for families, rest on documents that have not been shown."),
]))
S += [Spacer(1, 4 * mm), VerdictMeter(2), Spacer(1, 3 * mm),
      tiles([("+3.7 ha", GREEN, "New land at Freeport Terminal 2, 2023–2026 (Sentinel-2)"),
             ("0", RED, "Sites, sizes or assessments published for the large-scale project"),
             ("1 km", ORANGE, "Distance from the Freeport to three Natura 2000 sites"),
             ("7 yrs", GREY, "Since the seabed study was promised for consultation")]),
      Spacer(1, 4 * mm),
      up_down("Publication of the seabed study and a project description naming the site, area, fill source and "
              "habitat survey, showing it avoids protected habitats.",
              "Evidence that the chosen area overlaps seagrass meadows or protected sites, or that no assessment was "
              "carried out."),
      Spacer(1, 5 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the research says"),
          ("4", "What the data show"), ("5", "Where the evidence points different ways"),
          ("6", "Testing the claim"), ("7", "Verdict and requests for evidence"), ("8", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The main claim is in the English text of the Budget Speech 2026 [1], which we read in full on the Ministry "
           "for Finance website. The Prime Minister expanded on it the next day [2]. The environmental claim dates from "
           "2019, when the then Environment Minister said a seabed study had identified sites where reclamation was "
           "“possible and environmentally safe” [3]."))
S.append(std_table([
    [C("What was said", cellh), C("Who", cellh), C("Access", cellh)],
    [C("“A reclamation project is already under way in the Freeport, and now it is time to take the next step.”"),
     C("Finance Minister [1]"), C("Read in full")],
    [C("“The Government is preparing to launch a large-scale land reclamation project outside the Freeport perimeter "
       "next year.” Industrial and maritime use; relocation of “certain commercial activities” so spaces can be "
       "“enjoyed by our families”."), C("Finance Minister [1]"), C("Read in full")],
    [C("The sea near the Freeport is “an ideal depth”; the aim is “to relocate industries that bother people”."),
     C("Prime Minister [2]"), C("Video summary")],
    [C("“There are five or six sites where reclamation is possible and environmentally safe.”"),
     C("Environment Minister, 2019 [3]"), C("Read in full")],
], [104 * mm, 38 * mm, 28 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("SCOPE NOTE", tag),
               P("This check does not judge whether Malta should reclaim land. It asks whether the statements are "
                 "backed by evidence that has been shown. Absence of a document in our searches is not proof that it "
                 "does not exist; we list what we are asking for.", small)], bg=AMBER_PALE, bar=AMBER),
      Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Questions.</b> (1) Is a reclamation under way at the Freeport? (2) Has the large-scale project been "
           "launched or described? (3) Is there shown evidence that the sites cause the least environmental damage?"))
S.append(P("<b>Evidence.</b> Sentinel-2 satellite imagery over Terminal 2, summers 2017–2026: for each summer, the "
           "per-pixel median of eight clear scenes, with land where the water index (NDWI) is below zero [8]. Natura "
           "2000 boundaries from the European Environment Agency [7]. Freeport operator statements [5, 6]; a press "
           "analysis of budget allocations [4]; peer-reviewed seagrass studies [9, 10]. Scripts: "
           "<i>tools/cc-017-report/</i>; data: <i>data/cc-017/</i>."))
S.append(P("<b>Grades.</b> Direct satellite measurement and peer-reviewed observational studies are grade B; official "
           "statements, statistics and reviews grade C. ◆ marks a source known second-hand."))

# ================================================================== 3
S.append(CondPageBreak(70 * mm))
S.append(SectionHeading(3, "What the research says"))
S.append(P("Posidonia oceanica meadows, a priority habitat under the EU Habitats Directive, have lost an estimated 34% "
           "of their known area across the Mediterranean in fifty years, mainly through the combined effect of local "
           "pressures [9]. A critical review lists coastal development, dredging and dumping among the main human causes "
           "[10]. Land reclamation combines all three: the footprint is lost and the fill and sediment plume can smother "
           "nearby beds. This is why the location and a habitat survey decide whether a site does “least damage”; the "
           "claim cannot be judged without them."))

# ================================================================== 4
S.append(CondPageBreak(150 * mm))
S.append(SectionHeading(4, "What the data show"))
S.append(fig(FIG / "fig1_terminal2.png"))
S.append(P("Figure 1. Land at Freeport Terminal 2 from Sentinel-2. No change 2017–2023; new land from 2024, about "
           "3.7 ha by summer 2026, close to the stated 30,000 m² [5, 6].", cap))
S.append(fig(FIG / "fig2_natura.png", width=CW * 0.85))
S.append(P("Figure 2. Natura 2000 sites around the Freeport. The dashed circle is 1.5 km. The marine bird area "
           "MT0000111 (Żona fil-Baħar fil-Lbiċ) begins about 1 km south [7].", cap))
S.append(std_table([
    [C("Indicator", cellh), C("Value", cellh), C("Source", cellh), C("Grade", cellh)],
    [C("New land at Terminal 2, 2023 → 2026"), C("<b>+3.7 ha (±1)</b>"), C("Sentinel-2 [8]"), grade_tag("B")],
    [C("Stated reclamation at Terminal 2"), C("~30,000 m²; ~1 Mt fill"), C("Freeport Corporation [5]"), grade_tag("C")],
    [C("Natura 2000 sites within 1.5 km"), C("3"), C("EEA [7]"), grade_tag("C")],
    [C("Marine SPA MT0000111"), C("1.1 km; 256 km²"), C("EEA [7]"), grade_tag("C")],
    [C("Reclamation budget 2023 / 2024 / 2025"), C("EUR 500k / 100k / 10k"), C("MaltaToday analysis ◆ [4]"), grade_tag("C")],
    [C("Seabed study published"), C("No"), C("Searches, 3 Oct 2026"), C("–")],
    [C("Project description, screening or call for the new project"), C("None found"), C("Searches, 3 Oct 2026"), C("–")],
], [74 * mm, 40 * mm, 44 * mm, 12 * mm]))
S.append(P("All values in <i>data/cc-017/checks.csv</i>. Distances are from a reference point at the Freeport "
           "(14.531 E, 35.819 N).", cap))

# ================================================================== 5
S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(5, "Where the evidence points different ways"))
S.append(contested(
    "Q1  Is the next step under way?", "NOT VISIBLE", AMBER,
    "The government has repeated the plan at the highest level, and a smaller reclamation is being built at the same "
    "port, so the capability and intent exist.",
    "A year after the speech, no site, size, cost, fill source, environmental screening or call has been made public. "
    "Similar announcements since 2005 were not delivered outside ports [4].",
    "<b>For this claim:</b> the launch “next year” is not yet shown."))
S.append(contested(
    "Q2  Are the sites the least environmentally damaging?", "NOT SHOWN", RED,
    "A seabed study costing EUR 11 million exists, and ERA’s draft is reported to have aimed to avoid Posidonia and "
    "protected areas [4].",
    "The study has not been published or consulted on, seven years after it was promised for consultation [3]. The "
    "Freeport area lies about 1 km from three Natura 2000 sites [7].",
    "<b>For this claim:</b> the environmental assurance rests on a document that has not been shown."))
S.append(contested(
    "Q3  Will families gain space?", "UNSPECIFIED", GREY,
    "Moving noisy or heavy industry away from homes could free land and reduce nuisance.",
    "Which activities would move, and which spaces would be freed, has not been said.",
    "<b>For this claim:</b> the benefit cannot be tested yet."))

# ================================================================== 6
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(6, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> A reclamation project is already under way in the Freeport"),
     C("About 3.7 ha of new land at Terminal 2 since 2023 [8], as stated [5, 6]."), verd("SUPPORTED", GREENC)],
    [C("<b>B.</b> A large-scale project outside the perimeter will be launched in 2026"),
     C("No public step found by 3 Oct 2026; no site or size given."), verd("NOT SHOWN", GREY)],
    [C("<b>C.</b> The sites cause least environmental damage (2019)"),
     C("Seabed study unpublished; Natura 2000 sites ~1 km away [7]."), verd("NOT SHOWN", RED)],
    [C("<b>D.</b> Commercial activity will move so families can enjoy the space"),
     C("Activities and spaces not identified."), verd("NOT SHOWN", GREY)],
], [52 * mm, 88 * mm, 30 * mm], valign="MIDDLE"))

# ================================================================== 7
S += [Spacer(1, 6 * mm), SectionHeading(7, "Verdict and requests for evidence"),
      verdict_box("Not substantiated", "Accurate about the existing works; the new project and its environmental "
                  "assurance have not been shown. Confidence: moderate."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) The first sentence checks out: land is being reclaimed at the Freeport. (2) The large-scale "
           "project is described only by purpose; nothing public lets anyone check its size, site or effects. (3) The "
           "claim that the sites are the least environmentally damaging depends on a study that has not been "
           "published, in an area close to protected sites. A plan stated more strongly than the evidence offered is "
           "what our scale calls <i>Not substantiated</i>; it may prove sound once the documents are shown."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "The ERA seabed / land reclamation study, with its site list, habitat maps and method.",
    "The site, area, fill source and timetable of the project outside the Freeport.",
    "Any environmental screening, strategic environmental assessment or habitat survey for it.",
    "Which commercial activities would move, and which spaces would be freed for families.",
]))

# ================================================================== 8
S += [Spacer(1, 6 * mm), SectionHeading(8, "Limitations")]
for l in ["Searches cannot prove a negative: a step may have been taken without public record.",
          "Satellite land areas are accurate to about ±1 ha (shoreline pixels, moored ships, glint).",
          "Benthic habitat (Posidonia) maps for Marsaxlokk Bay were not obtained; proximity to Natura 2000 sites is "
          "not by itself evidence of harm.",
          "Budget allocations are known through a press analysis ◆.",
          "Peer-reviewed papers were read as abstracts."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Caruana C. (27 Oct 2025). Budget Speech 2026, pp. 52–53. Ministry for Finance.",
     "https://finance.gov.mt/wp-content/uploads/2025/11/Budget-Speech-2026.pdf"),
    ("2", "Lovin Malta (28 Oct 2025). ‘Game changer’: Robert Abela discusses land reclamation plans off coast of "
          "Birżebbuġa.", "https://lovinmalta.com/news/watch-game-changer-robert-abela-discusses-land-reclamation-plans-off-cost-of-birzebbuga/"),
    ("3", "MaltaToday (Sep 2019). Land reclamation decision informed by EUR 11 million seabed study.",
     "https://www.maltatoday.com.mt/news/national/98630/land_reclamation_decision_informed_by_11_million_seabed_study"),
    ("4", "MaltaToday (15 Apr 2025). The land reclamation saga: a never-ending story. ◆",
     "https://www.maltatoday.com.mt/news/national/134510/analysis__the_land_reclamation_saga_a_neverending_story"),
    ("5", "Malta Freeport Corporation (2026). Squaring-off project: visit by the Prime Minister and Cabinet ministers.",
     "https://maltafreeport.gov.mt/uncategorized/squaring-off-project-visit-by-the-prime-minister-and-cabinet-ministers/News"),
    ("6", "Malta Freeport Terminals (5 Sep 2025). Prime Minister visits Freeport as ambitious Terminal 2 expansion "
          "gathers pace.", "https://maltafreeport.com.mt/news/prime-minister-visits-freeport-as-ambitious-terminal-2-expansion-gathers-pace/"),
    ("7", "European Environment Agency. Natura 2000 sites, 2024 release (discomap service); queried 3 Oct 2026.",
     "https://bio.discomap.eea.europa.eu/arcgis/rest/services/ProtectedSites/Natura2000Sites/MapServer"),
    ("8", "Copernicus Sentinel-2 L2A via Microsoft Planetary Computer, summers 2017–2026.",
     "https://planetarycomputer.microsoft.com/dataset/sentinel-2-l2a"),
    ("9", "Telesca L. et al. (2015). Seagrass meadows (Posidonia oceanica) distribution and trajectories of change. "
          "<i>Scientific Reports</i> 5:12505. doi:10.1038/srep12505. (Abstract read.)", "https://doi.org/10.1038/srep12505"),
    ("10", "Boudouresque C.-F., Bernard G., Pergent G., Shili A., Verlaque M. (2009). Regression of Mediterranean "
           "seagrasses caused by natural processes and anthropogenic disturbances and stress: a critical review. "
           "<i>Botanica Marina</i> 52(5):395–418. doi:10.1515/BOT.2009.057. (Abstract read.)",
     "https://doi.org/10.1515/BOT.2009.057"),
    ("11", "MiŻien. Data and calculations: data/cc-017/; tools/cc-017-report/.", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient, or direct measurement · C review, "
                "guidance or official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "3 Oct 2026", "First issue. Right of reply to the Ministry for Finance and the Ministry "
                    "for the Environment not yet sent.")])

build_report(Report(
    number="017", out=str(FIG / "report.pdf"), kicker="Planning and the sea",
    title_lines=["Reclaiming land", "outside the", "Freeport"],
    subtitle_lines=["Testing a Budget 2026 promise about land reclamation in Malta",
                    "against satellite imagery, protected-area maps and research"],
    quote_lines=["“The Government is preparing to launch a", "large-scale land reclamation project",
                 "outside the Freeport perimeter next year.”"], quote_size=15,
    attribution="Clyde Caruana, Minister for Finance, Budget Speech 2026, 27 October 2025.",
    context="Earlier: a seabed study found sites with least environmental damage.",
    verdict="Not substantiated", verdict_note="Existing works confirmed; the new project and its safety not shown",
    footer_lines=["Version 1.0  ·  3 October 2026", "Status: draft (right of reply: Finance, Environment ministries)",
                  "Prepared from public sources, Sentinel-2 and EEA data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Land reclamation outside the Freeport – Malta", version="1.0", date="3 October 2026",
    pdf_title="Reclaiming land outside the Freeport. Claim Check 017",
    pdf_subject="Tests the Budget 2026 statement on a large-scale land reclamation project outside the Malta Freeport",
    story=S))
