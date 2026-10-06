# CC-034: Air Quality Plan 'already yielding results'

**Status:** Drafted (v1.0, 6 Oct 2026, maintainer session; verdict Not substantiated, moderate; pending right of reply
from ERA). See `primary-source.md` (the wording), `notes.md` (what each source says, access, search log) and
`references.bib`. Data: `data/cc-034/` (EEA station data, ERA's attainment reports, Eurostat). Report build:
`tools/cc-034-report/` (`eea_cache.py`, `g_cache.py`, `fetch.py`, `calc.py`, `figures.py`, `build_report.py`,
`build_flyer.py`; `digitise_fig26.py` reads the plan's Figure 26 off the PDF).

## Routes tried for the wording (6 Oct 2026)

| Route | Result |
|---|---|
| Claim record URL `era.org.mt/air-quality-plan-for-malta-2024/` | 403 to scripts (as on 5 Oct). |
| Wayback capture of 15 Aug 2025 (`web.archive.org/web/20250815211515/...`) | Connection reset from this network on 6 Oct (also for `/web/2025id_/` of the PDF). The capture and the plan PDF were downloaded through the Wayback Machine in the maintainer's session on 5 Oct 2026; on 6 Oct we read the saved page in full and the saved PDF in part (pages 3, 21-67, 91, 95 read; pp. 4-20, 68-90, 96-104 skimmed for effect estimates, see `notes.md`) (SHA-256: page `8e7c7beb...3077607`, PDF `56b99ee8...cf11c4`, matching `primary-source.md`). |
| WebSearch for "already yielded positive results" | Returns the same ERA page with the same sentence (search summary; not used as evidence). Also lists ERA's public-consultation report (`era.org.mt/wp-content/uploads/2025/02/AQP-Public-Consultation-Report.pdf`): not read (era.org.mt 403, Wayback unreachable). |
| Speaker's other pages | ERA press release "ERA is updating the national Air Quality Plan" and the 2018 State of the Environment report, chapter 2, found by search; not read (403). |

**Wording found (verbatim):** the ERA page ("actions that have already yielded positive results for Malta's air
quality"; page metadata: dated 12 Mar 2025) and the plan's executive summary, PDF p. 3 (measures "that have
already contributed to improvements in air quality in Malta, such as ..."). The claim record combines the two
documents; each passage is quoted with its own source in the report.

## Open access

Nothing committed. Open-access sources used (licence recorded in `references.bib`): Fenech et al. (2021), Frontiers in
Sustainable Cities, CC BY 4.0, read in full; Eibinger and Fernando (2026), CC BY 4.0, read as the authors' copy
(`eibinget.github.io/files/zerofare.pdf`); Grange et al. (2018), CC BY 4.0, abstract read.
