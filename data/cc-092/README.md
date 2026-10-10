# CC-092 data

Written by `tools/cc-092-report/fetch.py` (network), `search_programme.py` (network) and `calc.py` (offline), or
transcribed by hand from a source read in full. Retrieved or transcribed 10 Oct 2026 unless stated.

| File | What | Source |
|---|---|---|
| `eurostat_extract.csv` | Malta inventory total excl. LULUCF, LULUCF and forest land (kt CO2e); population of Malta and MT002; area of MT002; Malta's forest area (FAO); WEI+ for Malta and the EU, with flags and update dates | Eurostat API (env_air_gge, demo_r_pjangrp3, reg_area3, for_area, sdg_06_60) |
| `clc2018_gozo_polygons.csv` | CORINE Land Cover 2018 polygons in a box around Gozo: code, area (ha), extent | EEA map service CLC2018_WM, layer 0 |
| `nasa_power_gozo.json`, `nasa_power_yatir.json` | 1991-2020 climatology of rainfall (mm a day) and temperature | NASA POWER API (MERRA-2) |
| `gozo_energy_baseline_table16.csv` | Gozo's energy-related CO2 by sector, 2016-2020 (hand-transcribed) | Energy Baseline Scenario for Gozo (2023), Table 16, PDF p. 25 |
| `sequestration_rates.csv` | Low, central, high and sensitivity rates, with pools, period and grade (hand-transcribed) | Renna et al. 2024; Grünzweig et al. 2007; Bernal et al. 2018 (see literature/CC-092/references.bib) |
| `planting_inputs.csv` | Planting density, 20-year survival, Malta's recent planting count (hand-transcribed) | Grünzweig et al. 2007; Oliet et al. 2023; PQ 34270 via Claim Check 010 |
| `pn_programme_search.csv` | Search log: SHA-256 and term counts for the 16 web chapters and 16 PDFs of the PN programme | pn.org.mt (documents not committed) |
| `afforestation_offset.csv` | Forest needed and share offset for every emissions case and rate (calc.py) | derived |
| `checks.csv` | Every figure used in the report (calc.py; feeds data/facts.csv) | derived |

Gozo has no official greenhouse-gas inventory; the 2023 baseline is a study for the EU islands secretariat (energy only),
and the population-share figure is Malta's inventory scaled by population, not Gozo data.
