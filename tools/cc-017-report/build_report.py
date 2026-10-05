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
        "industry and maritime activity and let commercial activities move away from where families live. In 2019 the then "
        "Environment Minister said a seabed study had found “five or six sites where reclamation is possible and "
        "environmentally safe”. We tested what we could a year later.", lead)]
S.append(key_points([
    ("The existing reclamation is real.",
     "Sentinel-2 shows about 3.7 ha (±1) of new land at Freeport Terminal 2, summer 2023 to 2026, close to the "
     "30,000 m² the Freeport Corporation describes."),
    ("The large-scale project has no public detail.",
     "Neither the speech nor the Prime Minister gave a site, size, cost, fill source or timetable. We found no project "
     "description, environmental screening, planning application or call for it by 3 October 2026."),
    ("The environmental basis is unpublished.",
     "The EUR 11 million seabed study, said in 2019 to identify five or six “environmentally safe” sites and to go to "
     "public consultation, has not been published. Budget lines for reclamation fell from EUR 500,000 (2023) to "
     "EUR 10,000 (2025)."),
    ("The area is close to protected sites and mapped seagrass.",
     "Three Natura 2000 designations lie within about 0.5 km of the new land; a coarse 2016 map shows Posidonia "
     "meadows next to it, about 72 ha within 1 km. Malta reports its Posidonia beds overall as favourable; the 34% "
     "loss often cited is Mediterranean-wide."),
    ("Verdict: not substantiated (moderate confidence).",
     "The statement is a plan, and its first sentence is accurate. But the 2019 assurance that the sites are "
     "“possible and environmentally safe”, and the benefits for families, rest on documents that have not been shown."),
]))
S += [Spacer(1, 4 * mm), VerdictMeter(2), Spacer(1, 3 * mm),
      tiles([("+3.7 ha", GREEN, "New land at Freeport Terminal 2, 2023–2026 (Sentinel-2)"),
             ("0", RED, "Sites, sizes or assessments published for the large-scale project"),
             ("72 ha", ORANGE, "Of mapped Posidonia within 1 km of the new land (coarse 2016 map)"),
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
           "for Finance website. The Prime Minister expanded on it at a press conference after the Budget, as quoted by "
           "Lovin Malta on 28 October 2025 [2]. The environmental claim dates from 2019, when the then Environment "
           "Minister said a seabed study had identified sites where reclamation was “possible and environmentally "
           "safe” [3]."))
S.append(std_table([
    [C("What was said", cellh), C("Who", cellh), C("Access", cellh)],
    [C("“A reclamation project is already under way in the Freeport, and now it is time to take the next step.”"),
     C("Finance Minister [1]"), C("Read in full")],
    [C("“The Government is preparing to launch a large-scale land reclamation project outside the Freeport perimeter "
       "next year.” Industrial and maritime use; relocation of “certain commercial activities” so spaces can be "
       "“enjoyed by our families”."), C("Finance Minister [1]"), C("Read in full")],
    [C("“The sea near the Freeport is an ideal depth for these kinds of projects, and our idea is to relocate "
       "industries that bother people.”"), C("Prime Minister [2]"), C("Read in full")],
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
           "launched or described? (3) Is there shown evidence that the sites are “possible and environmentally safe”, as "
           "said in 2019?"))
S.append(P("<b>Evidence.</b> Sentinel-2 satellite imagery over Terminal 2, summers 2017–2026: for each summer, the "
           "per-pixel median of eight clear scenes, with land where the water index (NDWI) is below zero [8]. Natura "
           "2000 boundaries from the European Environment Agency [7]. Freeport operator statements [5, 6]; a press "
           "analysis of budget allocations [4]; peer-reviewed seagrass studies [9, 10]. New in version 1.2: the seagrass "
           "map of EMODnet Seabed Habitats [12] (open data, CC BY 4.0); sea depth from EMODnet Bathymetry [13]; and "
           "Malta’s own assessment of its Posidonia beds under Article 17 of the Habitats Directive [14]. Scripts: "
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
           "nearby beds. This is why the location and a habitat survey decide whether a site is “environmentally safe”; "
           "the claim cannot be judged without them."))
S.append(P("The 34% figure is for the whole Mediterranean, not for Malta. Malta’s own reports to the EU assess its "
           "Posidonia beds as favourable overall in both 2013–2018 and 2019–2024: 68.46 km² of meadow, from a complete "
           "survey in 2018–2019, of which 2.08 km² was not in good condition, with a stable trend [14]. That is a "
           "national assessment; it does not report the meadows of any one bay, and it does not test a new project."))

# ================================================================== 4
S.append(CondPageBreak(150 * mm))
S.append(SectionHeading(4, "What the data show"))
S.append(fig(FIG / "fig1_terminal2.png"))
S.append(P("Figure 1. Land at Freeport Terminal 2 from Sentinel-2. No change 2017–2023; new land from 2024, about "
           "3.7 ha by summer 2026, close to the stated 30,000 m² [5, 6].", cap))
S.append(fig(FIG / "fig2_natura.png", width=CW * 0.85))
S.append(P("Figure 2. Natura 2000 sites around the Freeport. The square marks the reference point used in version "
           "1.0, on the shore west of Terminal 2; the dashed circle around it is 1.5 km. The marine bird area MT0000111 "
           "(Żona fil-Baħar fil-Lbiċ) begins about 1.1 km south of that point and about 0.4 km south of the new land at "
           "Terminal 2 [7].", cap))
S.append(std_table([
    [C("Indicator", cellh), C("Value", cellh), C("Source", cellh), C("Grade", cellh)],
    [C("New land at Terminal 2, 2023 → 2026"), C("<b>+3.7 ha (±1)</b>"), C("Sentinel-2 [8]"), grade_tag("B")],
    [C("Stated reclamation at Terminal 2"), C("~30,000 m²; ~1 Mt fill"), C("Freeport Corporation [5]"), grade_tag("C")],
    [C("Natura 2000 designations within 1.5 km"), C("3 (two overlap on the same cliffs)"), C("EEA [7]"), grade_tag("C")],
    [C("Marine SPA MT0000111: distance; area"), C("0.4 km; 256 km²"), C("EEA [7]"), grade_tag("C")],
    [C("Cliff SAC MT0000024 and SPA MT0000033"), C("0.5 km"), C("EEA [7]"), grade_tag("C")],
    [C("Mapped Posidonia: nearest to the new land; within 1&nbsp;km"), C("Next grid cell (0.01 km); 72&nbsp;ha"),
     C("EMODnet, 2016 map [12]"), grade_tag("C")],
    [C("Sea depth within 1 km of the new land (10th–90th pct.)"), C("5–30 m (median 18 m)"), C("EMODnet [13]"),
     grade_tag("B")],
    [C("Depth of mapped meadows: in the bay; within 1 km of the new land (10th–90th pct.)"),
     C("11–35 m (median 26 m); 21–32 m (median 29 m)"), C("EMODnet [12, 13]"), grade_tag("B")],
    [C("Malta’s Posidonia beds, overall (2013–18; 2019–24)"), C("Favourable; favourable, stable"),
     C("Article 17 [14]"), grade_tag("C")],
    [C("Reclamation budget 2023 / 2024 / 2025"), C("EUR 500k / 100k / 10k"), C("MaltaToday analysis ◆ [4]"), grade_tag("C")],
    [C("Seabed study published"), C("No"), C("Searches, 3 Oct 2026"), C("–")],
    [C("Project description, screening or call for the new project"), C("None found"), C("Searches, 3 Oct 2026"), C("–")],
], [74 * mm, 40 * mm, 44 * mm, 12 * mm]))
S.append(P("All values in <i>data/cc-017/checks.csv</i> and <i>bay_stats.csv</i>. Distances are the shortest distance from the new land at "
           "Terminal 2 (Sentinel-2, 2023–2026) to each site boundary; from the edge of the 1.0 × 1.1 km Terminal 2 "
           "window they are 0.3 and 0.4 km (<i>data/cc-017/natura2000_distances.csv</i>). The site of the planned "
           "project is not known. MT0000033 lies almost wholly inside MT0000024. The seagrass map’s cells are about "
           "190 × 230 m, so its distance to the new land is only as precise as one cell.", cap))
S.append(fig(FIG / "fig3_bay.png"))
S.append(P("Figure 3. Marsaxlokk Bay. Sea depth from EMODnet (cells of about 100 m; near parts of the shore the grid "
           "has no depth) [13]; Posidonia meadows as mapped by EMODnet Seabed Habitats (Malta’s map of 2016, gridded "
           "at about 230 m, so coarse near the shore; CC BY 4.0) [12]; Natura 2000 sites [7]; new land at Terminal 2 "
           "[8]. The Prime Minister said the sea "
           "near the Freeport is “an ideal depth for these kinds of projects” [2]; the map shows the depths without "
           "judging which depth is ideal.", cap))

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
    "Q2  Are the sites “environmentally safe”?", "NOT SHOWN", RED,
    "A seabed study costing EUR 11 million exists, and ERA’s draft is reported to have aimed to avoid Posidonia and "
    "protected areas [4]. Malta reports its Posidonia beds overall as favourable and stable [14].",
    "The study has not been published or consulted on, seven years after it was promised for consultation [3]. The "
    "new land at Terminal 2 lies about 0.4 km from a marine Natura 2000 site and 0.5 km from protected cliffs [7]; "
    "a coarse 2016 map shows Posidonia next to it, with about 72 ha within 1 km [12].",
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
    [C("<b>C.</b> “There are five or six sites where reclamation is possible and environmentally safe” (2019)"),
     C("Seabed study unpublished; a marine Natura 2000 site lies ~0.4 km from the Terminal 2 works, and Posidonia "
       "is mapped next to them [7, 12]."), verd("NOT SHOWN", RED)],
    [C("<b>D.</b> Commercial activity will move so families can enjoy the space"),
     C("Activities and spaces not identified."), verd("NOT SHOWN", GREY)],
    [C("<b>E.</b> “The sea near the Freeport is an ideal depth for these kinds of projects” (Prime Minister)"),
     C("Within 1 km of the Terminal 2 works the sea is mostly 5–30 m deep [13]; “ideal” is not defined. Mapped "
       "meadows near the works lie at 21–32 m (11–35 m across the bay) [12, 13]."), verd("NOT TESTED", GREY)],
], [52 * mm, 88 * mm, 30 * mm], valign="MIDDLE"))

# ================================================================== 7
S += [Spacer(1, 6 * mm), SectionHeading(7, "Verdict and requests for evidence"),
      verdict_box("Not substantiated", "Accurate about the existing works; the new project and its environmental "
                  "assurance have not been shown. Confidence: moderate."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) The first sentence checks out: land is being reclaimed at the Freeport. (2) The large-scale "
           "project is described only by purpose; nothing public lets anyone check its size, site or effects. (3) The "
           "2019 statement that the sites are “possible and environmentally safe” depends on a study that has not been "
           "published, in an area close to protected sites. A plan stated more strongly than the evidence offered is "
           "what our scale calls <i>Not substantiated</i>; it may prove sound once the documents are shown."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "The ERA seabed / land reclamation study, with its site list, habitat maps and method.",
    "The site, area, fill source and timetable of the project outside the Freeport.",
    "Any environmental screening, strategic environmental assessment or habitat survey for it.",
    "The 2018–2019 national Posidonia survey reported to the EU, as a map of Marsaxlokk Bay (we did not find it "
    "published).",
    "Which commercial activities would move, and which spaces would be freed for families.",
]))

# ================================================================== 8
S += [Spacer(1, 6 * mm), SectionHeading(8, "Limitations")]
for l in ["Searches cannot prove a negative: a step may have been taken without public record.",
          "Satellite land areas are accurate to about ±1 ha (shoreline pixels, moored ships, glint).",
          "EMODnet’s Maltese seagrass map (EUSM16me, 2016) is gridded at about 230 m, so it is coarse near the "
          "shore: its cells overlap the coast in places (about 2.5 ha in the map frame), and distances to it are only "
          "as precise as one cell. A finer global layer exists but was not used, for licence reasons. The map shows "
          "where meadows were mapped, not their condition now; nearness to meadows or Natura 2000 sites is not by "
          "itself evidence of harm.",
          "EMODnet depth cells are about 100 m across; near the shore and in parts of the inner harbour the grid has "
          "no depth.",
          "We tried a bay-wide Sentinel-2 check for new land outside Terminal 2 (MNDWI, green and SWIR bands). It was "
          "not robust: over open water the index changed sign between scenes, giving tens of hectares of false change "
          "in control years, so it is not used (<i>tools/cc-017-report/s2_bay.py</i>).",
          "Budget allocations are known through a press analysis ◆.",
          "Peer-reviewed papers were read as abstracts."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Caruana C. (27 Oct 2025). Budget Speech 2026, pp. 52–53. Ministry for Finance.",
     "https://finance.gov.mt/wp-content/uploads/2025/11/Budget-Speech-2026.pdf"),
    ("2", "Diacono T., Lovin Malta (28 Oct 2025). ‘Game changer’: Robert Abela discusses land reclamation plans off "
          "coast of Birżebbuġa. (Read in full, 5 Oct 2026.)", "https://lovinmalta.com/news/watch-game-changer-robert-abela-discusses-land-reclamation-plans-off-cost-of-birzebbuga/"),
    ("3", "MaltaToday (Sep 2019). Land reclamation decision informed by EUR 11 million seabed study.",
     "https://www.maltatoday.com.mt/news/national/98630/land_reclamation_decision_informed_by_11_million_seabed_study"),
    ("4", "MaltaToday (15 Apr 2025). The land reclamation saga: a never-ending story. ◆",
     "https://www.maltatoday.com.mt/news/national/134510/analysis__the_land_reclamation_saga_a_neverending_story"),
    ("5", "Malta Freeport Corporation (2026). Squaring-off project: visit by the Prime Minister and Cabinet ministers.",
     "https://maltafreeport.gov.mt/uncategorized/squaring-off-project-visit-by-the-prime-minister-and-cabinet-ministers/News"),
    ("6", "Malta Freeport Terminals (5 Sep 2025). Prime Minister visits Freeport as ambitious Terminal 2 expansion "
          "gathers pace.", "https://maltafreeport.com.mt/news/prime-minister-visits-freeport-as-ambitious-terminal-2-expansion-gathers-pace/"),
    ("7", "European Environment Agency. Natura 2000 sites, 2024 release (discomap service); queried 3 and 5 Oct 2026.",
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
    ("12", "EMODnet Seabed Habitats (2025). Seagrass cover (Essential Ocean Variable) in Europe and the Caribbean, "
           "version 2025. European Marine Observation and Data Network (EMODnet) Seabed Habitats. Contains information "
           "sourced from multiple organisations through EMODnet Seabed Habitats. Licensed under CC BY 4.0 (European "
           "subset); queried 5 Oct 2026 and clipped to the map frame. Maltese polygons from map EUSM16me (2016), "
           "gridded at about 230 m; the source field names the Malta Environment and Planning Authority for some of "
           "them and is blank for those in this bay.",
     "https://emodnet.ec.europa.eu/geonetwork/srv/eng/catalog.search#/metadata/39746d9c-4220-425c-bc26-7cb3056c36a5"),
    ("13", "EMODnet Bathymetry Consortium (2024). EMODnet Digital Bathymetry (DTM 2024). "
           "doi:10.12770/cf51df64-56f9-4a99-b1aa-36b8d7b743a1. Via the EMODnet WCS, 5 Oct 2026.",
     "https://doi.org/10.12770/cf51df64-56f9-4a99-b1aa-36b8d7b743a1"),
    ("14", "European Environment Agency. Article 17 web tool: habitat 1120 Posidonia beds, Malta (Mediterranean marine "
           "region), periods 2013–2018 and 2019–2024; read 5 Oct 2026.",
     "https://nature-art17.eionet.europa.eu/article17/habitat/summary/?period=6&subject=1120"),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient, or direct measurement · C review, "
                "guidance or official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "3 Oct 2026", "First issue. Right of reply to the Ministry for Finance and the Ministry "
                    "for the Environment not yet sent."),
                   ("1.1", "5 Oct 2026", "Corrections. (1) The 2019 statement is quoted as said: “least environmental "
                    "damage” (a paraphrase) → “possible and environmentally safe” (cover, TL;DR, sections 2, 3, 5, 6 and 7); "
                    "sub-claim C now tests that wording. (2) Distance to Natura 2000: “about 1 km from the Freeport”, "
                    "measured from an onshore point west of Terminal 2 → 0.4 km from the new land at Terminal 2 to the "
                    "marine SPA MT0000111 and 0.5 km to the cliff sites (shortest distance to the EEA boundaries; "
                    "<i>data/cc-017/natura2000_distances.csv</i>); tile “1 km” → “0.4 km”. (3) “Three Natura 2000 "
                    "sites” → three designations, two of which (SAC MT0000024, SPA MT0000033) overlap on the same "
                    "cliffs. (4) Flyer: right of reply now names the Finance and Environment ministries, as the report "
                    "does; the −34% seagrass loss is labelled Mediterranean-wide. Verdict and confidence unchanged."),
                   ("1.2", "5 Oct 2026", "Upgrade. (1) New Figure 3: a map of Marsaxlokk Bay with sea depth "
                    "(EMODnet), mapped Posidonia meadows, full-resolution Natura 2000 boundaries and the new land at "
                    "Terminal 2; within 1 km of the new land the sea is mostly 5–30 m deep. (2) Fairness: Malta’s Article 17 "
                    "reports assess its Posidonia beds as favourable overall (2013–2018; 2019–2024, stable); the −34% "
                    "loss is Mediterranean-wide (section 3, Q2, TL;DR, flyer). (3) The Prime Minister’s words are now "
                    "quoted in full from Lovin Malta, and tested as sub-claim E (not tested: “ideal” is not defined). "
                    "(4) Tile “0.4 km” → mapped Posidonia within 1 km of the new land (the 0.4 km stays in the text). "
                    "(5) A bay-wide Sentinel-2 check for other new land was tried and dropped as not robust "
                    "(limitations). Verdict and confidence unchanged."),
                   ("1.2", "5 Oct 2026", "Maintainer decision (5 Oct 2026): the map and all seagrass statistics now use "
                    "the EMODnet Seabed Habitats layer only (CC BY 4.0), whose Maltese map (2016) is gridded at about "
                    "230 m (limitations). Mapped Posidonia lies next to the new land (0.01 km, one grid cell), 72 ha "
                    "within 1 km; mapped meadows lie at 11–35 m in the bay (median 26 m) and 21–32 m within 1 km "
                    "(median 29 m). Tile and flyer card “72 ha”. Verdict and confidence unchanged.")])

build_report(Report(
    number="017", out=str(FIG / "report.pdf"), kicker="Planning and the sea",
    title_lines=["Reclaiming land", "outside the", "Freeport"],
    subtitle_lines=["Testing a Budget 2026 promise about land reclamation in Malta",
                    "against satellite imagery, seabed and protected-area maps and research"],
    quote_lines=["“The Government is preparing to launch a", "large-scale land reclamation project",
                 "outside the Freeport perimeter next year.”"], quote_size=15,
    attribution="Clyde Caruana, Minister for Finance, Budget Speech 2026, 27 October 2025.",
    context="In 2019: a seabed study found sites “possible and environmentally safe” (Environment Minister).",
    verdict="Not substantiated", verdict_note="Existing works confirmed; the new project and its safety not shown",
    footer_lines=["Version 1.2  ·  5 October 2026", "Status: draft (right of reply: Finance, Environment ministries)",
                  "Prepared from public sources, Sentinel-2, EEA and EMODnet data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Land reclamation outside the Freeport – Malta", version="1.2", date="5 October 2026",
    pdf_title="Reclaiming land outside the Freeport. Claim Check 017",
    pdf_subject="Tests the Budget 2026 statement on a large-scale land reclamation project outside the Malta Freeport",
    story=S))
