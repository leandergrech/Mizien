"""Claim Check 149 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, GREY, AMBER  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="149", out=str(OUT / "flyer.pdf"), kicker="Planning and housing, Malta",
    title_lines=["Building", "mad?"],
    subtitle="MaltaToday’s figures for dwellings approved in 2025, rebuilt from the NSO’s quarterly tables",
    quote_lines=["“Approved residential units reached 12,325", "in 2025, the third-highest annual total ever…”"],
    attribution="MaltaToday (James Debono), 27 July 2026",
    context="Also: a record 226 units approved on ODZ land.",
    note="We summed the NSO’s quarterly tables for 2022–2025.",
    verdict="Largely supported", verdict_right=["Headline numbers exact;", "ODZ record not checked."],
    cards=[("12,325", GREEN, "Approved in 2025", "Sum of the NSO’s four quarters; matches its annual figure."),
           ("+41.4%", GREEN, "On 2024", "8,716 approved new dwellings in 2024 (NSO)."),
           ("2", AMBER, "Higher years found", "2018 and 2019, from press reports of NSO figures."),
           ("226", GREY, "ODZ units", "Planning Authority data; we could not read it.")],
    fair="These are approvals, not homes built; some permits lapse or change.",
    asks=["Planning Authority: the 2007–2025 ODZ series.", "NSO: annual totals for 2007–2021."],
    footer="Version 1.0  ·  17 November 2026  ·  Public data only  ·  No right of reply needed",
    pdf_title="Claim Check 149 – Building mad?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
