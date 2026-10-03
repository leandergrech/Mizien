"""Claim Check 017 flyer. Output: out/flyer.pdf and out/flyer.png"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import Flyer, build_flyer, flyer_png, GREEN, ORANGE, RED  # noqa: E402

OUT = HERE / "out"
build_flyer(Flyer(
    number="017", out=str(OUT / "flyer.pdf"), kicker="Planning and the sea, Birżebbuġa",
    title_lines=["Reclaiming land", "outside the Freeport"],
    subtitle="A Budget promise, tested against satellite images, protected-area maps and research",
    quote_lines=["“The Government is preparing to launch a large-scale", "land reclamation project outside the Freeport…”"],
    attribution="Clyde Caruana, Minister for Finance, Budget Speech 2026, 27 October 2025",
    context="“…perimeter next year.” In 2019: a seabed study found “environmentally safe” sites.",
    note="Checked one year on, 3 October 2026.",
    verdict="Not substantiated", verdict_right=["Existing works real;", "new project not shown."],
    cards=[("+3.7 ha", GREEN, "Reclamation under way",
            "Satellite images confirm new land at Freeport Terminal 2 since 2023."),
           ("0", RED, "Published details",
            "No site, size, cost, fill source or assessment for the large project."),
           ("7 yrs", ORANGE, "Seabed study unpublished",
            "Promised for public consultation in 2019; still not public."),
           ("1 km", ORANGE, "To protected sites",
            "Three Natura 2000 sites, incl. a 256 km² marine bird area."),
           ("−34%", RED, "Seagrass at risk",
            "Mediterranean Posidonia meadows lost a third in 50 years (research).")],
    fair="Moving industry away from homes could help residents. The plan may prove sound once the study and a site "
         "are published.",
    asks=["The ERA seabed study.",
          "Site, size and fill source.",
          "Any environmental screening.",
          "Which activities would move."],
    footer="Version 1.0  ·  3 October 2026  ·  Public data only  ·  Right of reply: Ministry for Finance (not yet sent)",
    pdf_title="Claim Check 017 – Reclaiming land outside the Freeport"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
