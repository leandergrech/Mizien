# Claim Check 051: report and flyer generators

```
python fetch_data.py     # EEA Natura 2000 -> data/cc-051/natura2000_marine.csv (network; shapely, pyproj)
python calc.py           # -> data/cc-051/checks.csv
python figures.py        # out/fig1_map.png, out/fig2_denominators.png (network)
python build_report.py   # out/report.pdf
python build_flyer.py    # out/flyer.pdf, out/flyer.png
```
