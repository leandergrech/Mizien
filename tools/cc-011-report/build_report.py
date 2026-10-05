"""Claim Check 011 report. Run green_access.py and figures.py first. Output: out/report.pdf

Until v1.1 this check also covered the PN's net-zero Gozo pledge; since v1.2 (5 Oct 2026) that is Claim Check 107.
"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []

# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("Before the general election of 30 May 2026 [9], <b>Labour</b> (now in government) promised that nobody "
        "would live more than <b>ten minutes’ walk from an open or green space</b>. We tested whether the pledge has "
        "a baseline, a definition and a counting method that would let anyone check it, and measured how far Malta "
        "is from it today under each reading.", lead)]
S.append(key_points([
    ("The pledge may already be met, or be far off. It depends on the definition.",
     "If any open or green space counts, about 99.9% of residents already live within 800 m. If only public parks "
     "of at least 0.5 ha count, 55–68% do, leaving some 170,000–240,000 people outside."),
    ("The manifesto gives no definition, baseline or date.",
     "Without them the pledge cannot be checked, and could be declared met without any new green space."),
    ("The WHO-style measure is far off.",
     "About a quarter of residents live within 300 m of a public park of at least 0.5 ha, the distance and size "
     "WHO Europe suggests as an indicator."),
    ("Verdict: not substantiated.",
     "The pledge is not wrong; it is not stated in a way that can be measured."),
]))
S += [Spacer(1, 4 * mm), VerdictMeter(2), Spacer(1, 3 * mm),
      tiles([("99.9%", GREEN, "Residents within 800 m of any green or open space (straight line)"),
             ("55%", ORANGE, "Within an 800 m walk of a public park of at least 0.5 ha"),
             ("~240,000", ORANGE, "People outside that walk (WorldPop 2025 model)"),
             ("24%", RED, "Within 300 m of such a park (WHO Europe indicator)")]),
      Spacer(1, 4 * mm),
      up_down("A published definition of “open or green space”, a baseline map and a target year from the "
              "government.",
              "A government statement that the pledge is met using a broad definition without new space being "
              "created."),
      Spacer(1, 5 * mm)]
S += toc([("1", "The pledge and what we could verify"), ("2", "Method"), ("3", "Why the definition decides the answer"),
          ("4", "Ten minutes from green space"), ("5", "Testing the pledge"), ("6", "Verdict and requests for evidence"),
          ("7", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The pledge and what we could verify"))
S.append(P("Our candidate record took the pledge from a MaltaToday summary [3]. We then found Labour’s own text [1], in "
           "Maltese. The translation is ours; the original wording is quoted so readers can check it. It differs from "
           "the news summary in a way that matters: it says <i>open or green</i> space, not green space."))
S.append(std_table([
    [C("Source", cellh), C("What it says (our translation)", cellh), C("Our access", cellh), C("Status", cellh)],
    [C("<b>Partit Laburista</b>, manifesto <i>Int Malta</i>, 2026, priority 19, p. 17 [1]"),
     C("“Kull persuna f’pajjiżna ma tkunx aktar minn għaxar minuti mixi ’l bogħod minn "
       "spazju miftuħ jew aħdar.” <i>Every person in our country will be no more than ten minutes’ "
       "walk from an open or green space.</i> On p. 21 the indicator is “access to open spaces and the "
       "availability of recreational zones”, to be met through green spaces within ten minutes’ walk and "
       "investment in Manoel Island, White Rocks, Fort Campbell and other parks."),
     C("Read: pp. 17 and 21 of the 268-page PDF (hash recorded)."), C("<b>The pledge</b>")],
    [C("<b>MaltaToday</b>, May 2026 [3]"),
     C("“every citizen is within a 10-minute walk of a green space”."), C("Read (Wayback copy)."),
     C("Summary")],
], [36 * mm, 82 * mm, 32 * mm, 20 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("FAIRNESS NOTE", tag),
               P("Labour won the general election of 30 May 2026 [9], so its pledge is now a government commitment. "
                 "The goal is legitimate: nearby green space is associated with better health [5]. The opposition PN "
                 "proposes a Parks Act to give “park” and “green space” a legal definition [2], which "
                 "would address part of the problem identified here. This check is about whether the pledge can be "
                 "measured. The PN’s own environmental pledge for Gozo, assessed here until version 1.1, is now "
                 "Claim Check 107.", small)], bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Question.</b> Does the pledge have a definition, baseline and counting method that would allow it to be "
           "checked, and how far is Malta from it today under each reading?"))
S.append(P("<b>Green-space access.</b> We overlaid WorldPop’s 2025 population grid (100 m cells, constrained to "
           "built-up areas) with OpenStreetMap green and open spaces downloaded on 2 October 2026 [7]. For six "
           "definitions, from strict (public parks of at least 1 ha) to broad (any green or open space, including "
           "squares and beaches), we computed the share of residents within 300 m, 615 m and 800 m in a straight line. "
           "A ten-minute walk at 4.8 km/h is 800 m along streets; 615 m in a straight line allows for typical detours "
           "(factor 1.3). 300 m is the WHO Europe indicator distance [4]. Code: <i>tools/cc-011-report/green_access.py</i>."))
S.append(P("<b>Grades.</b> WHO guidance, meta-analyses of observational studies and official statistics are C; our own "
           "analysis is a screening estimate and is labelled as such."))

# ================================================================== 3
S.append(CondPageBreak(60 * mm))
S.append(SectionHeading(3, "Why the definition decides the answer"))
S.append(P("The pledge rests on a phrase that is not defined: <i>open or green space</i>. Does a paved square count, a "
           "strip of roadside grass, a patch of garrigue, a beach? The research on green space and health uses many "
           "different access measures and they do not give the same answers [4, 6]. WHO Europe proposes a minimum size "
           "(0.5 ha, with 1 ha as an additional indicator) and a short distance (300 m) precisely because tiny or "
           "distant spaces are used less [4]."))

# ================================================================== 4
S.append(PageBreak())
S.append(SectionHeading(4, "Ten minutes from green space"))
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
S.append(CondPageBreak(90 * mm))
S.append(SectionHeading(5, "Testing the pledge"))
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
    [C("<b>C.</b> Related pledge in the same manifesto: a 40% cut in carbon emissions by 2030 vs 2005 "
       "(priority 18)"), C("Labour [1]"),
     C("Same aim as the Climate Action Authority’s; scope not stated. See CC-003."), verd("SEE CC-003", GREY)],
], [46 * mm, 20 * mm, 70 * mm, 34 * mm], valign="MIDDLE"))

# ================================================================== 6
S += [Spacer(1, 6 * mm), SectionHeading(6, "Verdict and requests for evidence"),
      verdict_box("Not substantiated", "The pledge lacks the definition and baseline needed to check it. "
                  "Confidence: moderate. Our access analysis is a screening estimate."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> The pledge can be read as already achieved or as needing new parks within reach of about "
           "240,000 people; the manifesto does not say which. A pledge is not a statement of fact, so we do not call it "
           "false; we rate it <i>Not substantiated</i> because, as worded, it cannot be shown to be achieved or missed."))
S.append(P("<b>What this verdict does not say.</b> It does not say the goal is undesirable, or that anyone acted in bad "
           "faith. A checkable version of the pledge would read: <i>“By [year], every resident will live within "
           "800 m by foot of a public park of at least [size]; today [X]% do (map published).”</i>"))
S.append(CondPageBreak(45 * mm))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "From the government: the definition of “open or green space” used for priority 19 (minimum size, public "
    "access, whether squares, beaches and verges count).",
    "From the government: the baseline share of residents within ten minutes, the method (walking network or straight "
    "line) and the target year.",
    "From the government: the scope of the 40% emissions cut in priority 18 (total or effort-sharing emissions).",
]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag),
               P("Before wider circulation this draft should be sent to the Partit Laburista and, as the pledge is now "
                 "a government commitment, the Office of the Prime Minister or the responsible ministry, with a fixed "
                 "deadline (suggested 14 days). Responses will be appended and the verdict revisited.", small)],
              bg=AMBER_PALE, bar=AMBER)]

# ================================================================== 7
S += [Spacer(1, 6 * mm), SectionHeading(7, "Limitations")]
for l in ["The access analysis uses straight-line distances, a modelled population grid and OpenStreetMap tags, whose "
          "completeness in Malta we did not validate. Private gardens were excluded where tagged as private; some may "
          "remain. Grass verges and road islands are included in the broad definitions. A walking-network analysis "
          "would give lower shares for every definition.",
          "The manifesto translation is ours. The Labour PDF was read at pp. 17 and 21 only; other chapters may add detail.",
          "We read the green-space health literature [5, 6] as abstracts or metadata only; it is context for why the "
          "pledge matters, not evidence for the verdict."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Partit Laburista (2026). <i>Int Malta</i>: Manifest Elettorali 2026. Priorities list p. 17; indicators "
          "p. 21. SHA-256 466a60f9… recorded in literature/CC-011/references.bib.",
     "https://partitlaburista.org/wp-content/uploads/2026/08/Manifest_Elettorali_INT_MALTA_2026.pdf"),
    ("2", "Partit Nazzjonalista (2026). <i>Nifs Ġdid</i>: Programm Elettorali, chapter Ambjent (Parks Act).",
     "https://pn.org.mt/en/nifsgdid/ambjent/"),
    ("3", "MaltaToday (May 2026). Labour publishes its manifesto: here is a breakdown.",
     "https://www.maltatoday.com.mt/news/election-2026/141840/labour_publishes_its_manifesto_here_is_a_breakdown"),
    ("4", "WHO Regional Office for Europe (2016). <i>Urban green spaces and health: a review of evidence</i>. "
          "Copenhagen. (Indicator section read.)",
     "https://www.who.int/europe/publications/i/item/WHO-EURO-2016-3352-43111-60341"),
    ("5", "Twohig-Bennett C., Jones A. (2018). The health benefits of the great outdoors: a systematic review and "
          "meta-analysis of greenspace exposure and health outcomes. <i>Environmental Research</i> 166:628–637. "
          "doi:10.1016/j.envres.2018.06.030. (Abstract read.)", "https://doi.org/10.1016/j.envres.2018.06.030"),
    ("6", "Ekkel E.D., de Vries S. (2017). Nearby green space and human health: evaluating accessibility metrics. "
          "<i>Landscape and Urban Planning</i> 157:214–220. doi:10.1016/j.landurbplan.2016.06.008. (Metadata "
          "only; cited for the existence of competing metrics.)", "https://doi.org/10.1016/j.landurbplan.2016.06.008"),
    ("7", "WorldPop (2025). Malta constrained population 2025, 100 m, R2025A v1. CC BY 4.0. OpenStreetMap "
          "contributors, data via Overpass API, 2 Oct 2026, ODbL.",
     "https://data.worldpop.org/GIS/Population/Global_2015_2030/R2025A/2025/MLT/v1/100m/constrained/"),
    ("8", "MiŻien. Analysis code and outputs: tools/cc-011-report/; data/cc-011/.", ""),
    ("9", "IFES ElectionGuide. Malta: Maltese House of Representatives 2026 General (held 30 May 2026; results "
          "source: Electoral Commission of Malta). Accessed 5 Oct 2026.", "https://electionguide.org/elections/id/5161/"),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. Our own analyses are screening estimates.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "2 Oct 2026", "First issue, covering two pledges (Labour’s ten-minute green space and the "
                                         "PN’s net-zero Gozo). Claims restated from the parties’ own texts rather than "
                                         "news summaries. Draft pending right of reply."),
                   ("1.1", "5 Oct 2026", "Corrections: the flyer said that, read broadly, the pledge “is met today”; it "
                                         "now says “already almost met”, as the report does (a screening estimate). "
                                         "The unsourced seat count (“36 seats to 29”) is removed; the 30 May 2026 "
                                         "election is now sourced. Verdict and confidence unchanged."),
                   ("1.2", "5 Oct 2026", "Split at the maintainer’s request: this check now covers Labour’s "
                                         "ten-minute pledge only, under the title “Ten minutes’ walk to green "
                                         "space”. The PN’s net-zero Gozo pledge and its arithmetic are now Claim "
                                         "Check 107. Labour’s analysis and numbers are unchanged; references "
                                         "renumbered. Verdict and confidence unchanged.")])

build_report(Report(
    number="011", out=str(FIG / "report.pdf"), kicker="Election pledges, computed",
    title_lines=["Ten minutes’", "walk to green", "space?"],
    subtitle_lines=["Testing Labour’s 2026 green-space pledge", "against open population and map data"],
    quote_lines=["“Every person … no more than ten minutes’ walk", "from an open or green space.”"], quote_size=15,
    attribution="Partit Laburista, manifesto 2026, priority 19 (our translation).",
    context="Now a government commitment: Labour won the election of 30 May 2026.",
    verdict="Not substantiated", verdict_note="No definition or baseline: met already, or far off",
    footer_lines=["Version 1.2  ·  5 October 2026",
                  "Status: draft for right of reply (Partit Laburista / Government)",
                  "Prepared from public sources and open data. No site visits.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Ten minutes’ walk to green space – Labour manifesto 2026", version="1.2", date="5 October 2026",
    pdf_title="Ten minutes’ walk to green space? Claim Check 011",
    pdf_subject="Tests Labour's 2026 pledge that nobody lives more than ten minutes' walk from open or green space",
    story=S))
