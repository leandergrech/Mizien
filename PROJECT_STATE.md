# Project state (working notes)

Read this first when resuming work. It records decisions, conventions and what is outstanding, so a new session can
continue without re-deriving anything. Update it at the end of every work session.

*Last updated: 5 October 2026 (v1.1 corrections to 14 v1.0 checks, on branch `ccr-bd076c78-ydx75j`; CC-011 split requested; earlier: CC-051 v1.1: maps of all of Malta's reported waters, three reference areas and depth bands, on branch `ccr-bd076c78-ydx75j`; earlier: Miżien favicon added; homepage balance mark enlarged and given a slight tilt; CC-009 v1.0 merged into `main` at `77091be`; CC-010 v1.0 merged at `f638e15`; CC-002 evidence follow-up continues on `codex/cc-002-follow-up`; CC-007 v1.1 merged at `68025d0`).*

## What the project is

Miżien: an independent, science-first record of fact-checks on public claims in Malta (authorities, institutions,
parties, NGOs, opposition), focused on quality of life and the environment. Homepage is a 3D mind map of all claims
grouped by topic with links between them. The repository is public and doubles as the assistant's persistent storage.

## Repository

https://github.com/leandergrech/Mizien (public). Site: https://leandergrech.github.io/Mizien/ (GitHub Pages from
`main`, `/docs`). The repo URL is printed on the CC-001 report cover and flyer.

## Conventions

- **Name:** Miżien (with ż). Repo slug `mizien` because GitHub slugs are ASCII.
- **Claim IDs:** `CC-NNN` (three digits). One folder per claim under `claims/`, with `claim.yml` as the source of truth.
- **Verdict scale:** Supported, Largely supported, Not substantiated, Misleading, Contradicted. Confidence High, Moderate, Low.
- **Evidence grades:** A experiment, B observational, C review or guidance, D anecdote. Second-hand sources marked.
- **Pattern tags:** Selective metric, Input-as-outcome, Compliance-not-health, Conditional-turned-unconditional, Promise-without-baseline (provisional until a report is finished).
- **Right of reply** before wider circulation. Misleading or Contradicted only on evidence that can be shown.
- **Copyright:** paraphrase; quote the claim briefly; commit only open-access PDFs.
- **Language:** British English; Maltese names with correct spelling (Miżien, Għar Lapsi, Ħondoq, Magħtab, Għallis, Wirt Artna).
- **Report design:** A4, Liberation Serif body, Liberation Sans headings and tables. Palette: green #14452F, sage #7FA88B,
  amber #E3A72F, orange #D9772B (Not substantiated), red #B5483A, slate #2B3A42, cream #F6F4EE, pale green #E6EFE8.
  Report structure in `methodology/report-outline.md`. CC-001 generators in `tools/cc-001-report/`. From CC-003 on, the
  design lives in one shared module, `tools/mizien_report.py` (cover, body pages, meter, tables, contested-question
  blocks, flyer); each claim has `tools/cc-NNN-report/` with `calc.py`/analysis, `figures.py`, `build_report.py`,
  `build_flyer.py`. Outputs go to `out/` (git-ignored) and are copied to `claims/CC-NNN/`.
- **Numbers:** every figure in a report is recomputed by a script from data saved under `data/cc-NNN/` with the
  source query URL and retrieval date (`checks.csv` lists each check).
- **Spreadsheet:** `data/candidates.xlsx` is the tracker. `data/*.csv` are exports. After changing claim records run
  `python scripts/build_site_data.py`.

## Status

| ID | Status |
|---|---|
| CC-001 Upper Barrakka concrete | Report v1.1 and flyer done. Verdict: Not substantiated (plausible, not shown). Draft pending right of reply. |
| CC-002 Comino tree compensation | Report and flyer v1.1 drafted on `codex/cc-002-follow-up`. Verdict: Largely supported (moderate) for ERA's announced categories and conditions: 624 + 54 = 678; 92.04% non-protected; 54 × 10 = 540; a separate group of 348 is to be transplanted. The developer reports on-site nursery propagation since 2023, but publishes no stock or survival inventory. The full permit annex, 467/468 oleander discrepancy, transplant results and habitat recovery data remain unresolved. Science-only scope; no legal commentary. Right of reply not sought, at maintainer direction. |
| CC-003 Per-capita emissions vs 2030 | Report v1.0 and flyer drafted. **Verdict: Misleading (high).** CAA press release 13 Nov 2025 cites the -44% per-capita figure from the Commission's CAPR 2025 but omits its projection: effort-sharing emissions +41% in 2024, +30% to +42% by 2030 vs -19% target (largest gap in the EU). Half the per-capita fall is population growth. Pending right of reply; **must not be published before the reply deadline.** **v1.1 (5 Oct 2026, corrections):** flyer title says 'per person'; EU projection shown as −31% (WEM) / −38% (WAM); EU industry −36%; 'widest margin' qualified 'in percentage points' (Germany's gap is larger in tonnes); printed page numbers. |
| CC-004 Waste separation | Report v1.0 and flyer drafted. Verdict: Not substantiated (moderate). Separation up; recycling rate 16.7% (2024) vs 55% 2025 target; 79% landfilled; 412 million kg 'diverted' not reconcilable with Eurostat (271 kt). Pending right of reply. |
| CC-005 Bathing water | Styled report and flyer drafted in the shared CC-001 design. The Commission's exact 92% statement matches the EEA 2023 result (80/87); latest 2025 season is 88.5%. Balluta Bay closure and the CJEU wastewater-treatment case are contextual and do not refute the dated statistic. Draft verdict: Supported (high). Right of reply not sought, per maintainer direction. Viewer metadata uses the same Report / Flyer PDF / Flyer image actions as completed checks. **v1.1 (5 Oct 2026, corrections):** up/down boxes fixed; footer 'right of reply not sought'; 2023 samples 2,021 (EEA WISE); Balluta start 'late May 2024' (EHD report blocked; news says 21 vs 31 May). |
| CC-011 Ten minutes' walk to green space (was: Manifesto pledges) | Report v1.0 and flyer drafted. Verdict: Not substantiated (moderate) for both. Labour's pledge is "open or green" space (not "green space"): 99.9% already within reach on a broad reading, 55-68% for parks of at least 0.5 ha. PN's is a plan for a Net-Zero Gozo by 2040 with afforestation as one of several measures (news said "through afforestation"); no Gozo inventory; afforestation alone would need 1.5-8.5x Gozo's area. Pending right of reply. **v1.1 (5 Oct 2026, corrections):** flyer 'already almost met'; election source added (IFES), unsourced seat count removed. Split requested by the maintainer: CC-011 becomes the ten-minute park pledge; the PN net-zero Gozo pledge moves to its own claim. **v1.2 (5 Oct 2026):** split done: CC-011 now covers Labour's priority 19 only (title 'Ten minutes' walk to green space'); priority 18 (40% by 2030) kept as related sub-claim C, so the T7 edges stay. |
| CC-107 A net-zero Gozo by 2040 | Report v1.0 and flyer (5 Oct 2026), split from CC-011 at the maintainer's request. **Verdict: Not substantiated (moderate).** PN programme: a plan for a Net-Zero Gozo by 2040, no baseline, boundary or pathway. New: the 2023 Energy Baseline Scenario for Gozo (EU islands secretariat) gives energy CO2 118-154 kt a year (2016-20); afforestation alone would need 4.9-6.3x Gozo's area at the measured rate (1.5-8.5x wider range). First Gozo pin on the map (Victoria). No edges yet. Right of reply (PN) not sent. |
| CC-006 Spring hunting | Report and flyer v1.1 updated on `codex/cc-006-follow-up`. The report tests both Article 9 conditions. Quota-to-statutory-benchmark ratios are 99.3% for Quail and 59.8% for Turtle-dove. Draft verdict: Not substantiated (moderate): the statutory arithmetic is within the benchmark, but the 2026 enforcement outcome and ecological impact are not established. The 30 March 2026 Ornis minutes were not listed in the WBRU archive (checked 3 Oct); latest season outcome report listed was for 2025. Right of reply remains for the maintainer. |
| CC-007 Within EU limits vs WHO guideline | Report and flyer v1.1 merged into `main` at `68025d0`. PQ 29696 supplied by the maintainer; the Minister's answer is procedural, not a compliance claim. All 23 reported values are below the 25 µg/m³ EU limit and above the WHO 5 µg/m³ guideline. EEA validated files cross-check 11 station-years: ten match to 0.1 µg/m³; Attard 2024 differs (12.122 vs 11.9). Two St Paul's Bay values are n/a. Verdict: Largely supported (moderate), pending full series reconciliation. Right of reply remains with the maintainer. | **v1.2 (4 Oct 2026):** Newsbook read in full from Wayback (dated 18 Jul 2025), quoted verbatim, figures match the annex; confidence High. Codex's older uncommitted v1.0 copy in the main checkout is superseded.
| CC-008 | Transport | Report v1.0 and flyer merged into `main` at `6e1f342`. Verdict: Not substantiated (moderate). Marsa's 2021 travel-time and emissions percentages are agency-reported; the underlying survey/calculation was not found. Msida wording was prospective; the flyover entered use in December 2025 while the broader project continued. No local before/after noise series located. Pending maintainer right of reply. **v1.1 (5 Oct 2026, corrections):** the v1.0 'verbatim' Msida quote did not match the live IM page; now quotes the live page (Wayback capture 29 Oct 2024 not reachable from scripts; check in a browser). Marsa ambient air-quality wording noted; MaltaToday source dates added. |
| CC-009 Reverse osmosis and groundwater | Report and flyer v1.0 merged into `main` at `77091be`. WSC's 2025 report: 70.7% RO share; 11.5m m³ groundwater production, lowest decade. Chart values imply an 11.86% fall from 2024, while WSC prose says 11.4%. The latest RBMP reports two main aquifers poor quantitatively, 14 bodies poor chemically and 12/15 above the nitrate standard. Għar Lapsi Plant B was tendered, not commissioned. Verdict: Largely supported (moderate) for reduced WSC groundwater production; this is not proof of aquifer recovery. **v1.1 (5 Oct 2026, corrections):** Malta's 3rd-cycle EU (WISE) reporting lists 4 groundwater bodies poor quantitatively and 15/15 poor chemically, vs '2 and 14' in v1.0 (the 2 was our reading of the plan; 14 vs 15 is a real plan/WISE difference); both now shown. 'Lowest in a decade' attributed to WSC. |
| CC-010 Land & Trees | Report and flyer v1.0 drafted on `codex/cc-010-trees`. Project Green reported >8,000 trees and >25,000 shrubs planted in 2024. Labour pledge 305: 100,000 trees in the next five years (PDF p. 91; printed p. 89). A February 2026 parliamentary answer reports around 60,000 trees and >100,000 shrubs planted collectively by government entities through end-2025. Verdict: Largely supported (moderate) for the reported figures and pledge; the pledge window had not elapsed, and survival/canopy outcomes are unknown. Right of reply remains with the maintainer. **v1.1 (5 Oct 2026, corrections):** pledge reframed: the 30 May 2026 snap election (IFES) ended the legislature; ~75% of the five-year window had elapsed by end-2025 vs ~60% of trees; Labour 2026 manifesto counts >57,000 trees 2022–25; Project Green vouchers 23,000 (not trees planted). Verdict unchanged; maintainer to decide whether to split it. |
| CC-012 to CC-021 | Candidates added 3 Oct 2026 (records, sources, literature folders, map links). CC-012 Ta' Qali gravel and grass (both sides); CC-013 Buttigieg: permits keep prices in check; CC-014 Buttigieg: fewer enforcement notices (**In progress**: article blocked by egress on 3 Oct, wording unverified, no report; see `literature/CC-014/README.md`); CC-015 Buttigieg: 'three weeks left' (date check only; scope to confirm); CC-016 shore-to-ship 90%; CC-017 land reclamation (Budget 2026); CC-018 MDA on IMF; CC-019 Amphora: 830,000 m2 land lost; CC-020 noise compliance; CC-021 Gozo tunnel (lead only, weakest). Only CC-013, CC-014 and CC-018 have verbatim wording; the rest need primary sources. New topics Planning & Housing and Noise; new themes T8 (planning, housing and land take) and T9 (compliance-not-health). No NGO claim among them yet. |
| CC-012 Ta' Qali gravel | Report v1.0 and flyer drafted (3 Oct 2026, branch `claude/cc-012-taqali`). **Verdict: Contradicted (high)** for the government assurance that grass would regrow through the gravel (Ministry statement Sept 2025; Micallef). Sentinel-2 2023-2026 (tools/cc-012-report/fetch_s2.py): gravel zone ~2.8 ha found from summer brightening inside the OSM park polygon; greened every winter before (winter median NDVI 0.37-0.47), bare in winter 2025-26 (0.11) while the rest of the park greened; still bare with gravel on 27 Sep 2026. PN/Momentum current-state claim supported; 'permanently' not shown. Rerun fetch_s2.py to update after any works. **v1.1 (5 Oct 2026, corrections):** fetch_s2.py now applies the Sentinel-2 BOA_ADD_OFFSET (−1000, baseline ≥ 04.00). Winter NDVI zone 0.53–0.67 before the gravel vs park 0.65–0.68; 0.15 vs 0.68 in winter 2025–26 (v1.0: 0.37–0.47, 0.11, 0.38). Three pre-gravel winters; unsourced concert date removed; zone 2.76 ha (about a quarter larger than Momentum's 2.2 ha). |
| CC-013 Permits and prices | Report v1.0 and flyer drafted (3 Oct 2026, branch `claude/cc-013-permits-prices`). **Verdict: Largely supported (moderate).** Interview read in full (MaltaToday, 2 Mar 2025); 91,000 is the interviewer's figure (PA: 87,814 approved 2015-24). Research supports direction (Glaeser, Hilber, Saiz) but effect size is uncertain (Anenberg and Kung). Malta pop +31% vs EU +2%; real prices +34% vs +25%; overburden 1.1% -> 6.0% (EU 7.7%); overcrowding 4.7% vs 16.8%. **v1.1 (5 Oct 2026, corrections):** overburden series break at 2023 (Eurostat flag b): comparable runs 1.1→2.9% (2015–22) and 6.0/5.9/6.0% (2023–25), replacing '1.1%→6.0%, fivefold'; real prices +34% (p) / +25% now in checks.csv. |
| CC-020 EP noise study | Report v1.0 and flyer drafted (5 Oct 2026, branch `claude/cc-020-ep-noise-study-20261005`, worker C). **Verdict: Largely supported (moderate).** Study read in full (PDF from op.europa.eu download-handler, not committed). Conclusion follows from its evidence; END has only reporting thresholds (55/50 dB, above WHO 53/45 road) and excludes construction/entertainment noise. Eurostat ilc_mddw01: Malta 31.3% report street/neighbour noise (2023), highest in EU (EU 18.1%). **Unverified:** Maltese regulation vs Directive, Commission infringement register, 21% vs 9% survey (ERA annex 403; EU28 source unknown), WHO/EEA figures second-hand. No tag applied (study does not itself commit the Compliance-not-health pattern); T9 membership left as is. |
| CC-026 EU's largest rise in emissions | Report v1.0 and flyer drafted (5 Oct 2026, worker B). **Verdict: Largely supported (high).** Newsbook (18 Jun 2026) read in full; Eurostat release ddn-20260616-2 gives +169.4% (database now +169.7%). 98.6% of the 2015-2024 rise is air transport under Eurostat's residence principle; territorial UNFCCC inventory +1.6%. Central Bank of Malta report not read (second-hand). Right of reply not sent. |
| CC-014 Enforcement notices | Report v1.0 and flyer drafted (3 Oct 2026, branch `claude/cc-014-enforcement`). **Verdict: Misleading (moderate).** Interview wording read in full (Malta Independent, 7 Sep 2025). Notices: 1,033 a year 2001-09 (MEPA reports) vs 187 in 2020-24; complaints fell only 11% since 2009 (2,701 to 2,411); ~half of 2024 complaints confirmed illegal; 521 sanctioning applications and 482 removals vs 162 notices. PA's own 2024 report credits persuasion. Gaps: 2008, 2012-2018 (scanned/Issuu reports); 2019-23 second-hand. **v1.1 (5 Oct 2026, corrections):** 2019 complaints 3,134 (PA AR 2019 via Issuu, was 3,174); 'about six times' (1,003 vs 162); 2020 not the series high (FY 2004/05: 3,705); 2024 confirmed cases ~1,200–1,250 (PA categories sum to 1,252); flyer 'applications to legalise'. |
| CC-016 Shore-to-ship | Report v1.0 and flyer drafted (3 Oct 2026, branch `cc-016-shore-to-ship`). **Verdict: Misleading (moderate).** Infrastructure Malta page (1 Dec 2023) read in full: "promises to slash 90% of air pollution in the Grand Harbour". Connection voluntary until 2030 (FuelEU Art. 6). Transport Malta FOI records via Amphora Media (second-hand): 67 of 373 berths plugged in Jul 2024-Jul 2025, 9% of berth time; calls 357 -> 385 (2024-25). 90% plausible per connected ship (hotelling >90% of CO2). Gaps: FOI reply itself, ERA Senglea study, basis of 90%. **v1.1 (5 Oct 2026, corrections):** the 90% has a published basis: IM (30 Nov 2020, 19 Feb 2022) scoped it to cruise liners and Ro-Ros that connect (NO2 −93%, PM −92.6%, SO2 −99.6%, CO2 −39.6%); the 2023 page dropped the scope. Costs vary (€33m, €37m, €49.9m). |
| CC-017 Land reclamation | Report v1.0 and flyer drafted (3 Oct 2026, branch `cc-017-reclamation`). **Verdict: Not substantiated (moderate).** Budget Speech 2026 pp. 52-53 read in a browser (verbatim). Sentinel-2: +3.7 ha at Freeport Terminal 2 2023-26 (stated 30,000 m2), so the 'already under way' part holds. No site/size/screening/call for the large project found by 3 Oct 2026; ERA seabed study unpublished since 2019; three Natura 2000 sites ~1 km away. Gap: Posidonia maps for Marsaxlokk Bay. **v1.1 (5 Oct 2026, corrections):** nearest Natura 2000 site (SPA MT0000111) is 0.40 km from the new land at Terminal 2, not 1 km; 'possible and environmentally safe' is the 2019 Environment Minister's wording ('least environmental damage' was MaltaToday's paraphrase); two of the three designations overlap on the same cliffs. |
| CC-018 IMF and the MDA | Report v1.0 and flyer drafted (4 Oct 2026, branch `cc-018-imf-mda`). **Verdict: Largely supported (moderate).** IMF CR 26/29 read in full (PDF supplied by maintainer): prices 'aligned with fundamentals', ratios stable, weakening unlikely; but bank exposure 72% of private loans 'a vulnerability'. Eurostat tipsho60: Malta price-to-income -10.7% 2015-24, below long-term average. MDA wording via MaltaToday (own release not found). **v1.1 (5 Oct 2026, corrections):** MDA release found (mda.com.mt, 8 Feb 2026, modified 17 Jun 2026); it omits the IMF's 'vulnerability' point. Flyer quotes the IMF ('stable'); incomes grew faster than prices; overburden series break as in CC-013. Confidence could rise to High (maintainer). |
| CC-019 Green to Grey | Report v1.0 and flyer drafted (4 Oct 2026, branch `cc-019-green-to-grey`). **Verdict: Largely supported (moderate).** Amphora articles read (print copies supplied). Independent IO/Esri 10 m land cover: 1.4 km2 net consistent new built-up 2018-23 (3-year rule), so 0.83 km2 is plausible and conservative; previous cover 65% crops / 31% rangeland, so '95% farmland' not reproduced. EEA chart (2012-18): ~0.92 km2, Malta highest land take of EEA39. **v1.1 (5 Oct 2026, corrections):** independent-estimate windows relabelled (3-year rule catches land first built in the 2020–21 maps; 2-year rule 2019–22); Comino 'a quarter to 0.3' (island area source-dependent); 24 km² gross vs 18.9 km² net; year-to-year swings 3–27 km². |
| CC-012 to CC-014 | Checked locally on 3 Oct 2026 (above). First automated runs (3 Oct 2026) were blocked: the cloud environment's network allowlist refused every source host (Maltese news, gov and party sites, Wayback, Crossref, Eurostat). Status reset to Not started; leads kept in `data/sources.csv` and `literature/CC-0NN/README.md`; blocker recorded in `data/queue.csv`. |
| CC-022 Electricity burden | Report v1.0 and flyer drafted (4 Oct 2026, branch `cc-022-electricity-burden`). **Verdict: Largely supported (high).** Gov PR read in full (browser). Eurostat confirms all figures (MT lowest in PPS, 3rd nominal). Missing context: energy subsidies ~EUR 1.0bn 2022-25 (IMF). **v1.1 (5 Oct 2026, corrections):** 'lowest' qualified to the typical household band (2,500–4,999 kWh); other bands: 2nd, 3rd, 16th, 23rd of 27; 4th of 26 all-band. 2014 tariff cut sourced (Eurostat); the IMF ~€1bn covers electricity and fuel, 2025 projected. |
| CC-051 Marine protection | Report v1.0 and flyer drafted (4 Oct 2026, branch `cc-051-marine-protection`); **v1.1** (4 Oct 2026, branch `ccr-bd076c78-ydx75j`) adds three maps (all waters reported to the EU; the same protected sea against FMZ / EEZ / EU basis; depth bands) and a sharper summary. **Verdict: Misleading (moderate), unchanged.** EEA union of 18 marine sites = 4,137.5 km2: 36% of FMZ, 7.8% of EEZ, 5.5% of EU-reported waters. All of it lies within 25 nm; ~64,000 km2 (85%) of the reported waters beyond 25 nm has no protected site; whole FMZ = 15.2% of the reported waters; deep sea >1,000 m = 26% of the waters, 0.6% protected. Boundaries in `data/cc-051/boundaries.geojson` (FMZ rebuilt from Marine Regions 12 NM + 13 nm = 11,492 km2 vs official 11,480; EU-reported outline is the EEA's simplified web version, 75,484 km2). Note: ~183 km2 of protected sea is internal waters, which the official FMZ excludes, so like-for-like the FMZ share is 34-35% (ERA's 'more than 35%' is borderline; kept Supported). ERA qualifies (FMZ); minister's 'maritime zone' does not (quote via Amphora). Right of reply not yet sent. |

## Automation (3 October 2026)

Nightly checker routines A, B and C (Sonnet 5.5) take claims from `data/queue.csv`; a weekly intake routine adds ten
candidates, rebalances topics/subtopics and proposes patterns and themes. Conventions: `methodology/automation.md`.
Pattern tags are now read by the validator from `methodology/pattern-tags.md`; claims may carry an optional
`subtopic`; new topics and themes get colours automatically.

Pipeline hardening (3 October 2026, after the first runs): every run starts with `python scripts/net_check.py`
(and `net_check.py CC-NNN` per claim). If the network proxy refuses the core research hosts, the run changes
nothing and reports; if it refuses a claim's source hosts, the claim stays `Not started`, the attempt and blocker
go in `data/queue.csv`, and the worker tries its next claim. After 3 blocked attempts the blocker reads
`needs maintainer`: supply the verbatim passages in `literature/CC-NNN/primary-source.md` (as for CC-007) and
clear the Blocker cell. Workers merge `origin/main` into their branch instead of rebasing (no force-pushes).

## Site build (4 October 2026)

- **Right of reply only where a check goes against a claim** (maintainer decision, 5 October 2026): sought for
  *Not substantiated*, *Misleading* and *Contradicted* (pledges: *Not measurable*, *Off track*, *Missed*); a check that
  supports a claim needs none, and `right_of_reply.sought: false` records a decision not to seek one. The site shows
  each check's reply state (pending, not needed, not sought, sent, received); the validator requires a sent date to
  publish only where a reply is needed. Public wording updated (homepage, footer, disclaimer, verdict process, feed,
  README, standards.md).

- **Parts of a claim and pledge labels** (5 October 2026, maintainer decisions).
  - Sub-claims are numbered parent + letter (CC-017A, B...) and recorded in claim.yml as `subclaims:` (wording,
    finding, rating and the colour of the report's rating chip). Backfilled from the 15 reports with a sub-claim
    table. They share their claim's page (a "Parts of this claim" section, anchors `#CC-017A`), are linked wherever
    their number is mentioned, have their own hover card, and appear in the Għanqbuta view as small satellites of
    their claim (selectable: `?sel=part:CC-017C`). They are not claims of their own: no groups, links or pages.
  - Pledges get a label instead of a verdict (the Pledges section of `methodology/verdict-scale.md`, written by the ccr session): Not measurable, Not yet due, On
    track, Off track, Met, Missed, each with an as-of date, in a `pledge:` block (status, as_of, made_by, made_on,
    vehicle, deadline, target; optional term_end, occasion, overlaps). A pure pledge has no verdict and shows only
    its label; a mixed check shows both. The validator checks the block (Missed only after the deadline or term and
    with evidence_shown; Not yet due only before the deadline). Claim pages have a pledge box; `/pledges/` lists the
    labels, every pledge and overlapping pledges; the map has a **Pledges** grouping (who, when, what, gold lines
    between overlapping pledges), shown once a pledge exists. The ccr-bd076c78-ydx75j session adds the blocks for
    CC-010 (Off track; verdict kept), CC-011 and CC-107 (Not measurable; verdicts removed).

- **Stance timelines and patterns by kind of body** (5 October 2026).
  - Every claim page has a Timeline: the statement, sources as published (`data/sources.csv` dates; access dates are
    ignored), each step of the check from its research log, right of reply, the evidence review due a year after the
    last review, and earlier or later statements by the same body on the same topic.
  - **Research log** (maintainer decision, 5 October 2026: dates are when the research was done, independent of
    site versions): `history:` in claim.yml, oldest first, with steps added, started, wording, version (number and
    note), reply-sent, reply-received, published, correction, clarification and note. Backfilled for the 22
    researched claims from their reports' revision logs, or from the version and date on the report cover where there
    is no log (CC-002, 005, 006, 008, 009, 010; CC-006's version 1.0 is undated, so only 1.1 is listed). Intake dates
    come from `data/queue.csv`. Git dates are not used. `validate_claims.py` fails when a `version` has no entry.
  - **Corrections page** `/corrections/` (the Corrections tab): corrections and clarifications, then every version
    of every check, all dated by research. Corrections also show at the top of the check and in the feeds.
  - Optional `timeline:` events in claim.yml (date, kind, text, url) record later statements, new data, replies and
    corrections that are not claims of their own. `validate_claims.py` checks them.
  - Body pages: "Statements over time" (a row per topic, dots coloured by verdict, a dashed ring when only the year
    is known), the topics a body returned to in date order, and an Atom feed (`/bodies/<id>/feed.xml`; site-wide
    `/feed.xml`) of new claims, verdicts, report versions and replies.
  - `/bodies/patterns/`: claims, pattern tags, verdicts and topics by kind of body, sentences on where each tag
    turns up (only from 3 tagged claims, "most" from 60%), and issues over time (each theme's claims by date,
    coloured by kind of body). Never by person or party; counts, not ratings.
  - Map: a "When said" grouping (one group per year of the statement).
  - CC-007, source 6 (CDE News): its headline says "Saturday 19 July 2023" but the page was published on 19 July
    2025 (page metadata, checked 5 October 2026). Our record had the right date; a note now says the year in the
    headline is the publisher's. Logged as a clarification.
- **Who said it, connections and claim mentions.**
  - `data/bodies.csv` is the register of bodies and people: 63 organisations and 14 people, with kind, type, parent
    office, role and the exact speaker wording as aliases. Claims are matched by speaker text (`scripts/bodies.py`),
    or by an optional `bodies: [id, ...]` in claim.yml. `validate_claims.py` fails on register errors and warns on
    unmatched speakers: add the wording to `Aliases` rather than guessing.
  - `scripts/connections.py` works out second- and third-degree connections (shortest routes through
    `edges.csv`), theme bridges (claims in two themes), and each body's claims (its own and its people's and
    offices') and linked bodies (named in the same claim, or claims sharing a theme; counted per office).
  - Pages: `/bodies/` and `/bodies/<id>/` (a record, not a score: no ratings), a Connections section on every claim
    page, and `/methodology/connections/`. The map's "Who said it" grouping is a constellation: kind of body >
    body > person, with lines between linked bodies; `?sel=body:<id>`.
  - Every CC-NNN in page text is linked by a build transform (`eleventy.config.js`); `site/assets/claimrefs.js`
    shows a summary and verdict on a long hover or keyboard focus, from `/data/claim-briefs.json`.

- Each claim page shows the full report as HTML, then download buttons (report PDF, flyer PDF, flyer image) and a
  flyer preview. `tools/report_html.py` builds the HTML from each `build_report.py` story, with figures taken from
  the committed `report.pdf`, and checks that the PDF's words are all present. CI (and `npm run build`) regenerate
  it; `claims/*/report.html` and `report-figures/` are git-ignored. Fixed the map viewer showing a blank frame
  instead of the flyer image.

- The site is being moved to a static build: Eleventy 3 on Node 24, with `eleventy.config.js`, `package.json` and
  templates in `site/`. CI (`.github/workflows/site.yml`) validates claims, rebuilds data and builds `_site/` on
  every PR.
- During the transition, `docs/` is copied through unchanged, so the build matches what Pages serves today. Pages
  then move into `site/` one PR at a time.
- One maintainer-led session owns `docs/index.html`, `site/`, `scripts/build_site_data.py`,
  `scripts/validate_claims.py` and `.github/`. Other sessions: change these only after checking with it, and keep
  committing `build_site_data.py` outputs as before until the rules change.
- Maintainer decisions are recorded in `PLAN.md`, kept local for now on the `claude/mvp-plan` branch of this machine's
  clone:
  - Claim pages live at `/claims/CC-NNN/`.
  - Drafts stay `noindex` until a disclaimer and a visual verdict-process page are approved.
  - The deploy moves to GitHub Actions.
  - The network view is renamed "Għanqbuta" (spider; `?view=ghanqbuta`, with `?view=network` kept as an alias) and gets subtopic sub-hubs.

## Map view prototype (3 October 2026)

- `docs/index.html` has a **Network / Malta map** toggle (also `?view=map`, key M). Network view: larger default
  scale, right-drag / Shift-drag / two-finger pan, zoom towards the cursor or pinch point, double-click to zoom,
  arrow keys, +/-, 0 = Fit.
- Map view: stylised islands from OpenStreetMap (`scripts/build_geo.py` -> `docs/data/geo.json`, ODbL). Claims are
  pins at `location` (new optional field in claim.yml: place, lat, lon, scope = site | institution | national;
  validated). National claims sit at the institution (Castille, Parliament, City Gate, PA in Floriana).
- Districts: Valletta & Floriana opens into a street-level view (click the badge or zoom in); claims elsewhere are
  parked on an "Elsewhere in Malta" ring so links stay visible: one slot per site near its true bearing, slots
  kept apart, a site's claims stacked outwards. Every district has its own streets, walls (OSM city_wall / fort) and
  landmarks in geo.json (`bbox` per district in build_geo.py). Gozo (Victoria & the Ċittadella) unlocked at 15
  checks (16 on 3 Oct 2026; no Gozo claim yet); Grand Harbour & the Three Cities is built and unlocks at 20. Locked
  teasers hang below their circle so they do not cover open badges (Grand Harbour overlaps Valletta).
- Gamification: map layers unlock with completed checks (TIERS in index.html: 0 islands, 3 names/compass, 5 depth
  lines, 7 site names, 9 Valletta district, 12 streets, 15 Gozo district, 20 Grand Harbour, 30 living sea). A HUD
  shows level and the next unlock; a toast announces new layers since the visitor's last visit.
- Lens: a fisheye focus at the centre of the stage (Lens button, key L; on by default on phones in the map view,
  remembered in localStorage `mizien.lens`). Magnifies up to 3.2x at the centre, compresses the rim; drag the map
  under it. The scale bar hides while it is on.
- Transitions (district in/out, Fit) fold the camera zoom and pan into the map scale and centre, then animate the
  scale in log space about the fixed screen point (no jumps). The map view is orthographic so the fold is exact.
- Landmark medallions: every claim site has a line-art emblem (claim.yml location.icon; PLACE_ICONS in index.html).
  A site is 'discovered' (gold emblem) once any claim there has a verdict, otherwise a dashed '?'. Click opens a
  panel of its claims; the HUD counts sites discovered. Medallions are spread apart with leaders to their true spot.
- To do: a Gozo claim for the Gozo district (none yet; CC-021 Ċirkewwa is on the Malta side); test on phones; new
  claims must get a `location` (intake routine updated). geo.json is 226 KB with Grand Harbour streets included.

## Outstanding

- [ ] **v1.1 corrections (5 Oct 2026), maintainer decisions:** CC-010 split the verdict (counts supported; pledge
  delivery not substantiated)?; CC-018 raise confidence to High (MDA wording now primary)?; CC-022 is sub-claim A
  'Supported' too generous given other consumption bands?; CC-016 sub-claim A (IM's per-ship figures, study not
  cited); CC-019 confidence if the low IO/Amphora spatial overlap is confirmed; CC-009 footer says 'pending right of
  reply' but the body says not sought.
- [ ] **v1.1 corrections, browser checks:** Wayback 29 Oct 2024 capture of the IM Msida Creek page (CC-008); MaltaToday
  dates (CC-008, CC-017); EHD Balluta report start date (CC-005); ERA RBMP Chapter 6 groundwater tables and cover date
  (CC-009); PA 2024 annual report outcome categories (CC-014); an official Comino area (CC-019).
- [ ] Rebuild CC-004, CC-020 and CC-026 to pick up the ◆ fix in reference lists (empty box before 5 Oct 2026).
- [ ] `data/claims.csv`: the CC-002 row has misaligned columns (an unquoted comma); fix when CC-002's v1.1 branch merges.
- [ ] Upgrades proposed by the 4 Oct review (not yet done): CC-014 PA reports 2017–23 as primary series; CC-005 time
  series and site map; CC-017 bay map (seagrass, depth); CC-019 Amphora polygon cross-check; CC-004 Commission
  documents; CC-003 ranking and target-path charts; CC-022 band chart; CC-009 abstraction data; CC-018 new MDA
  sub-claims; CC-008 Msida NO2 series; CC-011 Gozo energy baseline.

- [ ] Decide author or affiliation line for reports and flyer (none yet).
- [ ] Add the Times of Malta article URL to `data/sources.csv` and `claims/CC-001/claim.yml`.
- [x] Run `python scripts/archive_sources.py` to fill `archive/manifest.csv` (committed on branch `archive-manifest`).
- [ ] Archive by hand the 27 robots-disallowed sources in `archive/manifest.csv` (gov.mt, ERA, NSO, MaltaToday,
  Newsbook, Italpress, arja.mt, Independent, Chambers). gov.mt sites (climateaction, publicservice, DOI) block
  automated access with Cloudflare; read them in a browser.
- [ ] Add the new CC-003/004/011 primary sources to the archive (CAA press release, PR260072en, PL manifesto PDF,
  PN programme pages). The PL manifesto SHA-256 is recorded in `literature/CC-011/references.bib`.
- [ ] Send right-of-reply drafts: CC-003 to the Climate Action Authority and Environment Ministry; CC-004 to the
  Environment Ministry and WasteServ; CC-011 to the Partit Laburista (and the Government) and the Partit
  Nazzjonalista. Record dates and deadlines in each `claim.yml`. Each report lists the questions to ask.
- [ ] Decide whether the site should show verdicts for drafts before the reply deadline (it currently does, e.g.
  "Misleading (Drafted)" for CC-003 once merged).
- [ ] `data/candidates.xlsx` is behind the CSVs for CC-003, CC-004, CC-011 (sources, edges, theme T7, quick check).
  It was not edited because openpyxl drops its drawings; update it by hand or treat the CSVs as the master.
- [ ] Decide whether the verdict scale needs a rule for pledges (CC-011 used Not substantiated = not measurable as worded).
- [ ] CC-003: obtain the CAA "Facts: emissions (June 2026)" factsheet (blocked).
- [ ] CC-004: verify COM(2023) 304 early-warning report directly (cited second-hand).
- [ ] Send CC-001 draft to Ambjent Malta and Fondazzjoni Wirt Artna; record dates in `claims/CC-001/claim.yml`.
- [ ] CC-006: obtain the 30 March 2026 Ornis Committee minutes or other primary vote record; monitor for the 2026 WBRU season outcome report; obtain final 2019–2024 Article 12 data, and FKNK survey methods/results. The official WBRU minutes and outcomes pages were checked on 3 Oct: neither the 2026 minutes nor 2026 season outcome report is listed. Right of reply remains for the maintainer.
- [ ] CC-007: reconcile the Attard 2024 difference between the PQ annex (11.9) and EEA mean of valid daily aggregates (12.122); obtain ERA's validated annual series and coverage/quality notes. The EEA files retrieved do not supply 14/25 station-years, including the two St Paul's Bay n/a cells. The Newsbook page was not retrievable for full-text review; an archived snapshot is recorded. Right of reply is for the maintainer.
- [x] CC-008: locate primary wording for Msida and Marsa; draft report/flyer and add evidence notes. Remaining: obtain the Marsa surveys/calculations and comparable local traffic, air and noise series; right of reply remains for the maintainer. Four earlier MaltaToday sources plus the OPM and Times of Malta pages are robots-disallowed and need browser archiving; ERA's source page also blocks automated access. The AEA publisher returned HTTP 403 to the archiver.
- [x] CC-005: locate Commission wording; compare EEA bathing-water seasons 2023–2025; confirm Balluta Bay warning from the EHD primary report; distinguish CJEU wastewater ruling from bathing-water classification.
- [x] CC-005: add sources to `archive/manifest.csv`. Commission page and CJEU judgment have archived snapshots; EEA 2025 is fetched and hashed. EEA 2024 and the EHD Balluta report are robots-disallowed with no snapshot; archive manually if needed. News leads are robots-disallowed but existing snapshots are recorded.
- [ ] CC-005: review drafted verdict, styled report and flyer; reply process remains for maintainer.
- [ ] Obtain open-access full text for the CC-001 A and B studies; fill gaps noted in `literature/CC-001/notes.md`.
- [ ] CC-009: reconcile WSC's 11.4% narrative with the 11.86% chart-derived change if the underlying workbook is obtainable; follow the Għar Lapsi procurement through award and commissioning. Future aquifer recovery requires comparable body-level abstraction, recharge, water-level, salinity and nitrate data. Right of reply remains for the maintainer.
- [x] CC-010: verify manifesto pledge wording, 2024 Project Green counts and end-2025 parliamentary count; calculate the approximate interim proportion; add evidence notes, report, flyer and source records. Two Mediterranean studies provide context only, not a Maltese survival rate.
- [ ] CC-010: obtain the tree-only project register, pledge scope and post-2025 count; follow pledge deadline in 2027; seek cohort survival, replacements and maintenance records. The manifesto PDF is hosted by Talk.mt; no copy was committed. Archive manifest marks this, Ambjent Malta's annual report, the parliamentary PDF and one secondary lead robots-disallowed.
- [ ] Verify and fix `literature/CC-001/references.bib` (first task 2 in CLAUDE.md; not done this session).
- [ ] Check the name and a domain are free; enable GitHub Pages (main, /docs).
- [ ] CC-002: obtain the full permit annex/species schedule and follow-up transplant-survival and habitat-monitoring data if publicly available. Keep all analysis to science; do not comment on the tribunal. The 3 October automated archive attempt hit DNS resolution failures for the two direct ERA releases and most other new sources; do not label these failures robots-disallowed. The older generic ERA press-releases entry is robots-disallowed. Archive direct pages manually when available.

- **Foreign and EU claims about Malta (maintainer, 4 Oct 2026):** claims made about Malta by EU institutions,
  international bodies and foreign speakers are checked like local ones; the intake was skewed towards local
  speakers and now aims for at least 2 of every 10 new claims from them. CC-020 is the first: its claimant is now
  the Feb 2026 study for the EP Petitions Committee (Hjerp and Coffey, Ecocentric; doi:10.2861/6278624), with
  verbatim passages in `literature/CC-020/primary-source.md`. Unblocked for worker C.
- **Claims waiting on the maintainer** show as `In progress` (queue Blocker `source:` or `needs maintainer`); see
  `methodology/automation.md`. There is no cap on the number of claims.

## How to resume a session

1. Clone the repository (it is public) and read this file, `README.md` and `data/claims.csv`.
2. Pick the next claim from the table above; open its `claim.yml`.
3. Collect literature into `literature/CC-NNN/`, then build the report from `methodology/report-outline.md`.
4. Work on a branch per claim and open a pull request for the maintainer.

## Branches (3 October 2026)

`archive-manifest`, `cc-003-climate`, `cc-004-waste` and `cc-011-manifestos` have been merged into `main` (PRs #1–4).
CC-005 outputs and viewer metadata were merged and pushed to `main` (merge commit `2110846`). CC-006's report, flyer and site metadata are integrated on `main` at `e0552b9` (fast-forward from `codex/cc-006-spring-hunting`). CC-008 was fast-forwarded and pushed to `main` at `6e1f342`. CC-002's report, flyer, viewer metadata and evidence notes were merged from `codex/cc-002-comino` at `ade9e4b`; v1.1 follow-up is pushed on `codex/cc-002-follow-up` at `bc5b516`, with the permit annex and ecological outcome gaps still unresolved. CC-007 v1.1 with EEA cross-check and session notes was merged into `main` at `68025d0`; the Attard 2024 difference and 14 missing EEA station-years remain unresolved. CC-009 v1.0 was merged into `main` at `77091be`. CC-010 report and flyer v1.0 were merged into `main` at `f638e15`; right of reply and the final pledge-period count remain with the maintainer.

## Notes for the next session

- The homepage map uses the Botanical style and circular balance wordmark. Its mobile layout has larger touch targets, direct zoom buttons and two-finger pinch, a slide-up map key, and a bottom-sheet claim panel; labels simplify at phone widths and the claims table hides its topic column. The enlarged balance mark is slightly tilted; `docs/favicon.svg` carries the same mark in browser tabs. `last_reviewed` dates anchor one leaf per completed evidence review; leaves move from green to brown over 365 days. Update the date after a fresh evidence review and rebuild site data.
- CC-002 editable draft: `claims/CC-002/report.md`; generated outputs: `report.pdf`, `flyer.pdf`, `flyer.png`. Do not treat the 10:1 planting condition as measured ecological equivalence or use cross-study findings as a Comino survival rate. The one-specimen oleander discrepancy remains unresolved.
- CC-008 editable draft: `claims/CC-008/report.md`; generated outputs: `claims/CC-008/report.pdf`, `flyer.pdf`, `flyer.png`. Do not present Marsa's percentages as independently reproduced. No survey file was located. Msida's PDS observations are from 2019 and are not a post-opening counterfactual. The national licensed-fleet figure in the original candidate is not a junction traffic measure and was not used.
- `archive/manifest.csv` records CC-008 source-fetch results. Manual browser archiving is still needed for the four earlier MaltaToday sources, the Office of the Prime Minister and Times of Malta; ERA blocks automated access and the AEA publisher returned HTTP 403. The three Infrastructure Malta pages were fetched and have Wayback snapshots.
- CC-002 direct ERA release URLs and most newly added sources remain unarchived because the archive script encountered temporary DNS resolution failures on 3 October 2026. The existing generic ERA press-releases URL is marked robots-disallowed. Do not describe the new URL failures as robots restrictions.
- CC-007 editable source transcription: `literature/CC-007/primary-source.md`; generated outputs: `claims/CC-007/report.pdf`, `flyer.pdf`, `flyer.png`. EEA validated-data comparison files and hashes are in `data/cc-007/`. The EEA daily mean for Attard 2024 is 12.122 µg/m³ versus 11.9 in the PQ annex; do not silently reconcile the difference. EEA files retrieved do not cover 14 of 25 possible station-years.

- Eurostat API (`ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/...`) works from scripts; see
  `tools/cc-003-report/calc.py` and the helper pattern in the CC-003/004 data files.
- WorldPop and Overpass work from scripts (send a User-Agent to Overpass or it returns 406).
- gov.mt, NSO and ERA pages can be read in a browser but not by scripts.
- Malta's population growth (+41% since 2005) distorts any per-capita metric; check that first in future claims.
- CC-003 and CC-011 are linked by theme T7: the CAA and Labour's manifesto both state a 40% cut by 2030 vs 2005
  with no scope. Worth a follow-up check.
- Claim files exposed by the site builder are copied into `docs/claim-files/`; the map panel offers an on-page viewer and adjacent download action for each output.
- Completed claim outputs share one `addFileAction` implementation. Use `report_pdf`, `flyer_pdf` and `flyer_png` in `claim.yml` for the standard Report / Flyer PDF / Flyer image viewer and download pairs.

## Intake of 4 October 2026 (CC-022 to CC-100)

- 79 candidate claims added from web searches, bringing the list to 100. All are `Not started`, wording `Paraphrase: locate quote`, one locator source each in `data/sources.csv`; nothing verified yet. Sides covered: government and agencies, PN, ADPD, Momentum, NGOs (BirdLife, Moviment Graffitti), business (MDA, MHRA, Malta Chamber), unions (GWU), media (Amphora, The Shift, Newsbook, Lovin Malta, Malta Business Weekly) and EU bodies (Commission, EEA).
- Two new topics: Tourism & Population, Health & Safety. Every claim now has a `subtopic` (2-5 per topic, names reused exactly; CC-020 Noise left null) for the planned sub-hubs in the Għanqbuta (formerly Network) view.
- Map places geocoded with OpenStreetMap Nominatim (4 Oct 2026); Sant'Antnin did not resolve and its claims use Magħtab or Marsaskala.
- 30 weak links (Weak (indicative) or Pattern, not causal) added to existing themes T2-T9 and a new theme T10 (tourism pressure).
- Queue: new claims spread across workers A/B/C (open loads 28/27/27). Several claims overlap earlier ones by design (CC-025/CC-094 with CC-003; CC-081 with CC-004; CC-041-043 with CC-005).
- Site and UI changes (Għanqbuta rename, subtopic sub-hubs, Eleventy build) are owned by the mizien-60 session; do not edit docs/index.html or scripts without checking with it.

## Weekly intake 2026-10-04 (CC-101 to CC-106)

Second intake of the day (the 79-claim bulk intake ran earlier). Six candidates added, not ten: searches turned up few specific, checkable, non-duplicate statements, and padding was avoided. All are `Not started`, verdict null.

| ID | Topic / subtopic | Side | Claim | Wording |
|---|---|---|---|---|
| CC-101 | Water / Water supply & groundwater | EU | Commission formal notice INFR(2026)2115: no abstraction registration or prior authorisation regime (8 Jul 2026) | Verbatim found (Commission page) |
| CC-102 | Governance & Promises / Accountability | Oversight body | Ombudsman: 58% of Commissioner for Environment and Planning recommendations unimplemented in 2025 | Paraphrase: locate quote |
| CC-103 | Health & Safety / Heat & health | Government | Health Ministry refused heat-death localities, promising publication within three months (26 Aug 2026) | Paraphrase: locate quote |
| CC-104 | Noise | Party (PN) | Malta fails Directive 2002/49/EC (petition, Oct 2024; older than 60 days, noise is least covered) | Paraphrase: locate quote |
| CC-105 | Noise | Party (ADPD) | No study of Freeport and airport noise on residents (26 May 2026) | Paraphrase: locate quote |
| CC-106 | Nature & Wildlife / Hunting & birds | NGO (BirdLife Malta) | Malta holds 1,600-1,800 pairs of Yelkouan shearwater, ~10% of world population (undated page) | Verbatim found (BirdLife page) |

- **Queue:** CC-101, 102, 105 to worker A; CC-103, 106 to B; CC-104 to C (open unblocked loads before 25/26/26 A/B/C, after 28/28/27).
- **Taxonomy:** no category added or renamed. Noise now has 3 claims and, as before, no subtopics. Governance & Promises has 5 claims (subtopics Accountability, Manifestos & pledges).
- **Patterns:** no new pattern tag. CC-105 provisionally tagged Compliance-not-health.
- **Themes:** CC-101 added to T3 (three edges to groundwater/abstraction claims CC-009, CC-039, CC-047 only, not to every member). New T11 Heat, power cuts and health (CC-027, 090, 097, 103), T12 Oversight and disclosure (CC-102, 103; pattern, not causal), T13 Noise governance (CC-020, 104, 105). All Weak (indicative) or Pattern, not causal. 13 edges added (96 total). `Linked claims (count)` was recounted for every claim from edges.csv; 49 older rows changed because their stored counts were stale.
- **Coverage (claims per topic, before to after):** Water 15 to 16, Governance & Promises 4 to 5, Health & Safety 3 to 4, Noise 1 to 3, Nature & Wildlife 8 to 9; all others unchanged. Sides by speaker keyword (approximate): Government 25 to 26, Regulators and agencies 37 to 38, Parties 9 to 11, NGOs 6 to 7, EU 4 to 5, Business 8, Media 11.
- **Candidates for retagging or follow-up (not changed):** CC-090 and CC-103 should be read together; CC-103's deadline (about late November 2026) falls after this intake, so workers should not mark it before then. CC-104 and CC-020 point in opposite directions on compliance and should be checked against the same EEA noise submissions.
- **Considered and excluded:** PN wastewater ranking (duplicate of CC-042), Isla shore-to-ship underuse (near-duplicate of CC-016), 6,000 trees planted (overlaps CC-010/CC-054), EU recycling reasoned opinion (overlaps CC-004/CC-081), Noel Farrugia 'Evergreen Beaches' (no checkable figure), Momentum Gozo enforcement petition and Independent Gozo roads opinion (page unreadable, 403).
- **Network:** net_check reported Wayback unreachable (connection reset); Crossref, Eurostat, EEA ok. Several Newsbook/Independent pages return 403 to WebFetch; wording for CC-102 to CC-105 comes from search summaries and page summaries, hence 'Paraphrase: locate quote'.

### Needs maintainer
- CC-015: exact words of the PA chief's remark (recording/transcript) into `literature/CC-015/primary-source.md`.
- CC-023: 'on track by 2026' wording not found; supply the source passage.
- CC-025: UNFCCC document is browser-only; paste the passage.
- New claims CC-102 to CC-105: ombudsman.org.mt, the EP Petitions portal, ADPD and ERA pages are likely browser-only; supply wording if a worker is blocked.

- 5 Oct 2026, worker B: CC-024 blocked (source: browser-only; NECP PDF behind `sgcaptcha` wall, Wayback reset, IEA/climateaction.gov.mt/Independent 403); maintainer to paste NECP passages into `literature/CC-024/primary-source.md`.
