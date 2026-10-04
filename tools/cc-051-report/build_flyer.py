"""Claim Check 051 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="051", out=str(OUT / "flyer.pdf"), kicker="Nature and the sea, Malta",
    title_lines=["Over 30% of", "our seas protected?"],
    subtitle="A government claim, tested against EEA boundaries and EU reporting",
    quote_lines=["“Malta protects more than 30%", "of its maritime zone…”"],
    attribution="Environment Minister Miriam Dalli, 2025 (as quoted by Amphora Media)",
    context="ERA: “more than 35% of Malta’s Fisheries Management Zone”.",
    note="We measured the protected area from EEA maps.",
    verdict="Misleading", verdict_right=["True for one zone,", "not for Malta's seas."],
    cards=[("4,138 km²", GREEN, "Protected, as stated",
            "18 marine Natura 2000 sites, overlaps counted once (EEA)."),
           ("36%", GREEN, "Of the fisheries zone",
            "The 25-nautical-mile zone Malta manages."),
           ("5.5%", RED, "Of waters reported to the EU",
            "75,715 km²: the basis for the EU's 30% target."),
           ("18,600", ORANGE, "km² still needed",
            "To reach 30% on the basis Malta reports to the EU."),
           ("Paper", ORANGE, "Designation, not management",
            "Fishing and other uses continue in Natura 2000 sites.")],
    fair="ERA's own page names the fisheries zone. The problem is the minister's “maritime zone”, which reads as all of "
         "Malta's waters.",
    asks=["The minister's full statement.",
          "Malta's basis for the EU target.",
          "Management plans offshore.",
          "Monitoring results."],
    footer="Version 1.0  ·  4 October 2026  ·  Public data only  ·  Right of reply: Environment Ministry, ERA (not yet sent)",
    pdf_title="Claim Check 051 – Over 30% of our seas protected?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
