# Fact ledger: design sketch

A brainstorm, not a feature. Nothing here is used by the site build, `scripts/validate_claims.py` or
`scripts/build_site_data.py`, and no claim record depends on it. It tests one idea: keep checked facts once, with
their sources, so a new claim is first compared with what Miżien already holds before anyone opens a PDF.
Background, estimates and decisions: `PROJECT_STATE.md`, section "Fact ledger: design sketch (7 October 2026)".

## What is here

| File | What it is |
|---|---|
| `design.html` | The design proposal: inventory of what the project holds, state of the art, data model, build cost by phase, savings model with scenarios, impact on corrections, effect on the site's views. Open it in a browser. |
| `ledger/bases.csv` | The ways emissions are counted: territorial inventory, residence accounts, effort-sharing scope, and context (population, GDP, energy). |
| `ledger/series.csv` | 14 data series, each tied to one basis (dataset, filter, measure, unit). |
| `ledger/facts.csv` | 37 facts, hand-curated from six emissions checks (CC-003, CC-025, CC-026, CC-031, CC-109, CC-114). Key: series + measure + period + unit. `refs` points to the check rows each fact rests on (`CC-NNN:line` in `data/cc-nnn/checks.csv`, header = line 1). |
| `ledger/links.csv` | 56 links from sub-claims to facts, each with a role: supports, contradicts or context. |
| `ledger/explained.csv` | A person's explanation for each flagged pair (status explained, revision or open). |
| `build.py` | Verifies every fact against the check rows it cites, scans all check rows for figures repeated across reports, applies the consistency rule (same series, measure, period and unit must agree), computes claim-to-claim links through shared facts and compares them with `data/edges.csv`. Writes `ledger.sqlite` and `graph.json`. |
| `precheck.py` | Toy pre-check: reads a sentence, lists matching facts, earlier verdicts, the same fact on another basis, and notes. No language model: a small word list, number matching and direction (rise or fall). |
| `make_page.py`, `page_template.html` | Build `sketch.html`, the clickable graph (claims, sub-claims, facts, series, basis). |
| `bench/` | Benchmark of claim and fact matching on the project's own data (below). |

Generated files (`ledger.sqlite`, `graph.json`, `precheck.json`, `sketch.html`) are git-ignored.

```
python sketch/fact-ledger/build.py
python sketch/fact-ledger/precheck.py                      # the four test sentences
python sketch/fact-ledger/precheck.py "your sentence here"
python sketch/fact-ledger/make_page.py                     # then open sketch/fact-ledger/sketch.html
```

Needs only `pyyaml` (already in `scripts/requirements.txt`).

## What the build finds (7 October 2026)

- 268 check rows in the six reports; 37 facts; 0 broken references.
- 15 figures repeated across two reports, all in agreement (found by text alone).
- 3 flags under the consistency rule:
  - **open:** Malta's territorial total for 2024 is 2,170 kt in the inventory (`env_air_gge`; CC-003, CC-026, CC-031)
    and 2,198 kt in the bridging table (`env_ac_aibrid_r2`; CC-114). The bridging line also differs in 2013 (2,835 vs
    2,826 kt); its 2024 values are Eurostat estimates (flag i). Not explained in either report.
  - **explained:** air transport 68% (CC-026, all resident emissions incl. households) vs 71.8% (CC-114, industries only).
  - **revision:** the published intensity change +16.6% (January 2026 release, quoted by the PN) vs +14.3% (August 2026 data).
- 3 claim pairs share a fact but are not in `data/edges.csv`: CC-026–CC-114 (air transport), CC-026–CC-031 (2024
  inventory total), CC-031–CC-109 (road transport).

The four sentences in `precheck.py` were written for the test; nobody said them.

## Benchmark (`bench/`)

Laptop-sized machine (4 CPU cores, 15 GB RAM, no GPU). Answer keys from the repository: A, `data/edges.csv` links
between claims; B, the hand links from sub-claims to facts above; C, the 6 manifesto rows with Maltese wording
(matched to their own English summary among 625) and CC-114's Maltese press-release title (matched among all claims).
Small samples (76 claims, 23 sub-claims, 7 Maltese passages): read the results as directions.

| Method | A: related claims in top 5 | A: MRR | B: right facts in top 5 | C: Maltese → English rank (1 = best) | Speed (rows/s) |
|---|---|---|---|---|---|
| TF-IDF (as `scripts/similarity.py`) | 52% | 0.47 | 56% (59% with number matching) | 6, 1, 2, 1, 1, 3, 2 | ~2,700 |
| model2vec potion-base-8M | 48% | 0.54 | 49% | 1 to 208 | ~24,000 |
| model2vec potion-multilingual-128M | 42% | 0.47 | 43% | 1 to 229 | ~14,500 |
| bge-small-en-v1.5 | 53% | 0.59 | 52% | 2 to 84 | ~65 |
| paraphrase-multilingual-MiniLM-L12 | 49% | 0.58 | 46% | 1 to 214 | ~63 |
| TF-IDF + bge-small (z-scored sum, `hybrid.py`) | 59% | 0.58 | 59% | – | – |

Readings: small embedding models do not beat word matching on this corpus (numbers, place names, technical terms);
a hybrid adds about 7 points; text alone finds only about 55–60% of the right facts, the rest needs the ledger's
structured keys and number matching; Maltese is weak in small multilingual models (XLM-R, their usual base, left
Maltese out), so match on the English translation and keep the Maltese original beside it.
`bench/results.json` holds the numbers of the single-method run.

```
python -m venv .venv && .venv/bin/pip install model2vec fastembed pyyaml   # models download on first run
.venv/bin/python sketch/fact-ledger/build.py && .venv/bin/python sketch/fact-ledger/bench/bench.py
.venv/bin/python sketch/fact-ledger/bench/hybrid.py
```

## Lessons for the design

1. A fact's key needs the measure, not only the series: without it the consistency rule flagged 14 false conflicts.
2. References must be checked by machine: 45 of the 57 references typed by hand first pointed at the wrong row.
3. Automatic fixes need a person: 8 of the 45 suggested corrections picked a row with the same number but another meaning.
4. The counting basis is the most useful node: it explains why a ministry, a newspaper and an opposition party can
   all be right about the same country's emissions.
5. About 6 facts and 9 links per report: roughly 350 facts and 530 links for 57 reports.
