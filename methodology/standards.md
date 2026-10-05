# Standards

1. **Quote the speaker, not the headline.** Give outlet and date, link the original, and archive it.
2. **Separate the claim from the evidence offered for it,** and say who made which statement.
3. **Grade the evidence** and show differing views side by side where the science is unsettled.
4. **State what we could not access or verify,** and what would change the verdict either way.
5. **Ask for the missing evidence** in specific, answerable requests.
6. **Offer a right of reply** before wider circulation when a check finds a claim *Not substantiated*, *Misleading* or
   *Contradicted*, and append the response. A check that finds a claim *Supported* or *Largely supported* needs none.
7. **Correct errors openly** with a version number and change log.
8. **Whistle-blow only on evidence.** A verdict of Misleading or Contradicted requires documents or data that can be shown.
9. **Check every side.** Governments, opposition parties, NGOs, developers and agencies are held to the same standard.
10. **Be fair about trade-offs.** Say when a goal is legitimate (for example protecting heritage tunnels from flooding) and keep the check to the factual statement.

## Evidence review freshness

- Record the date the evidence was last reviewed in `claim.yml` as `last_reviewed: YYYY-MM-DD` when a report is complete.
- A botanical map leaf represents one completed evidence review in its topic group. Its colour moves from green to brown over 365 days; brown indicates that the evidence review is due for refresh.
- After refreshing a review, update `last_reviewed` and run `python scripts/build_site_data.py` so the map and preview use the new date.

## Right of reply (proposed procedure; edit as needed)

- When: only for a verdict of *Not substantiated*, *Misleading* or *Contradicted*; for a pledge, the labels *Not
  measurable*, *Off track* and *Missed* (maintainer decision, 5 October 2026). A check that supports a claim needs no
  reply. Where the maintainer decides not to seek one, record `right_of_reply.sought: false` with a `note`.

- Send the draft to the body concerned with a fixed deadline (suggested: 14 days).
- Record the date sent in `claim.yml` (`right_of_reply.sent`) and the deadline.
- Publish the response alongside the report. If new evidence moves the verdict, re-issue with a change log.
- Do not publish a *Misleading* or *Contradicted* verdict before the deadline has passed.

## Sub judice and live proceedings

Where a matter is before a tribunal or court, keep to the science and the public record. Do not comment on legal merits.

## Quoting and copyright

- Quote the claim itself briefly (a short phrase or sentence) and link to the archived source.
- Paraphrase everything else. Do not reproduce articles, paywalled papers or long passages.
- Commit only open-access PDFs to `literature/`. For everything else store the citation, DOI, link and our own notes.
