# CC-035 literature notes

Access: F = full text, A = abstract only, S = second-hand. All read on 6 October 2026 unless stated.
Grades follow `methodology/evidence-grades.md`.

| Key | Source | Access | Finding used | Grade |
|---|---|---|---|---|
| eea_quickfacts_2025 | EEA, *Air pollution quick country facts* (2025 country fact sheets) (modified 1 Dec 2025) | F | **The claim.** Malta: the rate of all-cause natural deaths attributable to long-term PM2.5 exposure above 5 µg/m3, per 100 000 inhabitants aged 30 or over, "is estimated to have been reduced by 67.7% between 2005 and 2023 (from 143.5 to 46.3, respectively), resulting in 172 (95% CI: 131-192) attributable deaths in 2023". The page's opening line: "just over 180,000 deaths in the EU" in 2023, "attributable deaths could have been avoided by meeting the WHO's guideline values". Same sentence pattern for every country (Malta 14th of 27 EU countries by size of fall; our ranking). | (claim) |
| eea_soe2025_malta | EEA, *Europe's environment 2025*, Malta, "Health impacts of air pollution" (published 29 Sep 2025) | F | Chart page (figures drawn in JavaScript), temporal coverage 2005-2022 (previous release). Text attributes Malta's PM2.5 emission cut "mainly" to cleaner power generation and says PM2.5 is "mainly influenced by natural and transboundary sources". Context only; not the statement checked. | C |
| eea_bod_2025 | EEA Briefing 16/2025, *Harm to human health from air pollution in Europe: burden of disease status, 2025*, doi:10.2800/8961999 (OP DOI; resolves to the briefing, checked with the doi.org handle API) | F | Counterfactual = WHO 2021 guideline levels (PM2.5 annual mean 5 µg/m3); results are "the attributable impacts that could have been avoided" had the guidelines been met. CIs come from the relative risks only; "Other possible uncertainties (for instance, the one related to exposure assessments) are not quantified." Rates are "per 100,000 inhabitants at risk" (aged 30+ for all-cause). Sensitivity analyses with 0 and 10 µg/m3. EU-27 2023: 182,000 deaths; 57% fewer than 2005. | C |
| eea_indicator_pm25 | EEA indicator *Premature deaths due to exposure to fine particulate matter in Europe* (published 30 Nov 2025) | F | Method history: until 2021 the WHO 2013 (HRAPIE) method; from 2022 RR 0.062 -> 0.08 per 10 µg/m3 and counterfactual 0 -> 5 µg/m3; "since the 2024 update" rates per population aged above 30; "Mortality calculations for all years back from 2005 have been recalculated using this updated methodology." Country falls 2005-2023 range from 35.1% (Greece) to 97.5% (Finland) (we reproduce both). Data source: *Burden of disease of air pollution (Countries & NUTS)*. | C |
| soares2025_etche_2025_8 | Soares J. et al. (2025). *Assessing the environmental burden of disease related to air pollution in Europe in 2023*, ETC HE Report 2025/8, doi:10.5281/zenodo.17658760 (DataCite record checked: title and six authors match). CC BY 4.0. PDF SHA-256 `45eb5cd4...ce30b` (9,452,003 bytes) | F | Table 1.1 (p. 9): all-cause PM2.5 RR 1.08 (1.06-1.09) per 10 µg/m3, adults 30+, Chen and Hoek 2020, recommended by WHO 2021. Annex 1 (pp. 45-46): PAF = (RR-1)/RR per 1 km cell, AD = PAF x crude death rate x population at risk, summed over cells. Annex 2 (pp. 47-49): RIMM maps (stations + CAMS Ensemble + altitude, meteorology, population); GHSL population scaled to Eurostat totals; natural deaths = all minus external causes (S00-T98, V01-Y89); "Causes of death data were available from 2011 onwards and this year is used as a proxy for years 2005 - 2010" (p. 49). Section 2.1.3 (p. 23): the 2005-2023 series uses "the same methodology" on "air quality maps produced by the ETC for the period from 2005 to 2023". That is the health-impact method (risk function, counterfactual, age group), not the concentration maps, which come from more than one method and model (see ETC HE 2025/5 below). **Table A3.1 (p. 53): Malta PWC 10.9 µg/m3. Table A3.2 (p. 54): Malta population 30+ 373 thousand. Table A4.1 (p. 55): Malta AD 173 (132-193), rate 46.3 (35.2-51.7).** | C |
| horalek2020_etcatni_2020_1 | Horálek J., Schreiberová M., Marková J. (2020). *Reference air quality maps 2005 and 2009*, ETC/ATNI Report 2020/1, doi:10.5281/zenodo.4293744 (DataCite checked). CC BY 4.0. PDF SHA-256 `bddb446c...dad4` | F | 2005 and 2009 maps made "using the same methodology and the same data sources as the current 2017 and 2018 maps" (p. 5): that is the 2020 report's own statement about the updated method, not a claim that the maps match the 2023 map. 2005 PM2.5 map: 173 PM2.5 stations Europe-wide (40 rural, 78 urban/suburban background, 55 traffic) plus about 1,410 "pseudo PM2.5" stations estimated from PM10 (Table A.1, p. 23: station classes are rural background, urban/suburban background and urban/suburban traffic only); EMEP MSC-W rv4.17a model (p. 23). Cross-validation RMSE of the 2005 PM2.5 map: rural 4.4 µg/m3 (33.2%), urban background 2.9 (15.9%), urban traffic 5.1 (24.0%) (Table A.4, p. 25). **Malta 2005 population-weighted PM2.5 21.2 µg/m3 (Table 2.3, p. 11)**; 2009 16.5. Our identification of the map behind the EEA's 2005 value: the EEA does not say which 2005 version its table uses, and its Malta value (21.0) differs from 21.2 without explanation (2005 also exists in an old-method version, ETC HE 2025/5 pp. 74-76). | C |
| horalek2025_etche_2025_5 | Horálek J. et al. (2025). *Air quality maps of EEA member and cooperating countries for 2023*, ETC HE Report 2025/5, doi:10.5281/zenodo.17427294 (DataCite checked). CC BY 4.0. PDF SHA-256 `ade25db4...5ec3` | F | Maps are not one method (pages checked against the PDF, 6 Oct 2026): PM2.5 maps use the updated method only from 2017, and 2005, 2009 and 2015-2019 exist in old and updated versions (pp. 74, 76); no 2006 map was prepared (p. 76); the ETC trend uses old-method maps for 2005-2014 and updated for 2015-2023 (pp. 76-77); EMEP model to 2019, CAMS Ensemble Forecast from 2020, kept from 2022 "due to the consistency with the interim maps" (p. 108); PM10-based pseudo PM2.5 stations are still used in 2023 (151 rural, 111 urban background and 344 traffic PM10 stations, p. 108; pseudo stations are excluded from the cross-validation, p. 118); 2030 PM2.5 limit value 10 µg/m3 (p. 76). 2023 PM2.5 map cross-validation RMSE 2.62 (rural), 2.9 (urban background), 2.4 (traffic) µg/m3; relative 27%, 26%, 22% (p. 118). Malta 2023 PWC 10.9 µg/m3, five-year mean 11.4 (Table 2.3, p. 25). Nine authors (DataCite); the ninth is Školoudová, Lucie. | C |
| chen_hoek_2020 | Chen J., Hoek G. (2020). Long-term exposure to PM and all-cause and cause-specific mortality: a systematic review and meta-analysis. *Environment International* 143:105974. doi:10.1016/j.envint.2020.105974 (Crossref checked: title and both authors match) | A (Europe PMC) | 107 studies (104 cohorts); PM2.5 and natural-cause mortality RR 1.08 (95% CI 1.06-1.09) per 10 µg/m3; RRs at low mean levels (below 25 down to 10 µg/m3) "similar or higher", consistent with linear or supra-linear functions; "high certainty of evidence". The basis of the WHO 2021 recommendation the EEA applies. | C (a systematic review and meta-analysis: on the scale in `methodology/evidence-grades.md` a review is C; the cohort studies inside it would be B) |
| scerri2018 | Scerri M.M. et al. (2018). Estimation of the contributions of the sources driving PM2.5 levels in a Central Mediterranean coastal town. *Chemosphere* 211:465-481. doi:10.1016/j.chemosphere.2018.07.104 (Crossref checked) | A (Europe PMC) | PMF on 180 filters from a year (2016) at Msida, described as a traffic site: traffic 27.3%, ammonium sulfate 23.6%, Saharan dust 15%, aged sea salt 12.7%, shipping 5%, fresh sea salt 4.6%, fireworks 2.9%. Context: a large natural share (dust and sea salt about 32%) in Malta's PM2.5 at that site and year. A corrigendum exists (doi:10.1016/j.chemosphere.2018.12.121; Crossref: Chemosphere 219:1061-1062, March 2019, same eight authors; Europe PMC lists no abstract and no open-access text); not read, so any change it makes is unchecked. | B (observational receptor-modelling study at one site; context only) |
| eurostat_sdg_11_52 | Eurostat `sdg_11_52`, Premature deaths due to exposure to PM2.5 (source EEA), updated 9 Dec 2025, doi:10.2908/SDG_11_52 (DataCite checked) | F (data) | Malta 348 (2005), 172 (2023) deaths; rate per 100 000 inhabitants (all ages) 86 and 31. No 2006 value. No flags on Malta. | C |
| eurostat_demography | Eurostat `demo_pjan`, `demo_magec`, `hlth_cd_aro` (retrieved 6 Oct 2026) | F (data) | Population 30+ on 1 Jan: 242,544 (2005), 373,224 (2023) (EEA table 242,534 and 373,208). Deaths 30+: 3,065 (2005), 3,987 (2023); external-cause share of deaths 30+: 2.57% (2011), 3.94% (2023). | C |
| eurostat_env_air_emis | Eurostat `env_air_emis` (NECD inventory), retrieved 6 Oct 2026 | F (data) | Malta primary PM2.5 emissions 750 t (2005), 310 t (2023); public electricity and heat 420 t to 3 t. Primary emissions only (not secondary or transboundary PM). | C |
| eea_stations | EEA Air Quality download service, AirBase (2002-2012) and E1a (2013+) Parquet files for Malta, PM2.5 and PM10 | F (data) | No PM2.5 reported to the EEA for Malta before Aug 2006 (Żejtun), Oct 2006 (Msida), Jun 2007 (Għarb). PM10 reported for 2005 at two stations (hourly): MT00002 49.0 µg/m3 (82% of days), Kordin (MT00003) 42.4 (81%). Station metadata (PanEuropean_metadata.csv, `data/cc-035/eea_station_metadata_mt.csv`): Kordin industrial urban; MT00002 not in the current metadata; Msida and St Paul's Bay traffic urban; Żejtun and Attard background urban; Għarb background rural-regional. PM2.5 instruments: beta-attenuation (Żejtun and Msida from 1 Jul 2006), gravimetric reference samplers from 2014, Msida GRIMM optical from 24 Sep 2021, Għarb TEOM-FDMS from Jun 2007. 2023 PM2.5: Attard 11.38, Msida 13.86, St Paul's Bay 9.53, Żejtun 10.93, Għarb 8.88 (mean 10.92; matches the PQ 29696 annex used in CC-007). | C |

## Recomputation (tools/cc-035-report/calc.py; data/cc-035/checks.csv)

- Statement figures reproduce exactly from the EEA table: 143.5 and 46.3 per 100 000 aged 30+; (143.5 - 46.3) /
  143.5 = 67.74%; 172 (131-192) deaths in 2023 (also Eurostat sdg_11_52). The ETC technical report gives 173 (132-193);
  46.3 x 373,208 / 100 000 = 172.8, but rounding does not explain the lower bound (35.2 x 373,208 / 100 000 = 131.4, against 131 and 132): a one-death difference we cannot explain.
- Our approximation of the method (attributable fraction at Malta's population-weighted concentration x Eurostat
  natural deaths aged 30+, with the 2011 external-cause share standing in for 2005, as the ETC does) gives 346 deaths
  for 2005 and 170 for 2023, within 0.6% and 1.2% of the EEA's 348 and 172. The EEA computes cell by cell, so a small
  difference is expected.
- The rate fall splits into a 61.7% fall in the attributable fraction (excess above 5 µg/m3: 16.0 -> 5.9) and a
  16% fall in the baseline natural death rate among people aged 30+ (1,238 -> 1,038 per 100 000; the over-30
  population grew 54%).
- Same maps, other choices: all concentrations (counterfactual 0) 54.7%; previous EEA method (RR 1.062, CF 0) 55.0%;
  above 10 µg/m3 92.4%; number of deaths 50.6%; start in 2007 56.6%; start in 2010 35.1%.
- Rough sensitivity of the 2005 start: shifting Malta's 2005 map value by the 2005 map's urban-background
  cross-validation RMSE (2.9 µg/m3, Europe-wide) gives a fall of 61.0% to 72.4%. Indicative only.
- Measured vs modelled: three long-running stations (Msida, Żejtun, Għarb) all have at least 75% valid days from
  2010 (also 2011, 2013-2023): mean 15.05 -> 11.22 µg/m3 (-25.4%) against the EEA's 13.8 -> 10.9 (-21.0%); the
  three-station mean sits 1.0 below to 1.3 above the map in those 13 years. Msida 2007-2023: 22.74 -> 13.86 (-39.1%);
  map 17.3 -> 10.9 (-37.0%). This is direct evidence that PM2.5 fell, but not an independent check of the map: the
  maps interpolate between these stations (ETC HE 2025/8 Annex 2; ETC HE 2025/5), so agreement is largely by
  construction. The 2023 five-station mean of 10.92 is an unweighted mean of two traffic (Msida, St Paul's Bay), two
  urban background (Żejtun, Attard) and one rural (Għarb) site.
- PM10 at the same stations did not fall: Msida 42.49 (2009) -> 43.7 (2023); Żejtun 29.3 (2007) -> 28.73 (2023); their
  PM2.5 fell 38.3% and 39.9%. Not untangled (instrument changes, see above).
- Indicative test of the 2005 start (labelled indicative in the report): 2005 PM10 (MT00002 49.0, Kordin 42.4) x the
  2007 PM2.5/PM10 ratios at Msida (0.535) and Żejtun (0.621) gives 22.7-30.4 µg/m3, not below the map's 21.0. The ratios
  come from other sites, another year and different valid days (coverage 65-93%); Kordin is industrial and MT00002 has
  no type in the metadata, and the ETC maps use only background and traffic stations (ETC/ATNI 2020/1 Table A.1), so the
  2005 map value may rest on no Maltese measurement at all.
- EU-27: rate 153.0 -> 59.7 (-61.0%); deaths 423,593 -> 182,399 (-56.9%; EEA says 57%). Malta 14th of 27 by fall.

## Search log (statements that something does not exist)

- "No PM2.5 reported to the EEA for Malta in 2005" (the report does not say "no PM2.5 measured"): the EEA download service lists every Malta PM2.5 file in AirBase (dataset 3,
  2002-2012) and E1a (dataset 2, 2013 on) for the query countries=MT, pollutants=PM2.5 (6 Oct 2026). The earliest
  valid PM2.5 day in them is 29 Aug 2006 (Żejtun). This covers data reported to the EEA; measurements never reported
  to the EEA would not appear. ETC/ATNI 2020/1 used AirBase v8 for the 2005 maps (p. 23), the same database. Not searched: Malta's own authority
  (ERA) records, the national air-quality reports and any measurement not sent to the EEA.
- "No 2006 value": absent from both the EEA table (years 2005, 2007-2023) and Eurostat sdg_11_52.
- Peer-reviewed literature on the EEA estimate for Malta: Crossref searches "Malta air pollution mortality burden fine
  particulate", "Malta PM2.5 source apportionment", "Malta particulate matter Saharan dust contribution PM10 PM2.5"
  (6 Oct 2026) found no study of PM2.5-attributable mortality in Malta; they found the Scerri et al. source studies.
  OpenAlex could not be searched (budget exhausted on this network).

## Gaps

- No uncertainty estimate for Malta's own map values (the RMSEs are Europe-wide cross-validation statistics).
- Scerri et al. (2016, Atmospheric Environment, doi:10.1016/j.atmosenv.2016.10.028, on Saharan dust and marine
  aerosol in PM10) found but not read (abstract elided by the publisher in Semantic Scholar; not in Europe PMC).
- Station types and instruments come from the EEA's PanEuropean metadata (6 Oct 2026); MT00002 (the other 2005 PM10
  site) is not in the current metadata, so its type is unknown.
- Which version of the 2005 map (old or updated method) the EEA's burden-of-disease table uses is not stated; its Malta
  2005 value (21.0) differs from ETC/ATNI 2020/1 (21.2) without explanation.
- Wayback copies not checked (429); both EEA pages need archiving by hand.
