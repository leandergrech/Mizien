# CC-009 primary wording and records

**Checked:** 3 October 2026

## WSC Annual Report 2025

The report's potable-water section states that 2025 total production was 39.5 million m³ and that 70.7% came from the four reverse-osmosis plants. It also reports groundwater production of 11.5 million m³, the lowest annual total in the preceding decade, and says it was 11.4% below 2024. WSC attributes that reduction to achieving lower blended salinity in reservoirs.

The report's Figure 20 provides annual reverse-osmosis and groundwater production values for 2022–2025. Recalculation from the chart values produces an 11.86% groundwater decline from 2024 to 2025, rather than the 11.4% in the prose. This is retained as an unresolved internal discrepancy. The 2025 report's 2022 historical groundwater value differs by 486 m³ from the rounded-period source value in the 2022 report; this is immaterial to the ratios shown and is noted in the data file.

Source: https://parlament.mt/media/139352/wsc-annual-report-2025.pdf, pp. 40–43.

## WSC tender notice

WSC's 25 August 2026 notice says it “issued a public tender” for a new reverse-osmosis plant at Għar Lapsi. The planned Plant B comprises six systems with a combined capacity of 30,000 m³/day. The European Union's procurement notice identifies the procedure as WSC/T/064/2026, published 28 August, with bids due 30 October 2026. These are tendered works and proposed capacity, not operating production.

Sources: https://www.wsc.com.mt/wsc-issues-e35-million-tender-for-new-ghar-lapsi-reverse-osmosis-plant/ and https://op.europa.eu/en/web/public-procurement/procurement-details/-/procurement/c70c57b4-61a5-4c26-a365-dc44067d6687.

## Groundwater status

The latest plan listed by ERA is Malta's 3rd River Basin Management Plan for 2021–2027. Chapter 6 says the Malta and Gozo Mean Sea Level aquifer systems are in poor quantitative status. It classifies 14 groundwater bodies as poor chemically, with nitrate the main failing parameter; the nitrate section names three bodies that do not exceed the 50 mg/L nitrate standard. The plan says overall status is poor for all assessed groundwater bodies because good overall status requires both quantitative and qualitative status to be good.

Source: ERA/EWA, *3rd River Basin Management Plan for Malta*, Chapter 6 (final status assessment): https://era.org.mt/wp-content/uploads/2023/09/3rd-River-Basin-Management-Plan-MALTA-Chapter-6-Assessment-of-Status-Final.pdf.

The RBMP is a separate status assessment from WSC's potable-water production series. A reduction in WSC's groundwater component is not by itself evidence that aquifer levels, salinity or chemical status have recovered. Private, agricultural and other abstraction volumes are not included in the WSC production denominator used here; the report does not assert that total national abstraction is unquantified.

## Corrections check, 5 October 2026 (v1.1)

**Groundwater-body status: plan versus EU reporting.** Malta's WFD reporting to the EEA was queried directly from the WISE map services (layer 0, `where=countryCode='MT'`, `outFields=*`, status codes 2 = Good and 3 = Poor per each layer's legend):

- 3rd cycle, `WFD2022_GroundWaterBody_WM` (status assessed 2021): 4 of 15 bodies poor quantitatively (MT001 Malta Mean Sea Level, MT013 Gozo Mean Sea Level, MT005 Pwales Coastal, MT010 Marfa Coastal); 15 of 15 poor chemically.
- 2nd cycle, `WFD2016_GroundWaterBody_WM` (status assessed 2010–2014): 2 poor quantitatively (MT001, MT013); 12 poor chemically (good: MT006 Miżieb Mean Sea Level, MT009 Mellieħa Coastal, MT012 Comino Mean Sea Level).

Per-body rows, query URLs and the retrieval date are in `data/cc-009/wise_gwb_status.csv`. The Chapter 6 record above names the Malta and Gozo Mean Sea Level systems as poor quantitatively and records 14 bodies poor chemically. It does not say that only those two are quantitatively poor; the earlier "2 poor" count was our inference. The 14 versus 15 chemical count is a real difference between the plan as recorded here and Malta's EU reporting for the same cycle. The plan could not be re-opened (ERA returns 403 to scripts), so the report shows both sources. A search-engine summary of the consolidated plan mentions the plan's objectives for the Pwales and Marfa Coastal bodies, which may mean the plan's tables also treat them as poor. That summary is second-hand and unverified; check Chapter 6's groundwater status tables in a browser.

**"Lowest in a decade".** The record above attributes this to WSC's 2025 report ("the lowest annual total in the preceding decade"; paraphrase, not a verbatim quote). The repo's own series (Figure 20) covers 2022–2025 only, so the outputs now attribute the decade comparison to WSC. The exact wording could not be re-checked: parlament.mt returns 403 to scripts.

**Reference [6].** The WSC Annual Report 2022 is now cited in section 2 for the 486 m³ difference in the 2022 groundwater value (see `data/cc-009/wsc_production.csv`). The difference changes neither the 64.3% share nor the 8.95% change.
