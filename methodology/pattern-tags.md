# Pattern tags

Tags describe recurring ways a claim can mislead. They are for filtering and for the mind map, not accusations.
Tags are **provisional** until a report is finished.

| Tag | Meaning |
|---|---|
| **Selective metric** | A favourable metric is cited while the regulator-relevant metric looks worse. |
| **Input-as-outcome** | Effort counted (trees planted, kilograms separated) is presented as if it were the result (trees surviving, recycling rate). |
| **Compliance-not-health** | Meeting a legal limit is presented as if it meant a health-protective level. |
| **Conditional-turned-unconditional** | A statement with a stated condition is reported or repeated without it. |
| **Promise-without-baseline** | A target or pledge with no stated starting point, scope or counting basis. |

## Adding a pattern

New patterns are proposed by the weekly intake (see `methodology/automation.md`). Add a row to the table above
with the tag in bold; `scripts/validate_claims.py` reads the allowed tags from this table. A new tag is provisional
until at least two finished reports confirm it.
