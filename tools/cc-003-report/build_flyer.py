"""Claim Check 003 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="003", out=str(OUT / "flyer.pdf"), kicker="Climate and emissions, Malta",
    title_lines=["Emissions per person down 44%,", "or off track for 2030?"],
    subtitle="A public claim, tested against EU and Eurostat data",
    quote_lines=["“Emissions per capita have fallen by 44% since", "2005, well above the EU average of 34%.”"],
    attribution="Climate Action Authority, press release, 13 November 2025",
    context="Citing the European Commission’s Climate Action Progress Report 2025.",
    note="The same EU report projects Malta will miss its 2030 target by the widest margin in the EU in percentage points.",
    verdict="Misleading", verdict_right=["Accurate numbers,", "incomplete picture."],
    cards=[("−44%", GREEN, "The figure is right",
            "Eurostat data reproduce the per-person fall (EU: −34%). Power-sector emissions fell 63%."),
           ("3rd / 20th", ORANGE, "Per person vs in total",
            "Malta’s cut ranks 3rd of 27 per person, 20th in total: population grew 41%. In tonnes, −27% vs EU −33%."),
           ("+30 pts", RED, "Over the yearly limit, 2024",
            "Target-sector emissions +41% vs a limit of +11%; over every year since 2022. A 2021 surplus has covered it so far."),
           ("49 pts", RED, "Projected 2030 gap",
            "Even with planned measures the Commission projects +30% against −19%: the EU’s largest gap in percentage points."),
           ("+49%", RED, "Transport since 2005",
            "Buildings and air-conditioning gases rose too, in total. Per person, the target sectors are flat, not falling.")],
    fair="Cutting power-sector emissions by almost two-thirds was real. Per person, target-sector emissions are "
         "flat (2.50 t to 2.52 t, our estimate), and no compliance shortfall has arisen yet.",
    asks=["The source and scope of the 44% and 34% figures.",
          "What “40% by 2030” covers: total or target sectors?",
          "A dated plan taking target-sector emissions from +41% to −19%.",
          "How much Malta expects to rely on buying allocations."],
    footer="Version 1.2  ·  5 October 2026  ·  Public data only  ·  Draft pending right of reply from the "
           "Climate Action Authority and the Environment Ministry",
    pdf_title="Claim Check 003 – Emissions down 44% per person, or off track for 2030?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
