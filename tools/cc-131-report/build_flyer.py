"""Claim Check 131 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, GREY  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="131", out=str(OUT / "flyer.pdf"), kicker="Waste and the circular economy",
    title_lines=["Malta’s construction", "waste: 100% recovered?"],
    subtitle="The Commission’s 2026 Country Report, checked against the JRC and Eurostat",
    quote_lines=["“By contrast, the rate of recovery of construction and", "demolition waste is 100, above the EU average of 89%.”"],
    attribution="European Commission, 2026 Country Report – Malta, 3 June 2026",
    context="Annex 8 (circular economy), citing a 2024 JRC assessment.",
    note="The sentence follows Malta’s low municipal and plastic recycling rates.",
    verdict="Largely supported", verdict_right=["Right on the legal measure;", "most of it was backfilling."],
    cards=[("100%", GREEN, "Malta, 2020 and 2022", "Recovered: all but 12 of 2.95 million tonnes in 2020. The report omits the % sign."),
           ("90.9%", GREEN, "EU-27, 2020", "Current Eurostat data. The 89% cited is from an older release; 91.4% in 2022."),
           ("58%", ORANGE, "Backfilling, 2020", "Most of Malta’s ‘recovery’ filled excavations such as spent quarries. EU: 12%."),
           ("42%", ORANGE, "Recycling, 2020", "Recycling alone: 21st of 27. It rose to 67% in 2022 (EU 80%)."),
           ("16 → 100", ORANGE, "2010 to 2012", "Quarry deposits were reclassified from landfill to backfilling.")],
    fair="EU law counts backfilling towards its 70% target, so the figure is correct. Recovery is not the same as recycling.",
    asks=["Commission: state the unit and the current EU value.", "ERA: how quarry deposits meet the backfilling definition.",
          "NSO: 2024 tables by operation.", "No right of reply needed."],
    footer="Version 1.0  ·  26 October 2026  ·  Public data only  ·  No right of reply needed",
    pdf_title="Claim Check 131 – Malta's construction waste recovery"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
