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
    note="The Authority’s own reports: it issues notices “only where contraveners are uncooperative”.",
    verdict="Misleading", verdict_right=["Accurate figures,", "incomplete explanation."],
    cards=[("1,033", GREEN, "Then: over 1,000 a year",
            "Average notices a year 2001–2009 (MEPA). The figure is right."),
           ("187", GREEN, "Now: around 200",
            "Average 2020–2024 (Planning Authority reports). Also right: notices fell 82%."),
           ("~2,860", ORANGE, "Complaints stayed high",
            "A year on average in 2017–2024: more than in 2009 (2,701) or 2011 (2,105)."),
           ("~1,200", RED, "Still confirmed illegal",
            "Complaints confirmed as illegal in 2024, close to 2018 (~1,280)."),
           ("7–13", RED, "Notices per 100 cases",
            "Of complaints confirmed as illegal, 2018–2024. Most end in removal or an application to legalise.")],
    fair="The chief executive also said the Authority has struggled with enforcement. Persuading owners first is a "
         "recognised approach, and most notices now carry daily fines. This check is about what fewer notices can show.",
    asks=["Complaints and outcomes for 2012–2016.",
          "Any survey showing illegal building has fallen.",
          "How many cases end in a sanctioning permit.",
          "The yearly source of 1,500 direct actions."],
    footer="Version 1.2  ·  5 October 2026  ·  Public data only  ·  Draft pending right of reply from the Planning Authority",
    pdf_title="Claim Check 014 – Fewer notices, or fewer illegalities?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
