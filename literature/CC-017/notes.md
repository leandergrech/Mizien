# CC-017 literature notes

Access: F = full text, A = abstract or summary only, S = second-hand (known through another source).
Searches run 3 October 2026 (Crossref, OpenAlex, web search; budget speech read in a browser).

| Key | Source | Access | Finding used | Grade |
|---|---|---|---|---|
| budget2026 | Budget Speech 2026, pp. 52-53 | F | The claim: government "is preparing to launch a large-scale land reclamation project outside the Freeport perimeter next year"; industrial and maritime use; relocation of "certain commercial activities". No site, size, cost or assessment. | (claim) |
| lovin_2025_abela | PM, press conference after the Budget, as quoted by Lovin Malta, 28 Oct 2025 | F (v1.2) | "The sea near the Freeport is an ideal depth for these kinds of projects, and our idea is to relocate industries that bother people."; no specifics. | (claim) |
| mt_2019_seabed | MaltaToday, Sep 2019 | F | Herrera: five or six sites "possible and environmentally safe" from an EUR 11m seabed study; to go to public consultation. "Least environmental damage" is the newspaper's paraphrase, not the minister's words (v1.1). | (claim) |
| mt_2025_saga | MaltaToday analysis, Apr 2025 | A (S) | Announcements since 2005, none delivered outside ports; seabed study (ERA draft) leaked 2019, never published; budget lines cut from EUR 500,000 to 10,000. | C |
| mfc_squaring_off, mft_2025_t2 | Freeport operator and corporation | A | Terminal 2 reclamation ~30,000 m2, ~1 Mt inert material, 11 caissons. | C |
| s2_l2a | Sentinel-2 | data | +3.7 ha (about +/-1) at Terminal 2, 2023-2026; no change 2017-2023. | B |
| eea_n2k_2024 | EEA Natura 2000 | data | v1.1: three designations within about 0.5 km of the new Terminal 2 land: the 256 km2 marine SPA MT0000111 (0.4 km) and two overlapping cliff designations, SAC MT0000024 and SPA MT0000033 (0.5 km; MT0000033 lies 99.9% inside MT0000024). v1.0 measured about 1 km from an onshore point west of Terminal 2. | C |
| telesca2015 | Telesca et al. 2015 | A | 34% regression of Posidonia meadows across the Mediterranean in 50 years (basin-wide, not a Malta figure), mainly cumulative local stressors. | B |
| boudouresque2009 | Boudouresque et al. 2009 | A | Coastal development, dredging and dumping are main human causes of Posidonia loss. | C |
| sengupta2018 | | metadata only | Not used. | - |
| unepwcmc_seagrass_v71 | UNEP-WCMC, Short 2021, Global Distribution of Seagrasses v7.1 | data | v1.2: FeatureServer layer 1 (polygons). In the map frame 14.505-14.600 E, 35.795-35.862 N: 59 polygons, 384.8 ha of P. oceanica (union), from two overlapping Maltese source datasets (ID 491, event dates 1961/2014, 225 ha; ID 493, event date 2002, 297 ha; 137 ha overlap). Nearest to the Terminal 2 new land 0.19 km; 23.5 ha within 0.5 km, 119.6 ha within 1 km. The review's figures (57 polygons, ~386 ha off the south-east) match this frame closely; its ~134 ha 'rough bay box' is not reproduced exactly (box not recorded). Licence: UNEP-WCMC General Data License (excluding WDPA) - no redistribution, no commercial use, publication allowed if not downloadable, with citation, release year and a link to www.unep-wcmc.org. Polygons kept in tools/cc-017-report/out/ only. | C |
| emodnet_seagrass_2025 | EMODnet Seabed Habitats, Seagrass cover (EOV) v2025 | data | v1.2: 26 Maltese polygons (map EUSM16me, determination 2016; source field 'Malta Environment and Planning Authority' for about half of the national area, blank for the 6 polygons in the bay); gridded at about 230 m; 195.9 ha in the frame, 72.1 ha within 1 km of the new land. CC BY 4.0 (European subset). Its grid cells reach the Freeport, so its distance to the new land is not meaningful. | C |
| emodnet_dtm_2024 | EMODnet Digital Bathymetry DTM 2024 | data | v1.2: WCS coverage emodnet__mean, 1/16 arc-minute cells. Within 1 km of the new land: depth 10th/50th/90th percentile 5/18/30 m; within 0.5 km 11/18/27 m. Mapped meadows in the frame: 8/19/34 m. Some cells near the shore and in the inner harbour have no depth (positive values in the grid). | B |
| eea_art17_1120_mt | EEA Article 17 web tool, habitat 1120, Malta (MMED) | F (web tool) | v1.2: 2013-2018: range 202 km2 FV; area 68.46 km2 (method a, complete survey in 2018-2019 per Malta's note), FV; structure and functions good 66.38-68.46 km2, not good up to 2.08 km2, FV; future prospects FV; overall FV, trend stable. 2019-2024: area 68.46 km2 (no change; method: extrapolation from limited data), FV; good 66.38 km2, not good 2.08 km2; overall FV, trend S (stable). National assessment; does not report individual bays. | C |
| sentinel2_mndwi_test | Sentinel-2 MNDWI, bay-wide | data (method test) | v1.2: not robust (control pairs 37-80 ha of false 'new land'); not used. tools/cc-017-report/s2_bay.py. | - |

## Gaps

- The ERA seabed / land reclamation study has not been published; no site list, habitat map or method is public.
- No project description, EIA screening, planning application or call was found for the reclamation outside the
  Freeport as of 3 Oct 2026. Absence in searches is not proof that nothing has started; ask the ministry.
- v1.2: Posidonia maps obtained from UNEP-WCMC (v7.1) and EMODnet (2025), but both compile older surveys (1961-2014,
  2002; EMODnet's Maltese layer dated 2016 and gridded). Malta's complete 2018-2019 survey (Article 17 note) was not
  found as a public map; this remains the most important missing environmental evidence for the bay.
- The UNEP-WCMC dataset page (data.unep-wcmc.org/datasets/7) had an expired TLS certificate on 5 Oct 2026 and the
  Wayback copy was blocked by the network policy; the citation and licence were verified from the DataCite record of
  doi:10.34892/x6r3-d211, the licence page on unep-wcmc.org, and the citation EMODnet reproduces in its metadata.
  The source table (Metadata_Seagrass.dbf) naming datasets 491 and 493 was not read.
- UNEP-WCMC licence conditions for the maintainer: it recommends review of materials by UNEP-WCMC before publication
  and "requires" two free copies of published materials (clause 4). Not done: no third parties contacted.
- The PM's words are Lovin Malta's rendering; a recording of the press conference was not checked.
- Source of fill: the Terminal 2 works use inert construction waste; a larger project's fill source is not stated.
