"""Claim Check 138 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, GREY, AMBER  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="138", out=str(OUT / "flyer.pdf"), kicker="Parks and open space, Malta",
    title_lines=["Protected from", "development?"],
    subtitle="The White Rocks national park notice, read against the Government’s statement about it",
    quote_lines=["“…biex jiġu mħarsa minn kwalunkwe", "żvilupp fil-futur.”"],
    attribution="Office of the Prime Minister, 29 July 2026",
    context="“…so that they are safeguarded from any future development”, on the White Rocks legal notice.",
    note="We read the notice, the law it is made under, two other park notices and the 2026 manifesto.",
    verdict="Not substantiated", verdict_right=["The park is real; the notice", "restricts no development."],
    cards=[("5", AMBER, "Regulations in the notice",
            "Title, definitions, establishment and two savings clauses (L.N. 209 of 2026)."),
           ("0", RED, "Restrictions on development",
            "Existing permits and authorisations are expressly kept (regulation 4)."),
           ("0", RED, "Mentions of Project Green",
            "The notice names no manager; the Majjistral park’s rules set one up in law."),
           ("100", GREY, "Later 2026 notices searched",
            "L.N. 210–309: none concerns White Rocks. Pledge: not yet due.")],
    fair="The OPM said the site “can be” protected and called this the “beginning” of a pledge. "
         "The planning zoning, which we could not read, may already restrict building.",
    asks=["OPM: which instrument will protect White Rocks from development, and when.",
          "Planning Authority: the site’s current zoning and any pending permits."],
    footer="Version 1.0  ·  17 November 2026  ·  Draft, pending right of reply",
    pdf_title="Claim Check 138 – Protected from development?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
