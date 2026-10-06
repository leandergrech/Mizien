"""Claim Check 114 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED, AMBER  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="114", out=str(OUT / "flyer.pdf"), kicker="Emissions intensity, Malta",
    title_lines=["Rising intensity,", "and what drives it"],
    subtitle="The PN’s reading of Eurostat’s greenhouse gas intensity figures, tested",
    quote_lines=["“Malta is the only EU Member State which … increased",
                 "the intensity of greenhouse gas emissions from 2013 …”"],
    attribution="Partit Nazzjonalista press release, signed by Eve Borg Bonello, 26 January 2026",
    context="It cites Eurostat (Malta +17%, EU −34%) and blames a lack of ambition on several fronts, among them, renewables.",
    note="Our translation of the Maltese release. Eurostat’s 2024 values are estimates.",
    verdict="Misleading", verdict_right=["Eurostat’s figure is right;", "the rise is airline fuel."],
    cards=[("+14%", RED, "Only rise in the EU",
            "Eurostat’s indicator, 2013–2024 (+17% in January); EU −34%. 2024 is an estimate."),
           ("72%", RED, "Airline fuel bought abroad",
            "Share of Malta’s 2024 figure; firms resident in Malta are counted wherever they fly."),
           ("−64%", GREEN, "Without air transport",
            "Same indicator since 2013 (EU’s 2nd-largest fall); a fall from every base year 2008–2023, −29.5% since 2016."),
           ("−61%", GREEN, "Territorial inventory",
            "Emissions in Malta per euro of GDP since 2013; a fall from every base year 2008–2023, −27% since 2016."),
           ("+1.4%", RED, "With zero power-sector emissions",
            "In 2024 the indicator would still be above 2013, so renewables cannot explain the rise.")],
    fair="The PN quoted Eurostat’s own headline correctly, and from base years 2014–2019 Malta’s rise is larger "
         "(+19.5% to +97%). Malta’s renewable shares are low (10.7% of electricity, the EU’s lowest). The issue is what "
         "the figure counts.",
    asks=["The PN’s source for “third from last”.",
          "Which other “fronts” the PN had in mind.",
          "Which airline operations drive the series.",
          "Malta’s reported 2024 accounts."],
    footer="Version 1.0  ·  6 October 2026  ·  Public data only  ·  Draft pending right of reply from the "
           "Nationalist Party",
    pdf_title="Claim Check 114 – Rising intensity, and what drives it"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
