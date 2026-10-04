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
    note="We checked every figure in the release.",
    verdict="Largely supported", verdict_right=["Accurate figures;", "the cost is left out."],
    cards=[("1st", GREEN, "Cheapest in purchasing power",
            "14.35 PPS per 100 kWh, lowest of 27 EU countries (Eurostat)."),
           ("3rd", GREEN, "Cheapest in euros",
            "EUR 0.130 per kWh in late 2024, as stated."),
           ("−0.2%", GREEN, "Stable since 2020",
            "The EU average rose 35% over the same period."),
           ("€1.0bn", RED, "Paid from public funds",
            "IMF: energy subsidies 2022–2025 (electricity and fuel)."),
           ("7.6%", GREEN, "Can't keep home warm",
            "Below the EU's 8.8% (2025); bill arrears 4.5% vs 7.0%.")],
    fair="Low, stable prices protected households through the energy crisis. The release leaves out that taxpayers "
         "fund the difference.",
    asks=["Electricity-only subsidy by year.",
          "Spending share by income group.",
          "Plans for targeted support.",
          "Cost-recovery tariff estimate."],
    footer="Version 1.0  ·  4 October 2026  ·  Public data only  ·  Right of reply: Energy Ministry (not yet sent)",
    pdf_title="Claim Check 022 – The lowest electricity burden in the EU?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
