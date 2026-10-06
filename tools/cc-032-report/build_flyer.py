"""Claim Check 032 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="032", out=str(OUT / "flyer.pdf"), kicker="Renewables, Gozo",
    title_lines=["Europe’s first", "solar flowers?"],
    subtitle="The Government’s claims about Gozo’s fifteen solar flowers, tested against the record",
    quote_lines=["“With the installation of these first solar", "flowers in Europe, we are demonstrating …”"],
    attribution="Clint Camilleri, Minister for Gozo and Planning, 21 October 2025",
    context="Lovin Malta’s English of his quoted words (Maltese original: TVM News). The Commission’s page says the same.",
    note="He added the energy would supply the Park and Ride’s electric buses.",
    verdict="Contradicted", verdict_right=["In service elsewhere in", "Europe from 2015."],
    cards=[("2016", RED, "Austria had one first",
            "Motorway operator ASFINAG put a SmartFlower into service at a rest area on the A21."),
           ("15", GREEN, "SmartFlowers installed",
            "The maker calls Gozo’s “one of the largest installations in Europe”, not the first."),
           ("≈85 MWh", GREEN, "Modelled output a year",
            "PVGIS, if 2.5 kWp each: 36% more than fixed panels. No metered output published."),
           ("2–3 h", ORANGE, "Of shuttle service a day",
            "What that output equals at bus consumption from other studies. Indicative only."),
           ("None", ORANGE, "Energy balance published",
            "No output or bus-use figures found; Parliament was told no feasibility study was made (Newsbook).")],
    fair="The flowers work, were EU-funded at about €850,000 and seem to be Malta’s first. A claim to be among "
         "Europe’s largest would have held.",
    asks=["What “first of its kind in Europe” meant.",
          "The flowers’ capacity and metered output.",
          "The shuttle buses’ charging energy and hours.",
          "How the flowers are wired to the chargers."],
    footer="Version 1.0  ·  6 October 2026  ·  Public data and the EU PVGIS model  ·  Draft pending right of reply from "
           "the Ministry for Gozo and Planning",
    pdf_title="Claim Check 032 – Europe’s first solar flowers?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
