# CC-003 literature notes

Access: F = full text, A = abstract or summary only, S = second-hand (known through another source).
Searches run 2 October 2026 (Crossref, OpenAlex, Commission and Eurostat sites).

| Key | Source | Access | Finding used | Grade |
|---|---|---|---|---|
| caa_pr_2025 | Climate Action Authority press release, 13 Nov 2025 | F (Wayback copy) | The claim: per-capita emissions down 44% since 2005 vs EU 34%; "reducing emissions both at household level and across the economy". Does not mention the 2030 ESR projection. | (claim) |
| ec_capr2025_swd | Commission SWD, Climate Action Progress Report 2025 | F (Malta passages) | ESR emissions +41% vs 2005 in 2024; 2030 projection +42% (WEM) / +30% (WAM) vs a -19% target; gaps of 61 and 49 points, largest in the EU in percentage-point terms (in tonnes Germany's 2030 shortfall, 64 Mt, is far larger than Malta's 0.5 Mt). EU-27: -31% (WEM) / -38% (WAM) vs -40%. EU industrial emissions -36% 2005-2023. Industry (F-gases) +293% 2005-2023; buildings +12%; domestic transport up 45-90% band. | C |
| ec_capr2025_ch3 | Commission web chapter 3 | F (relevant passages) | Germany, Ireland and Malta show the largest projected gaps in 2030 before flexibilities. | C |
| eurostat_env_air_gge, nama_10_pe | Eurostat | F (data) | Reproduces the per-capita fall (-46% 2005-2023, -48% to 2024; EU -34% / -36%). Absolute fall -27% (EU -33.5%). Population +41%. About half the per-capita fall is population growth. | C |
| eurostat_nrg_ind_ren | Eurostat | F (data) | Renewables 10.7% of electricity in 2024 (EU 47.5%); 17.2% of gross final energy. | C |
| camilleri2024 | Camilleri, Attard, Hickman 2024 | A | Malta: high car dependency and difficulty transitioning to sustainable mobility; backcasting policy packages. Context only. | C |
| warren2010 | Warren and Enoch 2010 | A | Car ownership growth on islands drives emissions; Malta among four case studies. Context only. | C |
| ehrlich1971 | Ehrlich and Holdren 1971 | S | Identity: impact = population x per-capita impact. Used for the decomposition logic only. | - |

## Gaps

- No peer-reviewed study found that decomposes Malta's emissions since 2005 into population, affluence and
  intensity effects. Our decomposition is a simple two-factor log split (tools/cc-003-report/calc.py).
- The Commission's exact per-capita series behind 44% / 34% is not published as a table; our Eurostat
  reproduction uses the 2026 inventory and differs by a few points (revisions). Direction and gap agree.
- Climate Action Authority factsheet (June 2026) could not be read: the gov.mt network blocks automated access
  and no archived copy exists. Archive by hand.
