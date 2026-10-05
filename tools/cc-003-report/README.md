# Claim Check 003: report and flyer generators

Uses the shared design in `tools/mizien_report.py` (same look as CC-001).

```
pip install reportlab matplotlib pillow pyyaml   # plus poppler-utils for the PNG
python fetch_eu27.py     # (network) all EU-27 emissions and population -> data/cc-003/eurostat_ghg_pop_eu27.csv
python calc.py           # recompute every figure -> data/cc-003/checks.csv
python figures.py        # out/fig1_index.png, fig2_sectors_esr.png, fig_rank.png, fig_path.png
python build_report.py   # out/report.pdf
python build_flyer.py    # out/flyer.pdf, out/flyer.png
```

Inputs: `data/cc-003/eurostat_ghg_population.csv` and `eurostat_renewables_share.csv` (Eurostat API, retrieved
2 Oct 2026; query URLs are in the files); `eurostat_ghg_pop_eu27.csv` (all 27 Member States, 2005 and 2024, with
status flags; retrieved 5 Oct 2026); `capr2025_esr_malta.csv` (Commission SWD Tables 25 and 26, typed, printed
page numbers). Copy `out/report.pdf`, `flyer.pdf`, `flyer.png` to `claims/CC-003/`.
