"""Claim Check 125 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, GREY  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="125", out=str(OUT / "flyer.pdf"), kicker="Climate policy, Malta",
    title_lines=["Malta’s Social", "Climate Plan"],
    subtitle="The Commission’s July 2026 description, checked against its own decision",
    quote_lines=["“… the Maltese Social Climate Plan will mobilise", "EUR 60.6 million.”"],
    attribution="European Commission, DG EMPL news article, 29 July 2026",
    context="Commission Implementing Decision C(2026) 5266 adopts the plan for 2026–2032.",
    note="The article also says the plan will cut primary energy use in social housing by 60%.",
    verdict="Largely supported", verdict_right=["Amounts exact; the 60% is", "a definition, not the payout target."],
    cards=[("60.6m", GREEN, "Exactly as stated", "EUR 60,599,503 in the decision: Fund 45,410,023, Malta 15,189,480."),
           ("25.07%", GREEN, "Malta’s share", "The claim says at least 25%. The numbers add up to the euro."),
           ("60%", ORANGE, "A definition", "The plan counts a 60% cut as a deep renovation. Annex II pays for energy class B or better."),
           ("236", ORANGE, "Units retrofitted", "By 2032: 4.7% of the 5,031 social housing units the plan cites."),
           ("Q1 2027", GREY, "First milestone", "The Fund pays on 16 milestones and targets; none has fallen due yet.")],
    fair="This checks the figures, not whether the plan is right. Savings, emissions and households helped are not yet measurable.",
    asks=["Housing Authority: pre-renovation energy use per unit.", "Commission: the guidance behind the 60%.",
          "Malta: date of the audit opinion due Q4 2026.", "Pledge label: not yet due."],
    footer="Version 1.0  ·  20 October 2026  ·  Public data only  ·  No right of reply needed",
    pdf_title="Claim Check 125 – Malta's Social Climate Plan"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
