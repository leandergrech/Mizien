"""Claim Check 167 report. Run calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("The Ministry for Finance’s Economic Survey of October 2026 says: <b>“While final energy consumption increased in "
        "2024, energy intensity declined considerably between 2019 and 2024, indicating improved energy efficiency "
        "relative to economic activity.”</b> Its energy section puts the fall at 27.1%. We rebuilt the figure from Eurostat "
        "and looked at what drives it.", lead)]
S.append(key_points([
    ("The 27.1% is Eurostat’s published figure.",
     "Malta’s energy intensity of GDP fell from 266.6 to 194.3 kilograms of oil equivalent per thousand euro "
     "(2010 prices) between 2019 and 2024, exactly 27.1%."),
    ("That indicator counts fuel sold to ships.",
     "Eurostat divides gross available energy by GDP, and for Malta 69% of that energy in 2024 was bunker fuel sold "
     "to international shipping. Bunker sales fell 7% over the period."),
    ("Without bunkers the fall is smaller but still considerable.",
     "Gross inland consumption per unit of GDP fell 17%, and final energy per unit of GDP 14%. The EU’s published "
     "indicator fell 16%."),
    ("It is mostly GDP growth, not lower energy use.",
     "Real GDP rose 28% while final energy use rose 10%. Energy use per person fell 2%."),
    ("Verdict: largely supported (moderate confidence).",
     "Energy intensity did decline considerably on every measure. The 27.1% overstates the domestic change because it "
     "includes ship fuel, and the Survey does not say so."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("−27.1%", GREEN, "energy intensity 2019–2024, Eurostat’s published indicator"),
             ("−16.6%", AMBER, "the same without international marine bunkers"),
             ("69%", RED, "share of Malta’s gross available energy sold as ship bunkers, 2024"),
             ("+10%", GREY, "final energy consumption 2019–2024; real GDP +28%")]),
      Spacer(1, 4 * mm),
      up_down("A Survey note giving the intensity excluding bunkers, or a measure of efficiency (such as energy per "
              "unit of output by sector) that shows a similar fall.",
              "Evidence that the fall comes mainly from bunker volatility or GDP revisions rather than lower energy use "
              "per unit of output."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What drives the fall"),
          ("4", "Testing the claim"), ("5", "Verdict"), ("6", "Limitations")])
S.append(PageBreak())

S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The sentence is in the overview of chapter 2 of the Economic Survey (October 2026, printed p. 34, PDF p. 48). "
           "Section 2.6.3 (pp. 64–65) adds: “Between 2019 and 2024, the economy’s energy intensity declined by 27.1 per "
           "cent”, and gives final energy consumption as 0.602 Mtoe in 2024, up 3.8% on 2023 [1]. We read the Survey "
           "from the maintainer’s copy (finance.gov.mt refuses scripts). The data are from Eurostat [2–5]."))
S.append(std_table([
    [C("Source", cellh), C("What it says", cellh), C("Our access", cellh), C("Status", cellh)],
    [C("<b>Ministry for Finance</b>, Economic Survey 2026 [1]"),
     C("Energy intensity “declined considerably between 2019 and 2024”; −27.1%."), C("Maintainer’s copy; read."),
     C("<b>The claim</b>")],
    [C("<b>Eurostat</b>, nrg_ind_ei [2]"), C("Energy intensity of GDP, Malta and EU-27."), C("API, 17 Nov 2026."),
     C("<b>Primary data</b>")],
    [C("<b>Eurostat</b>, nrg_bal_s, nama_10_gdp, demo_gind [3–5]"),
     C("Energy balance (incl. bunkers), real GDP, population."), C("API, 17 Nov 2026."), C("<b>Primary data</b>")],
], [38 * mm, 66 * mm, 40 * mm, 26 * mm]))

S += [Spacer(1, 4 * mm), SectionHeading(2, "Method")]
S.append(P("We downloaded the published indicator and its parts for 2015–2024 (<i>data/cc-167/</i>). In "
           "<i>tools/cc-167-report/calc.py</i> we recomputed intensity with three numerators: gross available energy "
           "(Eurostat’s definition, including international marine bunkers), gross inland consumption (excluding them) and "
           "final energy consumption. We also computed final energy per person. Eurostat data are grade C. "
           "<b>Verdicts</b> follow the five-point scale in Appendix A."))

S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(3, "What drives the fall"))
S.append(fig(FIG / "fig1_change.png", width=CW * 0.98))
S.append(P("Figure 1. Change in energy intensity and related measures, Malta 2019–2024, and the EU-27 indicator.", cap))
S.append(P("Eurostat’s energy intensity of GDP divides gross available energy by GDP [2]. Gross available energy includes "
           "fuel sold to ships on international voyages. For most countries that is small, but Malta is a large "
           "bunkering hub. In 2024, 2,100 of its 3,065 thousand tonnes of oil equivalent (69%) were international marine "
           "bunkers [3]. This is why Malta’s published intensity is about twice the EU’s. Bunker sales fell 7% from 2019 "
           "to 2024, which lowers the indicator without any change in energy use on the islands."))
S.append(fig(FIG / "fig2_index.png", width=CW * 0.98))
S.append(P("Figure 2. Real GDP and energy use, index 2019 = 100.", cap))
S.append(P("Leaving bunkers out, gross inland consumption rose 7% and final energy consumption 10%, while real GDP rose "
           "28% [3, 4]. Energy use per unit of GDP therefore fell by 14–17%, close to the EU’s 16%. That is a "
           "considerable decline, as the Survey says. But it comes from output growing faster than energy use, not from "
           "using less: with population up 13%, final energy per person fell only 2% [5]. Calling this “improved energy "
           "efficiency relative to economic activity” is a fair description of the ratio. It is not evidence of "
           "efficiency gains in any sector, which the Survey does not claim."))

S.append(CondPageBreak(70 * mm))
S.append(SectionHeading(4, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> Energy intensity declined by 27.1% between 2019 and 2024"), C("Ministry for Finance [1]"),
     C("Matches Eurostat’s published indicator exactly. That indicator includes ship bunkers (69% of the energy)."),
     verd("ACCURATE", GREENC)],
    [C("<b>B.</b> It “declined considerably … indicating improved energy efficiency relative to economic activity”"),
     C("Ministry for Finance [1]"),
     C("Without bunkers, −14% to −17%, close to the EU’s −16%. The fall is driven by GDP growth: energy use rose 7–10%."),
     verd("FAIR, OVERSTATED", AMBER)],
    [C("<b>C.</b> Final energy consumption increased in 2024"), C("Ministry for Finance [1]"),
     C("0.602 Mtoe in 2024, up 3.8% on 2023 (Eurostat)."), verd("ACCURATE", GREENC)],
], [42 * mm, 26 * mm, 68 * mm, 34 * mm], valign="MIDDLE"))

S += [Spacer(1, 6 * mm), SectionHeading(5, "Verdict"),
      verdict_box("Largely supported", "Energy intensity fell considerably on every measure. The 27.1% includes fuel sold "
                  "to ships, and without it the fall is 14–17%. Confidence: moderate."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> The Survey uses the official indicator correctly and notes that energy consumption rose. The "
           "caveat is that, for Malta, the indicator is dominated by bunker fuel. That inflates the size of the fall. "
           "Readers could take the 27.1% as domestic efficiency, but domestic intensity fell by about the EU average. "
           "<b>What this verdict does not say.</b> It does not assess Malta’s energy-efficiency policies or targets. The "
           "related emissions-intensity claims are CC-146 and CC-147."))
S.append(CondPageBreak(40 * mm))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list(["From the Ministry for Finance: energy intensity excluding international marine bunkers, "
                        "alongside the published indicator, in future Surveys."]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag),
               P("Not needed for this verdict (maintainer rule of 5 October 2026).", small)], bg=AMBER_PALE, bar=AMBER)]
S += [Spacer(1, 6 * mm), SectionHeading(6, "Limitations")]
for l in ["The published intensity uses an older GDP vintage; recomputed with current GDP the bunker-inclusive fall is "
          "24.5% rather than 27.1%.",
          "Intensity falls with structural change (growth in low-energy services) as well as with efficiency; we do not "
          "separate the two.",
          "2025 energy data are not yet published."]:
    S.append(P("• " + l, bul))
S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Ministry for Finance. Economic Survey, October 2026, pp. 34 and 64–65 (maintainer copy).",
     "https://finance.gov.mt/wp-content/uploads/2026/10/Economic-Survey-2026-Final.pdf"),
    ("2", "Eurostat. Energy intensity (nrg_ind_ei), updated 21 Apr 2026, retrieved 17 Nov 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/nrg_ind_ei/default/table"),
    ("3", "Eurostat. Simplified energy balances (nrg_bal_s), updated 2 Jun 2026, retrieved 17 Nov 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/nrg_bal_s/default/table"),
    ("4", "Eurostat. GDP and main components (nama_10_gdp), chain-linked volumes (2010), updated 11 Nov 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/nama_10_gdp/default/table"),
    ("5", "Eurostat. Population change (demo_gind), average population, updated 27 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/demo_gind/default/table"),
    ("6", "MiŻien. Data and script: data/cc-167/; tools/cc-167-report/calc.py. Related: CC-146, CC-147.", ""),
])
S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "17 Nov 2026", "First issue. Verdict Largely supported (moderate confidence); no right of "
                    "reply needed.")])

build_report(Report(
    number="167", out=str(FIG / "report.pdf"), kicker="Energy",
    title_lines=["Declined", "considerably?"],
    subtitle_lines=["Testing the Economic Survey’s energy-", "intensity figure for 2019–2024"],
    quote_lines=["“…energy intensity declined considerably", "between 2019 and 2024…”"], quote_size=15,
    attribution="Ministry for Finance, Economic Survey, October 2026, p. 34.",
    context="Section 2.6.3 gives the fall as 27.1 per cent.",
    verdict="Largely supported", verdict_note="Figure right; ship bunkers inflate it",
    footer_lines=["Version 1.0  ·  17 November 2026", "Status: no right of reply needed",
                  "Prepared from public sources and open data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Energy intensity – Economic Survey 2026", version="1.0", date="17 November 2026",
    pdf_title="Declined considerably? Claim Check 167",
    pdf_subject="Tests the Economic Survey 2026 statement that Malta's energy intensity fell considerably in 2019-2024",
    story=S))
