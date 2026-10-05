# CC-022 data

- `eurostat_prices.csv`: Eurostat nrg_pc_204, household electricity prices, consumption band DC (2,500-4,999 kWh), all
  taxes and levies, EUR and PPS per kWh, all reporting countries, 2019-S1 to 2025-S2. Written by
  `tools/cc-022-report/fetch_data.py` (retrieved 4 Oct 2026).
- `eurostat_prices_bands.csv`: Eurostat nrg_pc_204, PPS per kWh, all taxes, every consumption band (DA to DE and
  the all-band average), all reporting countries, 2024-S2 and 2025-S2, with Eurostat status flags. Same script
  (retrieved 5 Oct 2026).
- `eurostat_prices_mt_history.csv`: Eurostat nrg_pc_204, band DC, EUR per kWh, all taxes, Malta and EU-27,
  2012-S1 to 2025-S2, with status flags. Same script (retrieved 5 Oct 2026).
- `eurostat_poverty.csv`: Eurostat ilc_mdes01 (inability to keep home adequately warm) and ilc_mdes07 (arrears on utility
  bills), % of population, Malta and EU-27, 2015-2025. Same script.
- `imf_energy_subsidies.csv`: energy subsidies as % of GDP from IMF Country Report 26/29 (Table 2; 2025 is a staff
  projection), with Eurostat nominal GDP (nama_10_gdp) to convert to euros. PDF read in full for CC-018.
- `checks.csv`: written by `tools/cc-022-report/calc.py`.
