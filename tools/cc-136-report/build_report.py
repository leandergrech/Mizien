"""Claim Check 136 report. Run fetch.py, calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("In a feature of 6 June 2026, Agence France-Presse (AFP) wrote that Malta <b>“is the most densely populated "
        "country in Europe, and approvals for new buildings are soaring”</b> and that its <b>“population has grown "
        "nearly 30 percent over a decade”</b>. We tested the three factual statements against the World Bank, "
        "Eurostat and the Planning Authority’s published series.", lead)]
S.append(key_points([
    ("Densest in the EU by a wide margin, but not in all of Europe.",
     "Malta has 1,805 people per km² (World Bank, 2024), 3.4 times the next EU state, the Netherlands (534). Monaco, "
     "at 18,537, is about ten times denser than Malta. Vatican City is in neither dataset and was not tested."),
    ("“Nearly 30 percent” is right.",
     "Population grew 30.9% from 1 January 2015 to 2025 and 30.8% from 2016 to 2026. The wording errs about a point low."),
    ("“Soaring” fits the latest year, not the whole decade.",
     "Approved dwelling units rose 41% in 2025 to 12,325 and were 4.6 times the 2013 low, but 2025 was below the 2018 "
     "and 2019 peaks. The article names no measure; “new buildings” are counted here as dwelling units."),
    ("Verdict: largely supported (high confidence).",
     "The population and approvals statements hold. The density ranking holds for the EU and for every European "
     "state in the World Bank list except Monaco; the sentence as written says “in Europe”."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("1,805", AMBER, "people per km² in Malta, 2024; Monaco 18,537"),
             ("3.4×", GREEN, "Malta’s density relative to the next EU state"),
             ("+30.9%", GREEN, "Population growth, 1 Jan 2015 to 2025"),
             ("12,325", AMBER, "dwelling units approved in 2025 (+41%)")]),
      Spacer(1, 4 * mm),
      up_down("AFP or the article’s author stating that “in Europe” means the EU Member States, or excluding "
              "microstates; the sentence would then hold as worded.",
              "A measure of “approvals for new buildings” (buildings, not dwelling units) showing no rise, or a "
              "reading of “country in Europe” that the evidence cannot support beyond Monaco."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the data show"),
          ("4", "Where the evidence points different ways"), ("5", "Testing the claim"),
          ("6", "Verdict and requests for evidence"), ("7", "Limitations")])
S.append(PageBreak())

S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The sentences are in AFP’s own voice in a feature by Ella Ide, “Picturesque Malta set to ‘implode’ as "
           "concrete jungle devours all”, of 6 June 2026 [1]. They are not a quotation of a source. The feature also "
           "quotes an activist and an academic on development; those opinions are not part of this check, and we do "
           "not rate the article’s reference to “scandals”. We read the article in full in the wire copy carried by "
           "eNCA on 25 October 2026; we did not read AFP’s original."))
S.append(std_table([
    [C("Source", cellh), C("What it says", cellh), C("Our access", cellh), C("Status", cellh)],
    [C("<b>AFP</b>, 6 Jun 2026 [1]"),
     C("“The tiny Mediterranean island is the most densely populated country in Europe, and approvals for new "
       "buildings are soaring despite scandals dogging the development sector.” “The country’s population has grown "
       "nearly 30 percent over a decade.”"),
     C("Full text read (eNCA wire copy)."), C("<b>The claim</b>")],
    [C("<b>World Bank</b>, EN.POP.DNST [2]"), C("People per km² of land area, 44 European states."),
     C("Downloaded 26 Oct 2026 (data/cc-136/)."), C("<b>Primary data</b>")],
    [C("<b>Eurostat</b>, demo_r_d3dens [3], demo_gind [4]"), C("National density; population on 1 January."),
     C("Downloaded 26 Oct 2026."), C("<b>Primary data</b>")],
    [C("<b>Planning Authority</b>, Approved Dwelling Units 2007–2025 [5]"),
     C("Dwelling units approved each year."),
     C("pa.org.mt refuses scripts; series transcribed for CC-013 from the file read on 3 Oct 2026."),
     C("Primary data, second reading ◆")],
], [38 * mm, 66 * mm, 40 * mm, 26 * mm]))

S += [Spacer(1, 4 * mm), SectionHeading(2, "Method")]
S.append(P("<b>Questions.</b> (A) Is Malta the most densely populated country in Europe? (B) Are approvals for new "
           "buildings soaring? (C) Has the population grown nearly 30 percent over a decade?"))
S.append(P("<b>Evidence.</b> For A we ranked the World Bank’s latest density values (2024) for 44 European states, "
           "including Monaco, San Marino, Liechtenstein and Andorra, and cross-checked the Eurostat national series. "
           "For B we used the Planning Authority’s count of approved dwelling units, the only approvals series we "
           "could read; the article does not say what it counts. For C we computed growth between 1 January values "
           "in Eurostat’s demographic balance for every ten-year window ending 2022–2026 "
           "(<i>tools/cc-136-report/calc.py</i>; outputs in <i>data/cc-136/checks.csv</i>)."))
S.append(P("<b>Grades.</b> Official statistics, grade C. No literature is needed to test these figures. "
           "<b>Verdicts</b> follow the five-point scale in Appendix A."))

S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(3, "What the data show"))
S.append(fig(FIG / "fig1_density.png", width=CW * 0.98))
S.append(P("Figure 1. Population density of the ten densest European states in the World Bank list, with and "
           "without Monaco. Malta in amber.", cap))
S.append(P("Eurostat’s own series, which divides by total area, gives Malta 1,817 people per km² in 2024, against "
           "529 for the Netherlands and 110 for the EU-27 [3]. Malta is first among the countries in Eurostat’s "
           "dataset (EU, EFTA and candidate countries)."))
S.append(fig(FIG / "fig2_approvals.png", width=CW * 0.95))
S.append(P("Figure 2. Dwelling units approved by the Planning Authority each year.", cap))
S.append(P("Approvals fell from 11,141 in 2007 to 2,679 in 2013, then climbed to a peak of 12,829 in 2018. After a dip "
           "to 7,578 in 2021 they reached 12,325 in 2025, up 41% on 2024 and 28% on 2022 [5]."))
S.append(CondPageBreak(75 * mm))
S.append(fig(FIG / "fig3_population.png", width=CW * 0.95))
S.append(P("Figure 3. Malta’s population growth over each ten-year window (1 January to 1 January).", cap))

S.append(CondPageBreak(80 * mm))
S.append(SectionHeading(4, "Where the evidence points different ways"))
S.append(contested("Is Malta “the most densely populated country in Europe”?", "TRUE FOR THE EU, NOT FOR ALL OF EUROPE", AMBER,
                   "Malta’s density is 3.4 times that of the next EU state and the highest in Eurostat’s dataset of EU, "
                   "EFTA and candidate countries [3]. Among the 44 states in the World Bank list it is second.",
                   "Monaco’s density (18,537 people per km²) is about ten times Malta’s, so “in Europe” is not "
                   "literally correct if microstates count as countries [2]. Vatican City is in neither dataset and "
                   "was not tested.",
                   "Most readers will take the sentence to compare Malta with other European countries of ordinary "
                   "size. The statement is accurate for the EU and needs the qualifier “after Monaco” for Europe.",
                   label_a="FOR THE CLAIM", label_b="AGAINST"))

S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(5, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> Malta is the most densely populated country in Europe"), C("AFP [1]"),
     C("1,805 people per km² (2024): first in the EU (3.4× the Netherlands), second in the World Bank’s 44 European "
       "states after Monaco (18,537). Vatican City not tested."), verd("TRUE FOR EU; MONACO DENSER", AMBER)],
    [C("<b>B.</b> Approvals for new buildings are soaring"), C("AFP [1]"),
     C("Dwelling units approved: 12,325 in 2025 (+41%), 4.6× the 2013 level, below the 2018–2019 peaks. No measure "
       "given in the article; dwelling units used."), verd("LARGELY ACCURATE", GREENC)],
    [C("<b>C.</b> Population has grown nearly 30 percent over a decade"), C("AFP [1]"),
     C("+30.9% (2015–2025) and +30.8% (2016–2026); 28.6% to 2023."), verd("ACCURATE", GREENC)],
], [42 * mm, 18 * mm, 76 * mm, 34 * mm], valign="MIDDLE"))

S += [Spacer(1, 6 * mm), SectionHeading(6, "Verdict and requests for evidence"),
      verdict_box("Largely supported", "Population and approvals statements hold; the density ranking holds for the "
                  "EU but not for Europe as a whole (Monaco). Confidence: high."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> Two of the three statements match the data. The third is right for any ordinary reading of "
           "“country in Europe” among larger states, and Malta is the second-densest of the 44 states we could "
           "compare, but the sentence says “in Europe” without excluding Monaco. That is a minor caveat that does "
           "not change the substance: Malta is by far the most crowded country in the EU. "
           "<b>What this verdict does not say.</b> It does not assess the feature’s wider argument about "
           "development, its quoted opinions or its reference to “scandals”."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list(["From AFP: which measure of “approvals” the sentence rests on.",
                        "From the Planning Authority: approvals of new buildings (not only dwelling units) by year, "
                        "in a form that machines can read."]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag),
               P("Not needed for this verdict (maintainer rule of 5 October 2026).", small)], bg=AMBER_PALE, bar=AMBER)]
S += [Spacer(1, 6 * mm), SectionHeading(7, "Limitations")]
for l in ["The World Bank divides by land area and Eurostat by total area; the two differ for Malta by about 12 people "
          "per km² (1,805 against 1,817) and do not change any ranking.",
          "Vatican City and Kosovo are not in the World Bank data; Vatican City is not in Eurostat’s either. We did "
          "not find a sourced density for Vatican City and do not state one.",
          "The Planning Authority series counts approved dwelling units, not buildings, and approvals are not "
          "construction. Its file is refused to scripts (403); we use the transcription made for CC-013 from the "
          "file read on 3 Oct 2026 and did not re-open it. ◆",
          "We read AFP through the eNCA wire copy; the AFP original and any later corrections were not read."]:
    S.append(P("• " + l, bul))
S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "AFP (Ella Ide), 6 Jun 2026. Picturesque Malta set to ‘implode’ as concrete jungle devours all (eNCA wire copy, "
          "read 25 Oct 2026).",
     "https://www.enca.com/lifestyle/picturesque-malta-set-implode-concrete-jungle-devours-all"),
    ("2", "World Bank. Population density (people per sq. km of land area), EN.POP.DNST, last updated 8 Oct 2026, retrieved "
          "26 Oct 2026.", "https://data.worldbank.org/indicator/EN.POP.DNST"),
    ("3", "Eurostat. Population density by NUTS 3 region (demo_r_d3dens), national level, updated 25 Feb 2026, retrieved "
          "26 Oct 2026.", "https://ec.europa.eu/eurostat/databrowser/view/demo_r_d3dens/default/table"),
    ("4", "Eurostat. Population change – demographic balance (demo_gind), updated 30 Sep 2026, retrieved 26 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/demo_gind/default/table"),
    ("5", "Planning Authority. Approved Dwelling Units 2007–2025, as transcribed in data/cc-013/pa_approved_dwellings.csv "
          "(file read 3 Oct 2026).", "https://www.pa.org.mt/file.aspx?f=37489"),
    ("6", "MiŻien. Calculation script and outputs: tools/cc-136-report/calc.py; data/cc-136/checks.csv.", ""),
])
S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "26 Oct 2026", "First issue. Verdict Largely supported (high confidence); no right of reply needed.")])

build_report(Report(
    number="136", out=str(FIG / "report.pdf"), kicker="Statistics and international reports",
    title_lines=["Most crowded", "country in", "Europe?"],
    subtitle_lines=["Testing an AFP feature on Malta", "against World Bank, Eurostat and Planning Authority data"],
    quote_lines=["“The tiny Mediterranean island is the most densely", "populated country in Europe.”"], quote_size=15,
    attribution="Agence France-Presse (AFP), 6 June 2026.",
    context="AFP’s own voice, in a feature on development in Malta.",
    verdict="Largely supported", verdict_note="Right for the EU; Monaco is denser. Population and approvals hold",
    footer_lines=["Version 1.0  ·  26 October 2026", "Status: no right of reply needed",
                  "Prepared from public sources and open data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Density and growth – AFP, June 2026", version="1.0", date="26 October 2026",
    pdf_title="Most crowded country in Europe? Claim Check 136",
    pdf_subject="Tests AFP's statements on Malta's density, approvals and population growth",
    story=S))
