"""Claim Check 126 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, BLUE, AMBER  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="126", kicker="Climate and energy, Malta",
    out=str(OUT / "flyer.pdf"),
    title_lines=["PN on the BP gas deal", "and the missing pipeline"],
    subtitle="The Opposition’s statement of 22 June 2026, tested against Enemalta and the promoter",
    quote_lines=["“The Labour Government had promised that by this year", "Malta would have a pipeline for gas supply … it has failed.”"],
    attribution="Partit Nazzjonalista, statement, 22 June 2026",
    context="The BP agreement “will cover only nine months”, “without providing any details about the price”.",
    note="The contract facts hold and the pipeline is unbuilt; the dated promise “by this year” could not be found.",
    verdict="Not substantiated", verdict_right=["Contract facts hold;", "dated promise not shown."],
    cards=[("9.6 mo", GREEN, "BP supply after SOCAR ends",
            "13 Aug 2026 to end of May 2027 (291 days); 11.3 months from the 21 Jun announcement."),
           ("0", AMBER, "Prices published",
            "No price or volume; Enemalta did say it is linked to the TTF gas index."),
           ("2030", ORANGE, "Pipeline start-up (indicative)",
            "On the promoter’s page, updated Dec 2022; construction start 2028."),
           ("0", RED, "Statements found dating it to 2026",
            "Earlier targets of 2024 and 2025 are second-hand; none read in the original."),
           ("2022", BLUE, "PN also proposed a pipeline",
            "Its 2022 programme pledged a gas pipeline to Sicily (our summary).")],
    fair="Labour’s 2017 manifesto reportedly pledged the pipeline and its 2026 manifesto still lists it, so it is late against every date we found. "
         "We did not read the earlier manifestos in the original, so the missing 2026 date is a gap in our search, not proof.",
    asks=["The Labour or Government statement that dated the pipeline to 2026.",
          "The start date of BP supply and any publishable price."],
    footer="Version 1.0  ·  19 October 2026  ·  Public sources only  ·  Pending right of reply",
    pdf_title="Claim Check 126 – PN on the BP gas deal and the missing pipeline"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
