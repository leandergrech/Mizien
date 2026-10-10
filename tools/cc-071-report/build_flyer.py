"""Claim Check 071 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, reply_status, GREEN, ORANGE, RED, GREY  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="071", out=str(OUT / "flyer.pdf"), kicker="Transport",
    title_lines=["‘Free’ buses:", "€100 million a year?"],
    subtitle="The Shift’s headline figure and its gridlock claim, tested against official statistics",
    quote_lines=["“‘Free’ public transport reaches €100 million a year", "in subsidies as traffic gridlock worsens”"],
    attribution="The Shift News (Ivan Camilleri), 26 February 2026, headline",
    context="Body: the system “cost taxpayers almost €100 million in 2025, according to figures tabled in Parliament”.",
    note="We could not read the parliamentary reply behind the money; the euro figures are second-hand (see report).",
    verdict="Not substantiated", verdict_right=["Nearer €93 million on its own numbers;", "the link to congestion is not tested."],
    cards=[("+1.1 pt", ORANGE, "Congestion, Valletta area",
            "TomTom’s congestion level 49.2% to 50.3%, 2024 to 2025; speed down 0.5 km/h. Two years, one area."),
           ("+5.8%", ORANGE, "Passenger cars since 2022",
            "Eurostat: 317,234 to 335,693 cars by 2025. Population grew 10.4%, so cars per 1,000 residents fell from 610 to 585."),
           ("3 payments", GREY, "Add to less than the headline",
            "The article’s own three 2025 payments sum to under €100m, and one is for buying buses. Second-hand: replies not read."),
           ("Untested", GREY, "Did free travel fail?",
            "No counterfactual in the data. Rising payments and rising cars are both true; cause is not shown."),
           ("0", ORANGE, "Replies or accounts we could read",
            "parlament.mt, finance.gov.mt and Transport Malta refused our access.")],
    fair="Payments have risen every year in the figures reported, and cars and congestion have edged up. What is not shown is the €100 million or the cause.",
    asks=["The Minister’s replies, itemised for 2024 and 2025.", "2025 outturn for the PSO and free-travel lines.",
          "Payments by year on one basis.", "Traffic counts or vehicle-km, 2019–2025."],
    footer="Version 1.0  ·  10 October 2026  ·  Public data only  ·  " + reply_status("Not substantiated").capitalize(),
    pdf_title="Claim Check 071 – ‘Free’ buses: €100 million a year?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
