"""Claim Check 148 flyer. Output: out/flyer.pdf and out/flyer.png"""
import json, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED  # noqa: E402
R = json.load(open(HERE.parents[1] / "data" / "cc-148" / "results.json"))
OUT = HERE / "out"
build_flyer(Flyer(
    number="148", out=str(OUT / "flyer.pdf"), kicker="Climate and energy, Malta",
    title_lines=["Did Malta cut", "emissions most?"],
    subtitle="A Eurostat statement, tested against Eurostat’s revised data",
    quote_lines=["“The largest reductions in greenhouse gases", "were estimated for Malta (-6.2%).”"],
    attribution="Eurostat, news item, 14 August 2025",
    context="Q1 2025 compared with Q1 2024; EU +3.4%.",
    note="MaltaDaily’s headline (“tops EU”) is not rated.",
    verdict="Largely supported", verdict_right=["Accurate at release;", "later revised."],
    cards=[("−6.2%", GREEN, "What Eurostat estimated", "Malta’s Q1 2025 fall, the largest of 27 in the 14 August 2025 release."),
           ("−5.0%", ORANGE, "What the data say now", "Revised: Malta is 2nd, behind Finland (−10.1%)."),
           (f"{R['mt_annual_yoy']['2025']:+.1f}%", RED, "The full year", "Malta’s 2025 emissions on 2024 (sum of four quarters); the EU’s: +1.0%."),
           (f"{R['q1_2026_mt']:+.1f}%", RED, "The latest quarter", "Q1 2026 on Q1 2025."),
           ("20 / 7", GREEN, "Countries up / down", "Eurostat’s split holds in the revised data.")],
    fair="Eurostat made no claim about a trend. Figures are estimates that include international aviation and shipping. "
         "We could not retrieve the August 2025 vintage of the dataset.",
    asks=["Eurostat’s earlier dataset vintages.", "Why Malta’s series steps up between 2023 and 2024."],
    footer="Version 1.0  ·  2 November 2026  ·  Public data only  ·  No right of reply needed",
    pdf_title="Claim Check 148 – Did Malta cut emissions most in Q1 2025?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
