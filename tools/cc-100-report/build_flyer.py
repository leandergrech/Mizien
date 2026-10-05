"""Claim Check 100 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, GREY  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="100", out=str(OUT / "flyer.pdf"), kicker="Tourism and travel, Malta",
    title_lines=["Over 10 million", "airport passengers?"],
    subtitle="Malta International Airport's 2025 figure, tested against Eurostat",
    quote_lines=["“…full-year traffic for 2025 up to 10,061,969 passenger", "movements, marking a 12.3% increase…”"],
    attribution="Malta International Airport plc, company announcement 461/2026, 14 January 2026",
    context="Full-year traffic update to the Malta Stock Exchange.",
    note="A passenger movement is one arrival or one departure.",
    verdict="Supported", verdict_right=["Independent statistics confirm", "the total and the growth."],
    cards=[("10.07m", GREEN, "Eurostat, 2025",
            "Passengers carried at Malta's airport: 0.09% above the company's 10,061,969."),
           ("+12.3%", GREEN, "Growth over 2024",
            "From 8,968,239 passengers in 2024. Both sources agree."),
           ("1st", GREEN, "Year above 10 million",
            "Traffic was 7.3 million in 2019 and 7.8 million in 2023."),
           ("×2", GREY, "Movements, not people",
            "A return trip counts twice: roughly five million round journeys."),
           ("9.3m", ORANGE, "An outdated page",
            "The company's Facts and Figures page still shows its 2025 forecast.")],
    fair="The figure is accurate. Whether this growth is sustainable is a different question, asked in other checks.",
    asks=["MIA: update the Facts and Figures page.", "Readers: movements are not travellers.",
          "See CC-030 on airport emissions.", "See CC-083–085 on tourism."],
    footer="Version 1.0  ·  5 October 2026  ·  Public data only  ·  No right of reply needed",
    pdf_title="Claim Check 100 – Over 10 million airport passengers?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
