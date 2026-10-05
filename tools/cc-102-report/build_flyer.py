"""Claim Check 102 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, GREY  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="102", out=str(OUT / "flyer.pdf"), kicker="Governance, computed",
    title_lines=["Ombudsman:", "58% ignored?"],
    subtitle="The Ombudsman’s 2025 figures for environment and planning, recomputed from the report’s tables",
    quote_lines=["“7 recommendations, or 58%,", "were not implemented.”"],
    attribution="Office of the Ombudsman, Annual Report 2025, Commissioner for Environment and Planning",
    context="Reported 2 July 2026: the highest rate of any commissioner; 22 reports escalated to Parliament.",
    note="",
    verdict="Largely supported", verdict_right=["Matches the tables;", "small count."],
    cards=[("7 of 12", GREEN, "Sustained cases, 2025", "Recommendation not implemented at closure (58%). Table 1.3."),
           ("42%", ORANGE, "Still open when written", "Five of 12; two more were implemented after referral to the House."),
           ("25–58%", ORANGE, "Same office, 2023–25", "46%, 25%, 58%. Eight to thirteen cases a year: it swings."),
           ("58 vs 53%", ORANGE, "“Highest”", "Education 53% of sustained cases; 67% if only cases with a recommendation count."),
           ("22", GREEN, "Reports to Parliament", "Up from 14 (2023) and 16 (2024). Matches Table 1.22.")],
    fair="Not implementing a finding can be a legitimate disagreement; the report records what was not done, not why. "
         "The Commissioner’s remit covers planning, building and transport licensing as well as the environment.",
    asks=["The list of the 12 sustained cases and their status.",
          "How the per-office counts in Tables 1.3 and 1.22 reconcile.",
          "The authorities’ reasons for the five open cases.",
          "Case-level data for the Environment and Planning cases."],
    footer="Version 1.0  ·  5 October 2026  ·  Official data, our analysis  ·  Supported check, no right of reply needed",
    pdf_title="Claim Check 102 – Ombudsman: 58% ignored?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
