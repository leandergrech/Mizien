# CC-012 literature notes

Access: F = full text, A = abstract, S = second-hand, M = metadata only. Searches 3 October 2026 (Crossref,
OpenAlex; Maltese news read in full with curl; Sentinel-2 via Planetary Computer).

| Key | Source | Access | Finding used | Grade |
|---|---|---|---|---|
| mt_2025_ministry | Public Works Ministry statement via MaltaToday | F (relay) | Material retains moisture; "natural grass grows at a much faster rate well before the rainfall of the winter season". | (claim) |
| mt_2025_scrutiny | MaltaToday, Nov 2025 | F | Micallef said grass would sprout with autumn and winter rains; by autumn it had not. | (claim, context) |
| shift_2026_pm | The Shift, 15 Jan 2026 | F | PM verbatim: intervention after the concerts from April. Ministry source: no spring concerts scheduled (S). | (claim) |
| mi_2026_momentum, mi_2026_pn_feb | Malta Independent, Feb 2026 | F (relay) | Momentum expert: compacted gravel under sand prevents germination; PN: "choking the grass", could "permanently" turn barren. | (claim) |
| copernicus_s2 | Sentinel-2 L2A | F (data) | Gravel zone (2.8 ha) winter median NDVI 0.53-0.67 in 2023-2025 (rest of the park 0.65-0.68), 0.15 in winter 2025-26 (rest of the park 0.68); still bright gravel at end Sep 2026 (zone reflectance 0.30 in Aug-Sep 2026, 0.19-0.21 in Aug-Sep 2023-24). Values from v1.1 (5 Oct 2026), after applying BOA_ADD_OFFSET -1000; v1.0 omitted it (0.37-0.47 and 0.11). | B |
| nawaz2013, batey2009 | Reviews | A | Compaction reduces infiltration and root penetration; amenity use causes compaction. | C |
| hyatt2007 | Experiment | A | Emergence falls with compaction (soybean). | A (indirect) |
| li2003 | Gravel-sand mulch | M | Gravel mulch is used to conserve soil water. Supports the Ministry's rationale in drylands farming; not tested for turf. | - |

## Gaps

- The Momentum expert report and the government's landscaping consultant's report were not seen.
- No soil samples; NDVI shows greenness, not soil condition, so "permanently barren" cannot be tested.
- Whether any works began after 27 September 2026 is unknown.
- The 2026 concert dates at the picnic area: no source found.

## Corrections

- v1.1 (5 Oct 2026): the Sentinel-2 L2A offset for processing baseline 04.00 and later (BOA_ADD_OFFSET -1000,
  confirmed in s2:processing_baseline and MTD_MSIL2A.xml) was missing in v1.0; all NDVI and brightness values were
  recomputed. No source was found for the 2026 concert dates (v1.0 named Summer Daze in August 2026); removed.
