"""Claim Check 150 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, GREY, AMBER  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="150", out=str(OUT / "flyer.pdf"), kicker="Waste, Malta",
    title_lines=["412 million kg", "diverted?"],
    subtitle="The Minister’s landfill-diversion figure, set against the NSO’s municipal waste tables",
    quote_lines=["“…we have diverted roughly 412 million", "kilogrammes of waste away from landfill…”"],
    attribution="Miriam Dalli, Minister for the Environment, 19 January 2026",
    context="“…over the past five years through increased organic and packaging waste separation.”",
    note="We computed four readings of “diverted” from NSO data for 2020–2024.",
    verdict="Not substantiated", verdict_right=["Matches what was collected,", "not what was kept out of landfill."],
    cards=[("424", AMBER, "Thousand t collected separately", "Paper, metals, glass, packaging, organic; 2020–2024."),
           ("270", GREEN, "Thousand t recycled or recovered", "Same five years (NSO treatment table)."),
           ("+6%", GREY, "Growth in separate collection", "About 90 thousand t in 2019; 95 thousand in 2024."),
           ("255", RED, "Thousand t landfilled in 2024", "Down from a 2019 peak of 321 thousand t.")],
    fair="Recycling has risen and landfill has fallen since 2019. The mixed-waste and organic figures fit the NSO data.",
    asks=["Ministry and WasteServ: how 412 million kg was calculated.",
          "WasteServ: separately collected waste later landfilled."],
    footer="Version 1.0  ·  17 November 2026  ·  Draft, pending right of reply",
    pdf_title="Claim Check 150 – 412 million kg diverted?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
