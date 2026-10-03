"""Claim Check 012 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="012", out=str(OUT / "flyer.pdf"), kicker="Parks and open space, Malta",
    title_lines=["Will the grass come", "back at Ta’ Qali?"],
    subtitle="Government and opposition claims, tested with satellite images",
    quote_lines=["“The natural grass grows at a much faster rate", "well before the rainfall of the winter season.”"],
    attribution="Public Works Ministry statement, September 2025, as reported by MaltaToday",
    context="PM, Jan 2026: “after the concerts are done, the intervention will happen.”",
    note="PN and Momentum: the gravel is choking the grass and could leave the area barren.",
    verdict="Contradicted", verdict_right=["The grass did not return;", "the gravel is still there."],
    cards=[("0.37–0.47", GREEN, "Green every winter before",
            "Winter greenness (NDVI) of the picnic area 2023–2025, level with the rest of the park."),
           ("0.11", RED, "Bare in winter 2025–26",
            "After the gravel, the area stayed brown while the rest of the park greened."),
           ("Summer", ORANGE, "The dust problem was real",
            "The area was already bare every summer before the gravel, as the park management said."),
           ("27 Sep", RED, "No intervention visible",
            "Last clear image of 2026: gravel still in place, after the summer concerts."),
           ("2.8 ha", GREEN, "Same area as the critics measured",
            "Found in the images; Momentum’s inspection reported about 2.2 ha.")],
    fair="Whether the damage is permanent cannot be seen from space: it depends on whether the gravel is removed. "
         "Intent and procurement are not assessed.",
    asks=["The consultant’s report and dates.",
          "The specification of the material.",
          "Momentum’s inspection report in full.",
          "The 2026 events calendar."],
    footer="Version 1.0  ·  3 October 2026  ·  Contains modified Copernicus Sentinel data  ·  Draft pending right of reply",
    pdf_title="Claim Check 012 – Will the grass come back at Ta' Qali?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
