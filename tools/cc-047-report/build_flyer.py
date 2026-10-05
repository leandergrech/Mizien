"""Claim Check 047 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, GREY, AMBER  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="047", out=str(OUT / "flyer.pdf"), kicker="Water, Malta",
    title_lines=["Nitrates: 2–4 times", "the EU limit?"],
    subtitle="A reported figure for the eastern main aquifer, tested against monitoring data",
    quote_lines=["“…the highest concentrations of nitrate are observed in the", "eastern areas of the MSLA, ranging from 100 to 200 mg/L.”"],
    attribution="Laudi et al., 2026, quoted by MaltaToday, 13 February 2026",
    context="MaltaToday adds: “two to four times higher than the EU safety limit of 50 mg/L”.",
    note="We could not read the paper's full text; the quotation is second-hand.",
    verdict="Largely supported", verdict_right=["The figures match; the", "eastern range is second-hand."],
    cards=[("2–4×", GREEN, "The arithmetic",
            "100 and 200 mg/L are two and four times the 50 mg/L limit."),
           ("68.2%", RED, "Monitoring points at 50+",
            "30 of 44 groundwater points averaged 50 mg/L or more, 2020–2023 (Commission review)."),
           ("63.6%", GREY, "Same share, 2016–2019",
            "The share above the limit has risen."),
           ("75–200", AMBER, "mg/L, same team, 2025",
            "Groundwater under potato and forage fields; the north-west regional aquifer was 25–100."),
           ("?", GREY, "Tap water",
            "Not tested: public supply is blended and treated.")],
    fair="Most monitoring points exceed 50 mg/L, so the headline picture holds. The exact eastern range needs the paper or EWA station data.",
    asks=["EWA: station data for the eastern aquifer.", "Journal authors: the page for the quoted sentence.",
          "Readers: the study did not assess livestock.", "Readers: shallow wells are worst (83% over)."],
    footer="Version 1.0  ·  5 October 2026  ·  Public sources  ·  No right of reply needed",
    pdf_title="Claim Check 047 – Nitrates: 2–4 times the EU limit?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
