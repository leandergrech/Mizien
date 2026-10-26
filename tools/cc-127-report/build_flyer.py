"""Claim Check 127 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, GREY, AMBER  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="127", out=str(OUT / "flyer.pdf"), kicker="Land and agriculture, Malta",
    title_lines=["Lowest organic", "share in the EU?"],
    subtitle="The Commission’s statement on Malta, tested against Eurostat",
    quote_lines=["“Malta has the lowest proportion of organic farming", "in the EU.”"],
    attribution="European Commission, SWD(2026) 702 final, 2 October 2026",
    context="“Only 66 hectares (less than 1%) … was managed organically in 2022.”",
    note="Document read in the Austrian Parliament’s copy.",
    verdict="Supported", verdict_right=["Reproduces from Eurostat", "in every year tested."],
    cards=[("0.62%", RED, "Malta, 2022", "Share of farmland under organic farming (Eurostat)."),
           ("2.2%", GREY, "Next lowest, 2022", "Bulgaria and Ireland; Malta is lowest in every year 2012–2024."),
           ("66 ha", GREEN, "Organic area, 2022", "The Commission’s figure matches Eurostat (65 ha converted, 1 ha in conversion)."),
           ("9.1%", AMBER, "EU-27 average, 2020", "Last published estimate; Malta was 0.62% that year."),
           ("?", GREY, "Farmland denominator", "10 700 ha is not sourced; surveys give 8 880–9 800 ha. Still under 1%.")],
    fair="Austria and Greece are missing from the latest release but were far above Malta when last published.",
    asks=["Commission: the source of the 10 700 ha.", "Agriculture Directorate: the organic register area.",
          "Readers: the 2022 EU average is not yet published.", "Readers: 2023 and 2024 show 80 ha."],
    footer="Version 1.0  ·  21 October 2026  ·  Public sources  ·  No right of reply needed",
    pdf_title="Claim Check 127 – Lowest organic share in the EU?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
