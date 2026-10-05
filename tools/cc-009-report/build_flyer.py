"""Build the CC-009 flyer in the shared Miżien design."""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, BLUE  # noqa: E402

OUT = ROOT / "claims" / "CC-009"
build_flyer(Flyer(
    number="009", out=str(OUT / "flyer.pdf"), kicker="Water, Malta",
    title_lines=["More RO, less", "WSC groundwater"],
    subtitle="What the Water Services Corporation’s figures show, and what they don’t",
    quote_lines=["“70.7% ... from the four Reverse Osmosis plants”"],
    attribution="Water Services Corporation, Annual Report 2025",
    context="WSC production, 2022–2025 · Plant B tender, August 2026",
    note="A lower WSC groundwater share is not proof of aquifer recovery.",
    verdict="Largely supported", verdict_right=["WSC reliance fell;", "aquifers last assessed as poor."],
    cards=[
        ("70.7%", GREEN, "WSC production from RO", "In 2025, up from 64.3% in 2022. WSC groundwater production fell to 11.5 million m³."),
        ("4%", ORANGE, "of national groundwater use", "WSC's 2025 cut (1.55 million m³) against an estimated 38.5 million m³ abstracted in 2024; 57% goes to farming."),
        ("0 of 15", RED, "bodies in good overall status", "Both main aquifers are over-abstracted; Malta's EU reporting lists all 15 as poor chemically."),
        ("15–40 yrs", RED, "travel time, Malta's main aquifer", "Peer-reviewed tracer study: changes in water quality take years to decades to show."),
        ("30,000 m³/day", BLUE, "planned Għar Lapsi Plant B", "Tendered in August 2026; not commissioned or measured output."),
    ],
    fair="RO supplied more of WSC's potable water and its groundwater production fell, to WSC's lowest in a decade. That is real, but small beside national use, and not proof of recovery.",
    asks=["Publish metered abstraction and recharge by groundwater body and user.",
          "Monitor water levels, salinity and nitrate on a comparable basis.",
          "Reconcile WSC's 11.4% narrative with its 11.86% chart-derived decline.",
          "Report Plant B's actual output and its effect on groundwater production."],
    footer="Version 1.2  ·  5 October 2026  ·  Draft pending right of reply (WSC; Energy and Water Agency)",
    pdf_title="Claim Check 009 – More RO, less WSC groundwater"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
