"""Claim Check 075 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, AMBER, GREEN, ORANGE  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="075", out=str(OUT / "flyer.pdf"), kicker="Cars per person, Malta",
    title_lines=["Is Malta seventh in the", "EU for cars per person?"],
    subtitle="A media report of Eurostat figures, tested against the data",
    quote_lines=["“Malta is ranked number seven, just between Germany",
                 "and Poland … with 585 cars per 1,000 inhabitants.”"],
    attribution="Lovin Malta, 21 September 2024",
    context="The outlet’s own text, citing Eurostat. No year is given for the figure.",
    note="Eurostat counts passenger cars at year end per resident; the figures match 2022.",
    verdict="Largely supported", verdict_right=["Right for 2022;", "the year is not stated."],
    cards=[("585", GREEN, "The figure is right",
            "Eurostat, 2022: passenger cars per 1,000 inhabitants in Malta. No flag on the value."),
           ("7th of 27", GREEN, "So is the rank",
            "Between Germany (587) and Poland (584). All 27 Member States report for 2022."),
           ("2022", AMBER, "But which year?",
            "The article calls the data “as of 2023”. Its figures are 2022’s; on 2023 figures Malta is 11th."),
           ("14th", ORANGE, "Lower since",
            "571 in 2025, below the EU-27’s 584. The population grew faster than the number of cars."),
           ("1,014", GREEN, "Cars per km² of land",
            "Most in the EU by far in 2022 (Netherlands 261). Malta has 313 km² of land, not 246.")],
    fair="The number of cars in Malta rose every year to 335,693 at the end of 2025; cars per person fell because the "
         "population grew faster (+39.6% against +34.5% since the end of 2012).",
    asks=["The graphic Lovin Malta used, and its data date.",
          "When Eurostat first published the 2023 values.",
          "NSO: licensed versus garaged and rented cars."],
    footer="Version 1.0  ·  6 October 2026  ·  Public data only  ·  Draft · no right of reply needed",
    pdf_title="Claim Check 075 – Is Malta seventh in the EU for cars per person?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
