"""Claim Check 109 flyer. Run calc.py first. Output: out/flyer.pdf and out/flyer.png"""
import csv
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, AMBER  # noqa: E402

CHK = {r["check"]: r for r in csv.DictReader(open(HERE.parents[1] / "data" / "cc-109" / "checks.csv"))}
v = lambda k, f="{:.1f}": f.format(float(CHK[k]["value"]))
G = v("Transport share of ESR emissions 2024, the report's own Graph 3.1")
ROAD = v("Road transport only (1.A.3.b), 2026 inventory, as share of the approximated ESR total, 2024")
FIN = v("Transport change 2005-2024, 2026 inventory (final submission)", "{:.0f}")
NAV = CHK["Domestic navigation share of ESR transport, 2005 and 2024"]["value"].split(" / ")[1]
NAVCH = v("Domestic navigation (1.A.3.d) change 2005-2024", "{:.0f}")
EU = v("EU-27: ESR transport (1.A.3 - aviation CO2) change 2005-2024", "{:.0f}")

OUT = HERE / "out"
build_flyer(Flyer(
    number="109", out=str(OUT / "flyer.pdf"), kicker="Transport emissions, Malta",
    title_lines=["Is transport 48% of Malta’s", "effort-sharing emissions?"],
    subtitle="A European Commission statement, tested against EEA and Eurostat data",
    quote_lines=["“It has generated 48% of these emissions in 2024,", "up by 45% since 2005.”"],
    attribution="European Commission, 2026 Country Report – Malta, SWD(2026) 218 final, 3 June 2026, p. 66",
    context="The passage begins: “Transport is the dominant source of Malta’s effort sharing emissions.” Also pp. 6, 14.",
    note="Effort sharing: emissions outside the EU emissions trading system, under Malta’s national target. 2024 data approximated.",
    verdict="Largely supported", verdict_right=["Transport dominates and is", "up 45%; its share is 53%."],
    cards=[("53%", GREEN, "Share on the report’s definition",
            f"Transport excluding aviation CO2, 2024: the report’s own Graph 3.1 shows {G}%. Its text says 48%."),
           ("+45%", GREEN, "The rise since 2005 holds",
            f"0.53 to 0.76 Mt on the approximated 2024 data the report uses. Malta’s final 2026 inventory: +{FIN}%."),
           ("20 of 20", GREEN, "Largest sector every year",
            "Transport has been Malta’s biggest effort-sharing source in every year since 2005. Next: small "
            "industry, 19–20%."),
           (f"{ROAD}%", AMBER, "One route to 48%",
            "Road transport alone divided by the effort-sharing total. Our identification: the report does not "
            "say how it got 48%."),
           (f"{float(NAV):.0f}%", AMBER, "Not only road",
            f"Domestic shipping is {NAV}% of effort-sharing transport (2024), up {NAVCH}% since 2005. The report "
            "labels the series “road transport”.")],
    fair=f"The Commission’s message holds, and more strongly than its 48% suggests: transport dominates Malta’s "
         f"effort-sharing emissions and keeps rising, while across the EU-27 the same sector fell {EU[1:]}% "
         "(2005–2024).",
    asks=["The calculation behind the 48% (Commission).",
          "Whether its “road transport” series includes shipping.",
          "Final 2024 figures after the 2027 review.",
          "The EEA’s 2024 sector split, as a table."],
    footer="Version 1.0  ·  6 October 2026  ·  Public data only  ·  No right of reply needed",
    pdf_title="Claim Check 109 – Is transport 48% of Malta's effort-sharing emissions?"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
