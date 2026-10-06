# Claim Check 035: report and flyer generators

Uses the shared design in `tools/mizien_report.py` (same look as CC-001).

```
pip install reportlab matplotlib pillow pyyaml pyarrow   # plus poppler-utils for the PNG
python fetch.py          # EEA burden-of-disease table, Eurostat, EEA station files -> data/cc-035/
                         # (python fetch.py ebd | eurostat | stations to refresh one part)
python calc.py           # recompute every figure -> data/cc-035/checks.csv, station_vs_model.csv, eu27_rate_change.csv
python figures.py        # out/fig1_rate.png, fig2_measured.png, fig3_choices.png
python build_report.py   # out/report.pdf
python build_flyer.py    # out/flyer.pdf, out/flyer.png
```

Inputs (all retrieved 6 Oct 2026):
- `eea_ebd_malta_pm25.csv`, `eea_ebd_countries_pm25.csv`, `eea_ebd_eu27_pm25.csv`: the EEA's *Burden of disease of air
  pollution (Countries & NUTS)* table, exported through its Table publisher (column names are the export's labels; the
  `download_sha256` column hashes the zip as served, which changes with each export).
- `eurostat_*.csv`: Eurostat API extracts with the `flag` column (sdg_11_52, demo_pjan, demo_magec, hlth_cd_aro,
  env_air_emis).
- `eea_stations_malta_annual.csv`: annual means of valid days per station (a day from hourly data needs 18 valid
  hours); `eea_station_file_manifest.csv` lists every Parquet file with its SHA-256.

Copy `out/report.pdf`, `flyer.pdf`, `flyer.png` to `claims/CC-035/`.
