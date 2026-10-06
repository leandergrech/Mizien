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
    verdict="Largely supported", verdict_right=["The buses are electric;", "the quoted “vision” has no date."],
    cards=[("100%", GREEN, "Gozo’s buses are electric",
            "Public transport in Gozo has been fully electric since late May 2026 (22 new buses, EUR 11 million), per TVM News."),
           ("22", GREEN, "New electric buses in Gozo",
            "TVM News, May and July 2026: all Gozo bus services now electric, with a new charging depot."),
           ("≈3%", ORANGE, "Of Gozo road emissions",
            "Our rough scale check: about 2.6% of a population-proportional estimate. Buses are a small part of the total."),
           ("n/a", GREY, "Target year in the quoted words",
            "Not in the quoted words; plan not read. Pledge label: Not measurable (as of 6 Oct 2026), on those words only."),
           ("+39%", RED, "Malta’s road-transport emissions",
            "2005 to 2024 (Eurostat, national figure). The bus change covers only the bus fleet.")],
    fair="The electric fleet is real and an early, concrete step. A vision statement is not a false statement; the "
         "question is whether the plan can be checked once its target is published.",
    asks=["The published plan: target year, baseline, boundary.", "Gozo’s own emissions inventory.",
          "Transport Malta’s fleet record.", "Whether ferries are in the boundary."],
    footer="Version 1.1  ·  6 October 2026  ·  Public data only  ·  Right of reply on hold until the Gozo plan is read",
    pdf_title="Claim Check 031 – Gozo: the first climate-neutral region?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
