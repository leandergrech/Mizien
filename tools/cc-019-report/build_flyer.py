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
    subtitle="A newsroom’s satellite estimate, tested against its own map, high-resolution images and a land-cover model",
    quote_lines=["“Nearly 830,000 square metres of nature and cropland", "have been built up in Malta between 2018 and 2023.”"],
    attribution="Amphora Media, Green to Grey, 11 September 2026",
    context="The press is held to the same standard as everyone else.",
    note="Companion piece: “nearly 95%” of it was farmland.",
    verdict="Not substantiated", verdict_right=["Built over by 2025, not 2023;", "a third was not farmland."],
    cards=[("0.83 km²", GREEN, "Amphora’s map adds up",
            "Its 397 published polygons cover 828,429 m²: “nearly 830,000” is exact."),
           ("72.5%", GREEN, "Imagery confirms most",
            "of a random sample of that area went from green to grey (2015–16 to 2025 images)."),
           ("59%", ORANGE, "Fields, not 95%",
            "of the sampled land was fields before; 64% with orchards. The rest: scrub, garrigue."),
           ("55%", ORANGE, "By 2023, not 830,000",
            "of Amphora’s area was grey by May 2023: about 456,000 m². The rest followed by 2025."),
           ("93.7 ha", GREEN, "EEA figures check out",
            "New artificial land 2012–2018 in the EEA’s change maps; Amphora quotes 92 ha.")],
    fair="Amphora published its map, so anyone can check it, and most of the land in it really was built over. Our "
         "imagery check is by eye on 40 draws, and fallow fields can look like scrub.",
    asks=["Basis of the 95% figure.",
          "Imagery year: 2023 or 2025?",
          "Class of the unknown 37%.",
          "Development-zone status."],
    footer="Version 1.2  ·  5 October 2026  ·  Public data only  ·  Right of reply: Amphora Media (not yet sent)",
    pdf_title="Claim Check 019 – 830,000 m2 of green land built over?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
