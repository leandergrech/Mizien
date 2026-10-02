"""Claim Check 002 flyer. Run build_report.py first."""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, AMBER  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="002", out=str(OUT / "flyer.pdf"), kicker="Land and trees, Malta",
    title_lines=["What do the tree", "numbers prove?"],
    subtitle="Comino's removal, transplant and replacement plan, checked against the evidence",
    quote_lines=["“54 protected trees will be removed”", "“540 new indigenous trees”"],
    attribution="Environment and Resources Authority, 11 August 2026",
    context="Comino · planned removals, planting and transplantation",
    note="These are announced conditions, not measured outcomes.",
    verdict="Largely supported", verdict_right=["Math checks out;", "outcome unmeasured."],
    cards=[
        ("678", ORANGE, "specimens for removal", "ERA's categories: 624 non-protected plus 54 protected."),
        ("92.04%", GREEN, "non-protected share", "624 of 678; rounds to the stated 92%."),
        ("540", GREEN, "new indigenous trees", "Ten for each of the 54 protected trees scheduled for removal."),
        ("348", AMBER, "trees to transplant", "Separate from removal; ERA says 341 are protected. Failures trigger a further 10:1 condition."),
        ("Not shown", RED, "ecological offset", "No public survival or habitat-recovery results for these Comino trees were available at review."),
    ],
    fair="ERA's counts and ratios reconcile. The developer reports nursery propagation since 2023, but publishes no stock or survival data. Ecological replacement remains unmeasured.",
    asks=["Publish the complete species and condition schedule.",
          "Publish the final species, provenance and aftercare plan.",
          "Report transplant and planting survival at years 1, 3 and 5.",
          "Monitor native biodiversity and habitat function, not counts alone."],
    footer="Version 1.1  ·  3 October 2026  ·  Draft pending right of reply",
    pdf_title="Claim Check 002 – What do the tree numbers prove?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
