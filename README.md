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
| CC-002 | Land & Trees | Comino tree compensation | Not started | - |
| CC-003 | Climate & Energy | Per-capita emissions vs 2030 projection | Drafted | Misleading |
| CC-004 | Waste | 'Strong progress' in waste separation | Drafted | Not substantiated |
| CC-005 | Water | '92% excellent' bathing water | Not started | - |
| CC-006 | Nature & Wildlife | Spring hunting derogation | Not started | - |
| CC-007 | Air | Within EU limits vs WHO guideline | Not started | - |
| CC-008 | Transport | Flyovers and congestion | Not started | - |
| CC-009 | Water | Reverse osmosis and groundwater | Not started | - |
| CC-010 | Land & Trees | Tree-planting counts | Not started | - |
| CC-011 | Governance & Promises | 2026 manifesto pledges | Not started | - |

The interactive 3D map is the homepage of the site (`docs/`). Candidates are numbered CC-001 to CC-011; all but
CC-001 are still to be checked.

## Repository map

```
claims/CC-NNN/       claim.yml (the record), report.pdf, flyer.pdf, flyer.png
methodology/         verdict scale, evidence grades, pattern tags, standards, templates
data/                claims.csv, edges.csv, themes.csv, sources.csv, quick_checks.csv, claims.json, candidates.xlsx
literature/CC-NNN/   references.bib, notes.md, open-access PDFs only
archive/             manifest.csv of archived claim sources (links and hashes)
docs/                the GitHub Pages site with the 3D mind map
scripts/             validate_claims.py, build_site_data.py, archive_sources.py
tools/               generators for the CC-001 report and flyer
PROJECT_STATE.md     working notes: conventions, design tokens, status and next steps
```

## Run it locally

```
pip install -r scripts/requirements.txt
python scripts/validate_claims.py
python scripts/build_site_data.py
python -m http.server -d docs      # open http://localhost:8000
```

## Publish the site

In the repository settings choose **Pages**, then deploy from the `main` branch and the `/docs` folder. The site will be at https://leandergrech.github.io/Mizien/.

## Contribute or contest a verdict

See [`CONTRIBUTING.md`](CONTRIBUTING.md) and [`CORRECTIONS.md`](CORRECTIONS.md). Use the issue forms to propose a
claim, contest a verdict, or reply as the body concerned.

## Licences

Content: CC BY 4.0 ([`LICENSE-CONTENT.md`](LICENSE-CONTENT.md)). Code: MIT ([`LICENSE`](LICENSE)). Third-party
material remains under its owners' rights.

## Independence

Miżien is independent and is not affiliated with any party, authority or institution. Drafts are marked as pending
right of reply until the body concerned has had the chance to respond.
