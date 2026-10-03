"""Claim Check 014 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="014", out=str(OUT / "flyer.pdf"), kicker="Planning enforcement, Malta",
    title_lines=["Fewer notices,", "or fewer illegalities?"],
    subtitle="A public claim, tested against twenty years of annual reports",
    quote_lines=["“We had times when we issued over 1,000", "enforcement notices per year.”"],
    attribution="Johann Buttigieg, Planning Authority CEO, The Malta Independent, 7 September 2025",
    context="Now around 200, which he attributed to there being fewer illegalities.",
    note="The Authority’s own 2024 report credits the fall to persuading contraveners first.",
    verdict="Misleading", verdict_right=["Accurate figures,", "incomplete explanation."],
    cards=[("1,033", GREEN, "Then: over 1,000 a year",
            "Average notices a year 2001–2009 (MEPA). The figure is right."),
           ("187", GREEN, "Now: around 200",
            "Average 2020–2024 (Planning Authority). Also right: notices fell 82%."),
           ("−11%", ORANGE, "Complaints barely fell",
            "2,701 complaints in 2009, 2,411 in 2024; 3,313 in 2020."),
           ("~1,200", RED, "Still confirmed illegal",
            "About half of 2024 complaints were confirmed as illegal development."),
           ("521", RED, "Settled by legalising",
            "In 2024 more cases ended in a sanctioning application than any other way; 162 got a notice.")],
    fair="The chief executive also said the Authority has struggled with enforcement. Persuading owners first is a "
         "recognised approach. This check is about what fewer notices can show.",
    asks=["Complaints and outcomes for 2012–2018.",
          "Any survey showing illegal building has fallen.",
          "How many cases end in a sanctioning permit.",
          "The yearly source of 1,500 direct actions."],
    footer="Version 1.0  ·  3 October 2026  ·  Public data only  ·  Draft pending right of reply from the Planning Authority",
    pdf_title="Claim Check 014 – Fewer notices, or fewer illegalities?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
