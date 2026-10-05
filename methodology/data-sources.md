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
| Maltese news and other outlets | Locating and quoting claims | Tested from the cloud network on 5 Oct 2026 with curl and a browser User-Agent. **Readable:** tvmnews.mt (public broadcaster; carries most government statements, often with direct quotes), newsbook.com.mt, lovinmalta.com, theshiftnews.com, amphora.media, maltairport.com, partitlaburista.org. **403:** timesofmalta.com, maltatoday.com.mt, independent.com.mt, one.com.mt. When one outlet is refused, search for the same statement elsewhere (WebSearch works even where a host is refused) before recording a blocker. |
| gov.mt, pa.org.mt, era.org.mt, nso.gov.mt, parlament.mt, pn.org.mt | Primary statements, PQs | 403 to scripts (tested 5 Oct 2026): browser only. Government press releases are usually reported by TVM News with the statement and direct quotes; EU-funded projects often have a European Commission page (reforms-investments.ec.europa.eu) repeating the claim. Record `source: browser-only (<url>)` only after those routes fail. |

## Before you record a blocker

A claim's first source is often not the only one. Before writing `source:` or `network:` in the queue, try and
note in `literature/CC-NNN/README.md` which of these you tried (5 Oct 2026, after three of five blockers in one night
turned out to have readable sources):

1. The URL in the claim record, then its Wayback copy.
2. A web search for the statement's key words: the same statement is usually carried by several outlets, and the
   readable ones are listed above (TVM News for government statements).
3. The speaker's own site and, for EU-funded projects, the European Commission's project pages; for EEA, Eurostat or
   Commission figures, the other pages and datasets of the same body (text pages, APIs, data downloads).
4. Only then record the blocker, naming the routes tried.

## Pitfalls seen so far

- **EU Publications Office PDFs** download with curl from `https://op.europa.eu/o/opportal-service/download-handler?identifier=<cellar id>&format=pdf&language=en&productionSystem=cellar` (cellar id is on the doi.org landing page); europarl.europa.eu PDFs return 202 empty (CC-020).
- **EEA pages:** the *Europe's environment 2025* country pages draw their numbers in JavaScript charts, but the same numbers are often stated in text elsewhere: the *Air pollution country fact sheets 2025: quick country facts* page (`eea.europa.eu/en/topics/in-depth/air-pollution/air-pollution-country-fact-sheets-2025/quick-country-facts`) has each country's PM2.5 death figures in its HTML (CC-035, 5 Oct 2026). Eurostat `ilc_mddw01` (noise from neighbours or street, EU-SILC, self-reported) works through the API (CC-020).

- **energywateragency.gov.mt** PDFs return an `sgcaptcha` redirect to scripted clients (CC-024): browser-only.

- **Who said it.** A figure in an interviewer's question is not the speaker's claim (CC-013: the 91,000 dwellings).
- **Paraphrase vs quote.** Newspapers paraphrase around short quotes; quote only the words inside quotation marks
  and label the rest as the outlet's paraphrase (CC-014).
- **Second-hand series.** When an annual report is unreachable, news reports of it are usable but must be marked
  second-hand in the data file and the report.
- **Nominal vs real.** Check whether price indices are deflated before comparing growth.
- **Do not trigger downloads in a browser session**; read PDFs in the page instead.
- **Cloud routines' network.** Run `python scripts/net_check.py` first; see `methodology/automation.md`.

- **airportcarbonaccreditation.org** web pages return an `sgcaptcha` wall, but its WordPress API is readable: `/wp-json/wp/v2/accredited-airport?slug=malta` gives an airport's current level (CC-030 review, 5 Oct 2026). Carbon-credit retirements can be checked in the Gold Standard public API (`public-api.goldstandard.org/credits/<id>`) and other registries' public endpoints. `maltairport.com` press releases and sustainability reports download with curl (follow redirects, `-L`); MIA's report gives Scope 1-3 in GRI 102 and PwC limited assurance on Scope 1-2.
