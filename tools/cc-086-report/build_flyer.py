"""Claim Check 086 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, AMBER, RED  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="086", out=str(OUT / "flyer.pdf"), kicker="Tourism and concessions",
    title_lines=["Comino kiosks:", "a tender from summer 2026?"],
    subtitle="The Minister’s 2025 promise, tested against the Tourism Authority’s own statement",
    quote_lines=["“However, starting in the summer of 2026,", "everyone will have to compete and pay the right price.”"],
    attribution="Ian Borg, Minister for Tourism, quoted by The Shift, 14 Apr 2025",
    context="On Comino’s kiosks and beach concessions, which were left unchanged for 2025.",
    note="The record’s wording on reducing the kiosks is a paraphrase and is not rated.",
    verdict="Missed", verdict_right=["No tender for summer 2026,", "by the MTA’s own account."],
    cards=[("0", RED, "Tenders found", "For the kiosks or beach concessions between February and 12 Oct 2026 (search, not a full register)."),
           ("8 Feb", RED, "MTA: no tender this summer", "“This will have to wait until we have the permit” (Tourism Authority spokesperson)."),
           ("300", GREEN, "Days of notice", "Between the Minister’s promise (14 Apr 2025) and the MTA saying it would not happen."),
           ("11", ORANGE, "Kiosks, March 2025", "The Minister’s figure: “might be too many”. No later count found."),
           ("42", AMBER, "Days since summer ended", "From 31 Aug to 12 Oct 2026; 12 days on the most generous reading (30 Sep).")],
    fair="The Tourism Authority says the intention remains and the delay is a planning permit it has applied for. A tender "
         "later would still be welcome; it would not be the date the Minister gave.",
    asks=["Any tender or call for Comino kiosks in 2026.",
          "The number of kiosk concessions in 2025 and 2026.",
          "The status of application PA00738/26.",
          "The Ministry’s February 2025 statement."],
    footer="Version 1.0  ·  12 October 2026  ·  Public sources only  ·  Pending right of reply",
    pdf_title="Claim Check 086 – Comino kiosks: a tender from summer 2026?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
