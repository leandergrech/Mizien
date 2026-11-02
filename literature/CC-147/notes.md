# CC-147 notes

## Access
| Source | Access |
|---|---|
| Climate Action Authority, FACTSHEET-AEA.pdf (Feb 2026; PDF creation date 4 Feb 2026) | **Full text, 7 pp.**, from the Internet Archive capture of 15 Apr 2026 (SHA-256 15f860d2...a4f2). Claim on p. 5; aviation weight p. 3; residence principle p. 1. |
| Eurostat env_ac_ainah_r2, env_ac_aibrid_r2, nama_10_a64 | Data, downloaded 2 Nov 2026 (`data/cc-147/eurostat_aea.csv`). Eurostat flag `i` on 2024 values (see Eurostat metadata); dataset update stamps 2026-08-07 and 2026-10-29. |

## Search log (rule 5a: absence statements)
- Crossref bibliographic search, 2 Nov 2026, queries "Manual for air emissions accounts Eurostat" and "Eurostat air emissions accounts residence principle international aviation": no peer-reviewed paper on emissions intensity with and without aviation for Malta. The hits were unrelated (SSRN aviation-agreements paper, IMF Indonesia TA report, etc.). No `references.bib` entries therefore; the evidence is official statistics (grade C). Eurostat's methodological pages (e.g. env_ac_ainah_r2 metadata) were not read in this run.
- Not searched: Malta National Inventory Report by sector (the territorial totals come from Eurostat's bridging table instead).

## What did not reproduce
- Factsheet p. 5 "9.6%" and "190.9%", and p. 4 "16.6%" (2013-2024): no start/end years or definitions given; our nearest figures (all-activities intensity 2013-2024: +8.7% with households, +13.7% without) do not match. Not rated.
- Factsheet's own p. 3 chart: emissions excluding air and water transport 2024 = 2,116.77 kt; current Eurostat release gives 2,108.26 kt (-8.5 kt, vintage).
- The exact 19%: our rebuilds give -22.2% (CLV subtraction, air + water), -21.2% (air only), -22.2% (territory basis), -33.7% (current-price GVA, cross-check only). The factsheet's workings are not published.

## Quality of the series
Chain-linked GVA for H51 is negative in 2020, 2022-2024 (-EUR 219 m in 2020, which is also the current-price value because 2020 is the reference year). Chain-linked H50 starts in 2020 and H51 in 2017 in the downloaded range, so start-year sensitivity removes air transport only.
