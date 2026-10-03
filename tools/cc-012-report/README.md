# Claim Check 012: report and flyer generators

Uses the shared design in `tools/mizien_report.py` (same look as CC-001).


```
pip install reportlab matplotlib pillow pyyaml rasterio pyproj scipy   # plus poppler-utils for the PNG
python fetch_s2.py       # Sentinel-2 via Planetary Computer -> data/cc-012/ (network; ~10 min)
python calc.py           # -> data/cc-012/checks.csv
python figures.py        # out/fig1_map.png, out/fig2_timeseries.png
python build_report.py   # out/report.pdf
python build_flyer.py    # out/flyer.pdf, out/flyer.png
```

Rerun `fetch_s2.py` to update the record after any works on site. Copy outputs to `claims/CC-012/`.
