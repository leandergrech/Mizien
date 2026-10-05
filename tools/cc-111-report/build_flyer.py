"""Claim Check 111 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, GREY  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="111", out=str(OUT / "flyer.pdf"), kicker="Waste, Malta",
    title_lines=["621 kg of waste a head,", "74% landfilled?"],
    subtitle="The European Commission's 2026 Country Report, tested against Eurostat",
    quote_lines=["“…Malta has brought its landfill rate down from 82%", "to 74%. However, this is still one of the highest in the EU.”"],
    attribution="European Commission, 2026 Country Report – Malta, 3 June 2026",
    context="Annex 8, on the last 10 years; the same passage gives 621 kg of waste per person in 2024 (EU 517 kg).",
    note="The report cites Eurostat's municipal waste dataset (env_wasmun), which we downloaded and re-ran.",
    verdict="Supported", verdict_right=["Every figure reproduces", "from the cited Eurostat data."],
    cards=[("621 kg", GREEN, "Waste per person, 2024",
            "Eurostat: 621 kg in Malta, 517 kg in the EU-27. Sixth-highest of the 20 states with 2024 data."),
           ("82→74%", GREEN, "Landfill rate, 2013 to 2023",
            "Landfilled as a share of waste generated: 82.0% and 73.6%. Most of the fall came in 2023 alone."),
           ("3rd", ORANGE, "Rank in the EU, 2023",
            "Only Greece (81%) and Romania (76%) landfilled a larger share. Malta is first of 20 states for 2024."),
           ("72%", GREY, "Landfill rate in 2024",
            "The newer year is similar. Measured against waste treated, it is 79.2% (the figure in CC-081)."),
           ("22%", RED, "EU average landfill rate",
            "Not yet published for 2023; 22.6% in 2022 and 21.3% in 2024 bracket the report's figure.")],
    fair="The passage is accurate. The fall from 82% to 74% is real but mostly one year; the report's summary itself "
         "calls the decade's change marginal.",
    asks=["Eurostat: the EU-27 landfill rate for 2023.", "Waste authorities: why 2015 landfilling exceeds generation.",
          "Readers: check the denominator when sources differ."],
    footer="Version 1.0  ·  5 October 2026  ·  Public data only  ·  No right of reply needed",
    pdf_title="Claim Check 111 – 621 kg of waste a head, 74% landfilled?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
