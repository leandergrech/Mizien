# Data for CC-123 (KPMG: 8,716 residential units approved in 2024)

Retrieved 16 Oct 2026.

- `kpmg_text.csv`: the figures and sentences read from KPMG, *Construction Industry and Property Market Report 2025*
  (for the Malta Development Association, Dec 2025), with PDF page numbers. The report is not committed (copyright);
  SHA-256 in `source_hash.txt`.
- `pa_approved_dwellings_2022_2025.csv`: Planning Authority, Approved Dwelling Units 2007-2025, rows 2022-2025 copied from
  `data/cc-013/pa_approved_dwellings.csv` (transcribed on 3 Oct 2026; pa.org.mt returns 403 to scripts, so it was not re-read
  on 16 Oct 2026).
- `nso_quarterly_secondhand.csv`: NSO quarterly "Residential Building Permits" releases, Q1 2023 to Q3 2025. nso.gov.mt returns
  403 to scripts, so the figures come from web-search summaries of the releases and one outlet article (second-hand, marked
  in the report).
- `sts_cobp_a_MT_DW.json`: Eurostat sts_cobp_a, Malta, number of dwellings in residential buildings with 2+ dwellings
  (BPRM_DW, CPA_F410012_410013), unit I21 (index, 2021 = 100), annual, not seasonally adjusted; API response as received
  (dataset updated 2 Oct 2026).
- `checks.csv`: every figure used in the report, written by `tools/cc-123-report/calc.py`.
