# Claim Check 075: report and flyer generators

Uses the shared design in `tools/mizien_report.py` (same look as CC-001).

```
pip install reportlab matplotlib pillow pyyaml   # plus poppler-utils for the PNG
python fetch.py          # Eurostat road_eqs_carhab, road_eqs_carmot, demo_gind, reg_area3 (with flags) -> data/cc-075/
python fetch_vintage.py  # what Eurostat had published earlier: Statistics Explained revisions 627098 and 647912 (MediaWiki
                         # API), their Figure 3 charts, the 17 Jan 2024 release chart -> data/cc-075/ (vintage_sources.csv)
python read_charts.py    # read the three charts by pixel measurement -> data/cc-075/chart_reads.csv
python calc.py           # recompute every figure -> data/cc-075/checks.csv
python figures.py        # out/fig1_trend.png, fig2_rank2022.png, fig5_published2023.png
python build_report.py   # out/report.pdf
python build_flyer.py    # out/flyer.pdf, out/flyer.png
```

Inputs are described in `data/cc-075/README.md`. `reported_values.csv` holds figures stated in texts and tables we read
(the Lovin Malta article, Eurostat's releases and Statistics Explained revisions, and second-hand NSO figures, marked).
The report's status line names the body asked for a reply (`status_note`, maintainer session of 6 Oct 2026).
Copy `out/report.pdf`, `flyer.pdf`, `flyer.png` to `claims/CC-075/`.
