# CC-013 data

- `eurostat_housing.csv`: Eurostat prc_hpi_a (nominal house prices), tipsho10 (deflated), sts_cobp_a (permits for
  residential buildings with 2+ dwellings, index 2015=100, two series per year: number of dwellings, BPRM_DW, and
  m2 of useful floor area, BPRM_SQM; not used in the report), demo_gind (population), ilc_lvho07a (housing cost
  overburden), ilc_lvho05a (overcrowding); Malta and EU-27; retrieved 3 Oct 2026 from the Eurostat dissemination
  API. Status flags for ilc_lvho07a, tipsho10, prc_hpi_a and sts_cobp_a were checked on 5 Oct 2026 and are in the
  `note` column (e.g. Malta ilc_lvho07a 2023: b, break in time series; Malta tipsho10 and prc_hpi_a 2025: p,
  provisional). The sts_cobp_a item labels were corrected on 5 Oct 2026 (the floor-area rows had carried the
  dwellings label).
- `eurostat_eu27_pop_prices_rents.csv` (v1.2): all 27 Member States and the EU-27 aggregate, long format with the
  Eurostat status flag of every value and the query URL: demo_gind (population on 1 January, 2015 and 2025),
  tipsho10 (deflated house price index, I15_A_AVG, 2015 and 2025), prc_hicp_aind (HICP actual rentals CP041,
  INX_A_AVG, 2015 and 2025), prc_hpi_q (house prices, all dwellings, annual rate of change, 2025-Q2 to 2026-Q2) and
  prc_hpi_cow (country weights in the EU-27 house price index, 2025). Written by `tools/cc-013-report/fetch_eu27.py`
  (retrieved 5 Oct 2026). A separate file so that `eurostat_housing.csv`, also read by CC-018, is unchanged.
- `pa_approved_dwellings.csv`: Planning Authority, Approved Dwelling Units 2007-2025, read 3 Oct 2026.
- `census2021_dwellings.csv`: NSO Census 2021, vol. 2, dwelling stock and occupancy.
- `checks.csv`: written by `tools/cc-013-report/calc.py`.
