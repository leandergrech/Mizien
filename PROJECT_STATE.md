# Project state (working notes)

Read this first when resuming work. It records decisions, conventions and what is outstanding, so a new session can
continue without re-deriving anything. Update it at the end of every work session.

*Last updated: 3 October 2026 (CC-008 merged into main; CC-002 report, flyer and literature notes drafted on `codex/cc-002-comino`).*

## What the project is

Miżien: an independent, science-first record of fact-checks on public claims in Malta (authorities, institutions,
parties, NGOs, opposition), focused on quality of life and the environment. Homepage is a 3D mind map of all claims
grouped by topic with links between them. The repository is public and doubles as the assistant's persistent storage.

## Repository

https://github.com/leandergrech/Mizien (public). Site: https://leandergrech.github.io/Mizien/ (GitHub Pages from
`main`, `/docs`). The repo URL is printed on the CC-001 report cover and flyer.

## Conventions

- **Name:** Miżien (with ż). Repo slug `mizien` because GitHub slugs are ASCII.
- **Claim IDs:** `CC-NNN` (three digits). One folder per claim under `claims/`, with `claim.yml` as the source of truth.
- **Verdict scale:** Supported, Largely supported, Not substantiated, Misleading, Contradicted. Confidence High, Moderate, Low.
- **Evidence grades:** A experiment, B observational, C review or guidance, D anecdote. Second-hand sources marked.
- **Pattern tags:** Selective metric, Input-as-outcome, Compliance-not-health, Conditional-turned-unconditional, Promise-without-baseline (provisional until a report is finished).
- **Right of reply** before wider circulation. Misleading or Contradicted only on evidence that can be shown.
- **Copyright:** paraphrase; quote the claim briefly; commit only open-access PDFs.
- **Language:** British English; Maltese names with correct spelling (Miżien, Għar Lapsi, Ħondoq, Magħtab, Għallis, Wirt Artna).
- **Report design:** A4, Liberation Serif body, Liberation Sans headings and tables. Palette: green #14452F, sage #7FA88B,
  amber #E3A72F, orange #D9772B (Not substantiated), red #B5483A, slate #2B3A42, cream #F6F4EE, pale green #E6EFE8.
  Report structure in `methodology/report-outline.md`. CC-001 generators in `tools/cc-001-report/`. From CC-003 on, the
  design lives in one shared module, `tools/mizien_report.py` (cover, body pages, meter, tables, contested-question
  blocks, flyer); each claim has `tools/cc-NNN-report/` with `calc.py`/analysis, `figures.py`, `build_report.py`,
  `build_flyer.py`. Outputs go to `out/` (git-ignored) and are copied to `claims/CC-NNN/`.
- **Numbers:** every figure in a report is recomputed by a script from data saved under `data/cc-NNN/` with the
  source query URL and retrieval date (`checks.csv` lists each check).
- **Spreadsheet:** `data/candidates.xlsx` is the tracker. `data/*.csv` are exports. After changing claim records run
  `python scripts/build_site_data.py`.

## Status

| ID | Status |
|---|---|
| CC-001 Upper Barrakka concrete | Report v1.1 and flyer done. Verdict: Not substantiated (plausible, not shown). Draft pending right of reply. |
| CC-002 Comino tree compensation | Report and flyer v1.0 drafted. Verdict: Largely supported (moderate) for ERA's announced categories and conditions: 624 + 54 = 678; 92.04% non-protected; 54 × 10 = 540; a separate group of 348 is to be transplanted. This does not demonstrate ecological replacement. The full permit annex, 467/468 oleander discrepancy, transplant results and habitat recovery data remain unresolved. Science-only scope; no legal commentary. Right of reply not sought, at maintainer direction. |
| CC-003 Per-capita emissions vs 2030 | Report v1.0 and flyer drafted. **Verdict: Misleading (high).** CAA press release 13 Nov 2025 cites the -44% per-capita figure from the Commission's CAPR 2025 but omits its projection: effort-sharing emissions +41% in 2024, +30% to +42% by 2030 vs -19% target (largest gap in the EU). Half the per-capita fall is population growth. Pending right of reply; **must not be published before the reply deadline.** |
| CC-004 Waste separation | Report v1.0 and flyer drafted. Verdict: Not substantiated (moderate). Separation up; recycling rate 16.7% (2024) vs 55% 2025 target; 79% landfilled; 412 million kg 'diverted' not reconcilable with Eurostat (271 kt). Pending right of reply. |
| CC-005 Bathing water | Styled report and flyer drafted in the shared CC-001 design. The Commission's exact 92% statement matches the EEA 2023 result (80/87); latest 2025 season is 88.5%. Balluta Bay closure and the CJEU wastewater-treatment case are contextual and do not refute the dated statistic. Draft verdict: Supported (high). Right of reply not sought, per maintainer direction. Viewer metadata uses the same Report / Flyer PDF / Flyer image actions as completed checks. |
| CC-011 Manifesto pledges | Report v1.0 and flyer drafted. Verdict: Not substantiated (moderate) for both. Labour's pledge is "open or green" space (not "green space"): 99.9% already within reach on a broad reading, 55-68% for parks of at least 0.5 ha. PN's is a plan for a Net-Zero Gozo by 2040 with afforestation as one of several measures (news said "through afforestation"); no Gozo inventory; afforestation alone would need 1.5-8.5x Gozo's area. Pending right of reply. |
| CC-006 Spring hunting | Report and flyer v1.0 integrated into main. The report tests both Article 9 conditions. Quota-to-statutory-benchmark ratios are 99.3% for Quail and 59.8% for Turtle-dove. Draft verdict: Not substantiated (moderate): the statutory arithmetic is within the benchmark, but the 2026 enforcement outcome and ecological impact are not established. The 30 March 2026 Ornis minutes were not listed in the WBRU archive; latest season outcome report listed was for 2025. Right of reply remains for the maintainer. |
| CC-007 | Air | Local draft in the original checkout: report/flyer and source transcription drafted; Saint Paul's Bay 2020–21 readings and ERA validation series remain incomplete. Not committed or pushed. |
| CC-008 | Transport | Report v1.0 and flyer merged into `main` at `6e1f342`. Verdict: Not substantiated (moderate). Marsa's 2021 travel-time and emissions percentages are agency-reported; the underlying survey/calculation was not found. Msida wording was prospective; the flyover entered use in December 2025 while the broader project continued. No local before/after noise series located. Pending maintainer right of reply. |
| CC-009 to CC-010 | Candidates only. |

## Outstanding

- [ ] Decide author or affiliation line for reports and flyer (none yet).
- [ ] Add the Times of Malta article URL to `data/sources.csv` and `claims/CC-001/claim.yml`.
- [x] Run `python scripts/archive_sources.py` to fill `archive/manifest.csv` (committed on branch `archive-manifest`).
- [ ] Archive by hand the 27 robots-disallowed sources in `archive/manifest.csv` (gov.mt, ERA, NSO, MaltaToday,
  Newsbook, Italpress, arja.mt, Independent, Chambers). gov.mt sites (climateaction, publicservice, DOI) block
  automated access with Cloudflare; read them in a browser.
- [ ] Add the new CC-003/004/011 primary sources to the archive (CAA press release, PR260072en, PL manifesto PDF,
  PN programme pages). The PL manifesto SHA-256 is recorded in `literature/CC-011/references.bib`.
- [ ] Send right-of-reply drafts: CC-003 to the Climate Action Authority and Environment Ministry; CC-004 to the
  Environment Ministry and WasteServ; CC-011 to the Partit Laburista (and the Government) and the Partit
  Nazzjonalista. Record dates and deadlines in each `claim.yml`. Each report lists the questions to ask.
- [ ] Decide whether the site should show verdicts for drafts before the reply deadline (it currently does, e.g.
  "Misleading (Drafted)" for CC-003 once merged).
- [ ] `data/candidates.xlsx` is behind the CSVs for CC-003, CC-004, CC-011 (sources, edges, theme T7, quick check).
  It was not edited because openpyxl drops its drawings; update it by hand or treat the CSVs as the master.
- [ ] Decide whether the verdict scale needs a rule for pledges (CC-011 used Not substantiated = not measurable as worded).
- [ ] CC-003: obtain the CAA "Facts: emissions (June 2026)" factsheet (blocked).
- [ ] CC-004: verify COM(2023) 304 early-warning report directly (cited second-hand).
- [ ] Send CC-001 draft to Ambjent Malta and Fondazzjoni Wirt Artna; record dates in `claims/CC-001/claim.yml`.
- [ ] CC-006: locate and archive the 30 March 2026 Ornis Committee minutes; obtain the 2026 WBRU season outcome report, final 2019–2024 Article 12 data, and FKNK survey methods/results. Right of reply remains for the maintainer.
- [ ] CC-007: obtain the two missing St Paul's Bay 2020–21 values and ERA's validated series with coverage/quality notes; full-text verification of the Newsbook report remains unavailable. Right of reply is for the maintainer.
- [x] CC-008: locate primary wording for Msida and Marsa; draft report/flyer and add evidence notes. Remaining: obtain the Marsa surveys/calculations and comparable local traffic, air and noise series; right of reply remains for the maintainer. Four earlier MaltaToday sources plus the OPM and Times of Malta pages are robots-disallowed and need browser archiving; ERA's source page also blocks automated access. The AEA publisher returned HTTP 403 to the archiver.
- [x] CC-005: locate Commission wording; compare EEA bathing-water seasons 2023–2025; confirm Balluta Bay warning from the EHD primary report; distinguish CJEU wastewater ruling from bathing-water classification.
- [x] CC-005: add sources to `archive/manifest.csv`. Commission page and CJEU judgment have archived snapshots; EEA 2025 is fetched and hashed. EEA 2024 and the EHD Balluta report are robots-disallowed with no snapshot; archive manually if needed. News leads are robots-disallowed but existing snapshots are recorded.
- [ ] CC-005: review drafted verdict, styled report and flyer; reply process remains for maintainer.
- [ ] Obtain open-access full text for the CC-001 A and B studies; fill gaps noted in `literature/CC-001/notes.md`.
- [ ] Collect literature for CC-009 to CC-010 (each folder lists what to collect).
- [ ] Verify and fix `literature/CC-001/references.bib` (first task 2 in CLAUDE.md; not done this session).
- [ ] Check the name and a domain are free; enable GitHub Pages (main, /docs).
- [ ] CC-002: obtain the full permit annex/species schedule and follow-up transplant-survival and habitat-monitoring data if publicly available. Keep all analysis to science; do not comment on the tribunal. The 3 October automated archive attempt hit DNS resolution failures for the two direct ERA releases and most other new sources; do not label these failures robots-disallowed. The older generic ERA press-releases entry is robots-disallowed. Archive direct pages manually when available.

## How to resume a session

1. Clone the repository (it is public) and read this file, `README.md` and `data/claims.csv`.
2. Pick the next claim from the table above; open its `claim.yml`.
3. Collect literature into `literature/CC-NNN/`, then build the report from `methodology/report-outline.md`.
4. Work on a branch per claim and open a pull request for the maintainer.

## Branches (3 October 2026)

`archive-manifest`, `cc-003-climate`, `cc-004-waste` and `cc-011-manifestos` have been merged into `main` (PRs #1–4).
CC-005 outputs and viewer metadata were merged and pushed to `main` (merge commit `2110846`). CC-006's report, flyer and site metadata are integrated on `main` at `e0552b9` (fast-forward from `codex/cc-006-spring-hunting`). CC-008 was fast-forwarded and pushed to `main` at `6e1f342`. CC-002 is being prepared on `codex/cc-002-comino`; right of reply remains with the maintainer.

## Notes for the next session

- CC-002 editable draft: `claims/CC-002/report.md`; generated outputs: `report.pdf`, `flyer.pdf`, `flyer.png`. Do not treat the 10:1 planting condition as measured ecological equivalence or use cross-study findings as a Comino survival rate. The one-specimen oleander discrepancy remains unresolved.
- CC-008 editable draft: `claims/CC-008/report.md`; generated outputs: `claims/CC-008/report.pdf`, `flyer.pdf`, `flyer.png`. Do not present Marsa's percentages as independently reproduced. No survey file was located. Msida's PDS observations are from 2019 and are not a post-opening counterfactual. The national licensed-fleet figure in the original candidate is not a junction traffic measure and was not used.
- `archive/manifest.csv` records CC-008 source-fetch results. Manual browser archiving is still needed for the four earlier MaltaToday sources, the Office of the Prime Minister and Times of Malta; ERA blocks automated access and the AEA publisher returned HTTP 403. The three Infrastructure Malta pages were fetched and have Wayback snapshots.
- CC-002 direct ERA release URLs and most newly added sources remain unarchived because the archive script encountered temporary DNS resolution failures on 3 October 2026. The existing generic ERA press-releases URL is marked robots-disallowed. Do not describe the new URL failures as robots restrictions.

- Eurostat API (`ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/...`) works from scripts; see
  `tools/cc-003-report/calc.py` and the helper pattern in the CC-003/004 data files.
- WorldPop and Overpass work from scripts (send a User-Agent to Overpass or it returns 406).
- gov.mt, NSO and ERA pages can be read in a browser but not by scripts.
- Malta's population growth (+41% since 2005) distorts any per-capita metric; check that first in future claims.
- CC-003 and CC-011 are linked by theme T7: the CAA and Labour's manifesto both state a 40% cut by 2030 vs 2005
  with no scope. Worth a follow-up check.
- Claim files exposed by the site builder are copied into `docs/claim-files/`; the map panel offers an on-page viewer and adjacent download action for each output.
- Completed claim outputs share one `addFileAction` implementation. Use `report_pdf`, `flyer_pdf` and `flyer_png` in `claim.yml` for the standard Report / Flyer PDF / Flyer image viewer and download pairs.
