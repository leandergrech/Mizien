# Claim Check 062: report and flyer generators

Uses the shared design in `tools/mizien_report.py`.

```
pip install reportlab matplotlib pillow pyyaml numpy   # plus poppler-utils for the PNG
python calc.py           # recompute every figure -> data/cc-062/checks.csv
python figures.py        # out/fig1_steps.png, out/fig2_series.png
python build_report.py   # out/report.pdf
python build_flyer.py    # out/flyer.pdf, out/flyer.png
```

Inputs: `data/cc-062/` (KPMG tables transcribed with page numbers; Eurostat nama_10_a64 and naio_10_cp1750 for
Malta, retrieved 8 Oct 2026). Copy `out/report.pdf`, `flyer.pdf`, `flyer.png` to `claims/CC-062/`.
