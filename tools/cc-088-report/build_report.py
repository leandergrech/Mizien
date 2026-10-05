"""Claim Check 088 report. Run fetch.py, calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("On 9 July 2026, for World Population Day, Malta’s National Statistics Office (NSO) published news release "
        "NR 120/2026. It says: <b>“The estimated total population of Malta and Gozo stood at 588,254 at the end of "
        "2025, up by 2.4 per cent when compared to the previous year.”</b> It adds that net migration of 13,906 "
        "persons “was the main contributor to population growth in 2025”. We read the release and recomputed every "
        "figure in the claim from Eurostat’s demographic accounts.", lead)]
S.append(key_points([
    ("The headline figure reproduces.",
     "Eurostat’s population on 1 January 2026 is 588,254, and 588,254 / 574,250 is +2.44% over 2025."),
    ("Net migration of 13,906 reproduces, and it is the main driver.",
     "Net migration was up 31.0% on 2024 (10,614). Births minus deaths added only 98 people (193 in 2024). "
     "Migration accounts for 99.3% of the 14,004 increase."),
    ("The arithmetic is consistent.",
     "98 + 13,906 = 14,004 = 588,254 − 574,250, with no statistical adjustment left over. Every other percentage "
     "in the release that we could test (births −0.8%, deaths +1.4%, natural increase −49.2%) reproduces."),
    ("Verdict: supported (high confidence).",
     "One caveat on independence: Eurostat’s Maltese data come from the NSO, so agreement confirms transmission "
     "and arithmetic, not an independent count. The figure is an estimate."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(0), Spacer(1, 3 * mm),
      tiles([("588,254", GREEN, "Residents at the end of 2025, as the NSO says"),
             ("+2.4%", GREEN, "Growth over 2025 (recomputed +2.44%)"),
             ("13,906", GREEN, "Net migration in 2025, up 31.0% on 2024"),
             ("99.3%", GREEN, "Share of 2025 growth that came from migration")]),
      Spacer(1, 4 * mm),
      up_down("Supported is the top of the scale, so nothing moves it up.",
              "A revision of the 2025 estimate that changes the population or net migration materially. The NSO "
              "revises estimates when new data arrive; this check is of the figures as released in July 2026."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the data show"),
          ("4", "Where the evidence points different ways"), ("5", "Testing the claim"),
          ("6", "Verdict and requests for evidence"), ("7", "Limitations")])
S.append(PageBreak())

S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The claim record paraphrases a news report: “Malta’s population rose to 588,254 at the end of 2025 (+2.4%), "
           "with net migration of 13,906 the main driver”. The primary text is the NSO’s release NR 120/2026, "
           "“World Population Day: 11 July 2026”, dated 9 July 2026 [1]. nso.gov.mt refuses automated downloads, so we "
           "read the release in full from an Internet Archive copy. MaltaToday [2] and Lovin Malta [3] report the same "
           "figures; they locate the release and are not evidence."))
S.append(std_table([
    [C("Source", cellh), C("What it says", cellh), C("Our access", cellh), C("Status", cellh)],
    [C("<b>NSO</b>, NR 120/2026, 9 Jul 2026 [1]"),
     C("“The estimated total population of Malta and Gozo stood at 588,254 at the end of 2025. This is an increase of "
       "2.4 per cent when compared to the previous year.” “Net migration (immigration minus emigration), amounting "
       "to 13,906 persons, was the main contributor to population growth in 2025.”"),
     C("Full text read (Internet Archive copy of the release page)."), C("<b>The claim</b>")],
    [C("<b>MaltaToday</b>, 9 Jul 2026 [2]"), C("Reports the same figures from the release."),
     C("Read via Internet Archive."), C("Locator, ◆ second-hand")],
    [C("<b>Eurostat</b>, demo_gind [4]"), C("Population on 1 January, births, deaths, natural increase, net migration."),
     C("Downloaded 5 Oct 2026 (data/cc-088/)."), C("<b>Cross-check</b>")],
], [38 * mm, 74 * mm, 36 * mm, 22 * mm]))

S += [Spacer(1, 4 * mm), SectionHeading(2, "Method")]
S.append(P("<b>Question.</b> Do the population, its growth and the size and role of net migration in the NSO’s release "
           "reproduce from published data, and are they internally consistent?"))
S.append(P("<b>Evidence.</b> We downloaded Eurostat’s demographic balance for Malta (demo_gind, updated 30 September "
           "2026) and recomputed each figure in the claim and the percentages the release gives for births, deaths and "
           "natural increase (<i>tools/cc-088-report/fetch.py</i> and <i>calc.py</i>; outputs in "
           "<i>data/cc-088/checks.csv</i>). Eurostat’s “population on 1 January 2026” is the NSO’s end-2025 figure. "
           "We also tested that the components (natural increase plus net migration) add up to the change in the "
           "stock. <b>Independence.</b> Eurostat publishes the figures that the NSO transmits, so agreement shows the "
           "release is internally consistent and matches the figures Malta reports to the EU. It is not an independent "
           "count; the NSO is the only source for Malta’s resident population."))
S.append(P("<b>Grades.</b> Official statistics, grade C. No literature is needed to test the figure. <b>Verdicts</b> "
           "follow the five-point scale in Appendix A."))

S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(3, "What the data show"))
S.append(fig(FIG / "fig1_population.png", width=CW * 0.98))
S.append(P("Figure 1. Malta’s population on 1 January (left) and growth in each calendar year (right). "
           "End 2025 is the 1 January 2026 value.", cap))
S.append(P("Malta’s population rose from 439 thousand on 1 January 2015 to 588 thousand on 1 January 2026. Growth "
           "peaked at 4.2% in 2022 (the year of the highest net migration), slowed to 1.9% in 2024 and recovered to "
           "2.4% in 2025."))
S.append(fig(FIG / "fig2_components.png", width=CW * 0.95))
S.append(P("Figure 2. Components of Malta’s population change each year: net migration and natural increase. "
           "Natural increase was 98 in 2025.", cap))
S.append(P("Net migration has accounted for 98–99.6% of annual growth in each of the last four years. The NSO "
           "notes that “both immigration and emigration decreased” in 2025, so the rise in net migration from 10,614 "
           "to 13,906 reflects emigration falling by more than immigration, not a surge in arrivals. We did not test "
           "the immigration and emigration flows themselves."))

S.append(CondPageBreak(80 * mm))
S.append(SectionHeading(4, "Where the evidence points different ways"))
S.append(contested("Do other sources give different figures?", "NOT TESTABLE FROM THE RELEASE", AMBER,
                   "NSO NR 120/2026 and Eurostat demo_gind give identical population (588,254), net migration "
                   "(13,906) and natural increase (98) for 2025. We found no published figure that disagrees.",
                   "The claim record notes that national density figures “differ by source” (1,731 against 1,838 "
                   "per km²). The release gives densities only for localities (for example Tas-Sliema, 18,186 per "
                   "km²), not for Malta as a whole; Eurostat’s density table gives 1,817.4 for 2024 and no 2025 value. "
                   "Density is not part of the claim.",
                   "Differences in national density come from the choice of land area and population date, not from "
                   "the population count. We did not find where the 1,731 and 1,838 figures come from, and make no "
                   "finding on them.", label_a="AGREEMENT", label_b="OPEN POINT"))

S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(5, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> Population reached 588,254 at the end of 2025"), C("NSO [1]"),
     C("Eurostat demo_gind: 588,254 on 1 January 2026. Reported as an estimate."), verd("ACCURATE", GREENC)],
    [C("<b>B.</b> …an increase of 2.4% on the previous year"), C("NSO [1]"),
     C("588,254 / 574,250 = +2.44%, which rounds to 2.4%."), verd("ACCURATE", GREENC)],
    [C("<b>C.</b> Net migration was 13,906 in 2025, the main contributor to growth"), C("NSO [1]"),
     C("Eurostat: 13,906. Natural increase 98. Migration is 99.3% of the 14,004 increase; net migration up 31.0% on 2024."),
     verd("ACCURATE", GREENC)],
], [42 * mm, 18 * mm, 76 * mm, 34 * mm], valign="MIDDLE"))

S += [Spacer(1, 6 * mm), SectionHeading(6, "Verdict and requests for evidence"),
      verdict_box("Supported", "Every figure in the claim reproduces from the Eurostat data and the release is "
                  "internally consistent. Confidence: high."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> The population, its growth, the net migration figure and its role as main driver all match "
           "Eurostat’s demographic balance, and the components sum to the change in the stock. The report’s "
           "confidence is high for the question asked, which is whether the NSO’s figures are consistent with "
           "what Malta reports to Eurostat. <b>What this verdict does not say.</b> It does not assess how the NSO "
           "estimates the resident population or migration (the method is outside this check), and it takes no "
           "view on migration policy or on the causes of the 2025 change."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "From the NSO: the source of the national density figures (1,731 and 1,838 per km²) that circulate, if it is "
    "an NSO series.",
    "From the NSO: the revision policy for the end-year estimates and the method used to count net migration.",
]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag),
               P("Not needed for this verdict (maintainer rule of 5 October 2026: a reply is sought only for "
                 "<i>Not substantiated</i>, <i>Misleading</i> or <i>Contradicted</i>).", small)], bg=AMBER_PALE, bar=AMBER)]
S += [Spacer(1, 6 * mm), SectionHeading(7, "Limitations")]
for l in ["Eurostat’s data for Malta come from the NSO, so the cross-check is not independent. The population is an "
          "estimate, and estimates can be revised.",
          "We read the release from an Internet Archive copy of the NSO page because nso.gov.mt refuses automated "
          "access. We did not read the release’s tables (the page links them) and did not test the citizenship, "
          "age, sex, district or locality figures.",
          "We did not test immigration and emigration flows, only their difference."]:
    S.append(P("• " + l, bul))
S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "National Statistics Office, Malta (9 Jul 2026). World Population Day: 11 July 2026. News Release NR 120/2026. "
          "Read from the Internet Archive copy of the page.", "https://nso.gov.mt/world-population-day-11-july-2026/"),
    ("2", "◆ Azzopardi K. (9 Jul 2026). Malta’s population rose to 588,254 by end 2025: NSO. MaltaToday.",
     "https://www.maltatoday.com.mt/news/national/143059/maltas_population_rose_to_588254_by_end_2025_nso"),
    ("3", "◆ Attard D. (11 Jul 2026). World Population Day: Malta’s Population Reaches Record 588,254. Lovin Malta.",
     "https://lovinmalta.com/news/local/world-population-day-maltas-population-reaches-record-588254/"),
    ("4", "Eurostat. Population change – demographic balance and crude rates at national level (demo_gind), updated "
          "30 Sep 2026, retrieved 5 Oct 2026.", "https://ec.europa.eu/eurostat/databrowser/view/demo_gind/default/table"),
    ("5", "MiŻien. Calculation script and outputs: tools/cc-088-report/calc.py; data/cc-088/checks.csv.", ""),
])
S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "5 Oct 2026", "First issue. Verdict Supported (high confidence); no right of reply needed.")])

build_report(Report(
    number="088", out=str(FIG / "report.pdf"), kicker="Statistics, Malta",
    title_lines=["Population", "588,254?"],
    subtitle_lines=["Testing the NSO’s World Population Day release", "against Eurostat’s demographic accounts"],
    quote_lines=["“The estimated total population of Malta and Gozo", "stood at 588,254 at the end of 2025.”"], quote_size=15,
    attribution="National Statistics Office, News Release NR 120/2026, 9 July 2026.",
    context="Up 2.4% on the previous year; net migration of 13,906 the main contributor.",
    verdict="Supported", verdict_note="Every figure reproduces from Eurostat; the release is internally consistent",
    footer_lines=["Version 1.0  ·  5 October 2026", "Status: no right of reply needed",
                  "Prepared from public sources and Eurostat data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Population 588,254 – NSO World Population Day 2026", version="1.0", date="5 October 2026",
    status_note="no right of reply needed",
    pdf_title="Population 588,254? Claim Check 088",
    pdf_subject="Tests the NSO's July 2026 population release against Eurostat demographic data",
    story=S))
