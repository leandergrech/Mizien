# CC-009 literature notes

Access: F = full text, A = abstract or summary only, S = second-hand, N = not read. Checks run 5 October 2026 (v1.2).
Every DOI below was resolved on Crossref (`https://api.crossref.org/works/<doi>`); metadata in `references.bib`.

| Key | Source | Access | Finding used | Grade |
|---|---|---|---|---|
| stuart2010residence | Stuart et al. 2010, *Applied Geochemistry* 25(5):609-620, doi:10.1016/j.apgeochem.2009.12.010 | F (authors' accepted manuscript, NERC Open Research Archive eprint 9619; publisher version paywalled) | Saturated-zone travel times in the Malta Mean Sea Level aquifer 15-40 years (tritium, CFC/SF6); Gozo 25 to possibly more than 60 years; one perched aquifer about 15 years (abstract). Nitrate and other solutes held in the rock matrix move slowly, "providing a long-term source and sustained concentrations of nitrate"; the timescale of remedial measures depends on residence time (introduction, discussion). The sea-level aquifer's water table "is controlled by abstraction" and is up to only 3 m above sea level in places; abstraction leads to saline upconing (conceptual model; Figure 2 caption). | B |
| sapiano2020iwrm | Sapiano 2020, *Acque Sotterranee* 9(3):25-32, doi:10.7343/as-2020-477 | F (open access; copy in `open-access/`) | Groundwater is the only naturally renewable freshwater resource; the sea-level bodies are floating lenses "highly vulnerable to sea-water intrusion in response to abstraction activities" (p. 27). Long-term average groundwater abstraction about 40 Mm3 (p. 27). Table 1 (p. 28): renewable resources 65 (long-term) / 63 (2019) hm3; natural subsurface discharge 24 (assumed 50% of long-term recharge to the sea-level aquifers); unrecoverable runoff 4; actual available water resources 37 / 35; total abstraction 38 / 41; WEI+ 78% / 89%, against the 40% the EU treats as high water stress. Municipal-supply groundwater abstraction fell from about 21 Mm3 (early 1990s) to about 13 Mm3 (2019) (p. 30). Describes WSC's "Net-Zero Impact Water Utility" aim (p. 31). | C |
| mangion2008msl | Mangion and Sapiano 2008, in *Natural Groundwater Quality*, pp. 404-420, doi:10.1002/9781444300345.ch19 | N | Not read (closed access; no abstract available). Not cited for any finding. | - |

## Notes on use

- Sapiano (2020) is by an author at the Energy and Water Agency, the body responsible for national water policy, and
  was published in a workshop issue (accepted eight days after receipt). It is used for the published water balance
  and the hydrogeological description, not as an independent evaluation. We could not reproduce the WEI+ values (78%,
  89%) from the components printed in Table 1; they are cited as published.
- Sapiano's Table 1 uses the 2nd RBMP framework (long-term average and 2019). It is not the same method or period as
  Eurostat's env_wat_res recharge estimate (41.52 million m3 in 2024, flagged e), so the report shows the 37 million m3
  long-term estimate as a reference line only.
- Stuart et al. (2010) concerns residence times and nitrate; it says nothing about the 2025 WSC figures. It is used for
  one point: changes at the surface or in abstraction take years to decades to show in the sea-level aquifers' water
  quality, so one year's production data cannot show recovery.
- Lead not followed up: Lotti et al. 2021, Numerically enhanced conceptual modelling (NECoM) applied to the Malta Mean
  Sea Level Aquifer, *Hydrogeology Journal* 29:1517-1537, doi:10.1007/s10040-021-02330-2 (Crossref record checked;
  full text not reachable from scripts; not read, not cited).

## National data (v1.2)

Eurostat env_wat_abs (updated 2026-09-16) and env_wat_res (updated 2026-07-03), Malta, retrieved 5 October 2026, in
`data/cc-009/eurostat_water.csv` with flags (abstraction and recharge values flagged e, estimated; 2020 also b, break in
series; no public-supply value for 2021). 2024: total fresh groundwater abstraction 38.46 million m3; agriculture 21.77
(18.67 in 2023); public water supply 14.28; recharge into the aquifer 41.52. WSC's 2024-25 cut (1.553 million m3, chart
values) is 4.0% of the 2024 national total. Eurostat's public-supply abstraction exceeds WSC's groundwater production
by 0.86-1.19 million m3 in 2022-2024 (different measures; not explained by either source).

## Open-access copies

| File | Licence | SHA-256 |
|---|---|---|
| open-access/Sapiano-2020-Acque-Sotterranee-477.pdf | CC BY-NC-ND 4.0 (as printed in the PDF) | 67dfbaac3e01dbc6f60fdc92b5b36e3d2bd9a276babe9769ac4907412225e986 |
