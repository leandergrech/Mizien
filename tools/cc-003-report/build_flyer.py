"""Claim Check 003 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="003", out=str(OUT / "flyer.pdf"), kicker="Climate and emissions, Malta",
    title_lines=["Emissions down 44%,", "or off track for 2030?"],
    subtitle="A public claim, tested against EU and Eurostat data",
    quote_lines=["“Emissions per capita have fallen by 44% since", "2005, well above the EU average of 34%.”"],
    attribution="Climate Action Authority, press release, 13 November 2025",
    context="Citing the European Commission’s Climate Action Progress Report 2025.",
    note="The same EU report projects Malta will miss its 2030 target by the widest margin in the EU.",
    verdict="Misleading", verdict_right=["Accurate numbers,", "incomplete picture."],
    cards=[("−44%", GREEN, "The figure is right",
            "Eurostat data reproduce the per-person fall (EU: −34%). Power-sector emissions fell 63%."),
           ("+41%", ORANGE, "Population growth",
            "About half the per-person fall is more people, not fewer emissions. In total tonnes Malta cut 27%, the EU 33%."),
           ("+49%", RED, "Transport since 2005",
            "Buildings and air-conditioning gases rose too: the sectors closest to households went up, not down."),
           ("+41%", RED, "Against a −19% target",
            "Emissions under Malta’s binding 2030 target were 41% above 2005 in 2024."),
           ("49 pts", RED, "Projected 2030 gap",
            "Even with planned measures the Commission projects +30%: the largest gap in the EU.")],
    fair="Cutting power-sector emissions by almost two-thirds was a real achievement, and per-person figures are a "
         "standard indicator. This check is about what the press release leaves out.",
    asks=["The source and scope of the 44% and 34% figures.",
          "What “40% by 2030” covers: total or target sectors?",
          "A dated plan taking target-sector emissions from +41% to −19%.",
          "How much Malta expects to rely on buying allocations."],
    footer="Version 1.0  ·  2 October 2026  ·  Public data only  ·  Draft pending right of reply from the "
           "Climate Action Authority and the Environment Ministry",
    pdf_title="Claim Check 003 – Emissions down 44% per person, or off track for 2030?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
