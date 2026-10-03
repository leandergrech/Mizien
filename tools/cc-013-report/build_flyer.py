"""Claim Check 013 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="013", out=str(OUT / "flyer.pdf"), kicker="Housing and planning, Malta",
    title_lines=["Do permits keep", "prices in check?"],
    subtitle="A public claim, tested against research, Eurostat and the census",
    quote_lines=["“Continuing to issue permits helps keep", "property prices in check.”"],
    attribution="Johann Buttigieg, Planning Authority CEO, MaltaToday, 2 March 2025",
    context="“Stopping them would drive prices up.”",
    note="Asked about 91,000 dwellings approved in a decade (PA data: 87,814 in 2015–2024).",
    verdict="Largely supported", verdict_right=["Right in direction,", "size of effect unproven."],
    cards=[("Grade B", GREEN, "Research agrees",
            "Peer-reviewed studies: where supply is held back, demand turns into higher prices."),
           ("+31%", GREEN, "Huge demand shock",
            "Malta’s population grew 31% in 2015–2025; the EU’s grew 2%."),
           ("+34%", ORANGE, "Prices still rose faster",
            "Real house prices: Malta +34%, EU +25% (2015–2025)."),
           ("6.0%", RED, "Affordability worsening",
            "People overburdened by housing costs: 1.1% in 2015, 6.0% in 2025 (EU 7.7%)."),
           ("27.5%", ORANGE, "Not all homes are lived in",
            "Share of dwellings that were not a main residence in the 2021 census.")],
    fair="Overcrowding in Malta (4.7%) is a quarter of the EU rate. This check covers prices only, not the "
         "environmental cost of the permits.",
    asks=["Completions, not only approvals.",
          "How many new units become main homes.",
          "Any Malta estimate of the price effect.",
          "The source of the 91,000 figure."],
    footer="Version 1.0  ·  3 October 2026  ·  Public data only  ·  Right of reply: Planning Authority (not yet sent)",
    pdf_title="Claim Check 013 – Do permits keep prices in check?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
