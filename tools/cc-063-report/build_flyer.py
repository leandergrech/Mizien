"""Claim Check 063 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, GREY, AMBER  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="063", out=str(OUT / "flyer.pdf"), kicker="Construction waste, Malta",
    title_lines=["Development at an", "“almost complete standstill”?"],
    subtitle="The developers' June 2021 warning about construction waste",
    quote_lines=["“…development will come to an", "‘almost complete standstill.’” (MaltaToday)"],
    attribution="Malta Developers Association, statement of 2 June 2021, as reported by MaltaToday",
    context="Conditional on no solution to dumping being found.",
    note="Only the words in quotation marks are the Association's; the framing is the outlet's.",
    verdict="Not substantiated", verdict_right=["No standstill in the data,", "but the condition was never tested."],
    cards=[("+5.8%", GREEN, "Construction output, 2021",
            "Volume rose 5.8% in 2021 and 5.5% in 2022 (Eurostat, 2015 = 100: 145.5, 154.0, 162.5)."),
           ("2.1 Mt", AMBER, "Construction waste, 2022",
            "Down from 3.0 Mt in 2020 but above 2018 (2.0 Mt). Construction is 78% of Malta's waste."),
           ("€12/t", GREY, "Fixed gate fee since 2020",
            "Set by government after road works stopped; contractors said it strained tenders in June 2021."),
           ("15", GREY, "Measures, Oct 2021 strategy",
            "The government announced a construction and demolition waste strategy four months later."),
           ("No data", ORANGE, "Latest output figure: 2022",
            "Eurostat has no later year for Malta; we found no published series of quarry intake.")],
    fair="The shortage of disposal space was real: road works halted in 2020 and contractors raised it again in 2021. "
         "A warning is not a forecast with a method; no one has shown a standstill was near.",
    asks=["ERA: quarry intake and capacity by year.", "MDA: the evidence behind “almost complete standstill”.",
          "Government: status of the 2021 strategy's measures.", "NSO: construction output after 2022."],
    footer="Version 1.0  ·  5 October 2026  ·  Draft, pending right of reply",
    pdf_title="Claim Check 063 – Development at an almost complete standstill?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
