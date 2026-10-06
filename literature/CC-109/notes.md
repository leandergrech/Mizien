# CC-109 literature and data notes

Access: F = full text, A = abstract or summary only, S = second-hand (known through another source).
All work done 6 October 2026 (maintainer session). Searches: Crossref (bibliographic queries "Malta road transport
emissions", "Malta transport CO2 emissions car", "Malta car ownership congestion transport policy", "approximated
greenhouse gas inventory proxy estimates accuracy EU member states"); OpenAlex refused the session (shared daily budget
exhausted, HTTP 429), so abstracts were not taken from it; EEA catalogue (sdi.eea.europa.eu search API, titles
containing "Effort Sharing Legislation", "approximated", "National emissions reported"); Eurostat table of contents
(no effort-sharing dataset); Commission country pages (DG ECFIN, DG CLIMA).

| Key | Source | Access | Finding used | Grade |
|---|---|---|---|---|
| ec2026countryreportmt | Commission, 2026 Country Report - Malta, SWD(2026) 218 (3 Jun 2026) | F (both copies) | The claim (Annex 8, p. 66) and the same figures on pp. 6 and 14; Graph 3.1 (p. 14); footnote (140) on scope and approximated data; Table A8.1 (p. 71). | (claim) |
| eea_esr_2005_2024 | EEA, GHG emissions under the Effort Sharing Legislation, 2005-2024 | F (data) | Malta ESR totals: 1.0074 Mt (2005, EEA estimate), 1.4450 (2023, ESR review), 1.4374 Mt (2024, approximated inventory). Totals only. | C |
| eea_approx_2024 | EEA, approximated GHG inventory 2024 | F (data) | Malta 2024: 1.A.3 total 0.767 Mt; non-ETS 1.A.3 0.761 Mt (total minus domestic-aviation CO2); ESR total 1.437 Mt; ETS 0.736 Mt; buildings (1.A.4) 0.132, agriculture 0.071, waste 0.192 Mt; small industry (residual) 0.281 Mt. Transport 52.9% of ESR. | C |
| eurostat_env_air_gge / eea_govreg_2026v1 | Eurostat env_air_gge (2 Jun 2026) = EEA GovReg 2026 v1.0 (data of 15 Mar 2026) | F (data) | Malta 1.A.3 0.5300 (2005) and 0.7877 Mt (2024); aviation CO2 0.0019 and 0.0041; road 0.4953 and 0.6902; domestic navigation 0.0328 and 0.0933; rail and other not occurring. ESR transport +48.4% 2005-2024; road +39.4%; navigation +184%. No Eurostat flags on these rows. | C |
| graph31 (in ec2026countryreportmt) | The report's Graph 3.1, read from the PDF's vector paths | F | Transport 0.528 Mt of 1.016 (2005, 51.9%), 0.765 of 1.448 (2023, 52.8%), 0.765 of 1.437 (2024, 53.3%). 2024 total equals the EEA approximated ESR total (1.437). Change 2005-2024 +45.0%. | C |
| ec_capr2025_profile_mt | Commission (DG CLIMA), CAPR 2025 country profile Malta (Jan 2026) | F | Figure 11 (p. 10): transport 53% of Malta's ESR emissions in 2024 (EU-27 39%), same definition (domestic transport excluding aviation CO2). | C |
| ec_capr2024_profile_mt | Commission (DG CLIMA), CAPR 2024 country profile Malta | F | 2023 (approximated): transport 52% of ESR emissions; transport -3.4% on 2022. The final inventory has +5.7%. | C |
| ec2025countryreportmt | Commission, 2025 Country Report - Malta, SWD(2025) 218 (4 Jun 2025) | F (passages) | 2023 approximated: road transport +32% since 2005 (text p. 67; Table A8.1 p. 69: 32.2). The 2026 report gives 44.8 for the same year from the final inventory. | C |
| reg2018_842, reg2023_857 | Effort Sharing Regulation and its 2023 amendment | F (Art. 2) | Scope: energy, IPPU, agriculture, waste, excluding ETS Annex I activities other than maritime transport; CO2 from 1.A.3.a civil aviation treated as zero. So ESR transport = all domestic transport (road, navigation, rail, other) minus aviation CO2. | C (law) |
| camilleri2024 | Camilleri, Attard and Hickman 2024, Sustainability 16:430 | F | Context: transport 35% of national CO2 and road 87% of transport CO2, citing Malta's Fourth Biennial Report (S, second-hand, year not stated in the passage); high car dependency (84.3% of trips by car, NSO 2021, S). Our 2024 road share of ESR transport: 88.1%. | C |

## How the 48% was investigated (6 Oct 2026)

1. Read every place the report gives the figure (pp. 6, 14, 66) and the source it points to: footnote (141) -> Table
   A8.1 (p. 71). Table A8.1 gives growth rates and the ESR total in Mt (1.0 in 2005, 1.4 in 2024), **no share**.
2. Read Graph 3.1, which the chapter-3 sentence cites, from its vector paths (`read_graph.py`): 53.3% in 2024. The
   Council copy draws the same graph (same extents to 0.01 pt).
3. Recomputed the share from the EEA approximated inventory (52.9%) and found the Commission's own CAPR 2025 Malta
   profile (DG CLIMA) printing 53% for the same year and definition.
4. Tried other definitions and denominators (`calc.py`): road only (1.A.3.b, 2026 inventory) over the approximated
   ESR total = **48.0%**; road only in 2023 over the reviewed ESR total = 47.5%; ESR transport over our estimate of the
   ESR total from the final 2026 inventory = 54.8%. Only the road-only ratio gives 48%. **This is our identification;
   the report does not state how 48% was computed, and we cannot confirm it.** The 45% in the same sentence is not a
   road-only figure (road only: +39.4%).
5. Not found: any EEA or Commission page giving 48% for Malta's transport share. The EEA greenhouse gas data viewer
   (named in Table A8.1's sources) draws its charts in JavaScript; we used the EEA's downloadable datasets behind it
   instead. Searched: the two country reports, the CAPR 2024 and 2025 Malta profiles, the EEA ESR dataset and the
   approximated-inventory workbook (all read in full for Malta), and a web search for "Malta transport share effort
   sharing emissions 2024 48%". Absence is stated only for these sources.

## Which series is Table A8.1's "domestic road transport" row?

It matches all domestic transport minus aviation CO2 (1.A.3 - CO2 1.A.3.a) in every year 2018-2023 to 0.1 points,
and road transport alone (1.A.3.b) only to within 6.2 points (2020: road +6.0% vs table +9.8%). So the label is
narrower than the data. Domestic navigation (CRF 1.A.3.d; the data used do not say which vessels, so the report
does not name any) was 6.2% of ESR transport in 2005 and 11.9% in 2024.

## Approximated versus final data

- The 2024 ESR total in the report (40.8% above 2005) and in Graph 3.1 (1.437 Mt) is the EEA's approximated
  inventory (published Nov 2025; Member States report approximated inventories by 31 July; EEA statistical metadata
  calls them "a preliminary indicator").
- The final national inventory for 2024 (due by 15 Mar 2026 under Regulation (EU) 2023/857 Art. 2(1); EEA compilation of 15 Mar 2026 published on 17 Apr 2026 and by Eurostat on
  2 Jun 2026) puts ESR transport at 0.784 Mt, 3.0% above the approximated 0.761 Mt: +48.4% since 2005 and, on our
  estimate of the ESR total, 54.8% of it. The final ESR figures for 2024 are set after the 2027 comprehensive review.
- Past approximations moved: for 2023 the 2025 report gave +32.2% (approximated), the 2026 report +44.8% (final).
- The 2005 base differs by source: the legal ESR value is 1,020,601 t (Commission Implementing Decision (EU) 2020/2126,
  Annex I; OJ L 426, 17.12.2020, p. 58; read via the Publications Office 6 Oct 2026), and the approximated 2024 total
  (1,437.4 kt) is +40.8% on it, the report's figure; the EEA's 2005 ESR estimate is 1.0074 Mt; Graph 3.1's 2005 bar
  sums to 1.016 Mt; Table A8.1 rounds to 1.0. The transport growth rate does not depend on it.
- Consistency with Claim Check 094 (checked in parallel, 6 Oct 2026): it gives the same 1,437.4 kt, +40.8% on
  1,020,601 t, and 2030 projections of +29.7% (with additional measures) and +42.1% (with existing measures), which are
  also the values in the 2026 report's Table A8.1 (p. 71). This check does not test the projections.

## Gaps

- No peer-reviewed study tests the Commission's share or growth figures; the claim is statistical and the evidence is
  official statistics (grade C).
- The EEA's own sector split of ESR emissions (behind the greenhouse gas data viewer and Graph 3.1) was not obtained
  as a table; Graph 3.1 was read from the PDF instead (reading error about 0.002 Mt, checked against the EEA total).
- Our ESR total for 2024 on the final inventory is an estimate (total excl. LULUCF minus ETS minus aviation CO2), not
  an official figure.
- UNFCCC CRT tables for Malta were not opened; the EEA GovReg compilation of the same submission was used.
