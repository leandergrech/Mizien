"""Build the CC-007 one-page summary in the shared Miżien flyer style."""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="007", out=str(OUT / "flyer.pdf"), kicker="Air quality, Malta",
    title_lines=["Within limits,", "above the guideline"],
    subtitle="Five years of annual PM2.5 readings, checked against EU and WHO standards",
    quote_lines=["“…well within the considerably less stringent", "annual limits set by the EU for PM2.5.”"],
    attribution="Newsbook, 18 July 2025",
    context="The underlying figures were tabled in Parliamentary Question 29696.",
    note="The Minister’s answer tables data; it does not itself state that they comply.",
    verdict="Largely supported", verdict_right=["23 below 25", "10 EEA match"],
    cards=[
        ("23 / 23", GREEN, "Above WHO’s guideline", "All reported annual means exceed the 5 µg/m³ health-based guideline."),
        ("23 / 23", GREEN, "Within the historical EU limit", "Every available value is below the 25 µg/m³ legal limit for 2020–2024."),
        ("2 missing", ORANGE, "St Paul’s Bay", "The annex lists n/a for 2020 and 2021, so full five-station coverage is not shown."),
        ("14 / 23", ORANGE, "Above the 2030 EU standard", "Fourteen values exceed 10 µg/m³, the standard due by 2030—not a limit for these past years."),
        ("10 / 11", GREEN, "EEA values match", "One cross-check differs: Attard 2024, 12.122 vs 11.9 in the annex."),
    ],
    fair="The annex’s 23 values all meet the historical EU limit and exceed WHO guidance. The partial EEA check broadly agrees but differs for Attard in 2024; the two St Paul’s Bay n/a values remain unresolved.",
    asks=["ERA’s validated annual series and data-completeness notes.",
          "An explanation of the Attard 2024 difference.",
          "The missing St Paul’s Bay values for 2020 and 2021, if available.",
          "Keep the 2030 EU standard distinct from past compliance."],
    footer="Version 1.2 · 4 October 2026 · Draft for maintainer review · Reply process to be handled by maintainer",
    pdf_title="Claim Check 007 – Within limits, above the guideline"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
