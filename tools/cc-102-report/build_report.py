"""Claim Check 102 report. Run calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []

# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("Reporting on the Parliamentary Ombudsman’s 2025 annual report said that <b>58% of the Commissioner for "
        "Environment and Planning’s justified recommendations went unimplemented</b>, the highest rate of any "
        "commissioner, and that <b>22 reports were escalated to Parliament</b> [2]. We read the report itself [1] and "
        "recomputed the figures from its tables.", lead)]
S.append(key_points([
    ("The number is the Ombudsman’s own.",
     "Table 1.3 of the 2025 report [1]: of 12 sustained cases closed by the Commissioner, 7 recommendations "
     "(58%) were not implemented. The 22 reports sent to Parliament match Table 1.22."),
    ("It is a small count, and it moves a lot.",
     "7 of 12 is a 95% interval of roughly 32–81%. The same office had 6 of 13 (46%) in 2023 and 2 of 8 (25%) in "
     "2024. Over 2023–2025 it is 15 of 33 (45%)."),
    ("It is a snapshot at closure.",
     "The Commissioner’s own chapter says that five of the 12 were still unimplemented when the report was written; "
     "two more were implemented after being referred to the House. On that basis 42% remain open (counting "
     "the one “partly implemented” case of Table 1.3 as implemented)."),
    ("“Highest” holds on the Ombudsman’s table, not on every denominator.",
     "Environment and Planning 58% against Education 53% of sustained cases. Counting only cases where a "
     "recommendation was made, Education is 67% (8 of 12). The Commissioner’s remit is also wider than "
     "“environment”: planning, building, transport licensing and heritage."),
    ("Verdict: largely supported (high confidence).",
     "The figures match the primary source; the caveats above do not change the substance."),
]))
S += [Spacer(1, 4 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("7 of 12", GREEN, "Sustained cases with the recommendation not implemented, 2025 (58%)"),
             ("42%", AMBER, "Still unimplemented when the report was written (5 of 12; “partly” counted as implemented)"),
             ("45%", GREY, "Same office, 2023–2025 pooled (15 of 33)"),
             ("22", GREEN, "Reports sent to Parliament in 2025 (14 in 2023, 16 in 2024)")]),
      Spacer(1, 4 * mm),
      up_down("Case-level data for the 2025 cases showing a different count, or a final-opinion list in which "
              "fewer than seven recommendations were unimplemented at closure.",
              "A year-on-year series in which 2025 is not unusual, or authorities’ stated reasons showing that "
              "the recommendations were not accepted on legal grounds."),
      Spacer(1, 5 * mm)]
S += toc([("1", "The statement and the primary source"), ("2", "Method"), ("3", "What the 58% counts"),
          ("4", "Results"), ("5", "Testing the sub-claims"), ("6", "Verdict and requests for evidence"),
          ("7", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The statement and the primary source"))
S.append(P("Our candidate record took the figures from a Newsbook report of 2 July 2026 [2], which attributes them to "
           "the Parliamentary Ombudsman’s Annual Report for 2025. We read the report [1], published on the Office’s "
           "website. The Ombudsman’s wording is below. The newspaper’s phrase “justified recommendations” is a "
           "paraphrase of “sustained cases”."))
S.append(std_table([
    [C("Source", cellh), C("What it says", cellh), C("Our access", cellh), C("Status", cellh)],
    [C("<b>Office of the Ombudsman</b>, Annual Report 2025, p. 15 [1]"),
     C("“The Commissioner for Environment and Planning had 12 sustained cases, representing 15% of the total, of "
       "which 7 recommendations, or 58%, were not implemented.” Table 1.22 (p. 37): 22 reports sent to Parliament in "
       "2025."),
     C("Full text read (252 pages)."), C("<b>Primary</b>")],
    [C("<b>Newsbook</b>, 2 July 2026 [2]"),
     C("58% of the Commissioner for Environment and Planning’s justified recommendations “completely unimplemented”; "
       "22 reports escalated to Parliament."),
     C("Read in full."), C("Locator")],
], [36 * mm, 84 * mm, 30 * mm, 20 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("FAIRNESS NOTE", tag),
               P("The Ombudsman states the figure plainly and uses it to argue for a parliamentary committee to follow "
                 "up unimplemented reports. This check tests the numbers and how they are framed in reporting, not "
                 "the merits of any individual case, and does not assess the authorities named in the report. "
                 "Disagreement with a finding is a legitimate reason not to implement it; the report records "
                 "what was not implemented, not why.", small)], bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Question.</b> Do the Ombudsman’s tables support “58% unimplemented”, “highest among commissioners” and "
           "“22 reports escalated”, and how stable is the figure?"))
S.append(P("<b>Data.</b> We typed Table 1.3 (sustained cases closed, by office and outcome) from the 2023, 2024 and "
           "2025 annual reports [1, 3, 4] and Table 1.22 (reports sent to Parliament) from the 2025 report into "
           "<i>data/cc-102/ombudsman_sustained_cases.csv</i>, and checked that every row adds up. "
           "<i>tools/cc-102-report/calc.py</i> recomputes the rates on two denominators and checks the 2025 totals "
           "(81 sustained cases, 22 not implemented, 22 reports). Intervals are Wilson 95%."))
S.append(P("<b>Grades.</b> The Ombudsman’s annual reports are official institutional records (C). We have no access to "
           "the underlying case files; the case notes were not needed for the counts."))

# ================================================================== 3
S.append(CondPageBreak(60 * mm))
S.append(SectionHeading(3, "What the 58% counts"))
S.append(P("Table 1.3 counts <b>sustained cases closed during the year</b>, not complaints received and not individual "
           "recommendations: one case can carry several. “Not implemented” is the status when the case was closed. "
           "The Commissioner’s chapter [1, printed pp. 218–219; PDF pp. 219–220] gives the position later: of the 12 "
           "sustained cases, five recommendations were implemented, two more were implemented after referral to the "
           "House of Representatives, and five remained unimplemented (including the Planning Authority and the "
           "Transport Malta cases it lists). The two accounts reconcile only if the one “partly implemented” case is "
           "counted as implemented: Table 1.3 has 4 implemented + 1 partly = 5, which is the chapter’s five, and "
           "7 not implemented at closure = the chapter’s 2 implemented later + 5 still open. The 42% (5 of 12) "
           "depends on that reading. The Commissioner’s remit covers planning, building control, "
           "transport licensing and heritage as well as environmental matters; the Planning Authority alone accounts "
           "for 37 of 86 complaints in 2025 [1, Table 3.4]."))

# ================================================================== 4
S.append(PageBreak())
S.append(SectionHeading(4, "Results"))
S.append(fig(FIG / "fig1_rates.png"))
S.append(P("Figure 1. Left: share of the Commissioner for Environment and Planning’s sustained cases whose "
           "recommendation was not implemented. Right: 2025 rates by office on two denominators. "
           "Source: Office of the Ombudsman, annual reports 2023–2025, Tables 1.3 and 1.22 and the Commissioner’s "
           "2025 chapter; data in <i>data/cc-102/rates.csv</i>. *Five of the 12 were still unimplemented when the "
           "2025 report was written (“partly implemented” counted as implemented); two more were implemented after "
           "referral to the House.", cap))
S.append(std_table([
    [C("2025, by office", cellh), C("Sustained cases", cellh), C("Not implemented", cellh), C("% of sustained", cellh),
     C("% of cases with a recommendation", cellh)],
    [C("<b>Environment and Planning</b>"), C("12"), C("7"), C("<b>58%</b>"), C("58% (12)")],
    [C("Education"), C("15"), C("8"), C("53%"), C("<b>67%</b> (12)")],
    [C("Parliamentary Ombudsman"), C("17"), C("5"), C("29%"), C("31% (16)")],
    [C("Health"), C("37"), C("2"), C("5%"), C("12% (17)")],
    [C("All offices"), C("81"), C("22"), C("27%"), C("29% (76)")],
], [52 * mm, 26 * mm, 28 * mm, 28 * mm, 36 * mm]))
S.append(P("Source: Table 1.3 [1]; recomputed in <i>data/cc-102/rates.csv</i>. Cases with a recommendation = sustained "
           "cases minus those sustained with no recommendation.", cap))
S.append(callout([P("THE ARITHMETIC", tag),
                  P("7 ÷ 12 = 58.3%. The same ratio was 6 ÷ 13 = 46.2% in 2023 and 2 ÷ 8 = 25.0% in 2024; pooled, "
                    "15 ÷ 33 = 45.5%. With so few cases one case moves the rate by 8 points; the 95% interval for "
                    "7 of 12 is about 32–81%, and for 2024’s 2 of 8 about 7–59%. The year-to-year swing is "
                    "within what chance alone could produce, so we do not read 2025 as a proven trend. The Ombudsman’s "
                    "own series of reports to Parliament (Table 1.22) rises for the office as a whole, "
                    "14, 16 and 22, but not steadily for this Commissioner (5, 2, 7).", small)],
                 bg=BLUE_PALE, bar=BLUE))
S.append(Spacer(1, 3 * mm))
S.append(P("What this means for the statement", h2))
for t in ["• <b>The figure is correct as the Ombudsman states it.</b> Both the 58% and the 22 reports match the tables.",
          "• <b>“Highest” is true on the Ombudsman’s own basis</b> (58% against Education’s 53%), but the margin is one "
          "case’s worth and reverses if cases with no recommendation are excluded (Education 67%).",
          "• <b>“Went unimplemented” is a status at closure.</b> By the time the report was written two of the seven "
          "had been implemented, leaving five (42%).",
          "• <b>Newsbook’s “justified recommendations”</b> reads as a count of recommendations; the table counts "
          "sustained cases.",
          "• <b>The 22 reports</b> equals the total of not-implemented cases in Table 1.3, but the split by office "
          "differs in two places (Parliamentary Ombudsman 5 vs 4, Health 2 vs 3). Environment and Planning "
          "agrees at 7. We report this as a reconciliation point, not an error in the claim."]:
    S.append(P(t, bul))

# ================================================================== 5
S.append(CondPageBreak(80 * mm))
S.append(SectionHeading(5, "Testing the sub-claims"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> 58% of the Commissioner for Environment and Planning’s recommendations went unimplemented in 2025 "
       "(Table 1.3 counts the 12 sustained cases closed in 2025: 7 not implemented)"),
     C("Ombudsman [1]; Newsbook [2]"),
     C("7 of 12 sustained cases closed in 2025, status at closure (Table 1.3). Small count; 5 of 12 still open when the report was "
       "written."), verd("CONFIRMED", GREEN)],
    [C("<b>B.</b> The highest rate among the commissioners"), C("Newsbook [2] (its comparison, from the Ombudsman’s tables)"),
     C("58% against Education’s 53% of sustained cases; 67% for Education on cases with a recommendation."),
     verd("DEPENDS ON BASE", AMBER)],
    [C("<b>C.</b> 22 reports escalated to Parliament in 2025"), C("Ombudsman [1]; Newsbook [2]"),
     C("Table 1.22: 22, up from 16 (2024) and 14 (2023)."), verd("CONFIRMED", GREEN)],
], [46 * mm, 24 * mm, 66 * mm, 34 * mm], valign="MIDDLE"))

# ================================================================== 6
S += [Spacer(1, 6 * mm), SectionHeading(6, "Verdict and requests for evidence"),
      verdict_box("Largely supported", "The figures match the Ombudsman’s tables; the count is small and the "
                  "“highest” ranking depends on the base. Confidence: high."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> The 58% and the 22 reports are in the Ombudsman’s own report and recompute exactly. We rate the "
           "statement <i>Largely supported</i> rather than <i>Supported</i> because it is a snapshot of a very small "
           "count, two of the seven were implemented later, and “highest” is not robust to the choice of "
           "denominator. None of these changes the substance: a majority of this Commissioner’s sustained cases "
           "closed in 2025 without the recommendation being implemented."))
S.append(P("<b>What this verdict does not say.</b> It does not say the authorities were wrong not to act, or that the "
           "Commissioner’s findings were right in each case. It is not a judgement of any authority or person."))
S.append(CondPageBreak(45 * mm))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "From the Office of the Ombudsman: the list of the 12 sustained cases of 2025 with their status at closure.",
    "From the Office of the Ombudsman: how the per-office counts in Tables 1.3 and 1.22 reconcile.",
    "From the authorities concerned: the reasons given for not implementing the five open recommendations.",
]))

# ================================================================== 7
S += [CondPageBreak(45 * mm), Spacer(1, 6 * mm), SectionHeading(7, "Limitations")]
for l in ["Figures are typed from the published tables; we did not see case files. Counts are of cases, not of "
          "recommendations.",
          "Table 1.3 uses status at closure; later implementation is reported only in the Commissioner’s narrative.",
          "Cases closed in 2025 may have been opened in earlier years, so rates are not a measure of 2025 conduct alone.",
          "A rate on 8–13 cases a year cannot support a trend claim. We tested no individual case on its merits."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Office of the Ombudsman, Malta (2026). <i>Annual Report 2025</i>, Table 1.3 (pp. 15–16), Table 1.22 (p. 37), "
          "Commissioner for Environment and Planning chapter (pp. 214–220), Table 3.4. Page numbers are the printed ones "
          "(PDF page = printed page + 1). Presented to the Speaker "
          "of the House, June 2026. (Full text read.)",
     "https://ombudsman.org.mt/media/0ownfd4k/digital-annual-report-2025-en.pdf"),
    ("2", "Newsbook (2 July 2026). Public entities ignore Ombudsman as defiance reaches record high.",
     "https://newsbook.com.mt/en/public-entities-ignore-ombudsman-as-defiance-reaches-record-high/"),
    ("3", "Office of the Ombudsman, Malta (2025). <i>Annual Report 2024</i>, Table 1.3.",
     "https://ombudsman.org.mt/media/q4nbhpzv/annual-report-2024-ombudsman.pdf"),
    ("4", "Office of the Ombudsman, Malta (2024). <i>Annual Report 2023</i>, Table 1.3.",
     "https://ombudsman.org.mt/media/fr1ndd4u/annual-report-2023-en.pdf"),
    ("5", "Miżien. Analysis code and outputs: tools/cc-102-report/; data/cc-102/.", ""),
])

S.append(CondPageBreak(60 * mm))
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. The Ombudsman’s annual reports are official "
                "institutional records (C).")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "5 Oct 2026", "First issue. Verdict: largely supported, high confidence. No right of "
                                         "reply needed (supported check)."),
                   ("1.1", "6 Oct 2026", "Corrections after audit: said how the 42% depends on counting “partly "
                                         "implemented” as implemented; gave printed and PDF page numbers for the "
                                         "Commissioner’s chapter; sub-claim A wording says sustained cases closed in "
                                         "2025; Table 1.3 rows for 2023 and 2024 re-checked against the PDFs; "
                                         "Figure 1 enlarged; layout; status wording (no right of reply needed).")])

build_report(Report(
    number="102", out=str(FIG / "report.pdf"), kicker="Governance, computed",
    title_lines=["Ombudsman: 58%", "ignored?"],
    subtitle_lines=["Testing the Ombudsman’s 2025 figures", "on environment and planning recommendations"],
    quote_lines=["“7 recommendations, or 58%,", "were not implemented.”"], quote_size=16,
    attribution="Office of the Ombudsman, Annual Report 2025, on the Commissioner for Environment and Planning.",
    context="Newsbook, 2 July 2026: the highest rate among the commissioners; 22 reports escalated to Parliament.",
    verdict="Largely supported", verdict_note="Matches the tables; a small count and a snapshot",
    footer_lines=["Version 1.1  ·  6 October 2026",
                  "Status: draft; supported check, no right of reply needed",
                  "Prepared from public sources and open data. No site visits.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Ombudsman: 58% of environment recommendations ignored", version="1.1", date="6 October 2026",
    pdf_title="Ombudsman: 58% ignored? Claim Check 102",
    pdf_subject="Tests the Ombudsman's 2025 non-implementation figures for the Commissioner for Environment and Planning",
    story=S))
