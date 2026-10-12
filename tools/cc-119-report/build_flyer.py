"""Claim Check 119 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, BLUE  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="119", kicker="Climate and energy, Malta",
    out=str(OUT / "flyer.pdf"),
    title_lines=["Council on Malta’s", "renewables: the numbers"],
    subtitle="The Council’s draft Recommendation, tested against Eurostat data",
    quote_lines=["“Malta’s share of renewables … (17.2% in 2024) and in the", "electricity mix (16.7% in 2025) remains very low …”"],
    attribution="Council of the European Union, draft Recommendation on Malta, 3 July 2026",
    context="Almost exclusively solar, “with no wind or hydropower generation recorded”.",
    note="Every figure reproduces from Eurostat; the 16.7% is the share of domestic net generation, which the text does not say.",
    verdict="Largely supported", verdict_right=["Figures reproduce;", "one measure unnamed."],
    cards=[("17.2%", GREEN, "Renewables in 2024",
            "Exact (Eurostat). EU-27: 25.2%. Only Belgium, Luxembourg and Ireland are lower."),
           ("16.7%", GREEN, "Renewables in 2025 electricity",
            "Matches Malta’s domestic net generation (363 of 2,176 GWh). Eurostat’s consumption-based indicator gives 11.2% (provisional)."),
           ("47%", BLUE, "EU-27 renewables in generation",
            "The EU-27’s share of net generation in 2025 (47.3%); Malta is second lowest of 27."),
           ("97%", ORANGE, "Solar share of renewables",
            "PV is 326.7 of 336.0 GWh in 2024; the rest is biogas. No hydro in any year."),
           ("0.03 GWh", RED, "Wind generated in 2024",
            "A trace in Eurostat’s annual table (0.01% of renewable output): “none recorded” holds to rounding.")],
    fair="The text does not say which electricity measure 16.7% is. It is the more favourable of three readings, and every one is far below the EU’s. "
         "This is a draft text of 3 July 2026; the adopted version was not checked.",
    asks=["The source and measure behind “16.7% in 2025”.",
          "Whether the adopted text keeps paragraph (25) unchanged."],
    footer="Version 1.0  ·  12 October 2026  ·  Public data only  ·  No right of reply needed",
    pdf_title="Claim Check 119 – Council on Malta's renewables: the numbers"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
