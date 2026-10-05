# Claim Check 019: report and flyer generators

Uses the shared design in `tools/mizien_report.py` (same look as CC-001).

```
pip install reportlab matplotlib pillow pyyaml numpy scipy rasterio pyproj shapely   # plus poppler-utils for the PNG
python fetch_data.py     # Impact Observatory land cover 2017-2023 -> data/cc-019/ (network)
python crosscheck.py     # v1.2: Amphora's polygons, IO 2017-2025 (Esri), overlap, CORINE -> data/cc-019/ (network)
python calc.py           # recompute every figure -> data/cc-019/checks.csv
python figures.py        # out/fig1_overlap.png, out/fig2_estimates.png (needs crosscheck.py's out/ files)
python build_report.py   # out/report.pdf
python build_flyer.py    # out/flyer.pdf, out/flyer.png
```

Copy `out/report.pdf`, `flyer.pdf`, `flyer.png` to `claims/CC-019/`.

Amphora's GeoJSON is downloaded to `out/` and never committed (no licence stated); its SHA-256 is in
`data/cc-019/amphora_record.csv`.
