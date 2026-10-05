# CC-025 literature notes

Access: F = full text, A = abstract or summary only, S = second-hand. Searches run 5 October 2026 (Crossref, OpenAlex, Eurostat API).

| Key | Source | Access | Finding used | Grade |
|---|---|---|---|---|
| malta_cop30_2025 | Government of Malta, COP30 national statement, Nov 2025 | F (quoted paragraph only, supplied) | The claim: per capita -44%+ and per unit of GDP -80%+ vs 2005; "decoupling growth from emissions". | (claim) |
| eurostat env_air_gge, nama_10_gdp, nama_10_pe | Eurostat | F (data) | Per person -46% (2023) / -48.5% (2024). Per unit of GDP: -70% / -72% in chain-linked volumes (2020 prices), -82% / -84% at current prices. Real GDP +161%, total GHG -27%, GDP deflator +72%. No status flags on the Malta values used. EU-27: -34/-36% per person; -46/-48% (volumes) and -62/-65% (current prices) per unit of GDP. | C |
| haberl2020 | Haberl et al. 2020, ERL | A | Absolute vs relative decoupling; absolute long-term decoupling rare. Context only. | C |
| CC-003 | Miżien claim check | F | Per-person figure, population share (about half), 2030 projection. Reused, not repeated. | C |

## Gaps

- The rest of the COP30 statement was not read; the UNFCCC file returned a bot-check page to our automated download.
- The statement gives no year, scope or GDP basis. The Climate Action Authority's 81.6% (EU 61.9%) is close to our current-price result for 2023 (-81.9%, EU -62.2%); this suggests the same basis but neither source says so.
- No Eurostat table of "GHG intensity of GDP" was reachable through the API (sdg_13_20 and env_ac_aigg returned not available), so the ratio is our own calculation from the three source tables.
- No Malta-specific peer-reviewed decomposition of emissions was searched for again; see literature/CC-003/notes.md.
