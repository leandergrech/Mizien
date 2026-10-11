"""Claim Check 108 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, BLUE  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="108", out=str(OUT / "flyer.pdf"), kicker="Water, checked",
    title_lines=["Net-zero impact", "on the aquifer?"],
    subtitle="The Green Paper’s reason for leaving WSC’s boreholes out of groundwater licensing, tested",
    quote_lines=["“…the Corporation is moving towards the achievement of", "a net-zero impact on the groundwater environment…”"],
    attribution="Energy and Water Agency, Green Paper on groundwater abstraction, Nov 2023",
    context="Same page: WSC abstraction “will be capped at a maximum level of 14 Mm³ up to 2030”.",
    note="A proposal in a consultation document; we did not find whether it was adopted.",
    verdict="Not measurable", verdict_right=["No definition,", "no date."],
    cards=[("11.5", GREEN, "million m³ in 2025",
            "WSC groundwater production: 82% of the proposed 14 million m³ cap, and 15% below 2016."),
           ("+4%", ORANGE, "Cap above 2016",
            "The ceiling sits only 4% above the highest year we read (13.5 million m³ in 2016)."),
           ("13%", ORANGE, "New Water vs abstraction",
            "Treated wastewater supplied in 2022 (1.6 million m³) against what WSC abstracted (12.7)."),
           ("4 of 15", RED, "Aquifers in poor quantitative status",
            "Including both main sea-level aquifers (EU reporting, assessed 2021)."),
           ("No balance", ORANGE, "Nothing published",
            "No source we read sets out what is given back, measured how.")],
    fair="WSC’s share of groundwater in its supply fell from 42% to 29% since 2016, and the cap is met so far. "
         "Lower abstraction and reuse are sound aims; the question is whether ‘net zero’ can be checked.",
    asks=["A definition, baseline and date for ‘net-zero impact’.",
          "Annual New Water volumes and where they are used.",
          "Whether the cap and exemption were adopted.",
          "Any estimate of recharge from the networks."],
    footer="Version 1.0  ·  11 October 2026  ·  Label as of 11 Oct 2026  ·  Pending right of reply (EWA, WSC)",
    pdf_title="Claim Check 108 – Net-zero impact on the aquifer?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
