"""Claim Check 065 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, GREY  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="065", out=str(OUT / "flyer.pdf"), kicker="Planning and housing",
    title_lines=["Ġgantija:", "apartments in the buffer zone?"],
    subtitle="ADPD’s statement on the permit beside the Ġgantija Temples, tested against the records",
    quote_lines=["“Ma kienx biżżejjed tapprova l-kostruzzjoni ta’ appartamenti", "u garaxxijiet fil-buffer zone ta’ madwar il-Ġgantija.”"],
    attribution="ADPD – The Green Party (Sandra Gauci and Luke Caruana), 2 May 2026, in Maltese",
    context="Our translation: “It was not enough to approve apartments and garages in the buffer zone around Ġgantija.”",
    note="We did not read the Authority’s case file or the heritage assessment; sources are listed in the report.",
    verdict="Largely supported", verdict_right=["Approved, and in the buffer zone;", "“sacrilege” is an opinion, not rated."],
    cards=[("30 Apr", GREEN, "Planning Board approves, 10 to 1",
            "22 apartments and 20 garages in Xagħra (PA/00570/21), reported the same day by Newsbook and TVM News."),
           ("7 Mar 2024", GREEN, "Earlier permit revoked",
            "The Authority acknowledged that wrong information had been given on whether the site is in the buffer zone (as reported)."),
           ("150–157 m", GREY, "From the temples, as reported",
            "On the management plan’s map the zone reaches 127–477 m from the temple edge, so distance alone does not settle it."),
           ("Contested", ORANGE, "Does it harm the site?",
            "The assessment and the heritage Superintendence say no; NGOs call the assessment contradictory. Not rated."),
           ("0", ORANGE, "UNESCO comments found",
            "On the final design. UNESCO’s World Heritage Centre pages were refused to us.")],
    fair="The facts ADPD gave hold. Whether the building harms the temples is argued on both sides, and we did not rate it.",
    asks=["The Authority’s decision notice and conditions.", "The plot’s place on the official buffer-zone plan.",
          "The heritage impact assessment.", "Any UNESCO comment on it."],
    footer="Version 1.0  ·  9 October 2026  ·  Public data only  ·  No right of reply needed",
    pdf_title="Claim Check 065 – Ġgantija: apartments in the buffer zone?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
