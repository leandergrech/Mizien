"""Claim Check 036 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, GREY, AMBER  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="036", out=str(OUT / "flyer.pdf"), kicker="Air quality, Malta",
    title_lines=["Just a", "nuisance?"],
    subtitle="ERA’s view of construction and quarry dust, tested against its own source and the health evidence",
    quote_lines=["“… which is considered to be more of a", "nuisance rather than a health-related issue.”"],
    attribution="Environment and Resources Authority, State of the Environment Report 2018",
    context="On dust from mineral extraction and construction (ch. 2, p. 15).",
    note="We read the study ERA cites, the US EPA and WHO reviews, and Malta’s monitoring data.",
    verdict="Not substantiated", verdict_right=["True of the largest particles;", "not shown for its PM10 share."],
    cards=[("11–23%", AMBER, "Is PM10",
            "Share of deposited quarry dust below 10 µm in ERA’s source (ERA: 11–22%)."),
           ("1,200 t", RED, "PM10 a year",
            "From softstone quarries near homes. ERA’s source says it may affect health."),
           ("Suggestive", ORANGE, "Coarse PM and health",
            "US EPA rating for deaths, heart and lung effects; weaker than fine PM, not none."),
           ("47–72%", AMBER, "Of Malta’s PM10 is coarse",
            "At monitoring stations (EEA). Sources not separated.")],
    fair="Most construction dust by mass is larger than 10 µm and settles. For that part, “nuisance” is fair.",
    asks=["ERA: the source for “more of a nuisance”, and whether it covers PM10.",
          "ERA: any estimate of construction’s share of Malta’s PM10."],
    footer="Version 1.0  ·  16 November 2026  ·  Draft, pending right of reply",
    pdf_title="Claim Check 036 – Just a nuisance?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
