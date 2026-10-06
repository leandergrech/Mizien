"""Claim Check 039 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="039", out=str(OUT / "flyer.pdf"), kicker="Water, checked",
    title_lines=["A net-zero-impact", "water utility?"],
    subtitle="WSC’s 2019 promise of 4 billion litres less groundwater, tested against its own production reports",
    quote_lines=["“The Corporation’s ground water abstraction will be", "reduced by 4 billion litres per year.”"],
    attribution="Water Services Corporation, news release, 2 April 2019",
    context="Same release: “much more water with less energy”.",
    note="Baseline and date are not stated; we use 2016, the last report before the project framework that we read.",
    verdict="Not measurable", verdict_right=["No baseline,", "no date."],
    cards=[("−2.0 million m³", GREEN, "Groundwater, 2025 vs 2016",
            "WSC borehole production fell from 13.5 to 11.5 million m³: about half of the pledged 4.0."),
           ("0.4", ORANGE, "Only 0.4 million m³ in 2024",
            "2023 and 2024 were barely below 2016; one year is not yet a trend."),
           ("+50%", RED, "More desalination",
            "RO output rose from 18.6 to 27.9 million m³ between 2016 and 2025."),
           ("−33%", ORANGE, "Needed to stay flat",
            "Specific energy would have to fall by a third for RO electricity not to rise."),
           ("No total", ORANGE, "WSC’s electricity use",
            "Total kWh by year was not found; RO is only part of it.")],
    fair="Groundwater’s share of WSC production fell from 42% to 29% while total production grew by about 23%. "
         "Lower energy use and water security are sound goals; the question is whether the promises can be checked.",
    asks=["The baseline year and date behind “4 billion litres”.",
          "Total electricity use (kWh) by year.",
          "Whether all project components are complete.",
          "Specific energy of each RO plant by year."],
    footer="Version 1.1  ·  6 October 2026  ·  Label as of 6 Oct 2026  ·  Pending right of reply from the "
           "Water Services Corporation",
    pdf_title="Claim Check 039 – A net-zero-impact water utility?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
