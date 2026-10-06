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
    context="Lovin Malta’s English (tagged “Press Release”); Maltese original in TVM News. The Commission’s page repeats the claim.",
    note="He added the energy would supply the Park and Ride’s electric buses.",
    verdict="Contradicted", verdict_right=["Installed elsewhere in", "Europe from 2015."],
    cards=[("2016", RED, "In service in Austria by 2016",
            "Motorway operator ASFINAG put a SmartFlower into service at a rest area on the A21."),
           ("15", GREEN, "SmartFlowers installed",
            "The maker calls Gozo’s “one of the largest installations in Europe”, not the first."),
           ("≈85 MWh", GREEN, "Modelled output a year",
            "PVGIS, if 2.5 kWp each (capacity not published). No metered output published."),
           ("36.5%", GREEN, "Tracking gain, modelled",
            "More energy than fixed panels at the site in PVGIS, against “up to 40%” claimed."),
           ("None", ORANGE, "Bus-charging figures published",
            "The share covered cannot be calculated. Parliament was told no feasibility study was made "
            "(Newsbook, second-hand).")],
    fair=("The flowers were EU-funded (about €850,000). Parliament was told no other such installation exists in Malta "
          "(Newsbook, second-hand). A claim to be among Europe’s largest would have held."),
    asks=["What “first of its kind in Europe” meant.",
          "The flowers’ capacity and metered output.",
          "The shuttle buses’ charging energy and hours.",
          "How the flowers are wired to the chargers."],
    footer="Version 1.1  ·  6 October 2026  ·  Draft pending right of reply from the Ministry for Gozo and Planning "
           "and the Public Works Department",
    pdf_title="Claim Check 032 – Europe’s first solar flowers?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
