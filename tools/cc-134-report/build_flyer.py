"""Claim Check 134 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, GREY  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="134", out=str(OUT / "flyer.pdf"), kicker="Climate policy and taxation",
    title_lines=["Malta’s environmental", "taxes"],
    subtitle="The Commission’s 2026 Country Report, checked against Eurostat",
    quote_lines=["“Total environmental tax revenue is lower than", "the EU average (1.4% of GDP in 2024 against 2.1%).”"],
    attribution="European Commission, 2026 Country Report – Malta, 3 June 2026",
    context="Annex 10 (circular economy), with Annex 3 on taxation.",
    note="The report also gives energy and transport shares for 2023 and pollution taxes of 0.18% of GDP.",
    verdict="Largely supported", verdict_right=["Figures exact; one number", "is from the year before."],
    cards=[("1.35%", GREEN, "Malta, 2024", "Environmental taxes as a share of GDP: EUR 312.5 million on GDP of EUR 23,079 million."),
           ("2.08%", GREEN, "EU-27, 2024", "The Commission rounds to 1.4% and 2.1%. The gap is 0.73 points of GDP."),
           ("25th", ORANGE, "Of 27 states", "Only Ireland (0.98%) and Luxembourg (1.18%) are lower. Malta was 2.38% in 2019."),
           ("49 / 41", GREEN, "Energy / transport", "2023 shares: 48.5% and 41.6%. Together 90% of the total."),
           ("0.15%", ORANGE, "Pollution taxes, 2023", "The report says 0.18%, which is Eurostat’s 2022 value. Still above the EU’s 0.08%.")],
    fair="This tests the figures, not whether Malta should tax more. Revenue as a share of GDP is not a measure of policy strictness.",
    asks=["Commission: the data vintage behind the 0.18%.", "Finance Ministry: revenue by tax behind the three categories.",
          "Eurostat: any revision of Malta's 2024 values.", "No right of reply needed."],
    footer="Version 1.0  ·  26 October 2026  ·  Public data only  ·  No right of reply needed",
    pdf_title="Claim Check 134 – Malta's environmental taxes"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
