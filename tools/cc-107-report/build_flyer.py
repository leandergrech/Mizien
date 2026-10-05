"""Claim Check 107 flyer (split from Claim Check 011). Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="107", out=str(OUT / "flyer.pdf"), kicker="Election pledges 2026, computed",
    title_lines=["A net-zero", "Gozo by 2040?"],
    subtitle="The Nationalist Party’s 2026 pledge, tested on open data and a measured forest",
    quote_lines=["“A clear and realistic plan so that by", "2040 Gozo becomes a Net-Zero Island.”"],
    attribution="Partit Nazzjonalista, programme Nifs Ġdid 2026, chapter Għawdex (our translation)",
    context="News summaries said Gozo would become net zero “through afforestation”.",
    note="Until 5 October 2026 this was part of Claim Check 011 (Labour’s green-space pledge).",
    verdict="Not substantiated", verdict_right=["No baseline,", "no pathway."],
    cards=[("118–154 kt", ORANGE, "Gozo energy CO₂ a year",
            "2016–20, from a 2023 study for the EU islands secretariat. No official inventory."),
           ("~157 kt", ORANGE, "Our estimate",
            "Gozo’s population × Malta’s emissions per person. Close to the study’s highest year."),
           ("4.9–6.3×", RED, "Gozo’s area as forest",
            "Needed to offset those emissions by afforestation alone, at a measured semi-arid rate."),
           ("2040", ORANGE, "A plan to make a plan",
            "No baseline, boundary or pathway in the programme."),
           ("Cuts first", GREEN, "The PN’s own text",
            "Solar, EVs, buildings and restoration; afforestation is one measure, not the method.")],
    fair="Island decarbonisation is EU policy, and an energy baseline for Gozo already exists to build on. The "
         "goal is sound; the question is whether it can be measured.",
    asks=["A Gozo emissions inventory and its boundary.",
          "How much from cuts, forests and offsets.",
          "The area to be afforested, and the rate assumed.",
          "Will the plan start from the 2023 baseline?"],
    footer="Version 1.0  ·  5 October 2026  ·  Open data, our analysis  ·  Draft pending right of reply from "
           "the Partit Nazzjonalista",
    pdf_title="Claim Check 107 – A net-zero Gozo by 2040?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
