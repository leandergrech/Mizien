"""Claim Check 117 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, GREY  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="117", out=str(OUT / "flyer.pdf"), kicker="Waste, Malta",
    title_lines=["Did Malta miss its", "recycling targets?"],
    subtitle="The European Commission's July 2026 reasoned opinion, tested against Eurostat",
    quote_lines=["“…Malta missed the targets for total packaging,", "paper and cardboard and metals.”"],
    attribution="European Commission, July infringements package, 8 July 2026",
    context="Same page: Malta failed the 50% municipal recycling target “to be reached by 2020”; reasoned opinion INFR(2024)2135.",
    note="We downloaded Eurostat's recycling rates and compared them with the targets the Commission names.",
    verdict="Largely supported", verdict_right=["The findings reproduce;", "one year of one target was met."],
    cards=[("10.9%", RED, "Municipal recycling, 2020",
            "Target 50%. Lowest of the EU-27 on Eurostat's indicator; 16.7% in 2024 against 48.1% for the EU-27."),
           ("4 of 4", RED, "Years below target, total packaging",
            "40.0%, 36.8%, 30.8% and 43.4% in 2020 to 2023, against 55%. Paper and cardboard also below 60% every year."),
           ("3 of 4", ORANGE, "Years below target, metals",
            "27.1%, 13.0% and 15.2% in 2021 to 2023 against 50%. In 2020 it was 57.2%, above target."),
           ("2 months", GREY, "To respond",
            "A reasoned opinion is the second stage. The Commission may then refer the case to the Court of Justice."),
           ("?", GREY, "Not on the Commission's list",
            "Eurostat also shows plastics, wood and glass (2022) below target. We cannot say why they are not listed.")],
    fair="The Commission's findings hold up against Eurostat. A reasoned opinion is the Commission's position, not a "
         "court ruling, and we read its summary page, not the decision text.",
    asks=["Commission: the decision text and data for INFR(2024)2135.", "Government: its reply to the opinion, if published.",
          "Readers: this is a procedure, not a verdict of the Court."],
    footer="Version 1.0  ·  13 October 2026  ·  Public data only  ·  No right of reply needed",
    pdf_title="Claim Check 117 – Did Malta miss its recycling targets?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
