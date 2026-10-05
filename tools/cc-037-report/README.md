# Claim Check 037: report and flyer generators

Uses the shared design in `tools/mizien_report.py` (same look as CC-001).

```
pip install reportlab matplotlib pillow pyyaml   # plus poppler-utils for the PNG
python fetch.py          # download Eurostat ilc_mddw02 and ilc_li02 (with flags) -> data/cc-037/
python calc.py           # recompute every figure -> data/cc-037/checks.csv
python figures.py        # out/fig1_trend.png, fig2_rank.png
python build_report.py   # out/report.pdf
python build_flyer.py    # out/flyer.pdf, out/flyer.png
```

Inputs: `data/cc-037/eurostat_ilc_mddw02.csv` and `eurostat_ilc_li02.csv` (Eurostat API, retrieved 5 Oct 2026; the
`flag` column holds Eurostat's observation status: e estimated, u low reliability, b break in series).
Copy `out/report.pdf`, `flyer.pdf`, `flyer.png` to `claims/CC-037/`.
