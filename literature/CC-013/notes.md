# CC-013 literature notes

Access: F = full text, A = abstract or summary only, S = second-hand. Searches run 3 October 2026 (Crossref,
OpenAlex, Eurostat API; PA and NSO documents read in a browser because the sites block automated download).

| Key | Source | Access | Finding used | Grade |
|---|---|---|---|---|
| mt_2025_buttigieg | MaltaToday interview, 2 Mar 2025 | F | "Had we not issued these permits, Malta would face the same housing crises as other European countries. This is a supply-and-demand issue – continuing to issue permits helps keep property prices in check. Stopping them would drive prices up." The 91,000 figure is the interviewer's. | (claim) |
| pa_dwellings | PA approved dwelling units 2007-2025 | F | 87,814 units approved 2015-2024 (2,679 in 2013; 12,829 in 2018). | C |
| eurostat_housing | Eurostat | F (data) | Real house prices 2015-2025: Malta +34%, EU +25% (2015-2024: +26% vs +21%). Population 2015-2025: Malta +31%, EU +2%. Overburden: Malta 1.1% (2015) to 2.9% (2022); Eurostat flags a break in series (b) in 2023, then 6.0%, 5.9%, 6.0% (2023-2025); EU 7.7% in 2025. Malta's 2025 house-price values are provisional (p). Overcrowding: Malta 4.7%, EU 16.8%. | C |
| eurostat_eu27 (v1.2) | Eurostat demo_gind, tipsho10, prc_hicp_aind, prc_hpi_q, prc_hpi_cow (all EU-27) | F (data) | 2015-2025: Malta population +30.9% (1st of 27; LU +21.1%, IE +16.3%; EU +1.9%, so about 16.3 times, not "fifteen"); real house prices +34.2% (p), 16th of 27, median state +41.2%, PT +106.4%, HU +103.8% (p), HR +66.8%; DE +16.5%, FR +3.7%, IT -5.4%, which carry 48.9% of the EU-27 HPI weight (2025). Rents (HICP actual rentals): Malta +53.1% vs EU +20.5%, 8th of 27 (HU +105.4% first). Latest quarter: house prices +6.9% y/y in 2026-Q2 (p; nominal) vs EU +4.7%, Malta 14th of 26 (EL missing). Flags: BG, CY 2015 b; EL 2015 e, 2025 ep; EU-27 population 2015 e, 2025 ep. | C |
| nso_census2021_v2 | NSO Census 2021 vol. 2 | F (commentary) | 27.5% of dwellings not a main residence (31.8% in 2011). | C |
| glaeser2005, hilber2016, saiz2010 | Peer-reviewed | A | Supply constraints raise prices and the price response to demand. Supports the mechanism. | B |
| anenberg2020 | Peer-reviewed | A | Marginal extra supply has small effects on rents; amenities dominate. Limits the size of the effect. | B |

## Gaps

- No peer-reviewed estimate of housing supply elasticity for Malta was found. Central Bank of Malta work on
  house-price determinants exists but is not peer-reviewed; not used.
- Malta's overburden rate jumps from 2.9% (2022) to 6.0% (2023). Checked via the Eurostat API on 5 Oct 2026:
  the 2023 value carries flag b (break in time series), so only 2015-2022 and 2023-2025 are compared. The
  cause of the break (survey or method change) was not identified.
- The MDA-commissioned figure ("prices up 59% since 2017") in the candidate record was not verified and is not used.
- Approvals are not completions; completions data were not found.
