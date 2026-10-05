"""Build the CC-007 report in the shared Miżien report style."""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

OUT = HERE / "out"
S = []

S += [SectionHeading(None, "TL;DR"), Spacer(1, mm),
      P("On 18 July 2025 Newsbook reported that measurements taken between 2020 and 2024 at ERA’s five monitoring "
        "stations “are well within the considerably less stringent annual limits set by the EU for fine particulate "
        "matter (PM2.5)”, while all stations are “well above stringent WHO guidelines”. The source behind the report is "
        "Parliamentary Question 29696: the Minister tabled annual station values for 2020–2024. The answer itself is "
        "procedural; the numbers, not a ministerial statement of compliance, are what this check tests.", lead)]
S.append(key_points([
    ("The historical EU comparison holds for reported values.",
     "All 23 values supplied are below the 25 µg/m³ annual EU limit applicable during 2020–2024."),
    ("Every reported value is above WHO’s health-based guideline.",
     "The annual means range from 7.4 to 13.9 µg/m³; the WHO guideline is 5 µg/m³."),
    ("Two station-years are missing.",
     "St Paul’s Bay is marked n/a in 2020 and 2021, so the table cannot establish compliance at all five stations for every year."),
    ("The next EU standard is stricter.",
     "Fourteen of 23 values exceed the 10 µg/m³ annual limit the EU requires states to attain by 2030. This is context, not a breach during 2020–2024."),
    ("An independent EEA cross-check is mostly consistent.",
     "The EEA validated daily files cover 11 station-years in 2020–2024. Ten match the annex when rounded to one decimal; Attard 2024 does not."),
    ("Newsbook’s figures match the table.",
     "Every station value Newsbook quotes for 2024, and its note that Msida was highest in the previous four years, match the annex."),
    ("Verdict: largely supported (high confidence).",
     "The comparison holds for all 23 annex values and is confirmed independently by EEA data. Two St Paul’s Bay entries are missing."),
]))
S += [Spacer(1, 4 * mm), VerdictMeter(1), Spacer(1, 1 * mm),
      tiles([("23/23", GREEN, "reported values above WHO’s 5 µg/m³ guideline"),
             ("23/23", GREEN, "reported values below the then-applicable EU 25 µg/m³ limit"),
             ("14/23", ORANGE, "above the EU 10 µg/m³ limit due by 2030")]),
      Spacer(1, 4 * mm),
      up_down("ERA’s validated annual series with completeness notes, and an explanation for the Attard 2024 difference.",
              "A corrected official table showing an annual mean above 25 µg/m³, or evidence the table’s values are not comparable to that limit."),
      Spacer(1, 4 * mm)]
S += toc([("1", "What was asked and answered"), ("2", "Standards and method"),
          ("3", "What the table shows"), ("4", "Interpretation and limitations"),
          ("5", "Verdict and evidence needed"), ("6", "Sources")])
S.append(PageBreak())

S += [SectionHeading(1, "What was asked and answered"),
      P("On 16 July 2025, MP Rebekah Borg asked the Minister for the Environment, Energy and Public Cleanliness "
        "for the annual PM2.5 means recorded by every ERA monitoring station for the previous five years. In her "
        "answer, Minister Miriam Dalli said the requested information was being laid on the Table of the House. "
        "The 1-page annex provided the station-by-station values reproduced in this report [1]."),
      callout([P("THE OFFICIAL ANSWER", tag),
               P("“Ninforma lill-Onor. Interpellanta li qed inpoġġi l-informazzjoni mitluba fuq il-Mejda tal-Kamra.”", lead),
               P("Translation: “I inform the Honourable Interpellant that I am laying the requested information on "
                 "the Table of the House.” This does not state that the values comply with an EU standard. The "
                 "compliance statement is an interpretation of the table.", small)], bg=PALE, bar=GREEN),
      Spacer(1, 3 * mm),
      P("The proposition assessed is Newsbook’s report of 18 July 2025, read in full from an archived copy [7]: the 2020–2024 "
        "measurements at the five ERA stations “are well within the considerably less stringent annual limits set by the EU” "
        "and above WHO’s guideline. It is not presented as a direct quotation from the Minister. The "
        "parliamentary portal lists the question as Legislature XIV, Sitting 368, question 29696, 16 July 2025 [1]."),
      std_table([
          [C("Year", cellh), C("Attard", cellh), C("Msida", cellh), C("St Paul’s Bay", cellh), C("Żejtun", cellh), C("Għarb", cellh)],
          [C("2020"), C("9.8"), C("11.0"), C("n/a"), C("9.6"), C("7.4")],
          [C("2021"), C("11.9"), C("12.4"), C("n/a"), C("10.7"), C("8.6")],
          [C("2022"), C("10.8"), C("11.7"), C("10.6"), C("10.1"), C("8.9")],
          [C("2023"), C("11.4"), C("13.9"), C("9.5"), C("10.9"), C("8.9")],
          [C("2024"), C("11.9"), C("11.6"), C("9.5"), C("10.4"), C("8.7")],
      ], [19 * mm, 25 * mm, 25 * mm, 31 * mm, 25 * mm, 25 * mm]),
      P("Table 1. Annual PM2.5 concentration in µg/m³, transcribed from the annex to PQ 29696 [1]. “n/a” is retained as printed.", cap)]

S += [SectionHeading(2, "Standards and method"),
      P("We compared every value in the parliamentary annex with three different reference points. The annual "
        "EU limit applicable during 2020–2024 was 25 µg/m³. The WHO’s 2021 air-quality guideline recommends "
        "5 µg/m³ as the annual mean; it is health-based guidance, not the EU legal limit [2–3]. Recast EU "
        "Directive 2024/2881 sets a 10 µg/m³ annual limit to be attained by 1 January 2030 [3]. We keep that "
        "future standard separate from compliance in the years reported."),
      P("The annex has 25 possible station-year cells. We transcribed its 23 numeric values and kept the two "
        "St Paul’s Bay n/a entries missing rather than imputing them. <i>tools/cc-007-report/calc.py</i> "
        "recalculates counts, range and station means from <i>data/cc-007/station_pm25.csv</i>; the formulas "
        "and results are saved in <i>data/cc-007/checks.csv</i>."),
      P("Evidence grades: the parliamentary answer is grade C (official monitoring data reproduced in an "
        "answer); the WHO guideline is grade C (evidence-based professional guidance); the EU limit is grade C "
        "(primary legislation). This is a standards-and-record check, not an independent exposure or health "
        "assessment. The WHO guideline is informed by systematic reviews of health evidence [2, 4].")]

S += [PageBreak(), SectionHeading(3, "What the table shows"),
      fig(OUT / "station_pm25.png"),
      P("Figure 1. Annual means at five ERA stations. Dashed lines mark the WHO guideline (5 µg/m³) and the EU "
        "standard due by 2030 (10 µg/m³). All reported values are also below the 25 µg/m³ EU limit applicable "
        "to 2020–2024. No value is plotted for St Paul’s Bay in 2020 or 2021.", cap),
      std_table([
          [C("Measure", cellh), C("Result", cellh), C("Interpretation", cellh)],
          [C("Reported values"), C("23 of 25"), C("Two station-years unavailable: St Paul’s Bay, 2020–21.")],
          [C("WHO annual guideline (5 µg/m³)"), C("23/23 above"), C("Every reported station-year exceeds the health-based guideline.")],
          [C("EU annual limit in 2020–2024 (25 µg/m³)"), C("23/23 at or below"), C("All available values meet the historical legal limit.")],
          [C("EU limit due by 2030 (10 µg/m³)"), C("14/23 above"), C("A forward-looking comparison; not the applicable limit in 2020–2024.")],
      ], [56 * mm, 33 * mm, 61 * mm]),
      Spacer(1, 3 * mm),
      P("Across the 23 supplied observations, annual means range from 7.4 µg/m³ (Għarb, 2020) to 13.9 µg/m³ "
        "(Msida, 2023). By station, means of the available years range from 8.50 µg/m³ at Għarb to 12.12 µg/m³ "
        "at Msida. The St Paul’s Bay mean uses only 2022–2024, since the first two years are absent. These are "
        "descriptive arithmetic means of the annual values in the annex, not multi-year regulatory statistics.")]

S += [SectionHeading(4, "Interpretation and limitations"),
      P("The three comparisons answer different questions. The 25 µg/m³ EU limit is a legal compliance benchmark "
        "for the period under review. The WHO value is a health-based guideline; being below a legal limit does "
        "not mean air pollution has no health relevance. The 10 µg/m³ EU standard signals a future regulatory "
        "direction. It is not valid to present the 2020–2024 readings above 10 as breaches of a limit that is "
        "to be attained in 2030 [2–3]."),
      contested("Compliance and health are distinct", "SUPPORTED WITH CAVEAT", GREEN,
                "Every numeric value in the official table is below the EU’s 25 µg/m³ limit applicable to the "
                "reported years.",
                "Every numeric value is above the WHO 5 µg/m³ annual guideline; 14 also exceed the future EU "
                "10 µg/m³ standard.",
                "The legal limit, health guideline and future EU standard have different purposes and dates. "
                "The table supports historical EU compliance for the available data, but not a general claim "
                "that the air is healthy or that every station complied in every year."),
      P("The EEA Air Quality download service publishes validated station measurements. We averaged its valid "
        "daily PM2.5 aggregates for each calendar year with available coverage from 2020 to 2024. This "
        "reproduced 11 of the annex’s 25 possible station-years: ten values round to the annex at one decimal "
        "place. The EEA mean of valid daily aggregates for Attard in 2024 is 12.122 µg/m³, while the annex "
        "reports 11.9. Both are above the WHO guideline and below the 25 µg/m³ EU annual limit; the 0.2 "
        "difference remains unexplained. The retrieved EEA files provide no validated daily series for the "
        "other 14 station-years, including St Paul’s Bay in 2020–21. Absence from those files does not establish "
        "that measurements were not made. Derived values, valid-day counts, source URLs and file hashes are "
        "saved in <i>data/cc-007/eea_validated_crosscheck.csv</i> and "
        "<i>data/cc-007/eea_station_file_manifest.csv</i>; regenerate them with "
        "<i>tools/cc-007-report/eea_crosscheck.py</i> [5]."),
      P("Neither the parliamentary table nor this partial EEA check provides a full basis for local exposure or "
        "individual health outcomes. ERA’s validated annual series, annual completeness notes and an explanation "
        "of the Attard difference are still needed for a complete reconciliation."),
      P("The official annex’s two n/a cells are material to the phrase “all five stations” across the full "
        "period. They are not evidence that St Paul’s Bay exceeded the legal limit; they leave those two "
        "station-years unverified.")]

S += [SectionHeading(5, "Verdict and evidence needed"),
      verdict_box("Largely supported", "All reported values meet the applicable EU limit and exceed WHO’s guideline; two station-years are missing. Confidence: high."),
      Spacer(1, 4 * mm),
      P("The reported comparison is supported for all 23 numeric observations in the annex: each is below the "
        "EU annual limit of 25 µg/m³ in force for 2020–2024, and each exceeds the WHO annual guideline of "
        "5 µg/m³. The EEA check independently supports this broad comparison for 11 station-years, although "
        "one rounded table value differs. Newsbook’s article, now read in full, quotes the 2024 station values "
        "exactly as tabled. Confidence is high because the official table and the EEA data agree; the verdict stops short of "
        "Supported because the annex marks two St Paul’s Bay values n/a, so “all five stations” is not shown for 2020 and "
        "2021. Attard’s 2024 value still needs reconciliation. The Minister’s answer tables figures but does not herself "
        "claim compliance."),
      P("A complete comparison needs ERA’s validated annual series with completeness and quality-control notes, "
        "the missing St Paul’s Bay results if they exist, and an explanation for the Attard 2024 difference."),
      P("Under our standards a right of reply is sought only where a check finds a claim Not substantiated, Misleading or Contradicted, so none is needed for this check. The status remains a draft for maintainer review."),
      P("Reproducible files: <i>data/cc-007/station_pm25.csv</i>, <i>data/cc-007/checks.csv</i>, "
        "<i>data/cc-007/eea_validated_crosscheck.csv</i> and scripts under <i>tools/cc-007-report/</i>. "
        "The exact Maltese question and answer, transcribed annex and attachment hashes are in "
        "<i>literature/CC-007/primary-source.md</i>."),
      SectionHeading(6, "Sources"),
      ]
S += references([
          (1, "House of Representatives (2025). Parliamentary Question 29696, Legislature XIV, Sitting 368, 16 July 2025; oral question and tabled annex.", "https://pqs.parlament.mt/?pqid=68a890cbcb302292bff56dce"),
          (2, "World Health Organization (2021). WHO Global Air Quality Guidelines, Table 3.26: annual PM2.5 guideline 5 µg/m³.", "https://iris.who.int/bitstream/handle/10665/345329/9789240034228-eng.pdf"),
          (3, "European Parliament and Council (2024). Directive (EU) 2024/2881, Annex I: 25 µg/m³ limit through 11 December 2026; 10 µg/m³ to be attained by 1 January 2030.", "https://eur-lex.europa.eu/eli/dir/2024/2881/oj/eng"),
          (4, "Pérez Velasco R., Jarosińska D. (2022). Update of the WHO global air quality guidelines: systematic reviews – An introduction. <i>Environment International</i> 170:107556. doi:10.1016/j.envint.2022.107556. WHO guideline-development context.", "https://doi.org/10.1016/j.envint.2022.107556"),
          (5, "European Environment Agency (accessed 3 October 2026). Air Quality Download Service, verified E1a station data. Annual figures here are means of valid daily aggregates and are used as a partial cross-check.", "https://air.discomap.eea.europa.eu/arcgis/rest/services/AirQuality/AirQualityDownloadServiceEUMonitoringStations/MapServer/0"),
          (6, "CDE (published 19 July 2025). Malta News Briefing – Saturday 19 July 2023. Reproduces the Newsbook PM2.5 comparison; secondary source only.", "https://cde.news/malta-news-briefing-saturday-19-july-2023/"),
          (7, "Newsbook (18 July 2025). “Air pollution exceeds WHO guidelines throughout Maltese islands.” The claim; read in full from the Wayback Machine snapshot of 20 July 2025.", "http://web.archive.org/web/20250720183305/https://newsbook.com.mt/en/air-pollution-exceeds-who-guidelines-throughout-maltese-islands/"),
      ])
S += [PageBreak()]
S += appendix_a("A experiment · B observational study with a control or gradient · C review, professional guidance, "
                "official statistics or primary legislation · D assertion or anecdote. The official parliamentary "
                "table is the direct evidence for the recorded annual means; this report does not infer exposures "
                "or health outcomes beyond those readings.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "2 Oct 2026", "First draft based on Parliamentary Question 29696 and its tabled annex."),
                   ("1.1", "3 Oct 2026", "Added an independent partial cross-check against EEA validated station data; documented one unresolved Attard 2024 difference."),
                   ("1.2", "4 Oct 2026", "Newsbook article read in full (Wayback snapshot): verbatim wording quoted, its figures checked against the annex; confidence raised to high.")])

build_report(Report(
    number="007", out=str(OUT / "report.pdf"), kicker="Air quality, Malta",
    title_lines=["Within limits,", "above the guideline"],
    subtitle_lines=["Five years of annual PM2.5 readings checked against EU and WHO thresholds"],
    quote_lines=["“…well within the considerably less", "stringent annual limits set by the EU…”"],
    attribution="Newsbook, 18 July 2025, on Parliamentary Question 29696",
    context="The Minister tabled the figures; the compliance statement is our test of that table.",
    verdict="Largely supported", verdict_note="All 23 values under 25; two St Paul’s Bay years missing",
    footer_lines=["Version 1.2  ·  4 October 2026", "Draft for maintainer review · no right of reply needed",
                  "Official table, standards and reproducible calculations", "Repository: github.com/leandergrech/Mizien"],
    running_head="PM2.5 · Malta 2020–2024", version="1.2", date="4 October 2026",
    status_note="no right of reply needed",
    pdf_title="Within EU limits, above WHO’s guideline? Claim Check 007",
    pdf_subject="Malta’s annual PM2.5 station means, 2020–2024, compared with historical EU, WHO and 2030 standards",
    story=S))
