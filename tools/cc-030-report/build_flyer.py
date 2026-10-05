"""Claim Check 030 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="030", out=str(OUT / "flyer.pdf"), kicker="Airport emissions, Malta",
    title_lines=["Carbon neutral,", "and what else?"],
    subtitle="An airport’s carbon claims, tested against its own assured figures",
    quote_lines=["“…set to avoid the emission of an average", "of 1,000 tonnes of carbon dioxide annually.”"],
    attribution="Malta International Airport plc, press release, 25 May 2026",
    context="A €12.5 million airfield electrification programme; the airport also holds ACA Level 3+.",
    note="Company wording; the saving is a projection to 2028.",
    verdict="Largely supported", verdict_right=["Neutral within its scope;", "saving plausible, unproven."],
    cards=[("5,444 t", GREEN, "Neutrality adds up",
            "Scope 1 + 2 + business travel against 5,450 t of credits bought (2025)."),
           ("99.3%", ORANGE, "Scope 3 sits outside",
            "Share of the airport’s reported footprint, mostly aircraft; Level 3+ does not cover it."),
           ("1,000 t", GREEN, "Projected saving a year",
            "From 2028: 18.5% of Scope 1 + 2, but 0.14% of Scope 3."),
           ("−22%", ORANGE, "Direct emissions vs 2015",
            "Scope 1 + 2 rose 8% in 2025; the company’s target is −65% by 2030."),
           ("?", RED, "Gross or net?",
            "Method, baseline and grid electricity for the 1,000 t are not published.")],
    fair="The company reports its Scope 3 openly and says the programme addresses it. We did not check the "
         "carbon credits' quality or the ACA directory.",
    asks=["The calculation behind the 1,000 tonnes.",
          "The 2025 ACA certificate and credit retirements.",
          "Ground-power use by stand, by year.",
          "Measured savings once stands operate."],
    footer="Version 1.0  ·  5 October 2026  ·  Public data only  ·  No right of reply needed",
    pdf_title="Claim Check 030 – Carbon neutral, and what else?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
