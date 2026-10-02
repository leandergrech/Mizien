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
    title_lines=["Does more RO", "mean recovery?"],
    subtitle="Reverse-osmosis supply, groundwater status and the Għar Lapsi tender",
    quote_lines=["“70.7% ... from the four Reverse Osmosis plants”"],
    attribution="Water Services Corporation, Annual Report 2025",
    context="WSC production, 2022–2025 · Plant B tender, August 2026",
    note="A lower WSC groundwater share is not proof of aquifer recovery.",
    verdict="Largely supported", verdict_right=["WSC reliance fell;", "aquifer status remains poor."],
    cards=[
        ("70.7%", GREEN, "WSC production from RO", "In 2025, up from 64.3% in 2022."),
        ("−8.95%", ORANGE, "WSC groundwater production", "Change from 2022 to 2025; not total national abstraction."),
        ("2 aquifers", RED, "poor quantitative status", "The latest River Basin Management Plan says Malta and Gozo's main aquifers remain over-abstracted."),
        ("12 of 15", RED, "above nitrate standard", "The plan names three exceptions; nitrate is not the only cause of poor chemical status."),
        ("30,000 m³/day", BLUE, "planned Għar Lapsi Plant B", "Tendered in August 2026; not commissioned or measured output."),
    ],
    fair="RO supplied more of WSC's potable production and its groundwater component fell. The latest national aquifer assessment still reports poor status; a tender does not establish recovery.",
    asks=["Publish abstraction and recharge by groundwater body and user sector.",
          "Monitor water levels, salinity and nitrate on a comparable basis.",
          "Reconcile WSC's 11.4% narrative with its 11.86% chart-derived decline.",
          "Report Plant B's actual output and its effect on groundwater production."],
    footer="Version 1.0  ·  3 October 2026  ·  Draft pending right of reply",
    pdf_title="Claim Check 009 – Does more RO mean recovery?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
