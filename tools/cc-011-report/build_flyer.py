"""Claim Check 011 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="011", out=str(OUT / "flyer.pdf"), kicker="Election pledges 2026, computed",
    title_lines=["Ten minutes’ walk", "to green space?"],
    subtitle="Labour’s 2026 green-space pledge, tested on open population and map data",
    quote_lines=["“Every person … no more than ten minutes’ walk", "from an open or green space.”"],
    attribution="Partit Laburista, manifesto 2026, priority 19 (our translation)",
    context="Now a government commitment: Labour won the election of 30 May 2026.",
    note="The PN’s net-zero Gozo pledge, checked here until v1.1, is now Claim Check 107.",
    verdict="Not measurable", verdict_right=["No definition,", "no baseline."],
    cards=[("99.9%", GREEN, "Any green or open space",
            "Share of residents already within 800 m (straight line). Read broadly, the pledge is already almost met."),
           ("55%", ORANGE, "Parks of at least 0.5 ha",
            "Within a realistic ten-minute walk. About 240,000 people are outside. Which one counts? Not said."),
           ("24%", RED, "WHO-style measure",
            "Within 300 m of a public park of at least 0.5 ha, the indicator WHO Europe suggests."),
           ("0", ORANGE, "Definitions published",
            "No minimum size, no baseline map, no target year in the manifesto."),
           ("3 parks", ORANGE, "Named in the manifesto",
            "Manoel Island, White Rocks, Fort Campbell: large parks, which suggests a stricter reading.")],
    fair="Green space near home is linked to better health, and the PN proposes a Parks Act to define “park”. The "
         "goal is sound; the question is whether it can be measured.",
    asks=["What counts as “open or green space”?",
          "Today’s baseline, and the method.",
          "A target year.",
          "The scope of the 40% carbon cut (priority 18)."],
    footer="Version 1.3  ·  5 October 2026  ·  Label as of 5 Oct 2026  ·  Draft pending right of reply from "
           "the Partit Laburista / Government",
    pdf_title="Claim Check 011 – Ten minutes’ walk to green space?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
