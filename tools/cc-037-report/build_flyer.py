"""Claim Check 037 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="037", out=str(OUT / "flyer.pdf"), kicker="Pollution, Malta",
    title_lines=["Is Malta first in the EU", "for reported pollution?"],
    subtitle="A media claim, tested against Eurostat survey data",
    quote_lines=["“35% of people in Malta reported exposure to", "pollution in 2023 — the highest share in the EU.”"],
    attribution="Amphora Media, 2026 Election Guidebook: The Environment, 12 May 2026",
    context="Citing Eurostat; the series is not named in the guidebook.",
    note="The survey asks about pollution, grime or other environmental problems: what people report.",
    verdict="Supported", verdict_right=["Accurate figures;", "reported, not measured."],
    cards=[("34.7%", GREEN, "The figure is right",
            "Eurostat EU-SILC, 2023: people reporting pollution, grime or other environmental problems."),
           ("12.2%", GREEN, "Nearly three times the EU",
            "EU-27 average in 2023. The ratio is 2.8."),
           ("1st", GREEN, "Highest in the EU",
            "Greece is second at 20.5%. Malta was first in all 17 survey years since 2005."),
           ("41% → 27%", ORANGE, "Fell, then rose again",
            "Share reporting problems: 41.4% in 2011, 26.5% in 2017, 34.7% in 2023."),
           ("Reported", ORANGE, "Perception, not measurement",
            "The intro says “exposure”; the survey records what households report.")],
    fair="Amphora’s body text uses the survey’s own wording, and its note that higher earners reported more "
         "problems matches the data (35.6% against 30.1%).",
    asks=["The report Amphora cites for the figure.",
          "Measured exposure data to set beside this survey.",
          "Why 2021 and 2022 have no data (survey module)."],
    footer="Version 1.0  ·  5 October 2026  ·  Public data only  ·  No right of reply needed (Supported)",
    pdf_title="Claim Check 037 – Is Malta first in the EU for reported pollution?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
