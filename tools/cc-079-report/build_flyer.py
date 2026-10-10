"""Claim Check 079 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, GREY, BLUE  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="079", out=str(OUT / "flyer.pdf"), kicker="Waste and energy, Malta",
    title_lines=["4.5% of Malta’s energy", "from burning waste?"],
    subtitle="WasteServ’s figures for the Magħtab waste-to-energy plant, tested against Eurostat and the NECP",
    quote_lines=["“It is expected to meet around 4.5% of", "Malta’s total energy needs.”"],
    attribution="WasteServ, ECOHIVE news, 26 June 2023",
    context="Same item: the plant “will be treating around 192,000 tonnes of non-recyclable waste”. In 2020: “4.5% as green energy”.",
    note="Data: Eurostat energy balances (retrieved 10 Oct 2026) and Malta’s National Energy and Climate Plan (Dec 2024).",
    verdict="Misleading", verdict_right=["4.5% fits electricity; of all Malta’s", "energy it is about 1.1–1.8%."],
    cards=[("4.5%", RED, "WasteServ’s figure",
            "The plant would meet “around 4.5% of Malta’s total energy needs”. WasteServ gave no method or year."),
           ("126 GWh", GREEN, "Electricity a year",
            "WasteServ’s own output figure; it matches the NECP design (14–16 MW net, about 24% efficient)."),
           ("4.4–4.7%", BLUE, "Share of electricity, 2022",
            "Where 4.5% fits: 126 GWh against Malta’s electricity use in the year before the statement."),
           ("1.5%", ORANGE, "Share of all energy, 2022",
            "126 GWh against final energy consumption (1.2% of primary energy): about three times smaller."),
           ("3.2%", GREY, "Electricity share, 2030",
            "Against the NECP’s projected supply. The NECP does not count the plant as renewable.")],
    fair="The tonnage (192,000 t) and the output (126 GWh) agree with the Government’s own energy plan, and 4.5% is a "
         "fair figure for electricity. The problem is the word “total”.",
    asks=["WasteServ: the calculation behind the 4.5%.",
          "WasteServ: will the plant supply heat, and how much?",
          "WasteServ or ERA: the EIA’s energy balance.",
          "Ministry: the January 2025 parliamentary answer."],
    footer="Version 1.0  ·  10 October 2026  ·  Public data only  ·  Draft pending right of reply from WasteServ",
    pdf_title="Claim Check 079 – 4.5% of Malta’s energy from burning waste?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
