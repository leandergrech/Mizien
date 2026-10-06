# Claim Check 094: report and flyer generators

Uses the shared design in `tools/mizien_report.py` (same look as CC-001).

```
pip install reportlab matplotlib pillow pyyaml openpyxl   # plus poppler-utils for the PNG
python fetch.py          # (network) EEA effort-sharing emissions, 2025 projections, NECPR table -> data/cc-094/
python calc.py           # recompute every figure -> data/cc-094/checks.csv
python figures.py        # out/fig1_path.png, fig2_gaps.png, fig3_sectors.png, fig4_ledger.png
python build_report.py   # out/report.pdf
python build_flyer.py    # out/flyer.pdf, out/flyer.png
```

Inputs: `data/cc-094/eea_esr_emissions.csv`, `eea_ghg_projections_esr.csv`, `eea_necpr2025_table2_malta.csv` (EEA
datastore, retrieved 6 Oct 2026 by `fetch.py`; raw files go to `out/raw/`, git-ignored); `esr_legal_inputs.csv`
(2005 levels, targets, Malta's allocations and flexibilities, typed from the regulations and implementing decisions,
read via the EU Publications Office); `com2025_668_statements.csv` (the figures the Commission states, printed page
numbers). Reused from CC-003: `data/cc-003/capr2025_esr_malta.csv` (Commission SWD Tables 25-26) and
`data/cc-003/eurostat_ghg_population.csv` (Eurostat population). Copy `out/report.pdf`, `flyer.pdf`, `flyer.png` to
`claims/CC-094/`.
