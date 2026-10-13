"""Claim Check 089 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="089", out=str(OUT / "flyer.pdf"), kicker="Population and infrastructure, Malta",
    title_lines=["Is growth outpacing", "infrastructure?"],
    subtitle="A public claim, tested against Eurostat and the World Bank",
    quote_lines=["“Infrastructure demands require", "urgent investment.”"],
    attribution="PwC Malta, posted by the Malta Chamber, 22 July 2026",
    context="Headline: population growth “creates urgent need”.",
    note="The wording is PwC’s; the Chamber carried it as sponsored content.",
    verdict="Largely supported", verdict_right=["Premises hold; one", "percentage is wrong."],
    cards=[("+2.44%", ORANGE, "Fastest growth in the EU",
            "Population grew 2.44% in 2025 (588,254 on 1 Jan 2026); EU-27 +0.16%."),
           ("391", RED, "Hospital beds per 100,000",
            "2024: 18th of 27, against 507 for the EU-27. PwC says 397 and 17th."),
           ("+34%", ORANGE, "Imports, not 25%",
            "PwC’s own figures (970 to 1,304 GWh) give +34%, not “circa 25%”."),
           ("636,000", GREEN, "2030 base case is plausible",
            "Between Eurostat’s baseline (621,470) and higher-migration (650,230).")],
    fair="Malta’s median age is 40.0 against 44.9 for the EU, and beds per head is a crude measure. PwC’s report was not "
         "readable, so its model is unchecked.",
    asks=["PwC’s report, with its assumptions.",
          "Planned beds and generation to 2030.",
          "A benchmark covering more than two indicators."],
    footer="Version 1.0  ·  13 October 2026  ·  Public data only  ·  No right of reply needed",
    pdf_title="Claim Check 089 – Is growth outpacing infrastructure?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
