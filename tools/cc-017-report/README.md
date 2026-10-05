# Claim Check 017: report and flyer generators

Uses the shared design in `tools/mizien_report.py` (same look as CC-001).

```
pip install reportlab matplotlib pillow pyyaml numpy scipy rasterio pyproj shapely   # plus poppler-utils for the PNG
python fetch_data.py     # Sentinel-2 and EEA Natura 2000 -> data/cc-017/ (network)
python distances.py      # distances from the Terminal 2 reclamation to Natura 2000 sites (network; v1.1)
python fetch_bay.py      # v1.2: bay map data: Natura 2000, seagrass, depth, Article 17 -> data/cc-017/, out/ (network)
                         #   (--stats: recompute data/cc-017/bay_stats.csv offline from the committed files and out/)
python s2_bay.py         # v1.2 method test (MNDWI bay-wide); not robust, not used for findings (network)
python calc.py           # recompute every figure -> data/cc-017/checks.csv
python figures.py        # out/fig1_terminal2.png, out/fig2_natura.png, out/fig3_bay.png (fig3 needs fetch_bay.py's out/)
python build_report.py   # out/report.pdf
python build_flyer.py    # out/flyer.pdf, out/flyer.png
```

Copy `out/report.pdf`, `flyer.pdf`, `flyer.png` to `claims/CC-017/`.

Seagrass comes from EMODnet Seabed Habitats only (CC BY 4.0; maintainer decision, 5 Oct 2026); Figure 3 carries the
attribution EMODnet asks for. The EMODnet depth grid stays in `out/`.
