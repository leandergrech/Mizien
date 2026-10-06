"""Claim Check 094 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="094", out=str(OUT / "flyer.pdf"), kicker="Climate targets, Malta",
    title_lines=["More in 2030", "than in 2005?"],
    subtitle="The Commission’s reading of Malta’s projections, tested against the data and the law",
    quote_lines=["“…This means Malta is projected to emit", "more in 2030 than in 2005.”"],
    attribution="European Commission, EU Climate Action Progress Report 2025, COM(2025) 668, p. 30, 6 Nov 2025",
    context="“Malta’s gap to target is 49 and 61 percentage points, exceeding its 19% reduction target.”",
    note="Effort-sharing sectors: transport, buildings, waste, farming, small industry, refrigerant gases.",
    verdict="Supported", verdict_right=["Reproduced from Malta’s", "own projections and EU law."],
    cards=[("49 / 61", GREEN, "The gap is right",
            "Points of gap to the −19% target, with planned / existing measures: 48.7 and 61.1 on our count."),
           ("+30% / +42%", RED, "Above 2005 in 2030",
            "1,324 / 1,450 kt against 1,021 kt in 2005. True for every 2005 figure we found."),
           ("+41%", ORANGE, "Already above in 2024",
            "1,437 kt in 2024 (approximated). Over the yearly limit in 2022, 2023 and 2024."),
           ("1st of 27", RED, "Largest gap in the EU",
            "In percentage points: Malta 49, Ireland 20, Germany 13. In tonnes Malta’s gap is small (0.5 Mt)."),
           ("1.6 Mt", ORANGE, "Left after flexibilities",
            "Over 2021–30, after the ETS flexibility and land credits: to buy from other states or cut.")],
    fair="Malta’s plan says the target rests on 2005 forecasts; in fact −19% was set in 2018 from GDP per capita "
         "(2005 is the base year). Population has grown 41% since 2005, and effort-sharing emissions per person "
         "are flat.",
    asks=["How Malta will cover its 2026–2030 excess, and at what cost.",
          "Approximated 2025 emissions and the 2027 projections.",
          "The effect of the new ETS2 on transport and buildings.",
          "Measures for transport, flat at 737 kt in both projections."],
    footer="Version 1.0  ·  6 October 2026  ·  Public data and EU law  ·  No right of reply needed",
    pdf_title="Claim Check 094 – More in 2030 than in 2005?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
