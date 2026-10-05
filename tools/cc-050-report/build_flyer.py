"""Claim Check 050 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, GREY, AMBER  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="050", out=str(OUT / "flyer.pdf"), kicker="Nature and wildlife, Malta",
    title_lines=["A “race to weaken", "hunting laws”?"],
    subtitle="BirdLife Malta's claim about Labour and the PN, tested",
    quote_lines=["“…dangerous political race to weaken", "environmental enforcement”"],
    attribution="BirdLife Malta, press release headline, 27 May 2026",
    context="Issued three days before the 2026 general election.",
    note="Fines for shooting protected birds have not been cut: they are only proposed.",
    verdict="Not substantiated", verdict_right=["Shown for Labour;", "not shown for the PN."],
    cards=[("Items 63–64", GREEN, "Labour manifesto",
            "Safeguards hunting within EU-permitted derogations; nothing on fines."),
           ("-40%", AMBER, "Reported ORNIS proposal",
            "Fines for shooting protected birds: EUR 5,000 to 3,000 and 10,000 to 6,000."),
           ("“Safeguarded”", GREY, "Alex Borg, PN, 26 May",
            "No mention of the Birds Directive, fines or licences."),
           ("0 of 16", GREY, "PN programme chapters",
            "None has a hunting or trapping item."),
           ("EUR 5,000", GREEN, "Fine in force today",
            "First conviction; EUR 10,000 for a repeat. No 2026 amendment found.")],
    fair="The Labour side is documented. The PN side rests on one pledge and a reading of EU law.",
    asks=["BirdLife Malta: sources for the candidate claims.", "Government: the ORNIS presentation and minutes.",
          "PN: does 'safeguarded' include penalties?", "PN: any hunting item beyond the programme?"],
    footer="Version 1.0  ·  5 October 2026  ·  Public sources  ·  Draft, pending right of reply",
    pdf_title="Claim Check 050 – A race to weaken hunting laws?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
