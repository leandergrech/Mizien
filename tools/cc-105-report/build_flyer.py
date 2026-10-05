"""Claim Check 105 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, GREY, AMBER  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="105", out=str(OUT / "flyer.pdf"), kicker="Noise, Malta",
    title_lines=["Noise near the Freeport", "and airport: never studied?"],
    subtitle="ADPD's call for a study, tested against official noise maps and local research",
    quote_lines=["“…yet to acknowledge that noise pollution is having an", "effect on the health of those who live near the Freeport…”"],
    attribution="ADPD – The Green Party, Birżebbuġa, 26 May 2026",
    context="Said by deputy chairpersons Carmel Cacopardo and Melissa Bagley.",
    note="No health-outcome study found; noise levels have been mapped or measured.",
    verdict="Largely supported", verdict_right=["No health study found,", "but noise is mapped or measured."],
    cards=[("0 of 5", RED, "ERA documents naming Freeport",
            "Of five read: round 4 mapping, two action plans, annex, airport report."),
           ("≈9,700", AMBER, "People in modelled aircraft noise",
            "At 55 dB Lden or more, 2016 (airport report). Exposure only, no health data."),
           ("5 of 5", AMBER, "Birżebbuġa points over 55 dBA",
            "By day, University of Malta survey 2020–21; Freeport named as a main source."),
           ("98%", GREY, "Residents calling noise a problem",
            "477 questionnaires (2022 paper); self-reported, not clinical."),
           ("2014–15", GREY, "Freeport-funded noise study",
            "Reported by TVM; the report itself not seen.")],
    fair="Noise near both sites has been measured or mapped; a health study of residents is still missing.",
    asks=["ERA: is the Freeport covered by any noise mapping?", "Malta Freeport Terminals: the 2014–15 report.",
          "Public Health: any health assessment of residents."],
    footer="Version 1.0  ·  5 October 2026  ·  Public sources  ·  No right of reply needed",
    pdf_title="Claim Check 105 – Noise near the Freeport and airport"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
