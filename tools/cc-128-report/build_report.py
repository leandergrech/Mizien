"""Claim Check 128 report. Run calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []
LG = colors.HexColor("#8DB36B")

# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("The European Commission’s country document on Malta (SWD(2026) 702, 2 October 2026) says: <b>“Malta did not consult on, "
        "adopt or report the RBMP according to the WFD timetable.”</b> It adds that Malta’s single national river basin management "
        "plan (RBMP) was published in March 2024, against a reporting deadline of March 2022 [1]. We tested the dates against the "
        "Directive’s own timetable [2], the Commission’s 2025 implementation report [3] and a document dated within the consultation [4].", lead)]
S.append(key_points([
    ("The Directive’s timetable puts the third plan at 22 December 2021.",
     "Article 13(7) requires the plan to be updated 15 years after entry into force and every six years after; Article 14 requires a "
     "draft one year before the period starts, with at least six months for comments; Article 15 requires reporting within three months [2]."),
    ("Malta’s draft was still open for comment on 18 March 2024.",
     "BirdLife Malta’s comments on the ‘drafting’ of the plan are dated that day [4]; ERA’s consultation page gives 20 September 2023 to "
     "18 March 2024 (second-hand). The plan therefore cannot have been adopted before then: at least 817 days after the due date."),
    ("Malta had submitted nothing by the Commission’s cut-off.",
     "At 30 September 2023 Bulgaria, Cyprus, Greece, Malta and Portugal had submitted neither river basin nor flood risk plans [3]."),
    ("Lateness was widespread, and says nothing about quality.",
     "The Commission wrote that “many adopted them late” and opened proceedings against all Member States [3]. The check is about dates only."),
    ("Verdict: largely supported (high confidence).",
     "The month of publication rests on the Commission’s text; we could not read the plan or ERA’s pages (403)."),
]))
S += [Spacer(1, 4 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("22 Dec 2021", GREEN, "Third plan due under Article 13(7)"),
             ("18 Mar 2024", RED, "Draft still open for comment (BirdLife Malta, first-hand)"),
             ("817 days", RED, "from due date to that day: the least the delay can be"),
             ("5 of 27", AMBER, "Member States with neither plan submitted by 30 Sep 2023")]),
      Spacer(1, 4 * mm),
      up_down("Nothing: Supported is the top of the scale. The caveats are the unread plan and the unverified day of publication.",
              "A dated ERA adoption notice or a WISE reporting receipt showing adoption and reporting before the deadline (neither is suggested by any source we read).",
              heads=("What would make it stronger", "What would lower it")),
      Spacer(1, 5 * mm)]
S += toc([("1", "The claim and its source"), ("2", "Method"), ("3", "The timetable and Malta’s dates"),
          ("4", "Where the evidence points different ways"), ("5", "Testing the claim"),
          ("6", "Verdict and requests for evidence"), ("7", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and its source"))
S.append(P("The wording is in the Commission staff working document SWD(2026) 702 final, ‘Member State: Malta’, which accompanies "
           "the Commission’s report on the Water Framework Directive (WFD) and Floods Directive (COM(2025) 2). We read the whole "
           "document (copy on the Austrian Parliament website). The sentence appears twice, in the ‘Reporting’ paragraph (p. 8) and in "
           "section 2.1 ‘Governance’, and the recommendations ask Malta to adhere “to the WFD timetable when consulting on, adopting "
           "and reporting on the updated RBMP” [1]."))
S.append(std_table([
    [C("Commission’s words", cellh), C("Where", cellh)],
    [C("“Malta did not consult on, adopt or report the RBMP according to the WFD timetable.”"), C("Section 2.1; the ‘Reporting’ box has “in line with”")],
    [C("“The deadline for reporting the third River Basin Management Plans (RBMPs) was March 2022.” “A single national RBMP for "
       "Malta was published in March 2024, accompanied by WISE e-reporting.”"), C("‘Reporting’, p. 8")],
    [C("“The coordination and integration between the WFD, FD and MSFD remain insufficiently described.”"), C("Section 2.1")],
], [120 * mm, 50 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("SCOPE NOTE", tag),
               P("We test the dates. The Commission’s view that coordination between the three Directives is ‘insufficiently "
                 "described’ is a judgement on the text of a plan we could not read, so it is not rated. A late plan says nothing "
                 "about its content, and we draw no conclusion about it. The check concerns the statement, not any person.", small)],
              bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Question.</b> Did Malta consult on, adopt and report its third RBMP by the dates the Directive sets, and is the "
           "Commission’s account of dates (published March 2024; deadline March 2022) right?"))
S.append(P("<b>Evidence.</b> The consolidated Directive 2000/60/EC, Articles 13, 14, 15 and 25 [2]; the Commission’s report COM(2025) 2 "
           "(4 February 2025), section 2 and note 12 [3]; BirdLife Malta’s written comments of 18 March 2024 on the draft plan [4]; and "
           "ERA’s consultation pages, which return 403 to scripts and are known to us only through a web-search summary (second-hand) [5]. "
           "Every date is in <i>data/cc-128/timeline.csv</i> with its source and access, and the arithmetic is in "
           "<i>tools/cc-128-report/calc.py</i>."))
S.append(P("<b>Grades.</b> The Directive and the Commission’s documents are official texts (grade C); BirdLife’s letter is an NGO "
           "document used only for its date (D). No peer-reviewed source bears on a date check. We have not read the plan, ERA’s "
           "adoption notice or the WISE reporting record."))

# ================================================================== 3
S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(3, "The timetable and Malta’s dates"))
S.append(P("The third plan period starts on 22 December 2021 on our reading of Articles 13(7) and 14, so the draft was due for "
           "comment by 22 December 2020 and the plan itself by 22 December 2021 [2]. The Commission and its country document speak "
           "of March 2022, which is the reporting date (three months after publication, Article 15(1)); the Commission’s report loosely "
           "says plans were to be adopted “by March 2022” [3]. On either date Malta was late."))
S.append(fig(FIG / "fig1_timeline.png"))
S.append(P("Figure 1. Dates due under the Directive (green) and Malta’s dates (red). * Dates from ERA pages are second-hand (web-search "
           "summary). The March 2024 point is the end of the month, the latest the Commission’s ‘March 2024’ can mean [1, 2, 3, 5].", cap))
S.append(std_table([
    [C("Step", cellh), C("Due", cellh), C("Malta", cellh), C("Gap", cellh)],
    [C("Draft plan for six months’ comment (Art. 14)"), C("22 Dec 2020"), C("Consultation 20 Sep 2023 – 18 Mar 2024 (second-hand), BirdLife [4]"), C("1,002 days to opening")],
    [C("Plan published / adopted (Art. 13(7))"), C("22 Dec 2021"), C("Draft open on 18 Mar 2024 [4]; ‘published March 2024’ [1]"), C("at least 817 days")],
    [C("Plan reported (Art. 15(1))"), C("March 2022"), C("Not submitted by 30 Sep 2023 [3]; with WISE e-reporting at publication [1]"), C("at least 557 days to the cut-off")],
], [54 * mm, 26 * mm, 62 * mm, 28 * mm]))
S.append(P("The 18 March 2024 date does not rest on ERA: BirdLife Malta’s comments are headed with it and welcome “the drafting of the 3rd "
           "River Basin Management Plan” [4]. The consultation ran 180 days, six calendar months, in line with Article 14(2) once it "
           "opened; the lateness is in when it opened. The earlier consultation on significant water management issues, due by "
           "22 December 2019, opened on 19 August 2020 according to ERA (second-hand), about 241 days late.", small))

# ================================================================== 4
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(4, "Where the evidence points different ways"))
S.append(contested(
    "Q1  Was Malta singled out?", "NO, LATENESS WAS COMMON", AMBER,
    "Malta is one of five Member States (with Bulgaria, Cyprus, Greece and Portugal) that had submitted neither river basin nor flood "
    "plans at the cut-off, and one of seven left out of the RBMP assessment [3].",
    "The Commission says “many adopted them late” and that it launched legal proceedings “against all Member States in breach” [3]; "
    "the Commission’s own sentence is not a finding that Malta was worse than most on content.",
    "<b>For this claim:</b> the statement is accurate and says nothing comparative; the context is that late adoption was widespread."))
S.append(contested(
    "Q2  What does ‘published in March 2024’ mean?", "MONTH CONFIRMED, DAY NOT", AMBER,
    "The Commission states March 2024 for publication with WISE reporting [1]; BirdLife’s comment on the draft is dated 18 March 2024 [4].",
    "ERA says (second-hand) that the final version followed the close of consultation on 18 March 2024 [5], leaving under two weeks "
    "in March; we could not read the plan or ERA’s notice to fix the day.",
    "<b>For this claim:</b> every reading puts adoption at least 26 months after the due date; the exact day does not change that."))

# ================================================================== 5
S.append(CondPageBreak(100 * mm))
S.append(SectionHeading(5, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> Malta did not consult on the RBMP on the timetable"),
     C("Draft due 22 Dec 2020 [2]; consultation opened 20 Sep 2023 (second-hand) [5], still open 18 Mar 2024 [4]."), verd("SUPPORTED", GREENC)],
    [C("<b>B.</b> Malta did not adopt it on the timetable"),
     C("Due 22 Dec 2021 [2]; still a draft on 18 Mar 2024 [4]. The adoption date itself was not read."), verd("SUPPORTED", GREENC)],
    [C("<b>C.</b> Malta did not report it on the timetable"),
     C("Reporting due March 2022 [1, 2]; not submitted at 30 Sep 2023 [3]; reported with March 2024 publication [1]."), verd("SUPPORTED", GREENC)],
    [C("<b>D.</b> Published in March 2024, against a March 2022 reporting deadline"),
     C("Both dates as the Commission states them [1]; the 2022 date is the reporting deadline, the Directive’s publication date is 22 Dec 2021; the day in March 2024 is not independently confirmed."),
     verd("LARGELY SUPPORTED", LG)],
    [C("<b>E.</b> Coordination of WFD, Floods and Marine Strategy Directives ‘insufficiently described’"),
     C("A judgement on the plan’s text, which we did not read. Not rated."), verd("NOT RATED", GREY)],
], [56 * mm, 84 * mm, 30 * mm], valign="MIDDLE"))

# ================================================================== 6
S += [Spacer(1, 6 * mm), SectionHeading(6, "Verdict and requests for evidence"),
      verdict_box("Largely supported", "The dates the Commission gives are consistent with the Directive, the Commission’s earlier "
                  "report and a document dated during the consultation. Confidence: high. No right of reply needed."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) Three independent lines agree that Malta’s plan was not in place, consulted on or reported by the "
           "due dates. (2) The caveats are minor: the day of publication, and the Commission’s loose use of ‘March 2022’ for a date the "
           "Directive puts at 22 December 2021 for publication. Our scale calls that <i>Largely supported</i>."))
S.append(P("<b>What this verdict does not say.</b> It does not rate the plan’s content, say why the dates were missed or compare "
           "Malta’s lateness with other countries’ beyond the Commission’s own list."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "From ERA and the Energy and Water Agency: the dated notice of adoption of the Third RBMP and the consultation notice of 2023.",
    "From the EEA: the WISE/CDR delivery record for Malta’s RBMP (date of reporting).",
    "From the Commission: whether ‘March 2022’ in the report refers to reporting or adoption.",
]))

# ================================================================== 7
S += [Spacer(1, 6 * mm), SectionHeading(7, "Limitations")]
for l in ["We did not read the Third RBMP, ERA’s consultation and adoption pages (403 to scripts; Wayback unreachable on 19 Oct 2026) "
          "or the WISE delivery record. ERA’s dates reach us through a web-search summary only and are marked second-hand.",
          "The ‘plan period starts 22 December 2021’ reading is ours, from Articles 13(7) and 14; the Directive does not define the start date in those words.",
          "The Commission’s report names the cut-off (30 September 2023) but not a submission date for Malta.",
          "We did not compare other Member States’ delays in the staff working documents beyond what COM(2025) 2 states."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "European Commission (2 Oct 2026). Staff Working Document SWD(2026) 702 final, Member State: Malta (third RBMPs, second flood hazard "
          "and risk maps and FRMPs), pp. 8, 9, recommendation 7(b). (Read in full.)",
     "https://www.parlament.gv.at/dokument/XXVIII/EU/94981/imfname_11680004.pdf"),
    ("2", "Directive 2000/60/EC (Water Framework Directive), consolidated text, Articles 13, 14, 15 and 25. (Read.)",
     "https://publications.europa.eu/resource/celex/02000L0060-20141120"),
    ("3", "European Commission (4 Feb 2025). Report on the implementation of the Water Framework Directive and the Floods Directive, "
          "COM(2025) 2 final, section 2 and note 12. (Passages read.)", "https://publications.europa.eu/resource/celex/52025DC0002"),
    ("4", "BirdLife Malta (18 Mar 2024). Comments on the Third River Basin Management Plan for Malta. (Read in full; used for its date.)",
     "https://birdlifemalta.org/wp-content/uploads/2024/03/BLM-comments-3rd-RBMN.docx.pdf"),
    ("5", "Second-hand: Environment and Resources Authority. Public consultation pages for Malta’s Third River Basin Management Plan (second-hand: "
          "web-search summary of 19 Oct 2026; host returns 403).",
     "https://era.org.mt/public-consultation-maltas-third-river-basin-management-plan-pursuant-to-the-water-framework-directive-2000-60-ec/"),
    ("6", "Miżien. Data and calculations: data/cc-128/; tools/cc-128-report/.", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. Second-hand sources are labelled as such.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "19 Oct 2026", "First issue. Verdict Largely supported. No right of reply needed.")])

build_report(Report(
    number="128", out=str(FIG / "report.pdf"), kicker="Water, checked",
    title_lines=["Did Malta miss", "the water-plan", "timetable?"],
    subtitle_lines=["Testing the Commission’s statement on Malta’s", "third river basin management plan"],
    quote_lines=["“Malta did not consult on, adopt or report the RBMP", "according to the WFD timetable.”"],
    quote_size=14,
    attribution="European Commission, staff working document SWD(2026) 702, 2 October 2026.",
    context="Plan published March 2024; reporting deadline March 2022.",
    verdict="Largely supported", verdict_note="Dates consistent with the Directive; day of publication unverified",
    footer_lines=["Version 1.0  ·  19 October 2026", "Status:",
                  "Prepared from public sources, EU documents.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Malta’s third river basin plan: timetable", version="1.0", date="19 October 2026",
    pdf_title="Did Malta miss the water-plan timetable? Claim Check 128",
    pdf_subject="Tests the Commission's statement that Malta did not consult on, adopt or report its third RBMP on the WFD timetable",
    story=S))
