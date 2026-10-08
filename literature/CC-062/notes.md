# CC-062 notes (8 Oct 2026)

## Access
- KPMG report PDF: downloaded with curl (HTTP 200, 124 pages). Read in full: cover pages, "Important information",
  foreword, executive summary, Chapter 1 (sections 1.1-1.7). Not read: Chapters 2 onward (property market, deeds,
  prices, appendices). Not committed (copyright); hash in `data/cc-062/source_hash.txt`.
- The NSO figures in KPMG's tables are read second-hand through KPMG (nso.gov.mt is 403 to scripts).
- The Central Bank of Malta multipliers (0.55, 0.78, "Type 1", 2015 SIOT) are known only through KPMG (second-hand).
  centralbankmalta.org/estimates-multipliers-maltese-economy returned 403 (WebFetch). Two web searches (8 Oct 2026)
  listed related papers (Rapa and Cassar, CBM working paper / Xjenza 2018, 2010 table; Cassar and Theuma, supply-side
  multipliers 2010 and 2015) that were NOT opened; we do not state that no published 2015 value-added multipliers exist.

## Search log for "could not be re-derived"
- Eurostat naio_10_cp1750 (domestic, industry by industry), Malta 2015 and 2020, queried 8 Oct 2026. In 2015 only 37
  industry columns have output; value added in those columns is EUR 6,443 million of 8,889 million (72%); F is a single
  aggregate (F41-F43 empty), no D, H, J, M69-71 columns. The 2020 table is fuller (55 columns) but the claim's
  multipliers are for the 2015 table. Rebuilding a Leontief inverse from this is not reliable, so not done.

## Reconciliation
- 2024 construction GVA: KPMG/NSO 809.0 (Table 1.2), Eurostat 893.6 (retrieved 8 Oct 2026). We do not know the cause
  (revision vintage is the likeliest; not verified). 2020-2023 shares agree within 0.15 pp.
- KPMG p. 32 says multiplier results (Section 1.7) are not percentage contributions "covered in the previous
  section"; Table 1.3 (Section 1.6) is KPMG's own percentage-contribution estimate. Not used against KPMG.

## Gaps
- The sentence has no table reference; Tables 1.1 and 1.3 are our matching, not KPMG's cross-reference.
