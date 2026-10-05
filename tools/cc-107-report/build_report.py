"""Claim Check 107 report (split from Claim Check 011 on 5 Oct 2026). Run gozo_calc.py and figures.py first.
Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []

# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("Before the general election of 30 May 2026 [7], the <b>Nationalist Party</b> promised “a clear and realistic "
        "plan” for <b>Gozo to become a Net-Zero Island by 2040</b>, with afforestation among the measures. News "
        "reports summarised it as net zero “through afforestation”. We tested whether the pledge has a baseline, a "
        "boundary and a pathway that would let anyone check it, and whether afforestation could do the job.", lead)]
S.append(key_points([
    ("A plan to make a plan.",
     "The programme promises a plan but publishes no emissions baseline, no boundary (imported electricity, ferries, "
     "tourism) and no pathway to 2040."),
    ("There is no official inventory, but there is a baseline to build on.",
     "A 2023 study for the EU’s Clean energy for EU islands secretariat put Gozo’s energy-related CO<sub>2</sub> at "
     "118,000–154,000 t a year in 2016–2020 [6]. Our population-based estimate is about 157,000 t."),
    ("Afforestation alone could not do it.",
     "Offsetting those emissions with new forest would need 4.9–6.3 times Gozo’s land area at a measured semi-arid "
     "rate (1.5–8.5 times across our wider range). The PN’s own text relies on cutting emissions first; the "
     "“through afforestation” version is a news summary."),
    ("Verdict: not substantiated (moderate confidence).",
     "A pledge is not a statement of fact, so it is not false; as worded it cannot be shown to be achieved or missed."),
]))
S += [Spacer(1, 4 * mm), VerdictMeter(2), Spacer(1, 3 * mm),
      tiles([("118–154 kt", GREY, "Gozo energy CO₂ a year, 2016–20 (EU islands study)"),
             ("~157 kt", GREY, "Our population-based estimate (no official figure)"),
             ("4.9–6.3×", RED, "Gozo’s area needed as new forest to offset that (measured rate)"),
             ("2040", ORANGE, "Target year; no published pathway")]),
      Spacer(1, 4 * mm),
      up_down("A Gozo emissions inventory with a stated boundary and a costed 2040 pathway showing the shares from "
              "cuts, afforestation and offsets.",
              "A net-zero claim for Gozo that relies on unspecified offsets, or leaves out ferries or imported "
              "electricity without saying so."),
      Spacer(1, 5 * mm)]
S += toc([("1", "The pledge and what we could verify"), ("2", "Method"), ("3", "What “net zero” would have to mean"),
          ("4", "The arithmetic"), ("5", "Testing the pledge"), ("6", "Verdict and requests for evidence"),
          ("7", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The pledge and what we could verify"))
S.append(P("Our candidate record took the pledge from a MaltaToday summary [2]. We then found the PN’s own text [1], in "
           "Maltese. The translation is ours; the original wording is quoted so readers can check it. The text sets a "
           "2040 date and lists afforestation as one measure among many, which the summary did not."))
S.append(std_table([
    [C("Source", cellh), C("What it says (our translation)", cellh), C("Our access", cellh), C("Status", cellh)],
    [C("<b>Partit Nazzjonalista</b>, programme <i>Nifs Ġdid</i>, chapter Għawdex [1]"),
     C("“Infasslu pjan ċar u realistiku biex sal-2040, Għawdex isir Net-Zero Island…” "
       "<i>We will draw up a clear and realistic plan so that by 2040 Gozo becomes a Net-Zero Island, the first in "
       "the Mediterranean where every unit of emissions is reduced or offset</i>, through solar panels, electric "
       "cars, taxis and vans, building efficiency, ecological restoration on land and at sea, afforestation, and "
       "water and soil conservation, among others."),
     C("Read in full in a browser."), C("<b>The pledge</b>")],
    [C("<b>MaltaToday</b>, May 2026 [2]"),
     C("Gozo “would become a net-zero island through afforestation”."), C("Read (Wayback copy)."), C("Summary")],
], [36 * mm, 82 * mm, 32 * mm, 20 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("FAIRNESS NOTE", tag),
               P("Labour won the general election of 30 May 2026 [7], so this is an opposition proposal; Labour’s own "
                 "environmental pledge from the same campaign is Claim Check 011, held to the same standard. Island "
                 "decarbonisation is EU policy, and an energy baseline for Gozo already exists [6] that a plan could "
                 "start from. This check is about whether the pledge can be measured. Until 5 October 2026 it was part "
                 "of Claim Check 011.", small)], bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Question.</b> Does the pledge have a baseline, boundary and counting method that would allow it to be "
           "checked, and is net zero through afforestation physically plausible on Gozo?"))
S.append(P("<b>Gozo’s emissions.</b> No official greenhouse-gas inventory exists for Gozo. We used two estimates: "
           "(a) population (41,253 on 1 January 2025 [4]) times Malta’s national emissions per person (2.5, 3.81 and "
           "5.0 t CO<sub>2</sub>e; 3.81 t is Malta’s 2024 figure in Claim Check 003 [8]); and (b) the energy-related "
           "CO<sub>2</sub> estimated for 2016–2020 in the 2023 Energy Baseline Scenario for Gozo [6] (electricity, "
           "transport on the island, ferries to and from it, heating and cooling)."))
S.append(P("<b>Sequestration.</b> A measured rate from a semi-arid Aleppo pine afforestation on rendzina over limestone "
           "(about 3.6 t CO<sub>2</sub>/ha/yr over 35 years [3]) and an optimistic 10 t. Gozo’s area is 67 km² [5]. "
           "Code: <i>tools/cc-107-report/gozo_calc.py</i>; results in <i>data/cc-107/gozo_net_zero_arithmetic.csv</i>."))
S.append(P("<b>Grades.</b> The afforestation inventory is B; official statistics and the EU islands study are C; our "
           "own arithmetic is an order-of-magnitude estimate and is labelled as such."))

# ================================================================== 3
S.append(CondPageBreak(60 * mm))
S.append(SectionHeading(3, "What “net zero” would have to mean"))
S.append(P("The pledge rests on a term that is not defined for Gozo. Which emissions count? The 2023 baseline counts "
           "electricity drawn from Malta’s grid, transport on the island and the ferries [6]; transport alone is "
           "60–70% of Gozo’s energy use there. A boundary that left out the ferries or imported electricity would make "
           "the target easier without any change on the island. And what counts as an offset: forests on Gozo, "
           "restoration at sea, or credits bought elsewhere? The programme does not say."))

# ================================================================== 4
S.append(PageBreak())
S.append(SectionHeading(4, "The arithmetic"))
S.append(fig(FIG / "fig2_gozo_forest.png"))
S.append(P("Figure 1. New forest needed to offset Gozo’s estimated annual emissions by afforestation alone, under "
           "three population-based emissions estimates and two sequestration rates, compared with Gozo’s land area.", cap))
S.append(std_table([
    [C("Emissions estimate", cellh), C("t CO<sub>2</sub> a year", cellh), C("Forest needed, measured rate", cellh),
     C("Multiple of Gozo", cellh)],
    [C("EU islands baseline, lowest year (2020) [6]"), C("118,333"), C("327 km²"), C("<b>4.9×</b>")],
    [C("EU islands baseline, highest year (2019) [6]"), C("153,997"), C("425 km²"), C("<b>6.3×</b>")],
    [C("Population × 3.81 t (central) [4, 8]"), C("157,174"), C("434 km²"), C("6.5×")],
    [C("Population × 2.5 t, optimistic 10 t/ha/yr"), C("103,133"), C("103 km²"), C("1.5×")],
    [C("Population × 5.0 t, measured rate"), C("206,265"), C("570 km²"), C("8.5×")],
], [70 * mm, 32 * mm, 40 * mm, 28 * mm]))
S.append(P("Measured rate 3.62 t CO<sub>2</sub>/ha/yr [3]; Gozo 67 km² [5]. Full results in "
           "<i>data/cc-107/gozo_net_zero_arithmetic.csv</i>.", cap))
S.append(callout([P("THE ARITHMETIC", tag),
                  P("Gozo population 41,253 × 3.81 t per person = about 157,000 t CO<sub>2</sub>e a year, close to the "
                    "highest year in the 2023 energy baseline (154,000 t in 2019). A measured semi-arid pine "
                    "afforestation stored about 3.6 t CO<sub>2</sub> per hectare per year [3]. Offsetting 118,000–154,000 t "
                    "would take 33,000–43,000 ha of new forest: 4.9 to 6.3 times Gozo’s 67 km² [5]. Planting 10% "
                    "of Gozo would offset about 1.5% of the central estimate.", small)], bg=BLUE_PALE, bar=BLUE))
S.append(Spacer(1, 3 * mm))
S.append(P("What this means for the pledge", h2))
for t in ["• <b>“Net zero through afforestation”, as reported, is not possible on Gozo.</b> But that is the "
          "news summary [2], not the PN’s text.",
          "• <b>The PN’s text relies on cutting emissions first</b> (solar, electric vehicles, efficient "
          "buildings), with restoration and afforestation as part of the mix. Whether that reaches net zero by 2040 "
          "depends on numbers the programme does not give: a baseline, a boundary, and the role of offsets bought "
          "from elsewhere.",
          "• <b>Sequestration in young plantations is slow at first and can be reversed</b> by drought or fire; "
          "the measured rate [3] is a 35-year average on a site with deep groundwater, not a guaranteed yield on "
          "Gozo’s thin soils.",
          "• <b>“The first island in the Mediterranean”</b> was not tested."]:
    S.append(P(t, bul))

# ================================================================== 5
S.append(CondPageBreak(80 * mm))
S.append(SectionHeading(5, "Testing the pledge"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> A clear and realistic plan for a Net-Zero Gozo by 2040"), C("PN [1]"),
     C("No plan published; no official inventory or boundary. A 2023 energy baseline exists [6] but the programme "
       "does not use or cite it. Cannot be assessed as “realistic”."), verd("NO BASELINE", ORANGE)],
    [C("<b>B.</b> Gozo net zero through afforestation (news summary)"), C("MaltaToday [2]"),
     C("Would need 4.9–6.3 times Gozo’s area as new forest at a measured rate. Not the PN’s own wording."),
     verd("NOT POSSIBLE AS REPORTED", RED)],
    [C("<b>C.</b> The first island in the Mediterranean where every unit of emissions is reduced or offset"),
     C("PN [1]"), C("Not tested."), verd("NOT TESTED", GREY)],
], [46 * mm, 20 * mm, 70 * mm, 34 * mm], valign="MIDDLE"))

# ================================================================== 6
S += [Spacer(1, 6 * mm), SectionHeading(6, "Verdict and requests for evidence"),
      verdict_box("Not substantiated", "A plan promised without a baseline, boundary or pathway; afforestation alone "
                  "would need 4.9–6.3 times Gozo’s area. Confidence: moderate."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> The pledge promises a plan for an outcome whose starting point and boundary are not defined, "
           "and the widely reported version (afforestation) is physically impossible on Gozo’s land area. A pledge is "
           "not a statement of fact, so we do not call it false; we rate it <i>Not substantiated</i> because, as "
           "worded, it cannot be shown to be achieved or missed."))
S.append(P("<b>What this verdict does not say.</b> It does not say the goal is undesirable, or that anyone acted in "
           "bad faith. A checkable version would read: <i>“Gozo’s emissions, on [boundary], were [X] t in [year]; by "
           "2040 we will cut them to [Y] t and offset the rest by [means].”</i>"))
S.append(CondPageBreak(45 * mm))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "From the PN: a Gozo emissions inventory and its boundary (imported electricity, inter-island ferries, tourism).",
    "From the PN: the share of the 2040 target expected from cuts, from afforestation and from offsets elsewhere.",
    "From the PN: the area to be afforested on Gozo and the species and sequestration rate assumed.",
    "From the PN: whether the plan would start from the 2023 Energy Baseline Scenario for Gozo.",
]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag),
               P("Before wider circulation this draft should be sent to the Partit Nazzjonalista with a fixed deadline "
                 "(suggested 14 days). Responses will be appended and the verdict revisited.", small)],
              bg=AMBER_PALE, bar=AMBER)]

# ================================================================== 7
S += [Spacer(1, 6 * mm), SectionHeading(7, "Limitations")]
for l in ["The population-based estimate uses national per-person figures; Gozo’s real profile (less industry, more "
          "tourism and ferry traffic) may differ. The 2.5–5.0 t range is our assumption.",
          "The 2023 baseline is a study prepared for the EU islands secretariat, not official statistics. It covers "
          "energy use only, attributes grid electricity with conversion factors, and reflects its authors’ views, not "
          "the Commission’s [6].",
          "The sequestration rate comes from one well-studied site in Israel; no Maltese measurements were found.",
          "The programme translation is ours."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Partit Nazzjonalista (2026). <i>Nifs Ġdid</i>: Programm Elettorali, chapter Għawdex.",
     "https://pn.org.mt/en/nifsgdid/ghawdex/"),
    ("2", "MaltaToday (May 2026). PN approves its electoral manifesto.",
     "https://www.maltatoday.com.mt/news/election-2026/141891/pn_approves_its_electoral_manifesto"),
    ("3", "Grünzweig J.M., Gelfand I., Fried Y., Yakir D. (2007). Biogeochemical factors contributing to enhanced "
          "carbon storage following afforestation of a semi-arid shrubland. <i>Biogeosciences</i> 4(5):891–904. "
          "doi:10.5194/bg-4-891-2007. (Full text read; open access.)", "https://doi.org/10.5194/bg-4-891-2007"),
    ("4", "Eurostat. Population on 1 January by NUTS 3 region (demo_r_pjanaggr3), MT002 Gozo and Comino, 2025. "
          "Retrieved 2 Oct 2026.", "https://ec.europa.eu/eurostat/databrowser/view/demo_r_pjanaggr3/default/table"),
    ("5", "European Commission. Clean energy for EU islands: Malta (Gozo area 67 km²).",
     "https://clean-energy-islands.ec.europa.eu/countries/malta"),
    ("6", "Vaz L., Rodrigues de Almeida J. (2023). <i>Clean energy for EU islands: Energy Baseline Scenario for "
          "Gozo</i>. Clean energy for EU islands secretariat, 25 January 2023. Table 16. (Read in full.)",
     "https://clean-energy-islands.ec.europa.eu/system/files/2025-06/REPORT_TechnicalAssistance_Gozo_20230223.pdf"),
    ("7", "IFES ElectionGuide. Malta: Maltese House of Representatives 2026 General (held 30 May 2026; results "
          "source: Electoral Commission of Malta). Accessed 5 Oct 2026.", "https://electionguide.org/elections/id/5161/"),
    ("8", "MiŻien. Analysis code and outputs: tools/cc-107-report/; data/cc-107/; Malta’s 2024 emissions per person "
          "from data/cc-003/checks.csv.", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. Our own arithmetic is an order-of-magnitude estimate.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "5 Oct 2026", "First issue as a separate check. The analysis first appeared as pledge 2 of "
                                         "Claim Check 011 (v1.0, 2 Oct 2026; v1.1, 5 Oct 2026). New in this issue: the "
                                         "2023 Energy Baseline Scenario for Gozo [6], which gives an energy-emissions "
                                         "baseline and puts the forest needed at 4.9–6.3 times Gozo’s area at the "
                                         "measured rate (the 1.5–8.5 times range is kept). Verdict as in Claim Check "
                                         "011: not substantiated, moderate confidence. Draft pending right of reply "
                                         "from the Partit Nazzjonalista.")])

build_report(Report(
    number="107", out=str(FIG / "report.pdf"), kicker="Election pledges, computed",
    title_lines=["A net-zero", "Gozo by 2040?"],
    subtitle_lines=["Testing the Nationalist Party’s 2026 pledge", "against open data and a measured forest"],
    quote_lines=["“A clear and realistic plan so that by", "2040 Gozo becomes a Net-Zero Island.”"], quote_size=15,
    attribution="Partit Nazzjonalista, programme Nifs Ġdid 2026, chapter Għawdex (our translation).",
    context="News summaries: Gozo would become net zero “through afforestation”.",
    verdict="Not substantiated", verdict_note="No baseline, boundary or pathway published",
    footer_lines=["Version 1.0  ·  5 October 2026",
                  "Status: draft for right of reply (Partit Nazzjonalista)",
                  "Prepared from public sources and open data. No site visits.", "Repository: github.com/leandergrech/Mizien"],
    running_head="A net-zero Gozo by 2040 – PN programme 2026", version="1.0", date="5 October 2026",
    pdf_title="A net-zero Gozo by 2040? Claim Check 107",
    pdf_subject="Tests the Nationalist Party's 2026 pledge of a plan for a net-zero Gozo by 2040",
    story=S))
