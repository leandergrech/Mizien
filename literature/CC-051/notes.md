# CC-051 notes

| Key | Source | Access | Finding used | Grade |
|---|---|---|---|---|
| era_mpa | ERA topic page | F | 18 marine sites, over 4,100 km2, >35% of the FMZ (qualified). | (claim) |
| amphora_2025_fatti | Amphora Media fact-check | F | Minister's unqualified "more than 30% of its maritime zone"; EEA confirms 75,715 km2 reported; FMZ ~11,480 km2. | S |
| bise_malta | BISE | A | Marine area over 75,000 km2; coverage below EU average. | C |
| eea_n2k_2024 | EEA Natura 2000 | data | Union of 18 marine sites: 4,137.5 km2 of sea (sum without dissolving overlaps: 5,496 km2). All of it within 25 nm of the baselines. | C |
| vliz_eez_v12 | Marine Regions EEZ v12 | data | Malta EEZ outline, 52,923 km2; 4,130 km2 of the protected sea inside it. | C |
| vliz_12nm_v4 | Marine Regions 12 NM v4 | data | 12-nm limit; 25-nm zone rebuilt from it = 11,492 km2 (official 11,480). 183 km2 of protected sea lies in internal waters. | C |
| eea_msfd_waters_2020 | EEA marine waters (MSFD) | data | Outline of the waters Malta reports to the EU (simplified, 75,484 km2 in UTM 33N); labelled "Area designated for hydrocarbon exploration and exploitation". About 64,000 km2 beyond 25 nm, none protected. | C |
| eea_emodnet_bathy | EMODnet depth via EEA | data | Reported waters: shelf <200 m 15.7% (14.0% protected), slope 58.4% (5.3%), deep >1,000 m 25.8% (0.6%). | C |
| ec_2020_biodiversity_strategy | COM(2020) 380 | F | 30% of the EU's sea; targets relate to the EU as a whole, each Member State's "fair share". | C |
| cbd_2022_gbf_t3 | CBD GBF Target 3 | F | 30% through "ecologically representative" systems of protected areas. | C |

## Gaps

- The minister's own text (event, date) was not found; quoted via Amphora.
- Protection here means Natura 2000 designation; management measures and their enforcement were not assessed.
- Percentages use the published EEZ (52,923 km2) and EU-reported (75,715 km2) areas. Since v1.1 the outlines are also
  used (Marine Regions EEZ v12; the EEA's simplified web outline of the MSFD marine waters, 75,484 km2); the full-
  resolution EEA dataset is a ~1 GB EU-wide download and was not used.
- The official 11,480 km2 FMZ excludes internal waters, while ERA's numerator includes ~183 km2 of protected internal
  waters; like-for-like the share is 34-35% (calc.py).
- Depth bands are a proxy for habitat types; no habitat map (e.g. EMODnet Seabed Habitats) was used.
