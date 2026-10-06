# CC-075 literature notes

Access: F = full text, A = abstract or summary only, S = second-hand.
Searches and downloads run 6 October 2026 (Eurostat API and news pages, Eurostat Statistics Explained PDFs and its
MediaWiki API, Crossref, OpenAlex, DataCite, WebSearch, Lovin Malta page and WordPress API, Newsbook).

| Key | Source | Access | Finding used | Grade |
|---|---|---|---|---|
| lovin_2024_cars | Lovin Malta (J. Darmanin), 21 Sep 2024 | F | The claim, in the outlet's own words (no quotation marks; Lovin is the speaker): "according to the statistics Malta is ranked number seven, just between Germany and Poland respectively, with 585 cars per 1,000 inhabitants". Also: Eurostat "shared a dataset detailing the unit of cars per thousand residents in each European country as of 2023"; a graphic by Paula Lago via The European Correspondent "better illustrated these rankings up to the year 2022"; Italy top at 682, Latvia lowest at 409; "approximately 1 car for every 2 people"; "with just 246 square kilometres of land, Malta is also up there among the countries with the highest car density in Europe". The article gives conflicting year signals (dataset "as of 2023", graphic "up to the year 2022"); the sentence with the 585 and the rank carries no year of its own, and the rank is in the present tense. | (claim) |
| eurostat_se_passenger_cars_rev647912 | Eurostat Statistics Explained "Passenger cars in the EU", revision 647912 (saved 19 Aug 2024, replaced 5 Nov 2024) | F (MediaWiki API) | **The version online on 21 Sep 2024.** "Data extracted in July 2024". Text (2023): Italy 694, Luxembourg 675, Cyprus 665, Finland 664, Estonia 630, Latvia 418, EU average 571. Figure 3 "Motorisation rate, 2023" (uploaded 25 Jul 2024, sha1 7dd8b8d6...): all 27 Member States; **Malta 12th, about 575** (France about 578 11th, Austria about 566 13th; pixel reading within 1.1 of every printed value). Table 2: Malta stock 317,234 (2022) and 323,852 (2023), as today. The 2023 text first appears in revision 646192 (23 Jul 2024). | C |
| eurostat_se_passenger_cars_rev627098 | Same article, revision 627098 (31 Jan 2024) | F (MediaWiki API) | "Data extracted in December 2023"; Figure 3 "Motorisation rate, 2022" (uploaded 16 Jan 2024): Malta sixth at about 602. | C |
| eurostat_news_20240117 | Eurostat news 17 Jan 2024 and its chart | F | Release of the 2022 figures: EU 560; Italy 684, Luxembourg 678, Finland 661, Cyprus 658; Latvia 414 lowest. **Its chart (2012 and 2022) shows Malta sixth at about 602**, Germany about 585, Poland about 571 (pixel reading within 1.2 of the printed values). Malta's 2022 value was later revised to 585 and Poland's to 584. | C |
| eurostat_road_eqs_carhab | Eurostat road_eqs_carhab (doi:10.2908/ROAD_EQS_CARHAB), today's data | F (data) | 2022: Malta 585 (no flag), 7th of 27 (all report), between Germany 587 (b) and Poland 584 (i); Italy 682, Latvia 406 (b); EU-27 564. Among all 41 countries Malta is 9th. 2023: 575, 11th (France now 573 p); 2024: 576, 13th; 2025: 571, 14th, EU 584. Malta 3rd in 11 years (1995, 1997, 2007-2012, 2014-2016); peak 616 in 2016. No flags on Malta; no value for 2003-2004. | C |
| eurostat_road_eqs_carmot | Eurostat road_eqs_carmot | F (data) | Malta stock at 31 Dec: 249,612 (2012), 313,177 (2021), 317,234 (2022), 335,693 (2025); rose every year 2006-2025. | C |
| eurostat_demo_gind | Eurostat demo_gind, population on 1 January | F (data) | Stock / population on 1 Jan of the next year reproduces road_eqs_carhab for all 27 Member States in 2022 (within 1 per 1,000). Malta 542,051 (1 Jan 2023), 588,254 (1 Jan 2026). | C |
| eurostat_reg_area3 | Eurostat reg_area3, land area | F (data) | Malta 313 km2 of land (Malta island 245; Gozo and Comino 68). 1,014 passenger cars per km2 in 2022, first of 27; Netherlands 261. | C |
| eurostat_news_20240506 / _20250521 | Eurostat regional news, 6 May 2024 and 21 May 2025 | F | Regional dataset tran_r_vehst; no Malta figures. Consulted; not cited in the report. | C |
| eurostat_se_passenger_cars | Statistics Explained "Passenger cars in the EU" (data extracted July 2026) | F (PDF) | Definition of passenger cars (includes taxis, private hire, shared and rented cars); methods "not harmonised at EU level"; registers "may include very old vehicles without signs of life". | C |
| eurostat_se_transport_equipment | Statistics Explained "Transport equipment statistics" (data extracted December 2025) | F (PDF) | 2024: EU 578; inactive vehicles may linger in registers. | C |
| warren_enoch_2010 | Warren and Enoch (2010), Island Studies Journal 5(2):193-216 | F | Malta car ownership then "the highest in the European Union"; 675 vehicles per 1,000 (different measure and years). | C |
| nso_motor_vehicles_q4_2022 | NSO release 023/2023 | S | 424,904 licensed motor vehicles at end-2022, 74.7% passenger cars (about 317,400), consistent with Eurostat's 317,234. Search summary only; PDF 403. | C ◆ |
| newsbook_2025_vehicles | Newsbook 30 Jul 2025, reporting NSO Q2/2025 | F (news) / S (NSO) | Licensed stock; vehicles "taken off the road due to restrictions" (garaged, resold, scrapped). Its passenger-car counts do not add up; not used. | C ◆ |

## How the earlier vintages were read

- Eurostat's dissemination API serves only the current vintage. Statistics Explained ignores `oldid` and `diff` for
  plain page requests (returns the current revision), but **its MediaWiki API works for scripts**:
  `api.php?action=query&prop=revisions&titles=...&rvstart=...&rvend=...` lists revisions, `revids=<id>&rvprop=content`
  returns a revision's wikitext, and `prop=imageinfo&iiprop=url|sha1|timestamp` gives each chart file's URL, upload
  time and checksum (`tools/cc-075-report/fetch_vintage.py`). Revisions scanned on 6 Oct 2026: 627098, 644029 (both
  "Data extracted in December 2023", 2022 chart, Italy 684, EU 560), and 646192, 646253, 646430, 646449, 646478,
  646525, 646741, 647044, 647912 and 655141 (all "Data extracted in July 2024", 2023 values, Italy 694, EU 571).
- The three charts (Figure 3 for 2023 and for 2022, and the January 2024 release chart) were read by pixel measurement
  (`tools/cc-075-report/read_charts.py`): bars found by colour, the scale fitted to the axis and the gridlines, and the
  result checked against every value Eurostat prints in the accompanying text (largest difference 1.2 cars per 1,000).
- Eurostat content is reused under its copyright notice (re-use authorised with acknowledgement); the chart files are
  saved in `data/cc-075/` with their checksums.

## Search log: the article's own sources

- **The European Correspondent graphic (Paula Lago).** WebSearch (two queries, 6 Oct 2026) found no copy. The article
  embeds a Lovin Malta Instagram post (`instagram.com/p/DALjVuJRIGd/`); Instagram returned a login page and no caption
  to scripts. Not read, so the data year and release the graphic used are unknown.
- **Internet Archive.** The availability API lists no capture of the article; web.archive.org reset every connection
  from this network (five tries, 6 Oct 2026) and WebFetch cannot reach it. Not needed for the vintage question once the
  Statistics Explained API was used.
- **Eurostat metadata (ESMS) for road equipment.** `road_eqs_esms.htm`, `road_esms.htm`, `road_eq_esms.htm`,
  `road_eqs_carhab_esms.htm` under `/cache/metadata/en/` and `/EN/` all returned 404. The denominator was established
  by recomputation (all 27 countries, 2022).
- **NSO and Transport Malta.** nso.gov.mt (site and the release PDF) and transport.gov.mt returned 403 to curl with a
  browser User-Agent; WebFetch also got 403 for the NSO PDF. Licensed-vehicle figures are therefore second-hand (◆).
- **Hire cars in Malta's stock.** No readable source gave the number of rented cars in Malta's licensed stock.

## Peer-reviewed literature searched

Crossref queries "car ownership Malta", "land transport policy small island state Malta", "motorisation rate vehicle
register stock inactive vehicles" (6 Oct 2026). Relevant: Warren and Enoch (2010), read in full; Attard (2005),
Transport Policy 12(1):23-33, doi:10.1016/j.tranpol.2004.09.001, closed access with no abstract in OpenAlex, so not
read and not cited. No peer-reviewed study of the comparability of national vehicle registers was found.

## The Lovin Malta page (archive record)

- Fetched 6 Oct 2026 with curl (browser User-Agent): 215,919 bytes, SHA-256
  `1482cd7d680b9c627e48207290def3916699133a1a3282ebf52c83f71f6dab38`. WordPress API (`/wp-json/wp/v2/posts/148257`)
  gives the same text, date 2024-09-21T13:15:53 UTC, modified three seconds later.
- robots.txt allows the page (disallows `/wp-admin` and `/search`; crawl-delay 600).
- The Internet Archive's availability API lists no capture of the article. **Manual task:** save a capture.
- The HTML is not committed (copyright).

## Gaps

- The data year and release used by the graphic the article relied on (Latvia 409 matches neither Eurostat's January
  2024 release, 414, nor today's data, 406).
- NSO's licensed-vehicle release (second-hand only) and the number of rented cars in Malta's stock.

## Re-read of the article, 6 Oct 2026 (audit correction, version 1.1)

- Lovin Malta WordPress API (post 148257) re-read in full on 6 Oct 2026. Paragraph 1: Eurostat "shared a dataset ... as of
  2023"; paragraph 2: a graphic "better illustrated these rankings up to the year 2022". The sentence with the rank and
  the 585 has no year. So the article gives conflicting year signals; the earlier "no year given" wording was too
  strong and was corrected.
- Two 602s: the January 2024 value for 2022 (about 602, chart reading) equals today's value for 2021 (602). The stock
  317,234 for 2022 is the same in revision 647912 (Table 2, July 2024) and in today's road_eqs_carmot; stock / 602
  implies about 527,000 people against 542,051 on 1 Jan 2023 today (data/cc-075/checks.csv). The January 2024 stock and
  population were not retrieved, so the cause of the revision is not identified.
- Vintages not seen: for September 2024 only the Statistics Explained revision and its figure; the database tables
  road_eqs_carhab and road_eqs_carmot as they stood then cannot be retrieved.
