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
    subtitle="An airport’s carbon claims, tested against its figures and public registries",
    quote_lines=["“…set to avoid the emission of an average", "of 1,000 tonnes of carbon dioxide annually.”"],
    attribution="Malta International Airport plc, press release, 25 May 2026",
    context="A €12.5 million airfield electrification programme; the airport also holds ACA Level 3+.",
    note="Company wording; the saving is a projection to 2028.",
    verdict="Not substantiated", verdict_right=["Neutral within its scope;", "the 1,000 t not shown."],
    cards=[("Level 3+", GREEN, "Neutrality confirmed",
            "ACA lists the airport at Level 3+; 3,780 of 5,450 t of credits found retired."),
           ("0.7%", ORANGE, "Inside the boundary",
            "Share of the reported 2025 footprint that ‘neutral’ covers; Scope 3 is outside."),
           ("€12.5m", GREEN, "Programme confirmed",
            "EU list shows a €5.39m grant: power at 35 stands, charging for e-buses."),
           ("≈300 t", ORANGE, "Diesel units alone",
            "A year if every turnaround used one for 22.5 min (gross, indicative)."),
           ("1,000 t", RED, "No method published",
            "Baseline, hours and grid electricity behind the figure are not shown.")],
    fair="MIA reports its Scope 3 openly and says the programme addresses it. We did not assess credit quality; "
         "one credit block was not found in the registries.",
    asks=["The calculation behind the 1,000 tonnes.",
          "Ground-power and APU parts of Scope 3.",
          "The third credit block’s registry record.",
          "Why Scope 1 nearly doubled in 2025."],
    footer="Version 1.1  ·  5 October 2026  ·  Public data only  ·  Draft pending right of reply from Malta "
           "International Airport",
    pdf_title="Claim Check 030 – Carbon neutral, and what else?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
