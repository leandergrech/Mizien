"""Claim Check 040 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="040", out=str(OUT / "flyer.pdf"), kicker="Water, Malta",
    title_lines=["Is water use", "per head low?"],
    subtitle="A public statement, tested against Eurostat",
    quote_lines=["“Per capita water consumption, today", "stands at around 110l/cap/day.”"],
    attribution="Manuel Sapiano, Energy and Water Agency, IWRA 1st Island Water Congress, 2024",
    context="Slide 10 of the keynote slide deck.",
    note="The keynote makes no comparison with other countries; that wording came from the intake record.",
    verdict="Largely supported", verdict_right=["Figure is close,", "“low” is not benchmarked."],
    cards=[("120", GREEN, "Eurostat: households, 2024",
            "Maltese households used about 120 litres per person per day (estimate); 116 in 2022."),
           ("+9%", ORANGE, "Above the slide’s 110",
            "Within about 10% of the keynote’s “around 110”; the slide does not define the measure."),
           ("176", ORANGE, "All uses of the public supply",
            "Litres per resident per day in 2024, including services such as hotels."),
           ("13th", RED, "Mid-table in the EU",
            "13th lowest of 19 states with data, 8% above the median of 111 litres."),
           ("?", GREEN, "Tariff effect untested",
            "No evidence in the deck that tariffs held use down; the schedule was not obtained.")],
    fair="The keynote does not claim Malta is lower than other countries. Its own deck says natural freshwater is "
         "insufficient even at efficient demand. We read slides, not a transcript.",
    asks=["The source and definition of the 110 litres.",
          "WSC billed domestic use, 2015–2024.",
          "The tariff schedule and its estimated effect.",
          "Population base used per person."],
    footer="Version 1.0  ·  7 October 2026  ·  Public data only  ·  No right of reply needed",
    pdf_title="Claim Check 040 – Is water use per head low?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
