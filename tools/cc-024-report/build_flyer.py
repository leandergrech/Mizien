"""Claim Check 024 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, BLUE  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="024", kicker="Climate and energy, Malta",
    out=str(OUT / "flyer.pdf"),
    title_lines=["Renewables by 2030:", "onshore and offshore?"],
    subtitle="Malta’s national energy plan, tested against its own sums and Eurostat data",
    quote_lines=["“Increase the Renewable Energy contribution from", "11.5% to 25% through multiple initiatives …”"],
    attribution="Government of Malta, final updated National Energy and Climate Plan, December 2024",
    context="The plan lists offshore technologies as a means; its 2030 projection counts none.",
    note="The plan’s own projection (24.5%) counts no offshore wind: it is not expected to be commissioned by 2030.",
    verdict="Not substantiated", verdict_right=["On the plan’s own path;", "offshore means not counted."],
    cards=[("24.5%", GREEN, "The 2030 figure",
            "The plan projects 24.5% (summary: 25%). 11.5% is the earlier contribution the plan raises."),
           ("0 MW", RED, "Offshore wind counted",
            "“Offshore wind does not contribute” to 2030, the plan says; its 350 MW is dated 2030 in one place, 2050 in another."),
           ("17.2%", GREEN, "Share in 2024 (Eurostat)",
            "Ahead of the plan’s own 15.5% path (the Commission’s reference points are higher). The rise is in heating and cooling; the electricity share moved from 9.5% to 10.7%."),
           ("350 MWp", ORANGE, "Solar PV expected by 2030",
            "From 241 MWp at end-2023, the plan’s own figures (pp. 74, 84). It gives no sum in points of share."),
           ("28%", BLUE, "The Commission’s formula",
            "It finds 24.5% below the 28% its formula gives, and the 2025 and 2027 points below its reference points.")],
    fair="Malta is ahead of the plan’s own path (pledge label: on track, on that path only). The plan itself discloses that offshore wind "
         "is left out of the 2030 sum. Cyprus, another island, reached 20.8% in 2024.",
    asks=["A breakdown of the 24.5% by technology and sector.",
          "When offshore wind is expected to be commissioned.",
          "The planned pace of solar PV additions to 2030.",
          "The 2019 plan’s wording on the 11.5% figure."],
    footer="Version 1.1  ·  6 October 2026  ·  Public data only  ·  Draft, pending right of reply",
    pdf_title="Claim Check 024 – Renewables by 2030: onshore and offshore?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
