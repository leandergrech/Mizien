# Data for CC-062 (construction and real estate share of GVA)

Retrieved 8 Oct 2026.

- `kpmg_tables.csv`: figures transcribed by hand from KPMG, *Construction Industry and Property Market Report 2025*
  (for the Malta Developers Association, Dec 2025), with PDF page numbers. The report is not committed (copyright).
  SHA-256 of the file read: see `source_hash.txt`.
- `nama_10_a64_MT.json`: Eurostat national accounts by industry (NACE A*64), current prices, million EUR; gross value
  added (B1G) and output (P1) for total economy, F (construction), L (real estate) and L68A (imputed rents of
  owner-occupiers). API response saved as received (Eurostat dataset updated 8 Oct 2026 per the response).
- `naio_10_cp1750_MT_2015.json`, `naio_10_cp1750_MT_2020.json`: Eurostat symmetric input-output tables, domestic
  output, industry by industry, Malta; used only to test whether the multipliers can be re-derived (they cannot: see
  `checks.csv`).
- `checks.csv`: every figure used in the report, written by `tools/cc-062-report/calc.py`.
