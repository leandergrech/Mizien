"""Claim Check 022 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="022", out=str(OUT / "flyer.pdf"), kicker="Climate and energy, Malta",
    title_lines=["The lowest electricity", "burden in the EU?"],
    subtitle="A ministry claim, tested against Eurostat and the IMF",
    quote_lines=["“…the burden on Maltese families is the lowest", "in the EU, at 14.33 PPS per 100kWh.”"],
    attribution="Energy Ministry press release, 6 May 2025",
    context="For the second half of 2024, adjusted for purchasing power.",
    note="We checked every figure, then measured burden against income and actual use.",
    verdict="Largely supported", verdict_right=["Lowest on price,", "second against income."],
    cards=[("1st", GREEN, "Cheapest in purchasing power",
            "14.35 PPS per 100 kWh for a typical household (2,500–4,999 kWh): lowest of 27 (Eurostat)."),
           ("2nd", GREEN, "Against income",
            "A typical bill is 2.2% of median income (EU 4.7%), second after Luxembourg; also second for low incomes."),
           ("5th", ORANGE, "On actual use",
            "Maltese homes use more power, a fifth of it for cooling: the average bill is 1.3% of income (EU 1.9%)."),
           ("€1.0bn", RED, "Paid from public funds",
            "IMF: energy subsidies 2022–2025, electricity and fuel together (2025 projected)."),
           ("−0.2%", GREEN, "Stable since 2020",
            "The EU average rose 35% over the same period. Malta’s price was cut in 2014.")],
    fair="Low, stable prices kept bills among the EU’s lightest relative to income through the energy crisis. "
         "The release leaves out that taxpayers fund the difference.",
    asks=["Electricity-only subsidy by year.",
          "Spending share by income group, after 2022.",
          "Plans for targeted support.",
          "Cost-recovery tariff estimate."],
    footer="Version 1.2  ·  5 October 2026  ·  Public data only  ·  No right of reply needed",
    pdf_title="Claim Check 022 – The lowest electricity burden in the EU?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
