"""Build the CC-010 flyer in the shared Miżien design."""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, BLUE  # noqa: E402

OUT = ROOT / "claims" / "CC-010"
build_flyer(Flyer(
    number="010", out=str(OUT / "flyer.pdf"), kicker="Land & Trees, Malta",
    title_lines=["How many trees", "were planted?"],
    subtitle="Checking public planting counts against the 100,000-tree pledge",
    quote_lines=["“100,000 siġra fil-ħames snin li ġejjin”"],
    attribution="Partit Laburista, 2022 manifesto, pledge 305",
    context="2024 annual count · end-2025 parliamentary answer · snap election 30 May 2026",
    note="Planted trees, shrubs, survival and canopy are different measures.",
    verdict="Largely supported", verdict_right=["Counts confirmed;", "~60,000 of 100,000."],
    cards=[
        (">8,000", GREEN, "trees reported in 2024", "Project Green's release reports this separately from over 25,000 shrubs."),
        ("~60,000", ORANGE, "trees reported by end-2025", "Minister's approximate figure in Parliament; Labour's 2026 manifesto says more than 57,000."),
        ("60% / 75%", RED, "pledge delivery not shown", "Of the 100,000 trees by end-2025, with 75% of the five years gone; the legislature ended on 30 May 2026."),
        (">100,000", BLUE, "shrubs reported by end-2025", "Reported separately from trees; not part of the tree pledge."),
        ("Not counted", BLUE, "surviving trees or canopy", "The records do not provide survival follow-up or a national linked tree register."),
    ],
    fair="The records confirm the 2024 totals, the pledge and about 60,000 trees by end-2025. The 100,000 was not reached by then, and no later count was found before the legislature ended. Planting is not survival or canopy.",
    asks=["Publish a project-level tree register for 2022–2026.",
          "Clarify which agencies and projects are included in the 60,000 total.",
          "Report survival, replacement and maintenance for each planting cohort.",
          "Keep shrub totals and tree vouchers separate from planted trees."],
    footer="Version 1.2  ·  5 October 2026  ·  Right of reply not sought",
    pdf_title="Claim Check 010 – How many trees were planted?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
