# CC-113: EEA: Malta among highest fossil-fuel subsidies

**Status:** Drafted (v1.0, 6 Oct 2026). Verdict Largely supported (moderate confidence); no right of reply needed.
See `notes.md` (sources, access, wording record, search log, gaps) and `references.bib`. Data: `data/cc-113/`
(EEA chart data, the European Commission's subsidy inventory, Eurostat GDP and subsidies, IMF and OECD/IISD data;
`checks.csv`, `shares_2023_variants.csv`). Report build: `tools/cc-113-report/`.

**Copyright note (6 Oct 2026).** The Commission's subsidy workbook carries "© Copyright Enerdata. Reproduction and
diffusion prohibited (web, photocopy, intranet...) without written permission." This repository is public, so only
country-level aggregates and a five-row Malta facts table are committed (`data/cc-113/ec_inventory_*.csv`); the
measure rows are rebuilt locally by `tools/cc-113-report/fetch.py` into a git-ignored folder, after a SHA-256 check of
the downloaded file. Details in `notes.md`.

No PDFs are committed. The evidence is EEA pages and chart data, the Commission's subsidy database (CIRCABC),
Commission and Council documents, Malta's draft budgetary plans, IMF data and Eurostat data, all linked in
`references.bib`. Raw downloads and their SHA-256 hashes: `data/cc-113/raw_files_sha256.csv`.

## Routes tried for the wording (6 Oct 2026)

1. **Claim record URL** (EEA indicator page): readable with curl and a browser User-Agent. The sentence is in the
   page HTML and in the page state (`window.__data`). Page metadata: published (effective) 29 Jan 2025 16:53 UTC,
   modified 29 Jul 2025, so the page was edited after publication.
2. **Wayback Machine and archive.today** (to see the original wording): both refused connections from this network
   (connection reset, `web.archive.org` CDX API and `archive.ph`; also refused to WebFetch). Not opened.
3. **The EEA's own fixed copies** (found by a web search for the sentence): (a) a browser-printed PDF of the indicator
   page served by the EEA under the 8th EAP monitoring publication, created 3 Feb 2025 (five days after
   publication); (b) the indicator PDF of the *Monitoring report on progress towards the 8th EAP objectives 2025*
   (file modified 26 Nov 2025). Both carry the same sentence, word for word. A 2023-edition indicator PDF returns
   410 Gone.
4. **Other EEA pages and data:** the three chart pages of the indicator (share of GDP 2023; by Member State; by
   energy vector) and their data packages; the *Europe's environment 2025* country page for Malta (fossil fuel
   subsidies, 29 Sep 2025), whose chart carries Malta's series 2015–2023.
5. **The EEA's data source:** the indicator names "DG ENER study on energy subsidies" with "direct link to the
   datasets is not available". The Commission's 9th State of the Energy Union page lists "Energy subsidies report
   (COM/2025/17), and the subsidy database (xl file)"; the database downloads from CIRCABC. COM(2025) 17 itself: EUR-Lex returned 202 with an empty body to scripts and WebFetch, but the EU Publications
   Office serves it (CELEX 52025DC0017, dated 28 Jan 2025; xhtml at
   http://publications.europa.eu/resource/cellar/7150e5a9-dd6f-11ef-be2a-01aa75ed71a1.0017.03/DOC_1), read 6 Oct 2026;
   DG ENER's news item of 29 Jan 2025 was also read. The 9th State of the Energy Union page is
   https://energy.ec.europa.eu/strategy/energy-union/ninth-report-state-energy-union_en. The 2025 edition of the study (op.europa.eu) returned 403.
6. **Newer Commission report:** COM(2026) 472 final (17 Sep 2026), read in full from Council document ST 13343/26.

The wording is the EEA's own, verbatim, and unchanged between 3 Feb 2025 and 6 Oct 2026 in every copy we could open.
