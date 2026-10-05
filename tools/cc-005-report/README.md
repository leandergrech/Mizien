# Claim Check 005 report and flyer

Uses the shared design in `tools/mizien_report.py`, matching the reports and flyers for CC-003, CC-004 and CC-011.

```sh
python fetch_data.py     # EEA bathing-water map service and DiscoData (network) -> data/cc-005/mt_site_classes.csv,
                         #   data/cc-005/excellent_share.csv
python figures.py        # out/fig1_share.png, out/fig2_map.png, out/fig3_sites.png (offline; Malta outline from
                         #   docs/data/geo.json)
python build_report.py   # out/report.pdf
python build_flyer.py    # out/flyer.pdf and out/flyer.png
```

Copy the three outputs to `claims/CC-005/`. The site builder publishes those files with paired **Open** and **Download** actions from the claim panel. `claims/CC-005/report.md` is the editable text source.
