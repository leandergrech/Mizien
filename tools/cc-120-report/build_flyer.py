"""Claim Check 120 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="120", kicker="Noise, Malta",
    out=str(OUT / "flyer.pdf"),
    title_lines=["54,000 exposed", "to road noise?"],
    subtitle="A European Parliament study, tested against the EEA",
    quote_lines=["“…54 000 inhabitants of Malta are being", "exposed to road noise levels over 55dB (Lden).”"],
    attribution="Hjerp and Coffey, study for the EP Petitions Committee, February 2026",
    context="Key findings on road and aircraft noise exposure and health burden.",
    note="Opinions are the authors’, not the Parliament’s.",
    verdict="Largely supported", verdict_right=["Figures match the EEA; health", "numbers outdated."],
    cards=[("54,000", GREEN, "Matches the EEA table",
            "Road noise above 55 dB Lden; 11,100 for aircraft. The EEA says such figures likely understate."),
           ("30", GREEN, "Fewest deaths in the EU",
            "Premature deaths a year from transport noise; Estonia is next at 80. Study says 20 (outdated)."),
           ("4th", ORANGE, "Low DALYs on END basis",
            "150 per 100,000, tied 4th lowest of 27. Study says 100."),
           ("11th", ORANGE, "Mid-table on WHO levels",
            "310 DALYs per 100,000, below the EU median of 350."),
           ("31.3%", RED, "Highest survey noise",
            "People reporting street or neighbour noise, 2023 (EU 18.1%).")],
    fair="The study’s Malta health numbers pre-date an EEA correction of 27 March 2026; the rankings are unchanged. "
         "The size of the underestimate for Malta is not known.",
    asks=["EEA’s June 2025 table to confirm the study’s figures.",
          "Malta’s noise-mapping coverage, Round 4.",
          "Health estimates below the Directive thresholds."],
    footer="Version 1.0  ·  14 October 2026  ·  Public data only  ·  No right of reply needed",
    pdf_title="Claim Check 120 – 54,000 exposed to road noise?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
