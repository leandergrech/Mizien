"""Claim Check 116 report. Run calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("At its 47th session in July 2025 the UNESCO World Heritage Committee adopted Decision 47 COM 7B.114 on the "
        "City of Valletta. It <b>“Notes with concern that the current planning policies and regulations do not "
        "sufficiently safeguard the setting of the property”</b> and asks Malta to act. We read the adopted decision "
        "and the Committee’s own working document and checked each part of the claim against them.", lead)]
S.append(key_points([
    ("The claim reports the decision accurately.",
     "All ten phrases we tested are in the adopted text: the concern about planning policies, the revision of the "
     "Views and Vistas Analysis and three planning documents to set effective height controls, the further "
     "development of the buffer zone, and an updated report by 1 December 2026."),
    ("The adopted decision matches the draft the Committee had before it.",
     "Apart from one comma, the adopted paragraphs are word for word the draft in the Committee’s document "
     "WHC/25/47.COM/7B.Add.3, which also carries the Advisory Bodies’ analysis behind the wording."),
    ("It is not a threat of delisting, and it is not a clean bill either.",
     "The decision “welcomes” the management plan, the views analysis and a proposed buffer zone, and contains no "
     "request about the List of World Heritage in Danger (0 mentions). It also finds the setting not sufficiently "
     "safeguarded. Both sides’ summaries (Section 4) stretch one half of that."),
    ("Verdict: supported (high confidence), for the claim as worded.",
     "The claim says what the Committee found and asked, and that is what the decision says. We did not "
     "independently test the planning policies themselves; the Committee’s finding rests on the Advisory Bodies’ "
     "review, which we could read only as summarised in the Committee’s document."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(0), Spacer(1, 3 * mm),
      tiles([("10 of 10", GREEN, "Phrases of the claim found in the adopted decision text"),
             ("4", GREY, "Planning documents the Committee asks Malta to revise (views analysis + three plans)"),
             ("0", GREEN, "Mentions of the Danger List, delisting or removal in the decision"),
             ("1 Dec 2026", AMBER, "Date the updated report is due, for the 49th session")]),
      Spacer(1, 4 * mm),
      up_down("Nothing: Supported is the top of the scale. (The decision text itself would have to differ from what "
              "we read for the verdict to change.)",
              "An adopted text that differs from the one we read, or a Committee correction of the decision.",
              heads=("What would move the verdict up", "What would move the verdict down")),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the decision says"),
          ("4", "Where the evidence points different ways"), ("5", "Testing the claim"),
          ("6", "Verdict and requests for evidence"), ("7", "Limitations")])
S.append(PageBreak())

S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The claim is a statement about a decision, so the test is the decision itself. The claim record was "
           "built from a news report and a UNESCO page that refused automated access; we found the adopted text on "
           "the World Heritage Centre’s decisions page [1] and the Committee’s working document for the session "
           "[2], and read both in full on 14 October 2026. The text of the decision is also cited by the news "
           "reports we read [3, 4, 5]."))
S.append(std_table([
    [C("Source", cellh), C("What it says", cellh), C("Our access", cellh), C("Status", cellh)],
    [C("<b>World Heritage Committee</b>, Decision 47 COM 7B.114, City of Valletta (Malta), 47th session, 2025 [1]"),
     C("“Notes with concern that the current planning policies and regulations do not sufficiently safeguard the "
       "setting of the property, and requests the State Party to revise the VVA, the 2006 North Harbour Local Plan, "
       "the 2014 Planning Policy Guide on the Use and Applicability of the Floor Area Ratio, and the 2022 Grand "
       "Harbour Local Plan to establish effective height controls within and around the property”. Finally, it "
       "requests an updated report “by 1 December 2026”."), C("Adopted text read in full."), C("<b>The claim</b>")],
    [C("<b>World Heritage Centre</b>, WHC/25/47.COM/7B.Add.3, pp. 71–74 [2]"),
     C("The draft decision (identical to the adopted text, see Section 3) and the analysis by the World Heritage "
       "Centre, ICOMOS and ICCROM that leads to it."), C("PDF read in full for the Valletta entry."),
     C("<b>Context</b>")],
    [C("<b>The Shift</b>, 18 Jun 2026 [3]"), C("The outlet’s summary of the Committee’s requests."),
     C("Read."), C("Locator")],
    [C("<b>Newsbook</b> [4] and <b>Lovin Malta</b> [5]"),
     C("Reports of the Opposition’s and the Ministry for Culture, Lands and Local Government’s reactions to the "
       "decision."), C("Read; the Ministry’s own statement was not."), C("Reactions " + DIAM)],
], [40 * mm, 72 * mm, 32 * mm, 26 * mm]))

S += [Spacer(1, 4 * mm), SectionHeading(2, "Method")]
S.append(P("<b>Question.</b> Does the claim state accurately what the Committee found and asked for?"))
S.append(P("<b>Evidence.</b> <i>tools/cc-116-report/calc.py</i> downloads the adopted decision and the Committee’s "
           "document, then checks by string comparison (a) that each phrase of the claim is in the adopted text, "
           "(b) that the adopted paragraphs match the draft in the document, and (c) that the text contains no "
           "request about the List of World Heritage in Danger (searches for “Danger”, “endanger”, “delist” and "
           "“removal”). Results, with the SHA-256 of each download and the retrieval date, are in "
           "<i>data/cc-116/checks.csv</i>. We read the Committee’s document for the Advisory Bodies’ reasons and "
           "for the history of the requests."))
S.append(P("<b>Grades.</b> The Committee’s decision and its working document are official records (grade C); the "
           "news reports are used to locate reactions only. <b>Verdicts</b> follow the five-point scale in Appendix "
           "A."))

S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(3, "What the decision says"))
S.append(fig(FIG / "fig1_timeline.png", width=CW * 0.98))
S.append(P("Figure 1. The Committee’s requests on the setting of Valletta, 2009 to 2026, as recorded in Decision "
           "47 COM 7B.114 and the Committee’s document WHC/25/47.COM/7B.Add.3.", cap))
S.append(P("<b>The finding.</b> Paragraph 4 of the decision notes with concern that current planning policies and "
           "regulations do not sufficiently safeguard the setting of the property, and requests revision of four "
           "documents (the Views and Vistas Analysis, the 2006 North Harbour Local Plan, the 2014 Floor Area Ratio "
           "policy guide and the 2022 Grand Harbour Local Plan) to establish effective height controls within and "
           "around the property [1]. The Committee’s document says why: ICOMOS’s review of the Views and Vistas "
           "Analysis recommends that the three plans be revised to include defined height controls, and it notes "
           "that the 2014 policy guide, while a step forward, “identifies locations and design criteria for tall "
           "buildings within the property’s setting”, some visible from the property across Marsamxett Harbour "
           "[2, p. 72]."))
S.append(P("<b>The buffer zone.</b> Paragraph 3 <i>welcomes</i> the submission of a draft management plan, the views "
           "analysis and “a proposal for a buffer zone”; paragraph 5 asks that the proposal be further developed, "
           "with attention to the northern boundary across Marsamxett Harbour, an area identified as having high "
           "development potential [1]. The Committee’s document traces the demand for a buffer zone with height "
           "controls to Decision 33 COM 7B.113 of 2009 [2, p. 72]."))
S.append(P("<b>The deadline.</b> Paragraph 8 requests an updated report by 1 December 2026 for the Committee’s 49th "
           "session [1]. The decision gives no reason for choosing that date."))
S.append(P("<b>What is not in it.</b> The adopted text has no request about the Danger List: searches of the "
           "2,946-character text for “Danger”, “endanger”, “delist” and “removal” find nothing (data/cc-116/"
           "checks.csv). The adopted text equals the draft in the Committee’s document, ignoring commas; the one "
           "exact difference is a comma after “45 COM 7B.190” in the recalling paragraph."))

S.append(CondPageBreak(80 * mm))
S.append(SectionHeading(4, "Where the evidence points different ways"))
S.append(P("The decision has been summarised in opposite ways. We set what each side said, as reported, beside the "
           "text. Statements by the Opposition and the Ministry are known to us only through outlets " + DIAM + "."))
S.append(contested("How serious is the decision?", "BOTH STRETCH THE TEXT", AMBER,
                   "<b>Opposition (PN statement, as reported by Newsbook " + DIAM + "):</b> the report confirmed that local "
                   "plans needed updating; the party’s MPs warned that Valletta was at risk of losing its World "
                   "Heritage status, and spoke of UNESCO’s condemnation of the lack of control over building "
                   "heights, tourism pressure and the absence of an effective buffer zone (Newsbook’s indirect "
                   "speech, not quoted).",
                   "<b>Ministry for Culture, Lands and Local Government (as reported by Newsbook and Lovin Malta "
                   + DIAM + "):</b> the Opposition “chose the path of alarmism” (Newsbook), and "
                   "Lovin Malta reports the Ministry calling it an “alarmist” and “negative” narrative. The outlets report the Ministry as saying the UNESCO report "
                   "made no claim that the status was at risk, that there was no other cause for concern, and that "
                   "the later deadline was a sign of confidence (indirect speech, not quoted).",
                   "The decision contains no request about the Danger List or loss of status (0 mentions), which "
                   "matches the Ministry on that point. It does find the setting not sufficiently safeguarded and "
                   "asks for four documents to be revised, which sits badly with a message that there was no other cause for "
                   "concern. On the buffer zone it welcomes a proposal and asks for it to be developed further; it "
                   "does not say one is absent. The decision gives no reason for the date, so “a sign of "
                   "confidence” is the Ministry’s reading and cannot be tested from the text.",
                   label_a="THE OPPOSITION, AS REPORTED", label_b="THE MINISTRY, AS REPORTED"))

S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(5, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> The Committee noted with concern that current planning policies and regulations do not "
       "sufficiently safeguard the setting of Valletta"), C("World Heritage Committee [1]"),
     C("Word for word in paragraph 4 of the adopted decision; the same sentence is in the draft in the "
       "Committee’s document [2, p. 73]."), verd("ACCURATE", GREENC)],
    [C("<b>B.</b> It asked for effective height controls within and around the property, through revision of the "
       "Views and Vistas Analysis and planning documents"), C("World Heritage Committee [1]"),
     C("Paragraph 4: revise the VVA, the 2006 North Harbour Local Plan, the 2014 Floor Area Ratio policy guide and "
       "the 2022 Grand Harbour Local Plan “to establish effective height controls within and around the "
       "property”."), verd("ACCURATE", GREENC)],
    [C("<b>C.</b> It asked for a further-developed buffer zone"), C("World Heritage Committee [1]"),
     C("Paragraph 5: the draft proposal “be further developed”, especially the northern boundary across "
       "Marsamxett Harbour. Paragraph 3 welcomes the proposal’s submission."), verd("ACCURATE", GREENC)],
    [C("<b>D.</b> It asked for an updated report by 1 December 2026"), C("World Heritage Committee [1]"),
     C("Paragraph 8: “by 1 December 2026”, for examination at the 49th session."), verd("ACCURATE", GREENC)],
], [44 * mm, 22 * mm, 70 * mm, 30 * mm], valign="MIDDLE"))

S += [Spacer(1, 6 * mm), CondPageBreak(75 * mm), SectionHeading(6, "Verdict and requests for evidence"),
      verdict_box("Supported", "The claim states accurately what the Committee found and asked for. "
                  "Confidence: high."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> Our scale rates a claim <i>Supported</i> when the evidence consistently backs it as stated. "
           "The claim reports a Committee decision; the adopted text and the Committee’s own draft say what the "
           "claim says, in all four parts. Confidence is high because the primary text was read in full and "
           "matches the draft."))
S.append(P("<b>What this verdict does not say.</b> It does not say the Committee’s finding is right or wrong: we did "
           "not test Malta’s planning policies or recent permits against it (Section 7). It does not say Valletta’s "
           "status is at risk; the decision does not say that either. And it is not a verdict on the Government’s or "
           "the Opposition’s reaction, which we set beside the text in Section 4."))
S.append(P("Evidence that would let us test the finding itself", h2))
S.append(requests_list([
    "From the Planning Authority and the Superintendence for Cultural Heritage: the revised Views and Vistas "
    "Analysis, any revised local plans and the updated buffer zone proposal, when published.",
    "Malta’s updated state of conservation report due by 1 December 2026, and the Committee’s response at its 49th "
    "session (this check should be revisited after both).",
    "ICOMOS’s technical review of the Views and Vistas Analysis (December 2024), which the Committee’s document "
    "summarises but which we did not read.",
]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag),
               P("Not needed. Under the maintainer’s rule of 5 October 2026 a reply is sought only for <i>Not "
                 "substantiated</i>, <i>Misleading</i> or <i>Contradicted</i> verdicts.", small)], bg=PALE, bar=GREEN)]
S += [Spacer(1, 6 * mm), SectionHeading(7, "Limitations")]
for l in ["We tested the claim against the decision, not the decision against the ground: the Planning Authority’s "
          "site refuses automated access, so we did not read the 2014 policy guide or the local plans, and relied on "
          "the Committee’s document for what they contain.",
          "ICOMOS’s review of the Views and Vistas Analysis was read only as summarised in the Committee’s document.",
          "The Opposition’s and the Ministry’s statements are known only through Newsbook and Lovin Malta " + DIAM +
          "; we did not read either statement itself.",
          "The 1 December 2026 report had not fallen due when this check was written; nothing here judges "
          "whether it will be delivered or accepted."]:
    S.append(P("• " + l, bul))
S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "UNESCO World Heritage Committee (2025). Decision 47 COM 7B.114, City of Valletta (Malta), adopted at its "
          "47th session. World Heritage Centre decisions database, retrieved 14 Oct 2026.",
     "https://whc.unesco.org/en/decisions/8838"),
    ("2", "UNESCO World Heritage Centre (2025). State of conservation of properties inscribed on the World Heritage "
          "List, WHC/25/47.COM/7B.Add.3, entry 114 (pp. 71–74). Retrieved 14 Oct 2026.",
     "https://whc.unesco.org/archive/2025/whc25-47com-7BAdd3-en.pdf"),
    ("3", "The Shift News (18 Jun 2026). UNESCO: 15 years of chasing Malta for Valletta’s conservation report. "
          "Locator only.", "https://theshiftnews.com/2026/06/18/unesco-15-years-of-chasing-malta-for-vallettas-conservation-report/"),
    ("4", "Newsbook (n/d; after the 47th session, July 2025). PN accuses government of failing to protect Valletta’s World Heritage status; and: UNESCO "
          "demands urgent action to protect Valletta’s World Heritage status.",
     "https://newsbook.com.mt/en/pn-accuses-government-of-failing-to-protect-vallettas-world-heritage-status/"),
    ("5", "Lovin Malta (n/d; July 2025). UNESCO approves Valletta’s conservation report as government rejects Opposition "
          "‘alarmism’.", "https://lovinmalta.com/news/unesco-approves-vallettas-conservation-report-as-government-rejects-opposition-alarmism/"),
    ("6", "MiŻien. Check script and outputs: tools/cc-116-report/calc.py; data/cc-116/checks.csv.", ""),
])
S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "14 Oct 2026", "First issue. Verdict Supported (high confidence); no right of reply needed.")])

build_report(Report(
    number="116", out=str(FIG / "report.pdf"), kicker="Heritage and planning",
    title_lines=["UNESCO: Valletta’s", "setting not", "safeguarded?"],
    subtitle_lines=["Reading the World Heritage Committee’s decision", "against what was reported"],
    quote_lines=["“…the current planning policies and regulations do not", "sufficiently safeguard the setting of the property…”"],
    quote_size=14,
    attribution="UNESCO World Heritage Committee, Decision 47 COM 7B.114, City of Valletta, 2025.",
    context="Also asks for effective height controls, a further-developed buffer zone and a report by 1 December 2026.",
    verdict="Supported", verdict_note="The decision says what the claim says; it is not a delisting threat",
    footer_lines=["Version 1.0  ·  14 October 2026", "Status: no right of reply needed",
                  "Prepared from the Committee’s decision and working document.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Valletta’s setting – UNESCO Decision 47 COM 7B.114", version="1.0", date="14 October 2026",
    pdf_title="UNESCO: Valletta’s setting not safeguarded? Claim Check 116",
    pdf_subject="Tests a report of the World Heritage Committee's decision on the City of Valletta",
    story=S))
