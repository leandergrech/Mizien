"""Claim Check 116 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, GREY, AMBER  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="116", out=str(OUT / "flyer.pdf"), kicker="Heritage and planning, Valletta",
    title_lines=["UNESCO: Valletta's", "setting not safeguarded?"],
    subtitle="Reading the World Heritage Committee's decision against what was reported",
    quote_lines=["“…the current planning policies and regulations do not", "sufficiently safeguard the setting of the property…”"],
    attribution="UNESCO World Heritage Committee, Decision 47 COM 7B.114, City of Valletta, 2025",
    context="Adopted at the Committee's 47th session; read in full on 14 October 2026.",
    note="The claim reports the decision accurately. We did not test the policies themselves.",
    verdict="Supported", verdict_right=["The decision says what the claim says;", "it does not threaten delisting."],
    cards=[("10 of 10", GREEN, "Phrases of the claim found",
            "Concern about planning policies, height controls, buffer zone and the report date are all in the adopted text."),
           ("4", GREY, "Documents to be revised",
            "The Views and Vistas Analysis, the 2006 North Harbour Local Plan, the 2014 Floor Area Ratio guide and the 2022 Grand Harbour Local Plan."),
           ("0", GREEN, "Mentions of the Danger List",
            "The decision has no request about delisting or the List of World Heritage in Danger."),
           ("Welcomed", AMBER, "Buffer zone proposal",
            "The Committee welcomes the buffer zone proposal and asks for it to be developed, especially its northern boundary."),
           ("1 Dec 2026", AMBER, "Updated report due",
            "For the Committee's 49th session. The decision gives no reason for the date.")],
    fair="The Opposition and the Ministry each summarised the decision as reported; each stretches one half of the text "
         "(Section 4 of the report).",
    asks=["Planning Authority: the revised Views and Vistas Analysis.", "Malta's updated report, due 1 December 2026.",
          "ICOMOS's technical review of the Views and Vistas Analysis.", "Revised local plans and buffer zone, when published."],
    footer="Version 1.0  ·  14 October 2026  ·  No right of reply needed",
    pdf_title="Claim Check 116 – UNESCO: Valletta's setting not safeguarded?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
