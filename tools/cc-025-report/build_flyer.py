"""Claim Check 025 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, GREY  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="025", out=str(OUT / "flyer.pdf"), kicker="Climate and emissions, Malta",
    title_lines=["Emissions down 44% per person,", "80% per unit of GDP?"],
    subtitle="A statement at COP30, tested against Eurostat data",
    quote_lines=["“…reduced its per capita emissions by over 44% compared", "to 2005 and emissions per unit of GDP by more than 80%.”"],
    attribution="Government of Malta, COP30 national statement, November 2025",
    context="Delivered on behalf of the Minister for the Environment, Energy and Public Cleanliness.",
    note="The statement gives no year and does not say whether GDP is measured in current prices or in volumes.",
    verdict="Largely supported", verdict_right=["Strong decoupling is real;", "the 80% is a current-price figure."],
    cards=[("−48%", GREEN, "Per person: the figure is right",
            "Eurostat: −46% to 2023, −48.5% to 2024 (EU −34% and −36%). About half is population growth."),
           ("−84%", GREY, "Per unit of GDP, current prices",
            "Only on this basis is “more than 80%” reached (−82% to 2023). Inflation of the GDP figure adds to the fall."),
           ("−72%", ORANGE, "Per unit of GDP, volumes",
            "In real terms the fall is −70% (2023) and −72% (2024); no year reaches −80%. EU: −48%."),
           ("+161%", GREEN, "Real GDP growth since 2005",
            "Total emissions fell 27% over the same years: real decoupling of growth from emissions."),
           ("−27%", RED, "Total emissions: less than the EU",
            "EU −33%. Emissions have risen 18% since their 2016 low. The 2030 target is a separate question (CC-003).")],
    fair="The decoupling the sentence describes is real: output more than doubled while total emissions fell. Malta's "
         "intensity fell more than the EU's on either price basis.",
    asks=["The source and method behind “80%”.", "Whether GDP is in current prices or volumes.",
          "The year and emissions scope used.", "The rest of the statement, to check for context."],
    footer="Version 1.2  ·  6 October 2026  ·  Public data only  ·  No right of reply needed",
    pdf_title="Claim Check 025 – Emissions down 44% per person, 80% per unit of GDP?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
