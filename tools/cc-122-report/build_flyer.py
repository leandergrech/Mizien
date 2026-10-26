"""Claim Check 122 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, GREENC, ORANGE, RED, AMBER  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="122", out=str(OUT / "flyer.pdf"), kicker="Tourism and population, Malta",
    title_lines=["30,000 more", "hotel beds?"],
    subtitle="A news report, tested against Eurostat",
    quote_lines=["“Applications … include proposals for approximately", "30,000 additional hotel beds.”"],
    attribution="The Shift News, 29 August 2026",
    context="“The Shift is informed”: no document, list or method published.",
    note="Applications validated before the new rules of 15 June 2026; hotels and extensions.",
    verdict="Not substantiated", verdict_right=["The sums hold,", "the 30,000 is not shown."],
    cards=[("30,000", ORANGE, "Source not shown",
            "An unnamed source. The MTA gave no figure and the Planning Authority did not reply, says the outlet."),
           ("7.67m", GREENC, "Guest nights: correct",
            "30,000 beds × 365 nights × 70% occupancy reproduces The Shift’s 7.7 million."),
           ("1.8–2.2m", GREENC, "Arrivals: correct, at full occupancy",
            "Every bed full all year at 5–6 nights. At 70%, as for the nights: 1.3–1.5 million."),
           ("+52%", ORANGE, "Large against today",
            "Eurostat counts 58,099 bed-places in 2025. A wider measure than hotel beds."),
           ("4.6", AMBER, "Nights a stay",
            "Non-residents stayed 4.6 nights per arrival at establishments in 2025 (assumed 5–6).")],
    fair="Other pipeline measures are of the same order (27,672 beds on the MTA list, April 2024), so the scale is "
         "plausible. Applications are not permits or built beds.",
    asks=["The Planning Authority’s count of validated hotel applications.",
          "Their beds, category, location and status.",
          "MTA compliance-certificate applications.",
          "The source of The Shift’s figure."],
    footer="Version 1.0  ·  14 October 2026  ·  Public data only  ·  Pending right of reply",
    pdf_title="Claim Check 122 – 30,000 more hotel beds?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
