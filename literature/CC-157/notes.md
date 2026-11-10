# CC-157: notes

**Claim (outlets' wording):** extreme heat could cut Malta's GDP by more than 2.5% in 2055–2064 if there is no further
adaptation or mitigation (Business Now, 18 Jul 2025, citing Euronews and García-León et al.).

## Sources and how they were read

| Source | Read how | Notes |
|---|---|---|
| García-León et al. 2021, *Nat. Commun.* 12:5807, doi:10.1038/s41467-021-26050-z (CC BY 4.0) | **Full text** (PDF, 10 Nov 2026) and Supplementary Information 1 (region list); Crossref and OpenAlex checked | Open-access PDFs committed under `open-access/`. Malta is not named in the text; it is a row in **Fig. 4b**. |
| Business Now, 18 Jul 2025 | Via WebFetch (summary by a fetch model; curl gets a Cloudflare page), 10 Nov 2026 | Outlet gives the 2.5% figure and the study; **not a raw copy**: mark as read-through-summary. |
| Euronews, 15 Jul 2025 (Servet Yanatma) | Via WebFetch (extracted quotation), 10 Nov 2026; curl refused (406) | Wording ◆ second-hand: "impacts reaching or exceeding -2.5% of GDP by the 2055–2064 period". Not used for the verdict. |

## What the paper says

- Method: heat-exposure functions (ISO WBGT) turn heat stress into labour-productivity losses, fed into a regional
  CGE model (GTAP-based); two regional climate models (MPI-CSC-REMO2, KNMI-RACMO) under RCP8.5, socio-economic
  structure held fixed. Losses are annual, as a share of GDP; boxes in Fig. 4 show the interannual spread.
- Europe aggregate: 0.21% (1981–2010) → 0.77% (2035–45) → 0.96% (2045–55) → "beyond 1.14%" in the 2060s.
- Countries: Cyprus, Portugal, Spain, Croatia "gradually move from … 2% in 2040 to around 3% in 2060"; Balkan countries,
  Italy and Greece more than 2% in 2055–64. Malta is not mentioned in the text.
- No adaptation: the model "does not consider the likely existence of adaptation and heat-insulation measures …
  such as air conditioning"; authors argue effects on outdoor sectors are not much dented by it.
- Mitigation: signals of the two climate models are "very similar, irrespectively of the emission scenario" for the
  next four decades; scenarios diverge after 2050. Results for the other scenario are in the Supplementary Discussion
  (not in the Supplementary Information file we have: it contains the region list only).
- Limits stated: no occupational-injury costs, no urban heat island, heat functions based on few empirical studies.

## Malta's value (calc.py)

Not tabulated. Measured from the Fig. 4b dot plot (image CC BY, `data/cc-157/fig4_source_image.png`): **about −2.8%**
in 2055–64 (pixel measurement, ±0.1 pp), 4th largest of 29 entries after Cyprus (−3.4%), Croatia, Portugal. Eyeball
agrees (dot between −2.5 and −3.0). See `data/cc-157/checks.csv`.

## Search log (absence statements)

- "No later paper": a later (2025) paper with a Malta figure was **not searched for exhaustively**; the Business Now
  and Euronews texts both point to this 2021 study (Euronews as read via WebFetch; Business Now names García-León).
  Searched: Crossref DOI check, the two articles. Not searched: Google Scholar/OpenAlex for follow-up papers.
- No Malta-specific uncertainty range is given in the paper (text and Supplementary Information file 1 searched for
  "Malta": one hit, the region list).

## Gaps

- Source data / country table not published (GTAP licence; "available from the authors upon reasonable request").
- Supplementary Discussion on RCP8.5-SSP5 vs other scenarios not read (not in the SI file obtained).
