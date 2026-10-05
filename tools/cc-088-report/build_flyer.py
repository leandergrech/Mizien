"""Claim Check 088 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, GREY, AMBER  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="088", out=str(OUT / "flyer.pdf"), kicker="Population, Malta",
    title_lines=["Population", "588,254?"],
    subtitle="The NSO's World Population Day release, tested against Eurostat",
    quote_lines=["“The estimated total population of Malta and Gozo", "stood at 588,254 at the end of 2025.”"],
    attribution="National Statistics Office, News Release NR 120/2026, 9 July 2026",
    context="Up 2.4% on the previous year; net migration of 13,906 the main contributor.",
    note="We recomputed every figure in the claim from Eurostat's demographic accounts.",
    verdict="Supported", verdict_right=["Every figure reproduces", "from the Eurostat data."],
    cards=[("588,254", GREEN, "Residents, end 2025",
            "Eurostat's 1 January 2026 population matches the NSO's figure exactly."),
           ("+2.4%", GREEN, "Growth over 2025",
            "588,254 against 574,250 is +2.44%."),
           ("13,906", GREEN, "Net migration, 2025",
            "Up 31.0% on 2024 (10,614). Matches Eurostat."),
           ("99.3%", GREEN, "Growth from migration",
            "Births minus deaths added only 98 people (193 in 2024)."),
           ("98 + 13,906", GREY, "= the 14,004 increase",
            "The components add up to the change in the population, with nothing left over.")],
    fair="Eurostat's data for Malta come from the NSO, so this confirms consistency, not an independent count.",
    asks=["NSO: the revision policy for end-year estimates.", "NSO: the method for counting net migration.",
          "Readers: cite the NSO release, not a headline.", "Anyone quoting a national density: give the area used."],
    footer="Version 1.0  ·  5 October 2026  ·  Public data only  ·  No right of reply needed",
    pdf_title="Claim Check 088 – Population 588,254?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
