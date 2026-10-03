# Claim Check 014: report and flyer generators

Uses the shared design in `tools/mizien_report.py` (same look as CC-001).

```
pip install reportlab matplotlib pillow pyyaml   # plus poppler-utils for the PNG
python calc.py           # recompute every figure -> data/cc-014/checks.csv
python figures.py        # out/fig1_series.png, out/fig2_outcomes.png
python build_report.py   # out/report.pdf
python build_flyer.py    # out/flyer.pdf, out/flyer.png
```

Inputs: `data/cc-014/pa_enforcement_series.csv` (MEPA and Planning Authority annual reports read 3 Oct 2026, plus
news reports of PA data, marked second-hand). Copy `out/report.pdf`, `flyer.pdf`, `flyer.png` to `claims/CC-014/`.
