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
- `eurostat_burden_inputs.csv` (v1.2): every Eurostat input used to measure burden against income and use, long
  format with status flags and query URLs: nrg_pc_204 (EUR, all taxes, all bands, 2024-S1 to 2025-S2), nrg_pc_204_v
  (consumption shares by band), ilc_di03 (median and mean equivalised net income, EU-SILC 2024 and 2025), ilc_di01
  (first-quintile top cut-off and income share), nrg_d_hhq (household electricity use, total and by end use),
  lfst_hhnhtych (private households), nasa_10_nf_tr (B6G, S14_S15, RECV), hbs_str_t211 (CP0451, 2020), ilc_mdes01 and
  ilc_mdes07 (total and below 60% of median income, 2024-2025), ilc_hcmp03 (2012). Written by
  `tools/cc-022-report/fetch_burden.py` (retrieved 5 Oct 2026).
- `burden_measures.csv` (v1.2): each burden measure for every EU-27 Member State and the EU-27, with inputs, input
  flags and rank (1 = lowest burden; equal values share a rank). Written by `tools/cc-022-report/burden.py` (called by
  calc.py).
- `checks.csv`: written by `tools/cc-022-report/calc.py`.
