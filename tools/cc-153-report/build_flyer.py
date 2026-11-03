"""Claim Check 153 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="153", out=str(OUT / "flyer.pdf"), kicker="Planning and housing, Malta",
    title_lines=["Did Malta miss the", "renovation-plan deadline?"],
    subtitle="A Commission infringement notice, checked against the Commission’s own pages",
    quote_lines=["“…Malta (INFR(2026)2027)… failed to submit their draft", "National Building Renovation Plan… by the deadline of 31 December 2025”"],
    attribution="European Commission, March infringements package, 12 March 2026",
    context="The Commission gave the 19 Member States two months to respond.",
    note="The Commission’s notice states its view; a letter of formal notice is a first step, not a ruling.",
    verdict="Supported", verdict_right=["The notice, case number,", "deadline and period all check out."],
    cards=[("Grade C", GREEN, "Official documents",
            "Commission notice, the Directive’s Article 3 and the Commission’s plan register."),
           ("19", ORANGE, "Member States notified",
            "Malta (INFR(2026)2027) and 18 others, 12 March 2026."),
           ("31 Dec 2025", GREEN, "Draft-plan deadline",
            "Set by Article 3 of Directive (EU) 2024/1275."),
           ("0", RED, "Entries for Malta",
            "On the Commission’s plan page on 3 November 2026; 18 States and Wallonia are listed."),
           ("?", ORANGE, "Status since March",
            "Not confirmed either way; the register may lag.")],
    fair="This is a reporting deadline, not a measure of how many buildings Malta has renovated.",
    asks=["Whether Malta has submitted its draft plan.",
          "The Commission’s register entry for INFR(2026)2027.",
          "The date of Malta’s public consultation, if held."],
    footer="Version 1.0  ·  3 November 2026  ·  Public documents only  ·  No right of reply needed",
    pdf_title="Claim Check 153 – Did Malta miss the renovation-plan deadline?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
