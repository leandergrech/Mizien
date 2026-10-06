# CC-114 literature and source notes

Access: F = full text, A = abstract or summary only, S = second-hand. Searches run 6 October 2026 (Crossref,
OpenAlex, Eurostat API and website, pn.org.mt, Newsbook, WebSearch).

| Key | Source | Access | Finding used | Grade |
|---|---|---|---|---|
| pn_release_2026 | PN press release, signed Eve Borg Bonello, 26 Jan 2026 (Maltese) | F | The claim (see primary-source.md). | (claim) |
| newsbook_2026 | Newsbook, J. Balzan, 26 Jan 2026 | F | English quotes; 17%/34% as paraphrase. | (locator) |
| eurostat_ddn_20260123 | Eurostat news item, 23 Jan 2026 | F | "Only Malta (+17%)"; EU −34%; Estonia −64%, Ireland −50%, Finland −44%; dataset env_ac_aeint_r2. | C |
| eurostat_map_202601 | Eurostat map file (t = 20 Jan 2026), data block embedded | F | January vintage for all 27: Malta +16.6, EU −34.0 (data/cc-114/eurostat_map_jan2026.csv). | C |
| eurostat_se_gea_2026 | Eurostat Statistics Explained, "Greenhouse gas emission accounts" (June 2026) | F (open access, CC BY 4.0) | Still says "Only Malta (+17%)"; Malta among the top four per person, transport the key activity, emissions of transport companies allocated to the country of residence; "a multitude of factors may drive greenhouse gas emissions intensity, with improving environmental performance and decarbonisation policies being only one of them"; households excluded from intensity. | C |
| eurostat_aea_meta | Eurostat ESMS metadata env_ac_ainah_r2 | F | Accounts record emissions of resident units "regardless of where these emissions actually occur geographically"; Eurostat estimates the year after the last reported (year n−1). | C |
| nso_aea_meta_mt | NSO Malta national metadata for the air emissions accounts (last update 11 Feb 2026) | F | 2023 jump in air transport (H51) "due to an increase in international aviation activity, primarily due to the activity of airlines which started operating during 2023"; air-transport source is the OECD's residence-based data; charter flights 2013-2018 estimated by the NSO; revision of 2013-2018 air transport in February 2026; data "provisional". | C |
| Eurostat datasets | env_ac_aeint_r2, env_ac_ainah_r2, env_ac_aibrid_r2 (updated 7 Aug 2026), env_air_gge (2 Jun 2026), nama_10_gdp, nama_10_a64 (6 Oct 2026), nama_10_pe (2 Oct 2026), nrg_ind_ren (15 Sep 2026) | F (data) | All figures in data/cc-114/checks.csv. Flags kept: Malta's 2024 values in the three air-emissions datasets are 'i' (imputed by Eurostat). | C |
| usubiaga2015 | Usubiaga & Acosta-Fernández 2015, Economic Systems Research 27(4):458-477, doi:10.1080/09535314.2015.1049126 | A (OpenAlex; closed access) | Residence-principle (SEEA) and territory-principle emission accounts differ; "the differences are high for many countries and their magnitude is increasing over time". | C |
| haberl2020 | Haberl et al. 2020, Environmental Research Letters 15:065003, doi:10.1088/1748-9326/ab842a | A (OpenAlex; open access, CC BY) | Relative vs absolute decoupling; relative decoupling of GHG from GDP is frequent. Context for "intensity". | C |
| CC-025, CC-003 | Miżien claim checks | F | Territorial GHG per unit of GDP since 2005: −72% (volumes), −84% (current prices); reproduced here from the same Eurostat tables. | C |
| eurostat_ddn_20251218 | Eurostat news item, 18 Dec 2025, "25.2% of energy EU used in 2024 came from renewables" | F (text) | EU 25.2%; lowest three Belgium 14.3%, Luxembourg 14.7%, Ireland 16.1%; Malta not named (the item names no other country below the top three and bottom three). Malta's 17.2% in nrg_ind_ren is fourth from last, so "third from last" was not what Eurostat's own release showed. data/cc-114/eurostat_ren_news_dec2025.csv. | C |
| CC-026 (v1.1) | Miżien claim check (same accounts, 2015-2025) | F | Air transport 444 to 4,730 kt CO2e (2015-2024), reproduced here. Rated Largely supported because the article body explained the residence vs territorial difference; its headline read alone was rated "Needs context" (026D, amber). This release never names the basis, so sub-claim D gets that amber rating. | C |

## Key numbers (recomputed in tools/cc-114-report/calc.py)

- Eurostat's indicator (GHG of resident production units per euro of GVA, chain-linked 2020), 2013-2024: Malta
  +14.3% in the August 2026 data (325.2 to 371.7 g/€; 2024 imputed by Eurostat), +16.6% in the January map; EU −34.0%
  in both. Malta is the only Member State with an increase in both vintages.
- Malta's resident production units: 2.78 Mt (2013) to 6.59 Mt (2024). Air transport (H51) 0.30 Mt to 4.73 Mt, 71.8%
  of the 2024 total; all of the rise is "fuel purchased abroad" by resident units (Eurostat bridging table: 299 of 304 kt in 2013, 100% in 2024). Electricity, gas
  and steam (D) 1.70 Mt to 0.74 Mt (−56%). Air transport accounts for 116% of the net increase.
- Components of the NACE total, 2013 to 2024 (Mt CO2e): air transport 0.30 to 4.73; electricity, gas and steam 1.70 to
  0.74; other transport (H less H51) 0.18 to 0.26; all other activities 0.59 to 0.86. They sum to the total (2.78 to
  6.59). Figure 2's "other activities" is other transport plus all other (0.77 to 1.12).
- Air-transport fuel bought abroad (bridging table): 299 of 304 kt in 2013, 100% of 4.73 Mt in 2024 (an estimate); the
  rise in fuel bought abroad (4,431 kt) is at least the rise in air transport (4,426 kt): "all of the rise".
- Bound for the renewables explanation: with zero electricity-sector (D) emissions in 2024, the indicator would be
  371.69 x (1 - 743/6,589) = 329.8 g/EUR against 325.21 in 2013 (+1.4%). Renewable shares rose over the period:
  electricity 1.6% to 10.7%, overall 3.8% to 17.2% (nrg_ind_ren).
- Base-year sensitivity of OUR counter-figures (data/cc-114/sensitivity_base_years.csv, end year 2024). Without air
  transport: a fall from every base year 2008-2023 (-8.5% to -72.3%); from 2013 -64.0% (2nd of 27, EU -35.2%), from
  2016 -29.5% (17th, EU -30.1%). Territorial inventory per euro of GDP: a fall from every base year (-6.6% to
  -69.3%); from 2013 -61.3% (2nd, EU -35.5%), from 2016 -27.1% (21st, EU -29.8%). Most of the fall came in 2014-2016
  when electricity-sector emissions fell from 1,703 to 581 kt; from 2016 they rose 28% (to 743 kt).
- In the PN's favour: from base years 2014-2019, with end year 2024, Malta's rise is +19.5% to +97.0% (sensitivity.csv
  and sensitivity_base_years.csv), larger than the +14.3% from 2013; Malta is 27th of 27 from every base year 2008-2023.
- Malta's real GVA +108.5%, EU +20.3%.
- Without air-transport emissions: Malta −64.0% (2nd largest fall in the EU-27; EU −35.2%). Without transport and
  storage in both emissions and GVA: −66.3% (2nd).
- Territorial inventory (no LULUCF, no international bunkers) per euro of GDP in volumes: Malta −61.3% (2nd after
  Estonia; EU −35.5%); at current prices −72.9%. Since 2005 (CC-025): −72.2% / −83.8%, matching CC-025.
- Sensitivity: with base 2013, Malta is the only riser only for end year 2024; 2013-2023 Malta −8.3%, no Member State
  rose. With end 2024, Malta is the only riser for base years 2013-2019; from 2008-2012 it fell (2008: −9.0%).
- Release's other figures: Estonia, Ireland, Finland "reduced emissions" by 64/50/44%: these are intensity changes.
  Emissions 2013-2024, residence accounts / territorial inventory: Estonia -55.4% / -53.1%, Ireland +13.7% / -6.9%,
  Finland -37.9% / -37.6%. 2024 flags: Estonia and Finland 'i' (imputed), Ireland 'e' (estimated); inventory
  values unflagged. Ireland's air transport (H51) 9.90 to 16.32 Mt is 87% of its rise in residence-based emissions;
  its territorial inventory fell 57.95 to 53.93 Mt. The EU-27 values of env_ac_aeint_r2 are flagged 'i' in all years. Renewables: 10.7% is Malta's share in
  electricity (10.66% in 2024, lowest in the EU; EU 47.5%); the "just over 25%" is the EU's overall share (25.2%);
  Malta's overall share is 17.2%, fourth from last (Belgium 14.3, Luxembourg 14.7, Ireland 16.1).

## Search log for statements of absence

- "Eurostat and the NSO do not name the airlines": searched the NSO national metadata (full text, 6 Oct 2026), the
  Eurostat ESMS metadata and the Statistics Explained article (full text); none names an operator. We did not
  search company filings, so the report does not name any airline.
- "No January capture of the PN release": Internet Archive availability API with timestamp 20260126 returned
  30 May 2026 as the closest capture; the CDX listing could not be read (connection reset), so earlier captures cannot
  be ruled out completely.
- "No English version of the release": pn.org.mt press-release sitemap lists only the Maltese URL (hreflang mt and
  x-default), read 6 Oct 2026.
- `sdg_13_20` and `nrg_ind_ghg` (GHG intensity of energy consumption, a candidate indicator in the brief) returned
  HTTP 404 from the Eurostat API on 6 Oct 2026, and no such dataset appears in the API's table of contents; the
  release's own definition and map identify env_ac_aeint_r2 in any case.

- "The PN release never names the residence basis, aviation or fuel bought abroad": the saved page (6 Oct 2026) was
  searched by script for Maltese stems for aviation, flights, airlines, fuel, transport, residence, territory,
  inventory and bunkers; none occurs. The one transport-related word is *traffiku* (traffic), item 9 of
  primary-source.md. The saved page is the version modified 24 Apr 2026; no January copy was found (above).
- "Eurostat's December 2025 release does not name Malta among the lowest three": the news item's text was read in
  full on 6 Oct 2026; it names only the highest three and the lowest three. It does not give Malta's value, so
  Malta's rank rests on nrg_ind_ren (17.2%, fourth from last).

## Gaps

- 2024 values in the air emissions accounts are Eurostat's estimates (flag i); Malta reported to 2023. The rise "since
  2013" depends on that estimate.
- We did not read the OECD residence-based aviation data behind Malta's air transport figures, or any company
  filing, so which airlines are resident is not established here.
- The GVA of air transport (nama_10_a64, H51) is negative in volumes for 2022-2024 and not published for 2013 (no value in the API), so the
  "without air transport" measure removes emissions only; removing the whole transport section (H) from both sides
  gives a similar result (−66%).
- MaltaToday's report of the statement was not readable (403); not relied on.

## Version 1.1 (6 Oct 2026): audit corrections
No new searches. Added to calc.py: air transport alone per euro of total GVA (35.6 g/EUR in 2013, 265.5 in 2024, estimate flag i), an explicit test that zeroing electricity (NACE D) alone leaves 2024 (329.8) above 2013 (325.2), and the 2024 air-transport value with its flag (4,730 kt, i). Confidence lowered to Moderate: sub-claims D and F share the same Eurostat accounts, including the imputed 2024 value.
