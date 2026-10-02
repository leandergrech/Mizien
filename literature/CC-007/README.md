# CC-007: Within EU limits vs WHO guideline

**Status (3 October 2026):** PQ 29696 and its tabled annex were supplied by the maintainer; exact Maltese question and answer, annex values and PDF hashes are transcribed in [`primary-source.md`](primary-source.md). A separate cross-check of the EEA's validated daily files matched 10 of 11 available station-years to the annex at one decimal place. Attard 2024 differs (12.122 µg/m³ from the mean of EEA valid daily aggregates versus 11.9 in the annex). The Minister's answer is procedural and does not state that the values meet EU limits. The report and flyer distinguish that inference from the Minister's words.

## Evidence covered

WHO 2021 guideline and its systematic-review basis; EU ambient-air legislation; Parliamentary Question 29696 and its attached ERA station table; ERA station-network context; a partial EEA validated-data cross-check.

## Findings and gaps

- ERA's annual report for 2024 confirms five fixed stations at Msida, Żejtun, Attard, St Paul's Bay and Għarb (Gozo), and says their data are used for reporting under the Ambient Air Quality Directive. ERA's live-data page describes the five station pages as provisional and says validated data can be requested.
- ERA's published Air Quality Plan 2025 discusses PM10 exceedances at Msida (2018 and 2023); it is not evidence for the claim's PM2.5 comparison.
- The contemporaneous Newsbook lead is linked from `data/sources.csv`; the original Newsbook page was not retrievable for full-text review. A CDE briefing dated 19 July 2025 reproduces a Newsbook summary that all five stations were above the WHO PM2.5 guideline between 2020 and 2024 but below EU limits. It attributes that summary to Newsbook and does not quote the Environment Minister or link to the parliamentary answer. A Wayback snapshot of the Newsbook page is recorded in `archive/manifest.csv`.
- PQ 29696 asks for the annual PM2.5 mean at each ERA monitoring station for the latest five years. Minister Miriam Dalli's exact answer is that the requested information is being laid on the Table of the House. It is not a compliance claim.
- The annex lists 25 possible values and marks St Paul's Bay n/a for 2020 and 2021. Of 23 reported means, all exceed the WHO 2021 annual guideline of 5 µg/m³ and are below the EU annual limit of 25 µg/m³ applicable during the data years. Fourteen are above the recast EU 10 µg/m³ standard to be attained by 2030.
- The EEA Air Quality Download Service describes its station layer as E1a/validated data. Valid daily PM2.5 aggregates from 2020–2024 were available for 11 of the 25 station-years. Ten round to the same one-decimal value as the annex. The EEA mean of valid daily aggregates for Attard in 2024 is 12.122 µg/m³, versus 11.9 in the annex. Both are above WHO's 5 µg/m³ guideline and below the current EU annual limit of 25 µg/m³. The reason for this discrepancy is not established.
- The retrieved EEA files do not contain validated daily series for 14 other station-years, including St Paul's Bay in 2020–2021. Absence from these files does not show whether readings were taken; the PQ annex itself records n/a for those two cells.
- The 10 µg/m³ value is treated only as a future-standard comparison. The report does not call readings above 10 in 2020–2024 legal breaches.
- The Newsbook page is a secondary locator and was not retrievable for full-text review. The report attributes the comparison to Newsbook and does not attribute it to the Minister.
- The WHO guideline is informed by systematic reviews; the Pérez Velasco and Jarosińska paper records the WHO review process. No Malta-specific health-effect estimate is made.

## Sources inspected

- ERA, *Annual Report 2024*, especially the ambient monitoring section (five stations): https://parlament.mt/media/133878/era-annual-2024.pdf
- ERA, *Data from Air Monitoring Stations* (describes provisional live readings and validated data): https://era.org.mt/data-from-air-monitoring-stations/
- ERA, *Air Quality Plan for Malta 2025* (PM10 context only): https://era.org.mt/air-quality-plan-for-malta-2024/
- EEA, PM2.5 annual means by reported station (2023): https://www.eea.europa.eu/en/analysis/maps-and-charts/pm2.5-concentrations-in-2023
- EEA, exceedance of standards indicator (method and EU/WHO distinction): https://www.eea.europa.eu/en/analysis/indicators/exceedance-of-air-quality-standards
- EEA Air Quality Download Service, E1a validated station-data service: https://air.discomap.eea.europa.eu/arcgis/rest/services/AirQuality/AirQualityDownloadServiceEUMonitoringStations/MapServer/0
- CDE, *Malta News Briefing – Saturday 19 July 2023* (published 19 July 2025), reproduces the Newsbook summary: https://cde.news/malta-news-briefing-saturday-19-july-2023/
- House of Representatives, PQ 29696 portal record, Legislature XIV, Sitting 368, 16 July 2025: https://pqs.parlament.mt/?pqid=68a890cbcb302292bff56dce
- WHO, *Global Air Quality Guidelines* (2021), Table 3.26: https://iris.who.int/bitstream/handle/10665/345329/9789240034228-eng.pdf
- Directive (EU) 2024/2881, Annex I: https://eur-lex.europa.eu/eli/dir/2024/2881/oj/eng
- Pérez Velasco R, Jarosińska D (2022), WHO guideline systematic-review process, *Environment International* 170:107556, DOI 10.1016/j.envint.2022.107556: https://doi.org/10.1016/j.envint.2022.107556
- The PQ data and calculation inputs are in `data/cc-007/station_pm25.csv` and `data/cc-007/checks.csv`. EEA results, valid-day coverage and downloaded-file hashes are in `data/cc-007/eea_validated_crosscheck.csv` and `eea_station_file_manifest.csv`; regenerate the EEA cross-check with `tools/cc-007-report/eea_crosscheck.py` (optional `pyarrow` dependency listed beside it).

## Known leads

See `data/sources.csv` (filter on CC-007) for the news, government and EU sources found so far. Those locate the claim and its context; they are not the scientific evidence.

The supplied PDFs were transcribed rather than committed; their SHA-256 hashes and exact wording are retained in `primary-source.md`.
