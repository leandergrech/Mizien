# CC-019 data

- `amphora_figures.csv`: the figures in Amphora Media's 'Green to Grey' articles (11 and 12 Sep 2026; print copies
  supplied by the maintainer, kept locally in `literature/CC-019/`).
- `io_lulc_areas.csv`, `io_lulc_change.csv`, `new_built_strict.csv`: written by `tools/cc-019-report/fetch_data.py`
  from Impact Observatory / Esri 10 m annual land cover v2 (2017-2023, Microsoft Planetary Computer; retrieved
  4 Oct 2026). New built-up land is counted only where pixels change consistently across years (see the script);
  reverse changes gauge the noise. The strict (3-year) rule detects land first mapped as built in the 2020 or 2021
  map; the 2-year rule, land first mapped as built in 2019-2022. The `single-year` row (2018 vs 2023, added 5 Oct
  2026 for report v1.1) shows the simple comparison the rules replace.
- `checks.csv`: written by `tools/cc-019-report/calc.py`.

Added 5 Oct 2026 for report v1.2, written by `tools/cc-019-report/crosscheck.py`:

- `amphora_record.csv`: the record of Amphora Media's change polygons (the GeoJSON behind the Green to Grey map):
  URL, SHA-256, size, server date and the file's own metadata (generated 30 Aug 2026; 397 features; 162 without a 2018
  class; year range 2018-2025). The file itself is not committed: its licence is not stated. `crosscheck.py` downloads
  it to `tools/cc-019-report/out/` (git-ignored).
- `amphora_classes.csv`: Amphora's polygons by 2018 class (Dynamic World classes as named in the file): number, area
  from the geometry in UTM 33N, geodesic area, the file's own `area_m2` field (which sums to less than the geometry),
  and shares of all area and of the area with a known class (by geometry, field and count).
- `io_esri_series.csv`: Impact Observatory / Esri 10 m land cover 2017-2025 from Esri's Living Atlas image service
  (Sentinel2_10m_LandCover), exported on the v1.0 pixel grid. For 2017-2023 every pixel is identical to the Planetary
  Computer maps used in v1.0 (column `identical_to_planetary_computer_pct`); class areas on land (never water or no
  data in any year).
- `io_lulc_change_ext.csv`: the persistence rules of `io_lulc_change.csv` recomputed on the 2017-2025 maps, plus two
  rules that use the 2024 and 2025 maps (`strict-2025`: not built 2017-19, built 2023-25; `two-year-2025`: not built
  2017-18, built 2024-25).
- `amphora_io_overlap.csv`: Amphora's polygons rasterised on the 10 m grid (pixel centres) against the land cover: the
  class of Amphora's area in the 2018, 2023 and 2025 maps; built-up in all / none of 2017-19; the same for pixels at
  least 20 m inside a polygon edge; and, per rule, the share of Amphora's area the model maps as new built-up, the share
  of the model's new built-up land inside Amphora's polygons, and the same within 20 m.
- `corine_change.csv`: EEA CORINE Land Cover change polygons for Malta, 2006-2012 (CHA0612) and 2012-2018 (CHA1218),
  from the EEA discomap service: CLC codes before and after, area, centroid; `land_take` = change to an artificial
  class (CLC 1xx) from any other class. The service's layer description gives a 5 ha minimum mapping unit for change
  layers (25 ha for status layers).
