# Pledge labels

Maintainer decision, 5 October 2026. A pledge (a promise of future action, with or without a target) is not a
statement of fact, so it does not get a verdict on the five-point scale. It gets one of the labels below instead.
Every label carries an **as of** date: the date of the evidence behind it.

| Label | Meaning |
|---|---|
| **Not measurable** | The pledge as worded has no target, baseline or deadline against which progress can be checked. |
| **Not yet due** | The deadline or term has not passed, and there is not yet enough evidence to judge progress. |
| **On track** | Progress so far, shown by evidence, is at or above the pace needed to meet the target by the deadline. |
| **Off track** | Progress so far, shown by evidence, is below the pace needed to meet the target by the deadline. |
| **Met** | The target has been reached, shown by evidence. |
| **Missed** | The deadline or term has passed and the target was not reached. Used only after the deadline or term, with the evidence listed in `evidence_shown`. |

## Where labels show

- A **pure pledge check** (no factual claim to test) shows only its pledge label, and has no verdict:
  CC-011 (Labour: ten minutes' walk to green space) and CC-107 (PN: net-zero Gozo by 2040).
- A **mixed check** keeps its verdict for the factual part and also shows the label: CC-010 keeps *Largely supported*
  for the tree counts, and its 100,000-tree pledge is *Off track*.

## The `pledge:` block in claim.yml

```yaml
pledge:                             # illustrative values
  status: Off track                 # one of the labels above
  as_of: 2026-10-05                 # date of the evidence behind the label (a full date)
  made_by: [pl]                     # ids from data/bodies.csv
  made_on: 2022                     # date pledged (a year or month is enough)
  vehicle: "Party manifesto 2022, pledge 305"
  deadline: 2027                    # date, or null if none is stated
  target: "100,000 trees in five years"
  term_end: 2026-05-30              # optional: when the term the pledge was made for ended, if that matters
  occasion: "Party manifesto 2022"  # optional: what it was pledged in (default: vehicle up to its first comma)
  overlaps: [CC-NNN]                # optional: other pledges that overlap with this one
```

`scripts/validate_claims.py` checks the block: the label, an `as_of` full date not before `made_on`, `made_by` ids
in the register, `vehicle` and `target`, a parseable or null `deadline`, and that **Not yet due** is used only before
the deadline and **Missed** only after the deadline or term and with `evidence_shown`.
