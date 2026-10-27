# data/cc-135

- `nso_max_demand.csv`: NSO maximum electricity demand (MW). Monthly 2017-2021 from Table 7 of NR 177/2022 (Electricity
  Supply: 2021); for 2022-2025 the two highest months and the annual average from the text of NR 176/2023, NR 184/2024,
  NR 178/2025 and NR 178/2026. Transcribed via WebFetch on 26 Oct 2026 (nso.gov.mt refuses scripts); the release, URL
  and retrieval date are in each row. The release's 'annual average demand' is the mean of the twelve monthly maxima.
- `eurostat_pop_tourism_electricity.csv`: Eurostat demo_gind (population on 1 January, JAN; average population, AVG),
  tour_occ_nim (nights spent at tourist accommodation establishments, NACE I551-I553, all residences, monthly) and
  nrg_cb_e (electricity balance, GWh: GEP, IMP, EXP, FC, DL, NRG_E), Malta, with status flags, URL and retrieval date.
  Made by `tools/cc-135-report/fetch.py`.
- `ghcnd_luqa_monthly.csv`: NOAA GHCN-Daily station MT000016597 (Luqa), daily TAVG, TMAX and TMIN summarised to monthly
  means with day counts and the highest daily maximum. Made by `fetch.py`.
- `imf_statements.csv`: the figures the IMF paper states, with their place in the paper.
- `checks.csv`: every figure the report uses, from `tools/cc-135-report/calc.py`.
