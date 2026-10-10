# Automation

Scheduled cloud routines (Claude Code) work on this repository. The claim-check workers' instructions live in
`worker-routine.md` (since 5 Oct 2026); each worker routine's own prompt (claude.ai/code/routines) only names its
letter and points to that file. The intake routine's prompt still lives in the routine. This file records the
conventions they share. Rules in `CLAUDE.md` apply in full.

## Pipeline

```
weekly intake (Sun) ──> data/queue.csv ──> workers A, B, C (nightly) ──> PR per claim, merged ──> site
        │                     ▲                     │
        │                     └── attempt/blocker ──┘
        └── topics, subtopics, patterns, themes, edges
```

## Network preflight

Practical notes on sources that work and pitfalls: `methodology/data-sources.md`.

Cloud runs sit behind an egress allowlist. A host the allowlist refuses cannot be read at all, by any tool.
Every run therefore starts with `python scripts/net_check.py`:

- **Exit 3 (locked):** core research hosts (Crossref, Eurostat, EEA, Wayback) are refused. The run changes
  nothing, opens no PR and reports the refused hosts. The maintainer must widen the environment's network access.
- Before each claim, `python scripts/net_check.py CC-NNN` checks that claim's source hosts. **Exit 4 (blocked)**
  means none can be reached: record the attempt (below) and move to the next claim.
- `site-refused` (a bot wall such as 403 or 503) is not a proxy block: try the Wayback copy, another outlet
  quoting the speaker directly, or the parliamentary record before giving up.

## Nightly checkers (workers A, B, C)

- Each worker takes rows of `data/queue.csv` with its letter, in ID order, and completes at most **one** claim per
  run. A claim is eligible when its status is `Not started` or `In progress`, its `Blocker` cell is empty or starts
  with `network`, it has no open PR or live remote branch from another run, and (if `Attempts` > 0) its
  `Last attempt` is at least 6 days old. A maintainer unblock (empty `Blocker` and a
  `literature/CC-NNN/primary-source.md`) is eligible at once, without the 6-day wait.
- A worker may try up to three eligible claims in one run, stopping at the first it completes.
- **Blocked claim:** do not change its caveats or wording status. Increment `Attempts`, set `Last attempt` to today
  and `Blocker` to a short reason (`network: host1, host2` or `source: what is missing`). Useful leads found on the
  way go in `data/sources.csv` (marked not retrieved) and `literature/CC-NNN/README.md`. At 3 attempts set
  `Blocker` to `needs maintainer: <what to supply>`; workers then skip the claim.
- **Waiting on the maintainer:** when the `Blocker` starts with `source:` or `needs maintainer` (browser-only
  sources included), set the claim's status to `In progress` in `claim.yml` (`data/claims.csv` follows it), so the
  site shows it as started, and log the attempt in the claim's `history:` (`started`, then `note` for later attempts).
  A `network:` blocker leaves the status unchanged, since no work could be done.
- **Maintainer unblock:** paste the verbatim passages (with URL, outlet, date and date read) into
  `literature/CC-NNN/primary-source.md`, as for CC-007, and clear the `Blocker` cell. Workers treat that file as
  the archived primary wording.
- **Finished claim:** report, flyer and records as for any claim check; `Blocker` cleared.
- **Parts and pledges:** copy the report's sub-claim table into `subclaims:` in claim.yml (ids CC-NNNA, CC-NNNB...
  in order, with text, finding, rating and the chip's colour as `tone`); parts share their claim's page and appear
  on the map as satellites of it. A pledge gets a `pledge:` block with a label from the Pledges section of `methodology/verdict-scale.md`
  instead of a verdict: a pure pledge has `verdict: null`; a check that also tests facts keeps its verdict for them.
  `Missed` needs the deadline or term to have passed and `evidence_shown`.
- **Research log:** every run that does research on a claim adds a dated entry to its `history:` in `claim.yml`,
  using the date the research was done (today), not a merge or release date: `started` when work first begins,
  `wording` when the verbatim source is found, and `version` (with the version number and a one-line note matching
  the report's revision log) for each issue of the report. A finding that was wrong is fixed with a `correction`
  entry, and a right finding that could mislead gets a `clarification`; both need a note saying what was wrong and
  what changed. They appear on the claim page and on the site's Corrections page. `validate_claims.py` fails when a
  `version` has no entry.
- **Concurrency:** if `main` has moved, `git merge origin/main` into the branch (never rebase a pushed branch,
  never force-push), keep both sides' CSV rows, regenerate data with `scripts/build_site_data.py`, and re-run
  `scripts/validate_claims.py`, which fails on any leftover conflict marker.

## Weekly intake

- Adds up to ten new candidate claims a week, found on the web, as `Not started` records (no verdicts).
  Web search works even when hosts are refused; candidates whose wording could not be read are recorded as
  `Paraphrase: locate quote`.
- Balances topics and sides (government, regulators, parties, business, NGOs, media, EU) towards the
  least-covered ones, and avoids duplicates of existing claims.
- Assigns each new claim to a worker in `data/queue.csv`, keeping the three workers' open loads even.
- May split a large topic into subtopics with the optional `subtopic` field in `claim.yml` (shown by the
  "Subtopic" grouping on the map); topics themselves (`category`) are renamed only when clearly needed.
- Reviews all claims for recurring patterns and shared mechanisms: new pattern tags go in
  `methodology/pattern-tags.md` (provisional), new themes and link types in `data/themes.csv` and `data/edges.csv`
  (strength `Weak (indicative)` or `Pattern, not causal` until a report confirms them).
- Matches every new claim's speaker to the register of bodies and people (`data/bodies.csv`): add the speaker's
  exact wording to the `Aliases` of the right row (separated by `|`), or add a row with `ID, Name, Kind`
  (organisation or person), `Type`, `Parent` (a person's office), `Role` (as the source names it) and `Aliases`.
  `scripts/validate_claims.py` warns on any speaker that matches nothing. Never guess a role or affiliation.
- Follows stances over time: when a body repeats, changes or corrects a claim already listed, add the new statement as a
  claim of its own if it can be checked; otherwise add it to the existing claim's `timeline:` (date, kind, text, url;
  kinds: statement, data, reply, correction, note). New data that bears on a finished check goes there too, as `data`.
- Gives every new claim a `location` (place, lat, lon from OpenStreetMap or the source; scope `site`, or
  `institution`/`national` with the institution's address) so it appears on the map view, and an `icon` for its
  landmark medallion: one of the `place:` emblems in `site/assets/glyphs.js` (the glyph key at `/about/glyphs/` lists them
  with the places that use each; `pin` is the generic fallback). Use an emblem of its own for a place with an identity
  (a landmark, a plant, a bay) and share one only for the same kind of place (two ferry terminals). A claim about the
  whole country uses the Maltese cross (`cross`). Reuse the place name exactly when a claim shares a site, and give
  every claim at a place the same emblem. A new emblem is a new `place:` entry in `site/assets/glyphs.js` (a 24 x 24
  stroke-only path, drawn like the others); `scripts/validate_claims.py` and the site build read that file, and the
  build log warns about any place left on the generic pin. A new topic, subtopic, pledge label or theme needs a glyph in
  the same file (until it has one it shows its parent's, and the build log says which are missing).
- Never changes a verdict, a finished report, or a claim that has a report.

## Sheets

`claims/CC-NNN/claim.yml` is the source of truth; the tracker sheets are generated from it by `scripts/sheets.py`,
which `scripts/build_site_data.py` runs on every build: `data/claims.csv` (the claim sheet), `data/facts.csv` (every
row of every `data/cc-nnn/checks.csv`: the fact sheet), `data/actors.csv` (organisations and their claims, from the
register), the themes' edge counts in `data/themes.csv`, and the README claims table. Do not edit them by hand. The
workbook `data/candidates.xlsx` gathers every sheet (claims, facts, quick checks, patterns, themes, edges, sources,
bodies, actors, queue); it is binary, so only the maintainer's session rebuilds it (`python scripts/sheets.py --xlsx`),
at the end of a session. Hand-curated: `data/edges.csv`, `data/themes.csv` (except the counts), `data/sources.csv`,
`data/quick_checks.csv`, `data/queue.csv`, `data/bodies.csv`.

## Queue file

`data/queue.csv` columns: `ID, Worker, Added, Note, Attempts, Last attempt, Blocker` (CRLF line endings).
Worker is `A`, `B` or `C`; Attempts is a whole number. Validated by `scripts/validate_claims.py`.
