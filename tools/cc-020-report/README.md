# Claim Check 020: report and flyer generators

Uses the shared design in `tools/mizien_report.py` (same look as CC-001).

```
pip install reportlab matplotlib pillow pyyaml   # plus poppler-utils for the PNG
python calc.py           # recompute every figure -> data/cc-020/checks.csv
python figures.py        # out/fig1_noise_trend.png, fig2_noise_rank.png, fig3_thresholds.png
python build_report.py   # out/report.pdf
python build_flyer.py    # out/flyer.pdf, out/flyer.png
```

Inputs: `data/cc-020/` (Eurostat API ilc_mddw01; figures read from the EP study PE 783.089; retrieved 5 Oct 2026).
Copy `out/report.pdf`, `flyer.pdf`, `flyer.png` to `claims/CC-020/`.
