"""Claim Check 113 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="113", out=str(OUT / "flyer.pdf"), kicker="Energy subsidies, Malta and the EU",
    title_lines=["Malta among the EU’s highest", "fossil-fuel subsidies relative to GDP?"],
    subtitle="An EEA ranking, rebuilt from the Commission’s subsidy database",
    quote_lines=["“… the highest shares of [GDP] in Malta, Poland,", "and Slovakia (all at or above 1.5%).”"],
    attribution="European Environment Agency, Fossil fuel subsidies in Europe, published 29 Jan 2025",
    context="The sentence begins “In 2023, fossil fuel subsidies represented”; [GDP] abridges “gross domestic product "
            "(GDP)”.",
    note="Same wording in every copy we read (3 Feb 2025 to 6 Oct 2026). Subsidies counted the EU way, from Commission "
         "data.",
    verdict="Largely supported", verdict_right=["The ranking is right;", "the 1.5% line is close."],
    cards=[("3.37%", GREEN, "Reproduced exactly",
            "Malta’s 2023 share of GDP on the EEA’s data. Poland 2.09%, Slovakia 1.51%; EU-27 as a whole 0.66%."),
           ("Top 3", GREEN, "A robust ranking",
            "The same three lead with Eurostat’s GDP and, as a lower bound, without the unconfirmed items."),
           ("1.49%", ORANGE, "Slovakia at the line",
            "With Eurostat’s GDP of Oct 2026 (later than the EEA’s), Slovakia falls just under 1.5%."),
           ("96%", ORANGE, "One measure",
            "Of Malta’s 2023 figure: compensation to Enemalta for keeping energy prices frozen."),
           ("2.1×", ORANGE, "Size uncertain",
            "The 2023 amount is 2.1 times the IMF Article IV estimate of Malta’s energy-subsidy cost; for 2022 it was lower.")],
    fair="Before 2021 Malta was among the EU’s lowest (about 0.1% of GDP). In euros it is 19th of 27. The IMF’s "
         "price-gap data record no explicit subsidy for Malta. The Commission’s 2026 report puts Malta first again, "
         "for 2024.",
    asks=["The source and basis of Malta’s EUR 580m.",
          "Final 2023 figures for every country.",
          "Malta’s yearly outturn cost of energy support.",
          "The GDP series behind the EEA’s chart."],
    footer="Version 1.0  ·  6 October 2026  ·  Public data only  ·  Draft · no right of reply needed",
    pdf_title="Claim Check 113 – Malta among the EU's highest fossil-fuel subsidies?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
