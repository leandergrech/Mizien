# Claim Check 113: report and flyer generators

Uses the shared design in `tools/mizien_report.py` (same look as CC-001).

```
pip install reportlab matplotlib pillow pyyaml openpyxl   # plus poppler-utils for the PNG
python fetch.py          # EEA pages and chart data, the Commission subsidy database (CIRCABC REST download, SHA-256
                         # checked), Eurostat, IMF and OECD/IISD data -> data/cc-113/ (raw files in out/raw/, hashes
                         # in raw_files_sha256.csv). The workbook is (c) Enerdata: only country aggregates and the
                         # five Malta figures in the report are written to data/; the measure rows go to out/ (ignored)
python measure_fig16.py  # read COM(2025) 17 Figure 16 (28 Jan 2025) by pixel -> data/cc-113/com2025_17_fig16_measured.csv
python calc.py           # rebuild the 2023 shares four ways -> data/cc-113/checks.csv, shares_2023_variants.csv
python figures.py        # out/fig1_rank.png, fig2_measures.png
python build_report.py   # out/report.pdf
python build_flyer.py    # out/flyer.pdf, out/flyer.png
```

`data/cc-113/other_estimates_transcribed.csv` is typed by hand from documents (Malta's Draft Budgetary Plans 2024 and
2025, IMF CR 26/29 Table 2 as recorded for CC-022, COM(2026) 472 Figure 15 read from the chart), each row with its
page and URL. Copy `out/report.pdf`, `flyer.pdf`, `flyer.png` to `claims/CC-113/`.
