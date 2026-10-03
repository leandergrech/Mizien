# Automation

Three kinds of scheduled cloud routine (Claude Code) work on this repository. Their prompts live in the routines
themselves (claude.ai/code/routines); this file records the conventions they share.

## Nightly checkers (workers A, B, C)

- Each worker checks one claim per night, chosen from `data/queue.csv` rows with its letter, in ID order, skipping any
  claim whose status is not `Not started` or that already has a remote branch or open PR.
- Output, records and rules are as for any claim check (CLAUDE.md). Each finished claim is merged via its own PR.

## Weekly intake

- Adds up to ten new candidate claims a week, found on the web, as `Not started` records (no verdicts).
- Balances topics and sides (government, regulators, parties, business, NGOs, media, EU) towards the
  least-covered ones, and avoids duplicates of existing claims.
- Assigns each new claim to a worker in `data/queue.csv`, keeping the three workers' open loads even.
- May split a large topic into subtopics with the optional `subtopic` field in `claim.yml` (shown by the
  "Subtopic" grouping on the map); topics themselves (`category`) are renamed only when clearly needed.
- Reviews all claims for recurring patterns and shared mechanisms: new pattern tags go in
  `methodology/pattern-tags.md` (provisional), new themes and link types in `data/themes.csv` and `data/edges.csv`
  (strength `Weak (indicative)` or `Pattern, not causal` until a report confirms them).
- Never changes a verdict, a finished report, or a claim that has a report.

## Queue file

`data/queue.csv` columns: `ID, Worker, Added, Note`. Worker is `A`, `B` or `C`. Validated by
`scripts/validate_claims.py`.
