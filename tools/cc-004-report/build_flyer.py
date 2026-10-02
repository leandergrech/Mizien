"""Claim Check 004 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="004", out=str(OUT / "flyer.pdf"), kicker="Waste and recycling, Malta",
    title_lines=["More waste separated,", "but how much recycled?"],
    subtitle="A public claim, tested against Eurostat, NSO and EU targets",
    quote_lines=["“Malta continues to make strong progress", "in waste management.”"],
    attribution="Ministry for the Environment, press release PR260072en, 19 January 2026",
    context="Minister Dalli: the waste plan “is working”; 412 million kg diverted from landfill in five years.",
    note="EU targets are measured on waste actually recycled after sorting, not on kilograms separated.",
    verdict="Not substantiated", verdict_right=["Separation is up;", "the outcome isn’t shown."],
    cards=[("Rising", GREEN, "Separation is up",
            "NSO confirms more organic, grey-bag, glass and deposit-scheme waste. Landfilled municipal waste fell 21% since 2019."),
           ("16.7%", RED, "Actually recycled, 2024",
            "Share of municipal waste recycled. EU average 48%. The 2025 target is 55%."),
           ("79%", RED, "Still landfilled",
            "Of treated municipal waste in 2024. The 2020 target was missed by a wide margin."),
           ("412 vs 271", ORANGE, "Thousand tonnes",
            "Ministry’s “diverted” figure vs Eurostat’s recycled or recovered waste, 2020–24."),
           ("No year", ORANGE, "For “141 to 95.5 million kg”",
            "The mixed-waste fall of 32% has no start year and is not a published statistic.")],
    fair="Mandatory separation, organic collection and gate fees are measures that research links to higher "
         "recycling. The direction is right; the claim is about how far it has got.",
    asks=["Scope, years and method behind 412 million kg.",
          "How much separated waste is rejected and landfilled.",
          "Why no composting or digestion is reported as recycling.",
          "The year Malta expects to reach 55% recycled."],
    footer="Version 1.0  ·  2 October 2026  ·  Public data only  ·  Draft pending right of reply from the "
           "Environment Ministry and WasteServ",
    pdf_title="Claim Check 004 – More waste separated, but how much recycled?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
