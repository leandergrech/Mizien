# Claim Check 022: report and flyer generators

```
python fetch_data.py     # Eurostat prices and energy poverty -> data/cc-022/ (network)
python calc.py           # -> data/cc-022/checks.csv
python figures.py        # out/fig1_ranking.png, out/fig2_price_subsidy.png
python build_report.py   # out/report.pdf
python build_flyer.py    # out/flyer.pdf, out/flyer.png
```

Inputs: `data/cc-022/` (Eurostat; IMF CR 26/29 Table 2). Copy `out/report.pdf`, `flyer.pdf`, `flyer.png` to `claims/CC-022/`.
