"""Claim Check 025 report. Run fetch.py, calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []

# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("In its statement to the COP30 high-level segment (November 2025), the Government of Malta said: <b>“Malta "
        "has already reduced its per capita emissions by over 44% compared to 2005 and emissions per unit of GDP by "
        "more than 80%, demonstrating our commitment to decoupling growth from emissions.”</b> We tested both "
        "figures against Eurostat’s greenhouse-gas inventory, GDP and population series.", lead)]
S.append(key_points([
    ("The 44% figure is right.",
     "Eurostat gives −46% to 2023 (the latest year available when the statement was made) and −48.5% to 2024; the EU "
     "average is −34% and −36%. Malta passed −44% in 2016. Population growth of 41% explains about half of it "
     "(see CC-003)."),
    ("The “more than 80%” figure depends on the price basis, which the statement does not give.",
     "Against GDP at current prices, Malta’s emissions intensity fell 82% to 2023 and 84% to 2024. Against GDP in "
     "chain-linked volumes, the usual way to compare intensity over time, it fell 70% and 72%. No year to 2024 "
     "reaches −80% in volumes. The gap is a price effect: Malta’s GDP deflator rose about 72%."),
    ("The decoupling claim holds.",
     "Real GDP grew 161% between 2005 and 2024 while total emissions fell 27%: absolute decoupling, which the "
     "research literature calls rare [8 ◆]. Most of the fall came from power generation (CC-003)."),
    ("What the sentence does not say.",
     "Total emissions fell less than the EU average (−27% against −33%), and CC-003 shows that Malta’s emissions in "
     "the sectors under its binding 2030 target are above their 2005 level. We have read only the quoted paragraph of "
     "the statement, not the rest, so we cannot say whether it addresses this elsewhere."),
    ("Verdict: largely supported (moderate confidence).",
     "The substance, strong decoupling, is backed by the data. The headline “80%” holds only at current prices; in "
     "volumes it is about 70%."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("−48%", GREEN, "Emissions per person, 2005–2024 (claim: over 44%; EU −36%)"),
             ("−72%", ORANGE, "Emissions per unit of GDP in volumes, 2005–2024 (claim: over 80%; EU −48%)"),
             ("−84%", GREY, "The same ratio at current prices, the only basis on which “over 80%” holds"),
             ("+161%", GREEN, "Real GDP growth, 2005–2024, while emissions fell 27%")]),
      Spacer(1, 4 * mm),
      up_down("None: this is not the top of the scale only because of the price basis. Supported would need the statement, or a "
              "published government source, to name a basis on which “more than 80%” holds and say so.",
              "Evidence that the government’s own source uses volumes and obtains a different result; or the rest of "
              "the statement presenting the figures without the context needed to read them (then Misleading would "
              "have to be tested, as in CC-003)."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the data show"),
          ("4", "Where the evidence points different ways"), ("5", "Testing the claim"),
          ("6", "Verdict and requests for evidence"), ("7", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The wording comes from “COP30 Malta National Statement” on the UNFCCC site [1], read by the maintainer "
           "from the file itself (a Word document behind a <i>.pdf</i> address, dated 15–18 November 2025) and "
           "recorded in <i>literature/CC-025/primary-source.md</i>. The statement was delivered on behalf of Malta’s "
           "Minister for the Environment, Energy and Public Cleanliness; the document does not name the person who "
           "read it, so we attribute it to the Government of Malta. Our automated access to the UNFCCC file was "
           "refused (a bot check), so we relied on the supplied text, which covers the opening line and the paragraph "
           "quoted above."))
S.append(std_table([
    [C("Source", cellh), C("What it says", cellh), C("Our access", cellh), C("Status", cellh)],
    [C("<b>Government of Malta</b>, COP30 national statement, Nov 2025 [1]"),
     C("“Importantly, Malta has already reduced its per capita emissions by over 44% compared to 2005 and emissions "
       "per unit of GDP by more than 80%, demonstrating our commitment to decoupling growth from emissions.”"),
     C("The paragraph, as supplied by the maintainer (5 Oct 2026). Rest of the statement not read."),
     C("<b>The claim</b>")],
    [C("<b>Climate Action Authority</b>, press release, 13 Nov 2025 (CC-003) [2]"),
     C("Per-capita fall of 44% (EU 34%); emissions per unit of GDP down 81.6% (EU 61.9%). Different speaker, same "
       "figures, same week."),
     C("Read in CC-003 (Wayback copy)."), C("Context")],
    [C("<b>Eurostat</b>, env_air_gge, nama_10_gdp, nama_10_pe [3–5]"),
     C("Emissions inventory, GDP in current prices and chain-linked volumes, population."),
     C("Downloaded 5 Oct 2026 (data/cc-025/)."), C("<b>Primary data</b>")],
], [38 * mm, 74 * mm, 36 * mm, 22 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("RELATION TO CC-003", tag),
               P("CC-003 checked the same 44% figure in the Climate Action Authority’s release and rated that release "
                 "<i>Misleading</i> because it left out the Commission’s 2030 projection for the same report. This "
                 "check is separate: a different speaker and setting (a statement to a UN conference), and a second "
                 "figure (intensity per unit of GDP). For the per-person figure we reuse CC-003’s data and analysis "
                 "and do not repeat them in full.", small)], bg=BLUE_PALE, bar=BLUE), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Question.</b> Are the two figures accurate, and does the sentence fairly describe “decoupling growth "
           "from emissions”?"))
S.append(P("<b>Evidence.</b> The test is statistical. On 5 October 2026 we downloaded Eurostat’s greenhouse-gas "
           "inventory (env_air_gge, total excluding land use and international transport, 1990–2024), GDP "
           "(nama_10_gdp, current prices and chain-linked volumes at 2020 prices) and population (nama_10_pe) for Malta "
           "and the EU-27 (<i>tools/cc-025-report/fetch.py</i>), and recomputed every percentage with a script "
           "(<i>calc.py</i>; outputs in <i>data/cc-025/checks.csv</i>). No Eurostat status flags apply to the Malta "
           "values used. The statement gives no year and no GDP basis; we report 2023 (the last inventory year "
           "available in November 2025) and 2024. The 2024 emissions file is the same vintage as CC-003’s."))
S.append(P("<b>Why the GDP basis matters.</b> Emissions per unit of GDP divides emissions by GDP. If GDP is measured "
           "in current prices, inflation inflates the denominator and the ratio falls faster than the economy’s real "
           "efficiency improves. Comparing intensity over time is normally done in volumes (prices of a fixed year), "
           "so that only real output is counted. Both are computable; they give different numbers."))
S.append(P("<b>Grades.</b> Official statistics are grade C in our scale; the one peer-reviewed review used [8] is grade "
           "C (review) and is read as an abstract. <b>Verdicts</b> follow the five-point scale in Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(3, "What the data show"))
S.append(fig(FIG / "fig1_index.png", width=CW * 0.95))
S.append(P("Figure 1. Malta, indexed to 2005: real GDP, total emissions, emissions per person and emissions per unit "
           "of GDP on two bases. Only the dashed current-price line passes the −80% mark.", cap))
S.append(P("Malta’s real GDP grew 161% from 2005 to 2024, its population 41% and its total emissions fell 27%. Per "
           "person that is −48.5% (EU −36%), matching “over 44%”. Per unit of GDP it is −72% in volumes (EU −48%) and "
           "−84% at current prices (EU −65%). In 2023, the year the statement could have used, the figures are −70% "
           "and −82% (EU −46% and −62%)."))
S.append(fig(FIG / "fig2_bars.png"))
S.append(P("Figure 2. The three measures, Malta and EU-27, to 2023 and 2024. Dotted lines mark the claimed −44% and −80%.", cap))
S.append(P("The Climate Action Authority’s “81.6% (EU 61.9%)” [2] is close to our current-price results for 2023 "
           "(−81.9%, EU −62.2%), which suggests the same basis. That is our inference; neither document states "
           "the basis."))
S.append(callout([P("WHY THE TWO INTENSITY FIGURES DIFFER", tag),
                  P("Malta’s nominal GDP rose 350% from 2005 to 2024, its real GDP 161%. The ratio of the two (the implicit "
                    "GDP price level) rose 72%. On a logarithmic split, about 30% of the current-price intensity fall is "
                    "the price effect; the rest is real. The EU-27 price level rose 48% over the same period, so "
                    "the comparison with the EU holds on either basis: Malta’s intensity fell more.", small)],
                 bg=BLUE_PALE, bar=BLUE))

# ================================================================== 4
S.append(Spacer(1, 4 * mm))
S.append(SectionHeading(4, "Where the evidence points different ways"))
S.append(contested("Is “decoupling growth from emissions” fair?", "LARGELY YES", AMBER,
                   "Real GDP +161% while total emissions −27% (2005–2024). Absolute decoupling in this sense is "
                   "unusual in the literature [8 ◆].",
                   "The fall is concentrated in one step: after the 2015 interconnector and gas conversion (CC-003), "
                   "total emissions reached a low in 2016 and have since risen 18% to 2024 (calc.py). Total "
                   "emissions fell less than the EU average (−27% vs −33%). Emissions in the sectors under the national "
                   "target are not falling (CC-003). Production-based inventory only: it excludes international aviation and shipping and "
                   "emissions embodied in imports.",
                   "Both sides are accurate. “Decoupling” is a statement about GDP and emissions together, and the data "
                   "show it. It is not a statement about the 2030 target, so the second column limits how far the "
                   "sentence can be read, not whether it is true.", label_a="EVIDENCE FOR THE CLAIM",
                   label_b="CAVEATS"))

# ================================================================== 5
S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(5, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> Per-capita emissions down over 44% since 2005"), C("Govt of Malta [1]"),
     C("Reproduced from Eurostat: −46% to 2023, −48.5% to 2024; Malta passed −44% in 2016. The same figure was "
       "checked in CC-003. About half of it is population growth."), verd("ACCURATE", GREENC)],
    [C("<b>B.</b> Emissions per unit of GDP down more than 80%"), C("Govt of Malta [1]"),
     C("Holds at current prices (−82% to 2023, −84% to 2024). In chain-linked volumes it is −70% and −72%; no year "
       "reaches −80%. The statement names neither basis."), verd("TRUE ONLY AT CURRENT PRICES", AMBER)],
    [C("<b>C.</b> …demonstrating our commitment to decoupling growth from emissions"), C("Govt of Malta [1]"),
     C("Real GDP +161%, total emissions −27%: absolute decoupling over 2005–2024. A statement of commitment is "
       "not itself testable; the data show the decoupling it refers to."), verd("SUPPORTED", GREENC)],
], [42 * mm, 18 * mm, 76 * mm, 34 * mm], valign="MIDDLE"))

# ================================================================== 6
S += [Spacer(1, 6 * mm), SectionHeading(6, "Verdict and requests for evidence"),
      verdict_box("Largely supported", "The substance, strong decoupling, is backed by the data; the “80%” holds only "
                  "at current prices. Confidence: moderate."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) The 44% figure is accurate and matches Eurostat and CC-003. (2) The “more than 80%” "
           "figure is reproducible only with GDP at current prices; in volumes the fall is about 70–72%. That is a "
           "caveat on the size of the figure, not on its direction: Malta’s intensity fell much more than the EU’s on "
           "either basis. (3) Real GDP more than doubled while emissions fell, which is the decoupling the sentence "
           "describes. We rate the whole claim <i>Largely supported</i> rather than <i>Supported</i> because the "
           "headline figure is stated without the basis it needs, and it overstates the fall by about ten points on "
           "the usual basis. Confidence is moderate because we have read the supplied paragraph only, and the "
           "statement’s own source and method are not published."))
S.append(P("<b>What this verdict does not say.</b> It does not say Malta is on course for its 2030 target, which is "
           "a separate question (CC-003: Misleading for the authority’s release, which left out the projection; CC-094; "
           "CC-011). It does not say anyone chose the current-price basis to flatter the result: we found no document "
           "stating the basis. A fuller statement would read: <i>“Emissions per person fell 44% and per unit of GDP "
           "about 70% in real terms, while real GDP more than doubled; total emissions fell 27%.”</i>"))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "The source and method for “over 44%” and “more than 80%”, including the year, the emissions scope and whether GDP is in "
    "current prices or volumes.",
    "The full text of the statement, to check whether it mentions the 2030 effort-sharing projection.",
    "The name of the person who delivered the statement, if it is to be attributed beyond the Government of Malta.",
]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag),
               P("Not needed for this verdict (maintainer rule of 5 October 2026: a reply is sought only for "
                 "<i>Not substantiated</i>, <i>Misleading</i> or <i>Contradicted</i>). The requests above remain open to "
                 "the Environment Ministry and the Climate Action Authority.", small)], bg=AMBER_PALE, bar=AMBER)]

# ================================================================== 7
S += [Spacer(1, 6 * mm), SectionHeading(7, "Limitations")]
for l in ["We read only the paragraph supplied by the maintainer; our own download of the UNFCCC file was refused. "
          "Other parts of the statement may qualify or add to it.",
          "The statement gives no year, scope or GDP basis. We report 2023 and 2024, and the Eurostat total excluding "
          "land use and international transport (TOTX4_MEMO). Eurostat’s other total (TOTXMEMO) changes Malta’s "
          "intensity results by 0.1 point or less (EU-27: up to 0.8 points).",
          "Eurostat’s 2026 inventory may differ slightly from the national submission behind the statement.",
          "The literature [8] was read as an abstract only; it is context for the word “decoupling”, not evidence for "
          "the figures.",
          "Production-based emissions only: emissions embodied in imports and international aviation and shipping are "
          "outside the series."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Government of Malta (Nov 2025). COP30 Malta National Statement, high-level segment. UNFCCC. "
          "(Quoted paragraph as supplied by the maintainer, 5 Oct 2026; file is a Word document behind a .pdf address.)",
     "https://unfccc.int/sites/default/files/resource/MALTA_cop30cmp20cma7_HLS_ENG.pdf"),
    ("2", "Climate Action Authority (13 Nov 2025). Malta strengthens its contribution toward the EU’s climate goals. "
          "Press release (read in CC-003 from a Wayback copy).",
     "https://climateaction.gov.mt/press/malta-strengthens-its-contribution-toward-the-eus-climate-goals/"),
    ("3", "Eurostat. Greenhouse gas emissions by source sector (env_air_gge), retrieved 5 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/env_air_gge/default/table"),
    ("4", "Eurostat. GDP and main components (nama_10_gdp), updated 2 Oct 2026, retrieved 5 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/nama_10_gdp/default/table"),
    ("5", "Eurostat. Population and employment (nama_10_pe), retrieved 5 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/nama_10_pe/default/table"),
    ("6", "MiŻien. CC-003 report and data (per-person figure, 2030 projection): claims/CC-003; data/cc-003/.", ""),
    ("7", "MiŻien. Calculation script and outputs: tools/cc-025-report/calc.py; data/cc-025/checks.csv.", ""),
    ("8", "Haberl H. et al. (2020). A systematic review of the evidence on decoupling of GDP, resource use and GHG "
          "emissions, part II: synthesizing the insights. <i>Environmental Research Letters</i> 15(6):065003. "
          "doi:10.1088/1748-9326/ab842a. (Abstract read; open access, CC BY.)",
     "https://doi.org/10.1088/1748-9326/ab842a"),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "5 Oct 2026", "First issue. Verdict Largely supported (moderate confidence); "
                                         "no right of reply needed.")])

build_report(Report(
    number="025", out=str(FIG / "report.pdf"), kicker="Statistics and EU data",
    title_lines=["Emissions down 44%", "per person, 80%", "per unit of GDP?"],
    subtitle_lines=["Testing Malta’s COP30 statement on emissions", "against Eurostat data"],
    quote_lines=["“Malta has already reduced its per capita emissions by over", "44% compared to 2005 and emissions per unit of GDP by",
                 "more than 80%.”"], quote_size=14,
    attribution="Government of Malta, COP30 national statement, November 2025.",
    context="Delivered on behalf of the Minister for the Environment, Energy and Public Cleanliness.",
    verdict="Largely supported", verdict_note="The 80% holds only at current prices; about 70% in real terms",
    footer_lines=["Version 1.0  ·  5 October 2026", "Status: no right of reply needed",
                  "Prepared from public sources and Eurostat data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Per-person and per-GDP emissions – Malta at COP30", version="1.0", date="5 October 2026",
    status_note="no right of reply needed",
    pdf_title="Emissions down 44% per person, 80% per unit of GDP? Claim Check 025",
    pdf_subject="Tests the Government of Malta's COP30 statement on per-capita and per-GDP emissions",
    story=S))
