# CC-088: Population 588,254

**Status:** checked, verdict Supported (5 Oct 2026). No academic literature needed: this is an official-statistics check.

## Primary source (verbatim found)
National Statistics Office, News Release NR 120/2026, "World Population Day: 11 July 2026", released 9 July 2026,
https://nso.gov.mt/world-population-day-11-july-2026/. nso.gov.mt returns 403 to scripts; the page was read in full
from the Internet Archive copy (`https://web.archive.org/web/2026/<url>`). The release PDF is linked from that page as
NR-120-2026 (not retrieved). The release tables were not read.

## Cross-check
Eurostat demo_gind (Malta), downloaded 5 Oct 2026: `data/cc-088/eurostat_demo_gind.csv`; recomputation in
`tools/cc-088-report/calc.py` -> `data/cc-088/checks.csv`. Eurostat's Maltese data are supplied by the NSO, so this is
not an independent count.

## Second-hand (locators only)
MaltaToday (9 Jul 2026) and Lovin Malta (11 Jul 2026) report the same figures.

## Gaps
- National density figures (1,731 and 1,838 per km2) mentioned in the claim record: source not found; the NSO release
  gives locality densities only. Eurostat demo_r_d3dens: 1,817.4 (2024).
- Immigration and emigration flows, citizenship and age figures not tested.
