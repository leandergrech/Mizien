# Claim Check 003: report and flyer generators

Uses the shared design in `tools/mizien_report.py` (same look as CC-001).

```
pip install reportlab matplotlib pillow pyyaml   # plus poppler-utils for the PNG
python calc.py           # recompute every figure -> data/cc-003/checks.csv
python figures.py        # out/fig1_index.png, out/fig2_sectors_esr.png
python build_report.py   # out/report.pdf
python build_flyer.py    # out/flyer.pdf, out/flyer.png
```

Inputs: `data/cc-003/eurostat_ghg_population.csv` and `eurostat_renewables_share.csv` (Eurostat API, retrieved
2 Oct 2026; query URLs are in the files). Copy `out/report.pdf`, `flyer.pdf`, `flyer.png` to `claims/CC-003/`.
