"""Claim Check 124 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="124", out=str(OUT / "flyer.pdf"), kicker="Climate performance index, Malta",
    title_lines=["CCPI 2026:", "Malta 25th"],
    subtitle="An index’s country page, tested against Eurostat",
    quote_lines=["“Malta ranks 25th in the CCPI,", "up nine spots and a medium performer.”"],
    attribution="Climate Change Performance Index 2026, Malta page (© 2026 Germanwatch)",
    context="The page adds that “automobile use has not decreased”.",
    note="The rank is the index’s own computation and was not reproduced.",
    verdict="Largely supported", verdict_right=["Testable statements hold;", "the rank is untested."],
    cards=[("17.2%", RED, "Renewables, 2024",
            "Share of gross final energy: 4th lowest of 27; EU-27 25.2%. Up 9.0 points since 2019."),
           ("+5.8%", ORANGE, "More cars since 2022",
            "317,234 to 335,693 (2022–25); road energy +4.6%. Per resident: flat to slightly lower."),
           ("9,790", GREEN, "Battery-electric cars",
            "Up from 1,783 in 2021; 2.9% of the fleet, as in the EU-27."),
           ("-11.6%", GREEN, "Emissions per resident",
            "4.3 to 3.8 t CO2e (2022–24), excluding land use; still 82.7% of 1990.")],
    fair="Car use is measured by proxies, not vehicle-kilometres, and the index’s expert survey and scores were not available to us.",
    asks=["The CCPI report with Malta’s indicator scores.",
          "Vehicle-kilometre series for 2019–2025.",
          "Malta’s emissions projections against its 2030 target."],
    footer="Version 1.0  ·  19 October 2026  ·  Public data only  ·  No right of reply needed",
    pdf_title="Claim Check 124 – CCPI 2026: Malta 25th"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
