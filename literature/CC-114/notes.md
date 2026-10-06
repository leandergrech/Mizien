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

## Key numbers (recomputed in tools/cc-114-report/calc.py)

- Eurostat's indicator (GHG of resident production units per euro of GVA, chain-linked 2020), 2013-2024: Malta
  +14.3% in the August 2026 data (325.2 to 371.7 g/€; 2024 imputed by Eurostat), +16.6% in the January map; EU −34.0%
  in both. Malta is the only Member State with an increase in both vintages.
- Malta's resident production units: 2.78 Mt (2013) to 6.59 Mt (2024). Air transport (H51) 0.30 Mt to 4.73 Mt, 71.8%
  of the 2024 total; all of it is "fuel purchased abroad" by resident units (Eurostat bridging table). Electricity, gas
  and steam (D) 1.70 Mt to 0.74 Mt (−56%). Air transport accounts for 116% of the net increase.
- Malta's real GVA +108.5%, EU +20.3%.
- Without air-transport emissions: Malta −64.0% (2nd largest fall in the EU-27; EU −35.2%). Without transport and
  storage in both emissions and GVA: −66.3% (2nd).
- Territorial inventory (no LULUCF, no international bunkers) per euro of GDP in volumes: Malta −61.3% (2nd after
  Estonia; EU −35.5%); at current prices −72.9%. Since 2005 (CC-025): −72.2% / −83.8%, matching CC-025.
- Sensitivity: with base 2013, Malta is the only riser only for end year 2024; 2013-2023 Malta −8.3%, no Member State
  rose. With end 2024, Malta is the only riser for base years 2013-2019; from 2008-2012 it fell (2008: −9.0%).
- Release's other figures: Estonia, Ireland, Finland "reduced emissions" by 64/50/44%: these are intensity changes;
  their emissions changed −55.4%, +13.7% (Ireland's rose) and −37.9%. Renewables: 10.7% is Malta's share in
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

## Gaps

- 2024 values in the air emissions accounts are Eurostat's estimates (flag i); Malta reported to 2023. The rise "since
  2013" depends on that estimate.
- We did not read the OECD residence-based aviation data behind Malta's air transport figures, or any company
  filing, so which airlines are resident is not established here.
- The GVA of air transport (nama_10_a64, H51) is negative in volumes for 2022-2024 and not published for 2013 (no value in the API), so the
  "without air transport" measure removes emissions only; removing the whole transport section (H) from both sides
  gives a similar result (−66%).
- MaltaToday's report of the statement was not readable (403); not relied on.
