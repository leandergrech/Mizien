"""Claim Check 129 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, GREY  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="129", out=str(OUT / "flyer.pdf"), kicker="Air quality, Malta",
    title_lines=["Malta’s air pollution", "programme"],
    subtitle="The Commission's July 2025 statement, checked against the Directive",
    quote_lines=["“To date, these Member States have not submitted", "to the Commission the required updates.”"],
    attribution="European Commission, July infringements package, 17 July 2025",
    context="Letters of formal notice to six Member States (Malta: INFR(2025)2088).",
    note="A letter of formal notice is a first step, not a ruling.",
    verdict="Largely supported", verdict_right=["Case and legal duty confirmed;", "submission record not seen."],
    cards=[("INFR", GREEN, "The case exists", "Malta is named with INFR(2025)2088 in the Commission's own text."),
           ("4 yrs", GREEN, "The duty", "Directive 2016/2284 Art. 6(3): update at least every four years; first due 1 April 2019."),
           ("16–27", ORANGE, "Months late", "At the notice, from 16.5 months (March 2020 version) to 27.5 months (1 April 2023)."),
           ("Jun 2026", GREY, "Draft update", "A draft revised programme went to consultation, per Malta News Agency (second-hand)."),
           ("?", GREY, "Not seen", "The Commission's record of what Malta submitted could not be opened.")],
    fair="This is about a missing update, not about how clean Malta's air is. Other checks cover air quality.",
    asks=["ERA/Commission: date of the latest submission.", "ERA: publish the 2026 draft's submission date.",
          "See CC-034 and CC-035 on air quality.", "Notice is not a court finding."],
    footer="Version 1.0  ·  20 October 2026  ·  Public data only  ·  No right of reply needed",
    pdf_title="Claim Check 129 – Malta's air pollution programme"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
