# Claim Check 011: analysis, report and flyer generators

Uses the shared design in `tools/mizien_report.py` (same look as CC-001).

```
pip install reportlab matplotlib pillow pyyaml numpy scipy rasterio shapely pyproj   # plus poppler-utils
python green_access.py   # downloads WorldPop + OSM into cache/ (git-ignored) -> data/cc-011/green_access_results.csv
python gozo_calc.py      # -> data/cc-011/gozo_net_zero_arithmetic.csv
python figures.py        # out/fig1_green_access.png, out/fig2_gozo_forest.png
python build_report.py   # out/report.pdf
python build_flyer.py    # out/flyer.pdf, out/flyer.png
```

`green.overpass` is the OpenStreetMap query. Re-running later will use newer OSM data and give slightly different
results; the committed CSV records the OSM timestamp used (2 Oct 2026). Copy the outputs to `claims/CC-011/`.
