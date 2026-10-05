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
    title_lines=["Renewables by 2030:", "solar PV and offshore wind?"],
    subtitle="Malta’s national energy plan, tested against its own sums and Eurostat data",
    quote_lines=["“Increase the Renewable Energy contribution from", "11.5% to 25% through multiple initiatives …”"],
    attribution="Government of Malta, final updated National Energy and Climate Plan, December 2024",
    context="Our record summarises it as reaching the 2030 share through solar PV and offshore wind.",
    note="The plan’s own projection (24.5%) counts no offshore wind: it is not expected to be commissioned by 2030.",
    verdict="Not substantiated", verdict_right=["Target on its path;", "the route is not shown."],
    cards=[("24.5%", GREEN, "The 2030 figure",
            "The plan projects 24.5% (summary: 25%). The 11.5% in some summaries is the earlier contribution."),
           ("0 MW", RED, "Offshore wind counted",
            "“Offshore wind does not contribute” to 2030, the plan says; its 350 MW is dated 2030 in one place, 2050 in another."),
           ("17.2%", GREEN, "Share in 2024 (Eurostat)",
            "Ahead of the plan’s 15.5% path. The rise is in heating and cooling; the electricity share moved from 9.5% to 10.7%."),
           ("16 vs 11.5", ORANGE, "MWp of solar PV a year",
            "Needed to reach 350 MWp by 2030, against the net addition in 2024. The plan gives no sum in points of share."),
           ("28%", BLUE, "The Commission’s formula",
            "It finds 24.5% below the 28% its formula gives, and the 2025 and 2027 points below its reference points.")],
    fair="On the plan’s own path Malta is ahead (pledge label: on track). The plan itself discloses that offshore wind "
         "is left out of the 2030 sum. Cyprus, another island, reached 20.8% in 2024.",
    asks=["A breakdown of the 24.5% by technology and sector.",
          "When offshore wind is expected to be commissioned.",
          "The planned pace of solar PV additions to 2030.",
          "The 2019 plan’s wording on the 11.5% figure."],
    footer="Version 1.0  ·  5 October 2026  ·  Public data only  ·  Draft pending right of reply from the "
           "Energy and Water Agency and the responsible Ministry",
    pdf_title="Claim Check 024 – Renewables by 2030: solar PV and offshore wind?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
