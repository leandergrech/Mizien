# Claim Check 004: report and flyer generators

Uses the shared design in `tools/mizien_report.py` (same look as CC-001).

```
pip install reportlab matplotlib pillow pyyaml   # plus poppler-utils for the PNG
python calc.py           # recompute every figure -> data/cc-004/checks.csv
python figures.py        # out/fig1_recycling_rate.png, out/fig2_routes.png
python build_report.py   # out/report.pdf
python build_flyer.py    # out/flyer.pdf, out/flyer.png
```

Inputs: `data/cc-004/eurostat_municipal_waste.csv` (Eurostat API, retrieved
2 Oct 2026; query URLs are in the files). Copy `out/report.pdf`, `flyer.pdf`, `flyer.png` to `claims/CC-004/`.
