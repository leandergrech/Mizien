"""Claim Check 147 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="147", out=str(OUT / "flyer.pdf"), kicker="Climate and energy, Malta",
    title_lines=["Did emissions", "intensity fall 19%?"],
    subtitle="A government factsheet, tested against Eurostat’s tables",
    quote_lines=["“GHG intensity per every euro generated between", "2024 and 2020 in fact reduced by 19%”"],
    attribution="Climate Action Authority, factsheet on air emissions accounts, February 2026",
    context="Excluding air and maritime transport; Eurostat’s figures “show a growth rate of 87.2%”.",
    note="The 19% is the Authority’s own calculation; we rebuilt it from Eurostat data.",
    verdict="Largely supported", verdict_right=["Numbers check out;", "two valid measures compared."],
    cards=[("Grade C", GREEN, "Official data",
            "Eurostat air emissions accounts, value added and the territorial inventory bridge."),
           ("68%", ORANGE, "Air transport dominates",
            "Share of Malta’s 2024 emissions on Eurostat’s residence basis (EU-27: 4%)."),
           ("+86%", RED, "Eurostat’s total, reproduced",
            "GHG per euro of value added, 2020–2024, all activities (factsheet: +87.2%)."),
           ("−22%", GREEN, "Without air and water transport",
            "Our rebuild of the factsheet’s −19%; territorial emissions per euro also give −22%."),
           ("2020", ORANGE, "An unusual start year",
            "Air transport’s value added was negative in the Covid year, which flatters the fall; later start years give −8% to −15%.")],
    fair="Removing aviation changes the measure rather than correcting it: the factsheet itself says the Eurostat accounts "
         "count emissions by residence. Both figures are defensible.",
    asks=["The Authority’s workings for the −19%.",
          "The Eurostat data vintage it used.",
          "The periods behind the page-5 figures.",
          "Which measure should track progress."],
    footer="Version 1.0  ·  2 November 2026  ·  Public data only  ·  No right of reply needed",
    pdf_title="Claim Check 147 – Did emissions intensity fall 19%?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
