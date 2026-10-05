"""Claim Check 115 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, GREY, AMBER  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="115", out=str(OUT / "flyer.pdf"), kicker="Transport and the economy, Malta",
    title_lines=["Congestion cost €770m,", "3.4% of GDP?"],
    subtitle="The Malta Chamber's figure, traced to the government's transport plan",
    quote_lines=["“…traffic congestion imposed an estimated cost of €770", "million on the Maltese economy, equivalent to 3.4% of GDP.”"],
    attribution="The Malta Chamber of Commerce, Enterprise and Industry, LEAD proposals, 14 May 2026",
    context="Footnote: Transport Master Plan 2030, page 124.",
    note="The government's plan gives the figure but no calculation for 2025.",
    verdict="Not substantiated", verdict_right=["Cited correctly, but no method;", "3.4% is 3.1% of 2025 GDP."],
    cards=[("€770m", AMBER, "The government's figure",
            "National Transport Master Plan 2030: “up from €770 million in 2025”. No derivation is published."),
           ("3.1%", GREEN, "Share of 2025 GDP",
            "€770m against €24.7bn GDP at current prices. 3.4% would need GDP of €22.6bn."),
           ("€917m", GREY, "The plan's 2030 projection",
            "If nothing changes. Environmental costs (€195m a year) come on top of both figures."),
           ("€248m", GREY, "Lost time, 2030, in the annex",
            "The only costing we found models 2030 and 2060, not 2025, and does not show how €917m is built up."),
           ("€1.13bn", ORANGE, "Another estimate",
            "Engineer Marco Cremona (reported 3 June 2026) put it higher; we have not read his method first-hand.")],
    fair="The Chamber reported the government's own figure accurately and gave the page. A large cost is plausible; "
         "it is not yet testable.",
    asks=["Ministry for Transport: the method for €770m.", "Ministry: hours lost and values of time used.",
          "Malta Chamber: the GDP figure behind 3.4%.", "Publication of the plan's traffic model report."],
    footer="Version 1.0  ·  5 October 2026  ·  Draft, pending right of reply",
    pdf_title="Claim Check 115 – Congestion cost €770m, 3.4% of GDP?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
