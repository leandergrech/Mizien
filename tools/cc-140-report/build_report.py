"""Claim Check 140 report. Run fetch.py, calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("The Ministry for Finance’s Pre-Budget Consultation Document 2027 says: <b>“Eurostat statistics show that Malta’s "
        "energy import dependency is approximately 98.0 per cent, the highest in the European Union.”</b> No year is "
        "given. We checked both statements against Eurostat.", lead)]
S.append(key_points([
    ("The level is right.",
     "Eurostat’s indicator for Malta was 98.4% in 2024, the latest year, and between 97.0% and 99.0% in every year "
     "from 2019 to 2024. The EU-27 figure for 2024 is 57.3%."),
    ("The ranking is right.",
     "Malta was highest of the 27 Member States in every year from 2016 to 2024. In 2015 Cyprus was 0.03 points "
     "higher. In 2024 the next were Luxembourg (91.0%) and Cyprus (87.7%)."),
    ("The “98.0” has no stated year.",
     "No year gives exactly 98.0; 2024 gives 98.4. The gap is 0.4 points, and the decimal suggests more precision "
     "than the series has."),
    ("The indicator is mostly about shipping fuel.",
     "Bunker fuel for international shipping is 68.5% of the energy Eurostat counts for Malta in 2024, and it is "
     "all supplied from imports. Domestic use is a smaller figure, which this check does not compute."),
    ("Verdict: largely supported (high confidence).",
     "Both statements reproduce; the caveats concern the missing year and what the indicator measures."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("98.4%", GREEN, "Malta, 2024 (Eurostat); document says ≈98.0"),
             ("1st", GREEN, "Rank among 27 Member States in 2024 (next: Luxembourg 91.0%)"),
             ("57.3%", GREY, "EU-27 average, 2024"),
             ("68.5%", AMBER, "Share of Malta’s counted energy that is international maritime bunkers, 2024")]),
      Spacer(1, 4 * mm),
      up_down("The ministry naming a reference year that gives 98.0 on Eurostat’s indicator, or a revision that makes "
              "it so.",
              "A Eurostat revision that puts another Member State above Malta, or a figure for 2025 far from 98%."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the data show"),
          ("4", "What the figure does not say"), ("5", "Testing the claim"),
          ("6", "Verdict and requests for evidence"), ("7", "Limitations")])
S.append(PageBreak())

S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The claim is in the Ministry for Finance’s Pre-Budget Consultation Document 2027, launched on 30 September "
           "2026 [1]. The wording above was read on 26 October 2026 by the project’s intake session through a web reader, "
           "with the page given as 66 (it may be off by one). The ministry’s site returned HTTP 403 to our scripts "
           "on 30 October 2026, so we did not re-read the PDF for this report. MaltaToday reported the Finance "
           "Minister repeating the figure at the launch [2]; we did not read that article."))
S.append(std_table([
    [C("Source", cellh), C("What it says", cellh), C("Our access", cellh), C("Status", cellh)],
    [C("<b>Ministry for Finance</b>, Pre-Budget Consultation Document 2027 [1]"),
     C("“Eurostat statistics show that Malta’s energy import dependency is approximately 98.0 per cent, the highest "
       "in the European Union.”"), C("Read 26 Oct 2026 (web reader); not re-read 30 Oct (403)."), C("<b>The claim</b>")],
    [C("<b>Eurostat</b>, nrg_ind_id [3]"), C("Energy import dependency (net imports over gross available energy), "
                                            "all products, % , by country and year."),
     C("Downloaded 30 Oct 2026 (data/cc-140/)."), C("<b>Primary data</b>")],
    [C("<b>Eurostat</b>, nrg_bal_c [4]"), C("Malta’s imports, exports, gross available energy and bunkers, ktoe."),
     C("Downloaded 30 Oct 2026."), C("<b>Primary data</b>")],
], [38 * mm, 74 * mm, 36 * mm, 22 * mm]))

S += [Spacer(1, 4 * mm), SectionHeading(2, "Method")]
S.append(P("<b>Question.</b> Does Eurostat show Malta’s energy import dependency at about 98%, and is it the highest in "
           "the EU?"))
S.append(P("<b>Evidence.</b> We downloaded the indicator for all countries, 2015–2024 (<i>fetch.py</i>), ranked the 27 "
           "Member States by year, and rebuilt Malta’s figure from the energy balance as (imports − exports) / gross "
           "available energy (<i>calc.py</i>; outputs in <i>data/cc-140/checks.csv</i>). The rebuilt and published "
           "values agree to 0.1 point in every year 2019–2024, so the 98% is the standard Eurostat indicator and not a "
           "different calculation. Eurostat’s 2025 values were not yet published."))
S.append(P("<b>Grades.</b> Official statistics, grade C. No literature is needed for a statistic reported as such. "
           "<b>Verdicts</b> follow the five-point scale in Appendix A."))

S.append(CondPageBreak(100 * mm))
S.append(SectionHeading(3, "What the data show"))
S.append(fig(FIG / "fig1_dependency.png", width=CW * 0.95))
S.append(P("Figure 1. Energy import dependency, Malta, Cyprus, Luxembourg and the EU-27, 2015–2024 (Eurostat).", cap))
S.append(P("Malta’s value ranged from 97.0% to 99.0% over 2019–2024 (98.4% in 2024), against 55.5–62.5% for the EU-27. "
           "It was above 100% in 2016 and 2017 (101.1% and 103.1%), which Eurostat’s method permits when stocks are "
           "drawn down. In 2015 Cyprus (97.32%) was marginally above Malta (97.30%); from 2016 to 2024 Malta was first "
           "each year."))

S.append(Spacer(1, 4 * mm))
S.append(SectionHeading(4, "What the figure does not say"))
S.append(P("The indicator counts gross available energy including international maritime bunkers, the fuel sold to "
           "ships. For Malta these were 2,100 ktoe of 3,065 ktoe (68.5%) in 2024 [4]. Because the indicator is "
           "net imports over that total, a large share of ships’ fuel makes Malta’s ratio close to 100% whatever "
           "happens to domestic energy use. We did not compute a ratio without bunkers: it would need an assumption "
           "about how much of the bunker fuel is imported, and we have no sourced input for that. The statement "
           "is accurate as a statement about Eurostat’s indicator; it does not tell a reader how much of the energy "
           "used by households and businesses in Malta is imported. The document uses the figure in the context of "
           "energy subsidies (see CC-095); this check does not assess that argument."))

S.append(CondPageBreak(90 * mm))
S.append(SectionHeading(5, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> Malta’s energy import dependency is approximately 98.0 per cent"), C("Ministry for Finance [1]"),
     C("Eurostat: 98.4% in 2024; 97.0–99.0% in 2019–2024. No year is stated; none gives exactly 98.0."),
     verd("MOSTLY ACCURATE", GREENC)],
    [C("<b>B.</b> It is the highest in the European Union"), C("Ministry for Finance [1]"),
     C("Eurostat: first of 27 in every year 2016–2024 (next in 2024: Luxembourg 91.0%)."), verd("ACCURATE", GREENC)],
], [42 * mm, 18 * mm, 76 * mm, 34 * mm], valign="MIDDLE"))

S += [Spacer(1, 6 * mm), SectionHeading(6, "Verdict and requests for evidence"),
      verdict_box("Largely supported", "Both statements reproduce from Eurostat; the year is missing and the indicator is "
                                       "dominated by shipping fuel. Confidence: high."),
      Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> The level and the ranking reproduce. The caveats are minor and do not change the substance. "
           "<b>What this verdict does not say.</b> It does not say how dependent households and businesses are on "
           "imported energy, or whether subsidies are the right response."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list(["From the Ministry for Finance: the reference year of the 98.0 figure (future documents could "
                        "state it).", "From the maintainer: a downloaded copy of the Pre-Budget PDF, to confirm the "
                        "sentence and page."]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag), P("Not needed for this verdict (maintainer rule of 5 October 2026).", small)],
              bg=AMBER_PALE, bar=AMBER)]
S += [Spacer(1, 6 * mm), SectionHeading(7, "Limitations")]
for l in ["We could not re-read the PDF on 30 October 2026 (403); the wording rests on the earlier read recorded in the claim record.",
          "Eurostat’s 2025 values were not available; the ranking after 2024 is untested.",
          "We did not read the MaltaToday report of the launch."]:
    S.append(P("• " + l, bul))
S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Ministry for Finance (30 Sep 2026). Pre-Budget Consultation Document 2027.",
     "https://finance.gov.mt/wp-content/uploads/2026/09/PRE-BUDGET-2027-DOC.pdf"),
    ("2", "MaltaToday (30 Sep 2026). Report of the Pre-Budget Document launch (seen only as cited in the claim record; not read).", ""),
    ("3", "Eurostat. Energy imports dependency (nrg_ind_id), updated 16 Jul 2026, retrieved 30 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/nrg_ind_id/default/table"),
    ("4", "Eurostat. Complete energy balances (nrg_bal_c), updated 27 Aug 2026, retrieved 30 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/nrg_bal_c/default/table"),
    ("5", "MiŻien. Calculation script and outputs: tools/cc-140-report/calc.py; data/cc-140/checks.csv.", ""),
])
S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "30 Oct 2026", "First issue. Verdict Largely supported (high confidence); no right of reply needed.")])

build_report(Report(
    number="140", out=str(FIG / "report.pdf"), kicker="Statistics and government documents",
    title_lines=["98% energy", "import", "dependency?"],
    subtitle_lines=["Testing the Pre-Budget Document’s energy", "figure against Eurostat"],
    quote_lines=["“Eurostat statistics show that Malta’s energy import", "dependency is approximately 98.0 per cent, the",
                 "highest in the European Union.”"], quote_size=14,
    attribution="Ministry for Finance, Pre-Budget Consultation Document 2027, 30 September 2026.",
    context="Document launched for the 2027 Budget consultation.",
    verdict="Largely supported", verdict_note="Eurostat: 98.4% in 2024, highest of 27",
    footer_lines=["Version 1.0  ·  30 October 2026", "Status: no right of reply needed",
                  "Prepared from public sources and Eurostat data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Energy import dependency – Pre-Budget Document 2027", version="1.0", date="30 October 2026",
    pdf_title="98% energy import dependency? Claim Check 140",
    pdf_subject="Tests the Pre-Budget Document 2027 energy import dependency figure",
    story=S))
