"""Claim Check 141 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, GREY, AMBER  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="141", out=str(OUT / "flyer.pdf"), kicker="Population, Malta",
    title_lines=["Lowest in", "the EU?"],
    subtitle="The Pre-Budget Document’s ranking of Malta’s fertility rate, checked against Eurostat",
    quote_lines=["“Malta’s fertility rate is the", "lowest in the EU27…”"],
    attribution="Clyde Caruana, Minister for Finance, Pre-Budget Document 2027",
    context="Foreword, published 30 September 2026.",
    note="We ranked all 27 Member States in every year from 2000 to 2024.",
    verdict="Supported", verdict_right=["Lowest every year", "since 2017."],
    cards=[("1.01", RED, "Malta, 2024", "Live births per woman, the EU’s lowest (Eurostat)."),
           ("1.10", AMBER, "Spain, next lowest", "Lithuania 1.11. The EU-27 rate was 1.34."),
           ("8 of 8", GREEN, "Years lowest", "Malta has been lowest every year from 2017 to 2024."),
           ("2.1", GREY, "Replacement level", "The rate needed to keep a population stable without migration.")],
    fair="The foreword gives no year; the document’s own chapter gives 2024 and the same figures as Eurostat.",
    asks=["Not tested: the sentence’s second half, on what ageing will cost."],
    footer="Version 1.0  ·  17 November 2026  ·  Public data only  ·  No right of reply needed",
    pdf_title="Claim Check 141 – Lowest in the EU?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
