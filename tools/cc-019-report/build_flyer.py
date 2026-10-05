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
    subtitle="A newsroom’s satellite estimate, tested against its own map and an independent land-cover model",
    quote_lines=["“Nearly 830,000 square metres of nature and cropland", "have been built up in Malta between 2018 and 2023.”"],
    attribution="Amphora Media, Green to Grey, 11 September 2026",
    context="The press is held to the same standard as everyone else.",
    note="Companion piece: “nearly 95%” of it was farmland.",
    verdict="Largely supported", verdict_right=["Matches its own map;", "not independently confirmed."],
    cards=[("0.83 km²", GREEN, "Amphora’s map adds up",
            "Its 397 published polygons cover 828,429 m²: “nearly 830,000” is exact."),
           ("2–3%", RED, "Little overlap",
            "of an independent model’s new built-up land falls inside Amphora’s polygons."),
           ("96%", ORANGE, "Farmland, if grass counts",
            "Cropland plus grass, of the area with a known 2018 class; 37% has no class."),
           ("0.26%", GREEN, "Arithmetic checks out",
            "Share of Malta’s land; 116 pitches; a quarter to 0.3 of Comino."),
           ("93.7 ha", GREEN, "EEA figures check out",
            "New artificial land 2012–2018 in the EEA’s change maps; Amphora quotes 92 ha.")],
    fair="Amphora published its map, so anyone can check it. The independent model is noisy and may be the one that is "
         "wrong about 2018.",
    asks=["Basis of the 95% figure.",
          "Imagery year: 2023 or 2025?",
          "Class of the unknown 37%.",
          "Development-zone status."],
    footer="Version 1.2  ·  5 October 2026  ·  Public data only  ·  Right of reply: Amphora Media (not yet sent)",
    pdf_title="Claim Check 019 – 830,000 m2 of green land built over?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
