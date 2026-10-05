"""Claim Check 011 report. Run green_access.py, gozo_calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []

# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("Before the general election of 30 May 2026 both main parties made an environmental pledge that can be "
        "computed. <b>Labour</b> (now in government) promised that nobody would live more than <b>ten minutes’ "
        "walk from an open or green space</b>. The <b>Nationalist Party</b> promised a plan for <b>Gozo to become a "
        "Net-Zero Island by 2040</b>, with afforestation among the measures. We tested whether either pledge has a "
        "baseline, a definition and a counting method that would let anyone check it.", lead)]
S.append(key_points([
    ("Labour’s pledge may already be met, or be far off. It depends on the definition.",
     "If any open or green space counts, about 99.9% of residents already live within 800 m. If only public parks "
     "of at least 0.5 ha count, 55–68% do, leaving some 170,000–240,000 people outside."),
    ("The manifesto gives no definition, baseline or date.",
     "Without them the pledge cannot be checked, and could be declared met without any new green space."),
    ("The PN pledge is a plan to make a plan, with no Gozo emissions inventory.",
     "No official greenhouse-gas inventory exists for Gozo, and the programme does not say what counts (for "
     "example, electricity imported from Malta, ferries)."),
    ("Afforestation alone could not do it.",
     "Offsetting Gozo’s estimated emissions with new forest would need about 1.5 to 8.5 times Gozo’s land "
     "area. News reports summarised the pledge as “net zero through afforestation”; the programme lists "
     "afforestation as one of several measures."),
    ("Verdict: not substantiated, for both.",
     "Neither pledge is wrong; neither is stated in a way that can be measured."),
]))
S += [Spacer(1, 4 * mm), VerdictMeter(2), Spacer(1, 3 * mm),
      tiles([("99.9%", GREEN, "Residents within 800 m of any green or open space (straight line)"),
             ("55%", ORANGE, "Within an 800 m walk of a public park of at least 0.5 ha"),
             ("~157 kt", GREY, "Our estimate of Gozo’s yearly emissions (no official figure)"),
             ("6.5×", RED, "Gozo’s area needed as new forest to offset them (measured rate)")]),
      Spacer(1, 4 * mm),
      up_down("A published definition of “open or green space”, a baseline map and a target year from the "
              "government; a Gozo emissions inventory with a stated boundary and a costed 2040 pathway from the PN.",
              "A government statement that the pledge is met using a broad definition without new space being "
              "created; a net-zero claim for Gozo that relies on unspecified offsets."),
      Spacer(1, 5 * mm)]
S += toc([("1", "The pledges and what we could verify"), ("2", "Method"), ("3", "Why definitions decide the answer"),
          ("4", "Labour: ten minutes from green space"), ("5", "PN: a net-zero Gozo"), ("6", "Testing the pledges"),
          ("7", "Verdict and requests for evidence"), ("8", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The pledges and what we could verify"))
S.append(P("Our candidate record took both pledges from MaltaToday summaries [3, 4]. We then found the parties’ own "
           "texts [1, 2], both in Maltese. The translations are ours; the original wording is quoted so readers can "
           "check them. The two texts differ from the news summaries in ways that matter: Labour’s says <i>open or "
           "green</i> space, and the PN’s sets a 2040 date and lists afforestation as one measure among many."))
S.append(std_table([
    [C("Source", cellh), C("What it says (our translation)", cellh), C("Our access", cellh), C("Status", cellh)],
    [C("<b>Partit Laburista</b>, manifesto <i>Int Malta</i>, 2026, priority 19, p. 17 [1]"),
     C("“Kull persuna f’pajjiżna ma tkunx aktar minn għaxar minuti mixi ’l bogħod minn "
       "spazju miftuħ jew aħdar.” <i>Every person in our country will be no more than ten minutes’ "
       "walk from an open or green space.</i> On p. 21 the indicator is “access to open spaces and the "
       "availability of recreational zones”, to be met through green spaces within ten minutes’ walk and "
       "investment in Manoel Island, White Rocks, Fort Campbell and other parks."),
     C("Read: pp. 17 and 21 of the 268-page PDF (hash recorded)."), C("<b>Pledge 1</b>")],
    [C("<b>Partit Nazzjonalista</b>, programme <i>Nifs Ġdid</i>, chapter Għawdex [2]"),
     C("“Infasslu pjan ċar u realistiku biex sal-2040, Għawdex isir Net-Zero Island…” "
       "<i>We will draw up a clear and realistic plan so that by 2040 Gozo becomes a Net-Zero Island, the first in "
       "the Mediterranean where every unit of emissions is reduced or offset</i>, through solar panels, electric "
       "cars, taxis and vans, building efficiency, ecological restoration on land and at sea, afforestation, and "
       "water and soil conservation, among others."),
     C("Read in full in a browser."), C("<b>Pledge 2</b>")],
    [C("<b>MaltaToday</b>, May 2026 [3, 4]"),
     C("Labour: “every citizen is within a 10-minute walk of a green space”. PN: Gozo “would become a "
       "net-zero island through afforestation”."), C("Read (Wayback copies)."), C("Summaries")],
], [36 * mm, 82 * mm, 32 * mm, 20 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("FAIRNESS NOTE", tag),
               P("Labour won the general election of 30 May 2026 [13], so its pledge is now a government commitment; the PN’s "
                 "is an opposition proposal. We hold both to the same standard. Both goals are legitimate: nearby "
                 "green space is associated with better health [7], and island decarbonisation is EU policy. The PN "
                 "also proposes a Parks Act to give “park” and “green space” a legal definition, "
                 "which would address part of the problem identified here. This check is about whether the pledges "
                 "can be measured.", small)], bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Question.</b> Does each pledge have a definition, baseline and counting method that would allow it to be "
           "checked, and is it physically plausible as stated?"))
S.append(P("<b>Green-space access.</b> We overlaid WorldPop’s 2025 population grid (100 m cells, constrained to "
           "built-up areas) with OpenStreetMap green and open spaces downloaded on 2 October 2026. For six definitions, "
           "from strict (public parks of at least 1 ha) to broad (any green or open space, including squares and "
           "beaches), we computed the share of residents within 300 m, 615 m and 800 m in a straight line. A "
           "ten-minute walk at 4.8 km/h is 800 m along streets; 615 m in a straight line allows for typical detours "
           "(factor 1.3). 300 m is the WHO Europe indicator distance [5]. Code: <i>tools/cc-011-report/green_access.py</i>."))
S.append(P("<b>Gozo arithmetic.</b> Gozo’s emissions were estimated as population (41,253 on 1 January 2025 [9]) "
           "times national emissions per person (2.5, 3.81 and 5.0 t). Forest sequestration used a measured rate from "
           "a semi-arid Aleppo pine afforestation on rendzina over limestone (about 3.6 t CO<sub>2</sub>/ha/yr over 35 "
           "years [6]) and an optimistic 10 t. Code: <i>tools/cc-011-report/gozo_calc.py</i>."))
S.append(P("<b>Grades.</b> The afforestation inventory is B; WHO guidance, meta-analyses of observational studies and "
           "official statistics are C; our own analyses are screening estimates and are labelled as such."))

# ================================================================== 3
S.append(CondPageBreak(90 * mm))
S.append(SectionHeading(3, "Why definitions decide the answer"))
S.append(P("Both pledges rest on a word that is not defined. For Labour it is <i>open or green space</i>: does a "
           "paved square count, a strip of roadside grass, a patch of garrigue, a beach? For the PN it is "
           "<i>net zero</i>: which emissions count (Gozo draws its electricity through cables from Malta’s grid, and ferries "
           "cross between the islands; general knowledge, not sourced here), and what counts as an offset? The research on green "
           "space and health uses many different access measures and they do not give the same answers [5, 8]. WHO "
           "Europe proposes a minimum size (0.5 ha, with 1 ha as an additional indicator) and a short distance "
           "(300 m) precisely because tiny or distant spaces are used less [5]."))

# ================================================================== 4
S.append(PageBreak())
S.append(SectionHeading(4, "Labour: ten minutes from green space"))
S.append(fig(FIG / "fig1_green_access.png"))
S.append(P("Figure 1. Share of Malta’s residents within each distance of a green or open space, under six "
           "definitions. Straight-line distances overstate access; OpenStreetMap may miss or misclassify spaces. "
           "Screening estimate, not a network analysis.", cap))
S.append(std_table([
    [C("Definition", cellh), C("Within 800 m walk (615 m line)", cellh), C("Residents outside", cellh),
     C("Within 300 m (WHO)", cellh)],
    [C("Any open or green space, incl. squares and beaches"), C("99.7%"), C("about 1,400"), C("95%")],
    [C("Any green space, incl. scrub, garrigue, grass verges"), C("99.6%"), C("about 1,900"), C("95%")],
    [C("Public parks and gardens, any size"), C("92%"), C("about 43,000"), C("76%")],
    [C("Green space of at least 0.5 ha"), C("87%"), C("about 72,000"), C("51%")],
    [C("<b>Public parks and gardens of at least 0.5 ha</b>"), C("<b>55%</b>"), C("<b>about 243,000</b>"), C("24%")],
    [C("Public parks and gardens of at least 1 ha"), C("33%"), C("about 365,000"), C("13%")],
], [74 * mm, 36 * mm, 32 * mm, 28 * mm]))
S.append(P("Population base: WorldPop 2025, 542,820 residents (lower than NSO’s 574,250 because the grid is a "
           "model). Full results in <i>data/cc-011/green_access_results.csv</i>.", cap))
S.append(P("What this means for the pledge", h2))
for t in ["• <b>Read broadly, the pledge is already almost met.</b> On the manifesto’s own words (“open or "
          "green”), fewer than 2,000 modelled residents are more than a ten-minute walk from some qualifying "
          "space. The pledge could be declared fulfilled without creating anything.",
          "• <b>Read as the WHO-style measure, it is far off.</b> Only about a quarter of residents live within 300 m "
          "of a public park of at least 0.5 ha, and about 55% within a realistic ten-minute walk of one.",
          "• <b>The manifesto’s own examples</b> (Manoel Island, White Rocks, Fort Campbell) are large parks on "
          "the edges of the built-up area, which suggests a stricter reading than “any open space”. That is "
          "our inference; the manifesto does not say."]:
    S.append(P(t, bul))

# ================================================================== 5
S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(5, "PN: a net-zero Gozo"))
S.append(fig(FIG / "fig2_gozo_forest.png"))
S.append(P("Figure 2. New forest needed to offset Gozo’s estimated annual emissions by afforestation alone, under "
           "three emissions estimates and two sequestration rates, compared with Gozo’s land area.", cap))
S.append(callout([P("THE ARITHMETIC", tag),
                  P("Gozo population 41,253 × 3.81 t per person = about 157,000 t CO<sub>2</sub>e a year. A measured "
                    "semi-arid pine afforestation stored about 3.6 t CO<sub>2</sub> per hectare per year [6]. Offsetting "
                    "157,000 t would take about 43,000 ha (434 km²) of new forest: 6.5 times Gozo’s 67 km² "
                    "[10]. Even at an optimistic 10 t/ha/yr it is 157 km², 2.3 times the island. Planting 10% of "
                    "Gozo would offset about 1.5% of its emissions.", small)], bg=BLUE_PALE, bar=BLUE))
S.append(Spacer(1, 3 * mm))
S.append(P("What this means for the pledge", h2))
for t in ["• <b>“Net zero through afforestation”, as reported, is not possible on Gozo.</b> But that is the "
          "news summary [4], not the PN’s text.",
          "• <b>The PN’s text relies on cutting emissions first</b> (solar, electric vehicles, efficient "
          "buildings), with restoration and afforestation as part of the mix. Whether that reaches net zero by 2040 "
          "depends on numbers the programme does not give: a baseline inventory, a boundary (imported electricity, "
          "ferries, tourism), and the role of offsets bought from elsewhere.",
          "• <b>Sequestration in young plantations is slow at first and can be reversed</b> by drought or fire; "
          "the measured rate [6] is a 35-year average on a site with deep groundwater, not a guaranteed yield on "
          "Gozo’s thin soils.",
          "• <b>“The first island in the Mediterranean”</b> was not tested."]:
    S.append(P(t, bul))

# ================================================================== 6
S.append(PageBreak())
S.append(SectionHeading(6, "Testing the pledges"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> Nobody more than ten minutes’ walk from an open or green space"), C("Labour [1]"),
     C("No definition, baseline or year. Broad reading: about 99.7% already within reach. Strict reading: about "
       "55%."), verd("NO BASELINE", ORANGE)],
    [C("<b>B.</b> Delivered through green spaces within ten minutes and parks such as Manoel Island, White Rocks, "
       "Fort Campbell"), C("Labour [1]"),
     C("Named projects are real proposals; their effect on access depends on location. Not modelled here."),
     verd("NOT TESTED", GREY)],
    [C("<b>C.</b> A clear and realistic plan for a Net-Zero Gozo by 2040"), C("PN [2]"),
     C("No Gozo inventory or boundary; no plan published. Cannot be assessed as “realistic”."),
     verd("NO BASELINE", ORANGE)],
    [C("<b>D.</b> Gozo net zero through afforestation (news summary)"), C("MaltaToday [4]"),
     C("Would need 1.5–8.5 times Gozo’s area as new forest. Not the PN’s own wording."),
     verd("NOT POSSIBLE AS REPORTED", RED)],
    [C("<b>E.</b> 40% cut in carbon emissions by 2030 vs 2005 (priority 18)"), C("Labour [1]"),
     C("Same aim as the Climate Action Authority’s; scope not stated. See CC-003."), verd("SEE CC-003", GREY)],
], [46 * mm, 20 * mm, 70 * mm, 34 * mm], valign="MIDDLE"))

# ================================================================== 7
S += [Spacer(1, 6 * mm), SectionHeading(7, "Verdict and requests for evidence"),
      verdict_box("Not substantiated", "Both pledges lack the definition and baseline needed to check them. "
                  "Confidence: moderate. Our access analysis is a screening estimate."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> Labour’s pledge can be read as already achieved or as needing new parks within reach of "
           "about 240,000 people; the manifesto does not say which. The PN’s pledge promises a plan for an "
           "outcome whose starting point and boundary are not defined, and the widely reported version (afforestation) "
           "is physically impossible on Gozo’s land area. A pledge is not a statement of fact, so we do not call "
           "either one false; we rate them <i>Not substantiated</i> because, as worded, neither can be shown to be "
           "achieved or missed."))
S.append(P("<b>What this verdict does not say.</b> It does not say either goal is undesirable, or that either party "
           "acted in bad faith. A checkable version of the Labour pledge would read: <i>“By [year], every resident "
           "will live within 800 m by foot of a public park of at least [size]; today [X]% do (map published).”</i>"))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "From the government: the definition of “open or green space” used for priority 19 (minimum size, public "
    "access, whether squares, beaches and verges count).",
    "From the government: the baseline share of residents within ten minutes, the method (walking network or straight "
    "line) and the target year.",
    "From the government: the scope of the 40% emissions cut in priority 18 (total or effort-sharing emissions).",
    "From the PN: a Gozo emissions inventory, its boundary (imported electricity, inter-island ferries, tourism), and "
    "the share of the 2040 target expected from cuts, from afforestation and from offsets elsewhere.",
    "From the PN: the area to be afforested on Gozo and the species and sequestration rate assumed.",
]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag),
               P("Before wider circulation this draft should be sent to the Partit Laburista (and, as the pledge is now "
                 "a government commitment, the Office of the Prime Minister or the responsible ministry) and to the "
                 "Partit Nazzjonalista, with the same fixed deadline (suggested 14 days). Responses will be appended "
                 "and the verdict revisited.", small)], bg=AMBER_PALE, bar=AMBER)]

# ================================================================== 8
S += [Spacer(1, 6 * mm), SectionHeading(8, "Limitations")]
for l in ["The access analysis uses straight-line distances, a modelled population grid and OpenStreetMap tags, whose "
          "completeness in Malta we did not validate. Private gardens were excluded where tagged as private; some may "
          "remain. Grass verges and road islands are included in the broad definitions. A walking-network analysis "
          "would give lower shares for every definition.",
          "Gozo emissions are estimated from national per-person figures; Gozo’s real profile (less industry, more "
          "tourism and ferry traffic) may differ. The 2.5–5.0 t range is our assumption.",
          "The sequestration rate comes from one well-studied site in Israel; no Maltese measurements were found.",
          "Manifesto translations are ours. The Labour PDF was read at pp. 17 and 21 only; other chapters may add detail.",
          "We read the green-space health literature [7, 8] as abstracts or metadata only; it is context for why the "
          "pledges matter, not evidence for the verdict."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Partit Laburista (2026). <i>Int Malta</i>: Manifest Elettorali 2026. Priorities list p. 17; indicators "
          "p. 21. SHA-256 466a60f9… recorded in literature/CC-011/references.bib.",
     "https://partitlaburista.org/wp-content/uploads/2026/08/Manifest_Elettorali_INT_MALTA_2026.pdf"),
    ("2", "Partit Nazzjonalista (2026). <i>Nifs Ġdid</i>: Programm Elettorali, chapter Għawdex; chapter "
          "Ambjent (Parks Act).", "https://pn.org.mt/en/nifsgdid/ghawdex/"),
    ("3", "MaltaToday (May 2026). Labour publishes its manifesto: here is a breakdown.",
     "https://www.maltatoday.com.mt/news/election-2026/141840/labour_publishes_its_manifesto_here_is_a_breakdown"),
    ("4", "MaltaToday (May 2026). PN approves its electoral manifesto.",
     "https://www.maltatoday.com.mt/news/election-2026/141891/pn_approves_its_electoral_manifesto"),
    ("5", "WHO Regional Office for Europe (2016). <i>Urban green spaces and health: a review of evidence</i>. "
          "Copenhagen. (Indicator section read.)",
     "https://www.who.int/europe/publications/i/item/WHO-EURO-2016-3352-43111-60341"),
    ("6", "Grünzweig J.M., Gelfand I., Fried Y., Yakir D. (2007). Biogeochemical factors contributing to enhanced "
          "carbon storage following afforestation of a semi-arid shrubland. <i>Biogeosciences</i> 4(5):891–904. "
          "doi:10.5194/bg-4-891-2007. (Full text read; open access.)", "https://doi.org/10.5194/bg-4-891-2007"),
    ("7", "Twohig-Bennett C., Jones A. (2018). The health benefits of the great outdoors: a systematic review and "
          "meta-analysis of greenspace exposure and health outcomes. <i>Environmental Research</i> 166:628–637. "
          "doi:10.1016/j.envres.2018.06.030. (Abstract read.)", "https://doi.org/10.1016/j.envres.2018.06.030"),
    ("8", "Ekkel E.D., de Vries S. (2017). Nearby green space and human health: evaluating accessibility metrics. "
          "<i>Landscape and Urban Planning</i> 157:214–220. doi:10.1016/j.landurbplan.2016.06.008. (Metadata "
          "only; cited for the existence of competing metrics.)", "https://doi.org/10.1016/j.landurbplan.2016.06.008"),
    ("9", "Eurostat. Population on 1 January by NUTS 3 region (demo_r_pjanaggr3), MT002 Gozo and Comino, 2025. "
          "Retrieved 2 Oct 2026.", "https://ec.europa.eu/eurostat/databrowser/view/demo_r_pjanaggr3/default/table"),
    ("10", "European Commission. Clean energy for EU islands: Malta (Gozo area 67 km²).",
     "https://clean-energy-islands.ec.europa.eu/countries/malta"),
    ("11", "WorldPop (2025). Malta constrained population 2025, 100 m, R2025A v1. CC BY 4.0. OpenStreetMap "
           "contributors, data via Overpass API, 2 Oct 2026, ODbL.",
     "https://data.worldpop.org/GIS/Population/Global_2015_2030/R2025A/2025/MLT/v1/100m/constrained/"),
    ("12", "MiŻien. Analysis code and outputs: tools/cc-011-report/; data/cc-011/.", ""),
    ("13", "IFES ElectionGuide. Malta: Maltese House of Representatives 2026 General (held 30 May 2026; results "
           "source: Electoral Commission of Malta). Accessed 5 Oct 2026.", "https://electionguide.org/elections/id/5161/"),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. Our own analyses are screening estimates.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "2 Oct 2026", "First issue. Claim restated from the parties’ own texts rather than news "
                                         "summaries. Draft pending right of reply from the Partit Laburista, the "
                                         "Government and the Partit Nazzjonalista."),
                   ("1.1", "5 Oct 2026", "Corrections: the flyer said that, read broadly, the pledge “is met today”; it "
                                         "now says “already almost met”, as the report does (a screening estimate). "
                                         "The unsourced seat count (“36 seats to 29”) is removed; the 30 May 2026 "
                                         "election is now sourced [13]. Verdict and confidence unchanged.")])

build_report(Report(
    number="011", out=str(FIG / "report.pdf"), kicker="Election pledges, computed",
    title_lines=["Two green", "pledges: can", "anyone check them?"],
    subtitle_lines=["Testing Labour’s ten-minute green-space pledge and the PN’s", "net-zero Gozo plan against open data"],
    quote_lines=["“Every person … no more than ten minutes’ walk", "from an open or green space.”"], quote_size=15,
    attribution="Partit Laburista, manifesto 2026, priority 19 (our translation). And the PN: a plan for a",
    context="Net-Zero Gozo by 2040, with afforestation among the measures (programme, Gozo chapter).",
    verdict="Not substantiated", verdict_note="No definition or baseline for either pledge",
    footer_lines=["Version 1.1  ·  5 October 2026",
                  "Status: draft for right of reply (Partit Laburista / Government; Partit Nazzjonalista)",
                  "Prepared from public sources and open data. No site visits.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Manifesto pledges 2026 – green space and a net-zero Gozo", version="1.1", date="5 October 2026",
    pdf_title="Two green pledges: can anyone check them? Claim Check 011",
    pdf_subject="Tests Labour's 10-minute green-space pledge and the PN's net-zero Gozo plan",
    story=S))
