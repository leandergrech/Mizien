# Claim Check 095: report and flyer generators

Uses the shared design in `tools/mizien_report.py` (same look as CC-001).

```
pip install reportlab matplotlib pillow pyyaml openpyxl   # plus poppler-utils for the PNG
python fetch.py          # Eurostat HICP (prc_hicp_minr), electricity prices (nrg_pc_204, nrg_pc_205), COFOG 04.3
                         # (gov_10a_exp), GDP; the Weekly Oil Bulletin history -> data/cc-095/ (raw files in out/raw/,
                         # hashes in raw_files_sha256.csv)
python calc.py           # every number in the report -> data/cc-095/checks.csv, cost_series.csv
python figures.py        # out/fig1_prices.png, fig2_energy_inflation.png, fig3_costs.png
python build_report.py   # out/report.pdf
python build_flyer.py    # out/flyer.pdf, out/flyer.png
```

`data/cc-095/statements_and_estimates.csv` is typed by hand from the sources it names: the outlets' reports of the
minister's figures (30 Sep 2026) and the Malta Fiscal Advisory Council's and the Commission's documents, each row with
its page or paragraph and URL. `calc.py` also reads, without copying, `data/cc-113/other_estimates_transcribed.csv`
(Draft Budgetary Plans 2024 and 2025; IMF CR 26/29) and `data/cc-113/ec_inventory_malta_facts.csv` (the Commission
database's 2023 entries for Malta; Enerdata copyright, five figures only).

Copy `out/report.pdf`, `flyer.pdf`, `flyer.png` to `claims/CC-095/`, then run `python tools/report_html.py CC-095`
(must print "ok") before `python scripts/build_site_data.py`.
