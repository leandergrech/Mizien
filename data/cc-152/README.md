# CC-152 data

- `era_napcp_table4.csv`: Table 4 (PDF p. 63) and Table 1 (p. 14) of ERA's draft *First Update of Malta's National Air
  Pollution Control Programme* (consultation 5 Jun-17 Jul 2026; maintainer's copy, 102 pp.): 2005 base, 2023
  emissions, 2020/2025/2030 ceilings and With Measures projections (kt), and the Annex II commitments (%). The NOx
  commitments (42% for 2020-2029, 79% from 2030) were checked against Directive (EU) 2016/2284, Annex II, Table A
  (EUR-Lex, read in a browser 17 Nov 2026).
- `eurostat_nox_malta.csv`: Malta's national total NOx, 2005-2024, Eurostat env_air_emis (NFR_TOT_NAT, updated 7 Sep
  2026, retrieved 17 Nov 2026). This later submission differs slightly from the draft programme's figures (2005: 9.62 vs
  9.45 kt; 2023: 4.44 vs 4.22 kt) because of inventory recalculations.
- `eurostat_nox_shares.csv`: road transport (NFR 1A3b1-b4) and national navigation (1A3dii) NOx, 2023-2024, same table.
- `checks.csv`: written by `tools/cc-152-report/calc.py`.
