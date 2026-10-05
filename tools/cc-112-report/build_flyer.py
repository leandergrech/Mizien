"""Claim Check 112 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, GREY, AMBER  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="112", out=str(OUT / "flyer.pdf"), kicker="Population, Malta",
    title_lines=["Population up 25%", "in a decade?"],
    subtitle="An IMF staff paper, tested against Eurostat's demographic accounts",
    quote_lines=["“Malta’s population rose by 25 percent over a decade,", "largely due to immigration.”"],
    attribution="IMF staff, Malta: Selected Issues (Country Report No. 26/30), February 2026",
    context="A parenthesis in a list of drivers of the housing boom.",
    note="The paper gives no years, so we tested every ten-year window to 2026.",
    verdict="Largely supported", verdict_right=["Migration-driven growth is right;", "25% is low for the latest decade."],
    cards=[("+30.9%", ORANGE, "Latest decade, 2015–2025",
            "438,805 to 574,250 people. The latest decade available when the paper was written."),
           ("+24.6%", GREEN, "Decades ending 2020–2022",
            "Growth was 24.4–24.6%: these are the decades that match the 25%."),
           ("96%", GREEN, "Share from net migration",
            "Net migration was 93–97% of growth in every decade since 2010–2020."),
           ("+1.9%", GREY, "EU-27, 2015–2025",
            "Malta grew about sixteen times faster than the EU over the same decade."),
           ("588,254", GREY, "Population, 1 Jan 2026",
            "Up from 402,668 in 2005. Matches the NSO's end-2025 figure (CC-088).")],
    fair="The figure errs low, so it does not exaggerate the point it supports: population growth has added to housing "
         "demand.",
    asks=["IMF staff: the years behind “a decade”.", "IMF staff: the data source used.",
          "Readers: say which decade you mean.", "NSO: census-consistent back series."],
    footer="Version 1.0  ·  5 October 2026  ·  Public data only  ·  No right of reply needed",
    pdf_title="Claim Check 112 – Population up 25% in a decade?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
