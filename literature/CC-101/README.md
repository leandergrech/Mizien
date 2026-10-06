# CC-101: EU: no permits for water abstraction

**Status:** Drafted (v1.0, 6 Oct 2026, maintainer session). Verdict **Largely supported** (moderate confidence); no
right of reply needed. See `notes.md` (sources, access, the search log for every "not found" statement, hashes) and
`references.bib`. Data: `data/cc-101/` (Eurostat, EEA WISE, legislation.mt checks, figures transcribed from the
documents; `checks.csv`). Report build: `tools/cc-101-report/`.

## Where the verbatim wording was found (6 Oct 2026)

The claim is the European Commission's own summary of its letter of formal notice to Malta. The letter itself is not
published. The same paragraph appears, word for word, in two Commission documents, both read in full:

1. **Commission press corner, INF/26/1376, "July infringements package: key decisions", Brussels, 8 July 2026**,
   section 1 (Environment), item "Commission calls on Spain and Malta to ensure periodic review of water permits".
   Read through the press corner's print-PDF route
   (`ec.europa.eu/commission/presscorner/api/files/document/print/en/inf_26_1376/INF_26_1376_EN.pdf`, 222,060 bytes)
   and its JSON API (`/api/documents?reference=INF/26/1376`: publishDate 2026-07-08T16:19:14+02:00).
2. **European Commission Representation in Malta, "July infringements package: key decisions", 8 July 2026** (the
   claim record's URL), read with curl and a browser User-Agent.

## Routes tried

| Route | Result |
|---|---|
| Claim record URL (Representation in Malta) | Readable; wording found (above). |
| Commission press corner (INF/26/1376) | Readable via the print-PDF and API routes; identical wording. |
| `europa.eu/newsroom/ecpc-failover/pdf/inf-26-1376_en.pdf` (from a web search) | 404. |
| Infringement decisions register (`ec.europa.eu/implementing-eu-law/search-infringement-decisions/`, linked from the Representation page) | 404 to scripts; the register's API returned 500. Not read. |
| Wayback copies (`web.archive.org`) | Connection reset from this network all day (6 Oct 2026); none opened. |
| WebSearch for the Commission's wording and for a Maltese response | Found eubusiness.com, ieu-monitoring.com and smartwatermagazine.com re-publishing the Commission text; no Maltese government statement found. |
| tvmnews.mt search ("groundwater", 3 pages; "infringement") | No item on this letter or a government reply (6 Oct 2026). |
| tvmnews.mt and newsbook.com.mt WordPress APIs | Return empty lists for every search (API search appears disabled). |
| Amphora Media "Profit In Every Drop" (Aug–Sep 2026) | Readable; used only as a locator and, marked second-hand, for ERA data it reports. |

## Primary documents read for the test (all 6 Oct 2026)

- Directive 2000/60/EC (Water Framework Directive), via the EU Publications Office (EUR-Lex returns 202 with an empty
  body to scripts).
- Maltese law on legislation.mt (readable with curl): S.L. 549.100, 549.164, 549.165, 549.166, 549.168, 549.172,
  the Environment Protection Act (Cap. 549), the Water Services Corporation Act (Cap. 355), S.L. 545.14; titles of
  S.L. 549.160–549.184; titles of all 943 Legal Notices of 2024–2026 listed in the ELI sitemap.
- EWA and ERA, *Green Paper on the Regulation of Groundwater Abstraction in the Maltese Islands* (Nov 2023), and
  Malta's *Interim reporting on the implementation of the Programme of Measures* (3rd RBMP, April 2025), both from
  energywateragency.gov.mt (readable with curl at first; later requests met an `sgcaptcha` wall).
- SEWCU and ERA, *2nd Water Catchment Management Plan* (2015–2021), read from a copy on ampeid.org (era.org.mt
  refuses scripts).
- European Commission SWD(2019) 48 (Malta's 2nd RBMPs), COM(2025) 2 and SWD(2025) 13, via the Publications Office.
- Eurostat env_wat_abs (API) and EEA WISE WFD 2022 map services (Malta's reported water bodies and pressures).

## Not read

- The letter of formal notice INFR(2026)2115 and Malta's reply (neither published).
- Malta's 3rd River Basin Management Plan itself (ERA site refuses scripts; the Wayback captures of Chapters 3 and 8
  exist but web.archive.org was unreachable). Its Programme of Measures is known here through Malta's April 2025
  interim report on that programme.

No open-access PDFs are committed: the evidence is legislation, official reports and data, linked in `references.bib`
with SHA-256 hashes in `notes.md`.
