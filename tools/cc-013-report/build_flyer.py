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
           ("+31%", ORANGE, "The EU’s largest demand shock",
            "Malta’s population grew 31% in 2015–2025, the most in the EU (EU +2%)."),
           ("16th", GREEN, "Price rise below most states",
            "Real house prices +34% (provisional): above the EU aggregate (+25%), below the median state (+41%)."),
           ("+53%", RED, "Rents rose fast",
            "Rents paid by tenants rose 53% in 2015–2025, against 21% for the EU (8th of 27)."),
           ("6.0%", RED, "Affordability worsened",
            "People overburdened by housing costs: 1.1% (2015) to 2.9% (2022); about 6% since a 2023 "
            "series break (EU 7.7%).")],
    fair="Overcrowding in Malta (4.7%) is a quarter of the EU rate, and 27.5% of dwellings were not a main home in "
         "2021. This check covers prices only, not the environmental cost of the permits.",
    asks=["Completions, not only approvals.",
          "How many new units become main homes.",
          "Any Malta estimate of the price effect.",
          "The source of the 91,000 figure."],
    footer="Version 1.2  ·  5 October 2026  ·  Public data only  ·  Right of reply: Planning Authority (not yet sent)",
    pdf_title="Claim Check 013 – Do permits keep prices in check?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
