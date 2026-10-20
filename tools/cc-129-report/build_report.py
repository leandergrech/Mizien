"""Claim Check 129 report. Run calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
verd = lambda t, c: chip(t, c, w=29 * mm)
S = []
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("In its July 2025 infringements package the European Commission opened a case against Malta, INFR(2025)2088, "
        "for failing to update its national air pollution control programme (NAPCP). It said: <b>“To date, these Member "
        "States have not submitted to the Commission the required updates.”</b> We checked what the Directive requires, "
        "whether the case exists, and what happened afterwards.", lead)]
S.append(key_points([
    ("The case exists and the wording is the Commission’s own.",
     "Malta is named, with INFR(2025)2088, among six Member States that received letters of formal notice on 17 July 2025."),
    ("The legal duty is clear.",
     "Directive 2016/2284 Article 6(3) requires an update at least every four years; the first programmes were due on "
     "1 April 2019. On either reading of the start date, the update was over a year late in July 2025."),
    ("We could not see the submission record.",
     "That Malta had submitted nothing is the Commission’s statement. Its NAPCP page lists the programmes it holds "
     "for each country, but the links are in an application we could not read. A letter of formal notice is a first step, "
     "not a finding by the Court."),
    ("Malta’s own draft update appeared in June 2026 ◆.",
     "A Malta News Agency report of 17 July 2026 describes a revised programme issued for public consultation. We did "
     "not open the programme; no later step in INFR(2025)2088 was found in the packages we read."),
    ("Verdict: largely supported (moderate confidence).",
     "The statement is what the Commission said and fits the legal timetable; the submission record is not independently seen."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("6", GREY, "Member States in the same letters of formal notice, 17 Jul 2025"),
             ("27.5 mo", AMBER, "From 1 Apr 2023 (four years after the first due date) to the notice"),
             ("16.5 mo", AMBER, "From Mar 2024 (four years after the March 2020 version ◆) to the notice"),
             ("Jun 2026", GREY, "Draft update consulted ◆")]),
      Spacer(1, 4 * mm),
      up_down("None: the statement is accurate as far as we can see; ‘Supported’ needs the submission record itself (Reportnet or the "
              "Commission’s NAPCP library) showing no update before 17 July 2025.",
              "A record showing an update submitted before 17 July 2025, or the Commission closing the case as based on an error."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the record shows"),
          ("4", "What the statement does not say"), ("5", "Testing the claim"),
          ("6", "Verdict and requests for evidence"), ("7", "Limitations")])
S.append(PageBreak())

S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The claim record quotes the July 2025 infringements package, as republished by the Commission’s Representation "
           "in Malta [1], which we read in full on 20 October 2026. The passage, with its heading, is: "))
S.append(P("“Commission calls on Member States to update their national air pollution control programmes (NAPCP) to reduce "
           "the emissions of certain atmospheric pollutants.” The Commission “decided to open infringement procedures by "
           "sending letters of formal notice to Croatia (INFR(2025)2085), Latvia (INFR(2025)2087), Hungary "
           "(INFR(2025)2086), Malta (INFR(2025)2088), Portugal (INFR(2025)2089) and Slovakia (INFR(2025)2090) for failing "
           "to respect their obligations under Directive 2016/2284”, adding: “To date, these Member States have not "
           "submitted to the Commission the required updates.” Malta then had “two months to respond”.", bul))
S.append(std_table([
    [C("Source", cellh), C("What it says", cellh), C("Our access", cellh), C("Status", cellh)],
    [C("<b>European Commission</b>, July infringements package, 17 Jul 2025 [1]"),
     C("Letters of formal notice to six Member States, Malta included, for not submitting the required NAPCP updates."),
     C("Page read in full, 20 Oct 2026."), C("<b>The claim</b>")],
    [C("<b>Directive (EU) 2016/2284</b>, Articles 6 and 10 [2]"),
     C("Update “at least every four years”; first programmes to the Commission by 1 April 2019."),
     C("Text read, 20 Oct 2026."), C("<b>Primary law</b>")],
    [C("<b>Commission</b>, NAPCP page [3]"),
     C("Updates “at least every four years”; the first were due 1 April 2019; submitted programmes are linked by country."),
     C("Page read; the country links open an application we could not read."), C("<b>Primary</b>")],
    [C("<b>Malta News Agency</b>, 17 Jul 2026 [4] ◆"),
     C("Reports a draft revised NAPCP issued for consultation in June 2026."),
     C("Read in full; the programme itself not opened."), C("<b>Second-hand</b>")],
], [38 * mm, 70 * mm, 40 * mm, 22 * mm]))

S += [Spacer(1, 4 * mm), SectionHeading(2, "Method")]
S.append(P("<b>Question.</b> Did the Commission open this case, was an update due, and is there any sign Malta has since "
           "acted? <b>Evidence.</b> We read the Commission’s text, the Directive and the Commission’s NAPCP page. We then "
           "searched the Commission’s monthly packages for later steps in INFR(2025)2088 (Section 3 and "
           "<i>literature/CC-129/notes.md</i>) and computed how late the update was under two readings of the start date "
           "(<i>tools/cc-129-report/calc.py</i>; <i>data/cc-129/checks.csv</i>). Article 6(3) does not say from which date the four "
           "years run, so we show both. <b>Grades.</b> Law and Commission texts, grade C; the news report is second-hand. "
           "No scientific literature is needed for a procedural statement; emission levels are not tested here."))

S.append(CondPageBreak(100 * mm))
S.append(SectionHeading(3, "What the record shows"))
S.append(fig(FIG / "fig1_timeline.png", width=CW * 0.97))
S.append(P("Figure 1. Timeline of the update obligation and the case. Reading A counts four years from the first due date "
           "(1 April 2019); reading B counts four years from the March 2020 version of Malta’s programme, known to us only "
           "from a search listing of ERA’s page (◆; month only; the page returns 403 to scripts).", cap))
S.append(P("Under reading A the update was due on 1 April 2023 and the notice came 27.5 months later; under reading B, "
           "16.5 months later. Either way the Commission’s statement of lateness fits the dates."))
S.append(P("<b>Later steps.</b> The next step after a letter of formal notice would be a reasoned opinion. We read the "
           "Commission’s key-decisions texts for December 2025 [5], January, March, April, June, July and October 2026 and "
           "found no reasoned opinion on the NEC Directive for Malta. The packages for September and October 2025 and "
           "February and May 2026 were not retrievable, and the Commission’s infringement register did not answer our "
           "request, so we cannot say the case has not moved or closed. Packages do not list closures of cases."))
S.append(P("<b>Malta’s response.</b> A Malta News Agency report of 17 July 2026 [4] ◆ says the Environment and "
           "Resources Authority issued a draft revised NAPCP for consultation in June 2026. Directive Article 6(5) requires public "
           "consultation on drafts, so this is consistent with an update in preparation in 2026, not with one "
           "submitted by July 2025. We did not read the programme or find a submission date."))

S.append(Spacer(1, 4 * mm))
S.append(SectionHeading(4, "What the statement does not say"))
S.append(P("It does not say Malta is exceeding any emission ceiling; the infringement concerns the update and its "
           "submission. A letter of formal notice states the Commission’s preliminary view and invites a reply; it is not a "
           "ruling. The same press report [4] ◆ says Malta is on track for most pollutants but not for nitrogen oxides in 2030: "
           "that is a different question, which this check does not test. Related checks: CC-034 and CC-035 (air quality)."))

S.append(CondPageBreak(90 * mm))
S.append(SectionHeading(5, "Testing the claim"))
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> The Commission opened INFR(2025)2088 against Malta on 17 July 2025"), C("Commission [1]"),
     C("Page names Malta and the case number in the letters of formal notice."), verd("ACCURATE", GREENC)],
    [C("<b>B.</b> The NEC Directive requires NAPCP updates at least every four years"), C("Commission [1]"),
     C("Article 6(3) of the Directive says so [2]; first programmes were due 1 April 2019."), verd("ACCURATE", GREENC)],
    [C("<b>C.</b> “To date” Malta had not submitted the required update"), C("Commission [1]"),
     C("Consistent with the legal timetable and with a draft update appearing in 2026 ◆; submission record not seen."),
     verd("NOT TESTED", AMBER)],
], [42 * mm, 18 * mm, 76 * mm, 34 * mm], valign="MIDDLE"))

S += [Spacer(1, 6 * mm), SectionHeading(6, "Verdict and requests for evidence"),
      verdict_box("Largely supported", "The case and the legal duty are confirmed; the submission record is not independently seen. Confidence: moderate."),
      Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> The substance backs the Commission’s statement with one minor gap: we could not open the record of "
           "what Malta had submitted. <b>What this verdict does not say.</b> It does not say Malta has breached the Directive "
           "in a legal sense, nor that its air pollution is above any limit."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "From the Commission or the Environment and Resources Authority: the date of Malta’s latest NAPCP submission and the status of INFR(2025)2088.",
    "From ERA: the 2026 draft programme and the date it is to be sent to the Commission."]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag), P("Not needed for this verdict (maintainer rule of 5 October 2026).", small)],
              bg=AMBER_PALE, bar=AMBER)]
S += [Spacer(1, 6 * mm), SectionHeading(7, "Limitations")]
for l in ["The Commission’s NAPCP library and Reportnet, which show submission dates, were not readable by us; ERA’s site "
          "returns 403 to scripts, so the 2019–2020 programme and the 2026 draft were not opened.",
          "The March 2020 date and the June 2026 consultation are second-hand (◆), month only.",
          "Not found does not mean absent: our search for later steps covered the packages listed in Section 3 only."]:
    S.append(P("• " + l, bul))
S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "European Commission, Representation in Malta (17 Jul 2025). July infringements package: key decisions.",
     "https://malta.representation.ec.europa.eu/news/july-infringements-package-key-decisions-2025-07-17_en"),
    ("2", "Directive (EU) 2016/2284 of the European Parliament and of the Council on the reduction of national emissions "
          "of certain atmospheric pollutants (CELEX 32016L2284), Articles 6 and 10, retrieved 20 Oct 2026.",
     "http://publications.europa.eu/resource/celex/32016L2284"),
    ("3", "European Commission, DG Environment. National Air Pollution Control Programmes (NAPCP), retrieved 20 Oct 2026.",
     "https://environment.ec.europa.eu/topics/air/reducing-emissions-air-pollutants/national-air-pollution-control-programmes-napcp_en"),
    ("4", "Malta News Agency (17 Jul 2026). Malta at risk of missing 2030 NOx emissions target, ERA warns. ◆ second-hand.",
     "https://www.maltanewsagency.com/2026/07/malta-at-risk-of-missing-2030-nox-emissions-target-era-warns/"),
    ("5", "European Commission, Representation in Malta (11 Dec 2025). December infringements package: key decisions "
          "(and the January, March, April, June, July and October 2026 packages; see notes.md).",
     "https://malta.representation.ec.europa.eu/news/december-infringements-package-key-decisions-2025-12-11_en"),
    ("6", "MiŻien. Calculation script and outputs: tools/cc-129-report/calc.py; data/cc-129/checks.csv.", ""),
])
S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "20 Oct 2026", "First issue. Verdict Largely supported (moderate confidence); no right of reply needed.")])

build_report(Report(
    number="129", out=str(FIG / "report.pdf"), kicker="Air quality and EU law",
    title_lines=["Malta’s air", "pollution", "programme"],
    subtitle_lines=["Testing the Commission’s July 2025 statement that", "Malta had not updated its NAPCP"],
    quote_lines=["“To date, these Member States have not submitted", "to the Commission the required updates.”"],
    quote_size=15,
    attribution="European Commission, July infringements package, 17 July 2025.",
    context="Letters of formal notice under the NEC Directive (INFR(2025)2088).",
    verdict="Largely supported", verdict_note="Case and duty confirmed; submission record not seen",
    footer_lines=["Version 1.0  ·  20 October 2026", "Status: no right of reply needed",
                  "Prepared from public sources.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Air pollution programme – European Commission", version="1.0", date="20 October 2026",
    pdf_title="Malta's air pollution programme? Claim Check 129",
    pdf_subject="Tests the Commission's July 2025 statement on Malta's NAPCP update",
    story=S))
