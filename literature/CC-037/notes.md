# CC-037 literature notes

Access: F = full text, A = abstract or summary only, S = second-hand.
Searches run 5 October 2026 (Crossref, OpenAlex, Eurostat API, EU Publications Office). v1.1 additions marked (v1.1).

| Key | Source | Access | Finding used | Grade |
|---|---|---|---|---|
| amphora_guidebook_2026 | Amphora Media, 2026 Election Guidebook: The Environment, 12 May 2026 | F | The claim. Intro: "35% of people in Malta reported exposure to pollution in 2023 — the highest share in the EU." Body ("Is Malta becoming cleaner?"): "more than a third of people (35%) in Malta reported exposure to pollution, grime, and other environmental problems. This is the highest share in the EU and nearly three times the EU average of 12%. According to the report, high-earning households were more affected than low-earning ones." **No source is named or linked** (the HTML contains no Eurostat link or mention); only the income sentence is attributed, to an unnamed "report". | (claim) |
| eurostat_ilc_mddw02 | Eurostat EU-SILC, pollution, grime or other environmental problems (doi:10.2908/ILC_MDDW02) | F (data) | Malta 34.7% in 2023, EU-27 12.2%; Malta first of 27 (Greece 20.5%, Germany 16.8% flag u, France 16.0%); first among every country in the dataset (Türkiye 19.8% the highest non-EU). Malta first in all 17 survey years with data (2005–2020, 2023). Series: 41.4% (2011), 26.5% (2017), 37.4% (2014), 34.7% (2023). Income split 2023: 35.6% above vs 30.1% below 60% of median income; EU-27 11.8% vs 14.0%. Flags kept since v1.1: EU-27 2010–2020 'e' (estimated), Germany 2023 'u', Germany 2020 'bu', Greece 2009 'b'; Malta none. | C |
| eurostat_ilc_li02 (v1.1) | Eurostat EU-SILC, at-risk-of-poverty rate | F (data) | Malta 16.6% below 60% of median income in 2023, so the "above" group is 83.4% of people; EU-27 16.2%. | C |
| eurostat_se_qol_env (v1.1) | Eurostat, Statistics Explained, "Quality of life indicators – natural and living environment", last edited 14 Aug 2025 (data from March 2025) | F | Likely source of all three Amphora statements. Calls the indicator people "reporting exposure to pollution, grime or other environmental problems" and "self-reported exposure"; Malta "by far the highest share" (34.7%), then Greece, Germany, France; Malta among 9 countries where people at risk of poverty reported less (5.5 pp lower). Its EU income figures (14.1% / 11.9%) are from the March 2025 extraction; the database now gives 14.0% / 11.8%. Says the variables come from the EU-SILC 2023 three-yearly module "Labour market and housing". | C |
| eurostat_news_20250901 (v1.1) | Eurostat news, "12% of EU population reported pollution in their area", 1 Sep 2025 | F | EU 12.2% (15.1% in 2019); Malta 34.7%, Greece 20.5%, Germany 16.8%; Croatia lowest 4.2%. Uses "exposure to pollution, grime or other environmental problems". Data from the "Labour market and housing conditions" module, "collected every 3 years". | C |
| eurostat_se_silc_env_method (v1.1) | Eurostat, Statistics Explained, "EU-SILC methodology – environment of the dwelling", last edited 10 Aug 2023 | F | Definition: share of the population "who face the problem of pollution, grime or other environmental problems in the local area such as: smoke, dust, unpleasant smells or polluted water"; calculated as the weighted (RB050a) share of persons with HS180 = 1; the respondent judges whether it is a problem for the household, and "No common standards what is a problem are defined". Its line "All indicators are collected and disseminated on an annual basis" predates the 2021 change. | C |
| reg_2019_1700 (v1.1) | Regulation (EU) 2019/1700, OJ L 261I, 14.10.2019, p. 1 | F (Cellar XHTML) | Annex IV point 2: income and living conditions data "collected annually, every three years and every six years". EU-SILC follows it from 2021 (Eurostat ESMS metadata). | C |
| reg_del_2022_29 (v1.1) | Commission Delegated Regulation (EU) 2022/29, OJ L 7, 12.1.2022, p. 1 | F (Cellar XHTML) | Annex: module "Labour market and housing", detailed topic "Housing conditions details", variable HS180 "Pollution, grime or other environment problems" (with HS170 noise, HS190 crime). | C |
| reg_del_2020_256 (v1.1) | Commission Delegated Regulation (EU) 2020/256, OJ L 54, 26.2.2020, p. 1 | F (Cellar XHTML) | Annex I: "Labour Market and Housing (ILC3YC)" collected in 2023 and 2026 (2021–2028 plan). | C |
| aguilera2007 | Aguilera et al. 2007 (Epidemiology 18(5):S43) | A | In 504 women in Sabadell, self-reported air-pollution annoyance was associated with modelled NO2 and VOC levels; agreement by category 11-72%. Shows perception tracks measured exposure only partly. | B/C |

## Why 2021 and 2022 have no data (v1.1)

Until 2020 the item was collected and published every year. Since 2021 EU-SILC runs under Regulation (EU) 2019/1700,
which collects some items annually and others every three or six years (Annex IV). HS180 is in the three-yearly
"Labour market and housing" module (Delegated Regulation 2022/29), scheduled for 2023 and 2026 (Delegated Regulation
2020/256). 2023 is the first year of the new cycle; the next figures are for 2026. Eurostat's release says the same
("collected every 3 years").

## The Amphora page (archive record)

- Fetched 5 Oct 2026 by the review (curl, archiver user agent) and again in this session: 115,688 bytes, SHA-256
  `753d24b57116c0be164b13b7815be5f3f57ef42b8e785c72ae2a5563958f3979` (identical both times).
- Fetched 5 Oct 2026 10:57 UTC with `scripts/archive_sources.py`'s own fetch (Python urllib, archiver user agent):
  116,055 bytes, SHA-256 `90b30b66588cb4fa67fc3e8ce8e9f54c999e0aaa1c542f10954945c5d68aabd8` (stable on repeat). The two
  copies differ only in script blocks at the end of the page (a caching plugin and an analytics beacon); the visible
  text is identical (checked by extracting both). The
  manifest row (`archive/manifest.csv`) holds this hash.
- robots.txt allows the page (only `/wp-admin/` is disallowed). Python's robotparser reports it disallowed because
  amphora.media returns 403 to Python's default user agent when robotparser fetches robots.txt.
- Wayback: the availability API lists a capture of 16 Jun 2026
  (`http://web.archive.org/web/20260616063729/https://www.amphora.media/2026/05/2026-election-guidebook-the-environment`),
  but web.archive.org refused connections from this network (connection reset), so the capture was not opened and no
  new capture was made. **Manual task:** open the capture in a browser, check it shows the same wording, and save a
  fresh capture.
- The HTML is not committed (copyright).

## Gaps

- No peer-reviewed study comparing Eurostat's perception indicator with measured air quality in Malta was found.
  The Aguilera abstract is from Spain and is context only.
- Measured concentrations (EEA air quality, Malta stations) were not compared in this check; the claim is about reports, not measured exposure.
- Amphora does not name a source; the match to Eurostat ilc_mddw02 and to Eurostat's 2025 article and release is ours.
- The noise indicator (ilc_mddw01/ilc_mddw04) is not used in this check and no noise data file is kept; Eurostat's
  2025 article gives Malta 31.3% for noise (2023), the highest in the EU (see CC-020).

## Audit checks, 6 Oct 2026

- doi:10.2908/ILC_MDDW02: doi.org redirects to https://ec.europa.eu/eurostat/databrowser/product/page/ILC_MDDW02; DataCite
  (api.datacite.org) lists it, creator Eurostat, EN title "Pollution, grime or other environmental problems". Crossref has no
  record (DataCite DOI). Kept in reference 2.
- Amphora page (re-fetched 6 Oct 2026, 115,688 bytes, same size as the 5 Oct fetch): post-date element reads "12 May 2026".
- Wayback capture 20260616063729 opened on 6 Oct 2026: the intro sentence, the body sentences and "12 May 2026" are all present.
