# CC-107 literature notes: a net-zero Gozo by 2040 (PN programme 2026)

Split from CC-011 on 5 October 2026 (the analysis first appeared there as pledge 2, v1.0 2 Oct and v1.1 5 Oct 2026).
Access: F = full text, A = abstract or summary only, S = second-hand.

| Key | Source | Access | Finding used | Grade |
|---|---|---|---|---|
| pn_programme_2026_gozo | PN programme, Gozo chapter | F | A "clear and realistic plan" for Gozo to be a Net-Zero Island by 2040, emissions "reduced or offset" by solar, EVs, building efficiency, restoration, afforestation and more. No baseline, boundary or pathway. | (claim) |
| euislands2023gozo | Vaz and Rodrigues de Almeida 2023, Energy Baseline Scenario for Gozo (EU islands secretariat) | F | Energy-related CO2 2016-2020: 147,162 / 129,022 / 123,627 / 153,997 / 118,333 t (Table 16); transport 60-70% of energy use. Not official statistics; energy only. | C |
| grunzweig2007 | Grünzweig et al. 2007 | F (open access, committed) | Measured semi-arid afforestation sequestration of about 3.6 t CO2/ha/yr over 35 years. | B |
| yosef2018 | Yosef et al. 2018 | A (PDF committed, open access) | Context: semi-arid afforestation sequesters at continental scale. | C |
| eurostat_demo_r_pjanaggr3 | Eurostat, Gozo and Comino population | data | 41,253 on 1 January 2025. | C |
| ec_islands_malta | EC Clean energy for EU islands: Malta | F | Gozo area 67 km2 (all land). | C |

## Our own analysis (data/cc-107/)

- `gozo_net_zero_arithmetic.csv` (tools/cc-107-report/gozo_calc.py): forest area needed to offset Gozo's emissions,
  for population-based estimates (2.5 / 3.81 / 5.0 t per person; central 157,174 t) and for the 2023 energy
  baseline's lowest and highest years (118,333 t in 2020, 153,997 t in 2019). At the measured Yatir rate
  (3.62 t CO2/ha/yr) the baseline needs 4.9-6.3 times Gozo's 67 km2; the wider range is 1.5-8.5 times.

## Gaps

- No official greenhouse-gas inventory for Gozo. The 2023 energy baseline covers energy use only (electricity,
  transport on the island, ferries, heating and cooling) and attributes grid electricity with conversion factors;
  it is a study for the EU islands secretariat, not official statistics.
- No Malta-specific afforestation sequestration measurements found; Yatir (Israel, about 300 mm rain a year per
  Yosef et al. 2018) is the measured analogue. Maltese soils are thinner; rainfall is higher.
- The news reports (MaltaToday, May 2026) paraphrase the PN pledge as "net-zero through afforestation"; the
  programme lists afforestation as one of several measures.
- "The first island in the Mediterranean" was not tested.
