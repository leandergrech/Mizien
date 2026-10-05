# CC-017 data

Written by `tools/cc-017-report/fetch_data.py` (retrieved 3 Oct 2026):

- `s2_land_t2.csv`: land area (ha) in a 1.0 x 1.1 km window over Freeport Terminal 2, per summer (May to mid-October),
  from a per-pixel median of up to eight clear Sentinel-2 L2A scenes (Microsoft Planetary Computer). Land = median
  NDWI (B03, B08) below 0. Precision about +/-1 ha (shoreline pixels, ships at berth).
- `s2_mask_2023.csv`, `s2_mask_2026.csv`: the land masks of that window (1 = land).
- `natura2000_near_freeport.csv`, `natura2000.geojson`: Natura 2000 sites (EEA 2024 release, discomap service) in the
  box 14.40-14.65 E, 35.75-35.90 N; distance from a reference point on the shore west of Terminal 2 (14.531 E,
  35.819 N), as used in report v1.0. The geojson is simplified to about 20 m and is used for the map only.
- `natura2000_distances.csv` (added 5 Oct 2026, report v1.1): written by `tools/cc-017-report/distances.py`. Every
  Maltese Natura 2000 site in the EEA 2024 release (map service layers 0 and 1, `MS='MT'`, full-resolution
  boundaries), with the shortest distance in km, computed in UTM 33N (EPSG:32633), from (1) `new_land`: the
  Sentinel-2 pixels that are land in 2026 and sea in 2023 in groups of 20 or more pixels (3.3 ha, the Terminal 2
  reclamation), (2) `t2_window`: the 1.0 x 1.1 km Terminal 2 window above, which includes Freeport quays, and (3)
  `reference_point`: the v1.0 point. Position of the pixel grid about +/-15 m (checked against the OpenStreetMap
  coastline). `mostly_inside` lists any other designation covering more than half of a site's area.
- `checks.csv`: written by `tools/cc-017-report/calc.py`.
