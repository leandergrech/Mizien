# CC-118 literature notes

Access: F = full text, A = abstract only, S = second-hand, N = not read.

| Key | Source | Access | Finding used | Grade |
|---|---|---|---|---|
| council2026malta | Council doc. 11130/26 (draft, 3 Jul 2026), recital (30) | F | The claim: WEI+ 66.7% (Q3 2023, second-highest); 58% / 45% surface bodies; 82% / 100% groundwater bodies. Attributes the water-body figures to Malta's Third RBMP | C (official, relays other bodies' figures) |
| eea2025wei | EEA indicator page, worst seasonal WEI+ 2023 | F (chart data) | Malta Q3 66.7%, Cyprus Q3 92.1%, Greece Q3 37.4%, Romania Q3 33.9% | C (official statistics) |
| eurostat2026sdg0660 | Eurostat sdg_06_60 and metadata | F | Annual WEI+ 2023: CY 75.29, RO 47.38, MT 30.08; four-year average MT 33.43 (2nd); thresholds 20% / 40% | C |
| eea2022wise | EEA WISE WFD 2022 reporting, Malta | F (database) | 19 surface bodies + territorial waters; 15 groundwater bodies; status codes; areas | C (self-reported by Malta to the EEA) |
| ewa2024quant | EWA technical document, May 2024 | F | 35 monitoring boreholes; 21 (table) / 22 (text) significant negative trends 2000-2021 | C |
| hartfiel2020malta | Hartfiel et al. 2020, Sustainability | A | Review: over-extraction and saltwater intrusion; Malta's water stress | C |
| casadei2020wei | Casadei et al. 2020, Water | A | WEI+ is generally computed at country level; sub-basin values show local stress | C |
| wfd2000 | Directive 2000/60/EC | N | status classes only | - |

## Not read
- Malta's Third River Basin Management Plan (March 2024; era.org.mt returns 403 to scripts, 15 Oct 2026). The Council attributes the water-body percentages to it; we reproduced them from the EEA's WISE copy of Malta's 2022 reporting instead.
- The Commission's 2026 country report for Malta (the likely origin of the WEI+ sentence).
- The adopted Council Recommendation.

## Findings from the data (details in data/cc-118/checks.csv)
- 58% = 11 of 19 surface water bodies at good or high ecological status/potential (territorial waters have no ecological status). By area the same 11 bodies are 96.7% of surface-water area, because the 9 coastal bodies hold 99.96% of it.
- 45% = 9 of 20, which counts the territorial waters (chemical status 'Unknown') in the denominator; 9 of 19 is 47%.
- 82% = 292.5 of 356.9 km2 of groundwater bodies in poor quantitative status (4 of 15 bodies, 27% by number; the Malta Mean Sea Level body alone is 62% of the area).
- 100% = 15 of 15 groundwater bodies in poor chemical status.
- The 'without UPBT' chemical field is identical to the headline field for every Maltese surface body.

## Search log for absences (15 Oct 2026)
- Adopted text of the Council Recommendation: one web search ("Council Recommendation 2026 Malta ... adopted July 2026"); found only the Commission proposal COM(2026) 218 of 3 Jun 2026 and Council drafts 10183/26 and 11130/26. Absence of an adopted text is not established.
- Third RBMP tables: one web search; era.org.mt returned 403 to curl with a browser User-Agent for the plan PDF and the surface-water technical document. Wayback not tried (it reset all connections in the net check of 15 Oct 2026).

## Gaps
The RBMP's own counts; the Commission country report; why Eurostat's annual 2023 WEI+ for Romania (47.4%) exceeds the EEA chart's worst quarter for Romania (33.9%).
