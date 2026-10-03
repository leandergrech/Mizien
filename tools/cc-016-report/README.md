# Claim Check 016: report and flyer generators

Uses the shared design in `tools/mizien_report.py` (same look as CC-001).

```
pip install reportlab matplotlib pillow pyyaml   # plus poppler-utils for the PNG
python calc.py           # recompute every figure -> data/cc-016/checks.csv
python figures.py        # out/fig1_uptake.png, out/fig2_calls.png
python build_report.py   # out/report.pdf
python build_flyer.py    # out/flyer.pdf, out/flyer.png
```

Inputs: `data/cc-016/` (Infrastructure Malta, Valletta Cruise Port, Amphora Media analysis of Transport Malta FOI records; read 3 Oct 2026).
Copy `out/report.pdf`, `flyer.pdf`, `flyer.png` to `claims/CC-016/`.
