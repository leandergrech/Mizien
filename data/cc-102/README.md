# CC-102 data

- `ombudsman_sustained_cases.csv`: typed from Table 1.3 (sustained cases closed, by office and outcome) of the Ombudsman's
  annual reports 2023, 2024 and 2025, and Table 1.22 (reports sent to Parliament) of the 2025 report. Retrieved 5 Oct 2026
  from ombudsman.org.mt (URLs in `data/sources.csv`). Every row adds up to its sustained-case count.
- `rates.csv`: written by `tools/cc-102-report/calc.py`: not-implemented rates on two denominators, pooled 2023-2025, and the
  Commissioner's own end-of-2025 count (5 of 12 still open).
