# Claim Check 019: report and flyer generators

Uses the shared design in `tools/mizien_report.py` (same look as CC-001).

```
pip install reportlab matplotlib pillow pyyaml numpy rasterio pyproj   # plus poppler-utils for the PNG
python fetch_data.py     # Impact Observatory land cover 2017-2023 -> data/cc-019/ (network)
python calc.py           # recompute every figure -> data/cc-019/checks.csv
python figures.py        # out/fig1_map.png, out/fig2_estimates.png
python build_report.py   # out/report.pdf
python build_flyer.py    # out/flyer.pdf, out/flyer.png
```

Copy `out/report.pdf`, `flyer.pdf`, `flyer.png` to `claims/CC-019/`.
