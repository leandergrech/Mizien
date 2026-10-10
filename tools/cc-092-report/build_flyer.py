"""Claim Check 092 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, reply_status, AMBER, GREEN, ORANGE, RED  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="092", out=str(OUT / "flyer.pdf"), kicker="Election pledges 2026, computed",
    title_lines=["Could trees make", "Gozo net zero?"],
    subtitle="The afforestation in the Nationalist Party’s 2026 pledge, tested on measured forests and Gozo’s land",
    quote_lines=["“… every unit of emissions generated is", "reduced or offset”, afforestation included."],
    attribution="Partit Nazzjonalista, programme Nifs Ġdid (May 2026), Għawdex item 46 (our translation)",
    context="Goal: Gozo a Net-Zero Island by 2040. The plan itself is Claim Check 107.",
    note="News said “through afforestation” and reported an indigenous-tree strategy; neither is in the programme.",
    verdict="Not measurable", verdict_right=["No area, species,", "rate or date."],
    cards=[("4.9–6.3×", RED, "Gozo’s area as new forest",
            "Needed to offset its energy CO₂ (118–154 kt a year) by trees alone, at a measured dry-forest rate."),
           ("3–4%", ORANGE, "If all semi-natural land",
            "All 1,270 ha of semi-natural land (garrigue, maquis) would offset 3–4% of that CO₂ (1–8% across rates)."),
           ("0 ha", ORANGE, "Forest mapped on Gozo",
            "None at CORINE’s 25 ha scale. Malta’s whole forest is 470 ha (FAO definition, 2025)."),
           ("30%", AMBER, "Water already used",
            "Malta’s water exploitation index in 2023 (above 20% signals scarcity). In an arid trial, 42–70% of pines died within 20 years."),
           ("Not found", AMBER, "Indigenous-tree strategy",
            "“Indigenous” appears once in 16 chapters: for farm crop varieties and livestock breeds.")],
    fair="The PN’s environment chapter presents trees as a defence against heat, flooding and pollution, which this "
         "check does not assess. Afforestation can be a small part of a plan that cuts emissions; it cannot carry it.",
    asks=["What share of Gozo’s emissions trees should offset.",
          "The area, sites and species to be planted.",
          "Where the indigenous-tree strategy is set out.",
          "How plantations would be watered, sparing garrigue."],
    footer="Version 1.0  ·  10 October 2026  ·  Label as of 10 Oct 2026  ·  Draft " +
           reply_status("Not measurable") + " (Partit Nazzjonalista)",
    pdf_title="Claim Check 092 – Could trees make Gozo net zero?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
