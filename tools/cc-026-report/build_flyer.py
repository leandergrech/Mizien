"""Claim Check 026 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="026", out=str(OUT / "flyer.pdf"), kicker="Climate and energy, Malta",
    title_lines=["Malta’s 169% rise", "in emissions?"],
    subtitle="A news report of a Eurostat estimate, tested against the data",
    quote_lines=["“Malta recorded the highest increase in greenhouse", "gas emissions among European Union member states”"],
    attribution="Newsbook, 18 June 2026, reporting Eurostat",
    context="Emissions “rose by an estimated 169.4% between 2015 and 2025”.",
    note="Eurostat’s own release gives +169.4%; today’s database +169.7%. The EU fell 17.2%.",
    verdict="Largely supported", verdict_right=["The number is right;", "check what it counts."],
    cards=[("+169.7%", RED, "Eurostat accounts",
            "Malta 2015–2025; next highest Cyprus +10.7%. Only four EU states rose."),
           ("98.6%", ORANGE, "Air transport",
            "Share of the 2015–2024 increase from air transport attributed to Malta."),
           ("+2.9%", GREEN, "Everything else",
            "Malta without air transport, 2015–2024 (electricity −16.5%)."),
           ("+1.6%", GREEN, "National inventory",
            "UNFCCC territorial total 2015–2024; 27% below 2005."),
           ("Residence", ORANGE, "Why they differ",
            "Accounts count resident operators wherever they fly; the inventory counts emissions in Malta.")],
    fair="Newsbook’s text explains the aviation difference; its headline alone does not. Neither measure is wrong.",
    asks=["The Central Bank of Malta report.",
          "A national estimate of aviation emissions to and from Malta.",
          "Eurostat’s 2025 activity breakdown.",
          "Which operators drive the total (not assessed)."],
    footer="Version 1.0  ·  5 October 2026  ·  Public data only",
    pdf_title="Claim Check 026 – Malta’s 169% rise in emissions?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
