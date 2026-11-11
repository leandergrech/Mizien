# CC-156 sources and routes

Checked 11 November 2026 (worker B).

- Claim wording: Business Now, 17 Aug 2026. The subtitle (outlet's own voice) was returned exactly by a summarising fetch tool; the body was only summarised, so the week-13 figures (56 excellent, 30 good, 1 sufficient; 3-9 Aug) are second-hand.
- Data: EEA DiscoMap `BathingWater_Dyna_WM_2025` layer 3, all EU-27 states, via `tools/cc-156-report/fetch_data.py` -> `data/cc-156/country_excellent_share.csv`. DiscoData SQL returned 403 on this run, so only the map service was used; Malta's counts equal Claim Check 005's (which cross-checked them against DiscoData).
- Pooled EU coastal share 2016 here is 88.9% (waters with a class); CC-005 gives 87.8% (all identified waters). 2025 agrees (88.3%).
- Not obtained: Environmental Health Directorate weekly files (`environmentalhealth.gov.mt/wp-content/uploads/2026/08/Site-Classification-Week-12.pdf`, `-13`): 403 to curl and WebFetch. Wayback resets. So the week-13 figure is untested.
- No absence claims are made.
