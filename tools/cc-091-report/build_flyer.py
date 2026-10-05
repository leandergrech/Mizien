"""Claim Check 091 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, GREY, AMBER  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="091", out=str(OUT / "flyer.pdf"), kicker="Workplace safety, Malta",
    title_lines=["OHSA inspections doubled,", "74% of sites compliant?"],
    subtitle="The Occupational Health and Safety Authority's 2025 annual report, tested",
    quote_lines=["“…74% of sites were found to be adequately compliant with", "occupational health and safety requirements.”"],
    attribution="OHSA, Annual Report 2025, section 4.3.1 (tabled 1 July 2026)",
    context="The report also gives 23,711 inspections in 2025 and nine fatal accidents.",
    note="We transcribed the report's tables, recomputed the changes and compared deaths with Eurostat.",
    verdict="Largely supported", verdict_right=["Figures match the report;", "the 74% has no stated base."],
    cards=[("2.5x", GREEN, "Inspections, 2025 v 2024",
            "23,711 against 9,381 (+152.8%); 9.2 times the 2,585 of 2023. Divisional totals add up."),
           ("74%", AMBER, "Construction rated adequate",
            "OHSA's own rating: 21% needed orders and 5% a stop-work order. The base is not stated."),
           ("9", RED, "Workers died in 2025",
            "Three in construction, four in transport and storage, two in agriculture. Five in 2024."),
           ("65%", ORANGE, "Safe use of lifting machinery",
            "The weakest feature on site; falls protection 77%, scaffolds 76%."),
           ("5 of 9", GREY, "Victims were third-country nationals",
            "Four Maltese and five third-country nationals died.")],
    fair="The figures are the regulator's own and reproduce from its tables. More inspections is activity, not proof of safer sites.",
    asks=["OHSA: the base and definition behind the 74%.", "OHSA: reconcile 5% stop-work share with 526 stop orders.",
          "NSO/OHSA: 2025 fatality rates with denominators."],
    footer="Version 1.0  ·  5 October 2026  ·  Public sources  ·  No right of reply needed",
    pdf_title="Claim Check 091 – OHSA inspections doubled, 74% of sites compliant?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
