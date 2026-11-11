"""Claim Check 156 flyer. Output: out/flyer.pdf and out/flyer.png."""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, BLUE, RED  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="156", out=str(OUT / "flyer.pdf"), kicker="Bathing water, Malta",
    title_lines=["‘Best in Europe’", "to ‘bang average’?"],
    subtitle="An outlet’s headline claim, tested against EEA data",
    quote_lines=["“Maltese waters have suffered a downgrade", "from best in Europe to bang average.”"],
    attribution="Business Now, 17 Aug 2026",
    context="Malta’s counts are the EEA’s; its rank fell from third to eleventh of 22 EU coastal states.",
    note="‘Best’ is a loose word for third place; the fall is in the share rated excellent, not in safety.",
    verdict="Largely supported", verdict_right=["Right on the change;", "‘best’ was third."],
    cards=[("86 → 77", RED, "Sites rated excellent, 2016 → 2025", "Of 87 Maltese bathing waters: 98.9% down to 88.5% (EEA)."),
           ("3rd → 11th", ORANGE, "Rank among 22 EU coastal states", "Behind Slovenia (16 sites) and Cyprus in 2016; ten states ahead in 2025."),
           ("88.5%", BLUE, "Malta in 2025", "Against 88.3% pooled across EU coastal waters: ‘average’ fits."),
           ("0 poor", GREEN, "Maltese sites rated poor", "None in 2016 or 2025; every site met the minimum standard."),
           ("Not tested", ORANGE, "Week-13 figure (56 of 87)", "From the article only; a weekly count is not a season class.")],
    fair="The change is real and the article’s counts are exact. ‘Downgrade’ concerns the top class, not unsafe water.",
    asks=["Say ‘third’ or ‘top three’ rather than ‘best’.", "Compare season classes with season classes.",
          "Publish the weekly Directorate files with a method note.", "Report the share and the minimum-standard pass rate together."],
    footer="Version 1.0  ·  11 November 2026  ·  Public data only  ·  No right of reply needed  ·  Draft for maintainer review",
    pdf_title="Claim Check 156 – Best in Europe to bang average?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
