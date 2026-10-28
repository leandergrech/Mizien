"""Claim Check 144 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="144", out=str(OUT / "flyer.pdf"), kicker="Nature and wildlife, Malta",
    title_lines=["Highest density", "of hunters in Europe?"],
    subtitle="A news report’s claim, tested against FACE’s country table and Eurostat",
    quote_lines=["“Malta has the highest density of", "hunters in all of Europe.”"],
    attribution="Mongabay (Spoorthy Raman), 5 October 2026",
    context="The outlet’s own sentence; it does not say density per what.",
    note="FACE’s table is from 2009–2010; no current official count was readable.",
    verdict="Largely supported", verdict_right=["True per area,", "not per inhabitant."],
    cards=[("47", ORANGE, "Hunters per km²",
            "On FACE’s count of 15,000 and Malta’s 316 km²; next highest is Ireland at 5.0."),
           ("9.5×", GREEN, "A wide margin",
            "Malta stays first per km² even at 10,000 hunters (32) or 5,000 (16)."),
           ("5th", RED, "Not first per head",
            "36 hunters per 1,000 inhabitants; Ireland 83, Finland 59, Cyprus 56, Norway 40."),
           ("2010", ORANGE, "Old comparison",
            "FACE’s table dates from 2009–2010; Malta’s current count is NGO-sourced or second-hand.")],
    fair="This check covers the density ranking only, not hunters as people or the legality of any shooting.",
    asks=["The WBRU’s current total of licensed hunters.",
          "A current country-by-country table.",
          "The 2015 paper’s basis for the ranking."],
    footer="Version 1.0  ·  28 October 2026  ·  Public data only  ·  No right of reply needed",
    pdf_title="Claim Check 144 – Highest density of hunters in Europe?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
