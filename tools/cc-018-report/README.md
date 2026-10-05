# Claim Check 018: report and flyer generators

Uses the shared design in `tools/mizien_report.py` (same look as CC-001).

```
python fetch_data.py     # Eurostat tipsho60 -> data/cc-018/ (network)
python fetch_more.py     # v1.2: Eurostat GDP per head, house prices, household income -> data/cc-018/eurostat_more.csv
python fetch_cycles.py   # v1.2: IMF consultation cycles of the EU members -> data/cc-018/imf_consultation_cycles.csv (slow)
python calc.py           # recompute every figure -> data/cc-018/checks.csv
python figures.py        # out/fig1_price_income.png, out/fig2_bank_exposure.png, out/fig3_prices_incomes.png
python build_report.py   # out/report.pdf
python build_flyer.py    # out/flyer.pdf, out/flyer.png
```

`python figures.py fig3` draws only Figure 3; `python tools/restore_figures.py CC-018` restores the published
Figures 1 and 2 from `claims/CC-018/report.pdf`.

Inputs: `data/cc-018/` (IMF Country Report 26/29 extracts, Eurostat, IMF consultation cycles) and
`data/cc-013/eurostat_housing.csv`. Copy `out/report.pdf`, `flyer.pdf`, `flyer.png` to `claims/CC-018/`.
