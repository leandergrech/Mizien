"""Claim Check 157 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="157", out=str(OUT / "flyer.pdf"), kicker="Climate and economy, Malta",
    title_lines=["Will heat cost", "Malta 2.5% of GDP?"],
    subtitle="A reported projection, tested against the study it cites",
    quote_lines=["“GDP impacts from extreme heat exceeding", "-2.5 per cent by the 2055-2064 period.”"],
    attribution="Business Now, 18 July 2025, reporting García-León et al. (Nature Communications, 2021)",
    context="If there is no further adaptation or mitigation.",
    note="A projection, read from the study’s Figure 4b; not a forecast.",
    verdict="Largely supported", verdict_right=["The study does show it;", "approximate and scenario-bound."],
    cards=[("−2.8%", ORANGE, "Malta’s projected loss", "About 2.8% of GDP a year in 2055–2064, read from the study’s figure (±0.1 points)."),
           ("4th", RED, "Of 29 entries plotted", "Only Cyprus, Croatia and Portugal are higher; the Europe-wide figure is about 1.1%."),
           ("RCP8.5", GREEN, "High-emissions scenario", "No extra adaptation such as air conditioning; the authors expect rising losses even with stringent mitigation."),
           ("2021", ORANGE, "The study is four years older", "Published 4 October 2021; reported as news in July 2025."),
           ("Not tabled", GREEN, "No Malta table or range", "Malta appears only in a chart; its uncertainty is not given.")],
    fair="This tests what the study projects, not whether the model is right about 2055–2064. The authors list "
         "five gaps, including heat-island effects.",
    asks=["The authors’ Malta value and range.",
          "Results under lower-emission scenarios.",
          "Any newer Malta estimate.",
          "A link from the article to the paper."],
    footer="Version 1.0  ·  10 November 2026  ·  Public data only  ·  No right of reply needed",
    pdf_title="Claim Check 157 – Will heat cost Malta 2.5% of GDP?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
