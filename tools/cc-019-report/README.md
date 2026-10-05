# Claim Check 019: report and flyer generators

Uses the shared design in `tools/mizien_report.py` (same look as CC-001).

```
pip install reportlab matplotlib pillow pyyaml numpy scipy rasterio pyproj shapely   # plus poppler-utils for the PNG
python fetch_data.py     # Impact Observatory land cover 2017-2023 -> data/cc-019/ (network)
python crosscheck.py     # v1.2: Amphora's polygons, IO 2017-2025 (Esri), overlap, CORINE -> data/cc-019/ (network)
python spotcheck.py      # v1.2: PPS sample of Amphora's polygons vs Esri Wayback imagery -> data/cc-019/ (network)
python calc.py           # recompute every figure -> data/cc-019/checks.csv
python figures.py        # out/fig1_overlap.png, out/fig2_estimates.png (needs crosscheck.py's out/ files)
python build_report.py   # out/report.pdf
python build_flyer.py    # out/flyer.pdf, out/flyer.png
```

Copy `out/report.pdf`, `flyer.pdf`, `flyer.png` to `claims/CC-019/`.

Amphora's GeoJSON is downloaded to `out/` and never committed (no licence stated); its SHA-256 is in
`data/cc-019/amphora_record.csv`.

`spotcheck.py` (maintainer decision, 5 Oct 2026) draws 40 points on Amphora's area (systematic PPS, seed 20261005),
finds the Wayback imagery versions for each sampled polygon and their acquisition dates, and saves before / Sep 2018 /
2023 / latest strips with the outline to `out/spotcheck/` (never committed: Esri imagery is not redistributed). The
classes are entered by eye in the script's `CLASS` table after looking at every strip; the script then writes
`data/cc-019/imagery_spotcheck.csv` and `imagery_spotcheck_summary.csv`.
