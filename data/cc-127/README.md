# CC-127 data

All files are filtered copies of Eurostat datasets fetched by `tools/cc-127-report/fetch_data.py` on 21 October 2026
(API https://ec.europa.eu/eurostat/api/dissemination/). Status flags are kept where Eurostat gives them.

- `organic_share_pc_uaa.csv`: sdg_02_40, share of utilised agricultural area under organic farming (fully converted plus in conversion), EU-27 countries and the EU-27 aggregate, 2012-2024. Austria is absent from 2021 and Greece from 2022; the EU-27 aggregate stops at 2020 (estimate, flag e).
- `organic_area_ha.csv`: org_cropar, organic area in hectares (all crops, UAAXK0000) by production method (TOTAL, FCONV fully converted, UCONV in conversion).
- `uaa_malta_ef_lus_main.csv`: ef_lus_main, utilised agricultural area of Malta from farm-structure surveys (all farm types and sizes), hectares.
- `land_area_malta_km2.csv`: demo_r_d3area, total land area of Malta (last year 2015).
- `ranking_2022.csv`, `checks.csv`: output of `tools/cc-127-report/calc.py`.

The Commission statement itself is SWD(2026) 702 final (PDF pp. 5, 11, 29), read in the Austrian Parliament's copy.
