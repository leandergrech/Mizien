# CC-081: Landfill share rising

**Status:** BLOCKED on verbatim wording (5 Oct 2026). No report built.

## What is missing
The text of The Shift News article of 19 Feb 2026 (https://theshiftnews.com/2026/02/19/maltas-waste-management-is-going-in-reverse/). The page returns HTTP 404 to our fetches (direct, WebFetch, wp-json slug and search routes); Wayback has no copy. A web search lists the page and summarises it, but that summary is not verbatim and cannot be quoted. Maintainer: please paste the article text (or a saved copy) into `literature/CC-081/primary-source.md`.

## Routes tried
Direct URL (404); Wayback `web/2026/` and `id_/` (not archived); WordPress `wp-json/wp/v2/posts?slug=` and `?search=` (empty); site search `?s=` (no hit); WebFetch (404); web search (summary only, second-hand).

## Leads (the numbers appear to reproduce)
- Per the web-search summary of the NSO "Municipal Waste 2024" release (https://nso.gov.mt/municipal-waste-2024/, 403 to us, so second-hand): "79.2 per cent of treated municipal waste was landfilled, up from 78.6 per cent" in 2023; treated waste 322,119 t in 2024 (+3.1%). The Independent (17 Feb 2026) covers the related solid-waste release (403 to us).
- Eurostat env_wasmun (data/cc-111/, retrieved 5 Oct 2026): landfilled / treated = 78.6% (2023) and 79.2% (2024); landfilled / generated = 73.6% and 72.1%. So the figures match on the share-of-treated basis; the share of generated waste fell.
- Newsbook, 2 Dec 2025 (https://newsbook.com.mt/en/malta-hits-record-353000-tonnes-of-waste-as-landfills-struggle-to-keep-pace/): landfilled 255,107 t. 255,107 / 322,119 = 79.2% of treated, but Newsbook labels "72%" as the share of treated waste (72% is the share of the 353,525 t generated).
- Open questions for the report: the 0.6-point rise is small; the claim headline "in reverse" rests on basis choice (treated vs generated) and on one year. Cross-check CC-004 and CC-111.
