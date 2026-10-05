# Claim Check 014: report and flyer generators

Uses the shared design in `tools/mizien_report.py` (same look as CC-001).

```
pip install reportlab matplotlib pillow pyyaml   # plus poppler-utils for the PNG
python calc.py           # recompute every figure -> data/cc-014/checks.csv
python figures.py        # out/fig1_series.png, out/fig2_outcomes_by_year.png, out/fig3_ratio.png
python build_report.py   # out/report.pdf
python build_flyer.py    # out/flyer.pdf, out/flyer.png
```

Inputs: `data/cc-014/pa_enforcement_series.csv` (MEPA annual reports read 3 Oct 2026; Planning Authority annual
reports 2017-2023 read 5 Oct 2026 as Issuu page images; PA Annual Report 2024) and
`data/cc-014/pa_annual_reports_2017_2023.csv` (every value with page, image URL and SHA-256). `calc.py` also writes
`data/cc-014/outcomes_by_year.csv` for Figure 2. Copy `out/report.pdf`, `flyer.pdf`, `flyer.png` to `claims/CC-014/`.
