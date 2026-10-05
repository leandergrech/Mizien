# CC-013 data

- `eurostat_housing.csv`: Eurostat prc_hpi_a (nominal house prices), tipsho10 (deflated), sts_cobp_a (permits for
  residential buildings with 2+ dwellings, index 2015=100, two series per year: number of dwellings, BPRM_DW, and
  m2 of useful floor area, BPRM_SQM; not used in the report), demo_gind (population), ilc_lvho07a (housing cost
  overburden), ilc_lvho05a (overcrowding); Malta and EU-27; retrieved 3 Oct 2026 from the Eurostat dissemination
  API. Status flags for ilc_lvho07a, tipsho10, prc_hpi_a and sts_cobp_a were checked on 5 Oct 2026 and are in the
  `note` column (e.g. Malta ilc_lvho07a 2023: b, break in time series; Malta tipsho10 and prc_hpi_a 2025: p,
  provisional). The sts_cobp_a item labels were corrected on 5 Oct 2026 (the floor-area rows had carried the
  dwellings label).
- `pa_approved_dwellings.csv`: Planning Authority, Approved Dwelling Units 2007-2025, read 3 Oct 2026.
- `census2021_dwellings.csv`: NSO Census 2021, vol. 2, dwelling stock and occupancy.
- `checks.csv`: written by `tools/cc-013-report/calc.py`.
