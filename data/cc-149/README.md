# CC-149 data

- `nso_new_dwellings_quarterly.csv`: approved new dwellings by quarter, 2021 Q4 to 2025 Q4, from Table 1 of the NSO's
  Q4 news releases (NR 028/2023, NR 033/2024, NR 028/2025, NR 026/2026). The xlsx files refuse scripts; they were read in
  the built-in browser on 17 Nov 2026 (fetched from the nso.gov.mt page and unzipped in the page). Each Q4 release's
  Table 1 gives the four quarters of that year; 2024 Q4 is as revised in NR 026/2026 (same as NR 028/2025: 2,259).
- `annual_second_hand.csv`: 2018 and 2019 totals as reported in the press from NSO data. Second-hand: NSO releases
  before 2022 are not on the current NSO site.
- `checks.csv`: written by `tools/cc-149-report/calc.py`.

The Planning Authority dataset behind MaltaToday's ODZ, greenfield and conversion figures (2007-2025) was not read
(pa.org.mt shows a security check).
