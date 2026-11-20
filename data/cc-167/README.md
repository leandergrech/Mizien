# CC-167 data

`eurostat_malta_energy_gdp.csv`, Malta 2015-2024, retrieved from the Eurostat API on 17 Nov 2026:
- gross available energy (GAE), international maritime bunkers, gross inland consumption (GIC) and final energy
  consumption (energy use), ktoe: `nrg_bal_s`, all products (updated 2 Jun 2026);
- GDP, chain-linked volumes (2010), EUR million: `nama_10_gdp` B1GQ CLV10_MEUR (updated 11 Nov 2026);
- average population: `demo_gind` AVG (updated 27 Oct 2026);
- energy intensity of GDP, chain-linked volumes (2010), kgoe per thousand euro, Malta and EU-27: `nrg_ind_ei`
  EI_GDP_CLV10 (updated 21 Apr 2026). Eurostat's indicator is GAE divided by GDP, so it includes bunkers.

The intensity table uses an older GDP vintage than `nama_10_gdp` (its 2024 value implies GDP about 3.5% higher), so
ratios computed here from current GDP differ slightly from the published indicator. `checks.csv` is written by
`tools/cc-167-report/calc.py`.
