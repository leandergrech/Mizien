# CC-099: Foreign residents, 31% now and 38% by 2030 (PwC Malta)

**Status:** Drafted (v1.0, 6 Oct 2026, maintainer session). Verdict Not substantiated (low confidence); right of
reply to PwC Malta on hold until its *Summer 2026 Economic Update* is read. See `notes.md` (sources, access, search
log, page hashes) and `references.bib`. Data: `data/cc-099/` (Eurostat with flags, Jobsplus workbooks, `checks.csv`).
Report build: `tools/cc-099-report/`.

No open-access PDFs are committed: the evidence is Eurostat and Jobsplus data and web pages, all linked in
`references.bib`. The Central Bank of Malta policy note (SSRN, "green" open access per OpenAlex) could not be
downloaded from this network, so no copy or licence was checked.

## Who said it, and where (wording found 6 Oct 2026)

The claim record's text ("foreign residents now make up 31% of Malta's population, potentially rising to about 38% by
2030") is PwC Malta's press release on its *Summer 2026 Economic Update*. The **earliest copy found** is Finance Malta's
(Industry Update / PwC, **17 July 2026**, with PwC's boilerplate and "© 2026 PricewaterhouseCoopers"); Newsbook quoted
PwC's Territory Senior Partner the same day. The Malta Business Weekly reprinted it "By The Malta Business Weekly" on
Sunday 19 July 2026 (post 30680), the Malta Chamber on 22 July and Mondaq (author PwC) on 23 July. The record's own link (post 29055, 2 Jun 2025, by Silvan Mifsud, on the Central Bank
of Malta's Policy Note 1/2025) is a **different article that does not contain the claim**: it gives 28.1% of the
population as foreign nationals in 2023 and "just over 31%" of the working-age population (and later 30.4% for the
same share). The intake appears to have attached the wrong Malta Business Weekly link.

Verbatim (press release, read in full on financemalta.org, maltabusinessweekly.com, maltachamber.org.mt and mondaq.com; identical text; paragraphs 2 and 6 on Finance Malta):

- "The latest figures show that foreign residents now make up 31% of Malta's population, with net migration patterns
  continuing to drive growth."
- "Our projections are based on varying levels of slowdown in current net migration flows. Nonetheless, population is
  still expected to increase significantly, with the mix of foreign to local residents potentially reaching around 38%
  by 2030."

## Routes tried for the wording and the sources behind it (6 Oct 2026)

| Route | Result |
|---|---|
| Finance Malta, `financemalta.org/industry-updates/malta-s-rapid-population-growth-creates-urgent-need-to-focus-on-the-country-s-infrastructure-demands-for-the-future` (found on review; the coordinator's route) | 200 with curl and a browser User-Agent; read in full; dated 17 July 2026 ("Industry Update / PwC"); identical release text, with PwC's boilerplate. The earliest copy found, so the claim date is 17 Jul 2026. |
| Claim record URL (MBW post 29055), curl with browser User-Agent | 200; read in full; does **not** contain the claim (see above). Wayback lists a capture of 20 Jan 2026; web.archive.org refused connections from this network. |
| MBW WordPress API `/wp-json/wp/v2/posts?search=` ("38%", "foreign residents", "31% population", "2030 foreign", "foreigners population") | Found post 30680 (19 Jul 2026), which carries the claim verbatim. Read via the API and the HTML page. Wayback lists a capture of 10 Aug 2026 (not openable from here). |
| WebSearch for the statement | Found the PwC press room page and report page (both 403), Malta Chamber copy (22 Jul 2026, readable), Mondaq copy (23 Jul 2026, readable), Business Now (15 Jul 2026, readable), Newsbook (17 Jul 2026, readable), maltabusiness.it (18 Jul 2026, readable), The Malta Independent (17 Jul 2026, 403). |
| PwC Malta's own site: report page `pwc.com/mt/en/publications/economic-outlook/economic-outlook-summer-2026.html` and press room page | 403 to curl and to the WebFetch tool; Internet Archive availability API: no capture. **The report was not read.** |
| NSO World Population Day release (NR 120/2026, 9 Jul 2026), `nso.gov.mt/world-population-day-11-july-2026/` and its WordPress API | 403 (curl, WebFetch). Wayback lists a capture of 26 Sep 2026; web.archive.org refused connections. Figures taken from Newsbook, Lovin Malta, International Adviser and MEETinc (second-hand, ◆). |
| Central Bank of Malta Policy Note 1/2025 (centralbankmalta.org PDF; SSRN) | 403 (CBM, curl and WebFetch); SSRN Cloudflare challenge. Wayback capture of 16 Jun 2025 listed, not openable. Abstract read via Crossref (doi:10.2139/ssrn.5356748). |
| Eurostat dissemination API | Works: migr_pop1ctz, migr_pop3ctb, demo_gind, proj_25np, cens_21ctz_r3, cens_21cob_r3, migr_imm1ctz, migr_emi1ctz, migr_acq, demo_faczc, demo_maczc. |
| Jobsplus `labour-market-trends` pages and workbooks | Readable with curl and a browser User-Agent (Python urllib gets 403). |
| Identity Malta | Home page readable; no statistics used. |
