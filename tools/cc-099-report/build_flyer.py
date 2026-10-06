"""Claim Check 099 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, GREY  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="099", out=str(OUT / "flyer.pdf"), kicker="Population, Malta",
    title_lines=["31% foreign now,", "38% by 2030?"],
    subtitle="A business statement, tested against Eurostat, NSO and Jobsplus data",
    quote_lines=["“foreign residents now make up 31% of Malta’s population”",
                 "“…potentially reaching around 38% by 2030.”"],
    attribution="PwC Malta, Summer 2026 Economic Update press release, as posted by Finance Malta, 17 July 2026",
    context="The 38% is “the mix of foreign to local residents”, from PwC’s own demographic model.",
    note="“Foreign” is not defined in the release; the 31% matches the count of non-Maltese citizens.",
    verdict="Not substantiated", verdict_right=["31% is right;", "38% by 2030 not shown."],
    cards=[("31%", GREEN, "Right for end-2025",
            "Our calculation from Eurostat data, if 2025’s change was within the 2010–24 range: 30.9–31.1% non-Maltese citizens."),
           ("32.0%", GREY, "Higher by birthplace",
            "Residents born abroad on 1 January 2025 (Eurostat). Definitions change the figure."),
           ("39.8%", GREY, "Higher still in jobs",
            "Foreign nationals’ share of registered employment, December 2025 (Jobsplus)."),
           ("38%", ORANGE, "PwC’s own model",
            "We found no Eurostat or NSO projection by citizenship. PwC’s report could not be read."),
           ("≥1,610", RED, "What about 38% needs",
            "Fewer Maltese citizens a year in 2026–30 for 37.5–38.5% of PwC’s 636,000. They rose every year 2010–2024.")],
    fair="PwC’s current figure is right, and it labels the 2030 figure as a projection (“potentially”, “around”). "
         "This check asks only whether the 38% can be shown from published data.",
    asks=["How “foreign” and “local” are defined for 2030, and whether naturalisations are counted.",
          "The base-case local population for 2030.",
          "The share at 624,000 and at 660,000 (♦ range known second-hand).",
          "The NSO’s end-2025 table by citizenship."],
    footer="Version 1.0  ·  6 October 2026  ·  Public data only  ·  Right of reply on hold until PwC’s report is read",
    pdf_title="Claim Check 099 – 31% foreign now, 38% by 2030?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
