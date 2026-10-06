# Claim Check 099: report and flyer generators

Uses the shared design in `tools/mizien_report.py` (same look as CC-001).

```
pip install reportlab matplotlib pillow pyyaml openpyxl   # plus poppler-utils for the PNG, curl for Jobsplus
python fetch.py          # Eurostat (with flags) and Jobsplus workbooks -> data/cc-099/
python calc.py           # recompute every figure -> data/cc-099/checks.csv
python figures.py        # out/fig1_shares.png, out/fig2_locals.png
python build_report.py   # out/report.pdf
python build_flyer.py    # out/flyer.pdf, out/flyer.png
```

Inputs written by `fetch.py` (retrieved 6 Oct 2026): `eurostat_migr_pop1ctz.csv`, `eurostat_migr_pop3ctb.csv`,
`eurostat_demo_gind.csv`, `eurostat_proj_25np.csv`, `eurostat_census2021.csv`, `eurostat_migr_flows.csv`,
`eurostat_births_deaths_ctz.csv` (the `flag` column holds Eurostat's observation status: b break, e estimated),
`jobsplus_foreign_employment.csv`, `jobsplus_total_employment.csv` (jobsplus.gov.mt refuses Python's urllib, so the
workbooks are fetched with curl). Transcribed by hand with URLs: `pwc_release.csv` (the press release figures; report
figures as quoted by outlets marked ◆) and `nso_end2025_secondhand.csv` (the NSO's end-2025 figures as reported by news
outlets, ◆; nso.gov.mt returns 403).
Copy `out/report.pdf`, `flyer.pdf`, `flyer.png` to `claims/CC-099/`.
