# CC-005 literature and source notes

Research checked 2 October 2026. This is a statistical and regulatory claim; the main evidence is the EEA's official annual country series and the Commission's claim wording. The Balluta Bay case is used to test context, not to infer national bathing-water status.

| Key | Source | Access | Finding used | Grade |
|---|---|---|---|---|
| ec_eir_2025_mt | European Commission, Environmental Implementation Review 2025: Malta | F | Says 92% of Maltese bathing waters are excellent under the Bathing Water Directive. The same page separately says urban wastewater is not being properly treated as required by EU law. | C |
| eea_bwd_2023_mt | EEA, Malta bathing water quality 2023 | F | 80/87 coastal sites (92.0%) excellent; 3 good and 4 sufficient. | C |
| eea_bwd_2024_mt | EEA, Malta bathing water quality 2024 | F | 80/87 (92%) excellent; 3 good, 4 sufficient; 2,107 samples. Classification uses E. coli and intestinal enterococci. | C |
| eea_bwd_2025_mt | EEA, Malta bathing water quality 2025 | F | 77/87 (88.5%) excellent; 8 good, 2 sufficient; 2,100 samples. All 87 sites were monitored, none poor or unclassified. The 2025 profile was issued June 2026. | C |
| ehd_balluta_2024 | Environmental Health Directorate, Balluta Bay temporary closure report | F | B08/B09 health warning began in late May 2024 (exact start date unresolved; see below) and was lifted 12 August 2024 after three consecutive samples were below thresholds. The report describes microbial contamination and sewage overflow; it is one local, time-bounded event. | C |
| ecj_c304_23 | Court of Justice of the European Union, Case C-304/23, Commission v Malta | F (judgment) | Finding concerns failures to meet urban wastewater treatment obligations in named agglomerations. It does not classify the 87 bathing sites or establish that the 92% bathing-water result is false. | C |

## Interpretation and limits

The Commission's 2025 highlight reproduces the EEA 2023 result and is accurate as worded. “Excellent” is a Bathing Water Directive classification based on two faecal-indicator bacteria and multi-season monitoring; it does not mean that every site is always free of short-term pollution, nor is it a general assessment of marine ecological or chemical status. The latest available annual result (2025) is lower, at 88.5%, so the 92% figure should be dated rather than presented as current.

The Balluta Bay closure and the CJEU wastewater judgment are material environmental context, but neither contradicts the narrower 2023 country statistic. No blanket verdict about overall sea health is drawn. No peer-reviewed paper was needed to reproduce this official classification; this check does not assess broader health or ecological outcomes.

## Gaps

- The Commission highlight omits the reference year; the 2025 report's 92% corresponds to the EEA 2023 season.
- The national data are reported by Malta to the EEA; this check does not independently resample bathing sites.
- The Balluta report documents one bay (two sites) and one period, late May to 12 August 2024, not national prevalence.
- No source located for the candidate's “hours after receiving a Blue Flag” detail; it is excluded.
- The Commission claim page and CJEU judgment were fetched and have existing Wayback snapshots. The EEA 2025 factsheet was fetched and hashed, but no existing snapshot was found. The EEA 2024 factsheet and EHD Balluta report are marked `robots_disallowed` with no snapshot; archive these manually in a browser if a snapshot is needed. The two news leads are also robots-disallowed, but existing snapshots are recorded.

## Corrections check, 5 October 2026 (v1.1)

**Balluta Bay start date (unresolved).** The v1.0 report and `report.md` said the warning ran from 31 May 2024; `references.bib` said 21 May. The primary EHD report could not be re-opened: the PDF returns HTTP 403 to scripts and the Wayback Machine has no snapshot of it. Second-hand sources, which locate rather than settle the point: TVM News (21 May 2024) reported an EHD warning against swimming in part of Balluta Bay on 21 May; Lovin Malta (18 June 2024) listed B09 under warning "from the 21st May" (high bacterial counts) and B08 "from 31st May" (sewage overflow). The two sites therefore appear to have had different start dates. Our outputs now say "late May 2024", which holds under either reading. Re-check against the EHD report in a browser before stating a day.

**2023 sample count.** The EEA's 2023 Malta factsheet is no longer at its old URL (404), and its Wayback copy could not be retrieved from this environment. The count was taken instead from the EEA's WISE Bathing Water Directive dataset through DiscoData (`https://discodata.eea.europa.eu/sql`), retrieved 5 October 2026:

```sql
SELECT season, COUNT(*) AS samples, COUNT(DISTINCT bathingWaterIdentifier) AS sites
FROM [WISE_BWD].[latest].[timeseries_MonitoringResult]
WHERE bathingWaterIdentifier LIKE 'MT%' AND season >= 2022 GROUP BY season;
SELECT season, quality, COUNT(*) FROM [WISE_BWD].[latest].[assessment_BathingWaterStatus]
WHERE countryCode = 'MT' AND season >= 2022 GROUP BY season, quality;
```

Result: 2023 had 2,021 reported samples at 87 sites (classification 80 excellent, 3 good, 4 sufficient). The same count for 2024 gives 2,107, matching the EEA 2024 factsheet, which supports reading the 2023 figure on the same basis. The 2025 season was not yet in the dataset. Extract: `data/cc-005/eea_bwd_mt_seasons.csv`.

**Claim date (left as 2025).** The quoted wording comes from the Commission's *Environmental Implementation Review 2025* country summary for Malta (op.europa.eu webpub). That page shows no date beyond "© European Union 2025"; its PDF version was generated on 30 June 2025, and DG ENV's publication page for the Malta country report gives "Publication date 23 June 2025". The full staff working document, SWD(2025) 318 final, is dated Brussels, 7.7.2025, but it words the point differently ("Malta also has an excellent record when it comes to the Bathing Water Directive: 92% of Maltese bathing waters are excellent"). It also dates the figure explicitly: "in 2023, out of the 87 Maltese bathing waters, 80 (92%) were of excellent quality". The quoted page is therefore not SWD(2025) 318 and carries no exact date, so `claim.date` stays '2025'.
