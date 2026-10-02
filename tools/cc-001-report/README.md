# Claim Check 001: report and flyer generators

These scripts regenerate the CC-001 report (`report.pdf`) and flyer (`flyer.pdf`) exactly as committed.

```
pip install reportlab matplotlib pillow
# Linux: the scripts expect the Liberation fonts (package fonts-liberation) in /usr/share/fonts/truetype/liberation/
python figures.py        # three figures -> out/
python build_report.py   # out/report.pdf
python build_flyer.py    # out/flyer.pdf
```

To reuse the design for a new check, copy this folder to `tools/cc-NNN-report/` and replace the text blocks.
The design tokens (palette, fonts, verdict scale) are documented in `PROJECT_STATE.md`.
