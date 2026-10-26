"""Claim Check 128 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="128", kicker="Water, Malta",
    out=str(OUT / "flyer.pdf"),
    title_lines=["Missed the water-", "plan timetable?"],
    subtitle="The Commission’s statement on the third river basin plan, tested",
    quote_lines=["“Malta did not consult on, adopt or report the RBMP", "according to the WFD timetable.”"],
    attribution="European Commission, staff working document SWD(2026) 702, 2 October 2026",
    context="Plan published March 2024; reporting deadline March 2022.",
    note="The check is about dates, not the plan’s content.",
    verdict="Largely supported", verdict_right=["The dates fit the Directive and", "the Commission’s earlier report."],
    cards=[("22 Dec 2021", GREEN, "Plan due", "Article 13(7) of the Water Framework Directive: third plan, every six years."),
           ("18 Mar 2024", RED, "Draft still open", "BirdLife Malta’s comments on the draft plan carry this date."),
           ("817 days", RED, "The least the delay can be", "From the due date to the day the draft was still open."),
           ("5 of 27", ORANGE, "No plans by Sep 2023", "Bulgaria, Cyprus, Greece, Malta and Portugal at the Commission’s cut-off."),
           ("March 2024", ORANGE, "Published, per the Commission", "The month rests on the Commission; the day is not confirmed.")],
    fair="Late plans were common: the Commission says “many adopted them late” and opened proceedings against all Member States.",
    asks=["ERA’s dated notice of adoption.", "The EEA’s delivery record for Malta’s plan.", "Which ‘March 2022’ the Commission means."],
    footer="Version 1.0  ·  19 October 2026  ·  Public data only  ·  No right of reply needed",
    pdf_title="Claim Check 128 – Did Malta miss the water-plan timetable?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
