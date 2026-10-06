# Data for CC-045 (flood tunnels)

- `ghcnd_luqa_prcp_raw.csv`: NOAA NCEI Global Historical Climatology Network daily, station MT000016597 (Luqa, 35.85 N 14.48 E),
  element PRCP (tenths of mm), 1 Jan 1990 to 5 Oct 2026. Retrieved 6 Oct 2026 from
  `https://www.ncei.noaa.gov/access/services/data/v1?dataset=daily-summaries&stations=MT000016597&startDate=1990-01-01&endDate=2026-10-05&dataTypes=PRCP&format=csv`.
  Blank values are missing readings; no quality flags were requested. 2020-2023 and 2025 have many gaps.
- `lengths.csv`: tunnel lengths as each source states them (retrieved 6 Oct 2026).
- `luqa_annual.csv`, `heavy_days_since_2015.csv`, `checks.csv`: written by `tools/cc-045-report/calc.py`.
