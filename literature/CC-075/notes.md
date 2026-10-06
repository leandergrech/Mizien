# CC-075 literature notes

Access: F = full text, A = abstract or summary only, S = second-hand.
Searches and downloads run 6 October 2026 (Eurostat API and news pages, Eurostat Statistics Explained PDFs, Crossref,
OpenAlex, DataCite, WebSearch, Lovin Malta page and WordPress API, Newsbook).

| Key | Source | Access | Finding used | Grade |
|---|---|---|---|---|
| lovin_2024_cars | Lovin Malta (J. Darmanin), 21 Sep 2024 | F | The claim, in the outlet's own words (no quotation marks; Lovin is the speaker): "according to the statistics Malta is ranked number seven, just between Germany and Poland respectively, with 585 cars per 1,000 inhabitants". Also: Eurostat "shared a dataset detailing the unit of cars per thousand residents in each European country as of 2023"; a graphic by Paula Lago via The European Correspondent "better illustrated these rankings up to the year 2022"; Italy top at 682, Latvia lowest at 409; "approximately 1 car for every 2 people"; "with just 246 square kilometres of land, Malta is also up there among the countries with the highest car density in Europe". No year is given for the 585. | (claim) |
| eurostat_road_eqs_carhab | Eurostat road_eqs_carhab (doi:10.2908/ROAD_EQS_CARHAB) | F (data) | 2022: Malta 585 (no flag), 7th of 27 (all 27 report), between Germany 587 (b, break in series) and Poland 584 (i, imputed); Italy 682 top, Latvia 406 (b) lowest; EU-27 564. Among all 41 countries in the dataset Malta is 9th (Liechtenstein 773, Iceland 611 'i' also above). 2023: 575, 11th; 2024: 576, 13th, EU 577; 2025: 571, 14th, EU 584. Malta 3rd in 11 years (1995, 1997, 2007-2012, 2014-2016); peak 616 in 2016. No flags on any Malta value; no Malta value for 2003-2004. | C |
| eurostat_road_eqs_carmot | Eurostat road_eqs_carmot | F (data) | Malta stock at 31 Dec: 249,612 (2012), 313,177 (2021), 317,234 (2022), 335,693 (2025); it rose every year 2006-2025. | C |
| eurostat_demo_gind | Eurostat demo_gind, population on 1 January | F (data) | Malta 520,174 (2022), 542,051 (2023), 588,254 (2026). Stock / population on 1 Jan of the next year reproduces road_eqs_carhab for all 27 Member States in 2022 (within 1 per 1,000), so the denominator is the end-of-year population. | C |
| eurostat_reg_area3 | Eurostat reg_area3, land area | F (data) | Malta 313 km2 of land (MT001 Malta island 245; MT002 Gozo and Comino 68). Malta 1,014 passenger cars per km2 of land in 2022, first of 27; the Netherlands second at 261. | C |
| eurostat_news_20240117 | Eurostat news 17 Jan 2024 | F | The release of the 2022 figures: EU 560; Italy 684, Luxembourg 678, Finland 661, Cyprus 658; Latvia 414 lowest. Malta's passenger-car rate is not mentioned. The dataset has been revised since (Italy 682, Luxembourg 673, Cyprus 633, Latvia 406, EU 564). | C |
| eurostat_news_20240506 / _20250521 | Eurostat regional news, 6 May 2024 and 21 May 2025 | F | EU 0.56 cars per inhabitant in 2022; 0.55 in 2023. No Malta figures. | C |
| eurostat_se_passenger_cars | Statistics Explained "Passenger cars in the EU" (data extracted July 2026) | F (PDF) | Definition of passenger cars (includes taxis, private hire, shared and rented cars); methods "not harmonised at EU level"; registers "may include very old vehicles without signs of life (roadworthiness test, insurance, etc.)". | C |
| eurostat_se_transport_equipment | Statistics Explained "Transport equipment statistics" (data extracted December 2025) | F (PDF) | 2024: EU 578 and 12 countries above it; "some vehicles no longer on the road may still linger in certain national vehicle registers". | C |
| warren_enoch_2010 | Warren and Enoch (2010), Island Studies Journal 5(2):193-216 | F | Malta vignette: car ownership "now the highest in the European Union"; vehicle ownership 675 per 1,000; modal share of private car trips from about 55% (1989) to over 70% (2002). Year and definition differ from road_eqs_carhab, whose current vintage puts Malta 3rd in 2007-2012. | C |
| nso_motor_vehicles_q4_2022 | NSO release 023/2023 | S | 424,904 licensed motor vehicles at end-December 2022, 74.7% passenger cars (about 317,400; range 317,191-317,616 for 74.65-74.75%), consistent with Eurostat's 317,234. Search summary only; PDF refused (403). | C ◆ |
| newsbook_2025_vehicles | Newsbook 30 Jul 2025, reporting NSO Q2/2025 | F (news) / S (NSO) | NSO counts licensed vehicles; 9,366 vehicles were "taken off the road due to restrictions" in Q2 2025 (39.4% garaged, 29.6% resold, 29% scrapped). Its passenger-car counts do not add up and are not used. | C ◆ |

## Search log: the article's own sources and the data vintage

- **The European Correspondent graphic (Paula Lago).** WebSearch (two queries, 6 Oct 2026) found no copy. The article
  embeds a Lovin Malta Instagram post (`instagram.com/p/DALjVuJRIGd/`); Instagram returned a login page and no caption
  to scripts. Not read.
- **Eurostat data as of September 2024.** Eurostat's API serves only the current vintage. The Internet Archive's
  availability API lists no capture of the API URL; it lists a capture of the databrowser table (1 Dec 2024, a
  JavaScript page) and of the "Passenger cars in the EU" PDF (25 Feb 2024,
  `web.archive.org/web/20240225054426/https://ec.europa.eu/eurostat/statistics-explained/SEPDF/cache/25886.pdf`), but
  web.archive.org reset every connection from this network (five tries, 6 Oct 2026) and WebFetch cannot reach it.
  Statistics Explained ignores `oldid` and `diff` for scripts (returns the current revision). So we cannot show what
  the dataset held on 21 Sep 2024, nor whether any 2023 values were already published then.
- **Eurostat metadata (ESMS) for road equipment.** `road_eqs_esms.htm`, `road_esms.htm`, `road_eq_esms.htm`,
  `road_eqs_carhab_esms.htm` under `/cache/metadata/en/` and `/EN/` all returned 404. The denominator was established
  instead by recomputation (all 27 countries, 2022).
- **NSO and Transport Malta.** nso.gov.mt (site and the release PDF) and transport.gov.mt returned 403 to curl with a
  browser User-Agent; WebFetch also got 403 for the NSO PDF. Licensed-vehicle figures are therefore second-hand (◆).
- **Hire cars in Malta's stock.** No readable source gave the number of rented or hire cars in Malta's licensed
  stock (NSO and Transport Malta refused). Not quantified.

## Peer-reviewed literature searched

Crossref queries "car ownership Malta", "land transport policy small island state Malta", "motorisation rate vehicle
register stock inactive vehicles" (6 Oct 2026). Relevant: Warren and Enoch (2010), read in full; Attard (2005),
Transport Policy 12(1):23-33, doi:10.1016/j.tranpol.2004.09.001, closed access with no abstract in OpenAlex, so not
read and not cited. No peer-reviewed study of the comparability of national vehicle registers was found; Eurostat's
own methodological statements are used instead.

## The Lovin Malta page (archive record)

- Fetched 6 Oct 2026 with curl (browser User-Agent): 215,919 bytes, SHA-256
  `1482cd7d680b9c627e48207290def3916699133a1a3282ebf52c83f71f6dab38`. WordPress API (`/wp-json/wp/v2/posts/148257`)
  gives the same text, date 2024-09-21T13:15:53 UTC, modified three seconds later.
- robots.txt allows the page (disallows `/wp-admin` and `/search`; crawl-delay 600).
- The Internet Archive's availability API lists no capture of the article. **Manual task:** save a capture.
- The HTML is not committed (copyright).

## Gaps

- The vintage of the data the article used (its Latvia figure, 409, matches neither Eurostat's January 2024 release,
  414, nor the current dataset, 406).
- Whether Eurostat had published any 2023 values by 21 Sep 2024.
- NSO's licensed-vehicle release (second-hand only) and the number of hire cars in Malta's stock.
