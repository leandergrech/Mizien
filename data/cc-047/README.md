# CC-047 data

- `commission_nitrates_malta_2020_2023.csv`: figures transcribed by hand from the European Commission staff working
  document SWD(2026) 232 final, Part 20/27 (Malta country fiche, Nitrates Directive reports 2020-2023), section 4,
  as transmitted to the Council on 15 July 2026 (Council doc. 12018/26 ADD 19,
  https://data.consilium.europa.eu/doc/document/ST-12018-2026-ADD-19/en/pdf). Retrieved 5 October 2026.
  Averages of annual means per monitoring point, 2020-2023; 44 points, sampled every six months by the Energy and Water Agency.
- `study_ranges.csv`: nitrate ranges as reported in the Laudi et al. study (second-hand, via MaltaToday's quotation) and
  in the same team's EGU 2025 abstract (doi:10.5194/egusphere-egu25-13344, read via Crossref). The full text of
  Laudi et al. (2026), doi:10.1016/j.ejrh.2026.103162, was not retrievable by script (ScienceDirect 403; Elsevier API
  needs a key); the 100-200 mg/L sentence is therefore second-hand.
- `checks.csv`: output of `tools/cc-047-report/calc.py`.
