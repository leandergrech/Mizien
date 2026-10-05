# Data for CC-042 ("From Blue Flag to Red Alert")

Retrieved 5 October 2026. The Environmental Health Directorate (environmentalhealth.gov.mt) refuses automated
access (HTTP 403) and its closure-report PDFs are not in the Internet Archive, so the closure events below were
read from the news outlets that reproduce its notices, not from the PDFs themselves.

- `events_2025.csv`: the closure and Blue Flag events with dates, cause, source and how we read it.
- `eea_mt_classification.csv`: Malta's 87 bathing waters by EEA class, 2023-2025, and Fajtata (site A07) by year.
  Derived by `tools/cc-042-report/calc.py` from `data/cc-005/mt_site_classes.csv` (EEA DiscoMap
  BathingWater_Dyna_WM_2025 layer 3, retrieved 5 Oct 2026) and `data/cc-005/eea_bwd_mt_seasons.csv`
  (EEA DiscoData, WISE Bathing Water Directive; short-term pollution samples 2022-2024).
- `src/pn-facts-seawater.html`: copy of the PN's "Factcheck: Sea Water Quality" page (a partisan compilation; used only
  as a lead to the EHD report URLs, not as evidence).
