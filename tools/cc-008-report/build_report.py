"""Claim Check 008 report. Uses the shared Miżien report design."""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

S = []
S += [SectionHeading(None, "TL;DR"), Spacer(1, mm),
      P("Infrastructure Malta makes different claims about two different junction projects. For Marsa, its 2021 "
        "completion release reports 79% less travel time and reductions in particulate matter, NOx and CO2. For "
        "Msida, the 2024 statement describes lower delays, emissions and noise as expected benefits. The public "
        "material located does not include the underlying Marsa surveys, and the wider Msida project remained "
        "unfinished at the review date.", lead)]
S.append(key_points([
    ("Marsa has reported figures, not a public dataset.", "The completion release reports 79% less travel time, up to 70% less particulate matter, 52% less NOx and 50% less CO2. It does not link the survey series or calculation."),
    ("An interview points to surveys.", "In November 2021, an IM spokesperson said periodic surveys confirmed benefits; the surveys themselves and their methods were not published in the article."),
    ("Msida's statement preceded construction.", "In October 2024, before works began, IM called the new flyover “a critical move to reduce delays, emissions, and noise pollution”. It opened to vehicles in December 2025; other project works continued in 2026."),
    ("Noise is unverified.", "No comparable before-and-after noise measurements were found for either location."),
    ("Verdict: not substantiated.", "The outcomes are plausible and Marsa has agency-reported numbers, but the available public evidence cannot independently verify the combined claim."),
]))
S += [Spacer(1, 3 * mm), VerdictMeter(2), Spacer(1, 2 * mm),
      tiles([("79%", ORANGE, "Marsa travel-time reduction reported by IM"),
             ("Up to 70%", ORANGE, "Marsa particulate-matter emissions reported by IM"),
             ("0", RED, "Published local before/after noise series located")]),
      Spacer(1, 3 * mm),
      up_down("The underlying Marsa surveys, reproducible calculations, and comparable post-opening Msida traffic, "
              "ambient-air and noise measurements.",
              "Evidence that the agency's reported figures are inconsistent with its source measurements or that "
              "the observed local and network outcomes differ materially from the stated effects."), Spacer(1, 4 * mm)]
S += toc([("1", "Wording and project stages"), ("2", "What the records show"),
          ("3", "Induced travel and limits"), ("4", "Verdict and evidence needed"), ("5", "Sources")])
S.append(PageBreak())

S += [SectionHeading(1, "Wording and project stages"),
      P("Infrastructure Malta's 28 October 2024 Msida statement says the area has congestion that affects air "
        "quality and noise, and describes building a new flyover to replace the traffic-light-controlled junction "
        "as “a critical move to reduce delays, emissions, and noise pollution” [1]. The same page says initial "
        "work “will focus on strengthening the Msida waterfront quay” and gives 2027 for completion: works had not "
        "begun, so the stated reductions were expected effects, not measured results. The vehicle flyover opened "
        "in December 2025, but the wider project continued through 2026 [3]."),
      callout([P("THE MARSA AGENCY CLAIM", tag),
               P("The 15 April 2021 Marsa completion release reports “79%” less travel time and “up to 70%” less "
                 "air pollution. It also lists 52% less nitrogen oxides and 50% less carbon dioxide [2].", lead),
               P("These are Infrastructure Malta's reported project benefits. The source page does not link the "
                 "underlying traffic surveys, calculation files, pollutant inputs or uncertainty. It also says that "
                 "removing traffic-light waiting times “is resulting in significant air quality improvements in "
                 "Paola and Marsa”, a statement about local air quality for which it cites no monitoring data.", small)], bg=PALE, bar=GREEN),
      Spacer(1, 3 * mm),
      P("The two cases have different timelines. Marsa is a completed, multi-level project. Msida's road flyover "
        "began operating while other elements, including public spaces and the canal, were still being delivered. "
        "A single combined claim therefore needs separate evidence for each location and outcome."),
      std_table([
          [C("Source", cellh), C("What it establishes", cellh), C("Evidence limit", cellh)],
          [C("IM Marsa release, 2021"), C("Agency's stated time and emissions benefits"), C("No linked survey or method")],
          [C("Times of Malta, 2021"), C("IM spokesperson says periodic surveys confirm benefits"), C("Surveys not reproduced; secondary account")],
          [C("ERA Msida file"), C("Planning baseline and forecast rationale"), C("2019 observations; no post-opening test")],
          [C("PM, December 2025"), C("Flyover entered vehicle use; project continued"), C("No outcome measurements")],
      ], [39 * mm, 71 * mm, 70 * mm]),
      Spacer(1, 3 * mm),
      P("A planning document and an EIA-screening decision are not after-the-fact environmental measurements. "
        "The ERA file records the project process and planning description [4]. Its existence neither proves "
        "benefits nor shows that the impacts are absent.")]

S += [PageBreak(), SectionHeading(2, "What the public records show"),
      P("Marsa's completion release gives four headline percentages. A Times of Malta report later quoted an "
        "Infrastructure Malta spokesperson saying periodic surveys confirmed time and air-quality benefits, even "
        "though junction users were reported to be more than 19% above the 2013 level [5]. This is a useful lead "
        "to the agency's monitoring, but the surveys and methods were not provided in the article."),
      std_table([
          [C("Outcome", cellh), C("Published statement", cellh), C("Needed for independent checking", cellh)],
          [C("Marsa travel time"), C("79% reduction reported"), C("Routes, survey dates, peak periods, distribution and adjustment for demand")],
          [C("Marsa air pollution"), C("PM up to 70%; NOx 52%; CO2 50% reductions reported"), C("Separate emissions estimates from monitor concentrations; publish inputs and locations")],
          [C("Msida delay / emissions / noise"), C("Expected reductions stated in 2024"), C("Comparable data after full road layout is operating")],
          [C("Noise, both sites"), C("No local before/after result located"), C("Comparable noise levels, sites, times and traffic conditions")],
      ], [34 * mm, 53 * mm, 93 * mm]),
      Spacer(1, 3 * mm),
      contested("What do the Marsa percentages measure?", "UNDERLYING SERIES NOT PUBLIC", AMBER,
        "Infrastructure Malta describes reduced travel time and emissions, and later said its periodic traffic "
        "surveys confirmed benefits [2, 5]. The road layout separates several movements and removes the old "
        "traffic-light system, a plausible way to reduce delay for some routes.",
        "The source release does not identify the survey route, dates, traffic periods, baseline adjustment, "
        "pollutant model or uncertainty. “Emissions” does not mean a measured drop in ambient concentrations "
        "at every nearby location. Noise data were not found.",
        "Until the source series is available, the reported percentages remain attributed agency figures. They "
        "cannot be independently recomputed from the public materials cited here."),
      P("For Msida, the Environmental Resources Authority project file includes the planning statement, which "
        "relies on 2019 traffic counts and anticipates reduced travel time and pollution [4]. The 2024 IM wording "
        "also forecasts lower noise. Those documents describe the case for a proposed project. They are not "
        "evidence of its operating performance.")]

S += [SectionHeading(3, "Induced travel and what it means here"),
      P("Duranton and Turner analysed US cities and found that added interstate lane-kilometres were associated "
        "with more vehicle-kilometres travelled [6]. This peer-reviewed evidence supports induced travel as a "
        "possible network-level response to added capacity. It is not a direct estimate for a junction in Malta."),
      P("The finding cautions against assuming that an initial local delay reduction will guarantee lasting "
        "network-wide congestion relief. It does not establish that Marsa had no local travel-time benefit, and "
        "it cannot tell us what happened at Msida. A junction-level analysis must distinguish new trips from "
        "route changes, time-of-day shifts, demographic growth and other network changes."),
      callout([P("KEEP THE MEASURES DISTINCT", tag),
               P("Journey time, queue length, traffic volume, tailpipe emissions, ambient pollutant concentrations "
                 "and noise exposure are related but different outcomes. A before-and-after comparison should "
                 "name the measure and show its place, time period and method.", small)], bg=AMBER_PALE, bar=AMBER)]

S += [PageBreak(), SectionHeading(4, "Verdict and evidence needed"),
      verdict_box("Not substantiated", "Plausible benefits and agency-reported estimates; independent outcome data remain unavailable."),
      Spacer(1, 3 * mm),
      P("<b>Why.</b> Infrastructure Malta reports large Marsa travel-time and emissions reductions, and a later "
        "news report says the agency cited periodic surveys. The underlying surveys and calculation methods were "
        "not located. For Msida, the statement was made before works began; although the flyover is in vehicle use, the "
        "broader project remained in progress in 2026 and no comparable post-opening traffic, air or noise series "
        "was found. The combined claim is therefore stronger than the public evidence that can be checked. "
        "Confidence is moderate because relevant agency claims and planning documents exist, but key data are missing."),
      P("<b>What this verdict does not say.</b> It does not say that the infrastructure had no local benefit or "
        "that the published figures are false. It says the cited public record does not let readers reproduce "
        "or independently assess the outcomes."),
      P("Evidence that would settle the open questions", h2),
      requests_list([
          "Release Marsa's raw traffic counts and travel-time survey methodology, including routes, dates, time windows, baseline adjustments and uncertainty.",
          "Show how each emissions percentage was derived; report monitor-based ambient concentrations separately from estimated emissions.",
          "Publish Msida post-opening traffic, air-quality and noise measurements after the full road arrangement is operating, with defined comparison locations and periods.",
          "Track junction and wider-network outcomes for several years, accounting for fleet/population growth and route or time shifts.",
      ]),
      Spacer(1, 3 * mm),
      P("<b>Right of reply.</b> Not sought in this draft, at the maintainer's direction. Handle before wider circulation.", small),
      SectionHeading(5, "Sources"),
      *references([
          (1, "Infrastructure Malta, Msida Creek: enhancing connectivity and community spaces, 28 October 2024 (wording checked 5 October 2026).", "https://www.infrastructuremalta.com/news/msida-creek-enhancing-connectivity-and-community-spaces"),
          (2, "Infrastructure Malta, Infrastructure Malta completes the Marsa Junction Project, 15 April 2021.", "https://www.infrastructuremalta.com/news/infrastructure-malta-completes-marsa-junction-project"),
          (3, "Office of the Prime Minister, Inawgurata l-flyover tal-Imsida Creek, 17 December 2025 (Maltese).", "https://primeminister.gov.mt/latest-news/pr252279/"),
          (4, "ERA, PA/02053/20 and PA/06425/20 project record and documents.", "https://era.org.mt/era-project/pa02053-20_pa06425-20/"),
          (5, "Times of Malta, Roads agency insists Marsa junction cuts travel time by 70%, despite complaints, 29 November 2021 (secondary).", "https://timesofmalta.com/article/roads-agency-insists-marsa-junction-cuts-travel-time-by-70-despite.913440"),
          (6, "Duranton & Turner, The Fundamental Law of Road Congestion: Evidence from US Cities, American Economic Review 101(6), 2616–2652 (2011).", "https://doi.org/10.1257/aer.101.6.2616"),
      ]),
      Spacer(1, 4 * mm),
      P("Version 1.1 · 5 October 2026 · Draft pending right of reply · Evidence register: data/cc-008/assessment.csv", cap),
      Spacer(1, 4 * mm),
      *revision_log([
          ("1.0", "2 Oct 2026", "First issue. Right of reply not sought, at the maintainer's direction."),
          ("1.1", "5 Oct 2026", "Corrections: the Msida quotation now matches the wording on Infrastructure Malta's page "
           "(checked 5 October 2026); the earlier quotation included words (“this project”, “which will be”) not on "
           "the page as checked, and the forecast reading now rests on the statement having been published before "
           "works began. Added the Marsa release's wording on “significant air quality improvements in Paola and "
           "Marsa”. Heading typo “Mars” corrected to “Marsa”. Verdict and confidence unchanged."),
      ])]

build_report(Report(
    number="008", out=str(ROOT / "claims" / "CC-008" / "report.pdf"),
    kicker="Transport, Malta", title_lines=["Flyovers and", "congestion"],
    subtitle_lines=["What has been shown about journey time,", "air pollution and noise?"],
    quote_lines=["“reduce delays, emissions, and noise pollution”"],
    attribution="Infrastructure Malta, Msida Creek statement, 28 October 2024",
    context="Marsa Junction completed 2021 · Msida Creek flyover opened 2025; wider works ongoing",
    verdict="Not substantiated",
    verdict_note="Marsa figures reported; underlying surveys unavailable.",
    footer_lines=["Miżien · independent, science-first fact-checking", "Draft for review · right of reply remains with the maintainer"],
    running_head="Flyovers, traffic and local pollution", version="1.1", date="5 October 2026",
    pdf_title="Miżien Claim Check 008 – Flyovers and congestion",
    pdf_subject="Published outcome evidence for the Marsa and Msida flyover claims", story=S))
