"""Claim Check 167 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, GREY, AMBER  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="167", out=str(OUT / "flyer.pdf"), kicker="Energy, Malta",
    title_lines=["Declined", "considerably?"],
    subtitle="The Economic Survey’s energy-intensity figure, rebuilt from Eurostat with and without ship fuel",
    quote_lines=["“…energy intensity declined considerably", "between 2019 and 2024…”"],
    attribution="Ministry for Finance, Economic Survey, October 2026",
    context="The Survey puts the fall at 27.1 per cent.",
    note="We recomputed the indicator from Eurostat’s energy balance and GDP.",
    verdict="Largely supported", verdict_right=["Right figure; ship bunkers", "inflate the size of the fall."],
    cards=[("−27.1%", GREEN, "Published indicator", "Matches Eurostat exactly, 2019–2024."),
           ("69%", RED, "Of the energy is ship fuel", "International marine bunkers, 2024."),
           ("−16.6%", AMBER, "Without bunkers", "Close to the EU’s −15.9%."),
           ("+28% / +10%", GREY, "GDP / final energy", "Output grew faster than energy use.")],
    fair="The Survey notes that energy consumption rose; it does not say the indicator includes ship fuel.",
    asks=["Ministry for Finance: report intensity excluding marine bunkers too."],
    footer="Version 1.0  ·  17 November 2026  ·  Public data only  ·  No right of reply needed",
    pdf_title="Claim Check 167 – Declined considerably?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
