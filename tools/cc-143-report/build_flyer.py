"""Claim Check 143 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, GREY, ORANGE, RED  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="143", out=str(OUT / "flyer.pdf"), kicker="Water, Malta",
    title_lines=["EU: Malta’s groundwater status", "worse in the third water plan"],
    subtitle="The Commission’s 2026 plan comparison, tested against its 2019 text and EEA data",
    quote_lines=["“…no GWBs had a good chemical status in 2021, while",
                 "a fifth of GWBs had a good chemical status in 2015.”"],
    attribution="European Commission, SWD(2026) 702 final, Malta, 2 October 2026",
    context="Also: good quantitative status “decreased from 86.7% to 73.3% due to overabstraction”.",
    note="GWB = groundwater body; Malta has 15.",
    verdict="Largely supported", verdict_right=["Counts correct;", "cause not tested"],
    cards=[("13 → 11", GREEN, "Quantity: two bodies fell",
            "86.7% and 73.3% are 13 and 11 of 15 bodies. The 2019 Commission text and the EEA’s database agree."),
           ("3 → 0", GREEN, "Chemistry: none left",
            "A fifth is 3 of 15 in the second plan; all 15 bodies are in poor chemical status in 2021."),
           ("4 · 2 · 4", ORANGE, "Back to the first plan",
            "Poor quantitative status: four bodies in the first plan, two in the second, four in the third."),
           ("−10%", GREY, "Abstraction did not rise",
            "Eurostat’s estimate of groundwater abstraction fell from 41.6 to 37.3 million m³ (2015–2021). Estimated."),
           ("Cause?", GREY, "“Overabstraction”: not tested",
            "Monitoring grew from 3 to 7 bodies, and the document says comparability between cycles “might be low”.")],
    fair="The Commission notes that quantitative monitoring rose from 3 to 7 bodies, that 8 of 15 are still not "
         "monitored, and that recharge has fallen with rainfall. It calls the monitored area’s status “a systemic "
         "problem of overabstraction”.",
    asks=["Status of each of the 15 bodies in the second and third plans, with the method.",
          "Metered groundwater abstraction by body, 2013–2023.",
          "The basis of “due to overabstraction” in the Commission’s text.",
          "Whether the larger monitoring network explains part of the change."],
    footer="Version 1.0  ·  27 October 2026  ·  Public documents and data only  ·  No right of reply needed",
    pdf_title="Claim Check 143 – EU: Malta’s groundwater status worse in the third water plan"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
