"""Claim Check 110 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, GREY, BLUE  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="110", out=str(OUT / "flyer.pdf"), kicker="Transport, Malta",
    title_lines=["37.7% of new cars", "zero-emission?"],
    subtitle="The European Commission's 2026 Country Report, tested against Eurostat",
    quote_lines=["“…7 700 new passenger car registrations, of which 37.7%", "were ZEVs … well above the EU average of 13.6%.”"],
    attribution="European Commission, 2026 Country Report – Malta, 3 June 2026",
    context="Annex 8; up 17.4 points from 20.3% in 2023.",
    note="ZEV: battery electric or hydrogen. Plug-in hybrids do not count.",
    verdict="Supported", verdict_right=["The figures reproduce;", "Malta is second in the EU."],
    cards=[("37.7%", GREEN, "New cars, 2024",
            "Eurostat: 2,893 of 7,683 new cars were battery electric. In 2023 the share was 20.3%."),
           ("2nd", GREEN, "Rank in the EU",
            "Only Denmark (51.3%) was higher. Sweden and the Netherlands follow at about 35%."),
           ("13.5%", BLUE, "EU-27 average",
            "Eurostat's figure; the report says 13.6%. The tenth of a point changes nothing."),
           ("2.2%", GREY, "Share of the whole fleet",
            "Zero-emission cars were 2.2% of 330,484 cars at the end of 2024, the EU average."),
           ("+18/day", ORANGE, "Fleet growth, 2024",
            "The car stock grew by 6,632. The report says charging points lag behind.")],
    fair="The passage is accurate. A fast-changing new-car market is not yet a cleaner fleet; transport emissions are "
         "checked in CC-109.",
    asks=["Commission: the source of the 13.6% EU average.", "Transport Malta: charging points against plan.",
          "Annual fleet emissions from road transport.", "Readers: new cars are not the fleet."],
    footer="Version 1.0  ·  5 October 2026  ·  Public data only  ·  No right of reply needed",
    pdf_title="Claim Check 110 – 37.7% of new cars zero-emission?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
