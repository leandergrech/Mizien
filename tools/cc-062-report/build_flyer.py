"""Claim Check 062 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="062", out=str(OUT / "flyer.pdf"), kicker="Planning and housing, Malta",
    title_lines=["Is construction", "9% or 14% of the economy?"],
    subtitle="A KPMG report’s shares of GVA, tested against its tables and Eurostat",
    quote_lines=["“…around 9% of Gross Value Added … rising to", "approximately 14% once indirect linkages are factored in.”"],
    attribution="KPMG (Steve Stivala), foreword, Construction Industry and Property Market Report 2025",
    context="Construction and real estate; report commissioned by the Malta Development Association.",
    note="Direct share is KPMG’s Table 1.1; the 14% is Table 1.3.",
    verdict="Largely supported", verdict_right=["Both figures reproduce;", "bases differ."],
    cards=[("9.1%", GREEN, "The direct share reproduces",
            "KPMG: 9.1% of GVA in 2024. Eurostat’s current series: 9.6% on the same definition."),
           ("14.0%", GREEN, "The 14% reproduces too",
            "EUR 3,002 million of EUR 21,378 million in KPMG’s Table 1.3; its output inputs match Eurostat."),
           ("+3.2 pp", ORANGE, "Not the same basis",
            "The 14% counts imputed rents (owner-occupiers’ housing); the 9% does not. That is 3.2 of the 4.9 points."),
           ("+1.7 pp", ORANGE, "Linkages add less than they look",
            "On a like-for-like basis the direct share is 12.3%, so modelled indirect linkages add 1.7 points."),
           ("2015", RED, "Old multipliers",
            "Based on the 2015 input-output table; we could not re-derive them from Eurostat’s partial Maltese table.")],
    fair="KPMG discloses its method and warns the multipliers rest on assumptions; Table 1.1 says real estate "
         "excludes imputed rents. The foreword sentence does not.",
    asks=["The CBM or NSO multiplier table (0.55; 0.78).",
          "Multipliers from a newer NSO table.",
          "A note that 9% excludes and 14% includes imputed rents.",
          "Which NSO vintage the 2024 figures use."],
    footer="Version 1.0  ·  8 October 2026  ·  Public data only  ·  No right of reply needed",
    pdf_title="Claim Check 062 – Is construction 9% or 14% of the economy?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
