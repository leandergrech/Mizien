"""Claim Check 156 report. Run fetch_data.py and figures.py first. Output: out/report.pdf"""
import csv
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

OUT = HERE / "out"
FIG = HERE / "out"
LG = colors.HexColor("#8DB36B")
S = []

S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("Business Now’s subtitle of 17 August 2026 says: <b>“Maltese waters have suffered a downgrade from best in "
        "Europe to bang average.”</b> The EEA’s classifications bear it out. Malta rated 86 of its 87 bathing waters "
        "excellent in 2016 (98.9%), third of the 22 EU states with coastal bathing waters, behind Slovenia (16 sites) "
        "and Cyprus. In 2025 it rated 77 (88.5%), eleventh of 22 and level with the EU coastal average of 88.3%. "
        "“Best in Europe” is generous for a third place, and the ‘downgrade’ is in the share rated excellent, not in "
        "safety: no Maltese site was poor in either year.", lead)]
S.append(key_points([
    ("The article’s two Malta counts are right.", "86 of 87 sites excellent in 2016 and 77 in 2025, both as the EEA "
     "classes them. The other 2025 results are 8 good and 2 sufficient."),
    ("‘Best in Europe’ is a fair shorthand, not literal.", "In 2016 Malta was third of 22 coastal states "
     "(Slovenia 100% of 16 sites, Cyprus 99.1% of 112, Malta 98.9% of 87). It stayed in the top five until 2022."),
    ("‘Bang average’ describes 2025 closely.", "Malta’s 88.5% sits 0.2 points above the pooled EU coastal share "
     "(88.3%) and in the middle of the ranking (11th of 22; ten states higher)."),
    ("The fall is in the top class only.", "Every Maltese site met at least the directive’s minimum standard in "
     "2025, as in 2016. Rank is sensitive to small differences: Croatia, 12th, is at 88.3%."),
    ("The week-13 figure is not tested.", "The article’s 56 of 87 excellent in week 13 of 2026 is from the outlet; "
     "we could not open the Directorate’s weekly file. A weekly count is also not the same measure as a season class."),
]))
S += [Spacer(1, 3 * mm), VerdictMeter(1), Spacer(1, 2 * mm),
      tiles([("86 → 77", RED, "Maltese sites rated excellent, 2016 → 2025 (of 87)"),
             ("3rd → 11th", ORANGE, "Malta’s rank among 22 EU coastal states"),
             ("88.5%", BLUE, "Malta 2025 versus 88.3% EU coastal average"),
             ("0 poor", GREEN, "Maltese sites rated poor in 2016 or 2025")]),
      Spacer(1, 3 * mm),
      up_down("A ranking in 2016 that placed Malta first or a one-class gap to the leaders would move it to Supported; "
              "the EEA data do not show that (Malta was third).",
              "A different EEA count for either season; or a like-for-like EU average for 2025 that put Malta clearly "
              "above or below it (we find 0.2 points)."), Spacer(1, 4 * mm)]
S += toc([("1", "Claim and sources"), ("2", "What the indicator measures"), ("3", "Malta against the EU"),
          ("4", "Where the evidence points different ways"), ("5", "Testing the claim"),
          ("6", "Verdict and limits")])
S.append(PageBreak())

S += [SectionHeading(1, "Claim and sources"),
      P("The article, “Water quality of Maltese beaches registers stark decline” by Robert Fenech, was published by "
        "<i>Business Now</i> on 17 August 2026. Its subtitle, in the outlet’s own voice, reads: “Maltese waters have "
        "suffered a downgrade from best in Europe to bang average.” This is a statement by an outlet about public data, "
        "not by an authority. Business Now says its figures come from the European Environment Agency and from the "
        "Environmental Health Directorate’s weekly updates [1]. We read the article through a summarising fetch tool, "
        "so details other than the subtitle wording, which the tool quoted exactly, are second-hand "
        f"{DIAM} and every figure we rely on is recomputed from the EEA data."),
      std_table([
          [C("Source", cellh), C("What it establishes", cellh), C("Use", cellh)],
          [C("Business Now, 17 Aug 2026 [1]"), C("Subtitle wording; 86 of 87 excellent in 2016 and 77 in 2025; "
             f"56 of 87 in week 13 of 2026 {DIAM}."), C("Claim wording")],
          [C("EEA bathing-water map service, layer 3 [2]"), C("Class of every bathing water in every EU-27 state, "
             "seasons 2015–2025."), C("Primary statistical series")],
          [C("EEA Malta country factsheet 2025 [3]"), C("77 of 87 excellent, 8 good, 2 sufficient in 2025."),
           C("Cross-check")],
          [C("Directive 2006/7/EC [4]"), C("Classes and how a season’s class is assessed."), C("Method")],
          [C("Claim Check 005 [5]"), C("Malta’s own series, checked site by site against a second EEA dataset."),
           C("Cross-check")],
      ], [52 * mm, 87 * mm, 31 * mm]),
      Spacer(1, 3 * mm),
      P("<b>Method.</b> From the EEA service we took the class of each of the 22,010 EU-27 bathing waters for 2015–2025 "
        "and computed, per state and season, the share rated excellent among waters with a class that season, for "
        "coastal waters (inland waters are excluded because Malta has none). A state’s rank is one plus the number of "
        "states with a higher share; ties share a rank. The pooled EU coastal share is total excellent over total "
        "waters. Malta’s counts equal those in Claim Check 005. Data and scripts: <i>data/cc-156/</i>, "
        "<i>tools/cc-156-report/</i>.", body)]

S += [SectionHeading(2, "What the indicator measures"),
      P("The Bathing Water Directive classifies each site as excellent, good, sufficient or poor from two faecal "
        "indicators, <i>Escherichia coli</i> and intestinal enterococci. The class is assessed on the samples of the "
        "season and the preceding seasons (normally four), so it is a statistical summary, not a single week’s "
        "reading [4]. ‘Sufficient’ is the minimum the directive requires. A fall from excellent to good is a real "
        "change in the faecal-indicator statistics, but it is not a fall below the standard. The article itself "
        f"says that even an average result reflects a high level of safety {DIAM}.")]

S += [CondPageBreak(110 * mm), SectionHeading(3, "Malta against the EU"),
      P("Malta’s count fell from 86 excellent sites in 2016 to 77 in 2025. Over the same decade its position among "
        "EU coastal states fell from third to eleventh (Figure 1). Malta ranked second to fifth in every season "
        "until 2022, then ninth in 2023 and 2024 and eleventh in 2025. Counting all bathing waters, including inland "
        "ones, Malta went from third of 27 to ninth of 27."),
      fig(FIG / "fig1_rank.png"),
      P("Figure 1. Malta’s rank by share of coastal bathing waters rated excellent, seasons 2015–2025.", cap),
      CondPageBreak(130 * mm),
      P("Figure 2 shows each state’s share in 2016 and 2025. Several states moved more than Malta in either direction: "
        "Bulgaria rose from 63% to 97%, Belgium fell from 90% to 63%. Malta’s 2025 share (88.5%) lies between "
        "Germany (89.3%) and Croatia (88.3%), within 0.2 points of the pooled EU coastal share of 88.3%."),
      fig(FIG / "fig2_countries.png"),
      P("Figure 2. Share of coastal bathing waters rated excellent, EU-27 states, 2016 (open) and 2025 (filled).", cap)]

S += [CondPageBreak(100 * mm), SectionHeading(4, "Where the evidence points different ways")]
S.append(contested(
    "Q1  Was Malta ‘best in Europe’ and is it now ‘bang average’?", "LARGELY SUPPORTED", LG,
    "In 2016 Malta’s 98.9% placed it third of 22 coastal states, and in the top five for eight seasons (2015–2022); in 2025 it is "
    "eleventh of 22 with a share 0.2 points above the pooled EU coastal average. Both ends of the article’s "
    "description match the ranking.",
    "Third is not first: Slovenia (16 sites, 100%) and Cyprus (112 sites, 99.1%) were ahead in 2016, and the "
    "differences at the top are one or two sites. The rank in 2025 is also fragile (Croatia at 88.3% is 12th), and "
    "‘average’ rests on a share, not on safety: no Maltese site was poor in either year.",
    "<b>For this claim:</b> the direction and size of the change are right and the endpoints are fairly described. "
    "‘Best in Europe’ is a loose rendering of ‘among the top three’, so the verdict is Largely supported, not Supported."))

S += [CondPageBreak(95 * mm), SectionHeading(5, "Testing the claim")]
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> Malta was once ‘best in Europe’ for bathing water"),
     C("2016: 98.9% excellent, third of 22 coastal states, behind Slovenia (16 sites) and Cyprus; top five until "
       "2022 [2]."), verd("LARGELY SUPPORTED", LG)],
    [C("<b>B.</b> 86 of 87 beaches were excellent in 2016 against 77 in 2025"),
     C("EEA: 86 in 2016 and 77 in 2025 [2, 3, 5]."), verd("SUPPORTED", GREENC)],
    [C("<b>C.</b> Malta is now ‘bang average’"),
     C("88.5% against the pooled EU coastal 88.3%; 11th of 22 [2]. Average on the share rated excellent; every "
       "site passes the minimum standard."), verd("SUPPORTED", GREENC)],
    [C(f"<b>D.</b> 56 of 87 excellent in week 13 of 2026 {DIAM}"),
     C("Not tested: the Directorate’s weekly file could not be opened, and a weekly count is not a season "
       "classification, so it is not comparable with B."), verd("NOT TESTED", GREY)],
], [52 * mm, 88 * mm, 30 * mm], valign="MIDDLE"))

S += [Spacer(1, 6 * mm), SectionHeading(6, "Verdict and limits"),
      verdict_box("Largely supported", "Malta: 86 of 87 excellent in 2016 (3rd of 22 coastal states); 77 of 87 in 2025 "
                  "(11th, level with the EU average). Confidence: high on the figures, medium on ‘best in Europe’."),
      Spacer(1, 3 * mm),
      P("<b>Why.</b> The article’s counts are the EEA’s, and the EEA data show both the fall and Malta’s move from the "
        "top group to the middle of the EU ranking. The subtitle compresses ‘third’ into ‘best’, and it measures the "
        "top class, so ‘downgrade’ should not be read as unsafe water."),
      P("<b>Limits.</b> This check covers the bathing-water classification only, using data Malta reports to the EEA; "
        "it does not assess other pollutants, marine ecology or health outcomes, nor why individual sites changed "
        "class. Ranks depend on how many sites each state reports. Week-13 figures are untested."),
      P("Under our standards a right of reply is sought only where a check finds a claim Not substantiated, "
        "Misleading or Contradicted, so none is needed for this check. The report remains a draft for maintainer "
        "review.", small),
      Spacer(1, 4 * mm), SectionHeading(None, "References")]
S += references([
    (1, "Robert Fenech, “Water quality of Maltese beaches registers stark decline”, <i>Business Now</i>, 17 August "
        "2026. Read 11 November 2026 through a summarising fetch tool.",
     "https://businessnow.mt/water-quality-of-maltese-beaches-registers-stark-decline/"),
    (2, "EEA, bathing-water map service BathingWater_Dyna_WM_2025, layer 3 (class of each bathing water, 2015–2025). "
        "Queried 11 November 2026; data/cc-156/country_excellent_share.csv.",
     "https://water.discomap.eea.europa.eu/arcgis/rest/services/BathingWater/BathingWater_Dyna_WM_2025/MapServer/3"),
    (3, "EEA, <i>Bathing water quality in the season of 2025: Malta</i> (country factsheet), as cited in Claim Check 005.",
     "https://www.eea.europa.eu/en/topics/in-depth/bathing-water/state-of-bathing-water/bathing-water-country-factsheets-2025/mt-bathing-water-country-factsheet-2025.pdf/@@download/file"),
    (4, "Directive 2006/7/EC of the European Parliament and of the Council concerning the management of bathing "
        "water quality, Article 4 and Annex II.", "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32006L0007"),
    (5, "Miżien, Claim Check 005 (92% excellent bathing water), data/cc-005/.",
     "https://github.com/leandergrech/Mizien/tree/main/data/cc-005"),
])
S += [Spacer(1, 4 * mm)]
S += revision_log([
    ("1.0", "11 Nov 2026", "First issue. No right of reply needed."),
])

build_report(Report(number="156", out=str(OUT / "report.pdf"), kicker="Bathing water, Malta",
    title_lines=["‘Best in Europe’", "to ‘bang average’?"],
    subtitle_lines=["An outlet’s headline claim, tested against", "ten seasons of EEA bathing-water data"],
    quote_lines=["“Maltese waters have suffered a downgrade", "from best in Europe to bang average.”"],
    attribution="Business Now (Robert Fenech), 17 August 2026",
    context="86 of 87 sites excellent in 2016 (3rd of 22 EU coastal states); 77 in 2025 (11th, level with the average).",
    verdict="Largely supported", verdict_note="Right on the change; ‘best’ is third.",
    footer_lines=["Draft for maintainer review", "Status: derived"],
    running_head="Bathing water: best to bang average", version="1.0", date="11 November 2026",
    pdf_title="Claim Check 156 – Best in Europe to bang average?",
    pdf_subject="Malta bathing water classification, EU ranking 2015 to 2025", story=S))
