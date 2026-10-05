"""Claim Check 005 flyer. Output: out/flyer.pdf and out/flyer.png."""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, BLUE, RED  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="005", out=str(OUT / "flyer.pdf"), kicker="Bathing water, Malta",
    title_lines=["92% excellent", "bathing water"],
    subtitle="A public claim, tested against eleven seasons of EEA data",
    quote_lines=["“92% of Maltese bathing waters are", "of excellent quality.”"],
    attribution="European Commission, EIR 2025: Malta",
    context="The 92% matches 80 of 87 sites in 2023, the season the Commission’s full report names.",
    note="The 2024 season gave the same count. The summary sentence does not state the year.",
    verdict="Supported", verdict_right=["Right for 2023–24;", "date the figure."],
    cards=[("80 / 87", GREEN, "Excellent in 2023 and 2024",
            "92.0% both seasons, matching the Commission’s statement when it was published."),
           ("77 / 87", ORANGE, "Excellent in 2025",
            "88.5%: the lowest of the eleven seasons since 2015 (98.9% in 2016–2018)."),
           ("88.3%", BLUE, "EU-27 coastal average, 2025",
            "Malta’s lead over it shrank from 11 points in 2016 to 0.2 in 2025."),
           ("4 seasons", RED, "Balluta Bay B08 and B09",
            "Rated only sufficient every season 2022–2025; a 2024 warning fell within that run."),
           ("10 of 87", ORANGE, "Sites ever below excellent",
            "In 2025 St George’s Bay B03 and Xlendi D06/D07 fell to good; two other sites improved.")],
    fair="The 92% was accurate and current when published. Since then the share has fallen to 88.5%; "
         "classification uses two microbiological indicators and four seasons of samples.",
    asks=["State the season year beside the 92% figure.",
          "Use the latest EEA result (2025: 88.5%) for current conditions.",
          "Explain why Balluta Bay has stayed at the minimum class.",
          "Report the decline since 2018 alongside the headline share."],
    footer="Version 1.2  ·  5 October 2026  ·  Public data only  ·  No right of reply needed  ·  Draft for maintainer review",
    pdf_title="Claim Check 005 – 92% excellent bathing water"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
