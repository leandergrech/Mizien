# Claim Check 109: report and flyer generators

Uses the shared design in `tools/mizien_report.py`.

```
pip install reportlab matplotlib pillow pyyaml openpyxl pymupdf   # plus poppler-utils for the PNG
python fetch.py --govreg  # (network) Eurostat env_air_gge, EEA ESR emissions, EEA approximated inventory 2024,
                          # EEA GovReg 2026 v1.0 (Malta rows; 95 MB download) -> data/cc-109/
python read_graph.py      # (network) downloads both copies of the Commission report to out/ and reads Graph 3.1
                          # from the PDF's vector paths -> data/cc-109/graph31_bars.csv
python calc.py            # recompute every figure -> data/cc-109/checks.csv
python figures.py         # out/fig1_graph31.png, fig2_shares.png, fig3_change.png
python build_report.py    # out/report.pdf
python build_flyer.py     # out/flyer.pdf, out/flyer.png
```

Inputs: the CSVs written by `fetch.py` and `read_graph.py` (each row carries its source and retrieval date), and
`data/cc-109/commission_figures.csv`, typed from the Commission documents (2026 and 2025 Country Reports, CAPR 2024
and 2025 Malta profiles) with printed page numbers. `calc.py` also reads Claim Check 003's data
(`data/cc-003/eurostat_ghg_population.csv`, `capr2025_esr_malta.csv`) to check consistency.

Effort-sharing transport = greenhouse gases from CRF 1.A.3 minus CO2 from 1.A.3.a domestic aviation (Regulation (EU)
2018/842, Art. 2(3); Art. 2(1) as amended by Regulation (EU) 2023/857 keeps maritime transport in effort sharing).

Copy `out/report.pdf`, `flyer.pdf`, `flyer.png` to `claims/CC-109/`.
