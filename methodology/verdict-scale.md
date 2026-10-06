# Verdict scale

Every check ends with one verdict and a confidence level.

| Verdict | Meaning |
|---|---|
| **Supported** | Evidence consistently backs the claim as stated. |
| **Largely supported** | Backed by the evidence, with minor caveats that do not change the substance. |
| **Not substantiated** | Stated more strongly than the evidence offered or available allows. May be true in some conditions but has not been shown. |
| **Misleading** | Omits material facts so that the overall impression is inaccurate, even if individual statements are defensible. |
| **Contradicted** | The available evidence points against the claim. |

## Confidence

- **High**: multiple independent lines of evidence agree.
- **Moderate**: evidence is relevant but incomplete or indirect.
- **Low**: evidence is thin, second-hand or conflicting.

## Rules

- *Misleading* and *Contradicted* require documents or data that can be shown (`evidence_shown` in the claim record). Inference alone is not enough.
- A verdict applies to the **claim as the speaker worded it**, not to a headline or paraphrase of it. Where a headline drops a condition, say so.
- A verdict is not a judgement of motive. Nothing here says anyone acted in bad faith unless documents show it.

## Pledges

A pledge is a promise of future action: a manifesto commitment, a budget measure or a target. It cannot be true or
false when it is made, so it gets a pledge label instead of a verdict (maintainer decision, 5 October 2026). Each
label carries an "as of" date: the date of the evidence behind it.

- **Not measurable**: the pledge as worded has no definition, baseline or date against which delivery could be checked.
- **Not yet due**: the pledge is measurable, its deadline or term has not passed, and no progress data have been published yet.
- **On track**: published progress is at or ahead of a straight-line path (or the pledge's own milestones) to the target by the deadline.
- **Off track**: published progress is behind that path, and the target has not yet been shown to be met or missed.
- **Met**: documents or data show the target was reached, by the deadline if one was set.
- **Missed**: the deadline or term has passed, and documents or data that can be shown say the target was not reached.

Rules for pledges:

- A check of a pledge alone (for example CC-011, CC-107) shows the pledge label instead of a verdict. A check that also tests factual statements (for example CC-010's planting counts) keeps its verdict for those and shows the pledge label as well.
- *Missed* needs the deadline or term to have passed and evidence that can be shown, as for *Misleading* and *Contradicted*. Without a count at the deadline, the label stays at the last one the evidence supports.
- A label judges delivery against the pledge as worded, not anyone's intent. Revisit it when new data are published or the deadline passes, and record the change in the claim's research log.
- In `claim.yml` the label sits in a `pledge:` block: `status` (one of the labels above), `as_of`, `made_by` (ids in `data/bodies.csv`), `made_on`, `vehicle` (the manifesto, budget or plan), `deadline` (a date, or null when none is stated), `target`, `kind` (below), and an optional `note`.

### Kinds, election cycles and links (maintainer decisions, 6 October 2026)

Pledges are not made continuously: most come in bursts around elections. Each pledge has a `kind`:

- **campaign**: a manifesto or campaign promise, made before an election.
- **government**: a commitment made in office (budget speech, strategy, EU plan, ministerial statement).
- **proposal**: a party proposal made outside a campaign, or in opposition.
- **target**: a target set by an agency or company. Not a political promise; it keeps a label but is listed apart from the pledges.

Each pledge belongs to an **election cycle** (`data/cycles.csv`: the election and the legislature after it). A campaign
pledge belongs to the election it was made for (the first election on or after the date it was made); any other
pledge to the cycle in force when it was made (at the start of the period its date names, so a commitment dated only
by the month or year of an election falls in the earlier cycle). An explicit `cycle:` overrides this.

`data/manifesto_pledges.csv` is a light list of manifesto pledges (party, cycle, number, page, wording, archived
source), most never checked, so that pledges can be linked and promises nobody took up can be found. Wording is entered
only when transcribed verbatim from the archived document (`wording_status: Verbatim found`).

Optional fields that link a pledge to earlier ones:

- `follows: [CC-NNN or MP-...]`: the earlier pledge(s) this one carries forward. Set by a person at check time; similar
  wording found automatically is only ever shown as "similar", never as a link.
- `follows_search: {date, searched: [the manifestos or documents searched], found: [...]}`: recorded when looking for
  an earlier pledge, whatever the result.
- `drift: {type, note}`: how a linked commitment differs from the promise. Types: target lowered, deadline moved, scope
  narrowed, measure changed; the note gives both wordings.
- `source_of_commitment`: where a commitment first appears when it has no earlier pledge (for example "Budget Speech
  2026" or "EU regulation 2018/1999 (NECP)").

### Outliers

An outlier breaks the expected chain *campaign promise → government commitment → outcome*. Each is stated as a
finding with what it rests on, never as an inference, and never about motive:

- **Unanchored**: a government commitment with no earlier pledge. Shown only after a recorded `follows_search`:
  "No earlier pledge found (searched: Labour manifesto 2022, PN manifesto 2022, 5 Oct 2026). Commitment first appears in: Budget Speech 2026."
- **Dropped**: a campaign pledge of the governing party with no government follow-up. Only after the legislature has
  ended (or a stated review date) and a recorded search; until then "no follow-up found yet".
- **Drift**: linked, but the commitment differs from the promise: "Changed from the 2022 manifesto: deadline moved from 2027 to 2030."
- **Recycled**: the same promise made again in a later cycle while the earlier one was not met: "Also promised in 2022 (CC-010, Off track)."

Opposition proposals cannot be dropped or drift in the same way; they are followed only as recycled across elections,
or as adopted by a government.

## Summaries on Who said it

The "Who said it" pages summarise the verdicts on each body's claims (its own, its offices' and its people's), never a
person's. Five or more checked claims: a verdict bar of counts (no percentages). Three or four: a tentative balance on
a line from Contradicted (0) through Misleading (0.25), Not substantiated (0.5) and Largely supported (0.75) to
Supported (1), the average weighted by the age of each claim (the date it was made, not checked): the weight halves
every two years; an undated claim counts as three years older than the body's oldest dated checked claim, and if none
is dated all count the same, so the balance changes only when claims or verdicts do. Fewer than three: a count only.
Draft verdicts are counted. Pledge labels are shown separately and never counted as verdicts. Computed at build time
in `site/_lib/who.js`; explained to readers on the Connections page (`/methodology/connections/#summaries`).
