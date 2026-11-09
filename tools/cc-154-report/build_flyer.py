"""Claim Check 154 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, GREY, BLUE  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="154", out=str(OUT / "flyer.pdf"), kicker="Nature and wildlife",
    title_lines=["Finch trapping:", "what did Brussels write?"],
    subtitle="A news report of the Commission’s October 2025 letter, tested against the letter",
    quote_lines=["“That request still stands.”"],
    attribution="European Commission, DG Environment, letter to BirdLife Malta, October 2025",
    context="Speaker’s own words, English text of the letter.",
    note="We read the letter itself, a copy published by BirdLife Malta, and compared it with Italpress’s report.",
    verdict="Largely supported", verdict_right=["Accurate on the notice and referral;", "“in breach” is the outlet’s wording."],
    cards=[("Still stands", GREEN, "Formal notice, Feb 2025",
            "The Commission’s own words on its request that Malta implement the Court’s ruling."),
           ("May refer", GREEN, "Possible next step",
            "The letter names referral to the Court of Justice as a possible enforcement step."),
           ("0", GREY, "“In breach” in the letter",
            "The phrase is Italpress’s. The letter says the new derogation “seems similar” to the 2024 one and is being assessed."),
           ("393 days", BLUE, "Judgment to new derogation",
            "From the Court’s ruling of 19 Sep 2024 to the rules adopted on 17 Oct 2025."),
           ("Not read", GREY, "The 2025 rules and the new notice",
            "BirdLife Malta reports a new formal notice on 21 Nov 2025; we have not read it.")],
    fair="We rate the statements reported, not hunters, NGOs or officials.",
    asks=["The Commission’s notice INFR(2025)2128.", "The 17 Oct 2025 rules and the Government’s reasoning.", "The Commission’s own copy of the letter."],
    footer="Version 1.0  ·  9 November 2026  ·  Public sources only  ·  No right of reply needed",
    pdf_title="Claim Check 154 – Finch trapping: what did Brussels write?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
