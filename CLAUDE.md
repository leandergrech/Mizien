You are joining Miżien, an independent, science-first fact-checking project on public claims in Malta (authorities, institutions, parties, NGOs, opposition), focused on quality of life and the environment. Repo: https://github.com/leandergrech/Mizien (public, branch main). Site: https://leandergrech.github.io/Mizien/ (GitHub Pages from /docs).

START HERE
1. Read PROJECT_STATE.md first (conventions, design tokens, status, outstanding tasks), then README.md, methodology/*.md and data/claims.csv.
2. Run: pip install -r scripts/requirements.txt && python scripts/validate_claims.py && python scripts/build_site_data.py. Both must pass before and after any change.
3. Check the site builds and loads: npm ci && npm run build, then PATH_PREFIX=/ npx eleventy --serve (Node 24). Without Node, rely on the PR's "Site" check, which builds every PR.

NON-NEGOTIABLE RULES
- claims/CC-NNN/claim.yml is the source of truth. After changing any claim record, regenerate data/claims.json and docs/data/claims.json with scripts/build_site_data.py and commit both.
- Verdicts use the scale in methodology/verdict-scale.md. "Misleading" or "Contradicted" require documents or data that can be shown (evidence_shown field). Never publish either before the right-of-reply deadline has passed.
- Quote the speaker, not the headline. Do not start a report until verbatim primary-source wording is found and archived (wording_status: Verbatim found).
- Science first: peer-reviewed literature, then independent datasets (Eurostat, EEA, NSO, WHO), then EU/regulator reports, then news. News and advocacy sources locate claims; they are not evidence.
- Never invent citations, DOIs, figures or quotes. Verify every reference against Crossref or the publisher record. Entries in literature/*/references.bib marked "to verify" must be checked and fixed. Mark second-hand sources as such.
- Copyright: paraphrase; quote only short phrases; commit only open-access PDFs under literature/CC-NNN/open-access/. Never commit paywalled PDFs or full articles.
- Check every side equally (government, opposition, NGOs, developers). Criticise statements, not people. No claims about motive without documents.
- CC-002 (Comino) is before a planning tribunal: stick to the science, no legal commentary.
- Use British English and correct Maltese spellings (Miżien, Għar Lapsi, Ħondoq, Magħtab, Għallis, Wirt Artna).
- Do not contact third parties, send right-of-reply messages, or publish anything externally. Draft them and hand them to the maintainer.
- Never commit secrets, tokens or personal data. Never force-push. Work on a branch per claim (e.g. cc-003-climate), make small commits, and open a pull request for the maintainer to merge.

WORKING METHOD FOR A CLAIM
1. Open claims/CC-NNN/claim.yml and data/sources.csv (filter on the ID). Locate and archive the verbatim wording.
2. Split the claim into checkable sub-claims.
3. Collect literature into literature/CC-NNN/ (references.bib, notes.md noting full text / abstract / second-hand, gaps). Test numbers with formulas or scripts, not by eye; save them in data/ with the source and retrieval date.
4. Grade the evidence (A to D), show disagreements side by side, state what would change the verdict.
5. Build the report and flyer from tools/cc-001-report/ and methodology/report-outline.md. Match the CC-001 design. Output to claims/CC-NNN/. The claim page shows the full report as HTML, built from report.pdf and build_report.py by tools/report_html.py (CI does this on every build); run python tools/report_html.py CC-NNN to check it reports "ok".
6. Update claim.yml (status, verdict, tags, outputs), the Connections themes and edges if the claim links to others, and the README claims table.

FIRST TASKS, IN ORDER
1. Run scripts/archive_sources.py (network needed) and commit archive/manifest.csv. Report which sources were robots-disallowed so the maintainer can archive them by hand.
2. Verify and fix the bibliographic metadata in literature/CC-001/references.bib; obtain open-access versions where legal.
3. CC-003 (climate: per-capita emissions vs the Commission's 2030 projection) end to end, using EEA/Eurostat/Commission primary sources.
4. CC-004 (waste: "strong progress" vs EU recycling targets), same method.
5. Collect literature for CC-005 to CC-011 and locate verbatim primary wording for CC-005 to CC-010.

END OF EVERY SESSION
Update PROJECT_STATE.md (status, outstanding items, anything the next session must know), run both scripts, and summarise what changed, what is unverified, and what needs a human decision. Ask the maintainer before anything irreversible or public.
