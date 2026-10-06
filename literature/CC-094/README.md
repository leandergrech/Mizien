# CC-094: Commission: Malta to emit more in 2030 than in 2005

**Status:** Drafted (v1.0, 6 Oct 2026). Verdict Supported (high confidence); no right of reply needed. See
`primary-source.md` (the Commission's sentences, page numbers, file hashes), `notes.md` (sources, access, grades, search
log, gaps) and `references.bib`. Data: `data/cc-094/` (EEA effort-sharing emissions and projections, legal inputs,
the Commission's stated figures, `checks.csv`); the Commission's SWD tables for Malta are reused from
`data/cc-003/capr2025_esr_malta.csv`. Report build: `tools/cc-094-report/`.

Open access: `open-access/COM-2025-668-final_EN.pdf`, the report itself (75 pages, from the EU Publications Office).
Licence: © European Union, 2025, CC BY 4.0 (Decision 2011/833/EU).

Title: changed on 6 Oct 2026 from the intake's "Commission: Malta off track for 2030". The Commission did not use
"off track", and its gap is stated before any use of flexibilities.

## Routes tried for the verbatim wording (6 Oct 2026)

| Route | Result |
|---|---|
| Claim record URL, EUR-Lex HTML (`.../TXT/HTML/?uri=CELEX%3A52025DC0668`), and the PDF, ALL and ELI views | HTTP 202 with an empty body (bot challenge) for every view |
| Wayback Machine (availability API; `web/2026id_/` capture of the EUR-Lex URL) | No snapshot listed; web.archive.org reset the connection |
| Commission's CAPR 2025 page (climate.ec.europa.eu) | Page readable; its download of the report (HTML, 410 KB) returned an Azure WAF JavaScript challenge (403). The staff working document (SWD(2025) 347, PDF) downloaded |
| EU Publications Office (Cellar), content negotiation on `publications.europa.eu/resource/celex/52025DC0668` | **Worked**: XHTML and PDF of COM(2025) 668 final. Read in full for Malta; wording found |
| Chapter 3 web page of the CAPR (climate.ec.europa.eu) | Not re-read for this check (CC-003 cites it); the act itself was read instead |

The legal texts (Regulations (EU) 2018/842 and 2023/857; Implementing Decisions (EU) 2020/2126, 2023/1319, 2024/1884,
2026/895; Commission Decision (EU) 2023/863) were read the same way, through Cellar. Implementing Decision 2026/895
(Malta's allocations for 2026-2030, adopted 24 Apr 2026) was located with a web search.

## Data routes

- EEA datasets are on the EEA datastore (`sdi.eea.europa.eu/datastore/public`), a public Nextcloud share; files download
  through its WebDAV address (`tools/cc-094-report/fetch.py`). The EEA's web data viewers draw their numbers in
  JavaScript and were not needed.
- The Commission's NECP assessment extract for Malta (SWD(2025) 140) and Malta's final updated NECP were downloaded from
  commission.europa.eu with a browser User-Agent (same files as CC-024; NECP SHA-256 identical).
