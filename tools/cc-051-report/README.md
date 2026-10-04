# Claim Check 051: report and flyer generators

```
python fetch_data.py     # EEA Natura 2000, Marine Regions, EEA marine waters -> data/cc-051/natura2000_marine.csv,
                         #   data/cc-051/boundaries.geojson; EMODnet depth grid -> out/bathymetry.tif (network)
python calc.py           # -> data/cc-051/checks.csv, data/cc-051/depth_bands.csv (needs out/bathymetry.tif)
python figures.py        # out/fig1_map.png, fig2_wide_map.png, fig3_three_areas.png, fig4_depth.png
python build_report.py   # out/report.pdf
python build_flyer.py    # out/flyer.pdf, out/flyer.png
```
