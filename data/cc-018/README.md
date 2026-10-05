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
- `eurostat_more.csv` (v1.2): GDP per head (nama_10_pc: current prices, chain-linked 2020 prices, % of EU-27 at
  market prices and in PPS), house price index (prc_hpi_q, prc_hpi_a), households' gross disposable income (nasa_10_nf_tr,
  B6G, S14_S15) and population (nama_10_pe), Malta (and EU-27 for GDP per head), with status flags (p = provisional)
  and the query URL on every row; written by `tools/cc-018-report/fetch_more.py` (retrieved 5 Oct 2026).
- `imf_consultation_cycles.csv` (v1.2): the sentence stating the Article IV consultation cycle in the latest IMF
  staff report of each of the 27 EU members (2025-2026), plus Luxembourg's 2000 and 2002 reports, with eLibrary links;
  written by `tools/cc-018-report/fetch_cycles.py` (read 5 Oct 2026; imf.org itself returns 403 to scripts).
- `imf_extracts.csv` gained the v1.2 rows: 24-month cycle (pp. 26, 66) and per capita income (pp. 8, 25).
- `checks.csv`: written by `tools/cc-018-report/calc.py`.
