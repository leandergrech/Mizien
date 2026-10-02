"""Claim Check 005 flyer. Output: out/flyer.pdf and out/flyer.png."""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, BLUE  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="005", out=str(OUT / "flyer.pdf"), kicker="Bathing water, Malta",
    title_lines=["92% excellent", "bathing water"],
    subtitle="A public claim, tested against EEA season data",
    quote_lines=["“92% of Maltese bathing waters are", "of excellent quality.”"],
    attribution="European Commission, EIR 2025: Malta",
    context="The 92% result matches 80 of 87 sites in the 2023 season.",
    note="It is accurate for 2023; the report does not state the reference year beside the figure.",
    verdict="Supported", verdict_right=["Right for 2023;", "date the figure."],
    cards=[("80 / 87", GREEN, "Excellent in 2023",
            "The EEA result rounds to 92%, matching the Commission’s statement."),
           ("80 / 87", GREEN, "Excellent in 2024",
            "The share remained 92%; 2,107 samples were reported."),
           ("77 / 87", ORANGE, "Excellent in 2025",
            "The latest season was 88.5%, lower than the quoted 92%."),
           ("2 tests", BLUE, "What ‘excellent’ measures",
            "E. coli and intestinal enterococci under the Bathing Water Directive."),
           ("B08 / B09", ORANGE, "Balluta Bay, 2024",
            "A temporary warning affected two sites; it does not change the 2023 national classification.")],
    fair="The 92% statistic is accurate for the 2023 season. Short-term pollution warnings and wastewater treatment "
         "failures deserve attention, but they measure different things.",
    asks=["State the season year beside the 92% figure.",
          "Use the latest EEA result when describing current conditions.",
          "Explain that classification uses two microbiological indicators.",
          "Keep local warnings distinct from national multi-year results."],
    footer="Version 1.0  ·  2 October 2026  ·  Public data only  ·  Draft for maintainer review",
    pdf_title="Claim Check 005 – 92% excellent bathing water"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
