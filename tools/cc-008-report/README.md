# Claim Check 008 report and flyer

Uses the shared Miżien report design. Run from the repository root:

```sh
python tools/cc-008-report/fetch_data.py    # EEA hourly NO2 (network; needs pyarrow), ERA station metadata (Eionet CDR)
                                            #   and the Msida flyover from OpenStreetMap -> data/cc-008/
python tools/cc-008-report/calc.py          # -> data/cc-008/no2_jan_sep.csv, data/cc-008/checks.csv (offline)
python tools/cc-008-report/figures.py       # -> tools/cc-008-report/out/fig1_no2_monthly.png, fig2_jan_sep.png,
                                            #    fig3_map.png (offline; Malta outline from docs/data/geo.json)
python tools/cc-008-report/build_report.py
python tools/cc-008-report/build_flyer.py
```

Outputs are written to `claims/CC-008/`.
