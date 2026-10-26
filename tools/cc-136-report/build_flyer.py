"""Claim Check 136 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, GREY, AMBER  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="136", out=str(OUT / "flyer.pdf"), kicker="Population, Malta",
    title_lines=["Most crowded country", "in Europe?"],
    subtitle="An AFP feature, tested against World Bank, Eurostat and Planning Authority data",
    quote_lines=["“The tiny Mediterranean island is the most densely", "populated country in Europe.”"],
    attribution="Agence France-Presse (AFP), 6 June 2026",
    context="AFP's own voice, in a feature on development in Malta.",
    note="Three statements checked: density, approvals and population growth.",
    verdict="Largely supported", verdict_right=["Right for the EU; Monaco is denser.", "Population and approvals hold."],
    cards=[("1,805", AMBER, "People per km², 2024",
            "Highest in the EU, 3.4 times the Netherlands (534). Monaco: 18,537."),
           ("+30.9%", GREEN, "Population, 2015–2025",
            "AFP says “nearly 30 percent”. 2016–2026: +30.8%."),
           ("12,325", AMBER, "Dwelling units approved, 2025",
            "Up 41% on 2024 and 4.6 times 2013, but below the 2018–2019 peaks."),
           ("2nd", GREY, "Of 44 European states",
            "Malta ranks second in the World Bank list, after Monaco. Vatican City not tested.")],
    fair="Malta is by far the densest EU country; \"in Europe\" needs the words \"after Monaco\".",
    asks=["AFP: which measure of “approvals”.", "Planning Authority: approvals of new buildings by year.",
          "Readers: say “in the EU” when you mean it."],
    footer="Version 1.0  ·  26 October 2026  ·  Public data only  ·  No right of reply needed",
    pdf_title="Claim Check 136 – Most crowded country in Europe?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
