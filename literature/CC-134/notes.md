# CC-134 notes

- **Wording:** Commission 2026 Country Report for Malta (SWD(2026) 218 final), Council register copy ST-10135-2026-ADD-1
  (126 pp.), read 25-26 Oct 2026 (text extracted with pdftotext). The sentence on environmental tax revenue is on PDF p. 44
  (circular economy section of Annex 10); Annex 3 (taxation) table, with 'Environmental taxes (% of GDP)': Malta 2.4 / 1.6 / 1.5 / 1.4 and EU-27
  2.6 / 2.1 / 2.1 / 2.1 for 2019 / 2022 / 2023 / 2024, is on p. 77. Verbatim, quoted as printed (including the spacing in '0.18 %').
  Copyright: the Commission document is not committed (2.4 MB); the Council register URL is the reference.
- **Data:** Eurostat env_ac_tax (PC_GDP, MIO_EUR, PC_TSCO_X_ISCO; tax ENV, NRG, TRA, POL_RES; Malta, EU27_2020 and the 27
  states, 2015-2024; no status flags on Malta ENV 2022-2024) and nama_10_gdp (B1GQ, CP_MEUR), downloaded 26 Oct 2026 with
  `tools/cc-134-report/fetch.py`. Results in `data/cc-134/checks.csv`.
- **Findings:** 1.35% vs 2.08% (2024) match the Commission's 1.4 / 2.1 after rounding; Malta recomputed from EUR 312.5 m / EUR 23,079 m
  = 1.354%. Rank 25 of 27 (2023 and 2024). 2023 shares: energy 48.5%, transport 41.6% (Commission: around 49 and 41). The Commission's 0.18%
  for pollution and resources is Eurostat's 2022 value; 2023 is 0.15%, 2024 0.14%; EU 0.08% in all three years.
- **Search log (absence statements):** the statement that we did not test earlier Eurostat vintages: only the current vintage
  (updated 10 Feb 2026) was downloaded; the Eurostat Statistics Explained revision history was not searched. We cannot say whether the 0.18%
  comes from an earlier vintage.
- **Literature:** Turan, Esen and Yildirim (2026), DOI verified in Crossref; abstract via Crossref/OpenAlex (OECD panel, 27 economies, 1995-2023).
  Abstract only: used for context on what the measure shows, never as a finding on Malta. Eurostat ESMS: definition of environmental taxes.
- **Not read:** the Annex 3 sources behind the Commission's tax table (OECD, Taxation Trends); Malta's rates and the revenue by individual tax.
- **Gap:** why Malta's share fell from 2.38% (2019) to 1.35% (2024): the data do not say.
