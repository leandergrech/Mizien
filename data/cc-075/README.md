# CC-075 data

Written by `tools/cc-075-report/fetch.py` (Eurostat dissemination API, JSON-stat flattened to CSV).
The `flag` column keeps Eurostat's observation status: b break in time series, i imputed by Eurostat or other receiving agencies, p provisional, e estimated, d definition differs, m missing (data cannot exist); combinations carry both meanings. `checks.csv` is written by `calc.py`.

| File | Dataset | API URL | Updated (Eurostat) | Retrieved | Rows |
|---|---|---|---|---|---|
| `eurostat_road_eqs_carhab.csv` | road_eqs_carhab: Passenger cars - per thousand inhabitants | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/road_eqs_carhab?format=JSON&lang=en | 2026-07-30T23:00:00+0200 | 2026-10-06 | 1294 |
| `eurostat_road_eqs_carmot.csv` | road_eqs_carmot: Passenger cars, by type of motor energy and size of engine | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/road_eqs_carmot?format=JSON&lang=en&mot_nrg=TOTAL&engine=TOTAL&unit=NR | 2026-09-01T23:00:00+0200 | 2026-10-06 | 1498 |
| `eurostat_demo_gind_jan.csv` | demo_gind: Population change - Demographic balance and crude rates at national level | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/demo_gind?format=JSON&lang=en&indic_de=JAN | 2026-09-30T23:00:00+0200 | 2026-10-06 | 1733 |
| `eurostat_reg_area3_land.csv` | reg_area3: Area by NUTS 3 region | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/reg_area3?format=JSON&lang=en&landuse=L0008&unit=KM2 | 2026-01-22T23:00:00+0100 | 2026-10-06 | 524 |
