# CC-113 literature and source notes

Access: F = full text, A = abstract or summary only, S = second-hand, D = data.
Searches and downloads run 6 October 2026 (curl/urllib with a browser User-Agent; Crossref, OpenAlex, doi.org;
web searches for the EEA sentence, the Commission's subsidy reports and the IMF and OECD data).

| Key | Source | Access | Finding used | Grade |
|---|---|---|---|---|
| eea_ffs_indicator | EEA, *Fossil fuel subsidies in Europe* (indicator), published 29 Jan 2025, modified 29 Jul 2025 | F | The claim (verbatim below). EU FFS EUR 111bn in 2023; data source "DG ENER study on energy subsidies"; definition: WTO ASCM categories (direct transfers, tax expenditures, income or price support, RD&D). Methodology note still says data "deflated to 2022 prices" and cites the 2023 State of the Energy Union report, while the figures are in 2023 prices: leftover text from the previous edition. Calls the Commission report "forthcoming", though COM(2025) 17 was adopted on 28 Jan 2025 (the report itself is dated "Brussels, 28.1.2025"; the DG ENER news item of 29 Jan 2025 does not give that date). | C |
| eea_ffs_snapshots | EEA PDFs of the indicator: browser print created 3 Feb 2025 (8th EAP monitoring publication); 8th EAP monitoring report 2025 indicator PDF (modified 26 Nov 2025) | F | Same sentence, word for word. The 3 Feb 2025 copy labels the linked chart "Additional figure: Fossil fuel subsidies as a share of national gross domestic products, 2020"; the live page says "2023" (the chart itself is for 2023). | C |
| eea_ffs_charts | EEA chart pages and data packages: share of GDP 2023 (modified 7 May 2025); Figure 2 by Member State 2015 and 2023 (Data-package FIG2-278165-SUFI002-v2, Dec 2024); Figure 1 by vector (FIG1-278164-SUFI002-v3, Jan 2025) | D | Shares: MT 3.37%, PL 2.09%, SK 1.51%, HR 1.15%, BG 1.10%, EU-27 0.66%; lowest AT 0.07%, DK 0.08%, EE 0.12%. Malta EUR 0.633bn in 2023 (EUR 0.011bn in 2015). Figure note: "Data for 2023 are provisional as fossil fuel subsidy figures (about 7% of total) are still under evaluation, with 2022 data used as a proxy." Data licence: EEA standard re-use policy (source acknowledged). | C |
| eea_soer2025_malta | EEA, *Europe's environment 2025*, Malta: fossil fuel subsidies (chart, published 29 Sep 2025) | D | Malta 0.09% (2015) to 0.10% (2020), 1.33% (2021), 1.71% (2022), 3.37% (2023); EU 0.38% (2015) to 0.66% (2023). Lists Eurostat GDP as a source, but the values equal the Commission inventory's own shares, computed with the inventory's GDP series (IMF/World Bank via Enerdata), not Eurostat's. | C |
| ec_inventory_2024 | European Commission (DG ENER; Enerdata, Trinomics), *Inventory of energy subsidies in the EU27 – 2024 edition* (database dated 6 Sep 2024; file modified 9 Apr 2025), published with COM(2025) 17 on CIRCABC. **Copyright notice: see "Licence of the Commission database" below; measure rows are not committed.** | D (full database, read locally) | The data behind the EEA chart. Rebuilt from its measure rows (techno group "Fossil fuels", no double counting; for "TBC" measures with no 2023 value, the 2022 value): every EEA number reproduced to two decimals. GDP used: Enerdata from IMF and World Bank (Malta 2023 EUR 18,797m; Eurostat now EUR 20,915m). Malta 2023: "Energy Support Measures" EUR 580m (natural gas; income or price support, consumer price guarantee (cost support); crisis measure; description: "energy prices are frozen to their pre-COVID levels as the Governement is compensating Enemalta for the losses"), Gas Stabilisation Fund EUR 15m, three excise exemptions (inland navigation 6.8, fishing 1.3, domestic aviation 0.4), Melita TransGas pipeline 1.2; the excise cut on petrol and diesel is TBC (2022 value EUR 28.2m used as proxy). Total EUR 604.7m, or 632.9m with the proxy. | C |
| ener_news_20250129 | DG ENER news, "Energy subsidies report shows progress in 2023", 29 Jan 2025 | F | The 2024 report (COM(2025) 17): EU energy subsidies EUR 354bn in 2023; FFS EUR 111bn, 18% down on 2022. | C |
| com_2025_17 | European Commission, 2024 Report on Energy subsidies in the EU, COM(2025) 17 final, Brussels 28.1.2025 (CELEX 52025DC0017) | F (xhtml from the EU Publications Office; EUR-Lex itself refused scripts) | Read 6 Oct 2026 from http://publications.europa.eu/resource/cellar/7150e5a9-dd6f-11ef-be2a-01aa75ed71a1.0017.03/DOC_1 (SHA-256 in `data/cc-113/raw_files_sha256.csv`). Figure 16 "Fossil fuel subsidies compared to GDP (%, 2015 and 2023)" (source: Enerdata, Trinomics, 2024) is a bar chart with no table; we measured the 2023 bars by pixel (`tools/cc-113-report/measure_fig16.py`): MT 3.37 (3.367), PL 2.09 (2.091), SK 1.51 (1.507), HR 1.15 (1.152), BG 1.10, HU 1.01, DE 1.00, LT 0.89, EL 0.86, PT 0.82 (±0.01), all within 0.001 points of variant A (the EEA basis). Bars below about 0.8% are crossed by the EU-27 dashed line and the 2015 markers and read too low by this method (Belgium 0.65 against 0.76 by eye): not used. Footnote 6: data under "To be confirmed" were 8% of the 2023 total. This fixes the values as of 28 Jan 2025; the CIRCABC file we rebuilt from was modified on 9 Apr 2025, so for the top ten countries the CIRCABC values equal the chart of 28 Jan 2025. The text mentions Malta only in a footnote (solar over 50% of RES subsidies). | C |
| com_2026_472 | European Commission, Report on energy subsidies in the EU, COM(2026) 472 final, 17 Sep 2026 (Council ST 13343/26) | F | Seventh annual report, covering 2024 (2025 edition of the study, Enerdata and Trinomics). EU FFS 2023 revised to EUR 121bn (2024 prices; "EUR 120 billion" elsewhere in the same report); 2024 EUR 97bn, 0.5% of EU GDP. Figure 15 (p.14 of the Council PDF): Malta has the highest FFS per unit of GDP in 2024 (bar about 0.018, read from the chart; no table), FFS 80% of Malta's energy subsidies, almost all with no planned end date or one after 2030. Methodology "outlined in the Annex"; reporting under Article 35(n) of Regulation (EU) 2018/1999. | C |
| soteu_2024_page | DG ENER, 9th report on the state of the energy union (page; https://energy.ec.europa.eu/strategy/energy-union/ninth-report-state-energy-union_en; published 29 Jan 2025, modified 30 Jul 2026) | F | Lists "Energy subsidies report (COM/2025/17), and the subsidy database (xl file)" under "Reports and annexes": the subsidy report accompanies the State of the Energy Union. | C |
| nill_2024 | Nill, J. (2024), *Fossil Fuel Subsidies in EU Member States – Trends and Analytical Challenges*, European Economy Discussion Paper 214, DG ECFIN, doi:10.2765/28177 | F | Definitions side by side (pp. 6–8 printed): OECD inventory (budget transfers and tax expenditures, incl. transfer of risk); IEA price gap (end-use price vs reference price, no tax measures); IMF adds unpriced external costs ("implicit"); the EU inventory follows the OECD/WTO approach, codified by Implementing Regulation (EU) 2022/2299, excludes transfer of risk; electricity subsidies attributed to fossil fuels by the power-mix share; tax-expenditure benchmarks differ by country. Author's views, not the Commission's. DOI registered with the EU Publications Office (RA "OP"), resolves to catalogue KC-BD-23-031-EN-N (matches the PDF); not in Crossref or DataCite. | C |
| dbp_2024_mt | Government of Malta, Draft Budgetary Plan 2024 (Oct 2023), section 3.1, PDF p.34 (printed p.30) | F | Energy support (cuts to indirect taxes on energy; subsidies for the higher cost of imported fuels, electricity "and other basic commodities"): "expected to amount to 1.7 per cent of GDP in 2023, 0.8 percentage points lower than in 2022" (so 2.5% in 2022). | C |
| dbp_2025_mt | Government of Malta, Draft Budgetary Plan 2025 (Oct 2024), PDF p.40 (printed p.36) | F | Keeping energy and basic-commodity costs unchanged: 0.72% of GDP in 2025, 0.15 points less than 2024 (so 0.87% in 2024). | C |
| imf_cr2629 | IMF Country Report 26/29, Malta: 2025 Article IV (Feb 2026), Table 2, PDF p.33; doi:10.5089/9798229038249.002 | F (read for CC-022, 5 Oct 2026; not re-opened, imf.org refused scripts on 6 Oct) | Energy subsidies (untargeted electricity and fuel) 1.8% of GDP 2022, 1.4% 2023, 0.9% 2024, 0.8% 2025 (proj.). Crossref title "Malta", IMF Staff Country Reports 2026/029 (checked 6 Oct 2026). | C |
| imf_ffs_2023 | Black, Liu, Parry, Vernon(-Lin) (2023), *IMF Fossil Fuel Subsidies Data: 2023 Update*, IMF WP 23/169, doi:10.5089/9798400249006.001; data via IMF Climate Data dashboard | A + D | Price-gap method: explicit = supply cost above retail price; implicit = unpriced externalities and forgone VAT. Malta's explicit subsidies are zero in every year 2015–2025; explicit + implicit 2.86% (2022), 2.27% (2023), 15th of 27 both years. Published Aug 2023, so 2023 values were estimated before that year ended. The dashboard still serves the 2023 update; a 2025 update (WP 2025/270) exists, its country data not obtained (imf.org and elibrary refused scripts). | C |
| oecd_iisd_tracker | OECD/IISD Fossil Fuel Subsidy Tracker, country data, 2024 update (file Jan 2026) | D | Malta's rows come only from the IMF (no OECD-inventory or IEA rows); USD 0 in 2016–2024. The OECD inventory and the IEA price-gap estimates do not cover Malta. | C |
| eurostat_nama_10_gdp | Eurostat, GDP at current prices (doi:10.2908/NAMA_10_GDP), updated 6 Oct 2026 | D | Malta 2023 EUR 20,914.5m, Poland 751,931.7m, Slovakia 123,538.7m, EU-27 17,294,868.6m; no flags for 2023. | C |
| eurostat_nrg_cb_e | Eurostat, electricity supply, transformation and consumption (doi:10.2908/NRG_CB_E; DataCite checked 6 Oct 2026), Malta 2023, updated 11 Sep 2026 | D | Gross electricity production 2,344.3 GWh, imports 648.4 GWh, exports 26.2 GWh; imports are 21.7% of production plus imports (2,992.7 GWh). No flags. Used for the caveat that the database books the Enemalta line wholly to natural gas. | C |
| eurostat_gov_10a_main | Eurostat, general government subsidies D.3 (doi:10.2908/GOV_10A_MAIN), Malta | D | All-purpose subsidies EUR 195m (2019), 698m (2021), 824m (2022), 660m (2023), 509m (2024). | C |
| swd_2024_618 | European Commission, 2024 Country Report – Malta, SWD(2024) 618 final, 19 Jun 2024, PDF p.3 | F | In 2023, HICP inflation "reached 5.6% with energy prices being kept at 2020 levels". | C |
| bohm_peterson2024 | Böhm, J. & Peterson, S. (2024), Fossil Fuel Subsidy Inventories vs. Net Carbon Prices, *The Energy Journal* 45(4):59–79, doi:10.1177/01956574241277304 | A | Peer-reviewed. Subsidy inventories and carbon prices give different pictures of the price incentive on fossil fuels; proposes a net carbon price indicator (8 countries, 2018; not Malta). Abstract read via Crossref, 6 Oct 2026. | C |
| rentschler2017 | Rentschler, J. & Bazilian, M. (2017), Reforming fossil fuel subsidies: drivers, barriers and the state of progress, *Climate Policy* 17(7):891–914, doi:10.1080/14693062.2016.1169393 | A | Review; "discusses common definitions" and estimates of fossil-fuel subsidies. Open access (CC BY-NC-ND); not committed (not needed beyond the abstract). Crossref and OpenAlex checked 6 Oct 2026. | C |

## Licence of the Commission database (decision of 6 Oct 2026)

The workbook's "Table of content" sheet says: "© Copyright Enerdata. Reproduction and diffusion prohibited (web,
photocopy, intranet...) without written permission." This repository is public, so we do not redistribute the
database's measure rows. A first, unpublished version of this check held a measure-level extract
(`ec_inventory_measures.csv`); it was removed with `git rm`, and the extract now exists only on the machine that
rebuilds it (`tools/cc-113-report/out/`, git-ignored).

What is committed from the workbook, and why this is within what the coordinator allowed:

- country-level aggregates only: country x year totals (`ec_inventory_ffs_by_country.csv`, the workbook's own pivot,
  2018-2023 and "2023 incl. TBC"), the shares of GDP it prints (`ec_inventory_ffs_share_gdp.csv`) and the GDP series it
  used (`ec_inventory_gdp.csv`);
- `ec_inventory_malta_facts.csv`: the five Malta figures the report states (580 / 15 / 28.2 to be confirmed / 8.5 /
  1.2, EUR million, with their 2022 values, cost basis and classification), with the source cited. The three excise
  exemptions are added together; the measure rows are not reproduced.

Everyone can regenerate the rest: `fetch.py` downloads the workbook from the CIRCABC REST address, checks it against
the SHA-256 recorded on 6 Oct 2026 (`bf2b412b...`, 2,672,733 bytes; it warns if the file has changed) and writes the
measure-level rows to the git-ignored `tools/cc-113-report/out/`, where `calc.py` uses them to check that the pivot
totals equal the sum of the measure rows (largest difference 0.0). We have not asked Enerdata or DG ENER for written
permission; if the maintainer wants the measure table published, that permission is needed first. The licence of the
IMF Climate Data dashboard file and of the OECD/IISD tracker file (both committed in part as country-level series) was
not checked line by line; neither carries a prohibition we saw, but we did not search for their terms.

## The wording (verbatim)

EEA indicator page, read 6 Oct 2026 (page published 29 Jan 2025, modified 29 Jul 2025):

> The extent to which fossil fuel subsidies contribute to national economies also varies considerably across Member
> States. In 2023, fossil fuel subsidies represented the highest shares of gross domestic product (GDP) in Malta,
> Poland, and Slovakia (all at or above 1.5%). Countries with the lowest shares were Austria, Denmark, and Estonia
> (less than 0.2% of GDP).

Identical in the EEA's browser-printed copy of 3 Feb 2025 and in the 8th EAP monitoring report 2025 PDF (26 Nov
2025). What changed by 29 Jul 2025 could not be established (no archive service reachable); the only difference we
found between 3 Feb 2025 and now is the label of the linked chart ("2020" then, "2023" now).

## Hashes of documents read (SHA-256)

- EEA browser print, 3 Feb 2025 (`.../monitoring-progress-towards-8th-eap-objectives/indicators/19-fossil-fuel-subsidies/@@download/file`), 457,338 bytes: `86a888ac448da6a4ce044e1224be18f79fd241216b2668101b02223ed1338c5c`
- EEA 8th EAP monitoring report 2025 indicator PDF, 412,193 bytes: `16fe81bb71c375474892a78edaf1d81c4548b12e14f0c7f77bc1eadc6099c534`
- Council ST 13343/26 (COM(2026) 472), 1,035,824 bytes: `a8ee810223bb3e143bcfbe4667d4289e47c1547400b9721d61408a3a0a5056d1`
- Malta DBP 2024, 1,914,372 bytes: `56f992cbaa5e68c1c472e6f0e7b80cff3e5f4812356398a1fbffa73b139479e3`
- Malta DBP 2025, 2,613,613 bytes: `c8259bdc59eec84366e3d16c04f94513aeb864477014f870d0e2d91b00a68777`
- ECFIN Discussion Paper 214, 777,630 bytes: `f9721b2deed92a828a170a7559eaefef2dc6c0c9c7bf32b87c07375bffcd6522`
- SWD(2024) 618, 2,076,008 bytes: `ddea80873a10db07e28b25f968121a01192e831041c2869436aaf42909499577`
- Live EEA pages, chart data packages, the CIRCABC database, COM(2025) 17 (xhtml), Eurostat, IMF and tracker files: `data/cc-113/raw_files_sha256.csv`.

## Search log (statements that something was not found)

- "The IMF price-gap database records no explicit subsidy for Malta": IMF Climate Data dashboard CSV (all indicators,
  2015–2030), 6 Oct 2026; the 2025 update's country data were not obtained.
- "The OECD inventory and IEA estimates do not cover Malta": OECD/IISD tracker full data (all sources, 2010–2024),
  6 Oct 2026: Malta's only source is the IMF. We did not search the OECD's own database separately.
- "We could not reconcile Malta's EUR 580m (2023)": searched the inventory (measure description), Malta's DBP 2024 and
  2025, the Commission country report 2024, Eurostat gov_10a_main, IMF CR 26/29 (CC-018/CC-022 records) and the text
  of COM(2025) 17 (word search "Malta": one footnote on solar subsidies, nothing on this measure). The 2025 edition of
  the study (op.europa.eu, 403) and Malta's Financial Estimates (gov.mt, 403 to scripts) were not read.
- "We did not find why Malta's frozen prices do not register in the IMF price-gap database": the IMF dataset and the abstract
  of WP 23/169 only; the paper's text was not read.

## Gaps

- COM(2025) 17 gives the 2023 shares only as a chart (Figure 16); bars below about 0.8% could not be measured reliably, so only the top ten countries were compared with the CIRCABC file (all within 0.001 points).
- The 2025-edition database (final 2023 values) was not found on CIRCABC or elsewhere; COM(2026) 472 gives only
  charts by country (Malta first in 2024).
- The original 29 Jan 2025 page could not be opened (archives unreachable); the earliest copy read is 3 Feb 2025.
- No peer-reviewed study of Malta's energy price stabilisation was found. Crossref searches on 6 Oct 2026 ("Malta
  energy subsidies", "Malta electricity price freeze", "Enemalta energy prices fixed subsidy"; OpenAlex returned 429
  rate limits) found one working paper: Rapa, N. (2025), *Energy Subsidies in Malta: Estimating the Effects of
  Current Policies and Hypothetical Exit Strategies*, Central Bank of Malta Discussion Paper 4/2025 (SSRN posted
  content, doi:10.2139/ssrn.5353671, Crossref checked). Not peer-reviewed; the PDF returned 403
  (centralbankmalta.org) and was not read. Known only through Newsbook (21 Jul 2025): models the fixed-price policy;
  not used for any figure. Lead for a later version.
