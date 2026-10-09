"""Claim Check 055 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, GREY  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="055", out=str(OUT / "flyer.pdf"), kicker="Land and trees",
    title_lines=["Manoel Island:", "back to the public?"],
    subtitle="The return from MIDI, and the promise of a national park, tested against public records",
    quote_lines=["“We are transforming this area into a national park designed", "according to the wishes of the Maltese and Gozitan people.”"],
    attribution="Prime Minister Robert Abela, 13 May 2026 (as reported by Newsbook)",
    context="Said on the day the deed ending MIDI’s concession was signed.",
    note="The deed and the Prime Minister’s own release were not readable by us; we used MIDI’s announcements and news reports.",
    verdict="Supported", verdict_right=["The return is confirmed;", "“national park” is Not measurable."],
    cards=[("13 May", GREEN, "Public deed signed",
            "MIDI’s own announcement: concession over Manoel Island and Fort Tigné ended, “resulting in the return thereof to Government”."),
           ("57 days", GREEN, "From first announcement to deed",
            "17 March to 13 May 2026, after Parliament and MIDI’s shareholders approved."),
           ("€43m", GREY, "Net cost (not part of the claim)",
            "MIDI: €47.3m gross, “circa” €43m net of VAT; 55% of the €78m MIDI asked for."),
           ("0 of 6", ORANGE, "Acts that define a “national park”",
            "The term is absent from six Maltese Acts we searched. No plan, designation or date found."),
           ("30", ORANGE, "Padel courts sanctioned or approved",
            "Planning Authority, 16 July 2026, on the island’s former football ground (Lovin Malta). Pledge label: Not measurable (9 Oct 2026).")],
    fair="The return is real and documented. The Government has announced a local plan change and a management plan; we could not find them yet.",
    asks=["The deed and the shareholder circular.", "What “national park” means in law here.",
          "The local plan amendment, if made.", "Heritage Malta’s management plan."],
    footer="Version 1.0  ·  9 October 2026  ·  Public data only  ·  Pending right of reply (pledge label)",
    pdf_title="Claim Check 055 – Manoel Island: back to the public?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
