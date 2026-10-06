"""Claim Check 045 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, GREY  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="045", out=str(OUT / "flyer.pdf"), kicker="Flood tunnels, Malta",
    title_lines=["20 km of tunnels:", "do they manage flooding?"],
    subtitle="A public claim, tested against official sources and rainfall data",
    quote_lines=["“…they avoid flooding and damage caused", "by waters every time it rains.”"],
    attribution="Attributed by TVM News to Mario Ellul, Public Works Department, 4 July 2025",
    context="Said as the department works to extend the network from 16 km to a 20 km total.",
    note="The department puts 16 km in use and 20 km as the planned total.",
    verdict="Not substantiated", verdict_right=["Plausible by design,", "but not shown."],
    cards=[("16 km", GREEN, "In use now", "Public Works Department, 4 July 2025. A further 4 km is planned."),
           ("20 km", GREY, "The planned total", "The department’s own figure for the network once a further 4 km is built."),
           ("5-year", GREY, "Design storm", "The European Commission says the system is built for a 5-year storm over 65 km²."),
           ("2020", ORANGE, "Flooding continued", "Roads flooded in project localities in September 2020; two more tunnels were planned in 2022."),
           ("0", RED, "Before-and-after counts", "No published flood-incident series found in the sources we searched, so the effect cannot be measured.")],
    fair="The tunnels are real and were built to reduce flooding, and the department maintains them every year. This "
         "check is about the effect and the words “every time it rains”.",
    asks=["Flood incidents by locality, 2005 to date.",
          "Design storm for each catchment.",
          "Operating length of each tunnel.",
          "The Agency's before-and-after comparison."],
    footer="Version 1.1  ·  6 October 2026  ·  Public data only  ·  Draft, pending right of reply from the Public Works Department",
    pdf_title="Claim Check 045 – 20 km of tunnels: do they manage flooding?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
