# CC-147 report generators

```
pip install reportlab matplotlib pillow pyyaml   # plus poppler-utils for the PNG
python fetch.py          # (network) Eurostat extracts -> data/cc-147/eurostat_aea.csv
python calc.py           # recompute every figure -> data/cc-147/checks.csv
python figures.py        # out/fig1_air_share.png, out/fig2_intensity.png
python build_report.py   # out/report.pdf
python build_flyer.py    # out/flyer.pdf, out/flyer.png
```
Copy `out/report.pdf`, `flyer.pdf`, `flyer.png` to `claims/CC-147/`. Uses the shared design in `tools/mizien_report.py`.
