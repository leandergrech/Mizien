# CC-035: PM2.5 death rate down two-thirds

**Status:** Drafted (v1.0, 6 Oct 2026, maintainer session). Verdict **Largely supported** (high confidence); no right
of reply needed. See `notes.md` (sources, access, method, search log, gaps) and `references.bib`. Data:
`data/cc-035/` (EEA burden-of-disease table, Eurostat, EEA station files, `checks.csv`, `station_vs_model.csv`,
`eu27_rate_change.csv`). Report build: `tools/cc-035-report/`.

## The wording

Supplied by the maintainer on 5 Oct 2026 (`primary-source.md`) and **read again in the page HTML on 6 Oct 2026**
(EEA, *Air pollution country fact sheets 2025: quick country facts*, page "Modified 01 Dec 2025"; fetched with curl
and a browser User-Agent, HTTP 200, 954,977 bytes, SHA-256
`d8deb81af732a2d9c4fabda44c6af481ef53d4dff187764bcfb5dbda4817e6b8`). The Malta sentence is word for word as in
`primary-source.md`. The earlier record text ("fell by 67.7% ... to 172 attributable deaths") was the intake's
paraphrase; the report quotes the page.

## Routes tried (6 Oct 2026)

| Route | Result |
|---|---|
| Quick-facts page (claim record, source 2) | Read: Malta sentence in the HTML text. |
| *Europe's environment 2025* Malta page (claim record, source 1) | Read (HTTP 200, published 29 Sep 2025, modified 23 Sep 2025, SHA-256 `e1944b38...de69d`): the figures are in a chart; its text gives the emissions context and "Temporal coverage 2005-2022" (the previous data release). Not the statement checked. |
| Wayback Machine (availability API for both pages) | 429 Too Many Requests, three tries; not opened. **Manual task:** archive both pages. |
| EEA briefing *Harm to human health from air pollution in Europe: burden of disease status, 2025* (doi:10.2800/8961999) | Read (published 1 Dec 2025, modified 30 Sep 2026): method, counterfactuals, what the CI covers. |
| EEA indicator *Premature deaths due to exposure to fine particulate matter in Europe* | Read (published 30 Nov 2025): method changes since 2021 and the recalculation back to 2005. |
| EEA Table publisher, *Burden of disease of air pollution (Countries & NUTS)* (discomap AQViewer, fqn `Airquality_Dissem.ebd.countries_and_nuts`) | Downloaded as CSV through the app's own `download` endpoint: Malta (every scenario), all countries, EU-27. The older `hra.countries_sel` table named in the SDI catalogue no longer exists. |
| Eurostat API: `sdg_11_52`, `demo_pjan`, `demo_magec`, `hlth_cd_aro`, `env_air_emis` | Downloaded with flags. |
| Zenodo (ETC reports, CC BY 4.0) | ETC HE 2025/8, ETC HE 2025/5 and ETC/ATNI 2020/1 downloaded and read (see `notes.md`). Not committed (9.5, 18.9 and 3.9 MB; stable on Zenodo with DOIs); hashes in `notes.md`. |
| EEA Air Quality download service (`eeadmz1-downloads-api`, AirBase and E1a Parquet) | All 30 Malta PM2.5 and PM10 files downloaded; hashes in `data/cc-035/eea_station_file_manifest.csv`. |
| Crossref, DataCite, doi.org handle API, Europe PMC | DOIs verified; abstracts for Chen and Hoek (2020) and Scerri et al. (2018). OpenAlex refused (daily budget used up on this network). |

Earlier attempt (5 Oct 2026, worker B): the *Europe's environment 2025* Malta page draws the figures in a JavaScript
chart, so 67.7% and 172 were not in its text; the maintainer then supplied the quick-facts wording.

No open-access PDFs are committed: the reports are on Zenodo under stable DOIs and the evidence used from them is
recorded in `notes.md` with page or table numbers.
