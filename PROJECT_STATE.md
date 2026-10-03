# Project state (working notes)

Read this first when resuming work. It records decisions, conventions and what is outstanding, so a new session can
continue without re-deriving anything. Update it at the end of every work session.

*Last updated: 3 October 2026 (CC-009 v1.0 merged into `main` at `77091be`; CC-010 v1.0 merged into `main` at `f638e15`; CC-002 evidence follow-up continues on `codex/cc-002-follow-up`; CC-007 v1.1 merged at `68025d0`).*

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
| CC-002 Comino tree compensation | Report and flyer v1.1 drafted on `codex/cc-002-follow-up`. Verdict: Largely supported (moderate) for ERA's announced categories and conditions: 624 + 54 = 678; 92.04% non-protected; 54 × 10 = 540; a separate group of 348 is to be transplanted. The developer reports on-site nursery propagation since 2023, but publishes no stock or survival inventory. The full permit annex, 467/468 oleander discrepancy, transplant results and habitat recovery data remain unresolved. Science-only scope; no legal commentary. Right of reply not sought, at maintainer direction. |
| CC-003 Per-capita emissions vs 2030 | Report v1.0 and flyer drafted. **Verdict: Misleading (high).** CAA press release 13 Nov 2025 cites the -44% per-capita figure from the Commission's CAPR 2025 but omits its projection: effort-sharing emissions +41% in 2024, +30% to +42% by 2030 vs -19% target (largest gap in the EU). Half the per-capita fall is population growth. Pending right of reply; **must not be published before the reply deadline.** |
| CC-004 Waste separation | Report v1.0 and flyer drafted. Verdict: Not substantiated (moderate). Separation up; recycling rate 16.7% (2024) vs 55% 2025 target; 79% landfilled; 412 million kg 'diverted' not reconcilable with Eurostat (271 kt). Pending right of reply. |
| CC-005 Bathing water | Styled report and flyer drafted in the shared CC-001 design. The Commission's exact 92% statement matches the EEA 2023 result (80/87); latest 2025 season is 88.5%. Balluta Bay closure and the CJEU wastewater-treatment case are contextual and do not refute the dated statistic. Draft verdict: Supported (high). Right of reply not sought, per maintainer direction. Viewer metadata uses the same Report / Flyer PDF / Flyer image actions as completed checks. |
| CC-011 Manifesto pledges | Report v1.0 and flyer drafted. Verdict: Not substantiated (moderate) for both. Labour's pledge is "open or green" space (not "green space"): 99.9% already within reach on a broad reading, 55-68% for parks of at least 0.5 ha. PN's is a plan for a Net-Zero Gozo by 2040 with afforestation as one of several measures (news said "through afforestation"); no Gozo inventory; afforestation alone would need 1.5-8.5x Gozo's area. Pending right of reply. |
| CC-006 Spring hunting | Report and flyer v1.1 updated on `codex/cc-006-follow-up`. The report tests both Article 9 conditions. Quota-to-statutory-benchmark ratios are 99.3% for Quail and 59.8% for Turtle-dove. Draft verdict: Not substantiated (moderate): the statutory arithmetic is within the benchmark, but the 2026 enforcement outcome and ecological impact are not established. The 30 March 2026 Ornis minutes were not listed in the WBRU archive (checked 3 Oct); latest season outcome report listed was for 2025. Right of reply remains for the maintainer. |
| CC-007 Within EU limits vs WHO guideline | Report and flyer v1.1 merged into `main` at `68025d0`. PQ 29696 supplied by the maintainer; the Minister's answer is procedural, not a compliance claim. All 23 reported values are below the 25 µg/m³ EU limit and above the WHO 5 µg/m³ guideline. EEA validated files cross-check 11 station-years: ten match to 0.1 µg/m³; Attard 2024 differs (12.122 vs 11.9). Two St Paul's Bay values are n/a. Verdict: Largely supported (moderate), pending full series reconciliation. Right of reply remains with the maintainer. |
| CC-008 | Transport | Report v1.0 and flyer merged into `main` at `6e1f342`. Verdict: Not substantiated (moderate). Marsa's 2021 travel-time and emissions percentages are agency-reported; the underlying survey/calculation was not found. Msida wording was prospective; the flyover entered use in December 2025 while the broader project continued. No local before/after noise series located. Pending maintainer right of reply. |
| CC-009 Reverse osmosis and groundwater | Report and flyer v1.0 merged into `main` at `77091be`. WSC's 2025 report: 70.7% RO share; 11.5m m³ groundwater production, lowest decade. Chart values imply an 11.86% fall from 2024, while WSC prose says 11.4%. The latest RBMP reports two main aquifers poor quantitatively, 14 bodies poor chemically and 12/15 above the nitrate standard. Għar Lapsi Plant B was tendered, not commissioned. Verdict: Largely supported (moderate) for reduced WSC groundwater production; this is not proof of aquifer recovery. |
| CC-010 Land & Trees | Report and flyer v1.0 drafted on `codex/cc-010-trees`. Project Green reported >8,000 trees and >25,000 shrubs planted in 2024. Labour pledge 305: 100,000 trees in the next five years (PDF p. 91; printed p. 89). A February 2026 parliamentary answer reports around 60,000 trees and >100,000 shrubs planted collectively by government entities through end-2025. Verdict: Largely supported (moderate) for the reported figures and pledge; the pledge window had not elapsed, and survival/canopy outcomes are unknown. Right of reply remains with the maintainer. |
| CC-012 to CC-021 | Candidates added 3 Oct 2026 (records, sources, literature folders, map links). CC-012 Ta' Qali gravel and grass (both sides); CC-013 Buttigieg: permits keep prices in check; CC-014 Buttigieg: fewer enforcement notices; CC-015 Buttigieg: 'three weeks left' (date check only; scope to confirm); CC-016 shore-to-ship 90%; CC-017 land reclamation (Budget 2026); CC-018 MDA on IMF; CC-019 Amphora: 830,000 m2 land lost; CC-020 noise compliance; CC-021 Gozo tunnel (lead only, weakest). Only CC-013, CC-014 and CC-018 have verbatim wording; the rest need primary sources. New topics Planning & Housing and Noise; new themes T8 (planning, housing and land take) and T9 (compliance-not-health). No NGO claim among them yet. |

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
- [ ] CC-006: obtain the 30 March 2026 Ornis Committee minutes or other primary vote record; monitor for the 2026 WBRU season outcome report; obtain final 2019–2024 Article 12 data, and FKNK survey methods/results. The official WBRU minutes and outcomes pages were checked on 3 Oct: neither the 2026 minutes nor 2026 season outcome report is listed. Right of reply remains for the maintainer.
- [ ] CC-007: reconcile the Attard 2024 difference between the PQ annex (11.9) and EEA mean of valid daily aggregates (12.122); obtain ERA's validated annual series and coverage/quality notes. The EEA files retrieved do not supply 14/25 station-years, including the two St Paul's Bay n/a cells. The Newsbook page was not retrievable for full-text review; an archived snapshot is recorded. Right of reply is for the maintainer.
- [x] CC-008: locate primary wording for Msida and Marsa; draft report/flyer and add evidence notes. Remaining: obtain the Marsa surveys/calculations and comparable local traffic, air and noise series; right of reply remains for the maintainer. Four earlier MaltaToday sources plus the OPM and Times of Malta pages are robots-disallowed and need browser archiving; ERA's source page also blocks automated access. The AEA publisher returned HTTP 403 to the archiver.
- [x] CC-005: locate Commission wording; compare EEA bathing-water seasons 2023–2025; confirm Balluta Bay warning from the EHD primary report; distinguish CJEU wastewater ruling from bathing-water classification.
- [x] CC-005: add sources to `archive/manifest.csv`. Commission page and CJEU judgment have archived snapshots; EEA 2025 is fetched and hashed. EEA 2024 and the EHD Balluta report are robots-disallowed with no snapshot; archive manually if needed. News leads are robots-disallowed but existing snapshots are recorded.
- [ ] CC-005: review drafted verdict, styled report and flyer; reply process remains for maintainer.
- [ ] Obtain open-access full text for the CC-001 A and B studies; fill gaps noted in `literature/CC-001/notes.md`.
- [ ] CC-009: reconcile WSC's 11.4% narrative with the 11.86% chart-derived change if the underlying workbook is obtainable; follow the Għar Lapsi procurement through award and commissioning. Future aquifer recovery requires comparable body-level abstraction, recharge, water-level, salinity and nitrate data. Right of reply remains for the maintainer.
- [x] CC-010: verify manifesto pledge wording, 2024 Project Green counts and end-2025 parliamentary count; calculate the approximate interim proportion; add evidence notes, report, flyer and source records. Two Mediterranean studies provide context only, not a Maltese survival rate.
- [ ] CC-010: obtain the tree-only project register, pledge scope and post-2025 count; follow pledge deadline in 2027; seek cohort survival, replacements and maintenance records. The manifesto PDF is hosted by Talk.mt; no copy was committed. Archive manifest marks this, Ambjent Malta's annual report, the parliamentary PDF and one secondary lead robots-disallowed.
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
CC-005 outputs and viewer metadata were merged and pushed to `main` (merge commit `2110846`). CC-006's report, flyer and site metadata are integrated on `main` at `e0552b9` (fast-forward from `codex/cc-006-spring-hunting`). CC-008 was fast-forwarded and pushed to `main` at `6e1f342`. CC-002's report, flyer, viewer metadata and evidence notes were merged from `codex/cc-002-comino` at `ade9e4b`; v1.1 follow-up is pushed on `codex/cc-002-follow-up` at `bc5b516`, with the permit annex and ecological outcome gaps still unresolved. CC-007 v1.1 with EEA cross-check and session notes was merged into `main` at `68025d0`; the Attard 2024 difference and 14 missing EEA station-years remain unresolved. CC-009 v1.0 was merged into `main` at `77091be`. CC-010 report and flyer v1.0 were merged into `main` at `f638e15`; right of reply and the final pledge-period count remain with the maintainer.

## Notes for the next session

- The homepage map uses the Botanical style and circular balance wordmark. `last_reviewed` dates anchor one leaf per completed evidence review; leaves move from green to brown over 365 days. Update the date after a fresh evidence review and rebuild site data.
- The mobile homepage layout uses a taller map, larger touch targets, direct zoom buttons and two-finger pinch, a slide-up map key, and a bottom-sheet claim panel. Map labels simplify at phone widths; the claims table hides its topic column to stay readable.
- CC-002 editable draft: `claims/CC-002/report.md`; generated outputs: `report.pdf`, `flyer.pdf`, `flyer.png`. Do not treat the 10:1 planting condition as measured ecological equivalence or use cross-study findings as a Comino survival rate. The one-specimen oleander discrepancy remains unresolved.
- CC-008 editable draft: `claims/CC-008/report.md`; generated outputs: `claims/CC-008/report.pdf`, `flyer.pdf`, `flyer.png`. Do not present Marsa's percentages as independently reproduced. No survey file was located. Msida's PDS observations are from 2019 and are not a post-opening counterfactual. The national licensed-fleet figure in the original candidate is not a junction traffic measure and was not used.
- `archive/manifest.csv` records CC-008 source-fetch results. Manual browser archiving is still needed for the four earlier MaltaToday sources, the Office of the Prime Minister and Times of Malta; ERA blocks automated access and the AEA publisher returned HTTP 403. The three Infrastructure Malta pages were fetched and have Wayback snapshots.
- CC-002 direct ERA release URLs and most newly added sources remain unarchived because the archive script encountered temporary DNS resolution failures on 3 October 2026. The existing generic ERA press-releases URL is marked robots-disallowed. Do not describe the new URL failures as robots restrictions.
- CC-007 editable source transcription: `literature/CC-007/primary-source.md`; generated outputs: `claims/CC-007/report.pdf`, `flyer.pdf`, `flyer.png`. EEA validated-data comparison files and hashes are in `data/cc-007/`. The EEA daily mean for Attard 2024 is 12.122 µg/m³ versus 11.9 in the PQ annex; do not silently reconcile the difference. EEA files retrieved do not cover 14 of 25 possible station-years.

- Eurostat API (`ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/...`) works from scripts; see
  `tools/cc-003-report/calc.py` and the helper pattern in the CC-003/004 data files.
- WorldPop and Overpass work from scripts (send a User-Agent to Overpass or it returns 406).
- gov.mt, NSO and ERA pages can be read in a browser but not by scripts.
- Malta's population growth (+41% since 2005) distorts any per-capita metric; check that first in future claims.
- CC-003 and CC-011 are linked by theme T7: the CAA and Labour's manifesto both state a 40% cut by 2030 vs 2005
  with no scope. Worth a follow-up check.
- Claim files exposed by the site builder are copied into `docs/claim-files/`; the map panel offers an on-page viewer and adjacent download action for each output.
- Completed claim outputs share one `addFileAction` implementation. Use `report_pdf`, `flyer_pdf` and `flyer_png` in `claim.yml` for the standard Report / Flyer PDF / Flyer image viewer and download pairs.
