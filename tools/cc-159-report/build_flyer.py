"""Claim Check 159 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, GREY, AMBER  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="159", out=str(OUT / "flyer.pdf"), kicker="Population, Malta",
    title_lines=["Fifteen times", "the EU average?"],
    subtitle="An IMF staff statement, tested against Eurostat and World Bank data",
    quote_lines=["“With a population density fifteen times", "greater than the EU average …”"],
    attribution="International Monetary Fund staff, Country Report 26/29, February 2026",
    context="Overview of the 2025 Article IV staff report on Malta.",
    note="The density ratio and the report’s population table were checked; the link to strain on services was not.",
    verdict="Largely supported", verdict_right=["Ratio is 16.6 on 2024 data;", "fifteen is slightly low."],
    cards=[("16.6×", GREEN, "Malta ÷ EU-27, 2024",
            "1,817 people per km² against 110 (Eurostat). The ratio passed 15 in 2021."),
           ("13.9–17.2×", AMBER, "Depends on the “average”",
            "Unweighted mean of other states: 13.9. Median: 17.2. EU excluding Malta: 17.0."),
           ("−2%", AMBER, "IMF population vs Eurostat",
            "2024 and 2025 values sit about 2% below Eurostat’s 1 January figures."),
           ("3.4×", GREY, "Malta vs the next EU state",
            "World Bank, land area: Malta 1,805, Netherlands 534.")],
    fair="The sentence also says density strains infrastructure, housing and services. That is a judgement, "
         "and this check does not rate it.",
    asks=["IMF: the year and definition behind “fifteen times”.",
          "IMF: the basis of its 2024–2027 population values."],
    footer="Version 1.0  ·  9 November 2026  ·  Public data only  ·  No right of reply needed",
    pdf_title="Claim Check 159 – Fifteen times the EU average?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
