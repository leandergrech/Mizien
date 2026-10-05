"""Claim Check 053 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, GREY  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="053", out=str(OUT / "flyer.pdf"), kicker="Light pollution, Malta",
    title_lines=["Milky Way visible", "from 13% of Malta?"],
    subtitle="A University of Malta study of night-sky brightness, and how it was reported",
    quote_lines=["“…with the Milky Way being visible for only 12.8%", "of the area.”"],
    attribution="Caruana et al., Journal of Environmental Management, 2020",
    context="Reported as “Milky Way only visible from 13% of Malta”.",
    note="Sky Quality Meter readings in 347 one-kilometre cells, 2017–2019.",
    verdict="Supported", verdict_right=["Accurately reports a", "peer-reviewed measurement."],
    cards=[("12.8%", GREEN, "Milky Way visible",
            "Bortle class 4 or darker; 13.5% on the world atlas threshold. No darker sky anywhere."),
           ("87%", RED, "Light-polluted area",
            "Bortle class 5 or brighter across the islands; 96% on the island of Malta."),
           ("11%", GREY, "World atlas, 2016",
            "An independent satellite-based atlas gave a similar figure for Malta."),
           ("1.6%", ORANGE, "Island of Malta, 2018/19",
            "The class 4 area fell from 3.9% a year earlier. No newer survey found."),
           ("6–26%", GREY, "Depends on the threshold",
            "The study's own sensitivity test; 13% uses a standard threshold.")],
    fair="The headline matches the study. It describes 2017–2019; a repeat survey would show whether skies have "
         "darkened or brightened since.",
    asks=["UM / ERA: a repeat survey since 2019.", "ERA / PA: national lighting guidelines.",
          "Readers: data from 2017–2019.", "See CC-106 on light and seabirds."],
    footer="Version 1.0  ·  5 October 2026  ·  Published research  ·  No right of reply needed",
    pdf_title="Claim Check 053 – Milky Way visible from 13% of Malta?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
