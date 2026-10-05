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

Added 5 Oct 2026 for report v1.2, written by `tools/cc-017-report/fetch_bay.py` (map frame 14.505-14.600 E,
35.795-35.862 N):

- `natura2000_bay.geojson`: Natura 2000 sites in the frame, full-resolution boundaries from the EEA service (2024
  release; service copyright "EEA, Copenhagen, 2025"), clipped to the frame, as `natura2000.geojson` since v1.0.
- `seagrass_emodnet_bay.geojson`: EMODnet Seabed Habitats 'Seagrass cover (EOV)' polygons, version 2025, clipped to the
  frame (European subset, CC BY 4.0; map EUSM16me, determination 2016; gridded at about 230 m).
- UNEP-WCMC Global Distribution of Seagrasses v7.1 polygons are NOT committed: the UNEP-WCMC General Data License forbids
  redistribution. `fetch_bay.py` saves them to `tools/cc-017-report/out/` (git-ignored) to draw the map and compute
  statistics. Likewise the EMODnet depth grid (DTM 2024) stays in `out/`.
- `bay_stats.csv`: mapped Posidonia in the frame and within 0.5, 1 and 2 km of the Terminal 2 new land, and the shortest
  distance, per source (UNEP-WCMC datasets 491 and 493 and their union; EMODnet); depth percentiles of the EMODnet grid
  within 0.5, 1 and 2 km of the new land and on mapped meadows. Distances and areas in UTM 33N.
- `article17_1120_mt.csv`: Malta's Article 17 assessment of habitat 1120 (Posidonia beds), Mediterranean marine region,
  periods 2013-2018 and 2019-2024, parsed from the EEA Article 17 web tool (status codes: FV favourable; trend = or S
  stable).

Written by `tools/cc-017-report/s2_bay.py` (a method test that failed; not used for findings):

- `s2_mndwi_bay.csv`, `s2_mndwi_scenes.csv`: a bay-wide Sentinel-2 MNDWI check for new land outside Terminal 2 and the
  scenes it used. Control pairs of summers with no known reclamation gave 37-80 ha of false 'new land', so the method
  is not robust here (see the script's docstring).
