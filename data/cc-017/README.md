# CC-017 data

Written by `tools/cc-017-report/fetch_data.py` (retrieved 3 Oct 2026):

- `s2_land_t2.csv`: land area (ha) in a 1.0 x 1.1 km window over Freeport Terminal 2, per summer (May to mid-October),
  from a per-pixel median of up to eight clear Sentinel-2 L2A scenes (Microsoft Planetary Computer). Land = median
  NDWI (B03, B08) below 0. Precision about +/-1 ha (shoreline pixels, ships at berth).
- `s2_mask_2023.csv`, `s2_mask_2026.csv`: the land masks of that window (1 = land).
- `natura2000_near_freeport.csv`, `natura2000.geojson`: Natura 2000 sites (EEA 2024 release, discomap service) in the
  box 14.40-14.65 E, 35.75-35.90 N; distance from the Freeport (14.531 E, 35.819 N).
- `checks.csv`: written by `tools/cc-017-report/calc.py`.
