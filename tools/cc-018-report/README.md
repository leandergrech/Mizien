# Claim Check 018: report and flyer generators

Uses the shared design in `tools/mizien_report.py` (same look as CC-001).

```
python fetch_data.py     # Eurostat tipsho60 -> data/cc-018/ (network)
python calc.py           # recompute every figure -> data/cc-018/checks.csv
python figures.py        # out/fig1_price_income.png, out/fig2_bank_exposure.png
python build_report.py   # out/report.pdf
python build_flyer.py    # out/flyer.pdf, out/flyer.png
```

Inputs: `data/cc-018/` (IMF Country Report 26/29 extracts, Eurostat) and `data/cc-013/eurostat_housing.csv`.
Copy `out/report.pdf`, `flyer.pdf`, `flyer.png` to `claims/CC-018/`.
