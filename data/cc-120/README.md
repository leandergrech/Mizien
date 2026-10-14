# Data for CC-120 (EP study: Malta road-noise exposure and health burden)

| File | Content | Source and retrieval |
|---|---|---|
| `eea_exposure_lden55.csv` | People exposed above 55 dB Lden by source, and % of population (all sources), 27 Member States | EEA, *Environmental noise in Europe 2025*, Table 2.1 (PDF pp. 23-24), corrected online version of 27 Mar 2026, read 14 Oct 2026. Transcribed from the PDF text layer. |
| `eea_health_burden_table.csv` | Premature deaths a year and DALYs per 100,000, by source, on END thresholds (Table 3.7, p. 58) and on WHO levels (Table 3.12, p. 64), 27 Member States | Same report, same date. "-" read as 0. Modelled estimates, rounded. |
| `population_2022.csv` | Population on 1 January 2022 | Eurostat demo_pjan (API), retrieved 14 Oct 2026 (dataset updated 25 Sep 2026). Used for per-head rates. |
| `checks.csv` | Output of `tools/cc-120-report/calc.py` | Calculated |

Study figures (20 deaths, 100 DALYs per 100,000, 54,000 and 11,100) are read from PE 783.089, key findings and section 2.3.
