"""Claim Check 014 report. Run calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []

# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("In September 2025 the Planning Authority’s chief executive, Johann Buttigieg, told The Malta Independent: "
        "<b>“We had times when we issued over 1,000 enforcement notices per year.”</b> The newspaper reports that he "
        "said the number had fallen to around 200, <b>which he put down to there being fewer illegalities</b>: "
        "“people have recognised that it does not make sense to build illegally.” We tested both parts against "
        "twenty years of MEPA and Planning Authority annual reports.", lead)]
S.append(key_points([
    ("Both numbers are right.",
     "MEPA issued over 1,000 notices in five of the eight years we could read between 2001 and 2009 (1,369 in "
     "2001). The Planning Authority issued 191 in 2024; the 2020–2024 average is 187."),
    ("Complaints did not fall the same way.",
     "Notices fell 82%. Complaints of illegal development fell 11% since 2009 (2,701 to 2,411) and 35% since "
     "2004/05; in 2020 they reached 3,313. About half of the 2024 complaints were confirmed as illegal development."),
    ("What changed is how cases end.",
     "Notices per 100 complaints fell from about 30–40 to 5–10. In 2024, 521 confirmed cases ended in an "
     "application to sanction the works and 482 in removal by the owner; 162 led to a notice. The Authority’s own "
     "report credits the fall in notices to persuading contraveners first."),
    ("There is some support for “fewer”.",
     "Confirmed cases appear to have dropped by about a third between 2020 and 2024 (roughly 1,820 to 1,200). "
     "That is far smaller than the fall in notices, and complaints are an imperfect measure of illegal building."),
    ("Verdict: misleading (moderate confidence).",
     "The figures are accurate, but presenting the fall in notices as a sign of fewer illegalities leaves out the "
     "main documented reason: a change in how the Authority handles them."),
]))
S += [Spacer(1, 4 * mm), VerdictMeter(3), Spacer(1, 3 * mm),
      tiles([("1,033", GREEN, "Average notices a year, 2001–2009 (MEPA)"),
             ("187", GREY, "Average notices a year, 2020–2024 (PA)"),
             ("−11%", ORANGE, "Change in complaints of illegal development, 2009 to 2024"),
             ("~1,200", RED, "Complaints confirmed as illegal development in 2024")]),
      Spacer(1, 4 * mm),
      up_down("An independent measure of illegal building (for example aerial-photo change detection) showing a fall "
              "of the same order as the fall in notices; or Planning Authority data for 2012–2018 showing complaints "
              "and confirmed cases falling in step with notices.",
              "Data showing that confirmed illegal cases have been stable or rising; or that a growing share of "
              "illegal works is being regularised rather than removed."),
      Spacer(1, 5 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What a notice measures"),
          ("4", "What the data show"), ("5", "Where the evidence points different ways"),
          ("6", "Testing the claim"), ("7", "Verdict and requests for evidence"), ("8", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The claim comes from an interview with The Malta Independent on Sunday, published on 7 September 2025 "
           "[1], which we read in full. The interview took place during public consultation on planning bills and "
           "legal notices that would allow some illegal developments to be regularised. We assess the chief "
           "executive’s words as reported, not the headline."))
S.append(std_table([
    [C("What was said", cellh), C("Form", cellh), C("Our access", cellh)],
    [C("“We had times when we issued over 1,000 enforcement notices per year.”"), C("Direct quote [1]"), C("Read in full")],
    [C("Now reduced to around 200, “due to there being fewer illegalities”"), C("Newspaper’s paraphrase [1]"), C("Read in full")],
    [C("“I would say that over the last 20 years, people have recognised that it does not make sense to build "
       "illegally.”"), C("Direct quote [1]"), C("Read in full")],
    [C("Over 500 enforcement notices pending, over 5,000 cases for direct action; 1,500 illegalities removed by "
       "direct action over 30 years; clearing the backlog at the current rate “would take us more than 90 years”."),
     C("Direct quotes and paraphrase [1]"), C("Read in full")],
], [104 * mm, 34 * mm, 32 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("FAIRNESS NOTE", tag),
               P("In the same interview the chief executive acknowledged that the Authority had “struggled” with "
                 "enforcement and that there were “too many illegalities for the PA to enforce on everything”. A "
                 "persuasion-first strategy is a recognised approach in regulation (Section 3), and many cases now "
                 "end with the owner removing or legalising the works without a notice. This check is about whether "
                 "fewer notices shows fewer illegalities, not about whether the strategy is right.", small)],
              bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Question.</b> Is the fall from over 1,000 notices a year to about 200 accurate, and does the evidence "
           "show that it reflects fewer illegalities?"))
S.append(P("<b>Evidence.</b> We read the enforcement sections of the MEPA annual reports for 2004 to 2011 and the "
           "Planning Authority annual report for 2024 [2–9], which give notices issued and complaints received. For "
           "2019–2023 we used news reports of the Authority’s annual reports and of parliamentary answers [10–13], "
           "marked as second-hand. Every number was transcribed to <i>data/cc-014/pa_enforcement_series.csv</i> and "
           "every percentage recomputed with <i>tools/cc-014-report/calc.py</i>. We searched Crossref and OpenAlex for "
           "studies of planning enforcement in Malta and found none; the regulatory literature [14–16] is context."))
S.append(P("<b>Grades.</b> Annual reports and official answers are grade C (official statistics). News reports of "
           "them are grade C but second-hand. <b>Verdicts</b> follow the five-point scale in Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(90 * mm))
S.append(SectionHeading(3, "What a notice measures"))
S.append(P("An enforcement notice is something the regulator does: it records the Authority acting on an illegality "
           "it has found. The number issued depends on how many illegalities exist, how many are reported or "
           "detected, and how the Authority chooses to deal with them. If the Authority settles more cases by other "
           "means, notices fall even if illegal building does not. Counting notices as if they measured the "
           "underlying problem is the pattern our methodology calls <i>input as outcome</i>."))
S.append(P("Regulatory research supports both sides of the trade-off. Reviews of environmental enforcement find "
           "that inspections and sanctions deter future violations, both by the firm sanctioned and by others "
           "[14]. The “responsive regulation” tradition argues that regulators should start with persuasion and "
           "escalate only when that fails [15, 16]. Neither body of work treats a fall in sanctions as evidence, on "
           "its own, of a fall in violations."))

# ================================================================== 4
S.append(CondPageBreak(150 * mm))
S.append(SectionHeading(4, "What the data show"))
S.append(fig(FIG / "fig1_series.png"))
S.append(P("Figure 1. Enforcement notices issued (bars) and complaints of illegal development (dots), 2001–2024. "
           "Complaints did not fall in step with notices.", cap))
S.append(std_table([
    [C("Indicator", cellh), C("Then", cellh), C("Now", cellh), C("Change", cellh), C("Source", cellh)],
    [C("Notices a year (average)"), C("1,033 (2001–09)"), C("187 (2020–24)"), C("<b>−82%</b>"), C("[2–9, 10–13]")],
    [C("Complaints of illegal development"), C("2,701 (2009)"), C("2,411 (2024)"), C("−11%"), C("[6, 9]")],
    [C("Complaints, longer run"), C("3,705 (FY 2004/05)"), C("2,411 (2024)"), C("−35%"), C("[3, 9]")],
    [C("Notices per 100 complaints"), C("29–42 (2005–11)"), C("5–10 (2019–24)"), C("about −80%"), C("calculated")],
    [C("Confirmed illegal cases"), C("~1,820 (2020)"), C("~1,200 (2024)"), C("about −34%"), C("[9, 10]")],
], [52 * mm, 30 * mm, 30 * mm, 22 * mm, 36 * mm]))
S.append(P("All values in <i>data/cc-014/checks.csv</i>. 2012–2018 are missing: the 2012 and 2014 MEPA reports are "
           "scanned images and later reports are published only on a page-flip site.", cap))
S.append(fig(FIG / "fig2_outcomes.png"))
S.append(P("Figure 2. Outcomes of the 2024 complaints as reported by the Planning Authority [9]. Most confirmed "
           "illegal works ended without a notice: the owner applied to sanction them or removed them.", cap))
S.append(P("Reading across the data", h2))
for t in ["• <b>The headline numbers are accurate.</b> “Over 1,000 a year” matches 2001, 2002, 2004, 2005 and "
          "2009; “around 200” matches every year from 2019 to 2024.",
          "• <b>Complaints did not halve, let alone fall by four-fifths.</b> They were 2,105 in 2011 and 3,313 in "
          "2020, and around 2,400 in 2023 and 2024, even after the Authority stopped accepting anonymous reports [13].",
          "• <b>The share of cases ending in a notice collapsed.</b> In 2024 more than three times as many confirmed "
          "cases ended in a sanctioning application or removal as in a notice. In 2020, 818 complaints led to a "
          "sanctioning application [10].",
          "• <b>The Authority explains it this way itself.</b> Its 2024 report attributes the 18% fall in notices "
          "that year to a strategy of persuading contraveners to rectify before formal action [9, 13]. MEPA’s 2007 "
          "report attributed an earlier fall partly to closer monitoring of works in progress [5]."]:
    S.append(P(t, bul))

# ================================================================== 5
S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(5, "Where the evidence points different ways"))
S.append(contested(
    "Q1  Are there fewer illegalities than in the 2000s?", "POSSIBLY SOME; NOT FOUR-FIFTHS FEWER", AMBER,
    "Complaints are lower than in 2004/05 (−35%) and confirmed cases fell by about a third between 2020 and 2024. "
    "Higher daily fines and the sanctioning route may have changed behaviour, as the chief executive says.",
    "Complaints in 2024 were only 11% below 2009, and in 2020 they were the highest in the series we could read. "
    "About 1,200 complaints a year are still confirmed as illegal development.",
    "<b>For this claim:</b> a modest fall in reported illegalities is plausible; a fall of the size implied by "
    "notices (−82%) is not supported by the Authority’s own figures."))
S.append(contested(
    "Q2  Why did notices fall?", "MAINLY A CHANGE IN PRACTICE", RED,
    "Fewer new illegalities would mean fewer notices. Owners now more often remove works once contacted, which is "
    "the outcome enforcement aims for.",
    "Notices per complaint fell about five-fold. The Authority’s own report credits persuasion; hundreds of cases a "
    "year are closed by applications to legalise the works [9, 10].",
    "<b>For this claim:</b> the documented explanation is how cases are handled, which the statement does not "
    "mention."))
S.append(contested(
    "Q3  Do complaints measure illegal building?", "ONLY PARTLY", AMBER,
    "Complaints are the main way the Authority learns of illegal works, and confirmation rates (about half to 55%) "
    "are reported each year.",
    "Complaints depend on public vigilance, reporting tools and rules (anonymous reports stopped in 2024). No "
    "independent count of illegal building, such as aerial-photo change detection, has been published.",
    "<b>For this verdict:</b> confidence is moderate because both sides rely on proxies."))

# ================================================================== 6
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(6, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> “We had times when we issued over 1,000 enforcement notices per year”"),
     C("1,369 (2001), 1,030 (2002), 1,061 (2004), 1,077 (2005), 1,120 (2009) [2–6]."), verd("ACCURATE", GREENC)],
    [C("<b>B.</b> Now around 200"), C("164–233 a year, 2019–2024; 191 in 2024 [9–12]."), verd("ACCURATE", GREENC)],
    [C("<b>C.</b> The fall is due to fewer illegalities"),
     C("Complaints fell 11–35% against an 82% fall in notices; notices per complaint fell about five-fold; the "
       "Authority attributes the fall to persuasion."), verd("MISLEADING", colors.HexColor("#C85A3A"))],
    [C("<b>D.</b> Over 5,000 cases awaiting direct action; over 90 years to clear"),
     C("5,382 pending notices at end 2021 [11]; 74 closed by direct action in 2020 [10] implies about 73 years. "
       "Consistent in size."), verd("BROADLY CONSISTENT", AMBER)],
    [C("<b>E.</b> 1,500 illegalities removed by direct action in 30 years"), C("No annual series found."),
     verd("NOT TESTED", GREY)],
], [52 * mm, 88 * mm, 30 * mm], valign="MIDDLE"))

# ================================================================== 7
S += [Spacer(1, 6 * mm), SectionHeading(7, "Verdict and requests for evidence"),
      verdict_box("Misleading", "Accurate figures; the explanation leaves out the main documented cause. Confidence: "
                  "moderate. Based on MEPA and Planning Authority annual reports, which can be shown."),
      Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) Both figures are accurate. (2) Complaints of illegal development fell far less than "
           "notices, and about 1,200 complaints a year are still confirmed as illegal. (3) The share of cases ending "
           "in a notice fell about five-fold, as more cases ended in applications to legalise the works or in removal "
           "after contact, and the Authority’s own 2024 report gives persuasion as the reason. Presenting the fall in "
           "notices as evidence of fewer illegalities therefore gives an inaccurate overall impression, which our "
           "scale calls <i>Misleading</i>."))
S.append(P("<b>What this verdict does not say.</b> It does not say that illegal building has increased, that the "
           "persuasion-first approach is wrong, or that anyone acted in bad faith. A fuller statement would read: "
           "<i>“We used to issue over 1,000 notices a year; now about 200, because most cases are settled by "
           "removal or a sanctioning application before a notice is needed. Complaints are about 2,400 a year and "
           "half are still confirmed as illegal.”</i>"))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "Annual complaints, confirmed illegal cases, notices and outcomes for 2012–2018, to close the gap in the series.",
    "Any analysis behind the statement that illegalities have fallen (for example aerial or satellite surveys).",
    "How many confirmed cases each year end in a sanctioning permit, and how many of those permits are granted.",
    "The source of the figure of 1,500 direct actions over 30 years, by year.",
]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag),
               P("Before wider circulation this draft should be sent to the Planning Authority with a fixed deadline "
                 "(suggested 14 days). Under our standards a <i>Misleading</i> verdict is not published before that "
                 "deadline passes. Responses will be appended and the verdict revisited.", small)],
              bg=AMBER_PALE, bar=AMBER)]

# ================================================================== 8
S += [Spacer(1, 6 * mm), SectionHeading(8, "Limitations")]
for l in ["Complaints and confirmed cases are proxies for illegal building. They depend on public reporting and on "
          "Authority rules, which changed (anonymous reports stopped in 2024; a reporting app was introduced earlier).",
          "Definitions shift: MEPA reported by financial year until about 2006; the 2011 complaint count excludes sites "
          "already under a notice; the 2009 figures add the Gozo Office.",
          "2019–2023 figures are second-hand (news reports of annual reports and of parliamentary answers); the 2019 "
          "notice count is derived from a reported percentage.",
          "2008 and 2012–2018 are missing. A steady decline or a sudden policy change in those years would not change "
          "the comparison of endpoints, but would change how it is explained.",
          "No peer-reviewed study of planning enforcement in Malta was found; the regulatory literature is used for "
          "context only and was read as abstracts."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
M = "https://era.org.mt/wp-content/uploads/2019/05/"
S += references([
    ("1", "The Malta Independent (7 Sep 2025). CEO will not say PA failed in enforcement duties, but admits it has "
          "struggled. Interview with Johann Buttigieg.",
     "https://www.independent.com.mt/articles/2025-09-07/local-news/CEO-will-not-say-PA-failed-in-enforcement-duties-but-admits-it-has-struggled-6736272936"),
    ("2", "MEPA (2004). Annual Report and Accounts 2004: Enforcement Statistics (notices 2001–2004).", M + "MEPA-Annual-Report-2004.pdf"),
    ("3", "MEPA (2005). Annual Report and Accounts 2005: table 3; complaints.", M + "Annual-Report-2005.pdf"),
    ("4", "MEPA (2006). Annual Report and Accounts 2006: Enforcement.", M + "MEPA-_AnnualReport2006.pdf"),
    ("5", "MEPA (2007). Annual Report 2007: Follow up of Stop/Enforcement Notices.", M + "MEPA-Annual-Report-2007.pdf"),
    ("6", "MEPA (2009). Annual Report 2009: Enforcement; Gozo Office.", M + "Annual-Report-2009.pdf"),
    ("7", "MEPA (2010). Annual Report 2010: Enforcement Notices.", M + "MEPA-AR2010a.pdf"),
    ("8", "MEPA (2011). Annual Report 2011: Enforcement Directorate.", M + "Annual-Report-2011-Final.pdf"),
    ("9", "Planning Authority (2025). Annual Report 2024: Compliance Enforcement Directorate, pp. 28–30.",
     "https://www.parlament.mt/media/134019/pa-annual-report-2024.pdf"),
    ("10", "MaltaToday (2021). Planning Authority received 9 reports on illegalities each day in 2020. (Report of "
           "the PA Annual Report 2020; second-hand ◆.)",
     "https://www.maltatoday.com.mt/environment/environment/109955/planning_authority_received_9_reports_on_illegalities_each_day_in_2020"),
    ("11", "The Malta Independent (31 Jan 2022). Planning Authority says there are over 5,000 pending enforcement "
           "notices. (PA data; second-hand ◆.)",
     "https://www.independent.com.mt/articles/2022-01-31/local-news/Planning-Authority-says-there-are-over-5-000-pending-enforcement-notices-6736240240"),
    ("12", "MaltaToday (2024). Planning Authority yet to collect €674,740 from pending enforcement notices. "
           "(Parliamentary answer; second-hand ◆.)",
     "https://www.maltatoday.com.mt/news/national/127957/planning_authority_yet_to_collect_674740_from_pending_enforcement_notices"),
    ("13", "MaltaToday (2025). 2,400 reports of suspected illegal works in 2024. (Report of the PA Annual Report 2024.)",
     "https://maltatoday.com.mt/environment/townscapes/134952/2400_reports_of_suspected_illegal_works_in_2024"),
    ("14", "Gray W.B., Shimshack J.P. (2011). The effectiveness of environmental monitoring and enforcement: a review "
           "of the empirical evidence. <i>Review of Environmental Economics and Policy</i> 5(1):3–24. "
           "doi:10.1093/reep/req017. (Abstract read.)", "https://doi.org/10.1093/reep/req017"),
    ("15", "Gunningham N. (2017). Compliance, deterrence and beyond. In <i>Compliance and Enforcement of "
           "Environmental Law</i>, Edward Elgar, pp. 63–73. doi:10.4337/9781783477685.iv.4. (Abstract read.)",
     "https://doi.org/10.4337/9781783477685.iv.4"),
    ("16", "Ayres I., Braithwaite J. (1992). <i>Responsive Regulation</i>. Oxford University Press. "
           "doi:10.1093/oso/9780195070705.001.0001. (Cited via [15] ◆.)", ""),
    ("17", "MiŻien. Data and calculations: data/cc-014/; tools/cc-014-report/calc.py.", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "3 Oct 2026", "First issue. Draft pending right of reply from the Planning Authority.")])

build_report(Report(
    number="014", out=str(FIG / "report.pdf"), kicker="Planning enforcement",
    title_lines=["Fewer notices,", "or fewer", "illegalities?"],
    subtitle_lines=["Testing a public claim about planning enforcement in Malta", "against twenty years of annual reports"],
    quote_lines=["“We had times when we issued over 1,000", "enforcement notices per year.”"], quote_size=16,
    attribution="Johann Buttigieg, Planning Authority CEO, The Malta Independent, 7 September 2025.",
    context="Now around 200, which he attributed to fewer illegalities.",
    verdict="Misleading", verdict_note="Accurate figures; the explanation leaves out how cases are now handled",
    footer_lines=["Version 1.0  ·  3 October 2026", "Status: draft for right of reply (Planning Authority)",
                  "Prepared from public sources and annual reports.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Enforcement notices and illegalities – Malta", version="1.0", date="3 October 2026",
    pdf_title="Fewer notices, or fewer illegalities? Claim Check 014",
    pdf_subject="Tests the Planning Authority CEO's claim that fewer enforcement notices reflect fewer illegalities",
    story=S))
