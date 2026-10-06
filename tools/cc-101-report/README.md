# Claim Check 101: report and flyer generators

Uses the shared design in `tools/mizien_report.py` (same look as CC-001).

```
pip install reportlab matplotlib pillow pyyaml   # plus poppler-utils (pdftotext, pdftoppm)
python fetch.py          # Eurostat env_wat_abs, EEA WISE 2022 water bodies, pressures and groundwater status, legislation.mt checks -> data/cc-101/
python calc.py           # recompute every figure -> data/cc-101/checks.csv
python figures.py        # out/fig1_abstraction.png, out/fig2_timeline.png
python build_report.py   # out/report.pdf
python build_flyer.py    # out/flyer.pdf, out/flyer.png
```

`python fetch.py notices` reads the title of every 2024–2026 Legal Notice in legislation.mt's ELI sitemap (about 940
pages, four at a time); it keeps a cache in `out/ln_cache.json`, so an interrupted run resumes. `python fetch.py acts`
does the same for every 2024–2026 Act (title, plus counts of "groundwater", "abstract" and "borehole" in its text) and
probes the next six numbers in each year; `python fetch.py sl_titles` reads the titles of the S.L. 549, 423, 545, 355 and
427 instruments.

Inputs: `data/cc-101/` (Eurostat with its `flag` column: e estimated, b break in series; WISE retrievals with their
query URLs; legislation.mt instrument hashes and Legal Notice titles; `document_facts.csv` for figures and dates
transcribed from the documents, each with page and URL; `wise_2022_groundwater_status.csv` for groundwater-body status).
Copy `out/report.pdf`, `flyer.pdf`, `flyer.png` to `claims/CC-101/`.
