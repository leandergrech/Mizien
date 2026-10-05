"""Claim Check 008 flyer. Output: claims/CC-008/flyer.pdf and flyer.png."""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, BLUE  # noqa: E402

OUT = ROOT / "claims" / "CC-008"
build_flyer(Flyer(
    number="008", out=str(OUT / "flyer.pdf"), kicker="Transport, Malta",
    title_lines=["Flyovers and", "congestion"],
    subtitle="What has been shown about journey time, air pollution and noise?",
    quote_lines=["“reduce delays, emissions, and noise pollution”"],
    attribution="Infrastructure Malta, Msida Creek statement, 28 October 2024",
    context="Marsa complete · Msida flyover open; wider project works continue",
    note="The Marsa percentages are agency-reported. The survey files were not found in the public record reviewed.",
    verdict="Not substantiated", verdict_right=["Plausible benefits;", "data not inspectable."],
    cards=[("79%", ORANGE, "Marsa travel-time reduction", "Reported by Infrastructure Malta in its 2021 completion release; underlying survey not linked."),
           ("Up to 70%", ORANGE, "Marsa PM emissions reduction", "Agency-reported estimate; not the same as a measured change in ambient air concentrations."),
           ("2024", BLUE, "Msida wording was a forecast", "Before works began, IM called the flyover a move to reduce delays, emissions and noise; it entered use in December 2025."),
           ("No series", RED, "Local noise results", "No comparable before-and-after noise measurements were located for either junction."),
           ("Open", ORANGE, "What would verify the claim", "Publish the traffic surveys, calculation methods and local air/noise measurements."),
    ],
    fair="Flyovers can reduce stops for particular movements, and Infrastructure Malta reports benefits at Marsa. "
         "The public materials reviewed do not include the underlying surveys; Msida's wider project was still underway.",
    asks=["Publish the Marsa survey files and methods.",
          "Separate emissions estimates from ambient air-monitor readings.",
          "Measure traffic, air and noise after Msida's full road layout is operating.",
          "Track local and network effects over several years."],
    footer="Version 1.1  ·  5 October 2026  ·  Draft pending right of reply",
    pdf_title="Claim Check 008 – Flyovers and congestion"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
