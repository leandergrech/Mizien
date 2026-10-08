# Review lists

Files here are for the maintainer to review, and nothing in them is a finding. One is shown on the site, labelled as
unreviewed: see `pledge_link_candidates.csv` below.

- `pledge_link_candidates.csv`: for each manifesto pledge, its best candidates in the other election, written by
  `python scripts/pledge_links.py` (method in the script). Fill `decision` with yes or no. A pair goes into the
  `follows` column of `data/manifesto_pledges.csv` (or a claim's `follows:`) only after a yes; regenerating the file
  overwrites it, so copy decisions out first. The Pledges pages show part of it (since 8 Oct 2026), always as
  "similar wording, found automatically, not reviewed", never as a link: for the parties with a programme at both
  elections, each later pledge counted by its closest same-party candidate (strong, possible, none), and the strong
  same-party pairs listed (scripts/build_site_data.py, `pledge_similar`). Other parties' candidates are not shown.
- `pledge_link_benchmark.csv`: pairs used to test the ranking (`python scripts/pledge_links.py --evaluate`). The
  `basis` column says how far each pair can be trusted: `maintainer` (confirmed and recorded in `follows`), `noted`
  (recorded as related in PROJECT_STATE.md, not linked), `assistant` (the assistant's reading of the two summaries,
  not confirmed: a test case, not a link), `repeated` (the same wording in both programmes).
