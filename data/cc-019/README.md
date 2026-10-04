# CC-019 data

- `amphora_figures.csv`: the figures in Amphora Media's 'Green to Grey' articles (11 and 12 Sep 2026; print copies
  supplied by the maintainer, kept locally in `literature/CC-019/`).
- `io_lulc_areas.csv`, `io_lulc_change.csv`, `new_built_strict.csv`: written by `tools/cc-019-report/fetch_data.py`
  from Impact Observatory / Esri 10 m annual land cover v2 (2017-2023, Microsoft Planetary Computer; retrieved
  4 Oct 2026). New built-up land is counted only where pixels change consistently across years (see the script);
  reverse changes gauge the noise.
- `checks.csv`: written by `tools/cc-019-report/calc.py`.
