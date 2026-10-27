# CC-143 data

- `document_facts.csv`: figures transcribed by hand from the Commission staff working documents SWD(2026) 702 final
  (Malta, 2 Oct 2026; copy on parlament.gv.at, downloaded 27 Oct 2026) and SWD(2019) 48 final (Malta, 26 Feb 2019; Cellar
  PDF, downloaded 27 Oct 2026), each with the PDF page (SWD(2026): printed page = PDF page - 1).
- Re-used, not copied: `data/cc-101/wise_2022_groundwater_status.csv` (EEA WISE WFD 2022 reporting, status of each of the
  15 groundwater bodies, retrieved 6 Oct 2026) and `data/cc-101/eurostat_env_wat_abs.csv` (Eurostat env_wat_abs, Malta,
  retrieved 6 Oct 2026). The WISE server was in maintenance on 27 Oct 2026, so the second-cycle (2016 reporting) status per
  body could not be fetched.
- `checks.csv`: output of `tools/cc-143-report/calc.py`.
