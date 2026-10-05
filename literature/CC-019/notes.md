# CC-019 literature notes

Access: F = full text, A = abstract or summary only, S = second-hand.

| Key | Source | Access | Finding used | Grade |
|---|---|---|---|---|
| amphora_2026_g2g | Amphora Media, 11 Sep 2026 | F | ~830,000 m2 built up 2018-2023 (Dynamic World, manually verified, conservative); 0.26%; "about 116 football pitches - or two Manoel Islands - and roughly a quarter of Comino" (web text re-read 5 Oct 2026); EEA 920,000 m2 (2012-18) and 190,000 m2 (2006-12) second-hand. | (claim) |
| amphora_2026_g2g_agri | Amphora Media, 12 Sep 2026 | F | "nearly 95%" farmland; period not stated. | (claim) |
| io_lulc_v2 | Impact Observatory / Esri 10 m LULC | data | Consistent new built-up: 1.9 km2 gross, 1.4 km2 net for land first mapped as built in 2020-21 (3-year rule); 5.0 / 3.0 km2 for 2019-22 (2-year rule). The rules cannot see all of 2018-2023 (corrected in v1.1). Simple 2018 vs 2023: 24.2 km2 gross, 18.9 km2 net (noise). Built-up total changes by 3-27 km2 from year to year. Before: 65% crops, 31% rangeland, 4% bare. | B |
| eea_landtake_2018 | EEA static chart, 2012-2018 | F (chart) | Malta ~2,900-3,000 m2/km2, highest of 39. | C |
| brown2022, karra2021 | Dataset method papers | metadata | Context for the two models. | - |

## Gaps

- EEA land take 2012-2018: read from the EEA static chart (PDF supplied by maintainer): about 2,900-3,000 m2/km2,
  i.e. 0.91-0.94 km2, the highest of EEA39; consistent with the 920,000 m2 quoted. The 2006-2012 figure (190,000 m2)
  was not seen.
- Amphora's polygons (the map) were not downloaded, so the 830,000 m2 cannot be reproduced exactly.
- The 95% farmland share: class definitions differ between Dynamic World (crops, shrub & scrub, grass) and IO
  (crops, rangeland); abandoned Maltese fields may be classed as either. Amphora does not state its basis.
- "Top 5 in Europe": comparison by the Green to Grey network; country results not checked.
- Comino's area: 2.77 km2 from the OpenStreetMap outline (docs/data/geo.json); 3.5 km2 is the figure often quoted
  (e.g. Wikipedia, unsourced); Britannica gives about 3 km2. Amphora's "roughly a quarter" matches 3.5 km2 (0.24).
- Suggested upgrade (reviewer, 5 Oct 2026; not verified here): only 2.5-13% of IO new-built pixels overlap Amphora's
  polygons, so the two estimates largely flag different land. Obtaining the polygons and measuring the overlap would
  test whether the independent estimate corroborates Amphora's areas or only its order of magnitude.
