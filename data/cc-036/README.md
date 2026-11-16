# data/cc-036

- `eea_mt_pm_annual.csv`: annual mean PM10 and PM2.5 at Malta's monitoring stations, from the EEA Air Quality Statistics
  table (discodata; query URL in each row), retrieved 16 Nov 2026. `verification` 1 = verified, 3 = preliminary (up-to-date
  data); `coverage_ok` is the EEA's own data-coverage filter. calc.py uses verified rows with `coverage_ok` = Yes.
- `vella2005_size_fractions.csv`: share of deposited quarry dust below 10 µm, typed from Tables 2 and 3 of Vella & Camilleri
  (2005), Xjenza 10:47-54 (University of Malta repository PDF, read 16 Nov 2026) - the study ERA cites for this passage.
- `epa_isa2019_coarse.csv`: the US EPA's causality determinations for PM10-2.5 and PM2.5 (Integrated Science Assessment for
  Particulate Matter, Dec 2019, Table ES-1), typed 16 Nov 2026 (only outcomes where PM10-2.5 is above 'Inadequate' plus
  long-term respiratory).
- `checks.csv`: outputs of tools/cc-036-report/calc.py.
