# CC-092 literature notes: afforestation in a net-zero Gozo, and indigenous trees (PN programme 2026)

Checked 10 October 2026. Access: F = full text, A = abstract only, M = metadata/title only, S = second-hand.
The net-zero plan itself (baseline, boundary, pathway) is Claim Check 107; this check asks what afforestation could
contribute on Gozo and whether the programme has an indigenous-tree strategy.

| Key | Source | Access | Finding used | Grade |
|---|---|---|---|---|
| pn_programme_2026_ghawdex | PN programme, Għawdex item 46 | F | Afforestation is one of the listed initiatives by which "every unit of emissions" would be "reduced or offset" by 2040. No area, species, rate or date for afforestation. | (claim) |
| pn_programme_2026_ambjent | PN programme, Ambjent items 01, 20, 25 | F | "More afforestation" in Malta and Gozo (01); tree planting and afforestation against heat, flooding and pollution (20); garrigue (*xagħri*) in the Malta Nature Network to be protected (25). | (claim) |
| pn_programme_2026_agrikoltura | PN programme, Agrikoltura item 31 | F | Local plant varieties and livestock breeds: gene bank, nursery and support in three years. Only use of *indiġeni*; not trees. | (claim) |
| maltatoday2026breakdown | MaltaToday breakdown, May 2026 | S (search summary; 403) | Reportedly a nationwide afforestation strategy prioritising indigenous trees and valley restoration. Not found in the PN's text. | locator |
| grunzweig2007 | Grünzweig et al. 2007 | F | 99 g C m-2 yr-1 ecosystem (3.62 t CO2 ha-1 yr-1), 35 years, Aleppo pine on former shrubland; soil 50 g C. Not irrigated. | B |
| renna2024 | Renna et al. 2024 | A | Native holm and cork oak on former cropland (Spain): biomass 25-75 g C m-2 yr-1 (0.92-2.75 t CO2); soil C not higher; total not significantly higher; may need decades to become a sink. | B |
| bernal2018 | Bernal et al. 2018 | F (Europe PMC) | Planted forests 0-20 years, temperate dry: oak 5.3, pine 7.6, other conifers 6.4 t CO2 ha-1 yr-1 (biomass; soil excluded). | C |
| hoogmoed2012 | Hoogmoed et al. 2012 | A | Meta-analysis: no substantial change in soil carbon across three decades of afforesting pasture in Mediterranean climates. | C |
| maestre2004 | Maestre and Cortina 2004 | A | Aleppo pine plantations in semi-arid Mediterranean areas: more runoff and soil loss than shrubland in many studies, higher water use, mostly negative effects on spontaneous vegetation. | C |
| oliet2023 | Oliet et al. 2023 | A (PDF committed) | 20-year survival of planted Aleppo pine 29.5-57.5% in arid Spain; mortality settled only after 15 years. | A |
| jackson2005 | Jackson et al. 2005 | A | Plantations cut stream flow by 227 mm a year (52%) globally. | C |
| rotenberg2010 | Rotenberg and Yakir 2010 | A | Dry forests (200-600 mm) keep sequestering, but need several decades to balance their albedo and longwave warming. | B |
| yosef2018 | Yosef et al. 2018 | A | Model: at about 200 million ha, semi-arid afforestation would overwhelm the warming within about 6 years; Yatir about 300 mm rain. | C |
| veldman2015 | Veldman et al. 2015 | A | Planting trees in open, grassy ecosystems harms biodiversity and ecosystem services. | C |
| euislands2023gozo | Energy Baseline Scenario for Gozo (2023) | F | Energy CO2 118,333-153,997 t a year, 2016-2020 (Table 16, p. 25). Not official statistics. | C |
| eurostat_cc092 | Eurostat datasets | data | Malta forest 470 ha (FAO, 2025); forest land -0.16 kt CO2e in 2024; LULUCF +1.39 kt; MT002 land 68 km2; WEI+ 30.1% (2023), 36.7% (2022); metadata: Malta in permanent water scarcity. | C |
| eea_clc2018 | CORINE Land Cover 2018 | data | Gozo: no forest class mapped; semi-natural (323 + 333) 1,265 ha; farmland 3,801 ha; artificial 1,520 ha (of 6,586 ha). 323 includes maquis and garrigue. | C |
| eea_natura2000 | EEA Natura 2000 sites (Malta) | data | 453 ha (36%) of Gozo's semi-natural land and 782 ha (12%) of all its CORINE land lie inside Natura 2000 sites. | C |
| nasa_power | NASA POWER (MERRA-2) | data | Rainfall 1991-2020: Gozo about 570 mm, Yatir about 230 mm a year (reanalysis; Yosef et al. give about 300 mm for Yatir). | C |

## Our own analysis (data/cc-092/, tools/cc-092-report/calc.py)

- Forest needed to offset Gozo's 2016-2020 energy CO2 (118,333-153,997 t): 1,291-1,680 km2 (19-25 times Gozo's 67 km2)
  at the low rate; 326-425 km2 (4.9-6.3 times) at the central rate (as in Claim Check 107); 156-203 km2 (2.3-3.0 times)
  at the high rate.
- If all of Gozo's semi-natural land (1,265 ha) were planted: 0.8-1.0% (low), 3.0-3.9% (central), 6.2-8.1% (high) of
  that CO2. All farmland and semi-natural land (5,066 ha): 3.0-32.5%. All of Gozo: 4.0-43.0%.
- Central forest need about 90 times Malta's whole forest area (470 ha, 2025). Malta's forest-land removals in 2024
  (0.16 kt) are 0.1% of Gozo's 2019 energy CO2.
- Natura 2000 (natura.py): 453 ha (36%) of the semi-natural land, 271 ha (7%) of the farmland and 782 ha (12%) of all
  Gozo's CORINE land lie inside Habitats or Birds Directive sites.
- Stocking the semi-natural land at Yatir's 300 trees per ha, allowing for 46% survival after 20 years: about 825,000
  trees, about 52 years at Malta's recent government planting pace (about 60,000 trees from 2022 to end 2025).

## Search log (absence statements)

"No national indigenous-tree strategy in the PN programme" and "afforestation has no area, species, rate or date":
- PN programme, all 16 web chapters and all 16 chapter PDFs on pn.org.mt, full text, 10 Oct 2026: counts of
  *afforestazzjoni*, *siġar/siġra*, *indiġen-*, *nattiv-/endemi-*, net-zero, *xagħri*, *karbonju/carbon* and
  *strateġija* per document in `data/cc-092/pn_programme_search.csv` (script `tools/cc-092-report/search_programme.py`).
  *Indiġen-* occurs only in Agrikoltura item 31 (farm varieties and breeds); afforestation only in Għawdex 46 and
  Ambjent 01 and 20; none gives a number of trees, an area, a species or a date for afforestation.
- pn.org.mt sitemaps (posts, pages, events, articles, press releases, programme pages; 1,854 URLs), slugs searched for
  trees, afforestation, indigenous, net zero, Gozo and climate; six Gozo posts of April-May 2026 and two climate press
  releases read (none mentions net zero, afforestation or indigenous trees). Site search and WordPress API are not
  usable by scripts (as found for CC-114).
- Newsbook (PN programme at a glance; general council live report; Gozo EU funding) and TVM News (PN approves its
  manifesto; PN leader on investment in Gozo): read 10 Oct 2026; no mention of afforestation, trees or net zero. The
  Newsbook "at a glance" piece found by search is about the 2022 programme.
- WebSearch, 10 Oct 2026: "PN manifesto 2026 Gozo net-zero afforestation indigenous tree strategy"; "PN published its
  manifesto breakdown MaltaToday indigenous trees"; "Nationalist Party 2026 manifesto indigenous trees strategy Malta";
  "PN manifest elettorali 2026 strateġija siġar indiġeni afforestazzjoni Għawdex"; "afforestation strategy PN manifesto
  2026 indigenous trees valleys"; and a site-limited search of newsbook, tvmnews, lovinmalta, theshiftnews, gozotoday,
  netnews and illum. Only MaltaToday's breakdown (via the search engine's summary) mentions indigenous trees.
- MaltaToday 142040 and 141891: HTTP 403 (curl and WebFetch). web.archive.org: connection reset; archive.org
  availability API: HTTP 429.
- Not searched: PN speeches on video, social media posts, printed leaflets.

## Gaps

- No Malta- or Gozo-specific measurement of afforestation carbon was found (Crossref searches for Malta afforestation,
  Maltese woodland and Gozo returned nothing relevant on 10 Oct 2026). All rates are from Spain, Israel or global
  syntheses.
- CORINE's 25 ha minimum mapping unit misses small woods, tree rows and valley vegetation; the land shares are
  approximate. Planting all semi-natural land is a ceiling, not a feasible plan: class 323 includes garrigue, which the
  PN's own item 25 lists among the habitats to protect; 453 ha of it (36%) lies inside Natura 2000 sites
  (`data/cc-092/natura2000_overlap.csv`, measured on generalised CORINE polygons, so approximate). Whether the rest is
  protected under national law was not checked.
- Goberna et al. 2007 (Applied Soil Ecology 36:107-115, doi:10.1016/j.apsoil.2006.12.003; verified in Crossref) report
  in their title that Aleppo pine plantations did not restore soil organic carbon in a semi-arid Mediterranean soil.
  Only the title and metadata could be read (abstract withheld by the publisher's metadata); not used in the report.
- Ruiz-Peinado et al. 2017 (Forest Systems 26(2):eR04S, doi:10.5424/fs/2017262-11205; verified): review of forest
  management and carbon in the Mediterranean; open access but the publisher's server failed TLS verification and
  returned 503, so only the abstract (no rates) was read. Not used.
- Rainfall from a reanalysis (about 50 km cells) is approximate; no station series was read.
