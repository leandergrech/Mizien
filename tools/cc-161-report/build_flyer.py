"""Claim Check 161 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="161", out=str(OUT / "flyer.pdf"), kicker="Nightlife noise, Malta",
    title_lines=["“Without effective", "remedy”?"],
    subtitle="A public finding, tested for the evidence behind it",
    quote_lines=["“Residents complain without", "effective remedy.”"],
    attribution="Parliamentary Ombudsman, Part 2 of a two-part note, 3 March 2026",
    context="Said of regular nightlife venues licensed close to homes.",
    note="Part 1 of the note documents fragmented, complaint-driven enforcement.",
    verdict="Not substantiated", verdict_right=["A structural case,", "but no outcome data."],
    cards=[("5", GREEN, "Laws, several enforcers",
            "Part 1 lists five laws and their authorities: the Ombudsman’s own account."),
           ("0", ORANGE, "Outcome figures offered",
            "Part 2 gives no counts of complaints, fines or closures."),
           ("98", ORANGE, "Police reports, 4 towns",
            "Jan 2021 to Jun 2022 (second-hand); an input, not an outcome."),
           ("1", GREEN, "Remedy shown: boat parties",
            "Notice to Mariners 115 of 2025 after Ombudsman action. A different case."),
           ("?", RED, "Complaints resolved",
            "No published figure on how many noise complaints end in action.")],
    fair="The Ombudsman’s note is a legal analysis of human-rights case law, not a statistical study. This check asks "
         "only whether the outcome statement can be tested with public data.",
    asks=["Complaints to police, PA, ERA and councils.",
          "Outcomes: fines, closures, time to resolve.",
          "The cases behind the Ombudsman’s finding.",
          "Part 1’s recommendations: who acts, by when."],
    footer="Version 1.0  ·  9 November 2026  ·  Public data only  ·  Draft pending right of reply from the Ombudsman",
    pdf_title="Claim Check 161 – Without effective remedy?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
