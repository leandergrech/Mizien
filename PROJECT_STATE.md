# Project state (working notes)

Read this first when resuming work. It records decisions, conventions and what is outstanding, so a new session can
continue without re-deriving anything. Update it at the end of every work session.

*Last updated: 2 October 2026.*

## What the project is

Miżien: an independent, science-first record of fact-checks on public claims in Malta (authorities, institutions,
parties, NGOs, opposition), focused on quality of life and the environment. Homepage is a 3D mind map of all claims
grouped by topic with links between them. The repository is public and doubles as the assistant's persistent storage.

## Repository

https://github.com/leandergrech/Mizien (public). Site: https://leandergrech.github.io/Mizien/ once Pages is enabled
(Settings, Pages, deploy from `main`, `/docs`). The repo URL is printed on the CC-001 report cover and flyer.
As of 2 October 2026 the repository was created but still empty; the starter package is the first commit.

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
  Report structure in `methodology/report-outline.md`; generators in `tools/cc-001-report/`.
- **Spreadsheet:** `data/candidates.xlsx` is the tracker. `data/*.csv` are exports. After changing claim records run
  `python scripts/build_site_data.py`.

## Status

| ID | Status |
|---|---|
| CC-001 Upper Barrakka concrete | Report v1.1 and flyer done. Verdict: Not substantiated (plausible, not shown). Draft pending right of reply. |
| CC-002 to CC-011 | Candidates only. Start with CC-003 (climate) and CC-004 (waste): public datasets only. |

## Outstanding

- [ ] Decide author or affiliation line for reports and flyer (none yet).
- [ ] Add the Times of Malta article URL to `data/sources.csv` and `claims/CC-001/claim.yml`.
- [ ] Run `python scripts/archive_sources.py` to fill `archive/manifest.csv`.
- [ ] Send CC-001 draft to Ambjent Malta and Fondazzjoni Wirt Artna; record dates in `claims/CC-001/claim.yml`.
- [ ] Locate verbatim primary-source wording for CC-005 to CC-010 before any report.
- [ ] Obtain open-access full text for the CC-001 A and B studies; fill gaps noted in `literature/CC-001/notes.md`.
- [ ] Collect literature for CC-002 to CC-011 (each folder lists what to collect).
- [ ] Check the name and a domain are free; enable GitHub Pages (main, /docs).
- [ ] CC-002 (Comino) is before a planning tribunal: keep to the science.

## How to resume a session

1. Clone the repository (it is public) and read this file, `README.md` and `data/claims.csv`.
2. Pick the next claim from the table above; open its `claim.yml`.
3. Collect literature into `literature/CC-NNN/`, then build the report from `methodology/report-outline.md`.
4. Hand the finished files to the maintainer to commit (the assistant has no push access).
