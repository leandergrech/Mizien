"""Claim Check 005 report. Uses the shared Miżien report design. Run figures.py first. Output: out/report.pdf"""
import csv
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

OUT = HERE / "out"
FIG = HERE / "out"
SH = {int(r["season"]): r for r in csv.DictReader(open(HERE.parents[1] / "data" / "cc-005" / "excellent_share.csv"))}
S = []

S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("The European Commission’s 2025 Malta review says <b>92% of Maltese bathing waters are excellent</b>. The EEA "
        "data confirm it: 80 of 87 sites in 2023, the season the Commission’s full report names, and 80 of 87 again in "
        "2024, so the figure was accurate and current when published. The same data show a decade-long slide, from 86 "
        "of 87 sites (98.9%) in 2016–2018 to 77 (88.5%) in 2025, the lowest of the eleven seasons since 2015 and now "
        "level with the EU coastal average. Ten sites account for every rating below excellent; two at Balluta Bay "
        "have been rated only ‘sufficient’ for four seasons running.", lead)]
S.append(key_points([
    ("The 92% figure checks out.", "The EEA rated 80 of 87 Maltese bathing sites excellent in 2023 (92.0%), the "
     "season the Commission’s staff working document gives, and again 80 of 87 in 2024."),
    ("It is not the latest result.", "In 2025, 77 of 87 sites (88.5%) were excellent; 8 were good and 2 sufficient. "
     "None was poor."),
    ("The share has fallen over ten years.", "86 sites were excellent in each season 2016–2018; then 85, 84, 84, 82, "
     "80, 80 and 77. Malta’s lead over the EU-27 coastal average shrank from 11 percentage points in 2016 to 0.2 in "
     "2025 (Figure 1)."),
    ("The decline is concentrated in a few bays.", "77 sites were excellent in every season from 2015 to 2025. In 2025 "
     "St George’s Bay B03 (St Julian’s) and Xlendi D06 and D07 fell from excellent to good, while Birżebbuġa A11 and "
     "St Paul’s Bay C23 rose from sufficient to good (Figures 2 and 3)."),
    ("Balluta Bay is a persistent problem.", "Its two sites were excellent in 2015–2018, good in 2019–2021 and "
     "only sufficient, the lowest passing class, in every season 2022–2025. The 2024 health warning fell within "
     "that run."),
    ("Verdict: supported, with a date caveat.", "Accurate for 2023 and 2024. Used today without its year, it "
     "overstates the current result by about three and a half percentage points."),
]))
S += [Spacer(1, 3 * mm), VerdictMeter(0), Spacer(1, 2 * mm),
      tiles([("80 / 87", GREEN, "Excellent in 2023 and 2024 (92.0%): the figure quoted"),
             ("77 / 87", ORANGE, "Excellent in 2025 (88.5%), the lowest since 2015"),
             ("88.3%", BLUE, "EU-27 coastal average, 2025: Malta is now level with it"),
             ("4 seasons", RED, "Balluta Bay B08 and B09 rated only sufficient, 2022–2025")]),
      Spacer(1, 3 * mm),
      up_down("None: Supported is the top of the scale. Only the date caveat remains; it would fall away if the "
              "Commission’s summary named the 2023 season beside the 92% figure.",
              "A different EEA count for 2023; a source showing that the Commission meant a later season (the 2025 "
              "result was 88.5%); or evidence that its percentage used an incompatible denominator."), Spacer(1, 4 * mm)]
S += toc([("1", "Claim and sources"), ("2", "What the indicator measures"), ("3", "What the season data show"),
          ("4", "Where the evidence points different ways"), ("5", "Balluta Bay and wastewater"),
          ("6", "Verdict and limits")])
S.append(PageBreak())

S += [SectionHeading(1, "Claim and sources"),
      P("The Commission’s <i>Environmental Implementation Review 2025: Malta</i> summary states: “Malta also shows "
        "excellent records under the Bathing Water Directive: 92% of Maltese bathing waters are of excellent "
        "quality.” The sentence appears in the highlights and gives no reference year. The Commission’s full staff "
        "working document, SWD(2025) 318 of 7 July 2025, does: “in 2023, out of the 87 Maltese bathing waters, 80 "
        "(92%) were of excellent quality” [1, 2].")]
S.append(std_table([
    [C("Source", cellh), C("What it establishes", cellh), C("Use", cellh)],
    [C("European Commission, EIR 2025: Malta, and SWD(2025) 318 [1, 2]"),
     C("Exact 92% sentence; the full report dates it to 2023; wastewater discussed separately."), C("Claim wording")],
    [C("EEA bathing-water data: DiscoMap 2025 service and WISE dataset [3, 4]"),
     C("Class of each of Malta’s 87 sites in every season 2015–2025, with coordinates; EU-27 totals."),
     C("Primary statistical series")],
    [C("EEA, Malta bathing-water profiles, 2024 and 2025 [5, 6]"), C("Season totals and sample counts."),
     C("Cross-check")],
    [C("Directive 2006/7/EC [7]"), C("What is measured, and how a season’s class is assessed."), C("Method")],
    [C("Environmental Health Directorate, Balluta Bay report (2024) [8]"),
     C("Temporary warning at sites B08/B09 and when it was lifted."), C("Local context")],
    [C("CJEU, Commission v Malta, C-304/23 (2024) [9]"),
     C("Urban wastewater treatment obligations for named agglomerations."), C("Separate compliance issue")],
], [52 * mm, 87 * mm, 31 * mm]))
S += [Spacer(1, 3 * mm),
      P("<b>Method.</b> We downloaded the classification of every Maltese bathing water for each season from 2015 to "
        "2025 from the EEA’s bathing-water map service, and checked each site and season from 2015 to 2024 against "
        "the EEA’s WISE dataset: all 870 match. EU-27 shares are counted from the same sources; the 2023 result, "
        "88.9% of coastal bathing waters excellent, matches the EEA’s published figure. Data and scripts: "
        "<i>data/cc-005/</i>, <i>tools/cc-005-report/</i>.", body),
      SectionHeading(2, "What the indicator measures"),
      P("Under the Bathing Water Directive, classification rests on two faecal-indicator bacteria, <i>Escherichia "
        "coli</i> and intestinal enterococci. A season’s class is assessed from the samples of that season and the "
        "three before it, so a change in class reflects four seasons of results, not one bad week [7]. "
        "“Sufficient” is the minimum the directive requires; “excellent” is the best of four classes."),
      P("“Excellent” is a meaningful result for those parameters, but it does not cover every pollutant or the "
        "ecological and chemical state of the sea, and it does not rule out short-lived contamination: a site can "
        "receive a temporary warning and keep its class. The year and the denominator should accompany the "
        "percentage when it is repeated.")]

S += [CondPageBreak(120 * mm), SectionHeading(3, "What the season data show"),
      P("The 92% is the 2023 result, repeated in 2024. Seen across eleven seasons, it is a point on a falling line. "
        "Malta rated 86 of its 87 sites excellent in each season from 2016 to 2018. Since then the count has fallen "
        "every few seasons, to 77 in 2025 (Figure 1). Over the same period the EU-27 coastal average edged up, from "
        f"{SH[2016]['eu27_coastal_excellent_pct']}% in 2016 to {SH[2025]['eu27_coastal_excellent_pct']}% in 2025, "
        "so Malta’s lead over it has all but gone."),
      fig(FIG / "fig1_share.png"),
      P("Figure 1. Share of bathing waters rated excellent, Malta and the EU-27 coastal average, seasons 2015–2025. "
        "Numbers above Malta’s line are the sites rated excellent out of 87.", cap)]
S.append(std_table([
    [C("Season", cellh), C("Excellent", cellh), C("Good", cellh), C("Sufficient", cellh), C("Poor", cellh),
     C("EU-27 coastal, excellent", cellh), C("Samples", cellh)],
    [C("2022"), C("82 (94.3%)"), C("2"), C("3"), C("0"), C(f"{SH[2022]['eu27_coastal_excellent_pct']}%"), C("2,006")],
    [C("<b>2023</b>"), C("<b>80 (92.0%)</b>"), C("3"), C("4"), C("0"), C(f"{SH[2023]['eu27_coastal_excellent_pct']}%"),
     C("2,021")],
    [C("2024"), C("<b>80 (92.0%)</b>"), C("3"), C("4"), C("0"), C(f"{SH[2024]['eu27_coastal_excellent_pct']}%"),
     C("2,107")],
    [C("2025"), C("<b>77 (88.5%)</b>"), C("8"), C("2"), C("0"), C(f"{SH[2025]['eu27_coastal_excellent_pct']}%"),
     C("2,100")],
], [22 * mm, 30 * mm, 18 * mm, 22 * mm, 16 * mm, 38 * mm, 24 * mm]))
S += [Spacer(1, 4 * mm),
      P("<b>Which sites.</b> The decline is not spread along the coast. Of the 87 sites, 77 were excellent in every "
        "season from 2015 to 2025; ten account for every lower rating (Figure 3). Between 2024 and 2025 five sites "
        "changed class. Three fell from excellent to good: B03 on the left of St George’s Bay in St Julian’s, and "
        "D06 and D07 at Xlendi Bay in Gozo. Two rose from sufficient to good: A11 at St George’s Bay in Birżebbuġa and "
        "C23 in St Paul’s Bay (Figure 2). The net effect was three fewer excellent sites and two fewer sufficient "
        "ones."),
      CondPageBreak(150 * mm),
      fig(FIG / "fig2_map.png"),
      P("Figure 2. Malta’s 87 bathing waters coloured by their 2025 class, with the sites that changed class between "
        "2024 and 2025 and those below excellent in both.", cap),
      CondPageBreak(95 * mm),
      fig(FIG / "fig3_sites.png"),
      P("Figure 3. Class of the ten sites rated below excellent in at least one season, 2015–2025. Balluta Bay’s two "
        "sites have been only sufficient since 2022; St George’s Bay in St Julian’s now has both sites at good.", cap)]

S += [CondPageBreak(110 * mm), SectionHeading(4, "Where the evidence points different ways")]
S.append(contested(
    "Q1  Was “92% excellent” a fair description of Malta’s bathing water?", "ACCURATE, NOW DATED", AMBER,
    "The figure is exact for 2023 and the Commission’s full report says so. The 2024 season gave the same 80 of 87, "
    "so the figure was also current when the review appeared in mid-2025. 92% was above the EU-27 coastal average "
    f"({SH[2023]['eu27_coastal_excellent_pct']}% in 2023), and every Maltese site met at least the minimum standard.",
    "The summary sentence omits the year, and “excellent records” describes a record that was getting worse: 98.9% "
    "in 2016–2018, 92.0% in 2023–2024, 88.5% in 2025, the lowest in the series. In 2025 Malta was level with the EU "
    "coastal average. Two Balluta Bay sites have been at the minimum standard for four seasons.",
    "<b>For this claim:</b> the number was right when it was published, so the verdict stays Supported. The fair "
    "reading adds two things the sentence does not say: the result belongs to 2023 and 2024, and the trend since "
    "2018 is downward. Quoted today without its year, 92% overstates the current result."))

S += [CondPageBreak(70 * mm), SectionHeading(5, "Balluta Bay and wastewater")]
S.append(P("Balluta Bay’s two sites, B08 and B09, were excellent from 2015 to 2018, good from 2019 to 2021 and only "
           "sufficient in every season from 2022 to 2025 (Figure 3). Because each class draws on four seasons of "
           "samples, that is a persistent problem at these two sites, not a single bad summer [7]. Within that run, "
           "the Environmental Health Directorate issued a temporary warning at both sites in late May 2024, after "
           "microbial contamination and foul water from a storm-water tunnel; it was lifted on 12 August after three "
           "consecutive samples fell below the thresholds [8]. The 2023 national count already reflects Balluta’s "
           "sufficient rating: the two sites are among the seven not rated excellent that year."))
S.append(P("In Case C-304/23, the Court of Justice found failures to comply with urban wastewater treatment "
           "obligations for named agglomerations [9]. That judgment is not a bathing-water classification, and it "
           "does not show that the EEA’s 2023 result was false. The Commission’s own review reports bathing-water "
           "quality and wastewater treatment under separate headings."))
S.append(callout([P("FAIRNESS NOTE", tag), P("Warnings and wastewater failures matter for public health and for "
    "the sea, but they measure different things from the national classification. This check assesses the dated "
    "statistic and what the same data show since; it does not judge whether every beach is always clean or whether "
    "Malta’s marine environment is healthy overall.", small)], bg=AMBER_PALE, bar=AMBER))

S += [CondPageBreak(60 * mm), SectionHeading(6, "Verdict and limits"),
      verdict_box("Supported", "80 of 87 sites (92.0%) in 2023 and again in 2024. Since then: 77 of 87 (88.5%) in "
                  "2025. Confidence: high."), Spacer(1, 3 * mm),
      P("<b>Why.</b> The EEA’s data confirm 80 excellent sites out of 87 in 2023, the season the Commission’s full "
        "report names, which rounds to the 92% quoted; 2024 gave the same count, so the statement was current when "
        "published. Confidence is high because two EEA sources agree site by site. The caveat is the date: the "
        "share has fallen since 2018 and was 88.5% in 2025, so the year should be stated whenever 92% is used to "
        "describe Malta’s bathing water."),
      P("<b>Limits.</b> This verdict covers only the quoted statistic. The classification uses data reported by "
        "Malta; this check is not an independent sampling programme. It does not assess chemical pollutants, marine "
        "ecological status or health outcomes beyond the directive’s two microbiological indicators, and it does "
        "not explain why individual sites declined."),
      P("Right of reply has not been sought, as directed by the maintainer. The report remains a draft for maintainer "
        "review.", small),
      Spacer(1, 4 * mm), SectionHeading(None, "References")]
S += references([
    (1, "European Commission, <i>Environmental Implementation Review 2025: Malta</i> (country summary). Exact claim "
        "wording; separate wastewater discussion.", "https://op.europa.eu/webpub/env/eir-country-reports-summaries/en/malta.html"),
    (2, "European Commission, <i>2025 Environmental Implementation Review Country Report – Malta</i>, SWD(2025) 318 "
        "final, 7 July 2025. Dates the 92% to the 2023 season.", "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52025SC0318"),
    (3, "EEA, bathing-water map service BathingWater_Dyna_WM_2025, layer 3 (class of each bathing water, seasons "
        "2015–2025, with coordinates). Queried 5 October 2026; extract in data/cc-005/mt_site_classes.csv.",
     "https://water.discomap.eea.europa.eu/arcgis/rest/services/BathingWater/BathingWater_Dyna_WM_2025/MapServer/3"),
    (4, "EEA, WISE Bathing Water Directive dataset, [WISE_BWD].[latest].[assessment_BathingWaterStatus] and "
        "[timeseries_MonitoringResult], via DiscoData SQL. Retrieved 5 October 2026; data/cc-005/.",
     "https://discodata.eea.europa.eu/sql"),
    (5, "EEA, <i>Bathing water quality in the season of 2024: Malta</i> (country factsheet). 80/87 excellent; 2,107 samples.",
     "https://environmentalhealth.gov.mt/wp-content/uploads/2025/07/Malta_bathing_water_2024.pdf"),
    (6, "EEA, <i>Bathing water quality in the season of 2025: Malta</i> (country factsheet). 77/87 excellent; 2,100 samples.",
     "https://www.eea.europa.eu/en/topics/in-depth/bathing-water/state-of-bathing-water/bathing-water-country-factsheets-2025/mt-bathing-water-country-factsheet-2025.pdf/@@download/file"),
    (7, "Directive 2006/7/EC of the European Parliament and of the Council concerning the management of bathing "
        "water quality, Article 4 and Annex II.", "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32006L0007"),
    (8, "Environmental Health Directorate, <i>Report on the temporary closure at B08 and B09 Balluta Bay</i> (2024).",
     "https://environmentalhealth.gov.mt/wp-content/uploads/2024/09/Report-for-Balluta-Bay-the-Bathing-Prohibition-Period-and-Short-Term-Pollution-Period.pdf"),
    (9, "Court of Justice of the European Union, <i>Commission v Malta</i>, Case C-304/23, ECLI:EU:C:2024:906 "
        "(17 October 2024).", "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:62023CJ0304"),
])

S += [Spacer(1, 4 * mm)]
S += revision_log([
    ("1.0", "2 Oct 2026", "First issue. Right of reply not sought, at the maintainer’s direction."),
    ("1.1", "5 Oct 2026", "Corrections: (1) the ‘what would move the verdict’ boxes were reversed. ‘Up’ listed conditions "
     "that would lower the verdict, and ‘down’ cited a newer season at 92% or more. Now: up, none (Supported is the "
     "top of the scale; naming the 2023 season would remove the date caveat); down, a different 2023 count, a later "
     "intended season or an incompatible denominator. (2) Balluta Bay warning start: ‘31 May 2024’ → ‘late May "
     "2024’. Our bibliography gave 21 May, and news reports date the two sites’ warnings ten days apart; the "
     "primary report could not be re-opened to settle it. "
     "(3) 2023 sample count: ‘—’ → 2,021 (EEA WISE dataset). (4) Page footer: ‘pending right of reply’ → ‘right "
     "of reply not sought’, matching the maintainer’s decision. Verdict and confidence unchanged."),
    ("1.2", "5 Oct 2026", "Upgrade: added the EEA classification of all 87 sites for every season 2015–2025 (map "
     "service, checked site by site against the WISE dataset) and the EU-27 coastal share; three figures (Malta "
     "against the EU coastal average, a map of the 2025 classes, and the ten sites ever below excellent). New "
     "findings stated: the 92% was also the 2024 result, so it was current when published; the share has fallen "
     "from 98.9% (2016–2018) to 88.5% (2025), the lowest since 2015 and level with the EU coastal average; the "
     "five sites that changed class in 2025 are named. Balluta Bay is now described as sufficient in every season "
     "2022–2025, not as a single local episode. Added SWD(2025) 318, which dates the figure, and Directive "
     "2006/7/EC. Verdict and confidence unchanged."),
])

build_report(Report(number="005", out=str(OUT / "report.pdf"), kicker="Bathing water, Malta",
    title_lines=["92% excellent", "bathing water"],
    subtitle_lines=["A public claim, tested against eleven seasons", "of EEA bathing-water data"],
    quote_lines=["“92% of Maltese bathing waters are", "of excellent quality.”"],
    attribution="European Commission, Environmental Implementation Review 2025",
    context="True for 2023 and 2024 (80 of 87 sites). In 2025: 77 of 87, the lowest since 2015.",
    verdict="Supported", verdict_note="Accurate for 2023–24; date it.",
    footer_lines=["Draft for maintainer review", "Public data · Right of reply not sought, per maintainer direction"],
    running_head="92% excellent bathing water", version="1.2", date="5 October 2026",
    status_note="right of reply not sought",
    pdf_title="Claim Check 005 – 92% excellent bathing water",
    pdf_subject="Malta bathing water classification, seasons 2015 to 2025", story=S))
