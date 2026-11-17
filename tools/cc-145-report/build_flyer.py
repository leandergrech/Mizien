"""Claim Check 145 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, GREY, AMBER  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="145", out=str(OUT / "flyer.pdf"), kicker="Hunting and birds, Malta",
    title_lines=["Ten thousand", "hunters?"],
    subtitle="BirdLife Malta’s figures after the September 2026 storm, checked against the regulator’s licence data",
    quote_lines=["“Over 10,000 hunters [are]", "active at any one time.”"],
    attribution="Antonia Micallef, BirdLife Malta, to Mongabay, 5 October 2026",
    context="Also: 21 protected birds with shooting injuries collected, 14–21 September.",
    note="We read the Wild Birds Regulation Unit’s 2025 game-reporting data.",
    verdict="Largely supported", verdict_right=["The number holds; “at any", "one time” is not shown."],
    cards=[("10,091", GREEN, "Licences to hunt birds on land", "In 2025, one per licensee (WBRU)."),
           ("6.3%", AMBER, "Filed any catch report", "636 land licensees in 2025. Reports are needed only for a catch."),
           ("21", GREY, "Injured protected birds", "BirdLife’s own count for 14–21 Sep 2026. No list published."),
           ("0", GREY, "Counts of hunters out at once", "No published source measures this.")],
    fair="Read as “over 10,000 licensed hunters”, the figure is right to within 1%.",
    asks=["BirdLife Malta: the list of the 21 birds.", "WBRU: the 2026 licence count."],
    footer="Version 1.0  ·  17 November 2026  ·  Public data only  ·  No right of reply needed",
    pdf_title="Claim Check 145 – Ten thousand hunters?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
