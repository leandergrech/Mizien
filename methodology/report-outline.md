# Report outline (copy for a new check)

1. **Cover**: the exact claim, speaker, outlet, date and the verdict badge.
2. **TL;DR**: five points, the verdict meter, what would move the verdict up or down.
3. **The claim and what we could verify**: a table of sources and our access to each. A fairness note.
4. **Method**: question, evidence sought, grades, scale.
5. **Mechanism or background**: how the claimed effect could work, with one figure.
6. **What the studies found**: evidence map plus a table with grades.
7. **Where the science disagrees**: for each dispute, evidence of harm, evidence of little or no harm, why they differ, what it means here.
8. **Testing the claim**: sub-claims with ratings; the speaker's own reasoning checked.
9. **Verdict and requests for evidence**, plus right of reply.
10. **Limitations**, **References**, **Appendices** (scale and standards; revision log).

Design tokens and generators are in `tools/cc-001-report/` and `PROJECT_STATE.md`.

**Web version.** Each claim page carries the full report as HTML, made by `tools/report_html.py` from the same
content as the PDF (the build script's story) with the figures taken from the published `report.pdf`, and then the
downloads (report PDF, flyer PDF, flyer image). CI regenerates it on every build; it is not committed. Build with
the helpers in `tools/mizien_report.py` so the web version gets the same structure (key points, tables, contested
questions); `python tools/report_html.py CC-NNN` reports the share of the PDF's words present (it must be "ok").
