"""Claim Check 008 report. Uses the shared Miżien report design. Run fetch_data.py, calc.py and figures.py first.
Output: claims/CC-008/report.pdf"""
import csv
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
D = ROOT / "data" / "cc-008"
JS = {(r["window"], r["year"], r["station"]): float(r["no2_ugm3"]) for r in csv.DictReader(open(D / "no2_jan_sep.csv"))}
CK = {r["check"]: r["value"] for r in csv.DictReader(open(D / "checks.csv"))}
A = {(r["station"], r["year"]): r["no2_ugm3"] for r in csv.DictReader(open(D / "no2_annual.csv"))}


def js(code, y):
    return f"{JS[('Jan-Sep', str(y), code)]:.1f}"


MS = [js("MT00011", y) for y in (2024, 2025, 2026)]
RISE = CK["MT00011 Jan-Sep change 2025 to 2026 (%)"].lstrip("+")
D_OLD = round(int(CK["Distance, old Msida point MT00005 to new point MT00011 (m)"]), -1)
D_FLY = round(int(CK["Distance, MT00011 to nearest point of the flyover as mapped (m)"]), -1)
D_FLY0 = round(int(CK["Distance, MT00005 to nearest point of the flyover as mapped (m)"]), -1)
INC = CK["MT00011 minus background, Jan-Sep 2024/2025/2026 (ug/m3)"].split("/")

S = []
S += [SectionHeading(None, "TL;DR"), Spacer(1, mm),
      P("Infrastructure Malta says its Marsa junction cut travel time and air pollution, and that the Msida Creek "
        "flyover would cut delays, emissions and noise. The Marsa figures are the agency’s own, without published "
        "surveys. The Msida flyover opened on 18 December 2025; in the nine months since, nitrogen dioxide at the "
        f"Msida roadside monitor rose to {MS[2]} µg/m³ (January–September), from {MS[1]} a year earlier. With one "
        "monitor, unvalidated data and works still under way, that does not show the flyover made air worse; it "
        "shows the promised improvement has not yet appeared where it is measured.", lead)]
S.append(key_points([
    ("Marsa has reported figures, not a public dataset.", "79% less travel time and up to 70% less particulate "
     "matter, 52% less NOx and 50% less CO2, without the surveys or calculations. No EEA-reported air monitor has "
     "operated within 1.4 km of the junction since 2016."),
    ("Msida’s statement was a forecast.", "IM wrote it in October 2024, before works began. The flyover opened to "
     "traffic on 18 December 2025; the wider project is due for completion in 2027."),
    ("NO2 at the Msida monitor rose after opening.", f"January–September means: {MS[0]} (2024), {MS[1]} (2025), "
     f"{MS[2]} µg/m³ (2026, unvalidated), up {RISE}% on 2025. Attard and Żejtun rose about 4%; St Paul’s Bay fell "
     "6% (Figures 1 and 2)."),
    ("The series has limits.", f"A new sampling point, about {D_OLD} m east of the old one and {D_FLY} m from the "
     "flyover, replaced it in January 2024, so the record is not continuous. No noise data were found for either "
     "junction."),
    ("Verdict: not substantiated.", "The benefits are plausible, but the public evidence does not verify them, and "
     "the one measured outcome at Msida does not yet show them."),
]))
S += [Spacer(1, 3 * mm), VerdictMeter(2), Spacer(1, 2 * mm),
      tiles([("79%", ORANGE, "Marsa travel-time cut reported by IM; survey not published"),
             (f"+{RISE}%", RED, "NO₂ at the Msida monitor, Jan–Sep 2026 on 2025 (unvalidated)"),
             ("1.4 km", ORANGE, "from Marsa junction to the nearest EEA-reported NO₂ monitor"),
             ("0", RED, "Published before/after noise series for either junction")]),
      Spacer(1, 3 * mm),
      up_down("The underlying Marsa surveys and calculations, and validated Msida traffic, air and noise data, once "
              "the full road layout is operating, that show the stated reductions.",
              "Evidence that the agency’s figures are inconsistent with its source measurements, or validated, "
              "weather- and traffic-adjusted data from several sites showing that the flyovers raised local "
              "pollution or delays."), Spacer(1, 4 * mm)]
S += toc([("1", "Wording and project stages"), ("2", "What the records show"), ("3", "What the Msida air monitor shows"),
          ("4", "Induced travel and limits"), ("5", "Verdict and evidence needed"), ("6", "Sources")])
S.append(PageBreak())

S += [SectionHeading(1, "Wording and project stages"),
      P("Infrastructure Malta's 28 October 2024 Msida statement says the area has congestion that affects air "
        "quality and noise, and describes building a new flyover to replace the traffic-light-controlled junction "
        "as “a critical move to reduce delays, emissions, and noise pollution” [1]. The same page says initial "
        "work “will focus on strengthening the Msida waterfront quay” and gives 2027 for completion: works had not "
        "begun, so the stated reductions were expected effects, not measured results. The vehicle flyover opened "
        "to traffic on 18 December 2025, the day after its inauguration, but the wider project continued through "
        "2026 [3]."),
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
          [C("EEA air-quality data, 2022–2026"), C("Hourly NO2 at Msida and comparison stations"), C("One site; new sampling point; 2026 unvalidated")],
      ], [39 * mm, 71 * mm, 70 * mm]),
      Spacer(1, 3 * mm),
      P("A planning document and an EIA-screening decision are not after-the-fact environmental measurements. "
        "The ERA file records the project process and planning description [4]. Its existence neither proves "
        "benefits nor shows that the impacts are absent.")]

S += [CondPageBreak(60 * mm), SectionHeading(2, "What the public records show"),
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
        "at every nearby location. Kordin, the EEA-reported station in Paola, closed at the end of 2016, before the "
        "works; none has operated within 1.4 km of the junction since (Figure 3). Noise data were not found.",
        "Until the source series is available, the reported percentages remain attributed agency figures. They "
        "cannot be independently recomputed from the public materials cited here."),
      P("For Msida, the Environmental Resources Authority project file includes the planning statement, which "
        "relies on 2019 traffic counts and anticipates reduced travel time and pollution [4]. The 2024 IM wording "
        "also forecasts lower noise. Those documents describe the case for a proposed project. They are not "
        "evidence of its operating performance.")]

S += [CondPageBreak(120 * mm), SectionHeading(3, "What the Msida air monitor shows"),
      P("Malta’s air-quality network has a station at Msida classified as a traffic station, sited to measure "
        "pollution from road traffic, and its hourly nitrogen dioxide (NO2) readings are reported to the European "
        "Environment Agency [7, 9]. It is the one public, independent measurement close to either junction. We "
        "downloaded the hourly data for Msida and three comparison stations from January 2022 to September 2026, "
        "kept only hours flagged valid, and averaged them by month (Figure 1) and over January to September of each "
        "year (Figure 2) [7]. For scale, the annual limit value is 40 µg/m³, falling to 20 µg/m³ from 2030 [8]; the "
        f"new Msida point averaged {float(A[('MT00011', '2024')]):.1f} µg/m³ in 2024 (from 17 January) and "
        f"{float(A[('MT00011', '2025')]):.1f} in 2025."),
      P(f"<b>The monitor moved.</b> The old roadside point (MT00005), {D_FLY0} m from the flyover as now mapped and 5 m "
        "from the kerb, recorded NO2 from 2006; its annual mean fell from "
        f"{float(A[('MT00005', '2013')]):.1f} µg/m³ in 2013 to {float(A[('MT00005', '2023')]):.1f} in 2023, and its "
        "last valid readings are from December 2023. A new point (MT00011) started on 17 January 2024, about "
        f"{D_OLD} m east and {D_FLY} m from the flyover, 9 m from the kerb, according to the station metadata ERA "
        "reports to the EEA [9]. The two points never ran side by side with valid data, so the series is not "
        "continuous and only the new point can compare before and after the opening."),
      P(f"<b>After the opening.</b> In January–September 2026, the first nine full months after the flyover opened, "
        f"the new Msida point averaged {MS[2]} µg/m³, {RISE}% more than in the same months of 2025 ({MS[1]}) and above "
        f"2024 ({MS[0]}). At the urban background stations the rise was smaller: Attard {js('MT00008', 2025)} → "
        f"{js('MT00008', 2026)} and Żejtun {js('MT00004', 2025)} → {js('MT00004', 2026)}. At St Paul’s Bay, the other "
        f"traffic station, NO2 fell from {js('MT00009', 2025)} to {js('MT00009', 2026)} (Figure 2). Msida’s excess "
        f"over the background average grew from {INC[1]} µg/m³ in 2025 to {INC[2]} in 2026; it had already grown "
        f"from {INC[0]} in 2024, before the opening."),
      CondPageBreak(110 * mm),
      fig(FIG / "fig1_no2_monthly.png"),
      P("Figure 1. Monthly mean NO2 at Msida (old point to 2023, new point from January 2024) and at three comparison "
        "stations. 2026 values are up-to-date data not yet validated.", cap),
      CondPageBreak(80 * mm),
      fig(FIG / "fig2_jan_sep.png"),
      P("Figure 2. Mean NO2 over January–September at each station: 2024 and 2025 (validated) and 2026, after the "
        "flyover opened (unvalidated).", cap),
      callout([P("WHAT THIS DOES AND DOES NOT SHOW", tag),
               P("It shows that, nine months after the opening, NO2 at the only monitor near the Msida junction had "
                 "not fallen; it rose more than at the comparison stations. It does not show that the flyover caused "
                 f"the rise. This is one site, {D_FLY} m from the flyover; works on the wider project continue until "
                 "2027; the 2026 data are not yet validated (September has 61% of hours valid at Msida); the "
                 "comparison is not adjusted for weather or traffic volumes; and NO2 concentration is not the same "
                 "measure as delays, emissions or noise.", small)], bg=AMBER_PALE, bar=AMBER),
      Spacer(1, 3 * mm),
      CondPageBreak(120 * mm),
      fig(FIG / "fig3_map.png"),
      P("Figure 3. The Msida flyover, the Marsa junction and the NO2 monitoring points reported to the EEA.", cap)]

S += [CondPageBreak(70 * mm), SectionHeading(4, "Induced travel and what it means here"),
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

S += [CondPageBreak(70 * mm), SectionHeading(5, "Verdict and evidence needed"),
      verdict_box("Not substantiated", "Agency-reported Marsa estimates without public data; at Msida, the one "
                  "measured outcome has not improved since opening. Confidence: moderate."),
      Spacer(1, 3 * mm),
      P("<b>Why.</b> Infrastructure Malta reports large Marsa travel-time and emissions reductions, and a later "
        "news report says the agency cited periodic surveys. The underlying surveys and calculation methods were "
        "not located, and no EEA-reported monitor near Marsa has operated since 2016. For Msida, the statement was "
        "made before works began. Since the flyover opened, NO2 at the Msida monitor has risen, not fallen, more "
        "than at the comparison stations; no traffic or noise series was found. The combined claim is therefore "
        "stronger than the public evidence that can be checked. The Msida data support “not substantiated”, not "
        "“contradicted”: one site, a moved sampling point, unvalidated 2026 data and unfinished works cannot show "
        "the flyover made things worse. Confidence is moderate because agency claims and one independent series "
        "exist, but key data are missing."),
      P("<b>What this verdict does not say.</b> It does not say that the infrastructure had no local benefit or "
        "that the published figures are false. It says the cited public record does not let readers reproduce "
        "or independently confirm the outcomes, and that the one independent measurement does not yet show them."),
      P("Evidence that would settle the open questions", h2),
      requests_list([
          "Release Marsa's raw traffic counts and travel-time survey methodology, including routes, dates, time windows, baseline adjustments and uncertainty.",
          "Show how each emissions percentage was derived; report monitor-based ambient concentrations separately from estimated emissions.",
          "Publish Msida post-opening traffic, air-quality and noise measurements after the full road arrangement is operating, with defined comparison locations and periods.",
          "Explain why the Msida sampling point moved in January 2024 and publish any parallel readings from the two points.",
          "Track junction and wider-network outcomes for several years, accounting for fleet/population growth and route or time shifts.",
      ]),
      Spacer(1, 3 * mm),
      P("<b>Right of reply.</b> Not sought in this draft, at the maintainer's direction. Handle before wider circulation.", small),
      SectionHeading(6, "Sources"),
      *references([
          (1, "Infrastructure Malta, Msida Creek: enhancing connectivity and community spaces, 28 October 2024 (wording checked 5 October 2026).", "https://www.infrastructuremalta.com/news/msida-creek-enhancing-connectivity-and-community-spaces"),
          (2, "Infrastructure Malta, Infrastructure Malta completes the Marsa Junction Project, 15 April 2021.", "https://www.infrastructuremalta.com/news/infrastructure-malta-completes-marsa-junction-project"),
          (3, "Office of the Prime Minister, Inawgurata l-flyover tal-Imsida Creek, 17 December 2025 (Maltese). The flyover was to open to vehicles the following day.", "https://primeminister.gov.mt/latest-news/pr252279/"),
          (4, "ERA, PA/02053/20 and PA/06425/20 project record and documents.", "https://era.org.mt/era-project/pa02053-20_pa06425-20/"),
          (5, "Times of Malta, Roads agency insists Marsa junction cuts travel time by 70%, despite complaints, 29 November 2021 (secondary).", "https://timesofmalta.com/article/roads-agency-insists-marsa-junction-cuts-travel-time-by-70-despite.913440"),
          (6, "Duranton & Turner, The Fundamental Law of Road Congestion: Evidence from US Cities, American Economic Review 101(6), 2616–2652 (2011).", "https://doi.org/10.1257/aer.101.6.2616"),
          (7, "European Environment Agency, air-quality download service: hourly NO2 for Malta, sampling points MT00005, "
              "MT00011, MT00004, MT00008 and MT00009; validated (E1a) data to 2025 and up-to-date (E2a) data for 2026. "
              "Retrieved 5 October 2026; monthly, annual and January–September means in data/cc-008/.",
           "https://eeadmz1-downloads-webapp.azurewebsites.net/"),
          (8, "Directive (EU) 2024/2881 on ambient air quality and cleaner air for Europe (recast): NO2 annual limit of "
              "20 µg/m³ from 2030; the limit in force is 40 µg/m³.", "https://eur-lex.europa.eu/eli/dir/2024/2881/oj"),
          (9, "Environment and Resources Authority, Air Quality e-Reporting dataset D (measurement configuration) for "
              "2025, Eionet Central Data Repository, 3 February 2026: station and sampling-point locations, "
              "classification and kerb distance.",
           "https://cdr.eionet.europa.eu/mt/eu/aqd/d/envayh2iw/"),
          (10, "OpenStreetMap contributors, Msida Creek flyover carriageways (ways 1460775989 and 1460775991) and "
               "coastline, retrieved 5 October 2026 (ODbL).", "https://www.openstreetmap.org/way/1460775989"),
      ]),
      Spacer(1, 4 * mm),
      P("Version 1.2 · 5 October 2026 · Draft; right of reply not sought · Evidence register: data/cc-008/assessment.csv", cap),
      Spacer(1, 4 * mm),
      *revision_log([
          ("1.0", "2 Oct 2026", "First issue. Right of reply not sought, at the maintainer's direction."),
          ("1.1", "5 Oct 2026", "Corrections: the Msida quotation now matches the wording on Infrastructure Malta's page "
           "(checked 5 October 2026); the earlier quotation included words (“this project”, “which will be”) not on "
           "the page as checked, and the forecast reading now rests on the statement having been published before "
           "works began. Added the Marsa release's wording on “significant air quality improvements in Paola and "
           "Marsa”. Heading typo “Mars” corrected to “Marsa”. Verdict and confidence unchanged."),
          ("1.2", "5 Oct 2026", "Upgrade: added EEA hourly NO2 data for Msida and three comparison stations, 2022 to "
           "September 2026, with a new section and three figures (monthly series, January–September comparison, "
           "map of the monitoring points from ERA's station metadata). New finding: in the nine months after the "
           f"flyover opened (18 December 2025), NO2 at the Msida monitor was {RISE}% higher than a year earlier "
           "(unvalidated data), with caveats stated: one site, a new sampling point from January 2024, works "
           "continuing until 2027. Added that no EEA-reported monitor has operated near Marsa since 2016. Page "
           "footer and cover: “pending right of reply” → “right of reply not sought”, matching the text. Verdict and "
           "confidence unchanged."),
      ])]

build_report(Report(
    number="008", out=str(ROOT / "claims" / "CC-008" / "report.pdf"),
    kicker="Transport, Malta", title_lines=["Flyovers and", "congestion"],
    subtitle_lines=["What has been shown about journey time,", "air pollution and noise?"],
    quote_lines=["“reduce delays, emissions, and noise pollution”"],
    attribution="Infrastructure Malta, Msida Creek statement, 28 October 2024",
    context="Marsa Junction completed 2021 · Msida Creek flyover opened 18 Dec 2025; wider works ongoing",
    verdict="Not substantiated",
    verdict_note="Marsa figures unpublished; Msida NO2 not down.",
    footer_lines=["Miżien · independent, science-first fact-checking", "Draft for review · right of reply not sought (maintainer’s direction)"],
    running_head="Flyovers, traffic and local pollution", version="1.2", date="5 October 2026",
    status_note="right of reply not sought",
    pdf_title="Miżien Claim Check 008 – Flyovers and congestion",
    pdf_subject="Published outcome evidence for the Marsa and Msida flyover claims, with EEA NO2 data for Msida",
    story=S))
