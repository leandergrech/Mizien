# Claim Check 013: report and flyer generators

Uses the shared design in `tools/mizien_report.py` (same look as CC-001).

```
pip install reportlab matplotlib pillow pyyaml   # plus poppler-utils for the PNG
python calc.py           # recompute every figure -> data/cc-013/checks.csv
python figures.py        # out/fig1_permits_prices.png, out/fig2_affordability.png
python build_report.py   # out/report.pdf
python build_flyer.py    # out/flyer.pdf, out/flyer.png
```

Inputs: `data/cc-013/` (Eurostat API, PA approved dwellings, NSO Census 2021; retrieved 3 Oct 2026).
Copy `out/report.pdf`, `flyer.pdf`, `flyer.png` to `claims/CC-013/`.
