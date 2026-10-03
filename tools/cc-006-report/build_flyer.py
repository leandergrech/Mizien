"""Claim Check 006 flyer. Run build_report.py first."""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="006", out=str(OUT / "flyer.pdf"), kicker="Nature and wildlife, Malta",
    title_lines=["What does ‘small", "numbers’ mean?"],
    subtitle="The 2026 hunting quotas, checked against Malta’s own legal benchmark",
    quote_lines=["“Under strictly supervised conditions ... in small numbers”"],
    attribution="Directive 2009/147/EC, Article 9(1)(c)",
    context="Malta’s 2026 quotas: 2,400 Quail · 1,500 Turtle-doves",
    note="The benchmark is a statutory model, not a count of birds migrating over Malta.",
    verdict="Not substantiated", verdict_right=["The quota maths fits;", "implementation is open."],
    cards=[
        ("99.3%", ORANGE, "Quail quota / benchmark", "2,400 quota against the regulation’s 2,416-bird 1% benchmark."),
        ("59.8%", GREEN, "Turtle-dove quota / benchmark", "1,500 quota against the regulation’s 2,510-bird 1% benchmark."),
        ("Declining", RED, "Turtle-dove context", "WBRU reports a continuing central-eastern flyway decline; latest Article 12 data were provisional."),
        ("2025", ORANGE, "Latest outcome report", "WBRU records 1,336 patrols, 909 spot-checks and 19 detected offences for 2025."),
        ("Not yet", RED, "2026 supervision", "No 2026 season outcome report was listed in the WBRU archive at the 3 October review cut-off."),
    ],
    fair="Both quotas are below the legal mortality benchmark. That confirms the formula was followed on the Government’s inputs; it does not prove sustainability or strict supervision in practice.",
    asks=["Publish the 2026 outcome and enforcement data.",
          "Show the final population inputs and mortality method.",
          "Publish the Ornis minutes and vote.",
          "Release and independently validate the FKNK survey results."],
    footer="Version 1.1  ·  3 October 2026  ·  Draft pending right of reply",
    pdf_title="Claim Check 006 – What does small numbers mean?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
