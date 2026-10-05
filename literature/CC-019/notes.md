# CC-019 literature notes

Access: F = full text, A = abstract or summary only, S = second-hand.

| Key | Source | Access | Finding used | Grade |
|---|---|---|---|---|
| amphora_2026_g2g | Amphora Media, 11 Sep 2026 | F | ~830,000 m2 built up 2018-2023 (Dynamic World, manually verified, conservative); 0.26%; "about 116 football pitches - or two Manoel Islands - and roughly a quarter of Comino" (web text re-read 5 Oct 2026); EEA 920,000 m2 (2012-18) and 190,000 m2 (2006-12) second-hand. | (claim) |
| amphora_2026_g2g_agri | Amphora Media, 12 Sep 2026 | F | "nearly 95%" farmland; period not stated. | (claim) |
| io_lulc_v2 | Impact Observatory / Esri 10 m LULC | data | Consistent new built-up: 1.9 km2 gross, 1.4 km2 net for land first mapped as built in 2020-21 (3-year rule); 5.0 / 3.0 km2 for 2019-22 (2-year rule). The rules cannot see all of 2018-2023 (corrected in v1.1). Simple 2018 vs 2023: 24.2 km2 gross, 18.9 km2 net (noise). Built-up total changes by 3-27 km2 from year to year. Before: 65% crops, 31% rangeland, 4% bare. | B |
| eea_landtake_2018 | EEA static chart, 2012-2018 | F (chart) | Malta ~2,900-3,000 m2/km2, highest of 39. | C |
| brown2022 | Brown et al. 2022 (Dynamic World) | F (Table 1, via Europe PMC PMC9184477; CC BY) | v1.2: class definitions. 'Grass': "wild cereals and grasses with no obvious human plotting (i.e. not a structured field)", examples include natural meadows and pastures; 'Crops': "human planted/plotted cereals, grasses, and crops", examples include fallow plots of structured land. | C (method) |
| karra2021 | Karra et al. 2021 | metadata | Context for the IO model. | - |
| amphora_2026_geojson | Amphora's change polygons | data | v1.2: 397 polygons, 828,429 m2 (UTM 33N geometry; the file's own area_m2 field sums to 745,042 m2). Of the area with a known 2018 class: cropland 34.3%, grass 61.4% (95.7%; 95.6% by the area field, 95.3% by count); 37.4% of the area has no class; 2 polygons (4,429 m2) were water in 2018 (Gżira and Sliema waterfronts). File metadata: generated 30 Aug 2026, year range 2018-2025, status field 'status2025'. Licence not stated; not committed. | (claim) |
| io_esri_2025 | IO/Esri land cover 2017-2025, Living Atlas | data | v1.2: 2017-2023 identical to the Planetary Computer maps pixel for pixel. Built-up totals 2024: 150.3 km2, 2025: 173.5 km2. Overlap with Amphora: 68% of Amphora's area built-up in 2018 (69% for pixels at least 20 m inside an edge; 61% in all of 2017-19); 6-14% mapped as new; 2-3% of the model's new built-up land inside Amphora's polygons (5-7% within 20 m). Net totals by rule: 1.41, 2.96, 2.11, -0.06 km2. | B |
| eea_clc_change | EEA CORINE change layers | data | v1.2: 2006-12: one polygon, 20.6 ha, sclerophyllous vegetation (323) to dump site (132) near Magħtab; 2012-18: 10 polygons, 108.4 ha, of which 93.7 ha changed to artificial land (quarries 31.7 ha = 34%; airport from farmland 15.7 ha); one 14.7 ha polygon is urban to airport. Minimum mapping unit for change layers 5 ha (layer description). | C |

## Gaps

v1.2 (5 Oct 2026): the polygons were obtained and the overlap measured (see the table above); the 2006-2012 EEA
figure was checked against the CORINE change layer. Remaining:

- Neither Amphora's polygons nor the independent model's 2018 state were checked against high-resolution imagery, so
  it is unknown which is right where they disagree (68% of Amphora's area mapped as built-up in 2018).
- The basis of the 95% is our reading of Amphora's data (cropland + grass of the area with a known class), not
  confirmed by Amphora; the file's year range (2018-2025) differs from the article's (2018-2023).
- The reviewer's figures (68.8% built in 2018; 5.8-13.4% new; 2.5-3% overlap) were reproduced to within a few tenths
  of a percentage point (68.3%; 5.9-13.6%; 2.3-2.7%); differences come from pixel-centre rasterisation.

Earlier gaps (v1.0/v1.1):

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
