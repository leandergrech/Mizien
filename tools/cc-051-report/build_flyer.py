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
    note="We mapped every protected site against all of Malta's waters.",
    verdict="Misleading", verdict_right=["36% within 25 nm;", "5.5% of Malta's waters."],
    cards=[("4,138 km²", GREEN, "Protected, as stated",
            "18 marine Natura 2000 sites, all within 25 nautical miles."),
           ("36%", GREEN, "Of the fisheries zone",
            "The 25-nm zone ERA names: 15% of the waters Malta reports."),
           ("5.5%", RED, "Of waters reported to the EU",
            "75,715 km²: the basis for the EU's 30% target."),
           ("0 km²", RED, "Protected beyond 25 nm",
            "Where 85% of the waters Malta reports to the EU lie."),
           ("0.6%", ORANGE, "Of the deep sea protected",
            "Waters over 1,000 m deep: a quarter of the total.")],
    fair="ERA's own page names the fisheries zone, and the EU's 30% is an EU-wide target. The problem is the minister's "
         "“maritime zone”, which reads as all of Malta's waters.",
    asks=["The minister's full statement.",
          "Malta's basis for the EU target.",
          "Management plans offshore.",
          "Monitoring results."],
    footer="Version 1.1  ·  4 October 2026  ·  Public data only  ·  Right of reply: Environment Ministry, ERA (not yet sent)",
    pdf_title="Claim Check 051 – Over 30% of our seas protected?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
