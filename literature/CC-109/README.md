# CC-109: EU: transport is 48% of effort-sharing emissions

**Status:** checked (report v1.0, 6 Oct 2026, maintainer session). Draft verdict: Largely supported (high confidence);
no right of reply needed.

## Primary source (the claim): routes tried for the verbatim wording (6 Oct 2026)

| Route | Result |
|---|---|
| Claim record URL: Council copy, `data.consilium.europa.eu/doc/document/ST-10135-2026-ADD-1/en/pdf` (curl, browser User-Agent) | **Read.** 126 pages, PDF created 8 Jun 2026; SHA-256 `684d13b1...a9cd4ba`. Council cover note (page 1), then SWD(2026) 218 final. Printed page = PDF page - 2. |
| The Commission's own copy, found on DG ECFIN's country page `economy-finance.ec.europa.eu/.../country-report-malta_en` ("2026 Country Report (including annexes) - Malta") | **Read.** 110 pages, PDF created 5 Jun 2026; SHA-256 `401cca4c...1905ac50`. Committed as `open-access/ec_swd_2026_218_country_report_malta.pdf` (Commission document; the PDF carries no licence notice; reuse under Decision 2011/833/EU and the Commission legal notice, CC BY 4.0 unless otherwise indicated). Same wording as the Council copy in every passage used; page numbers differ (below). |
| Wayback Machine (`web.archive.org/web/2026/<url>`, availability API) | Not reachable from this network on 6 Oct 2026 (connection reset; API 429). Not needed: both live copies read. Archive by hand. |
| WebSearch for the wording | Finds the Council PDF and the Austrian Parliament's copy of the same Council document (`parlament.gv.at/dokument/XXVIII/EU/76309/imfname_11628204.pdf`, not opened). |

### The wording and where it appears (Commission copy page; Council copy page)

- Annex 8, "Sustainable transport", p. 66 (Council p. 72), the recorded quote: "Transport is the dominant source of
  Malta's effort sharing emissions. It has generated 48% of these emissions in 2024 (141), up by 45% since 2005."
  Footnote (141): "See Table A8.1 at the end of this Annex."
- Chapter 3, p. 14 (Council p. 15): "In terms of Malta's effort sharing emissions, transport had a share of 48% in
  2024, with emissions up by 45% since 2005 (see Graph 3.1 and Annex 8)." This sentence settles that "45%" is the
  change in emissions, not in the share.
- Summary, p. 6 (Council p. 6): "The transport sector remains the biggest source of Effort Sharing Regulation emissions
  in 2024 (48%)".
- Graph 3.1, p. 14 (Council p. 16): "Greenhouse gas emissions in the effort sharing sectors, 2005, 2023, and 2024";
  categories "Domestic transport (excl. aviation)", "Buildings (under ESR)", "Agriculture", "Small industry", "Waste";
  "Source: European Environment Agency."
- Footnote (140), p. 66 (Council p. 72): the ESR "applies jointly to buildings (heating and cooling), road transport,
  agriculture, waste and small industry"; 2024 effort-sharing emissions "are based on approximated inventory data. The
  final data will be established in 2027 after a comprehensive review."
- Table A8.1, p. 71 (Council p. 77): row "- domestic road transport" 25.1, 32.8, 9.8, 17.7, 37.1, 44.8, 45.0
  (2018-2024; EU-27 -1.4 in 2018, -5.6 in 2023). Data source: "European Environment Agency, greenhouse gas data
  viewer; European Commission, Climate Action Progress Report, 2025." The table gives no share.

## Evidence

- EEA, Greenhouse gas emissions under the Effort Sharing Legislation, 2005-2024 (published 6 Nov 2025).
- EEA, GovReg: Approximated estimates for greenhouse gas emissions, 2024 (published 5 Nov 2025).
- Eurostat env_air_gge (2026 inventory submission; updated 2 Jun 2026) and the EEA GovReg 2026 v1.0 compilation it
  republishes (data of 15 Mar 2026).
- The report's own Graph 3.1, read from the PDF's vector paths (`tools/cc-109-report/read_graph.py`).
- Commission (DG CLIMA), Climate Action Progress Report 2025 country profile Malta (January 2026), Figure 11, and the
  CAPR 2024 profile; Commission 2025 Country Report - Malta (previous year's approximated figures).
- Regulation (EU) 2018/842, Article 2, as amended by Regulation (EU) 2023/857 (scope of effort sharing).
- Camilleri, Attard and Hickman (2024), context on Malta's transport emissions.

Data: `data/cc-109/`. Calculations: `tools/cc-109-report/calc.py` (outputs `data/cc-109/checks.csv`). See `notes.md`
and `references.bib`.
