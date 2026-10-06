"""Claim Check 101 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, GREY, ORANGE  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="101", out=str(OUT / "flyer.pdf"), kicker="Water, Malta",
    title_lines=["Does Malta authorise", "water abstraction?"],
    subtitle="The Commission’s description of Maltese law, tested against the law",
    quote_lines=["“Malta has failed to put in place … a prior",
                 "authorisation regime to control the abstraction …”"],
    attribution="European Commission, July infringements package (INF/26/1376), 8 July 2026",
    context="Summary of its letter of formal notice to Malta, INFR(2026)2115 (the letter is not published).",
    note="The same text cites registration of surface-water abstraction and periodic review of these controls.",
    verdict="Largely supported", verdict_right=["Matches Maltese law", "as published."],
    cards=[("Art. 11(3)(e)", GREEN, "What the EU requires",
            "Registers of abstraction, prior authorisation and periodic review. Abstractions with no significant "
            "impact may be exempted."),
           ("2008", GREEN, "Registered, not licensed",
            "Groundwater sources had to be notified by Nov 2008. The law says notification gives no right to draw "
            "water."),
           ("Proposed", ORANGE, "Permits still a plan",
            "A 2023 Green Paper proposes ERA abstraction permits; in 2025 Malta called them “close to being "
            "finalised”. None in force on 6 Oct 2026."),
           ("3.4 km", GREEN, "Little surface water",
            "Three short watercourses and two pools. We found no rule to register surface-water abstraction."),
           ("Review?", GREY, "Not rated: a legal point",
            "The law repeats the Directive’s duty to review; the rules that run the controls set no term or review.")],
    fair="Malta does control sources: the register closed in 2008, no new boreholes since 2010 bar sea-wells, "
         "most private sources metered. In 2019 the Commission’s staff called this an authorisation regime.",
    asks=["The letter of formal notice and Malta’s reply.",
          "The draft abstraction regulation (Measure 053) and its timetable.",
          "ERA’s count of registered, metered and reporting sources.",
          "What Malta reports to Eurostat as surface-water abstraction."],
    footer="Version 1.0  ·  6 October 2026  ·  Public documents and data only  ·  No right of reply needed",
    pdf_title="Claim Check 101 – Does Malta authorise water abstraction?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
