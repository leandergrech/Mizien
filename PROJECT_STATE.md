# Project state (working notes)

Read this first when resuming work. It records decisions, conventions and what is outstanding, so a new session can
continue without re-deriving anything. Update it at the end of every work session.

*Last updated: 6 October 2026 (pledges stage 4: outliers and the manifesto list on the site; pledges stage 3: cycle disks in Explore; manifesto list extended to every contesting party: 625 pledges from 8 parties' programmes, coverage logged per party; pledges stage 1b: 235 manifesto pledges listed, three government commitments linked, first recycled pledge found; pledges stage 1: kinds, election cycles, manifesto list, outlier rules; pledges drawn as squares; orbit limits for flat views and a turnable pledge stack; Who said it method written up; Who said it: cards with verdict bars, tentative balance and the pledge stack; partial views fixed in Explore; design pass on branch `ccr-870a0223-rgsmf7`: level balance on the Maltese cross as the logo, a light theme, one glyph registry with a glyph for every kind of thing and a glyph key page; homepage deck of claim panels; phone fixes for the Pinned button and Display menu; pinning from claim pages, labels that follow the zoom, In common and saved sets in the tray; step 4: similar wording; step 3: pinned tray with related claims and compare, laurels and spacing sliders; site-wide filter across the web, map and timeline; homepage split from the viewer: new homepage at `/`, full-screen viewer at `/explore/`; earlier: interface revision on branch `ccr-b5c27334-uals26`: map view rebuilt on MapLibre with self-hosted tiles, timeline lanes, network toolbar, claims list off the homepage; timeline page `/timeline/` added; weekly intake CC-109 to CC-116; CC-030 v1.1: verdict changed to Not substantiated after an independent review, pending right of reply; v1.1 corrections to 14 v1.0 checks, on branch `ccr-bd076c78-ydx75j`; CC-011 split requested; earlier: CC-051 v1.1: maps of all of Malta's reported waters, three reference areas and depth bands, on branch `ccr-bd076c78-ydx75j`; earlier: Miżien favicon added; homepage balance mark enlarged and given a slight tilt; CC-009 v1.0 merged into `main` at `77091be`; CC-010 v1.0 merged at `f638e15`; CC-002 evidence follow-up continues on `codex/cc-002-follow-up`; CC-007 v1.1 merged at `68025d0`).*

## What the project is

Miżien: an independent, science-first record of fact-checks on public claims in Malta (authorities, institutions,
parties, NGOs, opposition), focused on quality of life and the environment. The homepage introduces the record with changing claim cards; the Explore tab (`/explore/`) is a 3D mind map of all claims
grouped by topic with links between them. The repository is public and doubles as the assistant's persistent storage.

## Repository

https://github.com/leandergrech/Mizien (public). Site: https://leandergrech.github.io/Mizien/ (GitHub Pages from
`main`, `/docs`). The repo URL is printed on the CC-001 report cover and flyer.

## Design pass: logo, light theme, glyphs (6 October 2026)

Done at the maintainer's request (aesthetics rework; merged by the "Miżien sota" session, no PR from the working session).

**Logo.** A level balance (beam horizontal, pans at one height) standing in the top notch of an eight-pointed Maltese cross.
One mark for every page: `site/_includes/brand-mark.njk` (recoloured through the `bm-*` classes and the `--mark-*` tokens;
the Explore header includes it too, it no longer carries a copy). Favicon: `docs/favicon.svg`, a dark rounded badge so it reads
on any tab colour. The report PDFs and flyers never drew the old tipping scales, so nothing outside the site changed.

**Light theme.** Deep green `#14452F` as the foreground (our reading of "court green": the colour of the report covers and
headings) on pale sage `#e8efe8` with cream cards. Dark stays the default and looks as before (pixel-compared against the
previous build: only the header differs, plus native controls such as checkboxes now follow `color-scheme`).
- `site/assets/theme.css` holds every colour token for both themes; every page loads it first. Colours with transparency are
  written `rgb(var(--rim) / .28)` so the base colour flips with the theme. `--amber` is for fills (always `#e3a72f`);
  `--accent` is amber as text, border, outline or stroke (deeper on light, so focus rings and amber text stay readable).
  Do not hard-code the dark greens in new CSS: use the tokens.
- The toggle (`_includes/theme-toggle.njk`, `assets/theme.js`) sits beside the main tabs on every page. The choice is kept in
  `localStorage` (`mizien.theme`); `?theme=light|dark` shows a theme for one visit (handy for links and for testing).
  `_includes/theme-init.njk` sets it before first paint (no flash). **With no stored choice the site follows the reader's
  system setting (maintainer decision, 6 Oct 2026), dark where the browser cannot say; it also follows a change while the page is open.**
- The claims web (sphere, lines, labels, rings) reads `--cv-*`/`--stage-*` tokens through `map.js` (`readCanvasTheme`); the Malta
  map has a dark and a light palette (`mapStyle`) and restyles in place when the theme changes.
- Checked: axe colour-contrast has 0 violations on 12 page types in the light theme (and on the glyph key and claim pages in
  both); a planted bad colour is caught by the same run, so the audit does evaluate the pages.

**Glyphs.** The idea (the maintainer's): design mirrors information, as map icons are curated in a game, for attention and
discovery. Rules, also printed on `/about/glyphs/`: one silhouette per kind of thing; the same thing looks the same in every
view; things that are the same idea share one glyph on purpose; colour is the verdict, the glyph is the kind (verdict glyphs
repeat the verdict so it reads without colour); **bodies share the glyph of their kind** (no emblem of their own: the register is
open-ended and neutral, and an emblem could read as a logo or an endorsement).
- `site/assets/glyphs.js` is the single registry: 129 glyphs, 8 shared (aliases listed in it). Read by `map.js`, `lens.js`, the
  Eleventy shortcodes `{% glyph name %}` / `{% bodyglyph b %}` (`eleventy.config.js`, via `scripts/glyphs.mjs`) and
  `scripts/validate_claims.py` (place keys). Keys: display names for topics, subtopics, verdicts, patterns, stages and kinds of
  body; `pledge:<label>`; `theme:T<n>`; `place:<key>`; `mode:<grouping>`; `person`. 24 x 24 box, stroke only.
- New in this pass: Health & Safety and Tourism & Population (topics had none), all 32 subtopics (they borrowed their topic's),
  the six pledge labels, ten themes (T6, T9, T10, T13, T15 share a pattern, topic or subtopic glyph), 18 place emblems; and
  collisions fixed (the scales meant Governance & Promises, courts and "group by verdict": it is now the verdict glyph only; the
  speech bubble meant Right of reply and Who said it: Who said it is a microphone; Promise-without-baseline has its own flag;
  Nature & Wildlife is a bird). Claims about the whole country use the Maltese cross (`cross`).
- Places: `location.icon` was changed in 63 `claim.yml` files (presentation only). Every claim at a place must carry the same
  emblem. `methodology/automation.md` says how intake picks one.
- `site/_data/glyphkey.js` runs on every build: it **fails** on two different things drawn identically or a claim naming an emblem
  that does not exist, and **warns** (build log, `[glyphs]`) about topics, subtopics, labels, themes or places with no glyph (they
  fall back to the parent's glyph, or the generic pin). New topic, subtopic, pledge label, theme or place emblem = a glyph in
  `glyphs.js`.
- Shown: web nodes and subgroup rows, filter lists and chips (Explore, timeline), claim pages (topic, subtopic, verdict, pledge
  label, a new "Where" fact with the place emblem, kind of body on every body chip), `/about/glyphs/` (footer and Explore legend).
- Not done on purpose: verdict glyphs inside every `.badge` (many templates; the claim page and filters have them), glyphs on
  individual claims' nodes (their colour is the verdict), unique glyphs for individual bodies (see above).
- Redrawn on 6 Oct 2026 at the maintainer's request: Emissions & targets (an arrow into a target), Open spaces & parks (a
  round tree and a bench), Construction waste (a wheelbarrow of rubble), Valletta (dome and spire on a bastion), Cittadella
  (walls and cathedral front on a hill), Gardjola (the domed lookout with its eye).
- Noticed, not changed: in the Explore panel the "shares: ..." lines under Similar wording (`map.js`, a `span.small` outside
  `#panel p.small`) render in body size instead of the small type used around them. Same on the previous build.

## Timeline page

`/timeline/` (site/timeline.njk, assets/timeline.js, assets/timeline.css) places every claim with a date on one
horizontal line. Claims are clumped by year, month, week, day or hour depending on zoom (buttons, pinch, Ctrl+scroll,
keys), and a claim is never placed more finely than its recorded date: month- or year-only claims are drawn as dashed
bars. **Lanes** (One line / By topic / By who said it / By verdict) split the line, one row per group, so clusters over
time show (e.g. which kind of body made the claims checked as Not substantiated, and when); **Checked claims only**
hides the rest. Both are kept in the address (`?lanes=who&checked=1`). A selected claim links to its page, to its place
on the map (`/?view=map&sel=claim:CC-NNN`, when it has a location) and to the claims web. Links in the page's data are
resolved against the script's own folder, so they work under the `/Mizien/` prefix (they did not before: fixed).
Optional `claim.time: "HH:MM"` (only with a full `claim.date`, checked by validate_claims.py) lets a claim sit on an
hour; no claim has a time yet. Undated claims appear in the text list only. The text list is the no-JavaScript version.

## Pledges: stage 4, outliers and the manifesto list on the site (6 October 2026)

- **`/pledges/` gains "Outliers"**: one subsection per type (recycled, drift, unanchored, dropped) with each recorded
  finding as worded by `pledge_outliers` / `manifesto_outliers`, or "None recorded yet" and why (unanchored needs a
  recorded search; dropped needs the 2022–26 follow-up check, not yet done). "Carried forward" lists the recorded
  same-chain links, which are not outliers. Data: `outlier_list` in the site data (`build_site_data.py`).
- **`/pledges/` gains "The manifesto list"**: the coverage table (election, party, programme, rows, rows with a target),
  parties alphabetical so none comes first; programmes not found show where and when they were searched.
- **New page `/pledges/manifestos/`** (`site/pledges-manifestos.njk`): every listed pledge by election and party, in
  collapsible sections, with number, our summary, target, section and page; checked rows link to their claim; linked
  rows show their links. Each row has its id as an anchor (e.g. `#MP-PL-2026-16-1`) and opening one opens its section.
  Data: `manifesto_coverage` in the site data.
- `data/manifesto_coverage.csv` gains `party_name` (checked by `pledges.py`).
- Next: stage 5 (timeline pledge bars); the dropped check for 2022–26 (research, shelved for now).

## Pledges: stage 3, cycle disks in Explore (6 October 2026)

The Explore "Pledges" grouping (`site/assets/map/map.js`, layout `stack`) is now "Pledges, election by election":
- **One disk per election cycle**, stacked with the oldest at the bottom (the legend groups are the cycles, so a cycle can
  be hidden). Campaign pledges sit on the outer ring, commitments made in office and the other kinds on the inner ring.
- **Chains line up:** pledges joined by `follows` (in the claim records and in the manifesto list) share one angle, so a
  promise and what came of it sit one above the other. Chains are grouped round the disk by the body that first made
  them; each body is named on the highest disk where it has a pledge.
- **Lines:** dashed for "carries forward", red (`RECYCLED_COL`) for "recycled" (promised again after the earlier one was
  not met: the methodology's rule, computed in `build_site_data.py`). The gold overlap lines stay.
- **Manifesto pledges in a chain** that were not checked are outline squares labelled with party, year and number
  (e.g. "Labour 2022 manifesto · 397"); hover shows the summary, a click opens the checked pledge in the same chain.
- The old Who/When/What spokes are gone from this view. Orbit: always from above (pitch -1.0 to -0.2).
- Data: `claims.json` manifesto rows now carry `cycle_label` and, where linked, `links` (`manifesto_rows()` in
  `build_site_data.py`).
- Checked locally: every Explore grouping without page errors, light and dark, desktop and phone, hover on disks,
  pledges, manifesto squares and both kinds of line, clicks, the site-wide filter and the orbit limit.
- Next: stage 5 (timeline pledge bars). Stage 4 is above.

## Pledges: stage 1b, manifesto research (6 October 2026)

- **Manifesto list:** `data/manifesto_pledges.csv` now has 235 rows. Labour 2022 (*Malta Flimkien*): chapter 05
  (environment, pledges 284–377) and chapter 06 (*Malta gżira climate neutral*, 378–412), plus pledge 305 with its
  verbatim wording (PDF p. 91, printed p. 89). Labour 2026 (*Int Malta*, numbered per chapter, ids MP-PL-2026-<chapter>-<item>):
  chapter 14 (*Pajjiż sabiħ*, items 1–64), chapter 16 (*Settur tal-enerġija reżiljenti*, 1–39) and item 13.28. Summaries
  in our own words (drafted from the PDFs by helper agents, spot-checked against the PDFs: 284, 305, 349, 362, 380, 397,
  16.01); verbatim excerpts only for the rows linked to claims. New columns `summary`, `target`, `measurable`, `follows`.
  PDFs read from the party URLs already in `data/sources.csv` (sha256 noted in each row); not committed.
- **Links recorded** (`follows` + `follows_search` in the claims, with a research-log entry):
  CC-024 → MP-PL-2022-378 (climate neutral by 2050, NECP named; no renewables share in the manifesto);
  CC-029 → MP-PL-2022-397 (offshore renewables incl. floating wind); CC-031 → MP-PL-2026-13-28 (Gozo the first part of
  the country to become climate neutral). All same-cycle: shown as "Carries forward", not as outliers.
- **First recycled pledge:** Labour 2026 item 16.01 (PDF p. 186) promises the first offshore wind farm, 300 MW, with no
  date: the same project as CC-029, labelled Off track. Linked in the list (`follows: CC-029; MP-PL-2022-397`) and
  computed as recycled (`manifesto_outliers` in the site data). Not yet shown on a page (stage 4, `/pledges/`).
- Noted, not linked: 2026 item 14.43 reports 57,000 trees planted 2022–25 and continues afforestation with no new number
  (2022 pledge 305 was 100,000 in five years; CC-010 Off track).
- **Still to do:** Labour 2022 chapter 07 (transport) and chapter 13 (Gozo); Labour 2026 chapters 15 and 17 (and the
  same further chapters for every other party, to keep the scope equal); the "dropped" check (after the 2022–26
  legislature, which has ended: which governing-party 2022 pledges in this list have no follow-up, after a search).
- **Outstanding: archive the manifesto PDFs** (Wayback is not reachable from the cloud: connection reset) and add the
  archive URLs; the sha256 of every copy read is in `data/manifesto_coverage.csv`.

### Every contesting party, to the same scope (6 October 2026)

Maintainer decision (relayed by the sota session), now a standing rule in `methodology/verdict-scale.md`: the list
covers the programme of every party that contested each election, to the same scope (whole environment chapters plus
climate and energy chapters), and a party with no programme found is logged with where and when it was searched.
- `data/cycles.csv`: new `contested` and `contested_source` columns, citing the Electoral Commission's nomination press
  releases (2022: "General Election 2022 - All nominations", 6 Mar 2022; 2026: "General Election 2026 - Nominations of
  candidates", 11 May 2026). The site returns HTTP 403 to the cloud; the maintainer saved copies, read 6 Oct 2026, and both
  lists match. Note: the DOI release pr261000en (11 Jun 2026) is a casual-election notice for PN seats, not the results.
- `data/manifesto_coverage.csv`: one row per party per election (status listed / no programme found / not yet listed,
  rows, document, URL, sha256, scope, searched, notes). `scripts/pledges.py` checks every contesting party has a row,
  that the row count matches the list, and that no list row belongs to a party that did not contest.
- **Rows per party** (625 in all):

  | Election | PL | PN | ADPD | ABBA | Volt | People's Party | Momentum | Aħwa Maltin | Imperium Europa |
  |---|---|---|---|---|---|---|---|---|---|
  | 2022 | 129 | 53 | 48 | 6 | 13 | none found | – | – | – |
  | 2026 | 105 | 96 | 88 | – | – | – | 52 | 35 | none found |

  Row counts differ because programmes differ in length and structure (ABBA's environment chapter is one page;
  Labour's are numbered pledge by pledge), not because of scope.
- **How:** helper agents found each party's own copy, extracted the in-scope chapters and drafted summaries with a short
  verbatim locator per row (kept in scratch, not committed). I re-extracted every PDF myself and a script confirmed every
  locator on the stated page (390/390); 16 random summaries were compared with the source text. Labour rows: the item
  number is found on the stated page for 232/234 by script; 14.50 and priority 19 checked by eye.
- **Scope calls** (whole-chapter rule, applied the same way to all): sections printed inside an environment chapter are
  kept even when off-topic (PN 2022 agriculture and fisheries; PN 2026 and Aħwa Maltin animal welfare, Aħwa Maltin
  hunting); standalone chapters on animals, agriculture, transport or Gozo are left out (ADPD *Annimali* and *Il-Biedja*,
  Momentum animal welfare, Volt's transport section). Climate items outside scope are noted in the agents' reports, not
  listed: e.g. ADPD 2026 Gozo zero-emission electricity by 2035, PN 2022 Tema 5 #227 emissions-based road licence,
  Volt 2022 fossil-fuel vehicle ban by 2035. Five ADPD rows record opposition to a named project (Ħal Far race track,
  Wied il-Għajn marina, Magħtab incinerator, the planning reform, 40% incineration).
- **Not found / to confirm:** People's Party 2022 (web chapters at partitpopolari.mt/manifest/, now offline; needs a
  manual Wayback fetch); Imperium Europa 2026 (only a Facebook post labelled "Manifesto", unreadable from here; needs a
  person with Facebook access); Aħwa Maltin 2026 (Drive copy not linked from the party's site, which blocks automated
  access; confirm from its own post); PN 2022 (a March 2022 report says the web version changed after launch; we used
  the launch-day PDF).

## Pledges: stage 1 and squares (6 October 2026)

Maintainer decisions of 6 October 2026: pledges are organised by **election cycle**, not year; a **light list of
manifesto pledges** is started; agency targets are a separate kind; pledges are **squares** everywhere; the outlier
types and wordings in `methodology/verdict-scale.md` (Pledges: Kinds, election cycles and links; Outliers).
- Data: `data/cycles.csv` (2022 and 2026 elections, IFES source; add earlier elections with a source when a pledge
  needs them), `data/manifesto_pledges.csv` (3 rows to start: Labour 2022 pledge 305, wording still to transcribe from
  the archived PDF p. 91; Labour 2026 priority 19; PN 2026 Għawdex chapter). `scripts/pledges.py` (cycles, kinds, links,
  checks), used by `validate_claims.py` (new "pledges:" line) and `build_site_data.py` (pledge `kind`, `kind_label`,
  `cycle`, `cycle_label`, `follows`, `follows_search`, `drift`, `source_of_commitment`; `pledge_outliers`, `cycles`,
  `manifesto_pledges` in the site data and claims.json).
- Kinds set: CC-010, CC-011, CC-107 campaign; CC-024, CC-029, CC-031 government; CC-039 target (WSC). No `follows`
  or `follows_search` recorded yet, so no outlier is shown: the searches are research steps still to do (stage 1b).
- Squares: the claims web (a rounded square in the pledge colour; the verdict as a dot inside when the facts were
  checked; key entry in the legend), the Explore panel lists, the timeline markers and key, the pinned tray, and the
  pledge stack. Not yet: the homepage deck and cards, claim-list badges, the map medallions' leaves.
- Who said it: the pledge stack is now **Pledges, election by election**: one disk per cycle (labels "2022–26",
  "2026–"), campaign pledges on the outer ring, commitments in office on a dashed inner ring; targets are listed apart
  on their body's card ("Target: …").
- Next (stage 1b, research): transcribe pledge 305; enter the environment and quality-of-life sections of the 2022
  and 2026 manifestos into `manifesto_pledges.csv` from the archived PDFs; run the `follows` searches for CC-024,
  CC-029 and CC-031. Then stage 3 (the Explore pledges grouping as cycle disks) and stage 4 (the `/pledges/` page).

## Orbit limits, turnable pledge stack, method write-up (6 October 2026)

- **Orbit limits** (`map.js`, `orbitLimits()`, maintainer request: "it gets confusing which side is up"). Flat
  arrangements can no longer be turned over: a plate or ring (patterns, who said it, pledges) is always seen from above,
  pitch between -1.25 and -0.12 (never edge-on or from below); a row (verdicts, stages, years) tilts between -0.75 and
  0.2 and swings at most 0.85 rad either side, so its left-to-right order never reverses. The topic sphere and the web of
  links still turn freely.
- **Pledges, year by year** can be turned (`assets/pstack.js`): drag sideways to turn the disks like a turntable, up
  or down to tilt them between about 6 and 17 degrees (always from above, newest year on top); on touch only sideways
  (vertical drags scroll the page); arrow keys and Home. A drag is not a click on a pledge. The server-drawn SVG is the
  no-JavaScript version; `who.js` writes the geometry into `data-geo` and each dot's angle and level.
- **Method:** "How a body's checks are summarised" on `/methodology/connections/#summaries` (bar, tentative balance
  with the scale values, the two-year half-life, undated claims, drafts counted, pledges apart, the pledge stack's
  lines), linked from the key on Who said it; the same in `methodology/verdict-scale.md` ("Summaries on Who said it").
- Body pages no longer repeat the verdict counts under "What the claims are about" (the bar above shows them).

## Who said it: cards, balance, pledge stack (6 October 2026)

Maintainer decisions of 6 October 2026: cards with verdict bars; a bar from 5 checked claims; at 3 or 4 a tentative
score that shows the work in progress, weighted by the freshness of the claim date (not the verdict date); pledge
labels always shown; pledges on stacked disks, one per year, similar pledges aligned and joined by lines coloured by
the average verdict. Built from the same `build/site-data.json` as every other view (`site/_lib/who.js`, filters
`whoSummary`, `pledgeStack` and `pluck` in `eleventy.config.js`; `_includes/who-meter.njk`, `_includes/pledge-stack.njk`;
styles in `assets/who.css`).
- **Index** (`site/bodies/index.njk`): each body's card shows claims and checks, then its verdict summary and its
  pledge labels. Verdict bar (counts per verdict, never percentages) from 5 checked claims. At 3 or 4: a tentative
  balance, a hollow dashed marker on a scale from Contradicted (0) to Supported (1), each check weighted by the age of
  the claim (weight halves every 2 years; an undated claim counts as 3 years older than the body's oldest dated checked
  claim, or all weigh the same if none is dated: maintainer decision 6 Oct 2026, so the balance changes only when the
  claims do), with progress dots towards 5. Below
  3: "n of 5 checks: too few to summarise", or "No checks yet". A key above the cards explains the three.
- **Pledges, year by year** on the index (all pledges) and on each body page (its own, with its offices and people):
  an SVG of stacked disks, the newest year on top. A pledge is a dot in its label colour, ringed in the colour of the
  verdict on its facts; pledges on the same topic sit at the same angle on every disk, so similar ones line up; lines
  join pledges from different years with similar wording, the same subtopic or the same topic, coloured by the average
  verdict of their facts (dashed when none is checked). A list of the same pledges follows the drawing.
  A body's pledges are those it made itself or through its offices and people (the pledge's "made by").
- **Body page:** the summary panel under the title (bar, balance or count; pledge labels) with links to the claims web,
  the map and the timeline (filtered to the kind of body), its own statements over time, and "Pin all n claims" with
  the Pinned tray. People get no bar or balance: their checks count towards the body they spoke for.
- Not done: a filter for a single body in the site-wide filter (decision 3 of the proposal is still open; it touches
  `map.js`).

## Partial views in Explore (6 October 2026)

When the site-wide filter or "Show only pinned" leaves only some claims, every view now lays out and frames just
those (`map.js`):
- Groups left with no claims are removed in every grouping (before, verdict, stage and year kept "0 claims" groups).
- The remaining groups draw closer together (`fill`, the square root of the share of groups still shown, at least
  0.42) and the view refits to them through `groupSpread()`. On the topic sphere, one to three groups sit round its
  middle (the spiral put one at the centre or two at the poles), and with four or fewer the opaque sphere is dropped so
  none hides behind it.
- A group with one claim shows the claim above it, clear of the group's label; under the filter or "Show only pinned",
  a set of 24 claims or fewer is always labelled, whatever the zoom (hiding groups in the legend does not trigger it).
  The pledges view always labels its claims, filtered or not (maintainer decision, 6 Oct 2026).
- The web of links centres and scales on the claims shown, not the whole web.
- Map: places with no claims left are hidden (as before) and the map now zooms to the places that remain (at most to
  zoom 15), on load and whenever the filter changes; Fit returns to them.

## Homepage deck and phone fixes (6 October 2026)

- **Deck of claim panels** in the homepage hero (`site/index.njk`, `_includes/deck-card.njk`, the second part of
  `assets/home.js`, styles in `home.css`): a random chain of the checked claims, one panel at a time (verdict-coloured
  head with ID, topic, verdict, confidence and Draft; then title, quote, speaker, date, place, link) with the next two
  fanned behind it. Swipe or drag the front card left for the next check and right to go back; arrows and arrow keys
  too. On wide screens (over 900 px) it sits beside the introduction and turns by itself every 5.2 s, pausing on
  hover, focus or a hidden tab, with a Pause button; never with reduced motion. On narrower screens it follows the
  introduction, before the counts, and only moves when swiped; on phones (640 px and under) the "From the record"
  grid is hidden, since the deck already covers it. Without JavaScript the first card shows, unmoving.
- **Phones:** the Pinned button stays at the right end of the sideways-scrolling filter row (`lens.css`, sticky); the
  Display menu in the web is placed on the page under its button (`map.js`), because the sideways-scrolling control row
  clipped it and it opened invisibly.

## After the plan: claim pages, zoom labels, In common (6 October 2026)

The three items left over from the interface review, done at the maintainer's request:
- **Pin from claim pages.** `site/claims/claim.njk` loads `tray.js` (and `lens.css`): a "Pin this claim" button and
  the Pinned tray sit in the header under the downloads. With `init({ url: false })` the tray leaves the page address
  alone; instead of "Show only pinned" it links to the pinned set in Explore and on the timeline, and Copy link copies
  an Explore link.
- **Web labels follow the zoom** (`map.js`, claim labels in the frame loop): at the overview only the groups are
  named; claim codes fade in from zoom 1.35; from 2.2 the codes give way to the claims' names. Hovered, selected,
  pinned and highlighted claims, and the members of an opened group, are always labelled. The Names button now means
  "names at every zoom".
- **In common** (a tray tab): what the pinned claims share, counted ("4 of 6") from the record: verdict, who said it,
  kind of body, topic, pattern, place, year, pledges; then the theme links and similar wording between them. Each row
  links to every claim like it (Explore with the matching filter, the body's page, or the timeline for a year). Shown
  only for two or more pinned claims; labelled as a lead, not a finding.
- **Saved sets**: "Save this set" names the pinned claims and keeps them in this browser (`mizien.tray` in
  localStorage); the Pinned tab lists the sets to pin again or delete. Copy link remains the way to share a set.

## Similar wording (6 October 2026)

Step 4. `scripts/similarity.py`, run by `scripts/build_site_data.py`: each claim's own words (title, claim text,
verbatim quote; not our counter-evidence) become a TF-IDF vector; two claims are "similar" when the cosine reaches
0.25 **and** they share at least two words (one shared word such as "Gozo" or "blue" is not enough). Words of the
reporting (outlet names, "reported", "told") and common filler are ignored. Each claim keeps its 5 most similar,
with the 3 shared words that weigh most. No library or service; the same result on every run. Calibrated on 5 Oct
2026 data: 57 pairs over 80 claims; top pairs are the Blue Flag claims (0.70), the fish farms (0.67), the Central Link
trees (0.65).
- Written to `data/claims.json` / `docs/data/claims.json` as `similar: [{id, score, terms}]` and to the claim pages'
  data. Shown as **Similar wording** in the Connections section of each claim page and on its card in Explore,
  always with the shared words, and as a reason in the pinned tray's **Find related** ("similar wording to CC-056:
  trees, project"; weight 3 at 0.4 and above, else 2). Labelled as a lead to read together, not a finding.
- To tune: THRESHOLD, MIN_SHARED, TOP and the ignored words at the top of `scripts/similarity.py`.

## Pinned tray, related claims, compare (6 October 2026)

Step 3. `site/assets/tray.js` (styles in `lens.css`), on /explore/ and /timeline/, as a **Pinned** button at the end of
the filter bar:
- **Pin** buttons on claim, group and place cards (web and map) and in the timeline's panel (each claim, or Pin all).
  Pins are kept in this browser (`mizien.tray`) and in the address (`?pin=CC-001,CC-017`; a shared link wins).
  Pinned claims are marked in every view: an amber ring in the web, an amber dot on their place, an amber outline on
  the timeline marker.
- **Show only pinned** narrows the site-wide filter to the pinned claims (`?only=…`, shown as a chip).
- **Find related**: claims scored by what they share with the pinned ones, each with its reasons: a theme link
  (3), the same body (3), the same pattern tag (2), the same place (2), the same topic (1), said within two months
  (1). Top 12; Pin one or Pin all. No hidden inference: the reasons are the data.
- **Compare**: keep the pinned claims as A, pin a second set (B), and see both side by side: verdict bar and
  counts, topics, who said it, places, years.
- Done since: similar wording as a reason (step 4), pinning from claim pages, In common and saved sets (below).

## Laurels and spacing (6 October 2026)

Maintainer decisions of 6 October 2026, built as part of step 3:
- **Laurels** (`site/assets/laurel.js`, one geometry for every view): a group in the claims web (and each subgroup), a
  place on the map and a clump on the timeline carry a laurel with **one leaf per checked claim, in its verdict
  colour** (pledge label colours for pledges). Leaves grow from just left of the bottom, up over the top and down the
  right, one slot per claim in the group, so a **full laurel means every claim there is checked**; colours run from
  the best verdict to the worst. **Freshness is opacity only**: opaque for a review in the last 90 days, fading to
  0.15 at a year, then an outline only (from `last_reviewed`). The old freshness colours (green to brown) are gone.
- Leaves never cover each other: neighbouring leaves are parallel, so they clear each other while the leaf length is
  at most 1.45x the spacing along the branch; the code uses 1.3x, falls back to a second ring and then a wider laurel.
  Checked for discs of 8 to 40 px and groups of 1 to 80 claims (no overlaps, no leaf inside the disc).
- Timeline clumps are now dark discs with a count (like the map's places); their verdict mix is in the laurel.
- **Spacing sliders** in the web (SPACING, in the control column / phone drawer): Groups apart (level 1),
  Subgroups out (level 2), Claims out (level 3), 50 to 200 %, remembered per reader (`mizien.spacing`). The view
  refits (the perspective distance scales with the spacing), so wider groups stay on screen.

## Site-wide filter (6 October 2026)

Step 2. `site/assets/lens.js` (with `lens.css`) is one filter shared by the claims web, the Malta map and the
timeline. Facets: **Topic**, **Verdict** (pledge labels and "Not yet checked" included), **Who said it** (the kind of
body, for every body a claim names), **Year said** (or Undated), **Pattern** (pattern tags), plus free-text **search**
(id, title, speaker, quote, place; accents ignored). Within a facet the values are alternatives; across facets they all
apply. Each facet opens a list with live counts (claims that would show given the other filters). Active filters show
as removable chips with "N of 116 claims" and Clear filters.
- Kept in the address with short keys: `?topic=water&verdict=misleading,contradicted&who=government&year=2026&pattern=selective-metric&q=bus`
  (keys are slugs of the names, made the same way in lens.js and timeline.11tydata.js). The view switch (Web, Map,
  Timeline) sits beside the filter bar on /explore/ and /timeline/ and carries the filter between them.
- Web: claims outside the filter join no group, so groups shrink or empty. Map: places only count claims in the
  filter. Timeline: points, lanes and counts follow it (the text list below the timeline is not filtered yet).
- The homepage question "Which claims didn't hold up?" now opens the web by who said it, filtered to Not
  substantiated, Misleading and Contradicted.

## Homepage and Explore split (6 October 2026)

Step 1 of the plan agreed with the maintainer (story first, tool second):
- **`/` (site/index.njk, assets/home.js, assets/home.css)**: a readable homepage on the standard layout. Introduction
  and counts; "From the record": 12 claim cards (verdict, Draft marker, quote, speaker, date) drawn from the checked
  claims, one swapped every ~4 s (random start; pauses on hover, touch or focus and when the tab is hidden; Pause
  button; no rotation with reduced motion); four starter questions that open the viewer already set up; recently
  checked; how the checks work and the verdict scale. Drafts keep their "Draft" marker on every card.
- **`/explore/` (site/explore.njk)**: the viewer (claims web and Malta map) in its own tab, filling exactly the visible
  screen (100dvh, no page scroll) on desktop and phones. Compact header. On phones the controls are in a "Views &
  filters" drawer that slides up over the viewer and closes when a card opens. `map.js` resolves data, pages and map
  files against the site root (`ROOT`), so it works from any page.
- Old viewer links (`/?view=…`, `/?group=…`, `/?sel=…`, `/?hide=…`, `/?split=…`) redirect to `/explore/` with the same
  query. Links in templates and timeline.js now point to `/explore/`. The nav's first tab is **Explore**; the brand
  goes home.
- Next steps: 2) done (see Site-wide filter; the timeline is reached from the same view switch rather than drawn
  inside /explore/); 3) pinning claims to a
  tray shown in every view, "find related" groups with stated reasons, compare two trays; 4) optional "similar
  wording" measure computed at build time.

## Interface revision (5 October 2026, evening)

Review of every view with the aim of letting readers find patterns themselves (which bodies, topics and verdicts go
together, where and when). Done in this pass:

- **Map view rebuilt** (`site/assets/map/map.js`, map view section). MapLibre GL 6.12 (npm, copied to
  `/assets/vendor/maplibre/` by eleventy.config.js) draws a vector map from a **self-hosted extract**:
  `docs/data/malta.pmtiles` (4.2 MB, zoom 0-14, OpenMapTiles schema from OpenFreeMap, trimmed to the layers the map
  draws; overzoomed to 18.5) and glyphs in `docs/data/fonts/` (Noto Sans, Latin ranges). No map service is contacted
  when someone opens the map. Rebuild with `pip install mapbox-vector-tile pmtiles && python scripts/build_tiles.py`
  (network needed; Geofabrik and Overpass are not reachable from the cloud sessions, OpenFreeMap is). Attribution:
  (c) OpenMapTiles (c) OpenStreetMap contributors (shown on the map). The land is drawn from the island outlines in
  `data/geo.json` and the town names come from its town list, so names follow the site's spelling.
- Zooming is continuous; roads, then streets, street names and buildings appear for the area in view. Each place is a
  **medallion**: the number of claims and one leaf per checked claim, coloured by verdict. Places that would touch on
  screen share a medallion, named after the biggest ("City Gate + 2 places"), which splits as you zoom; pressing a
  merged medallion zooms to its places. Claims are listed **only when a place is pressed** (panel grouped by the body
  that made them, with a verdict bar). Claims with no location are listed under "No place recorded" in the search
  column. Deep links `?view=map&sel=claim:CC-NNN` fly to the claim's place. Without WebGL the page falls back to the
  claims web with a message. The old canvas map (island outlines, trees of bodies and people) is removed.
- **Network (Għanqbuta)**: Names, Lens, Hide text and Pause moved into a Display menu (zoom and Fit stay); the title
  sits beside the control column instead of over the middle of the graph; the control column scrolls instead of
  squeezing; on phones, Arrange, the group list and the colour key fold behind "More options".
- **Homepage**: the claims table is gone; the list lives only on the All claims tab (maintainer request). The skip
  link goes to `/claims/`.
- **Timeline**: lanes, Years level, checked-only filter, links to the map and the web, verdict colours on single dots
  (they were all grey because of a CSS default: fixed).

Proposed next, for user-derived pattern matching (not done; needs a maintainer decision on scope):
1. One shared filter ("lens") across the web, the map and the timeline: topic, verdict, kind of body, pattern tag,
   year, carried in the address so a pattern found in one view opens in the others.
2. A "compare" mode: pin two groups (e.g. Government vs Opposition, or two topics) and see their verdict mix, timing
   and places side by side.
3. Semantic zoom in the web: group labels at overview, claim names only on zoom or hover (the CC-numbers clutter).
4. Make the leaves mean one thing. On the map a leaf is a checked claim coloured by **verdict**; in the web a leaf is a
   checked claim coloured by how **recently its evidence was reviewed**. Pick one meaning, or label both.

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
| CC-002 Comino tree compensation | Report and flyer v1.0 on `main`; a v1.1 (adding the developer's nursery statement) is drafted on the unmerged branch `codex/cc-002-follow-up`. Verdict: Largely supported (moderate) for ERA's announced categories and conditions: 624 + 54 = 678; 92.04% non-protected; 54 × 10 = 540; a separate group of 348 is to be transplanted. The developer reports on-site nursery propagation since 2023, but publishes no stock or survival inventory. The full permit annex, 467/468 oleander discrepancy, transplant results and habitat recovery data remain unresolved. Science-only scope; no legal commentary. Right of reply not sought, at maintainer direction. **Correction (5 Oct 2026):** the cover, page footer, closing line and flyer said 'pending right of reply'; they now say not sought, as the body does (no version change, so the v1.1 on the codex branch keeps its number; that branch has the same wording problem and needs the same fix if merged). |
| CC-003 Per-capita emissions vs 2030 | Report v1.0 and flyer drafted. **Verdict: Misleading (high).** CAA press release 13 Nov 2025 cites the -44% per-capita figure from the Commission's CAPR 2025 but omits its projection: effort-sharing emissions +41% in 2024, +30% to +42% by 2030 vs -19% target (largest gap in the EU). Half the per-capita fall is population growth. Pending right of reply; **must not be circulated beyond the site before the reply deadline.** **v1.1 (5 Oct 2026, corrections):** flyer title says 'per person'; EU projection shown as −31% (WEM) / −38% (WAM); EU industry −36%; 'widest margin' qualified 'in percentage points' (Germany's gap is larger in tonnes); printed page numbers. **v1.2 (5 Oct 2026, upgrade):** EU-27 ranking (Malta 3rd of 27 on the per-person cut, 20th on the total cut; the largest drop between the two rankings); yearly effort-sharing limits vs emissions from the Commission's Tables 25–26 (overshoot 22, 25, 30 points 2022–24; cumulative balance 0.0 Mt by 2024, −2.1 Mt projected 2030; first compliance check 2027); fairness note (per-person target-sector emissions flat, our proxy). Verdict unchanged. |
| CC-004 Waste separation | Report v1.0 and flyer drafted. Verdict: Not substantiated (moderate). Separation up; recycling rate 16.7% (2024) vs 55% 2025 target; 79% landfilled; 412 million kg 'diverted' not reconcilable with Eurostat (271 kt). Pending right of reply. **v1.1 (5 Oct 2026, upgrade):** COM(2023) 304, SWD(2023) 195 and SWD(2025) 318 read directly via Cellar (open-access copies in literature/CC-004/open-access/); EU-27 comparison (Malta +7.6 pp 2019–24, 4th of 20; 2nd-lowest rate). **Confidence raised to High (maintainer decision).** |
| CC-005 Bathing water | Styled report and flyer drafted in the shared CC-001 design. The Commission's exact 92% statement matches the EEA 2023 result (80/87); latest 2025 season is 88.5%. Balluta Bay closure and the CJEU wastewater-treatment case are contextual and do not refute the dated statistic. Draft verdict: Supported (high). Right of reply not sought, per maintainer direction. Viewer metadata uses the same Report / Flyer PDF / Flyer image actions as completed checks. **v1.1 (5 Oct 2026, corrections):** up/down boxes fixed; footer 'right of reply not sought'; 2023 samples 2,021 (EEA WISE); Balluta start 'late May 2024' (EHD report blocked; news says 21 vs 31 May). **v1.2 (5 Oct 2026, upgrade):** EEA per-site classes for all 87 sites 2015-2025: excellent 85, 86, 86, 86, 85, 84, 84, 82, 80, 80, 77; lead over the EU-27 coastal average fell from ~11 points (2016) to 0.2 (2025); ten sites account for every rating below excellent; Balluta B08/B09 Sufficient 2022-25. Three figures. Verdict unchanged (Supported, high); the sentence gives no year. |
| CC-011 Ten minutes' walk to green space (was: Manifesto pledges) | Report v1.0 and flyer drafted. Verdict: Not substantiated (moderate) for both. Labour's pledge is "open or green" space (not "green space"): 99.9% already within reach on a broad reading, 55-68% for parks of at least 0.5 ha. PN's is a plan for a Net-Zero Gozo by 2040 with afforestation as one of several measures (news said "through afforestation"); no Gozo inventory; afforestation alone would need 1.5-8.5x Gozo's area. Pending right of reply. **v1.1 (5 Oct 2026, corrections):** flyer 'already almost met'; election source added (IFES), unsourced seat count removed. Split requested by the maintainer: CC-011 becomes the ten-minute park pledge; the PN net-zero Gozo pledge moves to its own claim. **v1.2 (5 Oct 2026):** split done: CC-011 now covers Labour's priority 19 only (title 'Ten minutes' walk to green space'); priority 18 (40% by 2030) kept as related sub-claim C, so the T7 edges stay. **v1.3 (5 Oct 2026):** pure pledge check: verdict removed, pledge label **Not measurable** as of 5 Oct 2026 (maintainer decision on pledge labels). |
| CC-102 Ombudsman: 58% of environment recommendations ignored | Report v1.0 and flyer (5 Oct 2026, worker A). **Verdict: Largely supported (high).** Ombudsman AR2025 Table 1.3: 7 of 12 sustained cases not implemented at closure (58%); 22 reports to Parliament (Table 1.22). Caveats: tiny counts (46%, 25%, 58% in 2023-25); chapter says 5 of 12 still open when written; 'highest' reverses (Education 67%) if only cases with a recommendation count; Table 1.22 per-office split differs from 1.3 for Ombudsman and Health. PDFs not committed (hashes in data/sources.csv). No right of reply needed. |
| CC-107 A net-zero Gozo by 2040 | Report v1.0 and flyer (5 Oct 2026), split from CC-011 at the maintainer's request. **Verdict: Not substantiated (moderate).** PN programme: a plan for a Net-Zero Gozo by 2040, no baseline, boundary or pathway. New: the 2023 Energy Baseline Scenario for Gozo (EU islands secretariat) gives energy CO2 118-154 kt a year (2016-20); afforestation alone would need 4.9-6.3x Gozo's area at the measured rate (1.5-8.5x wider range). First Gozo pin on the map (Victoria). No edges yet. Right of reply (PN) not sent. **v1.1 (5 Oct 2026):** pure pledge check: verdict removed, pledge label **Not measurable** as of 5 Oct 2026 (maintainer decision on pledge labels). |
| CC-108 WSC 'net-zero impact' on groundwater | Candidate added 5 Oct 2026 at the maintainer's request (speaker-level counterpart to CC-009). WSC's Net Zero Impact Utility pages and the EWA Green Paper (2023: WSC boreholes exempt from groundwater tariffs, abstraction capped at 14m m³ a year to 2030). Wording from search summaries: read the pages in a browser and record verbatim text before any report. Edges CC-009 and CC-101 (T3). |
| CC-006 Spring hunting | Report and flyer v1.1 updated on `codex/cc-006-follow-up`. The report tests both Article 9 conditions. Quota-to-statutory-benchmark ratios are 99.3% for Quail and 59.8% for Turtle-dove. Draft verdict: Not substantiated (moderate): the statutory arithmetic is within the benchmark, but the 2026 enforcement outcome and ecological impact are not established. The 30 March 2026 Ornis minutes were not listed in the WBRU archive (checked 3 Oct); latest season outcome report listed was for 2025. Right of reply remains for the maintainer. |
| CC-007 Within EU limits vs WHO guideline | Report and flyer v1.1 merged into `main` at `68025d0`. PQ 29696 supplied by the maintainer; the Minister's answer is procedural, not a compliance claim. All 23 reported values are below the 25 µg/m³ EU limit and above the WHO 5 µg/m³ guideline. EEA validated files cross-check 11 station-years: ten match to 0.1 µg/m³; Attard 2024 differs (12.122 vs 11.9). Two St Paul's Bay values are n/a. Verdict: Largely supported (moderate), pending full series reconciliation. Right of reply remains with the maintainer. | **v1.2 (4 Oct 2026):** Newsbook read in full from Wayback (dated 18 Jul 2025), quoted verbatim, figures match the annex; confidence High. Codex's older uncommitted v1.0 copy in the main checkout is superseded.
| CC-008 | Transport | Report v1.0 and flyer merged into `main` at `6e1f342`. Verdict: Not substantiated (moderate). Marsa's 2021 travel-time and emissions percentages are agency-reported; the underlying survey/calculation was not found. Msida wording was prospective; the flyover entered use in December 2025 while the broader project continued. No local before/after noise series located. Right of reply not sought, at the maintainer's direction (as the report says). **v1.1 (5 Oct 2026, corrections):** the v1.0 'verbatim' Msida quote did not match the live IM page; now quotes the live page (Wayback capture 29 Oct 2024 not reachable from scripts; check in a browser). Marsa ambient air-quality wording noted; MaltaToday source dates added. **v1.2 (5 Oct 2026, upgrade):** EEA hourly NO2 for Msida (MT00011, located from ERA dataset D: a new sampling point from 17 Jan 2024, ~410 m from the flyover) and three comparison stations; Jan-Sep NO2 19.2 / 22.0 / 25.2 µg/m³ (2024/25/26, 2026 unvalidated): +14.3% in the nine months after the flyover opened. No EEA-reported monitor near Marsa since 2016 (Kordin closed). Three figures. Footer now 'right of reply not sought', matching the v1.0 revision log. Verdict unchanged. |
| CC-039 Net Zero Impact Utility | Report and flyer v1.0 (5 Oct 2026, worker C). Verbatim: WSC release 2 Apr 2019 'ground water abstraction will be reduced by 4 billion litres per year' (Wayback copy; live site bot-challenged). Pledge label **Not measurable** (no baseline or date). Against 2016 (WSC AR 2016: 13.5m m³), WSC groundwater was 2.0m m³ lower in 2025 (49% of 4.0) but only 0.4m lower in 2024; RO output +50%; RO electricity likely up (2016 specific energy 4.85 kWh/m³). 4.68 kWh/m³ for 2024 is second-hand. Right of reply pending (WSC). Live WSC page needs archiving by hand. Sapiano 2020 energy wording is on p. 30 (CC-009 notes say 31). CC-108 is the separate 'give back' claim. |
| CC-009 Reverse osmosis and groundwater | Report and flyer v1.0 merged into `main` at `77091be`. WSC's 2025 report: 70.7% RO share; 11.5m m³ groundwater production, lowest decade. Chart values imply an 11.86% fall from 2024, while WSC prose says 11.4%. The latest RBMP reports two main aquifers poor quantitatively, 14 bodies poor chemically and 12/15 above the nitrate standard. Għar Lapsi Plant B was tendered, not commissioned. Verdict: Largely supported (moderate) for reduced WSC groundwater production; this is not proof of aquifer recovery. **v1.1 (5 Oct 2026, corrections):** Malta's 3rd-cycle EU (WISE) reporting lists 4 groundwater bodies poor quantitatively and 15/15 poor chemically, vs '2 and 14' in v1.0 (the 2 was our reading of the plan; 14 vs 15 is a real plan/WISE difference); both now shown. 'Lowest in a decade' attributed to WSC. **v1.2 (5 Oct 2026, upgrade):** retitled 'More RO, less WSC groundwater' (maintainer decision); national abstraction (Eurostat env_wat_abs/res: 38.5m m³ fresh groundwater 2024, mostly agriculture; recharge 41.5m m³), peer-reviewed literature (Stuart et al. 2010; Sapiano 2020), three figures. Right of reply: **none needed** (Largely supported; maintainer, 5 Oct 2026, under the new right-of-reply rule). Speaker-level counterpart added as candidate CC-108. |
| CC-010 Land & Trees | Report and flyer v1.0 drafted on `codex/cc-010-trees`. Project Green reported >8,000 trees and >25,000 shrubs planted in 2024. Labour pledge 305: 100,000 trees in the next five years (PDF p. 91; printed p. 89). A February 2026 parliamentary answer reports around 60,000 trees and >100,000 shrubs planted collectively by government entities through end-2025. Verdict: Largely supported (moderate) for the reported figures and pledge; the pledge window had not elapsed, and survival/canopy outcomes are unknown. Right of reply not sought, at the maintainer's direction (as the report says). **v1.1 (5 Oct 2026, corrections):** pledge reframed: the 30 May 2026 snap election (IFES) ended the legislature; ~75% of the five-year window had elapsed by end-2025 vs ~60% of trees; Labour 2026 manifesto counts >57,000 trees 2022–25; Project Green vouchers 23,000 (not trees planted). Verdict unchanged; maintainer to decide whether to split it. **v1.2 (5 Oct 2026, upgrade):** pledge-progress figure; sub-claim table A–D, with D (delivery of 100,000 in the pledge period) Not substantiated (maintainer decision: split); no post-election count found. Footer/cover now 'right of reply not sought', matching the text. Pledge label **Off track** (as of 31 Dec 2025) in `pledge:`. |
| CC-012 to CC-021 | Candidates added 3 Oct 2026 (records, sources, literature folders, map links). CC-012 Ta' Qali gravel and grass (both sides); CC-013 Buttigieg: permits keep prices in check; CC-014 Buttigieg: fewer enforcement notices (**In progress**: article blocked by egress on 3 Oct, wording unverified, no report; see `literature/CC-014/README.md`); CC-015 Buttigieg: 'three weeks left' (date check only; scope to confirm); CC-016 shore-to-ship 90%; CC-017 land reclamation (Budget 2026); CC-018 MDA on IMF; CC-019 Amphora: 830,000 m2 land lost; CC-020 noise compliance; CC-021 Gozo tunnel (lead only, weakest). Only CC-013, CC-014 and CC-018 have verbatim wording; the rest need primary sources. New topics Planning & Housing and Noise; new themes T8 (planning, housing and land take) and T9 (compliance-not-health). No NGO claim among them yet. |
| CC-012 Ta' Qali gravel | Report v1.0 and flyer drafted (3 Oct 2026, branch `claude/cc-012-taqali`). **Verdict: Contradicted (high)** for the government assurance that grass would regrow through the gravel (Ministry statement Sept 2025; Micallef). Sentinel-2 2023-2026 (tools/cc-012-report/fetch_s2.py): gravel zone ~2.8 ha found from summer brightening inside the OSM park polygon; greened every winter before (winter median NDVI 0.37-0.47), bare in winter 2025-26 (0.11) while the rest of the park greened; still bare with gravel on 27 Sep 2026. PN/Momentum current-state claim supported; 'permanently' not shown. Rerun fetch_s2.py to update after any works. **v1.1 (5 Oct 2026, corrections):** fetch_s2.py now applies the Sentinel-2 BOA_ADD_OFFSET (−1000, baseline ≥ 04.00). Winter NDVI zone 0.53–0.67 before the gravel vs park 0.65–0.68; 0.15 vs 0.68 in winter 2025–26 (v1.0: 0.37–0.47, 0.11, 0.38). Three pre-gravel winters; unsourced concert date removed; zone 2.76 ha (about a quarter larger than Momentum's 2.2 ha). |
| CC-013 Permits and prices | Report v1.0 and flyer drafted (3 Oct 2026, branch `claude/cc-013-permits-prices`). **Verdict: Largely supported (moderate).** Interview read in full (MaltaToday, 2 Mar 2025); 91,000 is the interviewer's figure (PA: 87,814 approved 2015-24). Research supports direction (Glaeser, Hilber, Saiz) but effect size is uncertain (Anenberg and Kung). Malta pop +31% vs EU +2%; real prices +34% vs +25%; overburden 1.1% -> 6.0% (EU 7.7%); overcrowding 4.7% vs 16.8%. **v1.1 (5 Oct 2026, corrections):** overburden series break at 2023 (Eurostat flag b): comparable runs 1.1→2.9% (2015–22) and 6.0/5.9/6.0% (2023–25), replacing '1.1%→6.0%, fivefold'; real prices +34% (p) / +25% now in checks.csv. **v1.2 (5 Oct 2026, upgrade):** all 27 Member States 2015–25 (Malta population +30.9%, 1st; real house prices +34.2%, 16th; rents +53.1%, 8th); 'fifteen times' corrected to about 16; latest quarter. Verdict unchanged. |
| CC-020 EP noise study | Report v1.0 and flyer drafted (5 Oct 2026, branch `claude/cc-020-ep-noise-study-20261005`, worker C). **Verdict: Largely supported (moderate).** Study read in full (PDF from op.europa.eu download-handler, not committed). Conclusion follows from its evidence; END has only reporting thresholds (55/50 dB, above WHO 53/45 road) and excludes construction/entertainment noise. Eurostat ilc_mddw01: Malta 31.3% report street/neighbour noise (2023), highest in EU (EU 18.1%). **Unverified:** Maltese regulation vs Directive, Commission infringement register, 21% vs 9% survey (ERA annex 403; EU28 source unknown), WHO/EEA figures second-hand. No tag applied (study does not itself commit the Compliance-not-health pattern); T9 membership left as is. |
| CC-030 Carbon-neutral airport | Report v1.0 and flyer drafted (5 Oct 2026, worker C). **v1.1 (5 Oct 2026, corrections after an independent review; maintainer decision): verdict Not substantiated (moderate)** (was Largely supported). Neutrality as ACA defines it is now independently confirmed: ACA directory entry (Level 3+, modified 20 Nov 2025, read through the WordPress REST API) and ACA notice of 18 Dec 2025 (2024 residual emissions offset); Gold Standard block 585497 (1,620 t, Uganda, vintage 2024) and Rainbow transaction 9e16ced5 (2,160 t, France, vintage 2022) retired for MIA on 4 Jun 2026; the Canada block (1,670 t) not found (3,780 of 5,450 t). CINEA's AFIF list confirms the programme (24-MT-TC-AE-MIA, EUR 5,391,500 grant). The 1,000 t has no published method: on the one sourced diesel GPU rate (7.74 kg/h, Fleuti 2006 via Padhra 2018, second-hand; ~25 kg CO2/h) it needs ~40,500 GPU-hours (74 min per turnaround); a GPU at every turnaround for 22.5 min gives ~300 t gross; APU at ~326 kg CO2/h would need 5.6 min per turnaround. v1.0's 40-90 kg/h rates had no source. Claim restated from MIA's own documents (the 25 May release does not mention neutrality). Neutral boundary = 0.7% of the reported 2025 footprint; credits fall 105 t short on market-based Scope 2; Scope 1 +94% vs fuel +30%. 2025 movements (65,470) now primary (announcement 461/2026). Tag Promise-without-baseline. **Pending right of reply (MIA, not sent; draft letter for the maintainer's private doc).** Unverified: credit quality; the Canada block; Scope 1 breakdown; which footprint year the credits were retired against. No edges added (candidate link to CC-003). |
| CC-031 Gozo, first climate-neutral region | Report v1.0 and flyer drafted (6 Oct 2026, worker A). **Verdict: Largely supported (moderate)** for the fleet; **pledge label Not measurable** (as of 6 Oct 2026) for the quoted 'vision'. Wording from Gozo Today (one quoted sentence; fleet is the outlet's paraphrase). Fleet evidence: TVM News 28 May and 4 Jul 2026 (operator/government); Transport Malta page 403. Scale check (Eurostat, population-proportional, not Gozo data): 1.3 kt saving about 2.6% of approximate Gozo road transport. **The plan itself (KPMG for GRDA/CAA) was not found: if the maintainer can supply it, check its target year/baseline/boundary and revisit the pledge label.** Pending right of reply (pledge label). Gozo Today and TVM pages not yet archived (archive/manifest.csv): archive by hand or run scripts/archive_sources.py. |
| CC-029 First offshore wind farm | Report v1.0 and flyer drafted (6 Oct 2026, worker B). **Verdict: Largely supported (moderate)** for the facts (about 300 MW beyond 12 nm, three submissions, output 0.8 TWh = 24.6% of 2025 supply, Eurostat nrg_cb_e); **pledge label Off track** (as of 6 Oct 2026) for 'inform qualifying candidates by the first part of 2026': no public notice on ICM's news list (to 3 Oct 2026) or tenders page; the metocean tender (22 Apr 2026) was issued instead. The label rests on absence of a notice (a private one cannot be excluded): **maintainer decision: keep Off track, or Not yet due/Not measurable until ICM confirms the date.** Ministry release itself refused (gov.mt), so wording is via TVM News and Newsbook; MaltaToday (403) report of the April 2026 dialogue plan seen only in a search summary. NECP offshore wind assumption (energywateragency.gov.mt captcha) not read. Pending right of reply (pledge label). TVM/Newsbook/ICM pages not yet archived (Wayback unreachable from the cloud: archive by hand). |
| CC-037 Amphora: highest reported pollution | Report v1.0 and flyer drafted (5 Oct 2026, worker A). **Verdict: Supported (high).** Verbatim wording read on the Amphora page. Eurostat ilc_mddw02: Malta 34.7%, EU-27 12.2% (2023), first of 27 (Greece 20.5%), first in 17 of 17 survey years. **v1.1 (5 Oct 2026, corrections after an independent review; verdict and confidence unchanged, maintainer decision):** Amphora names no source and links none (speaker now 'Amphora Media'; 'citing Eurostat' removed everywhere); likely source Eurostat's Statistics Explained article (last edited 14 Aug 2025) and news release (1 Sep 2025). 'Reporting exposure' is Eurostat's own wording, so sub-claim D is Accurate (official wording), context not a caveat. Sub-claim E (income) Largely accurate: the split is above/below 60% of median income (the 'above' group is 83.4% of people, ilc_li02), reversed in 6 of 17 years, opposite EU-wide (14.0% vs 11.8%). Trend: +8.2 pp since 2017, highest since 2014 (37.4%). 2021–22 missing because the item (HS180) moved to the three-yearly EU-SILC module 'Labour market and housing' (Reg. (EU) 2019/1700 Annex IV; Delegated Regs 2022/29 and 2020/256: collected 2023 and 2026), all read via Cellar. Eurostat flags now kept in data/cc-037/ (EU-27 2010–2020 estimated; Germany 2023 low reliability). Claim quote moved under `claim:` (claims.json had an empty quote). Sources rows 355–361 (renumbered on integration). **Unverified:** whether Amphora used Eurostat's article or release; the Wayback capture of the Amphora page (16 Jun 2026, listed by the availability API) could not be opened (web.archive.org unreachable). No themes/edges added (could link to CC-020, same survey family). The old alias 'Amphora Media (citing Eurostat)' was removed from `data/bodies.csv`. |
| CC-024 Renewables target for 2030 | Report v1.0 and flyer drafted (5 Oct 2026, worker B, branch `claude/cc-024-renewables-20261005`). **Verdict: Not substantiated (moderate); pledge label On track (as of 15 Sep 2026).** Plan read in full (Commission copy): 24.5% projected for 2030 (summary 25%; 11.5% is the earlier contribution); offshore wind is *not* counted in the 24.5% (p. 83). Eurostat: Malta 17.2% in 2024 vs plan path 15.5%, 18.8% provisional 2025; rise is heating/cooling, electricity 9.5%→10.7%. Commission SWD(2025) 140: 24.5% below the 28% formula. NSO PV figures second-hand (403); 2019 NECP (11.5%) not read. Needs archiving by hand if the archive script cannot reach the Commission file. Right of reply not sent. |
| CC-025 Govt of Malta, COP30: per-capita and per-GDP emissions | Report v1.0 and flyer drafted (5 Oct 2026, worker A). **Verdict: Largely supported (moderate).** Wording is the paragraph supplied by the maintainer (our download of the UNFCCC file hit a bot check; rest of the statement unread). Eurostat: per person -46% (2023) / -48.5% (2024), matching CC-003; per unit of GDP -82% / -84% at current prices but -70% / -72% in chain-linked volumes, so "more than 80%" holds only at current prices (GDP deflator +72%); real GDP +161% with total emissions -27%. No right of reply needed. Data: `data/cc-025/`, `tools/cc-025-report/`. |
| CC-026 EU's largest rise in emissions | Report v1.0 and flyer drafted (5 Oct 2026, worker B). **Verdict: Largely supported (high).** Newsbook (18 Jun 2026) read in full; Eurostat release ddn-20260616-2 gives +169.4% (database now +169.7%). 98.6% of the 2015-2024 rise is air transport under Eurostat's residence principle; territorial UNFCCC inventory +1.6%. Central Bank of Malta report not read (second-hand). Right of reply not sent. |
| CC-045 Flood tunnels | Report v1.0 and flyer (worker C, 6 Oct 2026). **Verdict: Not substantiated (moderate), pending right of reply (Public Works Department).** Wording: TVM News 4 Jul 2025 (16 km in use, 20 km planned; Ellul quote); gov.mt release and MaltaToday article are 403 (not read). Luqa rainfall (NOAA GHCN-D) is context only, gaps after 2019. No flood-incident series found: needs Civil Protection or PWD incident data. Not archived via archive_sources.py (Wayback unreachable); archive by hand. |
| CC-014 Enforcement notices | Report v1.0 and flyer drafted (3 Oct 2026, branch `claude/cc-014-enforcement`). **Verdict: Misleading (moderate).** Interview wording read in full (Malta Independent, 7 Sep 2025). Notices: 1,033 a year 2001-09 (MEPA reports) vs 187 in 2020-24; complaints fell only 11% since 2009 (2,701 to 2,411); ~half of 2024 complaints confirmed illegal; 521 sanctioning applications and 482 removals vs 162 notices. PA's own 2024 report credits persuasion. Gaps: 2008, 2012-2018 (scanned/Issuu reports); 2019-23 second-hand. **v1.1 (5 Oct 2026, corrections):** 2019 complaints 3,134 (PA AR 2019 via Issuu, was 3,174); 'about six times' (1,003 vs 162); 2020 not the series high (FY 2004/05: 3,705); 2024 confirmed cases ~1,200–1,250 (PA categories sum to 1,252); flyer 'applications to legalise'. **v1.2 (5 Oct 2026, upgrade):** 2017–2023 series from the Planning Authority's own annual reports (Issuu page images), replacing second-hand figures; reports since 2018 say notices are issued 'only where contraveners are uncooperative'. Verdict and confidence unchanged. |
| CC-016 Shore-to-ship | Report v1.0 and flyer drafted (3 Oct 2026, branch `cc-016-shore-to-ship`). **Verdict: Misleading (moderate).** Infrastructure Malta page (1 Dec 2023) read in full: "promises to slash 90% of air pollution in the Grand Harbour". Connection voluntary until 2030 (FuelEU Art. 6). Transport Malta FOI records via Amphora Media (second-hand): 67 of 373 berths plugged in Jul 2024-Jul 2025, 9% of berth time; calls 357 -> 385 (2024-25). 90% plausible per connected ship (hotelling >90% of CO2). Gaps: FOI reply itself, ERA Senglea study, basis of 90%. **v1.1 (5 Oct 2026, corrections):** the 90% has a published basis: IM (30 Nov 2020, 19 Feb 2022) scoped it to cruise liners and Ro-Ros that connect (NO2 −93%, PM −92.6%, SO2 −99.6%, CO2 −39.6%); the 2023 page dropped the scope. Costs vary (€33m, €37m, €49.9m). **v1.2 (5 Oct 2026, upgrade):** berths figure (35 plugged in by MSC World Europa, 32 by all others, 306 not); per-ship vs harbour-wide 90%; MSC World Europa is LNG-powered (dual-fuel). Sub-claim A **Largely supported** (maintainer decision). Verdict unchanged. |
| CC-017 Land reclamation | Report v1.0 and flyer drafted (3 Oct 2026, branch `cc-017-reclamation`). **Verdict: Not substantiated (moderate).** Budget Speech 2026 pp. 52-53 read in a browser (verbatim). Sentinel-2: +3.7 ha at Freeport Terminal 2 2023-26 (stated 30,000 m2), so the 'already under way' part holds. No site/size/screening/call for the large project found by 3 Oct 2026; ERA seabed study unpublished since 2019; three Natura 2000 sites ~1 km away. Gap: Posidonia maps for Marsaxlokk Bay. **v1.1 (5 Oct 2026, corrections):** nearest Natura 2000 site (SPA MT0000111) is 0.40 km from the new land at Terminal 2, not 1 km; 'possible and environmentally safe' is the 2019 Environment Minister's wording ('least environmental damage' was MaltaToday's paraphrase); two of the three designations overlap on the same cliffs. **v1.2 (5 Oct 2026, upgrade):** Marsaxlokk Bay map (depth, seagrass, Natura 2000, Terminal 2); PM's 'ideal depth' wording (Lovin Malta) as sub-claim E (not tested); Article 17: Posidonia favourable in Malta's reports. **Maintainer decision: seagrass from EMODnet (CC BY 4.0) only; the UNEP-WCMC layer is dropped** (its licence requires sending copies). Done: EMODnet only (2016 map, cells of about 190 × 230 m): mapped Posidonia next to the new land (one grid cell), 72 ha within 1 km, meadows at 21–32 m within 1 km. Verdict unchanged. |
| CC-018 IMF and the MDA | Report v1.0 and flyer drafted (4 Oct 2026, branch `cc-018-imf-mda`). **Verdict: Largely supported (moderate).** IMF CR 26/29 read in full (PDF supplied by maintainer): prices 'aligned with fundamentals', ratios stable, weakening unlikely; but bank exposure 72% of private loans 'a vulnerability'. Eurostat tipsho60: Malta price-to-income -10.7% 2015-24, below long-term average. MDA wording via MaltaToday (own release not found). **v1.1 (5 Oct 2026, corrections):** MDA release found (mda.com.mt, 8 Feb 2026, modified 17 Jun 2026); it omits the IMF's 'vulnerability' point. Flyer quotes the IMF ('stable'); incomes grew faster than prices; overburden series break as in CC-013. Confidence could rise to High (maintainer). **v1.2 (5 Oct 2026, upgrade):** sub-claims D–G (IMF 24-month cycle Supported; 'first EU economy' **Contradicted**: Luxembourg was on the 24-month cycle in 2000 and 2002; GDP per head 'nearly doubled' Largely supported; 'far higher than the EU average' Not substantiated); the release's IMF phrases come from a Selected Issues paper published after the release date. **Confidence raised to High (maintainer decision).** |
| CC-019 Green to Grey | Report v1.0 and flyer drafted (4 Oct 2026, branch `cc-019-green-to-grey`). **Verdict: Largely supported (moderate).** Amphora articles read (print copies supplied). Independent IO/Esri 10 m land cover: 1.4 km2 net consistent new built-up 2018-23 (3-year rule), so 0.83 km2 is plausible and conservative; previous cover 65% crops / 31% rangeland, so '95% farmland' not reproduced. EEA chart (2012-18): ~0.92 km2, Malta highest land take of EEA39. **v1.1 (5 Oct 2026, corrections):** independent-estimate windows relabelled (3-year rule catches land first built in the 2020–21 maps; 2-year rule 2019–22); Comino 'a quarter to 0.3' (island area source-dependent); 24 km² gross vs 18.9 km² net; year-to-year swings 3–27 km². **v1.2 (5 Oct 2026, upgrade):** Amphora's polygons measured (828,429 m²: 'nearly', not 'over'; file says 2018–2025); IO already mapped 68% of them as built in 2018 and only 2–3% of IO's new built-up land falls inside them, so the model can neither confirm nor rule out 0.83 km² (v1.1 went too far); IO 2024–25 and CORINE change added. **Maintainer decision: spot-check ~40 polygons against 2018/2025 aerial imagery, then set confidence (Moderate if most of the sampled area went green to grey, else Low).** Done: 40 area-weighted draws (39 polygons) on Esri Wayback imagery (2015–16, Sep 2018, May 2023, 2025): 72.5% of the area confirmed green to grey (95% CI 57–84%), 7.5% partial, 17.5% unclear (mostly already under development by Sep 2018), 2.5% already grey, none still open; only 55% was grey by May 2023. Before-land: fields 59% (64% with orchards), scrub/garrigue 36%, so 'nearly 95% farmland' is overstated. **Confidence Moderate** by the maintainer's rule. Classifications are by eye (ours). **Verdict changed to Not substantiated (maintainer decision, 5 Oct 2026):** about 456,000 m² (330,000–574,000) was grey by May 2023 against 'nearly 830,000' for 2018–2023 (about 600,000 m² by 2025), and about a third of the land was scrub or garrigue, not farmland. Right of reply from Amphora Media needed (draft in the maintainer's private right-of-reply doc). |
| CC-012 to CC-014 | Checked locally on 3 Oct 2026 (above). First automated runs (3 Oct 2026) were blocked: the cloud environment's network allowlist refused every source host (Maltese news, gov and party sites, Wayback, Crossref, Eurostat). Status reset to Not started; leads kept in `data/sources.csv` and `literature/CC-0NN/README.md`; blocker recorded in `data/queue.csv`. |
| CC-022 Electricity burden | Report v1.0 and flyer drafted (4 Oct 2026, branch `cc-022-electricity-burden`). **Verdict: Largely supported (high).** Gov PR read in full (browser). Eurostat confirms all figures (MT lowest in PPS, 3rd nominal). Missing context: energy subsidies ~EUR 1.0bn 2022-25 (IMF). **v1.1 (5 Oct 2026, corrections):** 'lowest' qualified to the typical household band (2,500–4,999 kWh); other bands: 2nd, 3rd, 16th, 23rd of 27; 4th of 26 all-band. 2014 tariff cut sourced (Eurostat); the IMF ~€1bn covers electricity and fuel, 2025 projected. **v1.2 (5 Oct 2026, upgrade):** burden against income and use (typical bill 2.2% of median income vs EU 4.7%, 2nd after Luxembourg; 3.5% of a 20th-percentile income, 2nd; average household's actual bill 1.26% of household income, 5th of 26); price and rank in every band. **Verdict kept Largely supported; confidence lowered to Moderate (maintainer decision).** |
| CC-051 Marine protection | Report v1.0 and flyer drafted (4 Oct 2026, branch `cc-051-marine-protection`); **v1.1** (4 Oct 2026, branch `ccr-bd076c78-ydx75j`) adds three maps (all waters reported to the EU; the same protected sea against FMZ / EEZ / EU basis; depth bands) and a sharper summary. **Verdict: Misleading (moderate), unchanged.** EEA union of 18 marine sites = 4,137.5 km2: 36% of FMZ, 7.8% of EEZ, 5.5% of EU-reported waters. All of it lies within 25 nm; ~64,000 km2 (85%) of the reported waters beyond 25 nm has no protected site; whole FMZ = 15.2% of the reported waters; deep sea >1,000 m = 26% of the waters, 0.6% protected. Boundaries in `data/cc-051/boundaries.geojson` (FMZ rebuilt from Marine Regions 12 NM + 13 nm = 11,492 km2 vs official 11,480; EU-reported outline is the EEA's simplified web version, 75,484 km2). Note: ~183 km2 of protected sea is internal waters, which the official FMZ excludes, so like-for-like the FMZ share is 34-35% (ERA's 'more than 35%' is borderline; kept Supported). ERA qualifies (FMZ); minister's 'maritime zone' does not (quote via Amphora). Right of reply not yet sent. |
| CC-075 Seventh in the EU for cars | Report v1.0 and flyer drafted (6 Oct 2026, maintainer session). **Verdict: Misleading (high), pending right of reply (Lovin Malta).** Lovin Malta (21 Sep 2024), describing a Eurostat dataset 'as of 2023': Malta 'is ranked number seven, just between Germany and Poland ... with 585 cars per 1,000 inhabitants'. Right for 2022 in today's data (585, 7th of 27; Germany 587 b, Poland 584 i), but Eurostat had published 2023 figures by 25 Jul 2024: Statistics Explained 'Passenger cars in the EU' revision 647912 (live 19 Aug to 5 Nov 2024, 'Data extracted in July 2024'; Figure 3 sha1 7dd8b8d6...) puts Malta 12th at about 575 (EU 571). The article gives no year and presents seventh as current. Eurostat's January 2024 release had Malta's 2022 value at about 602 (6th), later revised to 585. Today: 11th for 2023, 14th for 2025 (571, below the EU's 584); population grew faster than the car stock. Earlier values read from Eurostat's charts by pixel measurement (within 1.2 of every printed value). **Unverified:** the data year of the graphic the article used (not found); NSO licensed-vehicle figures second-hand (403); rented cars in Malta's stock. |
| CC-094 Commission: Malta to emit more in 2030 than in 2005 | Report v1.0 and flyer drafted (6 Oct 2026, maintainer session; retitled from 'Commission: Malta off track for 2030', since the Commission did not say 'off track'). **Verdict: Supported (high).** Wording read in COM(2025) 668 (note to Figure 13 and s. 3.2, printed pp. 30-31) via the EU Publications Office (EUR-Lex refuses scripts); claim text restated from it; 'missing its target' (intake paraphrase) not rated. Malta's March 2025 projections (EEA): ESR 2030 1,323.8 kt WAM / 1,450.1 kt WEM vs the legal 2005 level 1,020.6 kt (Decision 2020/2126) = +29.7% / +42.1%, gaps 48.7 / 61.1 pp to -19% (Commission 49 / 61). Above 2005 against every 2005 figure and when re-based on reviewed 2023 data (+26% / +38%); 2024 approximated +40.8%. Ranking with planned measures (our reading of the Commission's basis), pp: MT 48.7, IE 20.3, DE 13.2; with existing measures DE falls to 8th; in tonnes DE 64 Mt, MT 0.5 Mt. 2021-2030 balance with the adopted allocations (Decision 2026/895): -2.09 Mt WAM / -2.71 Mt WEM; Malta's own flexibilities (ETS 0.51 Mt, LULUCF max 0.03 Mt) cover 26% / 20%, leaving -1.55 / -2.17 Mt to buy or cut (EU surplus 125-175 Mt is about 80-113 times the WAM figure); no safety reserve (Decision 2023/863). SWD(2025) 140 labels +29.4% as existing measures, but it matches the WAM projection (noted in the report). Consistent with CC-003 (same Commission tables; ESR per person 2.53 t in 2005 and 2024 from the EEA series vs CC-003's proxy 2.50/2.52 t). No right of reply needed. **Unverified:** Malta's own submission files (EEA copy used); 2025 approximated ESR emissions not yet published; AEA purchase intentions and price not public. Data: `data/cc-094/`, `tools/cc-094-report/`. |
| CC-035 PM2.5 death rate down two-thirds | Report v1.0 and flyer drafted (6 Oct 2026, maintainer session; review fixes applied 6 Oct). **Verdict: Largely supported (high confidence).** The EEA's quick-facts sentence reports its own estimate exactly (143.5 -> 46.3 per 100 000 aged 30+, -67.74%; 172 (131-192) deaths in 2023, as Eurostat sdg_11_52, which republishes it); the method recomputes from Eurostat deaths within 1.2%; measured PM2.5 fell from 2007 (Msida -39%, three long-running stations -25% since 2010). Caveats: the EEA maps are not one method (updated PM2.5 method from 2017, EMEP to CAMS from 2020), and no Maltese PM2.5 was reported to the EEA for 2005, so the 2005 start is a map value (21.0; ETC/ATNI 2020/1 gives 21.2, an unexplained gap; our identification of the map); the stations anchor the map and do not check it; the CI covers the risk function only. The number of deaths fell 50.6%. No right of reply needed. Title changed to 'PM2.5 death rate down two-thirds' (update claims.csv and README). **Unverified:** which 2005 map version the EEA uses; Wayback copies (429); Chen and Hoek and Scerri et al. read as abstracts, Scerri corrigendum not read; the indicative 2005 PM10-ratio test rests on other sites and another year; any 2005 PM2.5 data not reported to the EEA. |
| CC-099 Foreign residents: 31% now, 38% by 2030 | Report v1.0 and flyer drafted (6 Oct 2026, maintainer session; revised after independent review). **Verdict: Not substantiated (low confidence).** The words are PwC Malta's press release on its Summer 2026 Economic Update; earliest copy found is Finance Malta's (17 Jul 2026), reprinted by MBW (19 Jul), the Malta Chamber (22 Jul) and Mondaq (23 Jul). The record's original MBW link was a different article without the claim (speaker restated to PwC Malta, title changed). 31% accurate: our calculation from Eurostat data 30.9-31.1% non-Maltese citizens at end-2025 if 2025's change lay within the 2010-24 range (Eurostat has not published the 2026 split; NSO 31.1% second-hand); 32.0% born abroad (1 Jan 2025); 39.8% of registered employment (Jobsplus, Dec 2025). 38% by 2030 is PwC's own model and is not shown: no Eurostat or NSO projection by citizenship found; 'around 38%' tested as 37.5-38.5% of PwC's 636,000, which on citizenship needs Maltese citizens to fall by at least 1,610 a year over 2026-30, though they rose every year 2010-2024; only a projection that leaves out future naturalisations (as the Central Bank of Malta's baseline does, second-hand) gives such a fall, and the release states neither its definition nor its naturalisation assumption. Right of reply on hold until PwC's report is read (pwc.com 403; a browser read could move the verdict). **Unverified:** PwC report; NSO release first-hand; CBM note full text and its path to 2030; the Business Now and Newsbook accounts of the report; parliamentary reply on population projections. |
| CC-032 Solar flowers, first in Europe | Report v1.0 and flyer drafted (6 Oct 2026, maintainer session; review fixes applied the same day). **Verdict: Contradicted (high).** Wording: Camilleri's quoted 'dawn l-ewwel solar flowers fl-Ewropa' (TVM News, Maltese; Lovin Malta's English, tagged 'Press Release', 'these first solar flowers in Europe'); the English TVM article has 'first of its kind in Europe' only in indirect speech; the Commission page repeats the claim in its own words and is not rated. The 15 units are SmartFlowers (maker, 14 Nov 2025: 'one of the largest installations in Europe'); dated records: two installed at the Umwelt Arena, Switzerland (Moneycab, 19 May 2015, the arena's text); on sale in Spain from Jun 2015 (a product launch, not an installation); EV-charging version POP-e presented in Spain Jan 2016; in service at the ASFINAG Hinterbrühl rest area, Austria, Dec 2016 (MeinBezirk community post; IÖB corroborates; earliest in-service date); Vodafone Newbury UK Aug 2021. Bus charging Not substantiated: no capacity, metered output, bus consumption, hours or wiring published, so the share covered cannot be calculated (a 2-3 h/day order of magnitude is kept only as a conditional in report section 5); PQ (Newsbook, second-hand): no feasibility study. PVGIS: 85.1 MWh/yr if each unit is 2.5 kWp (37.5 kWp), +36.5% vs fixed. Cost: PQ EUR 699,611.98 excl. VAT; TED 742398-2024 EUR 718,830.07 (+18% VAT = 848,219; our identification). C1-I5 target 143 kWp by Q2 2026. No tags. Map pin at the Ta' Xħajma hub (Xewkija). **Pending right of reply (Ministry for Gozo and Planning; Public Works Department; draft letter for the maintainer's private doc).** **Unverified:** installed kWp and model; metered output; shuttle buses' model, consumption, hours and charging place; the PQ text itself; whether TED 742398-2024 is this contract; 'second in the world'; a LinkedIn profile reportedly calling Gozo 'the largest installation of SmartFlower Solar units in Europe' (HTTP 999, unread). |
| CC-034 Air Quality Plan 'already yielding results' | Report v1.0 and flyer drafted (6 Oct 2026, maintainer session; review fixes applied the same day). **Verdict: Not substantiated (moderate).** ERA's page (dated 12 Mar 2025 in its metadata) says the plan's actions 'have already yielded positive results'; we rate the plan's list of six measures (our reading). Power-sector reform shown to help (power-station SOx -99.8% 2014-18, -99.9% since 2008 but 55% of that fall before 2015; SO2 in air -83% at Żejtun; Kordin already 2.6 µg/m³ in 2014). Msida NO2 -22% and PM2.5 -17% (2015-17 to 2021-23), in step with fleet renewal, not tied to any named measure; PM10 flat (40.1 to 40.2) and 2023 the worst of 2015-2023 at the old Msida point after ERA's natural deduction (52 days, 35 allowed; ERA's 2024-25 counts are zone counts from other stations). Plan gives uptake, not effect, for grants, ferry landings, fast ferry, free public transport. Its school-transport NO2 test does not reproduce: peak to peak -1.0 µg/m³ in EEA data; its 2018-19 curves reproduce only with hour-ending labels and its 2014-17 baseline under neither labelling; a sustained -11.5 fall began in 2019, not tied to the measure. 10 of 11 station readings rose in the year after free public transport. Tag Input-as-outcome. Pending right of reply (ERA). **Unverified:** no weather normalisation or traffic data; Msida monitor moved Jan 2024 (2024-25 not compared) and Msida Creek works 112 m from the old point (start date not verified); ERA page and plan read from Wayback copies saved 5 Oct (archive unreachable 6 Oct); plan pp. 3, 21-67, 91, 95 read, pp. 4-20, 68-90, 96-104 skimmed only; plan's Figure 26 read off the PDF (±1 µg/m³); EEA UTC+1 convention second-hand; ERA consultation report unread; Scerri 2016 second-hand. |

| CC-111 Commission: 621 kg waste, 74% landfilled | Report v1.0 and flyer (5 Oct 2026, maintainer-requested batch, PR #73). **Verdict: Supported (high).** All figures reproduce from Eurostat env_wasmun (landfill as a share of waste generated); The Shift's 79.2% (CC-081) is the share of waste treated. |
| CC-110 Commission: 37.7% zero-emission new cars | Report v1.0 and flyer (5 Oct 2026, batch). **Verdict: Supported (high).** Eurostat road_eqr_carpda: 37.65% of 7,683 new cars; Malta 2nd in the EU; EU-27 13.53% (report 13.6%). |
| CC-112 IMF: population up 25% in a decade | Report v1.0 and flyer (5 Oct 2026, batch). **Verdict: Largely supported (high).** 25% fits decades ending 2020-2022; the latest decade (2015-2025) is 30.9%; net migration 93-97% of growth. IMF paper read from an Internet Archive copy. |
| CC-115 Chamber: congestion EUR 770m, 3.4% of GDP | Report v1.0 and flyer (5 Oct 2026, batch). **Verdict: Not substantiated (moderate); pending right of reply.** Chamber's LEAD PDF quotes the National Transport Master Plan 2030 (p. 124) accurately, but no derivation for 2025 is published; EUR 770m is 3.1% of 2025 GDP at current prices. |
| CC-100 MIA: over 10 million passengers | Report v1.0 and flyer (5 Oct 2026, batch). **Verdict: Supported (high).** Company announcement 461/2026: 10,061,969 movements (+12.3%); Eurostat avia_paoc 10,070,972. |
| CC-106 BirdLife: shearwaters 10% of world population | Report v1.0 and flyer (5 Oct 2026, batch). **Verdict: Largely supported (moderate).** Malta 1,600-1,800 pairs (ERA plan 1,795-2,635); share 4-13%, central 6-8%. IUCN/BirdLife global figure second-hand (CIESM). |
| CC-053 Milky Way visible from 13% | Report v1.0 and flyer (5 Oct 2026, batch). **Verdict: Supported (high).** Caruana et al. (2020): 12.8% (13.5% on the atlas threshold), 87% Bortle 5+; reproduces; data 2017-2019. |
| CC-049 BirdLife: 242 illegal hunting incidents | Wording found (BirdLife release 10 Oct 2025: Raptor Camp 12 Sep-5 Oct 2025; 51-minute police response). In progress: waiting on the incident log and police/WBRU data (queue blocker). |
| CC-104 PN: Malta fails EU noise law | Petition 1150/2024 located; only a summary, a paraphrase and general quotes are public. Evidence from EP study PE 783.089 in literature/CC-104/README.md. In progress: waiting on the petition text. |
| CC-097 GWU: beach workers and heat | Wording found (GWU statement 17 Jul 2026). In progress: waiting on Securital/ERA responses, OHS heat rules and Met Office warnings. |
| CC-088 NSO: population 588,254 | Report v1.0 and flyer (5 Oct 2026, agent batch 2, PR #75). **Verdict: Supported (high).** NSO NR 120/2026 (Wayback); Eurostat demo_gind reproduces all figures. |
| CC-076 NSO: 36 more vehicles a day | Report v1.0 and flyer (batch 2). **Verdict: Supported (high).** NSO NR 085/2026 Table 1: 460,648 at end Mar 2026, +36/day; pace recent (8-19/day in 2024-early 2025). |
| CC-091 OHSA: inspections doubled, 74% compliant | Report v1.0 and flyer (batch 2). **Verdict: Largely supported (moderate).** 23,711 inspections in 2025 vs 9,381; the 74% rating's base is not stated and cannot cover all construction inspections. |
| CC-047 Nitrates in the aquifer | Report v1.0 and flyer (batch 2). **Verdict: Largely supported (moderate).** Laudi et al. 2026 (abstract only; full text blocked) via MaltaToday; Commission fiche: 68% of groundwater points >= 50 mg/L. |
| CC-042 PN: 'From Blue Flag to Red Alert' | Report v1.0 and flyer (batch 2). **Verdict: Largely supported (moderate).** Sequence accurate (Fajtata closed 30 Jun-2 Jul 2025); 77/87 sites Excellent; 'systemic failure' not rated (opinion). |
| CC-105 ADPD: Freeport and airport noise never studied | Report v1.0 and flyer (batch 2). **Verdict: Largely supported (moderate).** Freeport absent from all ERA noise documents; airport noise is mapped (partly contradicts); no health study found. |
| CC-063 MDA: 'almost complete standstill' | Report v1.0 and flyer (batch 2). **Verdict: Not substantiated (moderate); pending right of reply (MDA).** Construction output +5.8% (2021) and +5.5% (2022); conditional warning, no analysis published. |
| CC-050 BirdLife: 'race' to weaken hunting enforcement | Report v1.0 and flyer (batch 2). **Verdict: Not substantiated (moderate); pending right of reply (BirdLife Malta).** Labour side documented (ORNIS proposal: fines -40%); PN side not shown. |
| CC-081 The Shift: landfill share rising | In progress: the article (19 Feb 2026) returns 404 and is not archived; waiting on its text. Data ready (79.2% of treated, 72.1% of generated, 2024). |
| CC-084 Tourists tripled in 15 years | In progress: no speaker wording for 'tripled' (ADPD's release says '4 miljun turist fis-sena wisq'; the tripling is Newsbook's own sentence). Maintainer to supply a statement or re-scope. |

## v1.2 upgrades and maintainer decisions (5 October 2026)

Branch `ccr-bd076c78-ydx75j`. Each upgraded check has a v1.2 entry in its revision log and `history:`.

**Maintainer decisions taken (5 Oct 2026)**

| Topic | Decision | Where |
|---|---|---|
| CC-010 | Split: counts Largely supported; delivery of 100,000 trees rated separately (Not substantiated); pledge label Off track | report v1.2, `pledge:` |
| CC-018 | Confidence raised to High | report v1.2 |
| CC-022 | Verdict stays Largely supported; confidence lowered to Moderate (income measures put Malta 2nd to 5th) | report v1.2 |
| CC-016 | Sub-claim A (IM's per-ship cuts) Largely supported | report v1.2 |
| CC-009 | Retitled "More RO, less WSC groundwater"; no right of reply (Largely supported; see the right-of-reply rule below) | report v1.2 |
| CC-004 | Confidence raised to High | report v1.1 |
| CC-019 | Spot-check ~40 of Amphora's polygons against aerial imagery, then set confidence (Moderate if most of the sampled area went green to grey, else Low) | done: 72.5% confirmed, confidence Moderate; verdict then changed to **Not substantiated** (period and farmland share overstated) (report v1.2) |
| CC-017 | Seagrass map and statistics from EMODnet (CC BY 4.0) only; UNEP-WCMC layer dropped (licence requires sending copies) | report v1.2 |
| Draft verdicts | Keep showing drafts on the site, marked as drafts; Misleading/Contradicted not circulated elsewhere before the reply deadline | CLAUDE.md, methodology/standards.md |
| Pledges | Six pledge labels with an "as of" date (Not measurable, Not yet due, On track, Off track, Met, Missed); pure pledge checks show only the label | methodology/verdict-scale.md (Pledges); `pledge:` in CC-010, CC-011, CC-107; CC-011 v1.3 and CC-107 v1.1 have `verdict: null` |
| Byline | Project name only ("Miżien · an independent fact-checking project") plus a "Contest a verdict" link to the issue form | tools/mizien_report.py (cover and flyer); reports rebuilt for this batch |
| CC-108 | New candidate: WSC's "net-zero impact" on groundwater | claims/CC-108 |

**Upgraded in this batch:** CC-003, CC-004, CC-005, CC-008, CC-009, CC-010, CC-013, CC-014, CC-016, CC-017, CC-018,
CC-019, CC-022 (v1.2; CC-004 v1.1). New sources rows 298–349 in `data/sources.csv` (renumbered after main's rows when merging, 5 Oct 2026).

**Template changes (tools/mizien_report.py, tools/report_html.py):** byline and contest link on covers and flyers;
pledge labels (`PLEDGES`, `PLEDGE_COLS`, `scale_of()`; `VerdictMeter(i, scale="pledge")`; `verdict_box()` and the
cover/flyer accept a pledge label; `appendix_a(..., pledges=True)` adds the pledge-label table); `up_down(..., heads=)`.
The report HTML colours pledge labels inline (`--v`/`--v-ink`), so it does not depend on new site.css classes.

**Rebuilding a report: figures.** `tools/cc-NNN-report/out/` is gitignored and may hold stale figures from an
earlier version (it did for CC-014). Before rebuilding a check that another branch or agent changed, run
`python tools/restore_figures.py CC-NNN --force` (figures from the committed PDF), or regenerate them with the
check's figures.py and data. Compare the text and figures with the committed PDF before committing.

**For the site session (Miżien sota), hand-off:** PR #55 adds the validator rules and display for `pledge:`, and
`subclaims:` in claim.yml. CC-011 and CC-107 now have `verdict: null`, so they show only the label. After #55 or this
branch merges, whoever merges second runs `git merge origin/main`, then `python scripts/subclaims.py --all` (several
sub-claim tables changed in v1.1/v1.2), then both scripts. The report HTML pledge meter uses the classes
`report-meter pledge-meter` and badges `v-not-measurable` etc. with inline colours; replace them with stylesheet
classes if #55 defines some.

## Ten checks with draft verdicts (6 October 2026, maintainer session)

Asked by the maintainer: "check up to 10 more claims now and submit the draft verdicts". Each claim was checked by
one agent (shared brief: worker-routine method, with shared files applied centrally), then reviewed independently;
every review found something to fix (two changed or sharpened a verdict), and the fixes were applied before
integration. Status on the site: Drafted, draft verdict; nothing sent.

| Claim | Draft verdict | Right of reply |
|---|---|---|
| CC-032 Solar flowers, first in Europe | Contradicted (high) | Pending: Ministry for Gozo and Planning, Public Works Department |
| CC-034 Air Quality Plan 'already yielding results' | Not substantiated (moderate) | Pending: ERA |
| CC-035 PM2.5 death rate down two-thirds (EEA) | Largely supported (high) | Not needed |
| CC-075 Seventh in the EU for cars (Lovin Malta) | Misleading (high); was Largely supported before review | Pending: Lovin Malta |
| CC-094 Commission: Malta to emit more in 2030 than in 2005 | Supported (high) | Not needed |
| CC-099 Foreign residents 31%, 38% by 2030 (PwC Malta) | Not substantiated (low) | On hold until PwC's report is read |
| CC-101 EU: no registration or prior authorisation of water abstraction in Malta | Largely supported (moderate) | Not needed |
| CC-109 EU: transport is 48% of effort-sharing emissions | Largely supported (high) | Not needed |
| CC-113 EEA: Malta among highest fossil-fuel subsidies relative to GDP | Largely supported (moderate) | Not needed |
| CC-114 PN: only EU state with rising emissions intensity | Misleading (high) | Pending: PN |

Letters for CC-032, 034, 075, 114 and (on hold) 099 are in the maintainer's private right-of-reply doc.

**Titles changed** (claim.yml, claims.csv, README): CC-035 (death *rate*), CC-094 (was "off track"), CC-101 (was
"no permits"), CC-113 ("relative to GDP"). **Speaker changed:** CC-099 is PwC Malta's press release (Finance Malta,
17 Jul 2026), not Malta Business Weekly's; PwC Malta added to data/bodies.csv. CC-032's map pin moved to the Ta'
Xħajma hub (Xewkija).

**Licence:** CC-113's source workbook (DG ENER inventory) is © Enerdata, reproduction prohibited: only country
aggregates and five Malta figures are committed; the measure-level extract was kept out of the git history.

**For the maintainer (browser checks):**
- CC-099: read PwC's Summer 2026 Economic Update (pwc.com refuses scripts); it decides the 38% and the letter.
- CC-101: Green Paper (Nov 2023) and interim report (Apr 2025) quotes and pages (EWA captcha); 3rd RBMP.
- CC-075: archive the Lovin Malta article; CC-035, CC-109: archive the EEA pages (Wayback unreachable or 429).
- CC-089: its "Malta Chamber" source is the same PwC release, so its speaker is probably PwC Malta.

**Proposed links, not yet applied** (themes.csv / edges.csv; recount 'Linked claims'):
CC-075 into T4 and CC-003–CC-075 (Weak); CC-109–CC-075 (T4); CC-114–CC-026 (T4, Strong; same residence-based
accounts); CC-094–CC-025 (Strong, shared target); CC-031–CC-032 (same hub and minister); CC-034–CC-007, CC-008,
CC-033, CC-038 (same stations and pollutants); CC-035–CC-037 and a stronger CC-007–CC-035; CC-099–CC-088 and
CC-099–CC-089 (same NSO release and PwC release); CC-101–CC-108 can move from Weak to documented.

## Maintainer unblocks (5 October 2026, afternoon)

Of the eleven In-progress claims, five more blockers had readable sources from the cloud network:

- **CC-024:** the Commission hosts the final updated NECP (381 pages); passages and page numbers in
  `literature/CC-024/primary-source.md` (25% ambition, 11.5% to 25%, 24.5% projected for 2030).
- **CC-025:** the UNFCCC file is a Word document behind a `.pdf` address and is readable. Maintainer decision: keep
  CC-025, reuse CC-003's analysis for the 44% and check the new 'more than 80%' per unit of GDP.
- **CC-034:** ERA's page wording via a Wayback capture (15 Aug 2025) and the plan PDF via Wayback.
- **CC-031:** reworded (maintainer decision) to Camilleri's quoted 'vision' plus Gozo Today's paraphrase of the
  fully electric fleet; check the plan's target (as a pledge if it has one) and the fleet.
- **CC-027:** the record had the wrong year: the statements are from 21 July 2026. Still blocked (indirect speech).
- **CC-021:** taken off the worker queue (a lead, not a statement); status Not started.

Queue rule changed: a maintainer unblock (empty Blocker plus `primary-source.md`) is eligible at once, without the
6-day wait (`methodology/automation.md`, `methodology/worker-routine.md`). Workers still do one claim a night, in ID
order, so worker A takes CC-025, CC-031 and CC-034 and worker B takes CC-024, CC-029, CC-032 and CC-035 over the
coming nights. README statuses were re-synced from the claim records (CC-027, CC-029, CC-035).

## Worker review (5 October 2026)

The maintainer asked for a review of the first night's worker output (CC-030 and CC-037 drafted, five claims blocked).

- **CC-037 (worker A):** the numbers are right; the verdict stays **Supported (high)**. v1.1 fixes the record and
  report: `claim.quote` was at the top level; the text said Amphora cites Eurostat (it names no source); the reasoning,
  sub-claim E and the up/down boxes disagreed with the verdict; the cover said 'published'; Eurostat's own Statistics
  Explained article was missing; the 2021-22 gap needed its reason (EU-SILC moved to Regulation (EU) 2019/1700) and
  the dataset flags had been dropped.
- **CC-030 (worker C):** the release does not contain the neutrality wording the worker quoted as one passage; the
  ACA directory (WordPress API) and the Gold Standard registry were readable after all; the GPU plausibility check
  used rates with no source. The maintainer set the verdict to **Not substantiated (moderate)**: the 1,000 t figure
  has no published method. A right of reply to MIA is needed (draft in the maintainer's private doc).
- **Blockers:** three of five had readable sources and are unblocked with `primary-source.md` (CC-029 and CC-032
  via TVM News, CC-032 also the Commission's project page, CC-035 the EEA quick-facts page). CC-027 stays blocked
  (Lovin Malta paraphrases only; Newsbook leads in its README). **CC-021 needs a decision:** no dated speaker says
  'about three times'; it summarises the Cordina cost-benefit study, so the claim should be reworded at intake (or
  replaced) before a worker takes it again.
- **Routines:** the worker instructions now live in `methodology/worker-routine.md` (all blocker routes tried and
  logged, a source and date for each quoted passage, sourced inputs only, the scale applied literally, `claim.quote`
  inside `claim:`, right-of-reply wording, sources Refs renumbered after main's). The routine prompts can only be
  edited by the maintainer: after this branch merges, replace each worker routine's prompt with the short pointer
  (worker A, B or C) given in the session. Until then the routines run their old prompts.

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

*Superseded on 5 October 2026 (evening) by the MapLibre map: see "Interface revision". Kept for the history.*

- `docs/index.html` has a **Network / Malta map** toggle (also `?view=map`, key M). Network view: larger default
  scale, right-drag / Shift-drag / two-finger pan, zoom towards the cursor or pinch point, double-click to zoom,
  arrow keys, +/-, 0 = Fit.
- Map view: stylised islands from OpenStreetMap (`scripts/build_geo.py` -> `docs/data/geo.json`, ODbL). Claims are
  pins at `location` (new optional field in claim.yml: place, lat, lon, scope = site | institution | national;
  validated). National claims sit at the institution (Castille, Parliament, City Gate, PA in Floriana).
- Map view (redesigned 5 Oct 2026, no gamification): a simplified map with the island outlines, main roads
  (OSM motorway/trunk/primary; secondary once zoomed in) and town centres (OSM place=city/town/village; names in
  everyday use, Maltese spelling, `name` and `mt` both searchable). `python scripts/build_geo.py --keep-islands`
  refreshes roads and towns without touching the island outlines that the CC-017 and CC-019 reports read.
- Trees: each place a claim is about grows a tree: place medallion on the ground, then the office that made the
  claim (`officeOf` the claim's first speaker in the register), then the person who spoke for it (if any), then the
  claims, coloured by verdict. Places that would overlap on screen merge ("Valletta · 8 places"). Overview: only
  medallions with claim counts. Zoomed in (scale >= 2.4): bodies wrap into tiers above the place; a body shows its
  claims for a small place (<= 10 claims), at deep zoom (>= 7.2) or when in focus. A big place out of focus keeps two
  tiers and folds the rest behind a "+N more bodies" node. Places outside the window leave the map (culled).
- Find claims by place: the search box (map view only) matches claim sites and towns without accents (Hamrun finds
  Ħamrun); a town lists claims within 1.5 km of its centre. The grouping controls (Group by, Arrange, groups legend)
  are hidden in the map view; links between claims still work.
- Lens: a fisheye focus at the centre of the stage (Lens button, key L; on by default on phones in the map view,
  remembered in localStorage `mizien.lens`). Magnifies up to 3.2x at the centre, compresses the rim; drag the map
  under it. The scale bar hides while it is on.
- Zoom in the map view changes the map scale (the camera zoom is folded in after every step, claims moved with it),
  so places spread apart while the trees keep their size; icons grow with the scale (iconK). Fit and the place
  search animate the scale in log space about a fixed screen point; the map is orthographic so the fold is exact.
- To do: test the trees on phones with real use; new claims must get a `location` (intake routine updated).

## Audit of the PR #91 draft verdicts (6 October 2026)

Independent audits of the three harshest new verdicts: CC-032 (Contradicted), CC-075 and CC-114 (Misleading). No
figure or quote was wrong. Corrections issued as v1.1 (CC-025 v1.2):
- **CC-032:** verdict and confidence unchanged. MaltaToday source dated and read (reporter text only); sub-claim B
  rated on the minister's own words; his "lighting" wording quoted in D; flyer line made faithful to Newsbook.
- **CC-075:** stays Misleading, confidence High to Moderate (maintainer decision). "No year given" was wrong: the
  article gives conflicting years ("as of 2023" / graphic "up to 2022"); verdict boxes, the 602 explanation and
  limitations fixed; the report no longer claims a reply letter was drafted.
- **CC-114:** stays Misleading, confidence High to Moderate (maintainer decision). Renewables wording narrowed to
  "more renewable electricity, on its own, could not have removed the rise"; 2024 estimates labelled; 116% labelled
  as a share of the rise in emissions; C explained by the Ireland case.
- **CC-025:** context added for fairness with CC-114: on the residence basis per-person emissions rose 69% from
  2013 to 2024 (27th of 27). Verdict unchanged; neither statement names a basis, but CC-025's figures hold on the
  territorial inventory and draw no causal inference.
- Right of reply for CC-032, CC-075 and CC-114 may now be drafted (still pending; not circulated).

## Audit of the worker checks (6 October 2026)

Five independent Sonnet auditors re-checked the ten checks the nightly workers had produced (CC-020, 024, 025, 026,
029, 031, 037, 039, 045, 102; CC-030 had its own review on 5 Oct). No verdict or pledge label changed; nothing
material was wrong in any figure or quote, but there were recurring faults, all corrected (v1.1; CC-037 v1.2):
- **Rated paraphrase:** CC-024 and CC-045 were partly scored against the intake paraphrase or a headline; both now
  restate the speaker's own words and rate only those. CC-031 put TVM's indirect speech in quotation marks.
- **Status wording:** cover, footers and logs disagreed (CC-020, CC-026, CC-102). The report template now derives the
  wording (`reply_status()` in tools/mizien_report.py); `pledge_label=` for mixed checks.
- **Absence claims without a search log:** CC-029 (ICM news now read back to June 2025: no notice) and CC-045
  (flood-incident data search logged; an EWA before-and-after comparison exists but was not read).
- **Second-hand figures in headline places:** CC-039's 4.68 kWh/m³ was not just second-hand but wrong (it is the
  whole-utility figure for 2022); replaced by first-hand WSC figures. CC-024's PV tile and CC-031's 1,300 t thumbnail
  replaced.
- **Right of reply on hold** (new record field `right_of_reply.on_hold`, shown on the site as "right of reply on
  hold"): CC-031 until the Gozo plan is read; CC-045 until the EWA before-and-after comparison is read.
- **Worker routine:** new section 5a in methodology/worker-routine.md with the rules above.
- **For the maintainer:** obtain the Gozo climate-neutrality plan (CC-031) and the EWA before-and-after comparison of
  the flood relief project (CC-045, 2nd Flood Risk Management Plan, measure FLD1); Newsbook pages for CC-026 and
  CC-102 could not be re-read (blocked), their wording rests on the 5 Oct reads.

## Agent batch 2 (5 October 2026, PR #75)

Ten claims checked by Sonnet agents in separate worktrees (shared records written by the lead session from spec files):
eight completed (statuses above), two wait on the maintainer:
- **CC-081:** text of The Shift, 19 Feb 2026, "Malta's waste management is going in reverse" (save as
  literature/CC-081/primary-source.md).
- **CC-084:** an ADPD/Gauci statement that tourist numbers tripled, or a decision to re-scope the claim to Newsbook's
  sentence (speaker then Newsbook) or to drop it. The record names PN; the statement found is ADPD's.
- **Optional:** Laudi et al. (2026) open-access PDF for CC-047; EHD closure reports for CC-042; the 2014-15 Freeport
  noise study for CC-105.
- **Right of reply** needed for CC-063 (MDA) and CC-050 (BirdLife Malta). Not sent.
- **Archive by hand:** CC-076's NSO release (nso.gov.mt blocks scripts; the archive script timed out).
- **Judgement calls to confirm:** CC-050 Not substantiated vs Largely supported; CC-105 Largely supported with the
  airport sub-claim partly contradicted; CC-042 'systemic failure' left unrated as opinion.

## Maintainer-requested batch (5 October 2026, PR #73)

Ten claims chosen to balance coverage of finished checks (before: government 7, agencies 5, no NGO, no Tourism or
Health): CC-049, CC-053, CC-097, CC-100, CC-104, CC-106, CC-110, CC-111, CC-112, CC-115. Seven completed (statuses
above); three wait on documents for the maintainer's drop-box (literature/unsorted):
- **CC-049:** BirdLife Raptor Camp 2025 incident log or report table; police/EPU response-time data or a PQ answer for
  12 Sep-5 Oct 2025; WBRU autumn 2025 report.
- **CC-104:** full text of petition 1150/2024 (or the PN release of 11-12 Oct 2024); the Commission's reply
  (PETI-CM-778413).
- **CC-097:** Securital and ERA responses or the DIER outcome; OHS heat rules and any SOP in force in July 2026; Met
  Office heat warnings for mid-July 2026.
- **Right of reply** needed for CC-115 (Malta Chamber; Not substantiated). Not sent.
- **Archive by hand:** the IMF paper (imf.org 403), the National Transport Master Plan 2030 (infrastructure.gov.mt
  403), the ERA shearwater plan page (era.org.mt 403).

## Outstanding

- [x] **CC-019:** aerial-imagery spot-check integrated (5 Oct 2026); confidence Moderate. `data/cc-019/imagery_spotcheck.csv` lists Amphora's id, centroid, area and place for the 39 sampled polygons (no geometry); drop those columns if Amphora objects. Imagery not committed (Esri terms).
- [x] **CC-017:** EMODnet-only redraw integrated (5 Oct 2026). Rows 340 and 344 (UNEP-WCMC) are marked not used. Unverified: that EMODnet's 'EUSM16me' is IFREMER's EUSeaMap compilation.
- [ ] **CC-108:** read WSC's Net Zero Impact Utility pages and the EWA Green Paper (2023) in a browser; record
  verbatim wording, page numbers and archive links before any report.
- [x] **Right of reply rule (maintainer, 5 Oct 2026):** a reply is sought only where a check finds a claim Not substantiated, Misleading or Contradicted (pledges: Not measurable, Off track, Missed); Supported and Largely supported need none. Reports CC-002, 005, 007, 009, 013, 018, 020, 022 and 026 now say "no right of reply needed" (shared standards text updated in tools/mizien_report.py). Site wording in PR #59. Letter drafts for CC-003, 012, 014, 016, 019 and 051 are in the maintainer's private right-of-reply doc.
- [ ] `data/sources.csv` has duplicate Ref numbers from parallel branches (29–35, 88, 89, 290, 291). Nothing reads Ref as a key, but renumber them in one pass when no other branch is open. (Three CC-010 rows with unquoted commas were fixed on 5 Oct 2026.)
- [ ] **Rebuild the other reports with the byline** when they are next revised (CC-001, 002, 006, 007, 012, 020,
  026, 051 still carry the old cover and flyer footer).
- [ ] CC-018: the MDA release as first published (before its 17 June 2026 change) was not seen.
- [ ] CC-016: which fuel MSC World Europa uses at berth in Valletta (LNG or gasoil) is not known.
- [ ] CC-022: Malta's 2024 household income (national accounts) is provisional; re-run the income measures when final.

- [x] **v1.1 corrections (5 Oct 2026), maintainer decisions** (all decided 5 Oct 2026; see the v1.2 section): CC-010 split the verdict (counts supported; pledge
  delivery not substantiated)?; CC-018 raise confidence to High (MDA wording now primary)?; CC-022 is sub-claim A
  'Supported' too generous given other consumption bands?; CC-016 sub-claim A (IM's per-ship figures, study not
  cited); CC-019 confidence if the low IO/Amphora spatial overlap is confirmed; CC-009 footer says 'pending right of
  reply' but the body says not sought.
- [ ] **v1.1 corrections, browser checks:** Wayback 29 Oct 2024 capture of the IM Msida Creek page (CC-008); MaltaToday
  dates (CC-008, CC-017); EHD Balluta report start date (CC-005); ERA RBMP Chapter 6 groundwater tables and cover date
  (CC-009); PA 2024 annual report outcome categories (CC-014); an official Comino area (CC-019).
- [ ] Rebuild CC-020 and CC-026 (CC-004 done 5 Oct 2026) to pick up the ◆ fix in reference lists (empty box before 5 Oct 2026).
- [ ] `data/claims.csv`: the CC-002 row has misaligned columns (an unquoted comma); fix when CC-002's v1.1 branch merges.
- [x] Upgrades proposed by the 4 Oct review (done 5 Oct 2026 except where noted in the v1.2 section): CC-014 PA reports 2017–23 as primary series; CC-005 time
  series and site map; CC-017 bay map (seagrass, depth); CC-019 Amphora polygon cross-check; CC-004 Commission
  documents; CC-003 ranking and target-path charts; CC-022 band chart; CC-009 abstraction data; CC-018 new MDA
  sub-claims; CC-008 Msida NO2 series; CC-011 Gozo energy baseline.

- [x] Decide author or affiliation line for reports and flyer: project name only, plus a contest link (5 Oct 2026).
- [ ] Add the Times of Malta article URL to `data/sources.csv` and `claims/CC-001/claim.yml`.
- [x] Run `python scripts/archive_sources.py` to fill `archive/manifest.csv` (committed on branch `archive-manifest`).
- [ ] **CC-037 archive (manual):** web.archive.org refused connections from the cloud network on 5 Oct 2026. Open the listed capture of the Amphora guidebook page (16 Jun 2026, URL in `archive/manifest.csv`), check it shows the quoted wording, and save a fresh capture in a browser. Page hashes are in `literature/CC-037/notes.md`.
- [ ] `scripts/archive_sources.py` `robots_ok()` lets `RobotFileParser.read()` fetch robots.txt with Python's default user agent; sites that return 403 to it (amphora.media did on 5 Oct 2026) are then reported as robots-disallowed even when their robots.txt allows the page. Fetch robots.txt with the archiver's user agent and re-check the 27 sources marked robots_disallowed: some may be false positives.
- [ ] Archive by hand the 27 robots-disallowed sources in `archive/manifest.csv` (gov.mt, ERA, NSO, MaltaToday,
  Newsbook, Italpress, arja.mt, Independent, Chambers). gov.mt sites (climateaction, publicservice, DOI) block
  automated access with Cloudflare; read them in a browser.
- [ ] Add the new CC-003/004/011 primary sources to the archive (CAA press release, PR260072en, PL manifesto PDF,
  PN programme pages). The PL manifesto SHA-256 is recorded in `literature/CC-011/references.bib`.
- [ ] Send right-of-reply drafts: CC-003 to the Climate Action Authority and Environment Ministry; CC-004 to the
  Environment Ministry and WasteServ; CC-011 to the Partit Laburista (and the Government) and the Partit
  Nazzjonalista. Record dates and deadlines in each `claim.yml`. Each report lists the questions to ask.
- [x] (Decided 5 Oct 2026: keep showing drafts on the site, marked as drafts; no circulation elsewhere before the deadline.) Decide whether the site should show verdicts for drafts before the reply deadline (it currently does, e.g.
  "Misleading (Drafted)" for CC-003 once merged).
- [ ] `data/candidates.xlsx` is behind the CSVs for CC-003, CC-004, CC-011 (sources, edges, theme T7, quick check).
  It was not edited because openpyxl drops its drawings; update it by hand or treat the CSVs as the master.
- [x] (Decided 5 Oct 2026: six pledge labels, methodology/verdict-scale.md.) Decide whether the verdict scale needs a rule for pledges (CC-011 used Not substantiated = not measurable as worded).
- [ ] CC-003: obtain the CAA "Facts: emissions (June 2026)" factsheet (blocked).
- [x] CC-004: verify COM(2023) 304 early-warning report directly (read via Cellar, 5 Oct 2026).
- [ ] Send CC-001 draft to Ambjent Malta and Fondazzjoni Wirt Artna; record dates in `claims/CC-001/claim.yml`.
- [ ] CC-030 (v1.1, Not substantiated): send the right of reply to Malta International Airport (draft letter handed to the maintainer on 5 Oct 2026 for the private right-of-reply doc; not sent); record `right_of_reply.sent` and the deadline. Ask for the 1,000 t method, the GPU/APU parts of Scope 3 Category 11 and any AFIF CO2 estimate, the Canada credit block, and a Scope 1 breakdown. A published calculation could move the verdict to Largely supported.
- [ ] CC-006: obtain the 30 March 2026 Ornis Committee minutes or other primary vote record; monitor for the 2026 WBRU season outcome report; obtain final 2019–2024 Article 12 data, and FKNK survey methods/results. The official WBRU minutes and outcomes pages were checked on 3 Oct: neither the 2026 minutes nor 2026 season outcome report is listed. Right of reply remains for the maintainer.
- [ ] CC-007: reconcile the Attard 2024 difference between the PQ annex (11.9) and EEA mean of valid daily aggregates (12.122); obtain ERA's validated annual series and coverage/quality notes. The EEA files retrieved do not supply 14/25 station-years, including the two St Paul's Bay n/a cells. The Newsbook page was not retrievable for full-text review; an archived snapshot is recorded. Right of reply is for the maintainer.
- [x] CC-008: locate primary wording for Msida and Marsa; draft report/flyer and add evidence notes. Remaining: obtain the Marsa surveys/calculations and comparable local traffic, air and noise series; right of reply not sought (maintainer's direction). Four earlier MaltaToday sources plus the OPM and Times of Malta pages are robots-disallowed and need browser archiving; ERA's source page also blocks automated access. The AEA publisher returned HTTP 403 to the archiver.
- [x] CC-005: locate Commission wording; compare EEA bathing-water seasons 2023–2025; confirm Balluta Bay warning from the EHD primary report; distinguish CJEU wastewater ruling from bathing-water classification.
- [x] CC-005: add sources to `archive/manifest.csv`. Commission page and CJEU judgment have archived snapshots; EEA 2025 is fetched and hashed. EEA 2024 and the EHD Balluta report are robots-disallowed with no snapshot; archive manually if needed. News leads are robots-disallowed but existing snapshots are recorded.
- [ ] CC-005: review drafted verdict, styled report and flyer; right of reply not sought (maintainer's direction).
- [ ] Obtain open-access full text for the CC-001 A and B studies; fill gaps noted in `literature/CC-001/notes.md`.
- [ ] CC-009: reconcile WSC's 11.4% narrative with the 11.86% chart-derived change if the underlying workbook is obtainable; follow the Għar Lapsi procurement through award and commissioning. Future aquifer recovery requires comparable body-level abstraction, recharge, water-level, salinity and nitrate data. No right of reply needed (Largely supported; rule of 5 Oct 2026).
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

## Weekly intake 2026-10-05 (CC-109 to CC-116)

Eight candidates added, not ten: the searches found few further specific, checkable, non-duplicate statements, and padding was avoided. All are `Not started`, verdict null. Six of the eight come from EU, international or foreign-institution speakers or are about them (the collection was skewed to local speakers).

| ID | Topic / subtopic | Side | Claim | Wording | Source host reachable |
|---|---|---|---|---|---|
| CC-109 EU: transport is 48% of effort-sharing emissions | Report v1.0 and flyer drafted (6 Oct 2026, maintainer session). **Verdict: Largely supported (high).** Commission 2026 Country Report (SWD(2026) 218, Annex 8 p. 66; also pp. 6, 14). Transport (all domestic transport, aviation CO2 excluded: the ESR definition and that of the report's own Graph 3.1) is the largest effort-sharing sector in every year 2005-2024. '+45% since 2005' reproduces exactly as the rise in emissions: +45.0% on the approximated 2024 data (0.528 to 0.766 Mt; 1.A.3 minus the 0.924 kt aviation CO2 the EEA uses for the ESR total), matching Graph 3.1 and Table A8.1; +48.4% on the final 2026 inventory; the share moved 52.0% to 53.3%. The 48% does not reproduce: 53.3% (EEA approximated inventory and Graph 3.1, read from the PDF's vector paths), 53% (Commission CAPR 2025 Malta profile), 54.8% (final inventory, our estimate); only road-transport-alone ratios give 48% (47.5-48.3%; our identification). Small industry is second at 19%. Footnote (140) and Table A8.1 call the sector 'road transport' but the table's series includes domestic shipping (11.9% in 2024, +184% since 2005). 2024 ESR total 1,437.4 kt = +40.8% on the legal 2005 level 1,020,601 t (Decision 2020/2126), consistent with CC-094. No right of reply needed. **Unverified:** how the Commission computed 48%; the EEA's own 2024 sector split as a table (Graph 3.1 read from the PDF); final 2024 ESR figures (2027 review); Wayback copies not reachable from this network. |
| CC-110 | Transport / Cars & traffic | EU (Commission) | 37.7% of new cars in 2024 were zero-emission vs EU 13.6% (same report) | Verbatim found | Yes |
| CC-111 | Waste / Landfill & treatment | EU (Commission) | 621 kg of waste per person in 2024 vs EU 517; landfill rate 82% to 74%, EU 22% (same report) | Verbatim found | Yes |
| CC-112 | Tourism & Population / Population & labour | International (IMF) | Population rose 25% over a decade, largely due to immigration (Selected Issues, Feb 2026) | Verbatim found | Yes |
| CC-113 EEA: Malta among highest fossil-fuel subsidies relative to GDP | Report v1.0 and flyer drafted (6 Oct 2026, maintainer session; review fixes applied the same day). **Verdict: Largely supported (moderate).** EEA sentence verbatim (live page and EEA copies of 3 Feb and 26 Nov 2025; Wayback and archive.today unreachable). Every EEA share rebuilt from the Commission's subsidy database (2024 edition, CIRCABC; (c) Enerdata, so only country totals and five Malta figures are committed, measure rows rebuilt locally by fetch.py after a SHA-256 check) and matched by COM(2025) 17 Figure 16 (28 Jan 2025): MT 3.37%, PL 2.09%, SK 1.51%. The top three holds with Eurostat GDP of 6 Oct 2026 and, as a lower bound, with unconfirmed items set to zero, but SK falls to 1.49% / 1.39%. Malta's 2023 EUR 605m is 96% one line (Enemalta compensation, booked as actual costs and wholly to natural gas; 21.7% of Malta's 2023 electricity was imported), 2.1x the IMF's and 1.7x the Government's 2023 cost, but lower than both in 2022 and close to the Government's figure over 2022-23; the 2024 gap persists. IMF price-gap data record no explicit subsidy for Malta. Malta first again for 2024 in COM(2026) 472. **Unverified:** final 2023 values (2025-edition database not found); source and basis of Malta's EUR 580m; IMF CR 26/29 taken from the CC-018/CC-022 record; smaller bars of COM(2025) 17 Figure 16 not measurable. |
| CC-114 PN: only EU state with rising emissions intensity | Report v1.0 and flyer drafted (6 Oct 2026, maintainer session; revised the same day after an independent review, before circulation; version unchanged, 11 pages). **Verdict: Misleading (high).** Wording: PN press release in Maltese signed by Shadow Minister Eve Borg Bonello, 26 Jan 2026 (pn.org.mt, found via the press-release sitemap; translation ours); figures from Eurostat's news item of 23 Jan 2026 (env_ac_aeint_r2). The statistic is quoted correctly (Jan +16.6%, Aug 2026 data +14.3%, EU -34.0%, Malta 27th of 27 from every base year 2008-2023) but is residence-based: air transport by Malta-resident firms rose 0.30 to 4.73 Mt (72% of 2024; 116% of the net rise; all of the rise is fuel bought abroad). Our counter-figures are tested from every base year as strictly as the PN's: without air transport the indicator fell from every base year 2008-2023 (-8.5% to -72%), -64.0% since 2013 (2nd of 27) but -29.5% since 2016 (17th; EU -30.1%); territorial inventory per euro of GDP -61.3% since 2013 (2nd), -27.1% since 2016 (21st; EU -29.8%); most of the fall came in 2014-2016 (electricity-sector emissions 1,703 to 581 kt; 743 kt in 2024, +28% from 2016); from bases 2014-2019 Malta's rise is +19.5% to +97%. Renewables link rated Contradicted on the decomposition (with zero electricity-sector emissions the indicator would still be 1.4% above 2013; renewable shares rose 1.6% to 10.7% electricity, 3.8% to 17.2% overall); 'lack of ambition on several fronts' is a political judgement, not rated; 'every euro' (D) rated Needs context (amber), as CC-026D. Only with end year 2024 (Eurostat estimate): 2013-2023 -8.3%, no riser. Release mislabels Estonia/Ireland/Finland intensity cuts as emission cuts (emissions, residence accounts / territorial inventory: Estonia -55% / -53%, Finland -38% / -38%, Ireland +13.7% (flag e) / -6.9%); 10.7% is the electricity renewables share (overall 17.2%, 4th from last; Eurostat's release of 18 Dec 2025 names Belgium, Luxembourg and Ireland as the lowest three). Side by side with CC-025 (Government gave no basis; 'more than 80%' holds at current prices only, -72% in volumes) and CC-026 (same accounts; Largely supported because its body explained the residence vs territorial difference, its headline alone 'Needs context'). **Pending right of reply (Nationalist Party; draft letter in the maintainer's private doc); not to be circulated beyond the site before the deadline.** **Unverified:** which airlines are resident (not named by Eurostat or the NSO); Eurostat's 2024 estimate; no January copy of the release (page modified 24 Apr 2026); papers read as abstracts. |
| CC-115 | Transport / Cars & traffic | Business (Malta Chamber) | Congestion cost EUR 770 million in 2025, 3.4% of GDP (2026 election proposals; date to record) | Verbatim found (Lovin Malta quoting) | Partly (Chamber PDF probably browser-only) |
| CC-116 | Planning & Housing / Heritage & character | International (UNESCO WHC) | Malta's planning policies do not sufficiently safeguard Valletta's setting; height controls and report due 1 Dec 2026 | Paraphrase: locate quote | No (whc.unesco.org 403) |

- **Queue:** CC-109 to C, CC-110 to C, CC-111 to A, CC-112 to C, CC-113 to A, CC-114 to B, CC-115 to C, CC-116 to A. Open unblocked loads before 26/27/24 (A/B/C), after 29/28/28.
- **Taxonomy:** no category added or renamed; no new subtopic (all reuse existing names). Noise still has 3 claims and no subtopics. No Noise, Nature, Water, Health or NGO candidate qualified this week.
- **Patterns:** no new tag. CC-110 and CC-114 provisionally tagged Selective metric.
- **Themes and edges:** CC-109, 110, 115 added to T4; CC-111 to T5; CC-110, 114 to T6; CC-109, 114 to T7; CC-112 to T10. New T14 Energy subsidies (CC-022, 095, 113) and T15 Heritage and development control (CC-065, 066, 116), both Weak (indicative). 29 edges added (128 total). Edges were added only between claims that speak to the same issue (for example CC-114 with CC-025 and CC-003; CC-111 with CC-081 and CC-004; CC-115 with CC-008 and CC-071), not between every pair of the large themes, following the 4 Oct intake. `Linked claims (count)` was recounted for every claim (27 older rows changed).
- **Coverage (claims per topic, before to after, counted from claim.yml):** Transport 12 to 15, Climate & Energy 14 to 16, Planning & Housing 12 to 13, Tourism & Population 10 to 11, Waste 6 to 7; all others unchanged. Sides by body type: Government 32, Agencies 17, Regulators 14, Media 11, Business 10 to 11, Parties 10 to 11, EU and international 5 to 11, NGOs 5, Research 3, Oversight 1. Local speakers 103 to 105; EU, international and foreign speakers 5 to 11. NGOs and civil society remain the least covered side (5), then Noise (3).
- **Follow-ups (not changed):** CC-111's 74% landfill rate (2023) and CC-081's 79.2% (2024) and the NSO's 72% (2024) use different scopes: the worker should read the report footnote first. CC-115 and Cremona's EUR 1.13 billion (Malta News Agency, 3 Jun 2026) are alternative congestion-cost estimates. CC-114 and CC-025 pick different base years (2013 vs 2005). CC-116's 1 Dec 2026 deadline is after this intake: do not mark it before then. CC-113 is about 20 months old.
- **Considered and excluded:** NSO 2024 waste release (Newsbook, 2 Dec 2025; near-duplicate of CC-081/CC-004), EU Environmental Crime Directive and Industrial Emissions transposition notices (procedural, no checkable figure), 17% of beaches 'poor' (The Malta Post; overlaps CC-005 and the source is secondary), Din l-Art Ħelwa on the Comino tree permit (CC-002, sub judice, opinion), GRECO anti-corruption report (outside scope), Isla heat-island and Posidonia studies (MDPI pages returned 403; no checkable claim read).
- **Network:** `net_check.py` reported Crossref, ec.europa.eu, Wayback and EEA reachable. The Council, IMF and EEA documents were read through WebFetch; Newsbook, MaltaToday and whc.unesco.org gave 403 to some pages.

### Needs maintainer (weekly intake 2026-10-05)
- CC-116: the World Heritage Committee decision number and exact wording on Valletta (whc.unesco.org/en/soc/4677 returns 403) into `literature/CC-116/primary-source.md`.
- CC-115: the Malta Chamber's own election-proposal document (LEAD) and its date, with the method behind EUR 770 million (browser-only).
- Standing blockers (queue rows starting `source:`): CC-015, CC-023, CC-027, CC-028 (see the 4 Oct list above).

## Weekly intake 2026-10-04 (CC-101 to CC-106)

Second intake of the day (the 79-claim bulk intake ran earlier). Six candidates added, not ten: searches turned up few specific, checkable, non-duplicate statements, and padding was avoided. All are `Not started`, verdict null.

| ID | Topic / subtopic | Side | Claim | Wording |
|---|---|---|---|---|
| CC-101 EU: no registration or prior authorisation of water abstraction in Malta | Report v1.0 and flyer drafted (6 Oct 2026, maintainer session; review fixes applied 6 Oct). **Verdict: Largely supported (moderate).** Verbatim from the Commission's INF/26/1376 (8 Jul 2026), identical on the Representation page; the letter of formal notice INFR(2026)2115 is not public. The verdict covers the Commission's first sentence, rated on the facts: Maltese law (legislation.mt) has a register of groundwater sources (S.L. 549.164, notification due by 20 Nov 2008) and drilling permits (S.L. 549.165, moratorium with exceptions); both state they give no right to draw water; we found no permit to abstract and no surface-water registration in the instruments read, the titles of all 943 Legal Notices, the text of all 101 Acts of 2024-2026 or the titles of 344 S.L. (none found in force; the one borehole notice, L.N. 374 of 2024, only adds a research-borehole exception). EWA/ERA Green Paper (Nov 2023) proposes ERA abstraction permits; Malta's Apr 2025 interim report: framework 'close to being finalised' while describing the register as the control ('Only these registered sources are permitted to extract groundwater'). S.L. 549.100 reg. 12(3)(e) copies the review duty: sub-claim D not rated, nor legal sufficiency (legal questions); A (the Directive's requirement) is a premise, not rated. Caveat: SWD(2019) 48 wrote of 'a concession, authorisation and/or permitting regime to control groundwater and a register of groundwater use' (p. 121) and, p. 125, of authorisation legislation still to come. Surface water: 3 WFD watercourses (3.4 km), 2 pools; Eurostat 2.96m m3 'fresh surface water' abstraction (estimated, unexplained). No right of reply needed. **Unverified:** the letter and Malta's reply; the 3rd RBMP text itself (ERA 403, Wayback unreachable); no current count of metered sources (Malta: 'most' in 2025, more than 3 000 in 2019); Amphora's ERA figures (second-hand); the Green Paper and interim-report quotes were not re-checked by the reviewer (EWA captcha): check in a browser (list in literature/CC-101/notes.md). |
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
- CC-015: exact words of the PA chief's remark into `literature/CC-015/primary-source.md`. Only video has them (The Maltese Herald, 24 Sep 2026, protest at the planning conference); Newsbook and The Shift paraphrase.
- CC-023: a dated government statement with the 2026 completion date (Lovin Malta, 10 Jan 2025, has it only in paraphrase); the government press release on gov.mt or MaltaToday article 137267 (both 403 to scripts).
- CC-027: the words of 21 Jul 2026 (TVM interview with Abela; Dalli in Lovin Malta), both reported as indirect speech: a transcript or press release.
- CC-028: Enemalta's 76% statement (made to MCESD; no release on enemalta.com.mt; outlets paraphrase): a press statement, if one exists.
- ~~CC-025~~, ~~CC-024~~, ~~CC-034~~, ~~CC-031~~: unblocked 5 Oct 2026 (see 'Maintainer unblocks' below).
- New claims CC-102 to CC-105: ombudsman.org.mt, the EP Petitions portal, ADPD and ERA pages are likely browser-only; supply wording if a worker is blocked.

- 5 Oct 2026, worker B: CC-024 blocked (source: browser-only; NECP PDF behind `sgcaptcha` wall, Wayback reset, IEA/climateaction.gov.mt/Independent 403); maintainer to paste NECP passages into `literature/CC-024/primary-source.md`.

- **5 Oct 2026, worker C:** CC-021 (no dated speaker statement; the 'about three times' figure is a secondary summary of the Cordina cost-benefit study) and CC-027 (Lovin Malta paraphrases only) blocked, `source:` Blockers set, status In progress. CC-030 done. (Superseded 5 Oct 2026: the ACA directory and the Gold Standard and Rainbow registries were read through their public APIs for CC-030 v1.1; the ACA site's captcha blocks repeat automated requests.)
| CC-040 Water use per head | Report v1.0 and flyer drafted (7 Oct 2026, worker A). **Verdict: Largely supported (moderate).** E&WA keynote slides read (slide 10); no EU comparison in deck (intake wording not rated). Eurostat households 120 l/person/day 2024 (est.), Malta 13th of 19. Needs: IWRA PDF archived by hand (Wayback refused); WSC billed data. |
