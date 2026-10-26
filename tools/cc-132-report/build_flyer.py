"""Claim Check 132 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="132", out=str(OUT / "flyer.pdf"), kicker="Public transport, Malta",
    title_lines=["Below the EU", "average?"],
    subtitle="A sentence in the Commission’s 2026 Country Report, tested against Eurostat",
    quote_lines=["“58% of people in Malta reported never using", "public transport, below the EU average of 50.6%.”"],
    attribution="European Commission, 2026 Country Report for Malta, 3 June 2026",
    context="Annex 8 (transport), citing a Eurostat news article.",
    note="Eurostat’s survey of people aged 16 and over, 2024.",
    verdict="Largely supported", verdict_right=["Figures close;", "“below” should read “above”."],
    cards=[("50.6%", GREEN, "EU figure is exact", "Eurostat: 50.6% of people in the EU never used public transport."),
           ("58.6%", RED, "Malta’s share", "Eurostat’s table now shows 58.6%; the report says 58%."),
           ("+8.0", ORANGE, "Above, not below", "Malta is 8.0 points above the EU average."),
           ("7th", ORANGE, "Of 27 states", "Tied with Croatia; six states have a higher share of non-users.")],
    fair="The substance holds: Malta has more people who never use public transport than the EU average. One word "
         "reverses the comparison. This check does not assess Malta’s transport policy.",
    asks=["The table version that gives Malta as 58%.",
          "The survey question behind “never”.",
          "Before-and-after data on the free-fare scheme."],
    footer="Version 1.0  ·  26 October 2026  ·  Public data only  ·  No right of reply needed",
    pdf_title="Claim Check 132 – Below the EU average?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
