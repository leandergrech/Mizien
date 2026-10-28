"""Claim Check 137 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="137", out=str(OUT / "flyer.pdf"), kicker="Climate and energy, Malta",
    title_lines=["Were the July", "power cuts predictable?"],
    subtitle="The Malta Chamber’s statement, tested against NSO and Eurostat data",
    quote_lines=["“It is evident that the investment", "carried out was not enough.”"],
    attribution="Malta Chamber of Commerce, Enterprise and Industry, 21 July 2026",
    context="A statement on the July 2026 cuts; it gives no figures.",
    note="Quotes read through a web reader; the NAO review was not opened (second-hand).",
    verdict="Not substantiated", verdict_right=["Rise foreseeable;", "‘enough’ has no yardstick."],
    cards=[("+42.6%", ORANGE, "Peak demand 2018–23",
            "465 to 663 MW (NSO). Residents plus tourists grew 13.4%."),
           ("31%", ORANGE, "Explained by people",
            "Population and tourists account for about a third of the rise in the peak."),
           ("631 MW", GREEN, "The trend foresaw it",
            "A line fitted to 2017–2022 gives 631 MW for 2025; the actual peak was 637 MW."),
           ("?", RED, "Enough investment?",
            "No figure for what was invested or needed; the audit review was seen second-hand.")],
    fair="This check covers demand and investment, not who caused the July 2026 faults.",
    asks=["The Chamber’s figures on investment.",
          "The National Audit Office review in full.",
          "Enemalta’s load forecast and capital spending."],
    footer="Version 1.0  ·  28 October 2026  ·  Public data only  ·  Pending right of reply",
    pdf_title="Claim Check 137 – Were the July power cuts predictable?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
