"""Claim Check 034 flyer. Run calc.py first. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="034", out=str(OUT / "flyer.pdf"), kicker="Air quality, Malta",
    title_lines=["Cleaner air,", "already?"],
    subtitle="ERA’s statement that its Air Quality Plan’s measures have already worked, tested against station data",
    quote_lines=["“The plan outlines actions that have already", "yielded positive results for Malta’s air quality…”"],
    attribution="Environment and Resources Authority, Air Quality Plan for Malta 2025 web page, 12 March 2025",
    context="The plan names six: power-sector reform, transport grants, free school transport, ferries, "
            "free public transport.",
    note="Tested with 13 years of validated EEA data and ERA’s own reports.",
    verdict="Not substantiated", verdict_right=["Power reform shown to help;", "transport measures not shown."],
    cards=[("−99.9%", GREEN, "Power-station sulphur cut",
            "Sulphur oxides from power stations, 2008 to 2018; SO₂ in the air fell 82% at Żejtun."),
           ("−22%", GREEN, "NO₂ at Msida",
            "2015–17 to 2021–23, in step with a cleaner fleet; not tied to any named measure."),
           ("52 days", RED, "PM10 limit broken, 2023",
            "At Msida after ERA deducts dust and sea salt; 35 allowed. Worst of 2015–2025."),
           ("+8.1", ORANGE, "After free transport",
            "µg/m³ PM10 at Msida, year after Oct 2022 vs year before; 10 of 11 readings rose."),
           ("4 of 6", ORANGE, "No air data offered",
            "Grants, ferry landings, fast ferry, free transport: uptake or passengers only.")],
    fair="ERA states the 2018 and 2023 breaches itself, and the plan says traffic growth offset gains. Flat PM10 does "
         "not prove the measures did nothing.",
    asks=["The study behind “already yielded”.",
          "Data for the school-transport figures.",
          "Traffic counts near Msida, 2018–23.",
          "Sources of the 2023 PM10 excess."],
    footer="Version 1.0  ·  6 October 2026  ·  Public data only  ·  Draft pending right of reply from the Environment "
           "and Resources Authority",
    pdf_title="Claim Check 034 – Cleaner air, already?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
