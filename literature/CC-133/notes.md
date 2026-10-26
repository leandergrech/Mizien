# CC-133 notes

- **Wording:** Commission 2026 Country Report for Malta (SWD(2026) 218 final), Council register copy ST-10135-2026-ADD-1
  (126 pp.), read 25-26 Oct 2026 (pdftotext, and pages rendered to PNG for the graphs). The summary passage ("This continues
  to drive nominal property prices, which have risen steadily since 2014 and consistently outpace EU average growth. However,
  with income growth exceeding these gains, the price-to-income ratio has actually declined, tempering the impact on overall
  affordability (see Annex 16).") is on PDF p. 8 (printed p. 6). Annex 16 (housing) is on PDF pp. 113-116: "The price-to-income
  ratio in Malta has declined since 2007. Slightly higher overall income growth has offset the increase in house prices,
  limiting affordability pressures as measured by the price-to-income ratio." House prices and rents +5.9% and +1.7% in
  2024-2025. Graph A16.1 (source: Eurostat) plots nominal prices, rents and the price-to-income ratio for MT and EU-27 since
  2005. Graph A16.3 (PDF p. 116, image only, read from a 300 dpi render): house price to income ratio, 2000-25 avg = 100, EU-27
  102.0 (2023), 100.2 (2024); MT 96.9, 92.7; MT YoY -2.2, -4.3; rent-to-income MT 83.0 / 81.0 / 79.4 (2023-2025);
  overburden rate tenants at market rent MT 25.5 (2023), 19.7 (2024). The list of graphs gives a different page number
  (97) for A16.1: stale front matter; PDF page numbers are used throughout.
  Copyright: the Commission document is not committed; the Council register URL is the reference.
- **Indicator:** Eurostat tipsho60 "Standardised house price-to-income ratio" (MIP auxiliary indicator; updated 16 Apr 2026;
  latest year 2024). Income = adjusted household gross disposable income (B7G) per head of population (Eurostat ESMS
  tipsho20_esms, read 26 Oct 2026). Units PTIR_I15 (2015 = 100), PTIR_LT_AVG (2000-latest average = 100), RCH_A_AVG.
  Recomputed exactly for Malta 2024 (89.29) from prc_hpi_a, nasa_10_nf_tr B7G S14_S15 and nama_10_pe.
  The Commission's A16.3 values differ by 0.2 from PTIR_LT_AVG: probably a different averaging window ("2000-25") or vintage;
  not established.
- **Data:** see `data/cc-133/README.md`. Malta B7G 2021-2024 flagged p (provisional); Malta HPI 2025 flagged p.
- **Findings:** HPI up every year 2015-2025 (3.4-6.7%), +83.6% 2014-2025 (EU +65.6%). EU-27 annual growth higher in 2020,
  2021, 2022; cumulative since 2014 Malta always ahead (2022: 52.8% vs 52.3%). Ratio -11.5% 2014-2024, -23.1% 2007-2024,
  peak 2008; EU +5.8% since 2014. Adjusted GDI per head +95.7% 2014-2024 vs HPI +73.3%. EU-SILC median equivalised income
  (income years 2014-2024, survey 2015-2025) +62.6%: ratio on that income +6.6% (2013-2023: +8.2%); since 2007 -12.3%.
  HICP actual rentals MT +15.2% (2023), +8.9% (2024), +1.7% (2025).
- **Commission discussion paper (DP 228, Cousin et al. 2025):** read in full where relevant (pp. 20-23, Graph 9 p. 22,
  Annex V p. 82; PDF downloaded 26 Oct 2026, CC BY 4.0, not committed: 4.8 MB). ECFIN's price-to-income uses adjusted
  disposable income per capita (Graph 8 note). Graph 9 shows Malta's 2024Q4 ratio below 2014 and 2007 (direction read from
  the chart; no value used). p. 23: "with the exception of Bulgaria, Romania and Malta, house price growth has exceeded the
  change in borrowing capacity" (2019-2024). DOI 10.2765/3521352 resolves (302) to op.europa.eu; not registered in Crossref.
- **Literature:** Gan & Hill (2009) JHE 18(2):115-125, DOI verified in Crossref (title, authors); abstract not in Crossref or
  OpenAlex, read from the SSRN record 1310294 via WebFetch summary (purchase vs repayment affordability; median-based
  measures can understate the problem). Stone (2006) Housing Policy Debate 17(1):151-184, DOI verified in Crossref, abstract
  read via OpenAlex (residual-income approach). Both closed access; abstracts only; context, never a finding on Malta.
- **Search log (absence statements):** "the report does not say which vintage it used": the full Country Report text was
  searched (pdftotext) for "vintage", "tipsho", "price-to-income" on 26 Oct 2026; Graph A16.1 and A16.3 give only "Source:
  Eurostat" / "Source: European Commission". "No values given" for DP 228 Graph 9 / Annex V: the charts carry no data labels
  and the paper's text gives no Malta figure (pdftotext search for "Malta" and "MT", 26 Oct 2026).
- **Not read / not tested:** Central Bank of Malta property price index (advertised prices) and NSO RPPI releases; earlier
  Eurostat vintages; causes of the gap between the national-accounts and EU-SILC income measures.
