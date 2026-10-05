"""Claim Check 011 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="011", out=str(OUT / "flyer.pdf"), kicker="Election pledges 2026, computed",
    title_lines=["Two green pledges:", "can anyone check them?"],
    subtitle="Labour’s ten-minute green space and the PN’s net-zero Gozo, tested on open data",
    quote_lines=["“Every person … no more than ten minutes’ walk", "from an open or green space.”"],
    attribution="Partit Laburista, manifesto 2026, priority 19 (our translation)",
    context="And the PN programme: a plan for Gozo to be a Net-Zero Island by 2040, afforestation among the measures.",
    note="Both parties checked to the same standard. Labour now governs; the PN pledge is an opposition proposal.",
    verdict="Not substantiated", verdict_right=["No definition,", "no baseline."],
    cards=[("99.9%", GREEN, "Any green or open space",
            "Share of residents already within 800 m (straight line). Read broadly, the pledge is already almost met."),
           ("55%", ORANGE, "Parks of at least 0.5 ha",
            "Within a realistic ten-minute walk. About 240,000 people are outside. Which one counts? Not said."),
           ("No inventory", ORANGE, "Gozo emissions",
            "No official figure or boundary. We estimate about 157,000 t CO₂e a year."),
           ("6.5×", RED, "Gozo’s area as forest",
            "Needed to offset Gozo’s emissions by afforestation alone at a measured rate. Even optimistically: 2.3×."),
           ("2040", ORANGE, "A plan to make a plan",
            "The PN text relies on cuts first (solar, EVs, buildings); news summaries said “through afforestation”.")],
    fair="Green space near home is linked to better health, and island decarbonisation is EU policy. The goals are "
         "sound; the question is whether they can be measured.",
    asks=["Government: what counts as “open or green space”?",
          "Government: today’s baseline and a target year.",
          "PN: a Gozo emissions inventory and its boundary.",
          "PN: how much from cuts, forests and offsets."],
    footer="Version 1.1  ·  5 October 2026  ·  Open data, our analysis  ·  Draft pending right of reply from "
           "the Partit Laburista / Government and the Partit Nazzjonalista",
    pdf_title="Claim Check 011 – Two green pledges: can anyone check them?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
