# Claim Check 022: report and flyer generators

```
python fetch_data.py     # Eurostat prices and energy poverty -> data/cc-022/ (network)
python fetch_burden.py   # v1.2: income, use, households, spending -> data/cc-022/eurostat_burden_inputs.csv (network)
python calc.py           # -> data/cc-022/checks.csv and burden_measures.csv (via burden.py)
python figures.py        # out/fig1_ranking.png, fig2_price_subsidy.png, fig3_bands.png, fig4_burden.png
python build_report.py   # out/report.pdf
python build_flyer.py    # out/flyer.pdf, out/flyer.png
```

Inputs: `data/cc-022/` (Eurostat; IMF CR 26/29 Table 2). Copy `out/report.pdf`, `flyer.pdf`, `flyer.png` to `claims/CC-022/`.
