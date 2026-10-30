"""Claim Check 140 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, GREY  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="140", out=str(OUT / "flyer.pdf"), kicker="Energy, Malta",
    title_lines=["98% energy", "import dependency?"],
    subtitle="The Pre-Budget Document's energy figure, tested against Eurostat",
    quote_lines=["“…Malta's energy import dependency is approximately", "98.0 per cent, the highest in the European Union.”"],
    attribution="Ministry for Finance, Pre-Budget Consultation Document 2027, 30 September 2026",
    context="Document launched for the 2027 Budget consultation.",
    note="Import dependency = net imports / gross available energy.",
    verdict="Largely supported", verdict_right=["Level and ranking reproduce;", "the year is not stated."],
    cards=[("98.4%", GREEN, "Malta, 2024",
            "Eurostat's latest value; 97.0–99.0% in every year 2019–2024."),
           ("1st", GREEN, "Highest of 27",
            "Next in 2024: Luxembourg 91.0%, Cyprus 87.7%. Malta first every year 2016–2024."),
           ("57.3%", GREY, "EU-27 average, 2024",
            "Malta's ratio is about 41 points above the EU average."),
           ("68.5%", ORANGE, "Shipping fuel",
            "International maritime bunkers are 68.5% of the energy counted for Malta in 2024."),
           ("?", GREY, "No year given",
            "No year gives exactly 98.0; the document does not say which it used.")],
    fair="Accurate as a statement about Eurostat's indicator. It does not show how much household or business energy is imported.",
    asks=["Ministry: state the reference year.", "Readers: bunkers dominate the ratio.",
          "See CC-095 on energy subsidies.", "Data: Eurostat nrg_ind_id."],
    footer="Version 1.0  ·  30 October 2026  ·  Public data only  ·  No right of reply needed",
    pdf_title="Claim Check 140 – 98% energy import dependency?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
