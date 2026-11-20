"""Claim Check 158 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, GREY, AMBER  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="158", out=str(OUT / "flyer.pdf"), kicker="Climate governance, Malta",
    title_lines=["Significant", "strides?"],
    subtitle="The National Audit Office’s ClimateScanner review, recomputed and set beside the emissions record",
    quote_lines=["“This Review … shows that Malta has made", "significant strides in climate action.”"],
    attribution="National Audit Office, press release, 7 October 2025",
    context="On its review of Malta’s climate action using the ClimateScanner framework.",
    note="Every score was recomputed from the report’s item ratings; the tool’s handbook was read for its scale.",
    verdict="Largely supported", verdict_right=["Scores correct; they measure", "policies, not emissions results."],
    cards=[("6.92", GREEN, "Overall score, reproduced",
            "Average of Governance 6.55, Public Policies 8.00 and Finance 6.20."),
           ("12 of 18", GREEN, "Components rated strengths",
            "At or above 6.66; none at 3.33 or below."),
           ("6.66", AMBER, "The “intermediate” tier",
            "An item with many aspects present but room for improvement scores 6.66, the strength mark."),
           ("+41%", RED, "Effort-sharing emissions, 2024",
            "Against 2005, with a −19% target for 2030. Not something the tool scores.")],
    fair="The NAO’s report says plainly that ClimateScanner records whether policies exist, not their results. "
         "The press release does not repeat this.",
    asks=["NAO: say in public summaries that the tool does not measure results.",
          "Climate Action Authority: evidence for “progress in tackling climate change”."],
    footer="Version 1.0  ·  16 November 2026  ·  Public data only  ·  No right of reply needed",
    pdf_title="Claim Check 158 – Significant strides?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
