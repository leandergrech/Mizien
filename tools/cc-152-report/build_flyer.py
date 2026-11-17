"""Claim Check 152 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, GREY, AMBER  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="152", out=str(OUT / "flyer.pdf"), kicker="Air quality, Malta",
    title_lines=["Missing the", "NOx target?"],
    subtitle="ERA’s warning on the 2030 nitrogen-oxide ceiling, checked against EU law and Eurostat",
    quote_lines=["“…a significant risk of non-compliance", "with the NOx ceiling for 2030.”"],
    attribution="Environment and Resources Authority, June 2026",
    context="Draft update of the National Air Pollution Control Programme.",
    note="We checked the ceiling in the directive and the emissions record.",
    verdict="Supported", verdict_right=["Projection almost double", "the legal ceiling."],
    cards=[("3.88 kt", RED, "Projected for 2030", "With existing measures (ERA)."),
           ("1.98 kt", GREEN, "2030 ceiling", "79% below 2005, set in EU law."),
           ("4.4 kt", AMBER, "Emitted in 2024", "Flat at 4.1–4.6 kt since 2017 (Eurostat)."),
           ("42.6%", GREY, "From road transport", "Ferries add 15.5% (2023).")],
    fair="ERA’s warning is against Malta’s own interest; most planned transport measures are not yet quantified.",
    asks=["Final programme: quantified effect of the additional transport measures."],
    footer="Version 1.0  ·  17 November 2026  ·  Public data only  ·  No right of reply needed",
    pdf_title="Claim Check 152 – Missing the NOx target?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
