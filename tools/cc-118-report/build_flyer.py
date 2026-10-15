"""Claim Check 118 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="118", kicker="Water, Malta",
    out=str(OUT / "flyer.pdf"),
    title_lines=["Second-highest", "water stress?"],
    subtitle="The Council’s figures on Malta’s water, tested",
    quote_lines=["“…reached 66.7% in the third quarter of 2023,", "the second-highest level among EU Member States.”"],
    attribution="Council of the European Union, draft Recommendation on Malta, 3 July 2026",
    context="Recital (30), citing Malta’s Third River Basin Management Plan.",
    note="The Council relays figures from other bodies.",
    verdict="Largely supported", verdict_right=["Every figure reproduces from", "EEA and Eurostat data."],
    cards=[("66.7%", RED, "Matches the EEA", "Malta’s worst quarter (Q3) in 2023; only Cyprus (92.1%) is higher."),
           ("58%", GREEN, "Surface waters, by number", "11 of 19 bodies good or high; 97% by area, as coastal waters dominate."),
           ("45%", ORANGE, "Good chemical status", "9 of 20 bodies, counting the territorial sea; 47% without it."),
           ("82%", RED, "Groundwater area, poor quantity", "4 of 15 bodies, but the largest aquifer is in poor status."),
           ("100%", RED, "Groundwater, poor chemistry", "All 15 bodies fail good chemical status.")],
    fair="Eurostat’s annual 2023 figure ranks Malta third (Romania higher) and is 30%, not 67%; the Council says ‘seasonal’.",
    asks=["The Third RBMP’s status tables.", "Why EEA and Eurostat differ for Romania.", "The adopted Council text."],
    footer="Version 1.0  ·  15 October 2026  ·  Public data only  ·  No right of reply needed",
    pdf_title="Claim Check 118 – Second-highest water stress?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
