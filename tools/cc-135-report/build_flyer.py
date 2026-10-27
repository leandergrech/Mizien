"""Claim Check 135 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, GREY  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="135", out=str(OUT / "flyer.pdf"), kicker="Electricity and population",
    title_lines=["Peak electricity", "demand up 43%"],
    subtitle="An IMF staff paper, checked against NSO, Eurostat and Luqa weather data",
    quote_lines=["“Peak electricity demand has increased rapidly in recent", "years, rising from 465 MW in 2018 to 663 MW in 2023.”"],
    attribution="IMF staff, Taking Stock of Infrastructure in Malta, SIP/2025/007, Feb 2025",
    context="Para. 5: this ‘significantly outpaced’ population and tourists (+13%).",
    note="The paper adds that the rise ‘may be related’ to hotter summers (27.3 °C to 29.6 °C).",
    verdict="Largely supported", verdict_right=["Figures exact; the end years", "flatter the trend."],
    cards=[("663 MW", GREEN, "Peak, July 2023", "NSO maximum demand; 465 MW in August 2018. The rise is 42.6%."),
           ("+13.4%", GREEN, "People present", "Residents plus August tourists, 2018–2023, by the IMF’s own method (Eurostat)."),
           ("+13.4%", GREEN, "Energy used", "Final electricity consumption grew with the population; the peak grew far faster."),
           ("+24%", ORANGE, "On the trend line", "Over five years, 2017–2025. Other end years give 28% to 37%."),
           ("26.9 → 29.4", ORANGE, "Hottest month, °C", "Luqa: 2018 was the coolest summer of 2017–2025, 2023 the hottest.")],
    fair="This tests the paper’s figures, not its view on capacity, its 2040 projection or the 2026 power cuts.",
    asks=["IMF: the series and weather station used.", "NSO: Table 7 of the 2024 and 2025 releases.",
          "Enemalta / REWS: hourly system load 2017–2025.", "No right of reply needed."],
    footer="Version 1.0  ·  26 October 2026  ·  Public data only  ·  No right of reply needed",
    pdf_title="Claim Check 135 – Peak electricity demand up 43%"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
