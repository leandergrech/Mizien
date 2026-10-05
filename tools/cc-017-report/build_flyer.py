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
    subtitle="A Budget promise, tested against satellite images, seabed and protected-area maps and research",
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
           ("0.2 km", ORANGE, "To mapped seagrass",
            "Posidonia meadows mapped 0.2 km from the new land; a marine bird area 0.4 km."),
           ("Stable", GREEN, "Malta’s seagrass overall",
            "Malta reports its Posidonia beds favourable and stable; the 34% loss is Mediterranean-wide.")],
    fair="Moving industry away from homes could help residents, and Malta’s seagrass is in good condition overall. "
         "The plan may prove sound once the study and a site are published.",
    asks=["The ERA seabed study.",
          "Site, size and fill source.",
          "Any environmental screening.",
          "Which activities would move."],
    footer="Version 1.2  ·  5 October 2026  ·  Public data only  ·  Right of reply: Finance and Environment ministries "
           "(not yet sent)",
    pdf_title="Claim Check 017 – Reclaiming land outside the Freeport"))
flyer_png(str(OUT / "flyer.pdf"), str(OUT / "flyer.png"))
