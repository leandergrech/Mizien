# Data sources: what works, and pitfalls

Practical notes for anyone (human or routine) checking a claim. Add to this file when you learn something.

## Access

| Source | Use | Access notes |
|---|---|---|
| Eurostat dissemination API `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/<dataset>?geo=MT&...&format=JSON` | Prices, population, emissions, energy, housing, waste | Works with curl. **Read the dataset `label` before using it**: e.g. `tipsho20` is the *nominal* house price index and `tipsho10` the *deflated* one (a CC-013 near-miss). |
| Eurostat news items `ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-YYYYMMDD-N` and table metadata `.../cache/metadata/EN/<dataset>_simsae_dk.htm` | Citing Eurostat's own wording; residence vs territorial principle | Readable with curl. Statistics Explained pages are JavaScript-rendered. Eurostat revises series: re-download and note differences from the release. `env_ac_ainah_r2` (accounts, residence) vs `env_air_gge` (inventory, territorial; international aviation is a memo item). |
| Crossref `https://api.crossref.org/works/<DOI>` | Verify every DOI | Check that the returned title and authors are the paper you meant: two "remembered" DOIs on 3 Oct 2026 resolved to unrelated papers. |
| OpenAlex `https://api.openalex.org/works/doi:<DOI>` | Abstracts (inverted index), open-access links | Abstract missing for some publishers; then cite as metadata only. |
| Sentinel-2 L2A via Microsoft Planetary Computer (STAC search + anonymous SAS token) | Vegetation, land cover, before/after on a site | See `tools/cc-012-report/fetch_s2.py`. Define the study area from a signal other than the one you test (CC-012 used summer brightening to locate gravel, then tested winter greenness), and always compare with a control area. |
| OpenStreetMap Overpass `https://overpass-api.de/api/interpreter` | Site polygons | Rate-limited: retry. Many Maltese sites are not mapped in detail. |
| MEPA annual reports 2002-2011 on `era.org.mt/wp-content/uploads/2019/05/` | Planning enforcement, permits history | Cloudflare blocks curl; read in a browser. 2012 and 2014 are scanned images. |
| Planning Authority annual reports | Enforcement, applications | 2024 report is on `parlament.mt/media/134019/`; 2013-2023 only on Issuu. PA `file.aspx` links download files. |
| PA "Approved Dwelling Units 2007-2025" | Permits by year and type | Transcribed in `data/cc-013/pa_approved_dwellings.csv`. |
| NSO (nso.gov.mt), Census 2021 | Dwellings, population | Cloudflare blocks curl; browser only. Vacancy figures in `data/cc-013/census2021_dwellings.csv`. |
| Maltese news (Times of Malta, MaltaToday, Malta Independent, Newsbook, The Shift) | Locating and quoting claims | Usually readable with curl and a browser User-Agent from an unrestricted network; refused by the cloud routines' allowlist. |
| gov.mt, pa.org.mt, era.org.mt, parlament.mt, pn.org.mt | Primary statements, PQs | Cloudflare: browser only. In a routine, record `source: browser-only (<url>)` as the Blocker rather than spending the run. |

## Pitfalls seen so far

- **EU Publications Office PDFs** download with curl from `https://op.europa.eu/o/opportal-service/download-handler?identifier=<cellar id>&format=pdf&language=en&productionSystem=cellar` (cellar id is on the doi.org landing page); europarl.europa.eu PDFs return 202 empty (CC-020).
- **EEA country fact sheets** are JavaScript-rendered: the numbers cannot be read by script. Eurostat `ilc_mddw01` (noise from neighbours or street, EU-SILC, self-reported) works through the API (CC-020).

- **energywateragency.gov.mt** PDFs return an `sgcaptcha` redirect to scripted clients (CC-024): browser-only.

- **Who said it.** A figure in an interviewer's question is not the speaker's claim (CC-013: the 91,000 dwellings).
- **Paraphrase vs quote.** Newspapers paraphrase around short quotes; quote only the words inside quotation marks
  and label the rest as the outlet's paraphrase (CC-014).
- **Second-hand series.** When an annual report is unreachable, news reports of it are usable but must be marked
  second-hand in the data file and the report.
- **Nominal vs real.** Check whether price indices are deflated before comparing growth.
- **Do not trigger downloads in a browser session**; read PDFs in the page instead.
- **Cloud routines' network.** Run `python scripts/net_check.py` first; see `methodology/automation.md`.

- **airportcarbonaccreditation.org** returns an `sgcaptcha` wall to scripts (CC-030): browser-only. `maltairport.com` press releases and sustainability reports download with curl (follow redirects, `-L`); MIA's report gives Scope 1-3 in GRI 102 and PwC limited assurance on Scope 1-2.
