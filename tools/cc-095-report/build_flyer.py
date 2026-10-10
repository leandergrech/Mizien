"""Claim Check 095 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, AMBER  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="095", out=str(OUT / "flyer.pdf"), kicker="Energy subsidies and prices",
    title_lines=["EUR 400 million a year", "to keep energy prices fixed?"],
    subtitle="The Finance Minister’s pre-budget figures, tested against EU data",
    quote_lines=["“I expect those numbers to remain at the same", "level next year.”"],
    attribution="Clyde Caruana, Minister for Finance, Pre-Budget Document 2027 launch, 30 Sep 2026 (BusinessNow)",
    context="On energy subsidies of about EUR 400m this year (EUR 391.7m presented) and the same next year.",
    note="He also said fuel, electricity and gas prices “have not changed”. Pre-Budget Document not read (403).",
    verdict="Not substantiated", verdict_right=["Prices held, as stated;", "the EUR 400m cannot yet be tested."],
    cards=[("0.0%", GREEN, "Prices unchanged",
            "Malta’s energy prices in the year to Aug 2026; EU-27 +13.0%. The only EU country with no rise."),
           ("EUR 1.21", GREEN, "Diesel, fixed since 2020",
            "A litre in every weekly EU Oil Bulletin since 15 Jun 2020; EU average EUR 2.15 on 5 Oct 2026."),
           ("391.7m", ORANGE, "An estimate, not spending",
            "EUR, the minister’s 2026 figure (energy and food). No 2026 spending figure yet; amount not shown elsewhere."),
           ("41%", ORANGE, "Forecasts have missed",
            "The Government’s 2023 figure (EUR 242.5m) against EUR 595m planned for 2023 in October 2022."),
           ("1.1%", AMBER, "Not alone in subsidising",
            "Of GDP on fuel and energy subsidies in 2024 (Eurostat): Bulgaria and Slovakia the same, Hungary 1.3%.")],
    fair="The minister gave next year’s figure as an expectation and said the bill could rise with world prices. His "
         "earlier figures fit Eurostat and the IMF. Keeping prices fixed in 2027 is a commitment, labelled “not yet due”.",
    asks=["The breakdown of the EUR 391.7m by measure.",
          "The price assumptions behind 2027.",
          "Yearly spending on the same basis since 2022.",
          "2026 spending data when published."],
    footer="Version 1.0  ·  10 October 2026  ·  Public data only  ·  Right of reply on hold until the Pre-Budget "
           "Document 2027 is read",
    pdf_title="Claim Check 095 – EUR 400 million a year to keep energy prices fixed?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
