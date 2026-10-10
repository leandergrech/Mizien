"""Claim Check 092 report. Run fetch.py, search_programme.py, calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []

# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("Before the general election of 30 May 2026 [22], the <b>Nationalist Party</b> promised a plan to make <b>Gozo a "
        "Net-Zero Island by 2040</b>, “where every unit of emissions generated is reduced or offset”, listing "
        "<b>afforestation</b> among the initiatives [1]. News reports said net zero “through afforestation” [4] and "
        "reported an indigenous-tree strategy [5 ◆]. Claim Check 107 tested the net-zero plan; this check tests what new "
        "forest could do on Gozo.", lead)]
S.append(key_points([
    ("One item in a list, with no numbers.",
     "Afforestation appears once in the Gozo chapter and twice in the environment chapter, including “more "
     "afforestation” in Malta and Gozo [1, 2], with no area, species, sites, carbon rate or date."),
    ("Trees alone could not do it.",
     "Offsetting Gozo’s energy CO<sub>2</sub> (118,000–154,000 t a year, 2016–2020 [6]) would take new forest 4.9–6.3 "
     "times Gozo’s area at a rate measured in a dry pine forest [7], and 2.3–25 times across published rates [8, 9]."),
    ("Realistically, a few per cent.",
     "CORINE maps no forest on Gozo. Planting all of its 1,270 ha of garrigue, maquis and sparse vegetation [18] would "
     "offset about 3–4% of that CO<sub>2</sub> (1–8% across rates), and over a third of that land lies in Natura 2000 "
     "sites [23]."),
    ("Water and time limit it further.",
     "Malta is in permanent water scarcity [17]; 30–58% of planted pines survived 20 years in an arid Spanish trial "
     "[12]; native oak plantations in Spain added no soil carbon in up to 24 years [8]."),
    ("No indigenous-tree strategy in the programme. Pledge label: Not measurable (10 October 2026).",
     "“Indigenous” appears once, for farm varieties and breeds [3]. A pledge is not false; as worded, its "
     "afforestation cannot be shown to be delivered or missed."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(0, scale="pledge"), Spacer(1, 2 * mm),
      tiles([("4.9–6.3×", RED, "Gozo’s area needed as new forest to offset its energy CO₂ (measured rate)"),
             ("3–4%", ORANGE, "of that CO₂ offset if all Gozo’s semi-natural land were planted"),
             ("0 ha", GREY, "of forest mapped on Gozo (CORINE 2018)"),
             ("Not found", GREY, "an indigenous-tree strategy in the 16 programme chapters")]),
      Spacer(1, 3 * mm),
      up_down("An afforestation target for Gozo with area, sites, species, years and the carbon rate assumed, within a "
              "Gozo emissions inventory and a 2040 pathway.",
              "A plan that counts on Gozo’s trees for more than a few per cent of its emissions, or plants on garrigue "
              "the programme itself would protect.",
              heads=("What would make it measurable", "What would count against it")),
      Spacer(1, 3 * mm)]
S += toc([("1", "The pledge and what we could verify"), ("2", "Method"), ("3", "How new forests store carbon"),
          ("4", "What the studies found"), ("5", "Where the science disagrees"), ("6", "The arithmetic"),
          ("7", "Testing the pledge"), ("8", "Pledge label and requests for evidence"), ("9", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The pledge and what we could verify"))
S.append(P("Our candidate record took the claim from a MaltaToday breakdown of the programme [5], which says Gozo would "
           "become net zero through afforestation alongside a national indigenous-tree strategy. That article could not "
           "be read (HTTP 403; the Internet Archive was unreachable), so we went to the programme itself, <i>Nifs Ġdid</i>, "
           "published by the PN as 16 web chapters and 16 chapter PDFs (the pages are dated 18 May 2026). We read all of "
           "them on 10 October 2026 and searched each for the words this check turns on; the counts and file hashes are in "
           "<i>data/cc-092/pn_programme_search.csv</i>. The programme is in Maltese; translations are ours."))
S.append(std_table([
    [C("Source", cellh), C("What it says (our translation)", cellh), C("Our access", cellh), C("Status", cellh)],
    [C("<b>PN</b>, <i>Nifs Ġdid</i>, chapter Għawdex, item 46 [1]"),
     C("A plan so that by 2040 Gozo becomes a Net-Zero Island, “where every unit of emissions generated is reduced or "
       "offset” (<i>imnaqqsa jew ikkumpensata</i>) by initiatives such as solar panels, electric vehicles, building "
       "efficiency, ecological restoration on land and at sea, “afforestation” (<i>afforestazzjoni</i>) and water and "
       "soil conservation, “among others”."),
     C("Read in full (web page and PDF p. 16)."), C("<b>The pledge</b>")],
    [C("<b>PN</b>, chapter Ambjent, items 01, 20 and 25 [2]"),
     C("01: a park in every locality; “the plan also includes more afforestation and open spaces in both Malta and "
       "Gozo”. 20: tree planting and afforestation, with valley restoration and rain gardens, “to fight urban heat, "
       "flooding and pollution”. 25: a Malta Nature Network protecting valleys, rubble walls and garrigue (<i>xagħri</i>)."),
     C("Read in full (PDF pp. 8, 12, 13)."), C("Related pledges")],
    [C("<b>PN</b>, chapter Agrikoltura u Sajd, item 31 [3]"),
     C("Conservation and propagation of local plant varieties and livestock breeds (<i>indiġeni</i>), with a gene bank, "
       "nursery and support programme within three years."), C("Read in full (PDF p. 13)."),
     C("Only use of “indigenous”")],
    [C("<b>MaltaToday</b>, May 2026 [4]"), C("Gozo would become a net-zero island through afforestation."),
     C("Read via the Internet Archive for Claim Check 107 (5 Oct 2026)."), C("News summary")],
    [C("<b>MaltaToday</b>, breakdown, May 2026 [5 ◆]"),
     C("Seen only as a search engine’s summary: a nationwide afforestation strategy prioritising indigenous trees and "
       "valley restoration."), C("Not read (403)."), C("Locator; second-hand")],
], [33 * mm, 85 * mm, 30 * mm, 22 * mm]))
S += [Spacer(1, 3 * mm),
      callout([P("FAIRNESS NOTE", tag),
               P("Labour won the general election of 30 May 2026 [22], so this is an opposition proposal. The Government’s "
                 "own aim of a climate-neutral Gozo (Claim Check 031) and Labour’s 2022 pledge of 100,000 trees (Claim "
                 "Check 010) are held to the same standard. The PN’s environment chapter presents trees mainly as a defence "
                 "against heat, flooding and pollution [2]; those benefits are real but are not what this check measures. "
                 "Nothing here says afforestation is undesirable or that anyone acted in bad faith.", small)],
              bg=AMBER_PALE, bar=AMBER)]

# ================================================================== 2
S.append(CondPageBreak(70 * mm))
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Question.</b> As worded, can the afforestation in the PN’s pledge be measured, and how much of Gozo’s "
           "emissions could new forest on Gozo offset? Does the programme contain an indigenous-tree strategy?"))
S.append(P("<b>Gozo’s emissions.</b> There is no official greenhouse-gas inventory for Gozo. We use the energy-related "
           "CO<sub>2</sub> estimated for 2016–2020 in the 2023 Energy Baseline Scenario for Gozo [6] (118,333–153,997 t a "
           "year; electricity, transport on the island, ferries, heating and cooling), as in Claim Check 107, and as a "
           "cross-check Malta’s 2024 inventory total scaled by Gozo’s population share (157,634 t CO<sub>2</sub>e [17]), as "
           "in Claim Check 031."))
S.append(P("<b>Sequestration rates.</b> Three cases from the literature, each verified in Crossref: <i>low</i>, 0.92 t "
           "CO<sub>2</sub> per hectare a year, the lower end of tree-biomass gains in plantations of native holm and cork oak "
           "in Spain [8]; <i>central</i>, 3.62 t, the 35-year gain in trees and soil in the Yatir Aleppo pine forest in "
           "Israel [7]; <i>high</i>, 7.6 t, a global review’s rate for planted pine in dry temperate climates over the "
           "first 20 years [9]."))
S.append(P("<b>Land and water.</b> Gozo’s land cover from CORINE Land Cover 2018 [18]; land areas from the European "
           "Commission (Gozo 67 km² [20]) and Eurostat (Gozo and Comino 68 km² [17]); Malta’s forest area, forest-land "
           "removals and water exploitation index from Eurostat [17]; Natura 2000 sites from the EEA [23]; rainfall from "
           "NASA POWER [19]; survival and water use from field and review studies [11–13]."))
S.append(P("<b>Grades.</b> A experiment; B observational study with a control; C review, guidance or official statistics; "
           "D assertion. Our arithmetic gives ceilings, not forecasts. Code: <i>tools/cc-092-report/calc.py</i>; every "
           "figure in <i>data/cc-092/checks.csv</i>."))

# ================================================================== 3
S.append(CondPageBreak(60 * mm))
S.append(SectionHeading(3, "How new forests store carbon"))
S.append(P("A new forest takes CO<sub>2</sub> from the air as its trees grow and stores the carbon in wood and roots "
           "and in the soil [7, 9]. The rate varies with climate, site, species and management [9], and with what the land "
           "held before: in the Yatir forest, half the measured gain was in the soil [7], while native oaks planted on "
           "former cropland in Spain gained carbon in their wood but not in the soil [8]. The review rates used here count "
           "tree biomass only [9]. Trees must also survive: in an arid Spanish trial, 30–58% of planted pines were alive "
           "after 20 years [12]. Figure 1 sets the measured rates against what Gozo would need: to offset its energy "
           "CO<sub>2</sub> on its own 6,700 ha, every hectare would have to store 17.7–23.0 t a year."))
S.append(fig(FIG / "fig1_rates.png"))
S.append(P("Figure 1. Carbon stored by new forests in Mediterranean and dry climates (t CO<sub>2</sub> per hectare a year), "
           "and the rate every hectare of Gozo would need to offset its 2016–2020 energy CO<sub>2</sub>. Bars: the reported "
           "range [8] or the 95% interval [9].", cap))

# ================================================================== 4
S.append(CondPageBreak(80 * mm))
S.append(SectionHeading(4, "What the studies found"))
S.append(std_table([
    [C("Study", cellh), C("Design and place", cellh), C("Finding used here", cellh), C("Grade", cellh)],
    [C("Grünzweig et al. 2007 [7]"), C("Aleppo pine planted on grazed shrubland, Yatir, Israel; 35 years; compared with "
                                       "the shrubland. Not irrigated."),
     C("Ecosystem carbon rose by 99 g C/m² a year (3.62 t CO<sub>2</sub>/ha), half of it in soil."), grade_tag("B")],
    [C("Renna et al. 2024 [8]"), C("Native holm and cork oak on former cropland, Extremadura, Spain; plots 11–24 years "
                                   "old against unplanted controls."),
     C("Tree biomass 25–75 g C/m² a year (0.92–2.75 t CO<sub>2</sub>/ha); soil carbon not higher, so total carbon was "
       "not significantly higher; may take decades to become a sink."), grade_tag("B")],
    [C("Bernal et al. 2018 [9]"), C("Global synthesis of more than 335 studies and reports; plantation growth by species and climate."),
     C("Planted forests, dry temperate climates, first 20 years: oak 5.3, other conifers 6.4, pine 7.6 t CO<sub>2</sub>/ha "
       "a year (biomass only)."), grade_tag("C")],
    [C("Hoogmoed et al. 2012 [10]"), C("Meta-analysis of pasture afforestation in Mediterranean climates."),
     C("No substantial change in soil carbon across three decades."), grade_tag("C")],
    [C("Rotenberg and Yakir 2010 [14]"), C("Nine-year field study at the forests’ dry timberline."),
     C("Forests where 200–600 mm of rain falls keep sequestering, but need several decades of carbon gain to balance "
       "the warming from their darker surface."), grade_tag("B")],
    [C("Oliet et al. 2023 [12]"), C("Field experiment, Aleppo pine, arid south-eastern Spain, 20 years."),
     C("Survival 57.5% with mesh shelters, 46% unprotected, 29.5% in tube shelters."), grade_tag("A")],
    [C("Maestre and Cortina 2004 [11]"), C("Review of Aleppo pine plantations in semi-arid Mediterranean areas."),
     C("Higher water use, often more runoff and soil loss than shrubland, mostly negative effects on native vegetation."),
     grade_tag("C")],
    [C("Jackson et al. 2005 [13]"), C("Synthesis of more than 600 observations, with modelling."),
     C("Plantations cut stream flow by 52% (227 mm a year) on average."), grade_tag("C")],
    [C("Veldman et al. 2015 [16]"), C("Perspective on tree planting in open ecosystems."),
     C("Planting forest on grasslands and open woodlands harms biodiversity and ecosystem services."), grade_tag("C")],
], [31 * mm, 50 * mm, 77 * mm, 12 * mm]))
S.append(P("No measurement of afforestation carbon in Malta or Gozo was found (Crossref searches, 10 October 2026). "
           "The rates come from Spain, Israel and global syntheses; Gozo’s rainfall, about 570 mm a year in a reanalysis "
           "[19], is higher than Yatir’s (about 300 mm [15]).", cap))

# ================================================================== 5
S.append(CondPageBreak(90 * mm))
S.append(SectionHeading(5, "Where the science disagrees"))
S.append(contested(
    "Does afforestation in dry Mediterranean climates add soil carbon?", "UNSETTLED", AMBER,
    "At Yatir, soil organic carbon rose by 50 g C/m² a year over 35 years after pine was planted on grazed shrubland, "
    "about half of the forest’s total gain [7].",
    "Native oaks planted on former cropland in Spain added no soil carbon after up to 24 years [8]; a meta-analysis of "
    "pasture afforestation in Mediterranean climates found no substantial change across three decades [10].",
    "Former land use (grazed shrubland against cropland or pasture), species, age and soils differ. For Gozo we let the "
    "central case keep Yatir’s soil gain and the low case have none. Either way the forest area needed is several times "
    "Gozo’s size.",
    label_a="EVIDENCE OF A SOIL GAIN", label_b="EVIDENCE OF LITTLE OR NO SOIL GAIN"))
S.append(contested(
    "How soon does a new dry-land forest cool the climate?", "DEPENDS ON SCALE", AMBER,
    "In a climate model, semi-arid afforestation on the scale of about 200 million hectares changed rainfall and would "
    "outweigh its surface warming within about six years [15].",
    "Measured over nine years at the forests’ dry timberline, the darker forest surface warms the climate enough that "
    "several decades of carbon gain are needed to balance it [14].",
    "One is a field study at the dry edge of forests, the other a model of a continent-sized planting. For a small island and a "
    "2040 deadline, the field result is the closer guide: carbon accounting alone would overstate what young trees do "
    "for the climate by 2040. We do not adjust our figures for this.",
    label_a="FASTER BENEFIT", label_b="SLOWER BENEFIT"))
S.append(contested(
    "Can new trees establish on Gozo without irrigation?", "POSSIBLE, WITH LOSSES", AMBER,
    "Yatir grew without irrigation on about 300 mm of rain [7, 15], and dry forests keep sequestering where 200–600 mm "
    "falls [14]; Gozo receives about 570 mm a year (reanalysis) [19].",
    "In arid Spain 42–70% of planted pines died within 20 years [12]; plantations use more water and reduce stream flow "
    "[11, 13]; Eurostat records Malta in permanent water scarcity, with a water exploitation index of 30% in 2023 "
    "(above 20% signals scarcity) [17].",
    "Rainfall is not the same as water available to a seedling: soil depth, drought years and planting technique "
    "decide survival. Trees can grow on Gozo, but survival and water use limit how much planting adds, and the PN "
    "does not say how plantations would be watered.",
    label_a="EVIDENCE TREES CAN ESTABLISH", label_b="EVIDENCE OF LIMITS"))

# ================================================================== 6
S.append(CondPageBreak(95 * mm))
S.append(SectionHeading(6, "The arithmetic"))
S.append(fig(FIG / "fig2_forest_needed.png"))
S.append(P("Figure 2. New forest needed to offset Gozo’s 2016–2020 energy CO<sub>2</sub> [6] by trees alone, as a "
           "multiple of Gozo’s 67 km² [20], at the three rates.", cap))
S.append(std_table([
    [C("Rate (t CO<sub>2</sub>/ha a year)", cellh), C("Forest needed for 118,333 t (2020)", cellh),
     C("Forest needed for 153,997 t (2019)", cellh), C("Multiple of Gozo", cellh)],
    [C("Low, 0.92 (native oaks [8])"), C("1,291 km²"), C("1,680 km²"), C("19.3–25.1×")],
    [C("<b>Central, 3.62 (Yatir [7])</b>"), C("<b>326 km²</b>"), C("<b>425 km²</b>"), C("<b>4.9–6.3×</b>")],
    [C("High, 7.6 (planted pine [9])"), C("156 km²"), C("203 km²"), C("2.3–3.0×")],
], [52 * mm, 42 * mm, 42 * mm, 34 * mm]))
S.append(P("With Malta’s 2024 inventory scaled by Gozo’s population share (157,634 t CO<sub>2</sub>e [17]) the central "
           "case needs 435 km², 6.5 times Gozo. Full results: <i>data/cc-092/afforestation_offset.csv</i>.", cap))
S.append(fig(FIG / "fig3_land_offset.png"))
S.append(P("Figure 3. Gozo’s land in CORINE Land Cover 2018 [18] (6,586 ha mapped), and the share of its 2016–2020 "
           "energy CO<sub>2</sub> that new forest on that land could offset. These are ceilings: they assume every "
           "hectare is planted and reaches the rate.", cap))
S.append(callout([P("THE ARITHMETIC", tag),
                  P("In CORINE, Gozo’s only land that is neither built on nor farmed is about 1,270 ha (19%): class 323, "
                    "sclerophyllous vegetation, which includes garrigue and maquis [18], and class 333, sparsely vegetated "
                    "areas. Planted in full at Yatir’s rate, it would store 1,265 ha × 3.62 t = about 4,600 t CO<sub>2</sub> "
                    "a year, 3.0–3.9% of Gozo’s energy CO<sub>2</sub> (0.8–8.1% across the three rates). Planting all "
                    "farmland too (5,066 ha) would reach 12–16%; covering all of Gozo, 16–21%. Malta’s whole forest is "
                    "470 ha (FAO definition, 2025) [17], and in 2024 Malta’s forest land removed 0.16 kt CO<sub>2</sub>e "
                    "[17], 0.1% of Gozo’s 2019 energy CO<sub>2</sub>.", small)], bg=BLUE_PALE, bar=BLUE))
S.append(Spacer(1, 2 * mm))
S.append(P("What this means for the pledge", h2))
for t in ["• <b>Afforestation can be a small part of a net-zero Gozo, not the means to it.</b> The PN’s text relies on "
          "cutting emissions first (solar, electric vehicles, efficient buildings) and lists afforestation among several "
          "measures [1]; that is consistent with this arithmetic. The “through afforestation” version is a news "
          "summary [4].",
          "• <b>The planting effort would be large even for a few per cent.</b> Stocking the semi-natural land at Yatir’s "
          "300 trees per hectare [7], allowing for 46% survival after 20 years [12], means about 825,000 trees, about "
          "52 years at the pace at which government entities planted trees across Malta and Gozo in 2022–2025 (about "
          "60,000 trees [21]).",
          "• <b>That land is not empty.</b> Class 323 includes garrigue, which the PN’s own Malta Nature Network (item 25) "
          "would protect [2], and 36% of Gozo’s semi-natural land (453 ha) lies inside Natura 2000 sites [23]. Planting "
          "trees in open habitats can harm biodiversity [16], and Aleppo pine plantations have often suppressed native "
          "vegetation [11]."]:
    S.append(P(t, bul))

# ================================================================== 7
S.append(CondPageBreak(95 * mm))
S.append(SectionHeading(7, "Testing the pledge"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> Every unit of Gozo’s emissions “reduced or offset” by 2040, with afforestation among the initiatives"),
     C("PN [1]"),
     C("The PN gives afforestation no share. Trees alone would need 4.9–6.3 times Gozo’s area at a measured rate "
       "(2.3–25 times across rates); planting all of Gozo’s semi-natural land would offset about 3–4% (1–8%) of its "
       "energy CO<sub>2</sub> [6–9, 18]."), verd("A SMALL PART AT MOST", AMBER)],
    [C("<b>B.</b> “More afforestation and open spaces in both Malta and Gozo”"), C("PN [2]"),
     C("No area, number of trees, species, sites or date, so delivery cannot be checked. CORINE maps no forest on Gozo; "
       "Malta’s whole forest is 470 ha [17, 18]."), verd("NOT MEASURABLE (PLEDGE)", GREY)],
    [C("<b>C.</b> Gozo net zero “through afforestation”"), C("MaltaToday [4]"),
     C("Not the PN’s words: the programme lists afforestation among many measures [1]. Not rated."),
     verd("HEADLINE WORDING, NOT RATED", GREY)],
    [C("<b>D.</b> A national indigenous-tree strategy"), C("MaltaToday [5 ◆]"),
     C("Not in any of the 16 chapters (web and PDF, searched 10 Oct 2026). Nearest: local farm varieties and breeds "
       "with a gene bank and nursery (Agrikoltura 31) [3]; tree planting and afforestation against heat and flooding "
       "(Ambjent 20) [2]."), verd("NOT IN THE PROGRAMME", GREY)],
    [C("<b>E.</b> Water and land limits on planting (our check)"), C("Not claimed"),
     C("Malta in permanent water scarcity (WEI+ 30% in 2023) [17]; 30–58% 20-year survival in arid Spain [12]; the "
       "only land neither built on nor farmed is mostly CORINE class 323, which includes garrigue and maquis [18]; 36% of "
       "it lies in Natura 2000 sites [23], and the PN’s item 25 lists garrigue among the habitats to protect [2]."),
     verd("CONTEXT", AMBER)],
], [44 * mm, 20 * mm, 75 * mm, 31 * mm], valign="MIDDLE"))

# ================================================================== 8
S += [Spacer(1, 5 * mm), CondPageBreak(60 * mm), SectionHeading(8, "Pledge label and requests for evidence"),
      verdict_box("Not measurable", "As of 10 October 2026. Afforestation is listed without area, species, carbon rate or "
                  "date; trees on Gozo could offset only a few per cent of its emissions."), Spacer(1, 3 * mm)]
S.append(P("<b>Why.</b> The PN lists afforestation as one of the ways Gozo’s emissions would be “reduced or offset” by "
           "2040 and promises “more afforestation” in Malta and Gozo, but sets no quantity, place or date against which "
           "delivery could be checked. That is the definition of <i>Not measurable</i> (Appendix A). The arithmetic adds "
           "context, not a verdict: whatever is planted, trees on Gozo can carry only a small share of a net-zero target. "
           "The indigenous-tree strategy reported in the press is not in the programme, so it is not rated."))
S.append(P("<b>What this label does not say.</b> It does not say the pledge is false, that afforestation is a bad idea, "
           "or that anyone acted in bad faith. A checkable version would read: <i>“By [year] we will plant [area] ha of "
           "[species] at [sites] on Gozo, expected to store [X] t CO<sub>2</sub> a year by 2040, within a net-zero "
           "pathway that cuts emissions to [Y] t.”</i>"))
S.append(CondPageBreak(45 * mm))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "From the PN: the share of Gozo’s emissions that afforestation is expected to offset by 2040, and the rate per "
    "hectare assumed.",
    "From the PN: the area, sites and species to be planted on Gozo, and whether garrigue and other open habitats would "
    "be excluded.",
    "From the PN: whether it proposes a national indigenous-tree strategy, and where it is set out.",
    "From the PN: how new plantations would be watered and their survival monitored.",
]))
S += [Spacer(1, 3 * mm),
      callout([P("RIGHT OF REPLY", tag),
               P("Under the project’s rules a pledge labelled Not measurable is offered to its author for reply before any "
                 "wider circulation. The maintainer handles the right of reply to the Partit Nazzjonalista; any response "
                 "will be appended and the label revisited.", small)], bg=AMBER_PALE, bar=AMBER)]

# ================================================================== 9
S += [Spacer(1, 5 * mm), CondPageBreak(50 * mm), SectionHeading(9, "Limitations")]
for l in ["No measurement of afforestation carbon in Malta was found. The three rates come from Spain, Israel and a "
          "global review; Gozo’s soils, species and rainfall differ, and a review’s “dry temperate” class is not a "
          "Mediterranean-only figure [9].",
          "Gozo’s emissions come from a study prepared for the EU islands secretariat (energy only; not official "
          "statistics) and from a population share of Malta’s inventory, which is not Gozo data [6, 17].",
          "CORINE maps land in units of at least 25 ha, so small woods, tree rows and valley vegetation are missed; "
          "polygons were assigned to Gozo by their extent. CORINE maps 6,586 ha on Gozo, against 67 km² from the "
          "Commission [20] and 68 km² for Gozo and Comino from Eurostat [17].",
          "The offsets are ceilings: they assume every hectare is planted and reaches the rate, before losses to drought, "
          "fire or failed planting. The Natura 2000 overlap is measured on generalised CORINE polygons and is approximate.",
          "Rainfall comes from a reanalysis with grid cells of about 50 km and is approximate [19].",
          "MaltaToday’s breakdown [5] could not be read; its indigenous-tree wording is known only from a search "
          "engine’s summary. The translations of the programme are ours."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 4 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Partit Nazzjonalista (May 2026). <i>Nifs Ġdid</i>: Programm Elettorali 2026, chapter Għawdex, item 46 "
          "(web page; PDF 10-Ghawdex.pdf, p. 16). Read 10 Oct 2026.", "https://pn.org.mt/nifsgdid/ghawdex/"),
    ("2", "Partit Nazzjonalista (May 2026). <i>Nifs Ġdid</i>, chapter Ambjent, items 01, 20 and 25 (PDF "
          "13-Ambjent.pdf, pp. 8, 12, 13). Read 10 Oct 2026.", "https://pn.org.mt/nifsgdid/ambjent/"),
    ("3", "Partit Nazzjonalista (May 2026). <i>Nifs Ġdid</i>, chapter Agrikoltura u Sajd, item 31 (PDF "
          "14-Agrikoltura.pdf, p. 13). Read 10 Oct 2026.", "https://pn.org.mt/nifsgdid/agrikoltura-u-sajd/"),
    ("4", "MaltaToday (May 2026). PN approves its electoral manifesto. Read via the Internet Archive for Claim Check "
          "107 (5 Oct 2026).", "https://www.maltatoday.com.mt/news/election-2026/141891/pn_approves_its_electoral_manifesto"),
    ("5", "MaltaToday (May 2026). PN published its manifesto: Here is a breakdown. Not readable (403); known from a "
          "search engine’s summary ◆.",
     "https://www.maltatoday.com.mt/news/election-2026/142040/pn_published_its_manifesto_here_is_a_breakdown"),
    ("6", "Vaz L., Rodrigues de Almeida J. (2023). <i>Clean energy for EU islands: Energy Baseline Scenario for Gozo</i>. "
          "Clean energy for EU islands secretariat, 25 January 2023. Table 16, p. 25. (Read in full.)",
     "https://clean-energy-islands.ec.europa.eu/system/files/2025-06/REPORT_TechnicalAssistance_Gozo_20230223.pdf"),
    ("7", "Grünzweig J.M., Gelfand I., Fried Y., Yakir D. (2007). Biogeochemical factors contributing to enhanced "
          "carbon storage following afforestation of a semi-arid shrubland. <i>Biogeosciences</i> 4(5):891–904. "
          "(Full text.)", "https://doi.org/10.5194/bg-4-891-2007"),
    ("8", "Renna V., Martín-Gallego P., Julián F., Six J., Cardinael R., Laub M. (2024). Initial soil carbon losses may "
          "offset decades of biomass carbon accumulation in Mediterranean afforestation. <i>Geoderma Regional</i> "
          "36:e00768. (Abstract.)", "https://doi.org/10.1016/j.geodrs.2024.e00768"),
    ("9", "Bernal B., Murray L.T., Pearson T.R.H. (2018). Global carbon dioxide removal rates from forest landscape "
          "restoration activities. <i>Carbon Balance and Management</i> 13:22. Table 1. (Full text.)",
     "https://doi.org/10.1186/s13021-018-0110-8"),
    ("10", "Hoogmoed M., Cunningham S.C., Thomson J.R., Baker P.J., Beringer J., Cavagnaro T.R. (2012). Does "
           "afforestation of pastures increase sequestration of soil carbon in Mediterranean climates? <i>Agriculture, "
           "Ecosystems &amp; Environment</i> 159:176–183. (Abstract.)", "https://doi.org/10.1016/j.agee.2012.07.011"),
    ("11", "Maestre F.T., Cortina J. (2004). Are <i>Pinus halepensis</i> plantations useful as a restoration tool in "
           "semiarid Mediterranean areas? <i>Forest Ecology and Management</i> 198(1–3):303–317. (Abstract.)",
     "https://doi.org/10.1016/j.foreco.2004.05.040"),
    ("12", "Oliet J.A., Planelles R., Artero F., Jacobs D.F. (2023). Mesh-shelters provide more effective long-term "
           "protection than tube-shelters or mulching for restoration of <i>Pinus halepensis</i> in a Mediterranean arid "
           "ecosystem. <i>Frontiers in Forests and Global Change</i> 5:1092703. (Open access.)",
     "https://doi.org/10.3389/ffgc.2022.1092703"),
    ("13", "Jackson R.B., Jobbágy E.G., Avissar R., et al. (2005). Trading water for carbon with biological carbon "
           "sequestration. <i>Science</i> 310(5756):1944–1947. (Abstract.)", "https://doi.org/10.1126/science.1119282"),
    ("14", "Rotenberg E., Yakir D. (2010). Contribution of semi-arid forests to the climate system. <i>Science</i> "
           "327(5964):451–454. (Abstract.)", "https://doi.org/10.1126/science.1179998"),
    ("15", "Yosef G., Walko R., Avisar R., Tatarinov F., Rotenberg E., Yakir D. (2018). Large-scale semi-arid "
           "afforestation can enhance precipitation and carbon sequestration potential. <i>Scientific Reports</i> 8:996. "
           "(Abstract.)", "https://doi.org/10.1038/s41598-018-19265-6"),
    ("16", "Veldman J.W., Overbeck G.E., Negreiros D., et al. (2015). Where tree planting and forest expansion are bad for "
           "biodiversity and ecosystem services. <i>BioScience</i> 65(10):1011–1018. (Abstract.)",
     "https://doi.org/10.1093/biosci/biv118"),
    ("17", "Eurostat. env_air_gge, demo_r_pjangrp3, reg_area3, for_area and sdg_06_60 (with its metadata: thresholds and "
           "the note on Malta’s permanent water scarcity). Retrieved 10 Oct 2026.",
     "https://ec.europa.eu/eurostat/cache/metadata/en/sdg_06_60_esmsip2.htm"),
    ("18", "European Environment Agency / Copernicus Land Monitoring Service. CORINE Land Cover 2018 (map service "
           "CLC2018_WM), retrieved 10 Oct 2026; nomenclature guidelines, class 3.2.3.",
     "https://land.copernicus.eu/content/corine-land-cover-nomenclature-guidelines/html/index-clc-323.html"),
    ("19", "NASA Langley Research Center. POWER Climatology API (MERRA-2), 1991–2020, Gozo and Yatir. Retrieved 10 Oct 2026.",
     "https://power.larc.nasa.gov/"),
    ("20", "European Commission. Clean energy for EU islands: Malta (Gozo 67 km²). Read 10 Oct 2026.",
     "https://clean-energy-islands.ec.europa.eu/countries/malta"),
    ("21", "Parliament of Malta. PQ 34270, written answer of 18 Feb 2026 (about 60,000 trees planted to end 2025), as "
           "recorded in Claim Check 010.", "https://www.parlament.mt/media/137706/20260218_435o_par.pdf"),
    ("22", "IFES ElectionGuide. Malta: Maltese House of Representatives 2026 General (held 30 May 2026). Accessed "
           "5 Oct 2026.", "https://electionguide.org/elections/id/5161/"),
    ("23", "European Environment Agency. Natura 2000 sites, map service Natura2000Sites (Habitats and Birds Directive "
           "sites, Malta), retrieved 10 Oct 2026; overlap with CORINE 2018 in data/cc-092/natura2000_overlap.csv.",
     "https://bio.discomap.eea.europa.eu/arcgis/rest/services/ProtectedSites/Natura2000Sites/MapServer"),
    ("24", "Miżien. Code and outputs: tools/cc-092-report/; data/cc-092/ (checks.csv, afforestation_offset.csv, "
           "natura2000_overlap.csv, pn_programme_search.csv).", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or official "
                "statistics · D assertion or anecdote. ◆ marks a source known only second-hand. Our arithmetic gives "
                "ceilings, not forecasts.", pledges=True)
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "10 Oct 2026", "First issue. Pledge label Not measurable as of 10 October 2026; pending "
                                          "right of reply from the Partit Nazzjonalista. Complements Claim Check 107 "
                                          "(the net-zero plan) with the afforestation arithmetic, Gozo’s land cover, "
                                          "water limits and the search for an indigenous-tree strategy.")])

build_report(Report(
    number="092", out=str(FIG / "report.pdf"), kicker="Election pledges, computed",
    title_lines=["Could trees make", "Gozo net zero?"],
    subtitle_lines=["The afforestation in the Nationalist Party’s 2026 pledge,", "tested on measured forests and Gozo’s land"],
    quote_lines=["“By 2040 Gozo becomes a Net-Zero Island … where", "every unit of emissions generated is reduced or",
                 "offset”, with “afforestation” among the initiatives."], quote_size=14,
    attribution="Partit Nazzjonalista, programme Nifs Ġdid (May 2026), chapter Għawdex, item 46 (our translation).",
    context="News summaries said “through afforestation” and reported an indigenous-tree strategy; neither is the PN’s text.",
    verdict="Not measurable", verdict_note="As of 10 Oct 2026: no area, species, rate or date for afforestation",
    footer_lines=["Version 1.0  ·  10 October 2026", "Status:",
                  "Prepared from public sources and open data. No site visits.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Afforestation and a net-zero Gozo – PN programme 2026", version="1.0", date="10 October 2026",
    pdf_title="Could trees make Gozo net zero? Claim Check 092",
    pdf_subject="Tests the afforestation in the Nationalist Party's 2026 pledge of a net-zero Gozo, and its reported indigenous-tree strategy",
    story=S))
