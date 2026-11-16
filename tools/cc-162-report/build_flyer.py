"""Claim Check 162 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="162", out=str(OUT / "flyer.pdf"), kicker="Climate targets, Malta",
    title_lines=["Still more in 2030", "than in 2005?"],
    subtitle="The Commission’s 2026 sentence on Malta, tested against the data and the law",
    quote_lines=["“…This means Malta is projected to emit", "more in 2030 than in 2005.”"],
    attribution="European Commission, EU Climate Action Progress Report 2026, COM(2026) 601, p. 46, 9 Nov 2026",
    context="“Malta’s gap to target is 49 and 61 percentage points, exceeding its 19% reduction target.”",
    note="Effort-sharing sectors: transport, buildings, waste, farming, small industry, refrigerant gases.",
    verdict="Supported", verdict_right=["Reproduced from Malta’s", "own projections and EU law."],
    cards=[("49 / 61", GREEN, "The gap is right",
            "Points of gap to the −19% target, with planned / existing measures: 48.7 and 61.1 on our count."),
           ("+30% / +42%", RED, "Above 2005 in 2030",
            "1,324 / 1,450 kt against 1,021 kt in 2005."),
           ("+37%", ORANGE, "Already above in 2025",
            "1,400 kt in 2025 (approximated); over the yearly limit every year since 2022."),
           ("Unchanged", GREEN, "Malta’s projections",
            "The EEA’s 2026 dataset still holds Malta’s March 2025 submission, as for the 2025 report."),
           ("1.4 Mt", ORANGE, "Left after flexibilities",
            "Over 2021–30, after the ETS flexibility and land credits: to buy from other states or cut.")],
    fair="The −19% target was set in 2018 from GDP per capita (2005 is the base year). The Commission says the EU as a whole "
         "keeps a surplus of about 140 Mt, so Malta’s shortfall can be bought, and none had been reported.",
    asks=["How Malta will cover its 2026–2030 excess, and at what cost.",
          "Updated projections from Malta (next due 2027).",
          "The Commission’s staff working document SWD(2026) 331.",
          "Why the EEA revised Malta’s 2023 emissions by 35 kt."],
    footer="Version 1.0  ·  16 November 2026  ·  Public data and EU law  ·  No right of reply needed",
    pdf_title="Claim Check 162 – Still more in 2030 than in 2005?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
