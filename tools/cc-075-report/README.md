# Claim Check 075: report and flyer generators

Uses the shared design in `tools/mizien_report.py` (same look as CC-001).

```
pip install reportlab matplotlib pillow pyyaml   # plus poppler-utils for the PNG
python fetch.py          # download Eurostat road_eqs_carhab, road_eqs_carmot, demo_gind, reg_area3 (with flags) -> data/cc-075/
python calc.py           # recompute every figure -> data/cc-075/checks.csv
python figures.py        # out/fig1_trend.png, fig2_rank2022.png, fig3_growth.png, fig4_density.png
python build_report.py   # out/report.pdf
python build_flyer.py    # out/flyer.pdf, out/flyer.png
```

Inputs: the four Eurostat files in `data/cc-075/` (API, retrieved 6 Oct 2026; the `flag` column holds Eurostat's
observation status, labels in `data/cc-075/README.md`) and `data/cc-075/reported_values.csv` (figures stated in the
texts we read: the Lovin Malta article, Eurostat's release of 17 Jan 2024 and Statistics Explained articles, and
second-hand NSO figures, marked as such).
Copy `out/report.pdf`, `flyer.pdf`, `flyer.png` to `claims/CC-075/`.
