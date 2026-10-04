# Miżien

*Weighing public claims against the evidence.*

Repository: https://github.com/leandergrech/Mizien

**Miżien** (Maltese for a scale or balance) is an open, independent record of science-first checks on public claims
made in Malta by authorities, institutions, parties, NGOs and others, with a focus on quality of life and the
environment. Every claim is tested against the scientific literature first, then against official and independent
data. Every source is archived, so the record of what was said survives edits and deletions.

## How a claim is checked

1. **Record the claim** in the speaker's own words, with outlet, date and link. Archive the source.
2. **Split it** into checkable sub-claims.
3. **Search the science first**, then independent datasets, then regulator and EU reports.
4. **Grade the evidence** (A to D) and show disagreements side by side.
5. **Give a verdict** on a five-point scale, with a confidence level.
6. **Offer a right of reply** to the body concerned and publish its response.
7. **Publish with a version number and change log**, and correct errors openly.

Misleading or Contradicted verdicts need documents or data that can be shown. See [`methodology/`](methodology/).

## Verdict scale

Supported · Largely supported · **Not substantiated** · Misleading · Contradicted. Definitions are in
[`methodology/verdict-scale.md`](methodology/verdict-scale.md).

## Claims

| ID | Topic | Claim | Status | Verdict |
|---|---|---|---|---|
| CC-001 | Land & Trees | Upper Barrakka concrete | Drafted | Not substantiated |
| CC-002 | Land & Trees | Comino tree compensation | Drafted | Largely supported |
| CC-003 | Climate & Energy | Per-capita emissions vs 2030 projection | Drafted | Misleading |
| CC-004 | Waste | 'Strong progress' in waste separation | Drafted | Not substantiated |
| CC-005 | Water | '92% excellent' bathing water | Drafted | Supported |
| CC-006 | Nature & Wildlife | Spring hunting derogation | Drafted | Not substantiated |
| CC-007 | Air | Within EU limits vs WHO guideline | Drafted | Largely supported |
| CC-008 | Transport | Flyovers and congestion | Drafted | Not substantiated |
| CC-009 | Water | Reverse osmosis and groundwater | Drafted | Largely supported |
| CC-010 | Land & Trees | Tree-planting counts | Drafted | Largely supported |
| CC-011 | Governance & Promises | 2026 manifesto pledges | Drafted | Not substantiated |
| CC-012 | Land & Trees | Ta' Qali gravel and grass | Drafted | Contradicted |
| CC-013 | Planning & Housing | Permits keep property prices in check | Drafted | Largely supported |
| CC-014 | Planning & Housing | Fewer enforcement notices, fewer illegalities | Drafted | Misleading |
| CC-015 | Governance & Promises | 'Three weeks left' at the PA | Not started | - |
| CC-016 | Air | Shore-to-ship: 90% less harbour pollution | Drafted | Misleading |
| CC-017 | Planning & Housing | Land reclamation outside the Freeport | Drafted | Not substantiated |
| CC-018 | Planning & Housing | IMF 'confirms' MDA on housing | Drafted | Largely supported |
| CC-019 | Land & Trees | 830,000 m2 of land lost in five years | Drafted | Largely supported |
| CC-020 | Noise | Noise: compliant on paper | Not started | - |
| CC-021 | Transport | Malta-Gozo tunnel traffic | Not started | - |

The interactive 3D map is the homepage of the site (`docs/`). Claim documents open in an on-page viewer, with a separate download button. Claims are numbered CC-001 to CC-021. Report drafts are available for CC-001 to CC-011; CC-012 to CC-021 are candidates (added 3 October 2026). Right of reply remains for the maintainer where not yet handled.

## Repository map

```
claims/CC-NNN/       claim.yml (the record), report.pdf, flyer.pdf, flyer.png
methodology/         verdict scale, evidence grades, pattern tags, standards, templates, automation
data/                claims.csv, edges.csv, themes.csv, sources.csv, quick_checks.csv, claims.json, candidates.xlsx
literature/CC-NNN/   references.bib, notes.md, open-access PDFs only
archive/             manifest.csv of archived claim sources (links and hashes)
docs/                the GitHub Pages site with the 3D mind map (moving into site/)
site/                Eleventy templates for the built site (eleventy.config.js, package.json)
scripts/             validate_claims.py, build_site_data.py, archive_sources.py
tools/               mizien_report.py (shared report and flyer design) and per-claim generators
PROJECT_STATE.md     working notes: conventions, design tokens, status and next steps
```

## Run it locally

```
pip install -r scripts/requirements.txt
python scripts/validate_claims.py
python scripts/build_site_data.py
python -m http.server -d docs      # open http://localhost:8000
```

To build the full site as it will be deployed (needs Node 24, see `.nvmrc`):

```
npm ci
npm run build                      # validates, rebuilds data, then runs Eleventy into _site/
PATH_PREFIX=/ npx eleventy --serve # preview at http://localhost:8080
```

Editing claims does not need Node: CI builds the site on every pull request.

## Publish the site

The site is at https://leandergrech.github.io/Mizien/. Today GitHub Pages serves the `main` branch's `/docs` folder.
The `Site` workflow (`.github/workflows/site.yml`) builds the site with Eleventy on every pull request. To deploy it
from Actions instead, set **Settings › Pages › Source** to "GitHub Actions" and add the repository variable
`PAGES_SOURCE` = `actions`.

## Contribute or contest a verdict

See [`CONTRIBUTING.md`](CONTRIBUTING.md) and [`CORRECTIONS.md`](CORRECTIONS.md). Use the issue forms to propose a
claim, contest a verdict, or reply as the body concerned.

## Licences

Content: CC BY 4.0 ([`LICENSE-CONTENT.md`](LICENSE-CONTENT.md)). Code: MIT ([`LICENSE`](LICENSE)). Third-party
material remains under its owners' rights.

## Independence

Miżien is independent and is not affiliated with any party, authority or institution. Drafts are marked as pending
right of reply until the body concerned has had the chance to respond.
