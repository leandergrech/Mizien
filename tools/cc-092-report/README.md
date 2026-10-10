# Claim Check 092: report and flyer generators

Afforestation in the PN's 2026 pledge of a net-zero Gozo, and the reported indigenous-tree strategy. Uses the shared
design in `tools/mizien_report.py`. The net-zero plan itself is Claim Check 107.

```
python fetch.py              # network: Eurostat, CORINE 2018 (EEA), NASA POWER -> data/cc-092/
python search_programme.py   # network: PN programme search log -> data/cc-092/pn_programme_search.csv
python natura.py             # network: Gozo land inside Natura 2000 sites -> data/cc-092/natura2000_overlap.csv
python calc.py               # offline -> data/cc-092/afforestation_offset.csv, checks.csv
python figures.py            # out/fig1_rates.png, fig2_forest_needed.png, fig3_land_offset.png
python build_report.py       # out/report.pdf
python build_flyer.py        # out/flyer.pdf, out/flyer.png
```

Copy the outputs to `claims/CC-092/`. Hand-transcribed inputs (Table 16, literature rates, planting inputs) are in
`data/cc-092/` with their sources.
