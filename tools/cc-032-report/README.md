# Claim Check 032: report and flyer generators

Uses the shared design in `tools/mizien_report.py` (same look as CC-001).

```
pip install reportlab matplotlib pillow pyyaml   # plus poppler-utils for the PNG
python fetch.py          # PVGIS 5.3 runs (two-axis and optimal fixed) and OSRM route lengths -> data/cc-032/
python calc.py           # recompute every figure -> data/cc-032/checks.csv
python figures.py        # out/fig1_timeline.png, out/fig2_output.png
python build_report.py   # out/report.pdf
python build_flyer.py    # out/flyer.pdf, out/flyer.png
```

Inputs: `data/cc-032/inputs.csv` (transcribed, each with source and retrieval date), `european_records.csv` (dated
records of SmartFlowers in Europe), `pvgis_*.json` and `pvgis_monthly.csv` (PVGIS 5.3, retrieved 6 Oct 2026),
`route_osrm.csv` (OpenStreetMap via OSRM). Copy `out/report.pdf`, `flyer.pdf`, `flyer.png` to `claims/CC-032/`.
