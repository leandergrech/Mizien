"""Claim Check 123 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="123", out=str(OUT / "flyer.pdf"), kicker="Planning and housing, Malta",
    title_lines=["How many homes", "were approved?"],
    subtitle="A KPMG report’s residential approval figures, tested against official counts",
    quote_lines=["“…8,716 residential units were granted approval in 2024,", "representing a 7.4% increase compared with 2023.”"],
    attribution="KPMG, Construction Industry and Property Market Report 2025, section 2.1",
    context="Dec 2025; prepared for the Malta Development Association.",
    note="Planning Authority series; NSO quarterly releases read second-hand.",
    verdict="Largely supported", verdict_right=["Figures match;", "“permits” = units."],
    cards=[("8,716", GREEN, "2024 reproduces",
            "The Planning Authority’s approved dwelling units: 8,716 in 2024, 8,112 in 2023."),
           ("+7.4%", GREEN, "The growth rate reproduces",
            "8,716 / 8,112 is +7.45%. Eurostat’s narrower index of dwellings permitted: +7.3%."),
           ("5,170", ORANGE, "Units, not permits",
            "January–June 2025: the NSO’s two quarters sum to 5,170 dwellings (+9.7%, second-hand). Building permits: about 1,023."),
           ("12,325", GREEN, "The forecast came true",
            "KPMG expected 2025 to surpass 2024. The Planning Authority’s 2025 figure is 12,325, +41%."),
           ("1", RED, "One unexplained unit",
            "The NSO’s 2024 quarters sum to 8,717, one more than 8,716 (second-hand).")],
    fair="Every number in section 2.1 matches official counts. The noun “permits” for dwelling units is the only loose "
         "wording.",
    asks=["The NSO’s Q1 and Q2 2025 releases, read directly.",
          "The Planning Authority file re-read to confirm 2025 is a full year.",
          "KPMG’s note on “permits” versus dwelling units."],
    footer="Version 1.0  ·  16 October 2026  ·  Public data only  ·  No right of reply needed",
    pdf_title="Claim Check 123 – How many homes were approved?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
