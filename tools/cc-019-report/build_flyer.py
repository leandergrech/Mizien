"""Claim Check 019 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="019", out=str(OUT / "flyer.pdf"), kicker="Land and trees, Malta",
    title_lines=["830,000 m² of green", "land built over?"],
    subtitle="A newsroom’s satellite estimate, tested against an independent land-cover model",
    quote_lines=["“Nearly 830,000 square metres of nature and cropland", "have been built up in Malta between 2018 and 2023.”"],
    attribution="Amphora Media, Green to Grey, 11 September 2026",
    context="The press is held to the same standard as everyone else.",
    note="Companion piece: “nearly 95%” of it was farmland.",
    verdict="Largely supported", verdict_right=["Figure stands up,", "probably low."],
    cards=[("1.4 km²", GREEN, "Independent estimate",
            "Net new built-up land first mapped in 2020–21, in a second 10 m land-cover model."),
           ("0.26%", GREEN, "Arithmetic checks out",
            "Share of Malta’s land; 116 pitches; a quarter to 0.3 of Comino."),
           ("65%", ORANGE, "Mostly cropland",
            "Independent data; 31% was shrub or grass. Amphora: nearly 95%."),
           ("Noisy", ORANGE, "Single-year maps mislead",
            "Built-up area swings by up to 27 km² from year to year; only consistent change counts."),
           ("#1", ORANGE, "Highest land take in Europe",
            "EEA, 2012–2018, as a share of country area: about 0.92 km² in Malta.")],
    fair="Amphora described its figure as conservative, and the independent data agree. The farmland share needs a "
         "stated basis.",
    asks=["Amphora’s map polygons.",
          "Basis of the 95% figure.",
          "Development-zone status.",
          "The 2006–2012 EEA figure."],
    footer="Version 1.1  ·  5 October 2026  ·  Public data only  ·  Right of reply: Amphora Media (not yet sent)",
    pdf_title="Claim Check 019 – 830,000 m2 of green land built over?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
