"""Claim Check 035 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="035", out=str(OUT / "flyer.pdf"), kicker="Air pollution and health, Malta",
    title_lines=["Did Malta’s PM2.5 death", "rate fall by two-thirds?"],
    subtitle="The EEA’s own estimate, tested against its data and Malta’s stations",
    quote_lines=["“… is estimated to have been reduced by 67.7%", "between 2005 and 2023 …”"],
    attribution="European Environment Agency, Air pollution quick country facts (country fact sheets 2025), 1 Dec 2025",
    context="Malta, deaths attributable to PM2.5 above 5 µg/m³ per 100 000 aged 30+: 143.5 → 46.3; 172 deaths in 2023.",
    note="A modelled estimate: a WHO risk function applied to a concentration map and death statistics.",
    verdict="Largely supported", verdict_right=["Reported exactly; the 2005", "start is a map value."],
    cards=[("67.7%", GREEN, "The figures match",
            "143.5 → 46.3 per 100 000 aged 30+, in the EEA’s own table; 172 deaths in 2023, as Eurostat."),
           ("≤1.2%", GREEN, "The method reproduces",
            "From Eurostat’s death counts we get 346 and 170 deaths, against the EEA’s 348 and 172."),
           ("−39%", GREEN, "Measured PM2.5 fell",
            "At Msida, 22.7 → 13.9 µg/m³ from 2007 to 2023; three long-running stations −25% since 2010."),
           ("0", ORANGE, "None reported for 2005",
            "No Maltese PM2.5 reached the EEA for 2005 (first: August 2006); that year’s value is a map value."),
           ("−51%", ORANGE, "Deaths fell by half",
            "348 → 172: the rate fell more because the over-30 population grew 54%.")],
    fair="The EEA says “is estimated” and names the threshold and age group. Counting all concentrations, or starting "
         "in 2007, the fall is about 55–57%; the 95% CI covers only the risk function.",
    asks=["An uncertainty range for Malta’s 2005 exposure.",
          "Why the technical report gives 173, not 172.",
          "Any 2005 PM2.5 data not sent to the EEA."],
    footer="Version 1.0  ·  6 October 2026  ·  Draft  ·  Public data only  ·  No right of reply needed",
    pdf_title="Claim Check 035 – Did Malta's PM2.5 death rate fall by two-thirds?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
