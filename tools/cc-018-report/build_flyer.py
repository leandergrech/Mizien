"""Claim Check 018 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="018", out=str(OUT / "flyer.pdf"), kicker="Housing and planning, Malta",
    title_lines=["Did the IMF confirm", "the developers?"],
    subtitle="A developers’ claim, tested against the IMF report and Eurostat",
    quote_lines=["“The IMF’s assessment of the Maltese housing market", "confirms what the Malta Developers Association…”"],
    attribution="Malta Developers Association, release of 8 February 2026",
    context="“…for several years.” On the IMF’s 2025 Article IV report on Malta.",
    note="We read the IMF report and the MDA’s release in full.",
    verdict="Largely supported", verdict_right=["Sound on valuation;", "risks left out."],
    cards=[("−10.7%", GREEN, "Incomes grew faster than prices",
            "Eurostat price-to-income ratio, 2015–2024; now below its long-term average."),
           ("“Aligned”", GREEN, "IMF: ratios “stable”",
            "Prices “aligned with fundamentals”; weakening “currently low”."),
           ("72%", ORANGE, "Banks tied to property",
            "Share of private loans; the IMF calls it “a vulnerability”."),
           ("2000", RED, "Not the first EU economy",
            "Luxembourg was on the IMF’s two-year cycle in 2000–02. Malta is the only EU member on it now."),
           ("110", ORANGE, "Above the EU, not “far”",
            "GDP per head in purchasing power, EU = 100 (2025); 102 at market prices.")],
    fair="The statement is right about what the IMF said on valuation and stability. It leaves out the IMF’s "
         "warnings on banks and fast price growth, and the IMF did not assess affordability. The two-year IMF "
         "cycle the release cites is real.",
    asks=["The release as first published.",
          "The MDA-commissioned study.",
          "The basis for “first EU economy”.",
          "Affordability for renters."],
    footer="Version 1.2  ·  5 October 2026  ·  Public data only  ·  No right of reply needed",
    pdf_title="Claim Check 018 – Did the IMF confirm the developers?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
