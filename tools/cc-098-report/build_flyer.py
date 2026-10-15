"""Claim Check 098 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, GREY, BLUE  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="098", out=str(OUT / "flyer.pdf"), kicker="Tourism and population",
    title_lines=["Blue Lagoon: told to", "leave a public beach?"],
    subtitle="Moviment Graffitti’s account of 14 June 2026, tested against the authorities’ response",
    quote_lines=["“…ordered them to leave and even threatened", "to call the police.”"],
    attribution="Moviment Graffitti, press release, 24 June 2026",
    context="Speaker’s own words, English text of the release.",
    note="We did not watch the video; we compared the NGO’s account with four outlets, the authorities’ response and the law.",
    verdict="Largely supported", verdict_right=["The account is undisputed;", "the beach is public."],
    cards=[("14 Jun", BLUE, "Date of the incident",
            "As stated by the NGO; the video was released on 24 June 2026."),
           ("0", GREEN, "Denials found",
            "None in the four outlets read in full, nor in the ministry/MTA statement or the Prime Minister’s reported reply."),
           ("Public", GREEN, "Ministry and MTA",
            "Said the Blue Lagoon and surrounding bathing areas remain public land (TVM News’s indirect speech). The Lands Authority Act lists foreshores as public domain."),
           ("2 views", ORANGE, "Government statements differ",
            "Newsbook reports the Prime Minister as saying the area was “not public”."),
           ("Not read", GREY, "Concession terms",
            "No concession text is published that we could find, so the legal argument on occupation rights is not tested.")],
    fair="The NGO does not call for action against the officials; we rate the statement, not the individuals.",
    asks=["The video or the MTA’s account.", "The concession agreements and map.", "The ministry statement as issued."],
    footer="Version 1.0  ·  15 October 2026  ·  Public sources only  ·  No right of reply needed",
    pdf_title="Claim Check 098 – Blue Lagoon: told to leave a public beach?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
