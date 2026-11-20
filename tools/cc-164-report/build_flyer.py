"""Claim Check 164 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, GREY, AMBER  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="164", out=str(OUT / "flyer.pdf"), kicker="Tourism, Malta",
    title_lines=["€182 million", "from tourists?"],
    subtitle="The Budget 2027 eco-contribution, read in the speech and estimated from guest nights",
    quote_lines=["“Id-dħul minn dawn ir-reviżjonijiet", "mistenni jkun madwar €182 miljun.”"],
    attribution="Clyde Caruana, Budget Speech 2027, 26 October 2026",
    context="“The revenue from these revisions is expected to be around €182 million.”",
    note="We applied the new rates to the NSO’s 2025 guest nights.",
    verdict="Largely supported", verdict_right=["Rates exact; projection", "plausible, still a forecast."],
    cards=[("€8 / €10", GREEN, "A night from 2027", "Collective / short lets; caps €64 / €80 a person."),
           ("€176–193m", GREEN, "Our rough estimate", "Adults, before caps, from NSO 2025–26 nights."),
           ("€213m", GREY, "Estimates 2027, as reported", "Against €21m in 2026; includes cruise and Comino fees."),
           ("€80m", AMBER, "Not the ecotax", "In the speech, €80m is the work-permit fee yield.")],
    fair="The speech does not say whether €182m is total or extra revenue; the reported Estimates suggest extra.",
    asks=["Ministry for Finance: the basis of €182 million and the Estimates line."],
    footer="Version 1.0  ·  17 November 2026  ·  Public data only  ·  No right of reply needed",
    pdf_title="Claim Check 164 – €182 million from tourists?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
