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
    context="Marsa complete 2021 · Msida flyover open since 18 Dec 2025; wider works continue to 2027",
    note="Marsa’s figures are agency-reported, without surveys. The one public air monitor at Msida shows no improvement.",
    verdict="Not substantiated", verdict_right=["Plausible benefits;", "not shown in the data."],
    cards=[("79%", ORANGE, "Marsa travel-time reduction", "Reported by Infrastructure Malta in 2021; the underlying surveys are not published."),
           ("+14%", RED, "NO2 at the Msida monitor", "Jan–Sep 2026 mean 25.2 µg/m³ vs 22.0 in 2025 (2026 data unvalidated). Background stations: about +4%."),
           ("1 site", BLUE, "What the Msida data can say", "One monitor, about 410 m from the flyover, moved in Jan 2024; works continue. Not proof of harm."),
           ("1.4 km", ORANGE, "Nearest monitor to Marsa", "No EEA-reported air station has operated near the junction since Kordin closed in 2016."),
           ("No series", RED, "Local noise results", "No comparable before-and-after noise measurements were located for either junction."),
    ],
    fair="Flyovers can cut stops for some movements, and nine months is early; Msida’s works are unfinished and 2026 data "
         "are unvalidated. But the reductions claimed have not been shown in public data.",
    asks=["Publish the Marsa survey files and methods.",
          "Separate emissions estimates from ambient air-monitor readings.",
          "Explain the 2024 move of the Msida sampling point.",
          "Measure traffic, air and noise once Msida’s layout is complete."],
    footer="Version 1.2  ·  5 October 2026  ·  Draft; right of reply not sought",
    pdf_title="Claim Check 008 – Flyovers and congestion"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
