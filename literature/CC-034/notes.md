# CC-034 notes (6 Oct 2026)

## The statement

- **ERA web page** "Air Quality Plan for Malta 2025" (`era.org.mt/air-quality-plan-for-malta-2024/`; page metadata
  `datePublished` 2025-03-12), Wayback capture 15 Aug 2025, saved copy read in full on 6 Oct 2026:
  "The plan outlines actions that have already yielded positive results for Malta's air quality, measures committed to
  by the Government for imminent implementation, and additional proposed measures ..." The same page gives the plan's
  reason: ERA's assessment of 2018 and 2023 data found that the Msida station "exceeded the allowed number of
  exceedances for the daily limit value of particulate matter (PM10)".
- **The plan** (ERA, *Air Quality Plan for Malta*, approved policy, 104 pp., ISBN 978-9918-628-10-0, PDF created
  21 Jan 2025; pages read: 3, 21-67, 91, 95; pages skimmed for effect estimates of the six measures: 4-20, 68-90,
  96-104, none found, see the search log), executive summary, p. 3: "The Air Quality Plan presents measures from other policy documents that have
  already contributed to improvements in air quality in Malta, such as the reform in the power generation sector,
  grants for more sustainable transport, free school transport, improvement of ferry landing places, a fast ferry
  link between the main islands and free public transport for all."
- The claim record combines the two. The page is the speaker's public statement; the plan names the measures.

## What the plan offers as evidence of effect (pages read: 3, 21-67, 91, 95; pages 4-20, 68-90 and 96-104 skimmed for
any effect estimate of the six measures, none found: see the search log)

| Measure (plan section) | Start (plan) | Evidence of effect the plan gives | Our reading |
|---|---|---|---|
| Power-sector reform (10.11, pp. 57-58) | Interconnector Apr 2015; Marsa decommissioned 2015 except one gas-oil unit put on standby (p. 57); Delimara on gas 2017 | Kordin NO2 and nickel 2006-2016 (Fig. 23); SO2 diffusion-tube maps 2004/2008/2014/2018 (Fig. 24); national SO2 emissions (Fig. 15); SO2 "no longer a concern" | Effect shown (SO2, nickel). Confirmed by Eurostat inventory and EEA station data; part of the SO2 fall pre-dates it (the plan credits an earlier shift to low-sulphur fuel separately: section 9.1 p. 41, p. 42, p. 58). |
| Grants for sustainable transport (10.1, pp. 47-51) | From 2010, renewed yearly | Uptake only (vehicles scrapped 2017-21, Fig. 18; LPG conversions; fleet shares). Says the scrappage scheme "does not address the problem of the increasing number of vehicles on the road". | No air-quality effect offered. |
| (Bus reform 2011, fleet technology: 10.2.1, 10.3) | 2011 | PM2.5 at Msida 2012-15 "statistically significantly lower" than 2008-11; "part" attributed to the bus reform and fleet technology; NO2 "stabilised" | Not one of the six named measures; context. Test and data not given in the plan (cites ERA 2018). |
| Free school transport (11.1, pp. 59-60) | Scholastic year 2018-19 | Msida diurnal CO and NO2, Oct-Dec and Jun-Aug, 2014-17 vs 2018-19 (Figs 25-26): CO peak ~1200 to ~860 µg/m³; NO2 "around 10 µg/m³" lower at rush hour; "can also be attributed to other reasons" | Tested: see calc.py sections E and G. CO reproduced peak to peak (1.15 to 0.86 mg/m³; highest hour 07 to 06); NO2 peak to peak -1.0 µg/m³ (62.3 to 61.3, both at EEA Start 07); largest morning fall -5.0 (Start 11:00), largest evening -6.8 (Start 20:00). The plan's own curves (digitised): peaks about 69.6 (label 07) and 61.3 (label 08), about -8. |
| Ferry landing places (11.2, pp. 59-62) | Various | Ridership: 1.6 million ferry passengers in 2018 | No air-quality effect offered. |
| Fast ferry (11.6, p. 65) | June 2021 | ~42,000 passengers in the first month | No air-quality effect offered. |
| Free public transport for all (11.7, p. 65) | 1 Oct 2022 | None; "should further encourage the public to use such modes" | No air-quality effect offered; tested (calc.py section F). |

Other plan passages used: p. 25 (41 and 52 days after deduction; natural sources "affect the Maltese Islands and
therefore the entire monitoring network in a similar manner"; deductions allowed by the Directive); p. 27-28 (Scerri
et al. 2023 summary: sea salt 23%, Saharan dust 21%, road dust/crustal 18%, tyre and brake 17%, exhaust 3.4%; most
2010-plan measures implemented but exceedances returned because of population, traffic flows and vehicle
registrations); p. 31 (NO2 national average "rather constant between 2014 and 2019", 26.04-27.44 µg/m³; COVID drop
to 21.93 in 2020); p. 54 (fleet improvement "masked by the rising number of vehicles"); p. 87 (improvement "offset by
the increasing amount of vehicles"); p. 95 (Annex I: for core future measures "All efforts will be made to quantify
the improvement in air quality").

## Data (all in data/cc-034/, retrieved 6 Oct 2026)

- EEA download service: 85 Parquet files (PM10, PM2.5, NO2, SO2, CO; AirBase, E1a, E2a); SHA-256 in `eea_files.csv`.
  PM10 and PM2.5 are daily values; gases hourly. E2a (2026) is not validated and is not used for findings.
- ERA's attainment reports (dataflow G) 2015-2025 from the Eionet CDR: PM10 days above 50 before and after natural
  deduction (2018: 86 / 41; 2023: 84 / 52), annual means (2023: 43.7 / 35.8). Our counts from EEA daily values differ
  from ERA's by -1 to +4 days a year (checks.csv, A-eea-vs-era).
- Eurostat env_air_emis (updated 7 Sep 2026): Malta, NFR 1A1a, road transport, construction. No flags on these rows.
- Eurostat road_eqs_carpda (leg_form TOTAL) and road_eqs_carhab.
- Review fixes (6 Oct 2026): `pm10_daily.csv`, `pm25_daily.csv` and `no2_daily.csv` now hold the daily values to
  3 decimals as reported (they were rounded to 0.1, which turned the 2020 Msida count of 37 days over 50 into 36 in
  Figure 1); `clock_check.csv` (hourly rows on the 22 clock-change days of 2013-2023); `plan_fig26_digitised.csv`
  (the plan's Figure 26 read off the PDF by `digitise_fig26.py`, 300 dpi, y axis calibrated on 80 and 10, vertices at
  x = 595.5 + 63.5 i; reading error about ±0.5 µg/m³, up to ±1 at sharp peaks).

## Time labels (review fix, 6 Oct 2026; calc.py section G)

- EEA hourly files: `Start` is the beginning of the hour, `End` = `Start` + 1 h in every row. Every one of the 22 days on
  which Malta's clocks changed (last Sunday of March and October, 2013-2023) has 24 hourly rows (Msida NO2): a fixed
  clock, no daylight saving. Msida NO2 peaks at Start 06 in summer (every year 2013-2023) and at Start 07 in winter
  (every year but 2014, all days: 08), as traffic following local clock time gives on a fixed UTC+1 clock. The EEA's
  own statement that hourly date-times are UTC+1 is second-hand (seen in a web-search summary of the E1a/E2a data
  dictionary; the page was not opened). Oct-Dec includes about four weeks of summer time (the clocks change on
  25-31 October).
- CO winter peak hour (Start): 07 in 2013-15 and 2019-23, 06 in 2017-18 (2016: no valid values).
- The plan's Figures 25-26 give no hour convention. Fit of the EEA profile (all days or weekdays, pooled years) to the
  digitised plan curves, RMSE in µg/m³, label = Start or Start + 1: winter 2018-19 7.0 or 0.2; summer 2018-19 5.3 or
  0.2; winter 2014-17 5.8 or 5.0; summer 2014-17 5.0 or 2.7. Best subset of the years 2013-2019 (either day-type, either
  labelling) for the winter 2014-17 curve: 3.9 (best subset 2017 and 2018). So the plan's 2018-19 curves reproduce only
  with hour-ending labels, and its 2014-17 baseline reproduces under neither.
- Peaks: plan about 69.6 (label 07) and 61.3 (label 08), -8.3; EEA all days 62.3 and 61.3 (both Start 07), -1.0, the same
  under any shift applied to both periods; weekdays only 68.0 and 68.7, +0.7. A one-hour offset between the periods
  alone gives -7.5 (62.3 at Start 07 in 2014-17 against 54.8 at Start 06 in 2018-19).
- Independent reviewer's digitisation (same method, slightly different calibration) gave 69.4, 61.2 and -8.2; RMSEs 0.2
  and 0.3 (2018-19), 5.1 and 2.9 (2014-17), subset search 3.7: the same conclusions.
- Station metadata reused from CC-008 (`data/cc-008/aq_stations.csv`, ERA's dataset D 2025): the old Msida point ended
  20 Feb 2024 (validated data to end 2023); the new point started 17 Jan 2024, about 301 m away (`data/cc-008/checks.csv`).
- CC-033 (Delimara) and CC-038 (Saharan dust) have no data folders on this branch; nothing reused.

## Literature

| Source | Access | Used for |
|---|---|---|
| Scerri et al. (2023), Environmental Pollution 316:120569 | Abstract read (Semantic Scholar); Crossref metadata verified | Msida 2018 PM10 sources: exhaust 3.4%, tyre/brake 17%, road dust/crustal 18%; "no discernible trend" in PM10 over a decade; traffic PM10 policies have "minimal effect unless the non-exhaust emissions are adequately controlled" |
| Scerri, Kandler and Weinbruch (2016), Atmospheric Environment 147:395-408 | Metadata only; content known from the plan's summary (second-hand ◆) | Għarb PM10 dominated by natural and regional sources |
| Fenech, Aquilina and Vella (2021), Frontiers in Sustainable Cities 3:631280 (CC BY) | Full text read | COVID-19: monthly NO2 at Msida up to 54% below a random-forest business-as-usual; shows Msida NO2 responds to traffic; Transport Malta traffic counters near Msida (Blata l-Bajda) exist |
| Eibinger and Fernando (2026), Environmental and Resource Economics 89:45 (CC BY) | Authors' copy read (abstract, introduction, results summary) | Luxembourg's free public transport: road-transport CO2 -5.9%, larger for NOx (synthetic DiD) |
| Albalate, Borsati and Gragera (2024), Economics of Transportation 40:100380 | Abstract read (OpenAlex) | Spain's 2022 fare discounts: "no evidence" of improved air quality |
| Grange et al. (2018), Atmospheric Chemistry and Physics 18:6223-6239 (CC BY) | Abstract read | Meteorological normalisation as the standard way to separate weather from emissions in trends |
| IMO, "IMO 2020 - cutting sulphur oxide emissions" (imo.org, Hot Topics page) | Page read 6 Oct 2026 (WebFetch) | Ships' fuel-oil sulphur limit 0.50% m/m from 1 January 2020 (down from 3.50%) outside emission control areas: a co-driver of the SO2 fall at Żejtun |
| EEA data dictionary for the E1a/E2a time series (hourly date-time begin in UTC+1) | Second-hand ◆: web-search summary only; page not opened | Context for the fixed-clock finding, which rests on the data (clock_check.csv) |
| Fenech and Aquilina (2021), Atmospheric Environment 244:117918 | Metadata only | Not cited in the report (NO2 exposure, Northern Harbour) |
| Webster (2024), Transportation Research Part A 184:104076 | Metadata only (closed, no abstract) | Not cited |

## Search log (for statements that something was not found)

- Peer-reviewed evaluation of any of the six measures' air-quality effect in Malta: Crossref searches on 6 Oct 2026
  ("Malta free public transport 2022 car use", "Malta public transport reform 2011 air pollution", "Malta electricity
  interconnector Delimara gas emissions reduction", "Malta PM10 source apportionment traffic Msida", "Malta air
  quality nitrogen dioxide trend", "Fenech Aquilina air pollution Malta"); WebSearch "Malta free public transport
  impact car use air quality study 2024". None found. OpenAlex search was rate-limited (HTTP 429) on 6 Oct.
- ERA analysis behind "already yielded positive results": the plan (read as above) and the ERA page; ERA's
  public-consultation report not read (403 / Wayback unreachable). The absence is stated only for the plan.
- Transport Malta ridership: a MaltaToday report (TM: 12% rise in 2024) appears in search results; MaltaToday returns
  403, so the figure is second-hand ◆ and not used for any finding.
- Plan pages not read in full (4-20, 68-90, 96-104), searched for any estimate of the effect of the six measures (done
  6 Oct 2026 for the review fixes, on the text extracted from the saved copy of the PDF, SHA-256 56b99ee8...cf11c4, and
  checked by the independent reviewer's page skim): (a) the six measures' names and synonyms ("free public", "fast ferry",
  "ferry", "free school", "scrap", "grant", "power generation", "interconnector", "already", "contributed", "reduction
  in", "improvement in air"); hits on pp. 5-7, 9-10 (contents and lists of figures), 17, 19, 69, 71, 74-75, 80, 83,
  85-86, 88, 92-93 and 98-101; (b) any reduction, decrease, decline, fall or "lower" followed by a figure with % or
  µg (or the reverse). Result: no estimate of the effect of any of the six measures on air quality. The only quantified
  reductions in those pages are a 2.7% change in survey opinion (p. 19) and a roughly 50% NO2 reduction in the 2020
  lockdown (p. 69). Section 13 and Annex II describe future measures; p. 80 says a dispersion modelling exercise is under
  way "to quantify the improvement in air quality attributed to the relevant measure, or packages of measures" (the
  planned measures; not stated for the six past measures). Page 91 (read) says only that "significant progress has been
  made in reducing emissions". The absence is stated for the pages read and this search, not for the whole plan.
- Plan text on fuel sulphur and shipping (for the power-sector caveats): p. 41 (section 9.1, shift to low-sulphur fuel in
  power plants, 2004), p. 42 (the fall in SO2 national emissions attributed to the fuel shift, unleaded petrol and the
  power-sector reform), p. 58 (SO2 downwind of Marsa fell 2014-2018 "due to the closure of the Marsa Power Station,
  coupled with the prior shifting to ultra-low sulphur fuel"), p. 27 (shipping with aged sea salt 8.9% of PM10 at Msida in
  2018). The plan does not mention the 2020 ship-fuel sulphur cap.
