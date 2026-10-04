# CC-051 data

- `natura2000_marine.csv`: Maltese Natura 2000 sites (EEA 2024 release, discomap service) with area and sea area (km2,
  UTM 33N), and the dissolved union of the 18 sites with sea; written by `tools/cc-051-report/fetch_data.py` (4 Oct 2026).
  Land removed with the OpenStreetMap island outlines in `docs/data/geo.json`.
- `reference_areas.csv`: the reference areas ("denominators") used by different sources.
- `checks.csv`: written by `tools/cc-051-report/calc.py`.
