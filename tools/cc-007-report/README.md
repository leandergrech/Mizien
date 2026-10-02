# CC-007 report generator

Run from the repository root:

```sh
python tools/cc-007-report/calc.py
python tools/cc-007-report/figures.py
python tools/cc-007-report/build_report.py
python tools/cc-007-report/build_flyer.py
```

To refresh the partial cross-check against the EEA's validated PM2.5 daily aggregates, install the optional PyArrow dependency and run:

```sh
python -m pip install -r tools/cc-007-report/requirements-eea.txt
python tools/cc-007-report/eea_crosscheck.py
```

Inputs are transcribed from the primary PQ 29696 annex in `data/cc-007/station_pm25.csv`. The calculator writes the counts, range and station means to `data/cc-007/checks.csv`. The figure and PDFs are generated under the ignored `out/` directory; copy the report and flyer outputs to `claims/CC-007/`, then run `scripts/build_site_data.py` to publish the viewer copies under `docs/claim-files/`.

The data contain two `n/a` entries for St Paul's Bay. Do not interpolate them. The EEA cross-check covers only 11 of 25 station-years; ten match the annex to 0.1 µg/m³ and Attard 2024 differs. The 25 µg/m³ threshold applies to the 2020–2024 comparison; 10 µg/m³ is shown as the EU standard due by 2030, not as a past limit.
