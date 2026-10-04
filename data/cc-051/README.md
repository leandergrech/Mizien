# CC-051 data

- `natura2000_marine.csv`: Maltese Natura 2000 sites (EEA 2024 release, discomap service) with area and sea area (km2,
  UTM 33N), and the dissolved union of the 18 sites with sea; written by `tools/cc-051-report/fetch_data.py` (4 Oct 2026).
  Land removed with the OpenStreetMap island outlines in `docs/data/geo.json`.
- `reference_areas.csv`: the reference areas ("denominators") used by different sources.
- `boundaries.geojson` (WGS84): the protected sea (union of the 18 sites), Malta's 12-nm territorial sea (Marine
  Regions v4, doi:10.14284/633), the 25-nm Fisheries Management Zone rebuilt from it (25 nm from the baselines; with
  and without internal waters), the EEZ (Marine Regions v12, doi:10.14284/632) and the marine waters Malta reports to
  the EU (EEA "Marine waters used in MSFD" v1.0, map-service outline, simplified). Written by `fetch_data.py`
  (4 Oct 2026). Marine Regions and EEA data are CC BY 4.0.
- `depth_bands.csv`: area and protected share of the shelf (0-200 m), slope (200-1,000 m) and deep sea (over 1,000 m),
  within 25 nm and across all reported waters; EMODnet depth grid via the EEA Bathymetry image service (exported
  4 Oct 2026, 0.002-degree cells, not committed). Written by `calc.py`.
- `checks.csv`: written by `tools/cc-051-report/calc.py`.
