# data/cc-158

- `components.csv`: the 19 ClimateScanner components as scored by the National Audit Office, typed from the Appendix of
  *A review of Malta's climate action using the ClimateScanner framework* (NAO, October 2025; PDF pages 38-73), read
  16 Nov 2026 from the maintainer's copy (sha256 in archive/manifest.csv). Item counts per tier were taken from the
  Appendix tables; each component's score is recomputed from them in `tools/cc-158-report/calc.py`.
- Tier values (0, 3.33, 6.66, 10) and the 6.66 / 3.33 thresholds: INTOSAI ClimateScanner Handbook (May 2024), p. 11,
  and the NAO report Table 1 (PDF p. 14).
- Emissions outcomes are not re-downloaded: `calc.py` reads the files saved for CC-094 (`data/cc-094/eea_esr_emissions.csv`,
  EEA, retrieved 6 Oct 2026; `data/cc-094/esr_legal_inputs.csv`, EU legal texts read 6 Oct 2026) and CC-025
  (`data/cc-025/eurostat_gdp_ghg_pop.csv`, Eurostat env_air_gge, retrieved 5 Oct 2026).
- `checks.csv`: outputs of calc.py.
