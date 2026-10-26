# data/cc-133

- `eurostat_housing.csv`: Malta and EU27_2020 from the Eurostat dissemination API, with status flags, source URL, retrieval date (26 Oct 2026) and dataset update time in each row. Made by `tools/cc-133-report/fetch.py`:
  - `tipsho60` standardised house price-to-income ratio (PTIR_I15, PTIR_LT_AVG, RCH_A_AVG), 2000-2024;
  - `prc_hpi_a` house price index, total purchases (I15_A_AVG, RCH_A_AVG), 2004-2025 (nominal);
  - `prc_hicp_aind` CP041 actual rentals (INX_A_AVG, RCH_A_AVG);
  - `nasa_10_nf_tr` B6G and B7G, households and NPISH (S14_S15), received, current prices, EUR million;
  - `nama_10_pe` population (POP_NC, thousand persons);
  - `ilc_di03` median equivalised net income (MED_EI, EUR, all ages, both sexes); survey year t = income year t-1.
- `checks.csv`: every figure the report uses, from `tools/cc-133-report/calc.py`.
