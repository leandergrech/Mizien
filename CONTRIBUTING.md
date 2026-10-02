# Contributing to Miżien

Thank you for helping weigh claims against the evidence.

## Propose a claim

Open an issue with the **Propose a claim** form. A good proposal has:

- the exact words, who said them, where and when, with a link;
- why it can be tested against science or data;
- a quality-of-life or environmental angle for people in Malta.

We check claims from every side: governments, opposition parties, NGOs, agencies, developers and companies.

## Contest a verdict or correct an error

Open an issue with the **Contest a verdict** form and attach the evidence. Corrections are logged in the claim's
revision log. If a correction changes a verdict, the report is re-issued with a new version number.

## Add literature

Add the citation to `literature/CC-NNN/references.bib` and a line to `notes.md` saying what you read (full text,
abstract or second-hand). Only commit PDFs that are open access.

## Before you open a pull request

```
pip install -r scripts/requirements.txt
python scripts/validate_claims.py
python scripts/build_site_data.py
```

## Ground rules

- Be accurate, be fair, be specific. Criticise statements, not people.
- No personal data beyond what appears in the public statement being checked.
- Do not submit paywalled PDFs or long quotations.
