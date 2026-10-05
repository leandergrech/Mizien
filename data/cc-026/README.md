# CC-026 data

All from the Eurostat dissemination API, retrieved 5 Oct 2026. Unit: thousand tonnes CO2-equivalent (THS_T), all greenhouse gases.

- `malta_ainah_ghg.csv`: env_ac_ainah_r2 (air emissions accounts by NACE Rev. 2 activity, residence principle), Malta, 1995-2025. Columns: TOTAL_HH (all activities plus households), TOTAL (all NACE activities), H51 (air transport), H50 (water transport), D (electricity, gas, steam), H49 (land transport). Dataset updated 2026-08-07. The 2025 value of TOTAL_HH is Eurostat's early estimate (sum of four quarterly accounts); activity detail is not published for 2025.
- `eu_ainah_ghg_total_hh.csv`: the same dataset, TOTAL_HH, all geographies available (EU-27 and member states), 2015, 2024, 2025.
- `malta_unfccc_inventory.csv`: env_air_gge (greenhouse gas emissions by source sector, UNFCCC/CRF inventory, territorial principle), Malta, 1990-2024; updated 2026-06-02. TOTX4_MEMO = total excluding LULUCF and memo items (international aviation and navigation are memo items and excluded); CRF1A3A = domestic aviation; CRF1D1A and CRF1D1B = international aviation and navigation (memo items: fuel sold in Malta).
- Eurostat news item "EU economy greenhouse gas emissions: -17% since 2015", 16 Jun 2026 (ddn-20260616-2), read 5 Oct 2026: gives Malta +169.4%.
- Eurostat metadata env_ac_ainah_r2 (simsae), read 5 Oct 2026: residence principle.
- `checks.csv`: written by `tools/cc-026-report/calc.py`.

Note: values were re-downloaded on 5 Oct 2026 and differ slightly from the 16 Jun 2026 release because Eurostat revises the series (Malta +169.7% now against +169.4% then; Lithuania +8.4% now against +9.5%).
