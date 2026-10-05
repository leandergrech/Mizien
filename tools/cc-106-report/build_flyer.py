"""Claim Check 106 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, GREY, AMBER  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="106", out=str(OUT / "flyer.pdf"), kicker="Nature and wildlife, Malta",
    title_lines=["Shearwaters: 10% of", "the world population?"],
    subtitle="BirdLife Malta's figure, tested against regulator and published estimates",
    quote_lines=["“…around 1,600 – 1,800 pairs, constituting approximately", "10% of the global population.”"],
    attribution="BirdLife Malta, LIFE Arċipelagu Garnija project page (undated)",
    context="On the Yelkouan shearwater (Garnija), classed as Vulnerable.",
    note="The world total is poorly known: estimates span 11,000 to 55,000 pairs.",
    verdict="Largely supported", verdict_right=["An important share;", "“about 10%” rounds up 6–8%."],
    cards=[("1,795–2,635", GREEN, "Pairs in Malta, ERA plan",
            "The regulator's newer count overlaps and exceeds the page's 1,600–1,800."),
           ("21–36k", GREY, "Pairs worldwide",
            "The figure most often quoted; a 2008 review gave 11,355–54,524 pairs."),
           ("4–9%", AMBER, "Share with the page's count",
            "1,600–1,800 of 21,000–36,000 pairs: central 6%."),
           ("5–13%", GREEN, "Share with ERA's count",
            "10% is inside this range; central 7.8%."),
           (">50%", GREY, "One colony, Tavolara",
            "Sardinia's Tavolara holds over half the world population (Pezzo et al. 2021).")],
    fair="Malta holds an internationally important share of a vulnerable seabird. “Roughly 5–10%” would be safer.",
    asks=["BirdLife Malta: year and source of the count.", "BirdLife Malta: the global figure behind 10%.",
          "ERA: method for 1,795–2,635 pairs.", "ERA: latest Article 12 figures."],
    footer="Version 1.0  ·  5 October 2026  ·  Public sources  ·  No right of reply needed",
    pdf_title="Claim Check 106 – Shearwaters: 10% of the world population?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
