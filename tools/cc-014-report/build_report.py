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
        "MEPA and Planning Authority annual reports for 18 of the 24 years from 2001 to 2024, including every year "
        "since 2017.", lead)]
S.append(key_points([
    ("Both numbers are right.",
     "MEPA issued over 1,000 notices in five of the eight years we could read between 2001 and 2009 (1,369 in "
     "2001). The Planning Authority’s own reports give 164–233 a year from 2018 to 2024; the 2020–2024 average is 187."),
    ("Complaints did not fall the same way.",
     "Notices fell 82%. Complaints of illegal development averaged about 2,860 a year in 2017–2024, more than in "
     "2009 (2,701) or 2011 (2,105); only financial year 2004/05 (3,705) was higher (Figure 1)."),
    ("Confirmed illegal works are about where they were in 2018.",
     "About 1,280 complaints were confirmed as illegal development in 2018 and about 1,200–1,250 in 2024. The fall "
     "of about a third since 2020 is measured from a 2020–21 peak of about 1,820–1,880 (Figure 2)."),
    ("What changed is how cases end.",
     "Since 2018 only 7 to 13 in every 100 confirmed cases led to a notice; most ended in an application to sanction "
     "the works or removal by the owner. The Authority says so itself: it issues notices “only where contraveners "
     "are uncooperative” (2018 and 2019 reports)."),
    ("Verdict: misleading (moderate confidence).",
     "The figures are accurate, but presenting the fall in notices as a sign of fewer illegalities leaves out the "
     "main documented reason: a change in how the Authority handles them. Complaints are only a proxy for illegal "
     "building, and 2012–2016, when notices halved, is still missing."),
]))
S += [Spacer(1, 4 * mm), VerdictMeter(3), Spacer(1, 3 * mm),
      tiles([("1,033", GREEN, "Average notices a year, 2001–2009 (MEPA)"),
             ("187", GREY, "Average notices a year, 2020–2024 (Planning Authority)"),
             ("~1,200", RED, "Complaints confirmed as illegal development in 2024 (about 1,280 in 2018)"),
             ("7–13", ORANGE, "Notices per 100 confirmed cases, 2018–2024")]),
      Spacer(1, 4 * mm),
      up_down("An independent measure of illegal building (for example aerial-photo change detection) showing a fall "
              "of the same order as the fall in notices; or data for 2012–2016, when notices halved, showing confirmed "
              "cases falling in step.",
              "An independent measure showing illegal building rising while notices fell; or evidence that a growing "
              "share of illegal works is being regularised rather than removed."),
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
                 "enforcement and that there were “too many illegalities for the PA to enforce on everything”. The "
                 "Authority has described its persuasion-first strategy openly in every annual report since 2017 "
                 "(Section 3), and many cases now end with the owner removing or legalising the works without a "
                 "notice. This check is about whether fewer notices shows fewer illegalities, not about whether the "
                 "strategy is right.", small)],
              bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Question.</b> Is the fall from over 1,000 notices a year to about 200 accurate, and does the evidence "
           "show that it reflects fewer illegalities?"))
S.append(P("<b>Evidence.</b> We read the enforcement sections of the MEPA annual reports for 2004 to 2011 [2–8] and of "
           "every Planning Authority annual report from 2017 to 2024 [9–16]. The 2017–2023 reports are published only "
           "on Issuu; we downloaded their page images by script, read the Compliance and Enforcement Directorate pages, "
           "and recorded every value with its printed page, the image address and the image’s SHA-256 checksum (the "
           "images are not stored). Version 1.1 used news reports for 2019–2023; the primary values agree except for "
           "2019 notices (229, not the 228 we had derived) and 2023 complaints (2,463 received; the 2,456 reported in "
           "the news is the number closed). Every number is in <i>data/cc-014/</i> and every percentage is recomputed "
           "with <i>tools/cc-014-report/calc.py</i>. We searched Crossref and OpenAlex for studies of planning "
           "enforcement in Malta and found none; the regulatory literature [19–21] is context."))
S.append(P("<b>Confirmed cases.</b> Each year the Authority reports the share of complaints in which it found illegal "
           "development (about half to 59%) and how those cases ended. We multiply the stated share by complaints "
           "received. The reports are not always consistent: in 2019 the outcomes add up to 51% of complaints closed "
           "rather than received, and in 2023 to 48% against a stated 58%. Where removals are given only as a "
           "percentage (2020–2022) or as “the rest of the cases” (2018), we derive a count. Confirmed cases are "
           "therefore approximate."))
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
S.append(P("<b>The Authority’s own explanation.</b> Its annual reports describe the change openly. In 2017 it wrote "
           "of a gradual shift “away from a total Enforcement system”, with fewer notices and, it said, “a positive "
           "shift in compliance and self-regulation” [10, p. 18]; no measure of that shift is given. In 2018 and "
           "2019 it said the low number of notices was “in line with the strategy adopted by the Directorate to issue "
           "notices only where contraveners are uncooperative” [11, p. 20; 12, p. 18]. From 2020 it describes "
           "resolving infringements “through other means which are more efficient” [13, p. 28], and in 2022 calls "
           "persuasion “the main strategy” [15, p. 24]. This explains the fall in notices on the Authority’s own "
           "terms and supports the chief executive’s account of a deliberate change. It does not show that illegal "
           "building has fallen."))
S.append(P("Regulatory research supports both sides of the trade-off. Reviews of environmental enforcement find "
           "that inspections and sanctions deter future violations, both by the firm sanctioned and by others "
           "[19]. The “responsive regulation” tradition argues that regulators should start with persuasion and "
           "escalate only when that fails [20, 21]. Neither body of work treats a fall in sanctions as evidence, on "
           "its own, of a fall in violations."))

# ================================================================== 4
S.append(CondPageBreak(140 * mm))
S.append(SectionHeading(4, "What the data show"))
S.append(fig(FIG / "fig1_series.png"))
S.append(P("Figure 1. Enforcement notices issued (bars) and complaints of illegal development (dots), 2001–2024 "
           "[2–16]. Complaints did not fall in step with notices.", cap))
S.append(std_table([
    [C("Indicator", cellh), C("Then", cellh), C("Now", cellh), C("Change", cellh), C("Source", cellh)],
    [C("Notices a year (average)"), C("1,033 (2001–09)"), C("187 (2020–24)"), C("<b>−82%</b>"), C("[2–6, 9, 13–16]")],
    [C("Complaints of illegal development"), C("2,701 (2009)"), C("2,411 (2024)"), C("−11%"), C("[6, 9]")],
    [C("Complaints, longer run"), C("3,705 (FY 2004/05)"), C("2,411 (2024)"), C("−35%"), C("[3, 9]")],
    [C("Complaints a year (average)"), C("2,105–2,701 (2009, 2011)"), C("~2,860 (2017–24)"), C("higher"),
     C("[6, 8–16]")],
    [C("Notices per 100 complaints"), C("29–41 (2005–11)"), C("5–10 (2017–24)"), C("−77% (averages)"),
     C("calculated")],
    [C("Confirmed illegal cases"), C("~1,280 (2018)"), C("~1,200–1,250 (2024)"), C("−2% to −6%"), C("[9, 11]")],
    [C("Confirmed cases, from the peak"), C("~1,820–1,880 (2020–21)"), C("~1,200–1,250 (2024)"),
     C("−31% to −36%"), C("[9, 13, 14]")],
    [C("Notices per 100 confirmed cases"), C("not reported (MEPA)"), C("7–13 (2018–24)"), C("–"), C("[9, 11–16]")],
], [50 * mm, 36 * mm, 30 * mm, 22 * mm, 32 * mm]))
S.append(P("All values in <i>data/cc-014/checks.csv</i>. 2008 and 2012–2016 are missing: the 2012 and 2014 MEPA reports "
           "are scanned images and we found no readable report for 2013, 2015 or 2016. For 2024 the Authority reports "
           "“circa half” of 2,411 complaints as confirmed (about 1,206), but its four outcome categories sum to 1,252 "
           "(52%); hence the range.", cap))
S.append(CondPageBreak(135 * mm))
S.append(fig(FIG / "fig2_outcomes_by_year.png"))
S.append(P("Figure 2. Complaints confirmed as illegal development and how the cases ended, 2018–2024 [9, 11–16]. In "
           "every year 7–13 in every 100 confirmed cases ended in a notice. Confirmed cases in 2024 were close to "
           "2018; 2020 and 2021 were the peak.", cap))
S.append(fig(FIG / "fig3_ratio.png"))
S.append(P("Figure 3. Notices per 100 complaints: 29–41 in the MEPA years we could read, 5–10 under the Planning "
           "Authority since 2017.", cap))
S.append(P("Reading across the data", h2))
for t in ["• <b>The headline numbers are accurate.</b> “Over 1,000 a year” matches 2001, 2002, 2004, 2005 and "
          "2009; “around 200” matches every year from 2018 to 2024 (164–233). The Authority issued 315 in 2017.",
          "• <b>Complaints did not halve, let alone fall by four-fifths.</b> They were 2,105 in 2011, peaked at 3,313 "
          "in 2020 and were about 2,400 in 2023 and 2024. The Authority stopped accepting anonymous reports in 2024 "
          "[18]; in 2022 and 2023 it said about half of all complaints were anonymous [15, 16].",
          "• <b>Few confirmed cases end in a notice, and that has not changed since 2018.</b> The Authority confirmed "
          "roughly 1,200–1,900 illegal developments a year after complaints, and 7–13 in every 100 led to a notice. "
          "In 2024 about six times as many confirmed cases ended in a sanctioning application or removal by the owner "
          "(521 + 482 = 1,003) as in a notice (162); in 2019, eleven times (737 + 824 against 141) [9, 12].",
          "• <b>The steepest fall lies in the gap.</b> Notices halved between 2011 (618) and 2017 (315), years for "
          "which we found no readable report. The 2017 report already presents the move away from “a total Enforcement "
          "system” as the strategy of earlier years [10, p. 18]. MEPA’s 2007 report had attributed an earlier fall partly to closer "
          "monitoring of works in progress [5]; the 2024 report attributes the 18% fall that year to persuading "
          "contraveners first [9, 18]."]:
    S.append(P(t, bul))
S += [Spacer(1, 3 * mm),
      callout([P("FAIRNESS AND CONTEXT: DETERRENCE", tag),
               P("Daily fines on enforcement notices were introduced in 2012 [16, p. 24]. The share of new notices "
                 "carrying them rose from half in 2018 to about 78% in 2023 [11–16], and the Authority calls them “a "
                 "positive deterrent” [12–16]. Fewer notices that each carry a running fine could deter some illegal "
                 "building, which is consistent with the chief executive’s view, and research finds that sanctions "
                 "deter others as well as the offender [19]. The same 2023 report adds that the fines “need to be "
                 "revised to remain an effective financial deterrent today” [16, p. 24]. Neither point measures how "
                 "much illegal building there is.", small)],
              bg=AMBER_PALE, bar=AMBER)]

# ================================================================== 5
S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(5, "Where the evidence points different ways"))
S.append(contested(
    "Q1  Are there fewer illegalities than before?", "POSSIBLY SOME; NOT FOUR-FIFTHS FEWER", AMBER,
    "Complaints are lower than in 2004/05 (−35%), and confirmed cases fell by about a third from their 2020–21 peak. "
    "Most notices now carry daily fines, and in 2017 the Authority reported “a positive shift in compliance” [10]. "
    "Higher fines and the sanctioning route may have changed behaviour, as the chief executive says.",
    "Complaints averaged about 2,860 a year in 2017–2024, above 2009 (2,701) and 2011 (2,105). Confirmed cases in "
    "2024 (about 1,200–1,250) were close to 2018 (about 1,280), and between about 1,200 and 1,900 complaints a year "
    "were confirmed as illegal development throughout 2018–2024.",
    "<b>For this claim:</b> a modest fall in reported illegalities since the mid-2000s is plausible; a fall of the "
    "size implied by notices (−82%) is not supported by the Authority’s own figures."))
S.append(contested(
    "Q2  Why did notices fall?", "MAINLY A CHANGE IN PRACTICE", RED,
    "Fewer new illegalities would mean fewer notices. Owners now more often remove works once contacted, which is "
    "the outcome enforcement aims for.",
    "Notices per complaint fell about four-fold (33 to 7.6 per 100 on average). Every Planning Authority report since "
    "2017 explains the low number of notices by its strategy of issuing them only where contraveners do not "
    "cooperate; hundreds of cases a year end in applications to legalise the works [9–16].",
    "<b>For this claim:</b> the documented explanation is how cases are handled, which the statement does not "
    "mention."))
S.append(contested(
    "Q3  Do complaints measure illegal building?", "ONLY PARTLY", AMBER,
    "Complaints are the main way the Authority learns of illegal works, and the share confirmed (about half to 59%) "
    "is reported each year.",
    "Complaints depend on public vigilance and on rules that changed: construction-site complaints were counted "
    "separately in 2018, third-party-damage complaints were included in 2019, and anonymous reports (about half in "
    "2022–23) stopped in 2024. No independent count of illegal building, such as aerial-photo change detection, has "
    "been published.",
    "<b>For this verdict:</b> confidence is moderate because both sides rely on proxies."))

# ================================================================== 6
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(6, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> “We had times when we issued over 1,000 enforcement notices per year”"),
     C("1,369 (2001), 1,030 (2002), 1,061 (2004), 1,077 (2005), 1,120 (2009) [2–6]."), verd("ACCURATE", GREENC)],
    [C("<b>B.</b> Now around 200"), C("164–233 a year, 2018–2024 (191 in 2024); 315 in 2017 [9–16]."),
     verd("ACCURATE", GREENC)],
    [C("<b>C.</b> The fall is due to fewer illegalities"),
     C("Notices fell 82%; complaints fell 11–35% since 2004–09 and averaged about 2,860 a year in 2017–24. "
       "Confirmed cases in 2024 were close to 2018, and only 7–13 in 100 ended in a notice. The Authority attributes "
       "the fall to its strategy [9–16]."), verd("MISLEADING", colors.HexColor("#C85A3A"))],
    [C("<b>D.</b> Over 5,000 cases awaiting direct action; over 90 years to clear"),
     C("Pending notices: almost 7,000 (end 2018), 6,119 (2019), almost 5,600 (2020) [11–13]; 5,382 (end 2021) "
       "[17]. Notices closed by direct action: 27–135 a year in 2017–2020, mean 72 [10–13], which implies about 75 "
       "years. Consistent in size."), verd("BROADLY CONSISTENT", AMBER)],
    [C("<b>E.</b> 1,500 illegalities removed by direct action in 30 years"),
     C("Notices closed by direct action: 135, 52, 27 and 74 in 2017–2020 [10–13]. 1,500 in 30 years is 50 a year, "
       "the same order. No 30-year series found."), verd("PARTLY TESTED", GREY)],
], [52 * mm, 88 * mm, 30 * mm], valign="MIDDLE"))

# ================================================================== 7
S += [Spacer(1, 6 * mm), SectionHeading(7, "Verdict and requests for evidence"),
      verdict_box("Misleading", "Accurate figures; the explanation leaves out the main documented cause. Confidence: "
                  "moderate. Based on MEPA and Planning Authority annual reports, which can be shown."),
      Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) Both figures are accurate. (2) Complaints of illegal development fell far less than "
           "notices, and in 2024 about as many complaints were confirmed as illegal (about 1,200–1,250) as in 2018 "
           "(about 1,280). (3) Only 7–13 in every 100 confirmed cases now end in a notice, as more cases end in "
           "applications to legalise the works or in removal after contact, and the Authority’s own reports give that "
           "strategy as the reason for the low number of notices. Presenting the fall in notices as evidence of fewer "
           "illegalities therefore gives an inaccurate overall impression, which our scale calls <i>Misleading</i>."))
S.append(P("<b>What this verdict does not say.</b> It does not say that illegal building has increased, that the "
           "persuasion-first approach is wrong, or that anyone acted in bad faith. A fuller statement would read: "
           "<i>“We used to issue over 1,000 notices a year; now about 200, because we issue them only where owners do "
           "not cooperate, and most cases end in removal or a sanctioning application. Complaints are about 2,400 a "
           "year and about half are still confirmed as illegal.”</i>"))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "Complaints, confirmed cases, notices and outcomes for 2012–2016, when notices halved, to close the gap in the "
    "series.",
    "The base of the “confirmed” percentage each year, and counts (not only percentages) of cases closed by removal "
    "in 2020–2022.",
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
          "Authority rules, which changed (a reporting app was introduced; about half of complaints were anonymous in "
          "2022–23, and anonymous reports stopped in 2024).",
          "Definitions shift. MEPA reported by financial year until about 2006; the 2011 complaint count excludes sites "
          "already under a notice; the 2009 figures add the Gozo Office. The 2017 complaint count is rounded (3,000) "
          "and its 315 “enforcement notices” (192 + 123) do not match the 2018 report’s “15% fall” to 219, which "
          "implies about 258. The 2018 report counts 1,572 construction-site complaints and 310 construction-site stop "
          "notices separately; the 2019 count includes third-party-damage complaints.",
          "Confirmed cases are approximate: the stated share is applied to complaints received, the base of that share "
          "varies, the reported outcomes do not always add up to it, and removals for 2018 and 2020–2022 are derived. "
          "The 2020 report says complaints rose by 139 on 2019, but the 2019 report’s count implies 179.",
          "2008 and 2012–2016 are missing. Notices halved between 2011 and 2017, so the largest fall is not documented "
          "year by year; a steady decline or a sudden policy change in those years would not change the comparison of "
          "endpoints, but would change how it is explained.",
          "2024 values are from the 2024 report as read on 3 October 2026; it could not be re-read on 5 October "
          "(automated access blocked). Pending notices at the end of 2021 are second-hand [17].",
          "No peer-reviewed study of planning enforcement in Malta was found; the regulatory literature is used for "
          "context only and was read as abstracts."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
M = "https://era.org.mt/wp-content/uploads/2019/05/"
ISS = "https://issuu.com/planningauthority/docs/"
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
    ("10", "Planning Authority (2018). Annual Report 2017: Compliance and Enforcement Directorate, pp. 18–20. Read as "
           "page images on Issuu.", ISS + "pa_annual_report_2017"),
    ("11", "Planning Authority (2019). Annual Report 2018: Compliance &amp; Enforcement Directorate, pp. 20–24. Read as "
           "page images on Issuu.", ISS + "annual_report_2018_pa_march_final"),
    ("12", "Planning Authority (2020). Annual Report 2019: Compliance &amp; Enforcement Directorate, pp. 17–18. Read as "
           "page images on Issuu.", ISS + "annual_report_2019"),
    ("13", "Planning Authority (2021). Annual Report 2020: Compliance and Enforcement Directorate, pp. 27–29. Read as "
           "page images on Issuu.", ISS + "pa_2020_annual_report_v3"),
    ("14", "Planning Authority. Annual Report 2021 (on Issuu 9 Jan 2024): Compliance and Enforcement Directorate, "
           "pp. 28–29. Read as page images.", ISS + "pa_ar_2022_cmyk_single_page_ver2"),
    ("15", "Planning Authority. Annual Report 2022 (on Issuu 9 Jan 2024): Compliance &amp; Enforcement Directorate, "
           "pp. 23–24. Read as page images.", ISS + "20230117_pa_cd_annual_report_2022_web_final"),
    ("16", "Planning Authority (2025). Annual Report 2023: Compliance &amp; Enforcement Directorate, pp. 23–24. Read as "
           "page images on Issuu.", ISS + "pa_annual_report_2023"),
    ("17", "The Malta Independent (31 Jan 2022). Planning Authority says there are over 5,000 pending enforcement "
           "notices. (PA data; second-hand ◆.)",
     "https://www.independent.com.mt/articles/2022-01-31/local-news/Planning-Authority-says-there-are-over-5-000-pending-enforcement-notices-6736240240"),
    ("18", "MaltaToday (2025). 2,400 reports of suspected illegal works in 2024. (Report of the PA Annual Report 2024.)",
     "https://maltatoday.com.mt/environment/townscapes/134952/2400_reports_of_suspected_illegal_works_in_2024"),
    ("19", "Gray W.B., Shimshack J.P. (2011). The effectiveness of environmental monitoring and enforcement: a review "
           "of the empirical evidence. <i>Review of Environmental Economics and Policy</i> 5(1):3–24. "
           "doi:10.1093/reep/req017. (Abstract read.)", "https://doi.org/10.1093/reep/req017"),
    ("20", "Gunningham N. (2017). Compliance, deterrence and beyond. In <i>Compliance and Enforcement of "
           "Environmental Law</i>, Edward Elgar, pp. 63–73. doi:10.4337/9781783477685.iv.4. (Abstract read.)",
     "https://doi.org/10.4337/9781783477685.iv.4"),
    ("21", "Ayres I., Braithwaite J. (1992). <i>Responsive Regulation</i>. Oxford University Press. "
           "doi:10.1093/oso/9780195070705.001.0001. (Cited via [20] ◆.)", ""),
    ("22", "MiŻien. Data and calculations: data/cc-014/ (pa_enforcement_series.csv, pa_annual_reports_2017_2023.csv, "
           "outcomes_by_year.csv, checks.csv); tools/cc-014-report/calc.py.", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "3 Oct 2026", "First issue. Draft pending right of reply from the Planning Authority."),
                   ("1.1", "5 Oct 2026", "Corrections: (1) 2020 complaints were called “the highest in the series”; "
                    "now “the highest we could read after FY 2004/05 (3,705)”. (2) “More than three times as many” "
                    "cases ending in a sanctioning application or removal as in a notice → “about six times” "
                    "((521 + 482) / 162 = 6.2). (3) 2019 complaints 3,174 (derived from a news report) → 3,134 "
                    "(PA Annual Report 2019, p. 17; Figure 1 redrawn). (4) 2024 confirmed cases ~1,200 → "
                    "~1,200–1,250 and the 2020–24 change −34% → −31% to −34%, because the four outcome categories "
                    "sum to 1,252, more than the “circa half” (1,206) reported. Flyer: “Settled by legalising” → "
                    "“Applications to legalise” (applications, not permits). Verdict and confidence unchanged."),
                   ("1.2", "5 Oct 2026", "Upgrade: Planning Authority annual reports 2017–2023 read as Issuu page images "
                    "and used as the primary series in place of news reports [10–16]; each value recorded with printed "
                    "page, image URL and SHA-256. (1) Added 2017 (315 notices; about 3,000 complaints) and 2018 (219; "
                    "2,560); gap 2008 and 2012–2018 → 2008 and 2012–2016. (2) 2019 notices 228 (derived) → 229 "
                    "[12, p. 18]; 2023 complaints 2,456 → 2,463 (2,456 is complaints closed) [16, p. 23]; 2020–2023 "
                    "notices (169, 164, 180, 233) and 2020 complaints (3,313) confirmed; 2021 (3,192) and 2022 (2,804) "
                    "complaints added. (3) Notices per 100 complaints 29–42 (2005–11) and 5–10 (2019–24) → 29–41 "
                    "(rounding) and 5–10 (2017–24). (4) New: confirmed cases 2018–2024 with outcomes (Figure 2): "
                    "~1,280 in 2018 against ~1,200–1,250 in 2024, so the −31% to −34% since 2020 is now described as "
                    "from a 2020–21 peak (−31% to −36%); 7–13 notices per 100 confirmed cases. New Figure 3 (notices "
                    "per 100 complaints); Figure 1 redrawn; the 2024-only outcome chart is now part of Figure 2. "
                    "(5) Added the Authority’s stated policy (notices “only where contraveners are uncooperative”, "
                    "2018 p. 20, 2019 p. 18) and a deterrence note (daily fines since 2012 [16, p. 24]; on 50% → 78% "
                    "of notices, 2018 → 2023). (6) Sub-claim D now uses primary backlog and direct-action figures "
                    "(73 → about 75 years); E partly tested (27–135 a year, 2017–2020). (7) The “139 more complaints "
                    "in 2020” is in the Authority’s own 2020 report, not only in the news report. MaltaToday (2021, "
                    "2024) references replaced by the primary reports; references renumbered. Verdict and confidence "
                    "unchanged.")])

build_report(Report(
    number="014", out=str(FIG / "report.pdf"), kicker="Planning enforcement",
    title_lines=["Fewer notices,", "or fewer", "illegalities?"],
    subtitle_lines=["Testing a public claim about planning enforcement in Malta", "against twenty years of annual reports"],
    quote_lines=["“We had times when we issued over 1,000", "enforcement notices per year.”"], quote_size=16,
    attribution="Johann Buttigieg, Planning Authority CEO, The Malta Independent, 7 September 2025.",
    context="Now around 200, which he attributed to fewer illegalities.",
    verdict="Misleading", verdict_note="Accurate figures; the explanation leaves out how cases are now handled",
    footer_lines=["Version 1.2  ·  5 October 2026", "Status: draft for right of reply (Planning Authority)",
                  "Prepared from public sources and annual reports.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Enforcement notices and illegalities – Malta", version="1.2", date="5 October 2026",
    pdf_title="Fewer notices, or fewer illegalities? Claim Check 014",
    pdf_subject="Tests the Planning Authority CEO's claim that fewer enforcement notices reflect fewer illegalities",
    story=S))
