# CC-018 data

- `imf_extracts.csv`: figures and short phrases from IMF Country Report No. 26/29, *Malta: 2025 Article IV
  Consultation* (February 2026), with PDF page numbers. Read in full 4 Oct 2026; PDF kept locally in
  `literature/CC-018/` (not committed; IMF copyright).
- `eurostat_tipsho60.csv`: Eurostat standardised house price-to-income ratio (index 2015 = 100, ratio to long-term
  average, annual change), Malta and EU-27, written by `tools/cc-018-report/fetch_data.py` (retrieved 4 Oct 2026).
- Real house prices are reused from `data/cc-013/eurostat_housing.csv` (the overburden series there feeds Figure 1).
- `eurostat_ilc_lvho07a.csv`: housing-cost overburden rate, Malta and EU-27, 2015-2025, with Eurostat's status flags
  (query URL in the file; retrieved 5 Oct 2026). Malta 2023 is flagged `b` (break in time series), so calc.py
  reports 2015-2022 and 2023-2025 separately.
- `checks.csv`: written by `tools/cc-018-report/calc.py`.
