"""Claim Check 029 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, GREY  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="029", out=str(OUT / "flyer.pdf"), kicker="Climate and energy",
    title_lines=["Malta’s first offshore", "wind farm: on schedule?"],
    subtitle="The Energy Ministry’s capacity, bids and timetable, tested against public records",
    quote_lines=["“…an installed capacity of approximately 300MW…”", "Candidates told “by the first part of next year”."],
    attribution="Energy Ministry statement, 22 July 2025 (as reported by TVM News)",
    context="Statement as reported; only Minister Dalli’s words are in quotation marks in the source.",
    note="The ministry’s own release was not readable by us; we used TVM News, Newsbook and InterConnect Malta’s pages.",
    verdict="Largely supported", verdict_right=["The facts hold;", "the timetable is Off track."],
    cards=[("≈300 MW", GREEN, "Floating wind farm",
            "Beyond 12 nautical miles, in the planned EEZ, per InterConnect Malta. Two sites on offer, one to be built."),
           ("3", GREEN, "Submissions, July 2025",
            "Code Zero Consortium, Atlas Med Wind and MCKEDRIK, announced by the ministry."),
           ("24.6%", GREEN, "Of 2025 electricity supplied",
            "The farm’s 0.8 TWh a year, against Eurostat’s 3,252 GWh. ICM says about a quarter."),
           ("0", ORANGE, "Public notices of the next stage",
            "None found by 6 Oct 2026 for the step due “in the first part” of 2026. A EUR 3.6 million survey tender came in April."),
           ("2 yrs", GREY, "Of site data to be collected",
            "The survey for developers runs two years, so a concession looks later. Pledge label: Off track (as of 6 Oct 2026).")],
    fair="The project is real and active. A candidate notice may have been sent privately; we rate only what has been published.",
    asks=["When candidates were told the result.", "A current timetable for the dialogue stage.",
          "The metocean tender award.", "The NECP offshore wind assumption."],
    footer="Version 1.0  ·  6 October 2026  ·  Public data only  ·  Draft pending right of reply (pledge label)",
    pdf_title="Claim Check 029 – Malta's first offshore wind farm: on schedule?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
