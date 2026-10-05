"""Claim Check 042 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, GREY, AMBER, GREENC  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="042", out=str(OUT / "flyer.pdf"), kicker="Bathing water, Malta",
    title_lines=["From Blue Flag", "to Red Alert?"],
    subtitle="The PN on Fajtata Bay and the 2025 beach closures",
    quote_lines=["“The same government that boasts about the ‘quality’ of", "our beaches ends up having to close them within days.”"],
    attribution="Nationalist Party (PN), 1 July 2025, as reported by MaltaToday",
    context="After Fajtata Bay closed two days after 13 Blue Flags were announced.",
    note="Dates and causes come from news reports of the Environmental Health Directorate's notices.",
    verdict="Largely supported", verdict_right=["Sequence accurate; closures were brief;", "'systemic failure' is an opinion."],
    cards=[("2 days", GREENC, "Flag to warning",
            "Blue Flags announced Saturday 28 June 2025; Fajtata Bay warning on Monday 30 June (public-toilet overflow)."),
           ("2 days", GREENC, "How long it lasted",
            "Warning lifted on 2 July after repeated sampling showed the water fit for bathing."),
           ("Not sewage", AMBER, "Xlendi",
            "Closed 22-30 June for field run-off after rain; the PN listed it among sewage spills."),
           ("77 of 87", GREY, "Excellent in 2025",
            "EEA classification of Malta's bathing waters: none Poor; 92% were Excellent in 2024."),
           ("Excellent", GREEN, "Fajtata every year",
            "Fajtata (Triq il-Qaliet) has been rated Excellent in every season from 2015 to 2025.")],
    fair="Both sides are partly right: the closure followed the flags, but it was local and short, and Malta's bathing "
         "waters remain mostly Excellent.",
    asks=["EHD: publish closure reports in an archive.", "Water Services Corporation: sewage-incident log.",
          "Government: list of closures per season.", "PN: statement text in full."],
    footer="Version 1.0  ·  5 October 2026  ·  Public data only  ·  No right of reply needed",
    pdf_title="Claim Check 042 - From Blue Flag to Red Alert?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
