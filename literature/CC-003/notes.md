# CC-003 literature notes

Access: F = full text, A = abstract or summary only, S = second-hand (known through another source).
Searches run 2 October 2026 (Crossref, OpenAlex, Commission and Eurostat sites).

| Key | Source | Access | Finding used | Grade |
|---|---|---|---|---|
| caa_pr_2025 | Climate Action Authority press release, 13 Nov 2025 | F (Wayback copy) | The claim: per-capita emissions down 44% since 2005 vs EU 34%; "reducing emissions both at household level and across the economy". Does not mention the 2030 ESR projection. | (claim) |
| ec_capr2025_swd | Commission SWD, Climate Action Progress Report 2025 | F (Malta passages) | ESR emissions +41% vs 2005 in 2024; 2030 projection +42% (WEM) / +30% (WAM) vs a -19% target; gaps of 61 and 49 points, largest in the EU in percentage-point terms (in tonnes Germany's 2030 shortfall, 64 Mt, is far larger than Malta's 0.5 Mt). EU-27: -31% (WEM) / -38% (WAM) vs -40%. EU industrial emissions -36% 2005-2023. Industry (F-gases) +293% 2005-2023; buildings +12%; domestic transport up 45-90% band. | C |
| ec_capr2025_swd (v1.2) | Same SWD, Tables 25-26 | F (Malta, EU rows) | Table 25 (printed p. 114): Malta's yearly ESR limits vs 2005 are +102% (2021), +21%, +16%, +11% (2022-24), -19% (2030); emissions +30%, +43%, +42%, +41%; distance 73, -22, -25, -30 pp (Commission's own rounding: 42-16 = 26 but table says 25). Table 26 (p. 125): allocations 2.1, 1.2, 1.2, 1.1 Mt; emissions 1.3, 1.5, 1.4, 1.4 Mt; cumulative balance 0.7, 0.5, 0.3, 0.0 (2024), -0.4 (2025) ... -2.1 Mt (2030); 2005 base 1.0 Mt; ETS flexibility 0.5 Mt; LULUCF flexibility 0.0. Note p. 116: AEAs 2026-30 estimated; 2024-30 emissions from WAM projections; balance ignores cancellations and transfers. First compliance check 2027 for 2021-25 (p. 111). Typed into data/cc-003/capr2025_esr_malta.csv; checked against pdftotext of the PDF (reviewer's copy, created 6 Nov 2025). | C |
| ec_capr2025_ch3 | Commission web chapter 3 | F (relevant passages) | Germany, Ireland and Malta show the largest projected gaps in 2030 before flexibilities. | C |
| eurostat_env_air_gge, nama_10_pe | Eurostat | F (data) | Reproduces the per-capita fall (-46% 2005-2023, -48% to 2024; EU -34% / -36%). Absolute fall -27% (EU -33.5%). Population +41%. About half the per-capita fall is population growth. | C |
| eurostat_nrg_ind_ren | Eurostat | F (data) | Renewables 10.7% of electricity in 2024 (EU 47.5%); 17.2% of gross final energy. | C |
| camilleri2024 | Camilleri, Attard, Hickman 2024 | A | Malta: high car dependency and difficulty transitioning to sustainable mobility; backcasting policy packages. Context only. | C |
| warren2010 | Warren and Enoch 2010 | A | Car ownership growth on islands drives emissions; Malta among four case studies. Context only. | C |
| ehrlich1971 | Ehrlich and Holdren 1971 | S | Identity: impact = population x per-capita impact. Used for the decomposition logic only. | - |

## v1.2 additions (5 Oct 2026)

- EU-27 ranking (data/cc-003/eurostat_ghg_pop_eu27.csv, tools/cc-003-report/fetch_eu27.py): env_air_gge TOTX4_MEMO
  and nama_10_pe POP_NC for all 27 Member States, 2005 and 2024. Malta 3rd of 27 on the per-person cut (-48.5%;
  behind LU -60.4%, DK -51.3%) and 20th on the total cut (-27.4%). Largest drop between the rankings: MT 17 places,
  IE 12, CY 7. 2024 population flagged p (provisional) for BE, CY, DE, EL, ES, FR, HR, NL; no flags on Malta.
- ESR proxy: national total (TOTX4_MEMO) minus power generation (CRF1A1). Our estimate, not an official series.
  2005: 1.010 Mt (Commission base 1.0 Mt). Changes to 2021-2024: +30.9, +44.4, +39.4, +41.9% vs the Commission's
  +30, +43, +42, +41% (within 3 points). Per person: 2.50 t (2005), 2.52 t (2024). EU-27 ESR per person about
  -23% (Commission -20% with Eurostat population +3.9%).

## Gaps

- No peer-reviewed study found that decomposes Malta's emissions since 2005 into population, affluence and
  intensity effects. Our decomposition is a simple two-factor log split (tools/cc-003-report/calc.py).
- The Commission's exact per-capita series behind 44% / 34% is not published as a table; our Eurostat
  reproduction uses the 2026 inventory and differs by a few points (revisions). Direction and gap agree.
- Climate Action Authority factsheet (June 2026) could not be read: the gov.mt network blocks automated access
  and no archived copy exists. Archive by hand.
- The Commission SWD (capr2025_swd_en.pdf, 3.7 MB) is EU-licensed open access (Decision 2011/833/EU) but is not
  committed; the Commission site may show a bot check. Archive by hand if needed.
