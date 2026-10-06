"""Claim Check 075 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, GREY, ORANGE, RED  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="075", out=str(OUT / "flyer.pdf"), kicker="Cars per person, Malta",
    title_lines=["Is Malta seventh in the", "EU for cars per person?"],
    subtitle="A media report of Eurostat figures, tested against the data and its dates",
    quote_lines=["“Malta is ranked number seven, just between Germany",
                 "and Poland … with 585 cars per 1,000 inhabitants.”"],
    attribution="Lovin Malta, 21 September 2024",
    context="The outlet’s own text, citing a Eurostat dataset “as of 2023”, with a graphic “up to the year 2022”.",
    note="The 585 and seventh place are Eurostat’s 2022 figures, as revised after January 2024.",
    verdict="Misleading", verdict_right=["Right for 2022, but", "not Malta’s latest rank."],
    cards=[("585", GREEN, "Right for 2022",
            "Eurostat’s 2022 figure in today’s data: seventh of 27, between Germany and Poland."),
           ("12th", RED, "Eurostat’s 2023 figures",
            "Published by 25 July 2024, two months before the article: Malta about 575."),
           ("“is ranked”", ORANGE, "Presented as current",
            "Conflicting dates (“as of 2023”, graphic “up to the year 2022”), but seventh in the present tense."),
           ("≈602", GREY, "Revised since",
            "Eurostat’s January 2024 release had Malta’s 2022 value at about 602, sixth."),
           ("14th", ORANGE, "Lower since",
            "571 in 2025, below the EU-27’s 584: the population grew faster than the car stock.")],
    fair="The 585 is right for 2022 in Eurostat’s current data, and Malta still has by far the most cars per km² of "
         "land in the EU (1,014 in 2022; the Netherlands is second at 261).",
    asks=["Lovin Malta: the data year and Eurostat release it used.",
          "Lovin Malta: the graphic behind the rankings.",
          "NSO: licensed versus garaged and rented cars."],
    footer="Version 1.1  ·  6 October 2026  ·  Public data only  ·  Draft · pending right of reply",
    pdf_title="Claim Check 075 – Is Malta seventh in the EU for cars per person?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
