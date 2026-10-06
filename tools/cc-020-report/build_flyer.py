"""Claim Check 020 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="020", out=str(OUT / "flyer.pdf"), kicker="Noise, Malta",
    title_lines=["Is the noise law", "to blame?"],
    subtitle="A European Parliament study, tested against Eurostat and WHO levels",
    quote_lines=["“…not the cause of the noise", "problems in Malta.”"],
    attribution="Hjerp and Coffey, study for the EP Petitions Committee, February 2026",
    context="On transposition and implementation of the Environmental Noise Directive.",
    note="Opinions are the authors’, not the Parliament’s.",
    verdict="Largely supported", verdict_right=["Law is not the cause; that does", "not mean Malta is quiet."],
    cards=[("Grade C", GREEN, "Study holds together",
            "Two meaningful non-conformities; no END infringement case 2015–2025 (per the study)."),
           ("31.3%", RED, "Highest noise in the EU",
            "People reporting street or neighbour noise, 2023 (EU 18.1%)."),
           ("55 dB", ORANGE, "Thresholds above WHO",
            "END reporting threshold 55 dB; WHO road level 53 dB, aircraft 45 dB."),
           ("Outside", ORANGE, "Complaints mostly outside END",
            "Per the study, most complaints concern construction, entertainment and neighbourhood noise, outside the Directive."),
           ("2025", ORANGE, "Action plan late",
            "Plan due January 2025 not published by January 2026.")],
    fair="Malta has had no END infringement case in 2015–2025, per the study. We did not re-check the law, and the "
         "21% vs 9% survey figure has no identified source.",
    asks=["The survey behind the 21% vs 9% figure.",
          "Complaint data on construction and entertainment noise.",
          "Date of the next Action Plan.",
          "Legal check of the transposition table."],
    footer="Version 1.1  ·  6 October 2026  ·  Public data only  ·  No right of reply needed",
    pdf_title="Claim Check 020 – Is the noise law to blame?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
