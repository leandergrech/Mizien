"""Claim Check 016 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="016", out=str(OUT / "flyer.pdf"), kicker="Air quality, Grand Harbour",
    title_lines=["Does shore power cut", "pollution by 90%?"],
    subtitle="A public claim, tested against connection records, EU law and research",
    quote_lines=["“This initiative promises to slash 90%", "of air pollution in the Grand Harbour.”"],
    attribution="Infrastructure Malta, Shore-to-Ship project page, 1 December 2023",
    context="Repeated at the EUR 33 million project’s launch, 10 July 2024.",
    note="Connection records from Transport Malta, via an FOI request by Amphora Media.",
    verdict="Misleading", verdict_right=["Possible per ship,", "not what happened."],
    cards=[("Grade B", GREEN, "Works when ships plug in",
            "Research: time at berth causes most of a cruise ship’s emissions in port."),
           ("2030", ORANGE, "Voluntary until then",
            "EU law makes plugging in compulsory only from 1 January 2030."),
           ("9%", RED, "Of berth time plugged in",
            "67 of 373 berths connected, Jul 2024 – Jul 2025; one ship made half."),
           ("0%", RED, "Of long stays",
            "No ship staying two to four days plugged in."),
           ("+8%", ORANGE, "More cruise calls",
            "385 calls in 2025, up from 357 in 2024.")],
    fair="Shore power is a sound technology and use may grow. The 90% figure has no published basis, and no one has "
         "measured the harbour’s air before and after.",
    asks=["Transport Malta’s connection log.",
          "The basis of the 90% figure.",
          "ERA’s Senglea shipping study.",
          "Terms of the shore power deals."],
    footer="Version 1.0  ·  3 October 2026  ·  Public data only  ·  Right of reply: Infrastructure Malta (not yet sent)",
    pdf_title="Claim Check 016 – Does shore power cut pollution by 90%?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
