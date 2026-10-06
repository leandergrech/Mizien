"""Claim Check 031 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, GREY  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="031", out=str(OUT / "flyer.pdf"), kicker="Climate and energy, Gozo",
    title_lines=["Gozo: the first", "climate-neutral region?"],
    subtitle="A minister’s “vision” and the electric buses, tested against public data",
    quote_lines=["“…an important step to continue to realise our vision of", "Gozo becoming the first climate-neutral region in Malta.”"],
    attribution="Clint Camilleri, Minister for Gozo, 25 September 2026",
    context="Reported with a paraphrase: Gozo has begun its transition, including a fully electric public transport fleet.",
    note="We could not obtain the plan itself, so we do not know whether it sets a target year.",
    verdict="Largely supported", verdict_right=["The buses are electric;", "the “vision” has no date."],
    cards=[("100%", GREEN, "Gozo’s buses are electric",
            "Public transport in Gozo has been fully electric since late May 2026 (22 new buses, EUR 11 million), per TVM News."),
           ("1,300 t", GREEN, "CO2 saved a year (claimed)",
            "Malta Public Transport’s own figure, not independently checked."),
           ("≈3%", ORANGE, "Of Gozo road emissions",
            "Our rough scale check: about 2.6% of a population-proportional estimate. Buses are a small part of the total."),
           ("0", GREY, "Target years found",
            "The quoted words give no date, baseline or boundary. Pledge label: Not measurable (as of 6 Oct 2026)."),
           ("+39%", RED, "Malta’s road-transport emissions",
            "2005 to 2024 (Eurostat). Ferries, cars and power supply are not covered by the bus change.")],
    fair="The electric fleet is real and an early, concrete step. A vision statement is not a false statement; the "
         "question is whether the plan can be checked once its target is published.",
    asks=["The published plan: target year, baseline, boundary.", "Gozo’s own emissions inventory.",
          "Transport Malta’s fleet record.", "Whether ferries are in the boundary."],
    footer="Version 1.0  ·  6 October 2026  ·  Public data only  ·  Draft pending right of reply (pledge label)",
    pdf_title="Claim Check 031 – Gozo: the first climate-neutral region?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
