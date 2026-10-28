"""Claim Check 144 report. Run calc.py and figures.py first. Output: out/report.pdf"""
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
      P("Mongabay’s news report of 5 October 2026 on the shooting of migratory birds after the storm of 14 September "
        "says, in its own voice: <b>“Malta has the highest density of hunters in all of Europe.”</b> The sentence "
        "does not say what the density is measured against. We recomputed it from the only country-by-country "
        "table we could open, the European hunters’ federation FACE’s 2009–2010 table (35 countries), and from "
        "Eurostat’s land area and population. Per square kilometre Malta is first by a wide margin; per head of "
        "population it is not.", lead)]
S.append(key_points([
    ("Per square kilometre, the claim holds.",
     "Malta had 47 hunters per km² on FACE’s count of 15,000 (Eurostat area 316 km²), 9.5 times the next country, "
     "Ireland (5.0). It stays first even at 10,000 hunters (32 per km²) and would at 5,000 (16 per km²)."),
    ("Per head of population, it does not.",
     "On the same table Malta is 5th of 35 (36 per 1,000 inhabitants), behind Ireland (83), Finland (59), "
     "Cyprus (56) and Norway (40). With about 10,000 hunters and today’s population it is 18 per 1,000."),
    ("The sentence does not say which.",
     "‘Density’ most naturally means per area, which is the reading the evidence supports; a reader could "
     "also take it as hunters per inhabitant."),
    ("The numbers are old or second-hand.",
     "FACE’s table is from 2009–2010. No current official count was readable: the Wild Birds Regulation Unit’s "
     "reports are browser-only. The 10,000 figure is BirdLife Malta’s, as quoted by Mongabay."),
    ("Verdict: largely supported (moderate confidence).",
     "True on the usual meaning of density and robust to the uncertainty in Malta’s count; not true per capita, "
     "which the sentence does not exclude."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("47", ORANGE, "Malta hunters per km² (FACE count 15,000; area 316 km²). Next highest: Ireland, 5.0"),
             ("9.5×", GREEN, "Malta’s density as a multiple of the next country’s, FACE 2009–10 table"),
             ("5th", RED, "Malta’s rank of 35 per 1,000 inhabitants, same table (Ireland 1st)"),
             ("32", ORANGE, "Malta hunters per km² at 10,000 hunters (BirdLife Malta via Mongabay)")]),
      Spacer(1, 4 * mm),
      up_down("A current official count of Malta’s hunters and a current country-by-country table for Europe "
              "showing the same ranking per km²; or the cited paper stating the ranking and its basis.",
              "A current, comparable count showing another country (or a small state we could not rank) above "
              "Malta per km², or evidence that the sentence was meant per inhabitant."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the data show"),
          ("4", "Where the evidence points different ways"), ("5", "Testing the claim"),
          ("6", "Verdict and requests for evidence"), ("7", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The claim is a sentence in a short news report by Spoorthy Raman, published by Mongabay on 5 October 2026 "
           "[1], which we read in full. It is the outlet’s own sentence, not a quotation from BirdLife Malta or any "
           "official; it links to a 2015 paper in <i>Biological Conservation</i>. The next sentence is a quotation "
           "from Antonia Micallef of BirdLife Malta, who is quoted as saying “Over 10,000 hunters [are] active at any "
           "one time.” The check is of the density ranking only."))
S.append(std_table([
    [C("What was said", cellh), C("Who", cellh), C("Access", cellh)],
    [C("“Malta has the highest density of hunters in all of Europe.”"), C("Mongabay (outlet’s own words) [1]"),
     C("Read in full")],
    [C("“Over 10,000 hunters [are] active at any one time”"), C("A. Micallef, BirdLife Malta, quoted by Mongabay [1]"),
     C("Read in full")],
    [C("Linked source: Veríssimo D., Campbell B. (2015), <i>Biological Conservation</i>, doi:10.1016/j.biocon.2015.07.018"),
     C("Linked by Mongabay [2]"), C("Identity verified in Crossref; closed access, abstract not available, not read")],
], [88 * mm, 46 * mm, 36 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("SCOPE NOTE", tag),
               P("This check covers the density ranking only. It makes no statement about hunters as people, about "
                 "the legality of any shooting reported in the article, or about the incident figures attributed to "
                 "BirdLife Malta.", small)], bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Question.</b> Is Malta’s density of hunters the highest in Europe, and does the answer depend on what "
           "density is measured against?"))
S.append(P("<b>Evidence.</b> FACE’s table ‘Hunters in Europe’ (35 countries with a count; area, population and hunters) "
           "from its Annual Report 2009–2010 [3]; Eurostat population on 1 January and land area for Malta [4]; "
           "Malta hunter counts from FACE [3] and, for sensitivity, the 10,000 figure quoted by Mongabay [1] and a "
           "licence count from the Wild Birds Regulation Unit (WBRU) known to us only second-hand (◆) [5]. All numbers "
           "are recomputed by <i>tools/cc-144-report/calc.py</i> from files in <i>data/cc-144/</i>. For Malta we use "
           "Eurostat’s area and population rather than FACE’s rounded 0.3 thousand km² and 0.4 million; for other "
           "countries we use FACE’s own area and population, which are rounded to the nearest thousand km² or 0.1 million."))
S.append(P("<b>Grades.</b> Official statistics and the federation’s own table are grade C; the NGO’s count is grade D "
           "(assertion). <b>Verdicts</b> follow the five-point scale in Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(150 * mm))
S.append(SectionHeading(3, "What the data show"))
S.append(fig(FIG / "fig1_ranking.png"))
S.append(P("Figure 1. Hunters per km² (left) and per 1,000 inhabitants (right), top countries in FACE’s 2009–2010 table; "
           "Malta in orange. Malta leads per km² and is fifth per head.", cap))
S.append(std_table([
    [C("Indicator", cellh), C("Malta", cellh), C("Comparison", cellh), C("Source", cellh), C("Grade", cellh)],
    [C("Hunters per km², FACE count 15,000"), C("<b>47.5</b> (1st of 35)"), C("Ireland 5.0, Cyprus 5.0, Denmark 3.8"),
     C("FACE [3]; Eurostat [4]"), grade_tag("C")],
    [C("Malta as multiple of next highest"), C("<b>9.5×</b>"), C("Ireland"), C("calculated"), grade_tag("C")],
    [C("Hunters per km² at 10,000 hunters"), C("31.6"), C("6.3× Ireland"), C("Mongabay [1]; Eurostat [4]"), grade_tag("D")],
    [C("Hunters per km² at 5,000 (stress test)"), C("15.8"), C("3.2× Ireland"), C("calculated"), grade_tag("C")],
    [C("Hunters per 1,000 inhabitants, FACE count"), C("36.2 (<b>5th</b> of 35)"),
     C("Ireland 83.3, Finland 59.2, Cyprus 56.2, Norway 40.4"), C("FACE [3]; Eurostat [4]"), grade_tag("C")],
    [C("Hunters per 1,000 at 10,000 hunters, 2024 population"), C("17.7"),
     C("10 other countries’ 2010 values higher"), C("Mongabay [1]; Eurostat [4]"), grade_tag("D")],
    [C("Population growth 2010–2024"), C("+36%"), C("Eurostat"), C("demo_pjan [4]"), grade_tag("C")],
], [58 * mm, 30 * mm, 42 * mm, 28 * mm, 12 * mm]))
S.append(P("All values in <i>data/cc-144/checks.csv</i> and <i>ranking_2010.csv</i>. FACE’s counts are 2009–2010; the "
           "comparison with Malta’s current numbers therefore mixes years and is indicative only.", cap))
S.append(KeepTogether([fig(FIG / "fig2_sensitivity.png"),
                       P("Figure 2. Malta’s hunters per km² under four counts, against the next-highest country in FACE’s table. The "
                         "ranking per km² survives a two-thirds cut in Malta’s count.", cap)]))
S.append(P("Malta’s area (316 km²) is small and its population density is among the highest in the world, so any "
           "per-area count of a population-linked activity gives a high figure. That is a fact about the denominator, "
           "not about hunting: it is why the per-area and per-head rankings differ."))

# ================================================================== 4
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(4, "Where the evidence points different ways"))
S.append(contested(
    "Q1  Is Malta first in Europe for hunters per area?", "YES, BY A WIDE MARGIN", GREEN,
    "On FACE’s table Malta has 47.5 hunters per km², 9.5 times Ireland and Cyprus (5.0 each). Even with Malta’s "
    "count cut to a third (5,000) it stays first (15.8 per km²).",
    "FACE’s other countries’ areas are rounded to thousand km², so small states (Luxembourg, Cyprus) carry large "
    "rounding errors, and no 2026 table was readable. Microstates absent from the table (for example San Marino, "
    "Liechtenstein) are not tested.",
    "<b>For this claim:</b> on the usual reading (per area) it is supported with a large margin; the uncertainty in "
    "the year and the count would have to be several-fold to change the ranking."))
S.append(contested(
    "Q2  Is Malta first for hunters per inhabitant?", "NO", RED,
    "Malta’s 36 hunters per 1,000 inhabitants (FACE count, 2010 population) is high, fifth of 35.",
    "Ireland (83), Finland (59), Cyprus (56) and Norway (40) are higher on the same table. A second-hand 2018 chart "
    "(Statista, citing the German Hunting Association ◆) also puts Ireland, Finland and Cyprus ahead and does not list "
    "Malta. At 10,000 hunters Malta is at 18 per 1,000.",
    "<b>For this claim:</b> if ‘density’ were read per inhabitant, the claim would be contradicted by the same "
    "table. The sentence does not specify; we treat per area as the primary meaning of ‘density’."))
S.append(contested(
    "Q3  How many hunters does Malta have now?", "NOT KNOWN FROM A CURRENT OFFICIAL SOURCE", AMBER,
    "BirdLife Malta, quoted by Mongabay, says over 10,000 are active at any one time. A search summary of the WBRU "
    "2025 report gave 10,091 general licences for hunting birds on land ◆ (not opened).",
    "FACE’s 2009–2010 count is 15,000. BirdLife Malta has said elsewhere that WBRU has not published a total number "
    "of hunting licences (reported in a search summary ◆, not verified by us). Licensees may hold several licence "
    "categories.",
    "<b>For this claim:</b> the count matters less than the denominator, because every plausible count (5,000–15,000) "
    "keeps Malta first per km²."))

# ================================================================== 5
S.append(CondPageBreak(90 * mm))
S.append(SectionHeading(5, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> “Malta has the highest density of hunters in all of Europe”, read per area"),
     C("47.5 per km² on FACE’s count, 9.5× the next country; first at every count from 5,000 to 15,000 [3][4]."),
     verd("SUPPORTED", GREENC)],
    [C("<b>B.</b> The same sentence read per inhabitant"),
     C("Fifth of 35 on FACE’s table (36 per 1,000; Ireland 83); 18 per 1,000 at 10,000 hunters [3][4]."),
     verd("NOT FIRST", RED)],
    [C("<b>C.</b> “Over 10,000 hunters [are] active at any one time” (BirdLife Malta, quoted)"),
     C("Consistent in order of magnitude with FACE (15,000) and the WBRU licence count ◆ (10,091); no current "
       "official total read. Not a claim about density; context only."), verd("NOT RATED", GREY)],
], [58 * mm, 82 * mm, 30 * mm], valign="MIDDLE"))

# ================================================================== 6
S += [Spacer(1, 6 * mm), SectionHeading(6, "Verdict and requests for evidence"),
      verdict_box("Largely supported", "True per area, by a wide margin; not true per inhabitant, which the "
                  "sentence does not exclude. Confidence: moderate."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) ‘Density’ without qualification most naturally means per unit area, and on that measure "
           "FACE’s own table puts Malta first by a factor of 9.5, a margin that survives a two-thirds reduction in "
           "Malta’s count. (2) The same table ranks Malta fifth per inhabitant. A reader who takes density per head "
           "would be misled, so the claim is not ‘Supported’ outright. (3) The comparison table is from 2009–2010 and "
           "the current Malta count is NGO-sourced or second-hand, which limits confidence to moderate."))
S.append(P("<b>What this verdict does not say.</b> It does not say that the number of hunters is high or low in absolute "
           "terms, that hunting in Malta is lawful or unlawful, or anything about any person."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "The WBRU’s current total of licensed hunters (all categories, de-duplicated by person).",
    "A current FACE or national country-by-country table of hunter numbers.",
    "The basis of the claim in the 2015 paper linked by Mongabay (full text).",
]))

# ================================================================== 7
S += [Spacer(1, 6 * mm), SectionHeading(7, "Limitations")]
for l in ["The only country-by-country table we could open is FACE’s 2009–2010 table; its definition of ‘hunter’ "
          "(licence holders, or active hunters) may differ by country, and FACE itself rounds areas and populations.",
          "A 2023 FACE activity report was searched for country figures and held none; FACE’s current member-country "
          "statistics were not found. A search was also run for a more recent table (28 Oct 2026); only a 2018 "
          "Statista chart (second-hand ◆) and a paywalled 2025 count for seven countries were found.",
          "wbru.gov.mt returned HTTP 403 to scripts, so the WBRU 2024 and 2025 Game Reporting Data reports were not "
          "opened; the 10,091 figure is from a search summary and is marked ◆.",
          "The 2015 paper linked by Mongabay is closed access and no abstract was available; we did not read what it "
          "says about Malta.",
          "Microstates not in the FACE table were not tested.",
          "Mixing 2009–2010 counts for other countries with Malta’s current numbers is indicative only."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Raman S. (5 Oct 2026). Hunters reportedly kill hundreds of migratory birds stranded by thunderstorm in "
          "Malta. <i>Mongabay</i>.",
     "https://news.mongabay.com/short-article/2026/10/hunters-reportedly-kill-hundreds-of-migratory-birds-stranded-by-thunderstorm-in-malta/"),
    ("2", "Veríssimo D., Campbell B. (2015). Understanding stakeholder conflict between conservation and hunting in "
          "Malta. <i>Biological Conservation</i>. doi:10.1016/j.biocon.2015.07.018. (Identity verified in Crossref; not read.)",
     "https://doi.org/10.1016/j.biocon.2015.07.018"),
    ("3", "FACE (2010). Annual Report 2009–2010, p. 16: ‘Hunters in Europe’ (table of area, hunters, population by "
          "country). Retrieved 28 Oct 2026.",
     "https://www.face.eu/sites/default/files/attachments/data_hunters-region_sept_2010.pdf"),
    ("4", "Eurostat. demo_pjan (population on 1 January: 2010, 2024, 2025) and demo_r_d3area (area, Malta); retrieved "
          "28 Oct 2026.", "https://ec.europa.eu/eurostat/databrowser/"),
    ("5", "◆ Wild Birds Regulation Unit (2026). Game Reporting Data report 2025. Known only from a search summary; the "
          "site returned HTTP 403.", "https://wbru.gov.mt/wp-content/uploads/2026/07/Game-Reporting-Data-report-2025.pdf"),
    ("6", "Miżien. Data and calculations: data/cc-144/; tools/cc-144-report/calc.py.", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "28 Oct 2026", "First issue.")])

build_report(Report(
    number="144", out=str(FIG / "report.pdf"), kicker="Nature and wildlife",
    title_lines=["Does Malta have", "Europe’s highest", "density of hunters?"],
    subtitle_lines=["Testing a news report’s claim about hunter density",
                    "against FACE’s country table and Eurostat"],
    quote_lines=["“Malta has the highest density of", "hunters in all of Europe.”"], quote_size=16,
    attribution="Mongabay (Spoorthy Raman), 5 October 2026.",
    context="The outlet’s own sentence, linking to a 2015 paper.",
    verdict="Largely supported", verdict_note="True per area; not per inhabitant",
    footer_lines=["Version 1.0  ·  28 October 2026", "Status: draft · no right of reply needed",
                  "Prepared from public sources, FACE and Eurostat data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Hunter density – Malta", version="1.0", date="28 October 2026",
    pdf_title="Does Malta have Europe's highest density of hunters? Claim Check 144",
    pdf_subject="Tests Mongabay's statement that Malta has the highest density of hunters in Europe",
    story=S))
