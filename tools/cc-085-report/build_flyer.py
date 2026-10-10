"""Claim Check 085 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, reply_status, GREEN, ORANGE, GREY  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="085", out=str(OUT / "flyer.pdf"), kicker="Tourism and population",
    title_lines=["4.7 million tourists", "to fill the hotels?"],
    subtitle="The MHRA's figure for planned hotel beds, tested against its own study and Eurostat",
    quote_lines=["“Malta will need to attract 4.7 million tourists", "… [to] reach 80 percent occupancy throughout the year.”"],
    attribution="Tony Zahra, President of the MHRA, Horeca Malta, 23 December 2022",
    context="Omitted words: “each spending an average of 7 nights in Malta”. On the MHRA's Deloitte study; repeated in Nov 2024.",
    note="We read the study and its slides in full and recomputed every table.",
    verdict="Largely supported", verdict_right=["The figure is in the study;", "its 80% condition is not."],
    cards=[("4.68m", GREEN, "In the study: one scenario",
            "Airport table, p. 66: guest nights +70% on 2019, 7-night stays. Its other cases: 4.41m and 4.96m."),
           ("4.1–4.5m", GREEN, "Its bed-stock table and slides",
            "Tourists needed to keep 2019 occupancy if the expected beds are built. 2024 update: 4.4–4.8m."),
           ("75.4%", ORANGE, "Hotel room occupancy, 2019",
            "Eurostat; bed-places 66.2%. The study kept 2019 rates, not 80%. Only 4-star hotels reached 81.2%."),
           ("4.6–5.0m", GREEN, "The same beds at 80%",
            "Our calculation from the study's own bed scenarios: the figure survives the 80% condition."),
           ("+20.9%", GREY, "Hotel bed-places since 2019",
            "Eurostat, 2019 to 2025. The study assumed collective beds +80% to +100%; MTA lists 27,672 approved.")],
    fair="The MHRA's warning rests on its own study, and the arithmetic holds. What is overstated is the condition: "
         "the study used 2019 occupancy, and 4.7 million is one of several scenarios.",
    asks=["MHRA: the source of the 80% figure.", "MHRA: do 'the beds we have' include the pipeline?",
          "PA: approved but unbuilt hotel beds.", "MTA: the pipeline by year of opening."],
    footer="Version 1.0  ·  10 October 2026  ·  Public data only  ·  " + reply_status("Largely supported").capitalize(),
    pdf_title="Claim Check 085 – 4.7 million tourists to fill the hotels?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
