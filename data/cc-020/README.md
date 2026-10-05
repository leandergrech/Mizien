# Data for CC-020 (EP noise study)

| File | Content | Source and retrieval |
|---|---|---|
| `eurostat_noise.csv` | Population reporting "noise from neighbours or from the street", % of population, Malta, EU-27 and ten comparators, 2005-2023 | Eurostat `ilc_mddw01` (EU-SILC), API, retrieved 5 Oct 2026 (dataset updated 13 Aug 2026). Self-reported, all sources of noise, not limited to END sources. EU-27 series starts 2010; Malta has no 2021-2022 values in the extract. |
| `eurostat_noise_2023_eu27.csv` | The same indicator for all 27 Member States, 2023 | Same dataset, retrieved 5 Oct 2026 |
| `study_figures.csv` | Figures read from the EP study (PE 783.089) and the WHO values it reports | Study text, read 5 Oct 2026 (op.europa.eu copy). Second-hand for EEA/WHO figures: the study cites EEA 2025a. |
| `transposition_tally.csv` | Rough count of Yes/No rows in the study's Annex 1 transposition table | Our count from the PDF text, approximate (table layout) |
| `checks.csv` | Output of `tools/cc-020-report/calc.py` | Calculated |
