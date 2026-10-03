# Claim Check 017: report and flyer generators

Uses the shared design in `tools/mizien_report.py` (same look as CC-001).

```
pip install reportlab matplotlib pillow pyyaml numpy rasterio pyproj shapely   # plus poppler-utils for the PNG
python fetch_data.py     # Sentinel-2 and EEA Natura 2000 -> data/cc-017/ (network)
python calc.py           # recompute every figure -> data/cc-017/checks.csv
python figures.py        # out/fig1_terminal2.png, out/fig2_natura.png
python build_report.py   # out/report.pdf
python build_flyer.py    # out/flyer.pdf, out/flyer.png
```

Copy `out/report.pdf`, `flyer.pdf`, `flyer.png` to `claims/CC-017/`.
