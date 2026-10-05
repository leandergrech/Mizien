"""Claim Check 076 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, GREY  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="076", out=str(OUT / "flyer.pdf"), kicker="Transport, Malta",
    title_lines=["36 more vehicles", "a day?"],
    subtitle="The National Statistics Office's Q1 2026 release, tested against its own table",
    quote_lines=["“…the stock of licensed motor vehicles increased at a", "net average rate of 36 motor vehicles per day.”"],
    attribution="National Statistics Office, Motor Vehicles: Q1/2026, 13 May 2026",
    context="The same release gives the stock at the end of March 2026 as 460,648.",
    note="We rebuilt the figures from the NSO's Table 1 and its stated formula.",
    verdict="Supported", verdict_right=["Both figures reproduce exactly", "from the NSO's own table."],
    cards=[("460,648", GREEN, "Vehicles, end of March 2026",
            "NSO Table 1. The vehicle categories add up to the total in all 13 quarters."),
           ("+3,245", GREEN, "Net rise in the quarter",
            "460,648 minus 457,403 over 90 days is 36.06 a day, the NSO's formula."),
           ("63", ORANGE, "Newly licensed a day (gross)",
            "5,680 new licences. 6,963 vehicles went off the road and 4,140 returned; 36 is what is left."),
           ("35", GREY, "The Commission's figure",
            "Its 2026 Country Report says 35 a day; Q4 2025 gives 35.5 from the same table."),
           ("8 to 9", RED, "Daily rise in early 2024",
            "The pace is recent: 36 a day is typical of the last four quarters, not of 2024.")],
    fair="The figures are right and described as net. The two NSO methods differ by 388 vehicles (0.08% of the stock) in the "
         "quarter, which the release attributes to database cut-off dates.",
    asks=["NSO: confirm no revision to Q1 2026.", "NSO: the Q4 2025 release behind the Commission's 35.",
          "Transport Malta: why 2024 growth was so low."],
    footer="Version 1.0  ·  5 October 2026  ·  Public data only  ·  No right of reply needed",
    pdf_title="Claim Check 076 – 36 more vehicles a day?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
