"""Claim Check 086 report. Run calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []
MAROON = PLEDGE_COLS[5]

# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("On 14 April 2025 the Minister for Tourism, Ian Borg, told The Shift that Comino’s kiosks and beach concessions "
        "would stay as they were for the 2025 season, adding: <b>“However, starting in the summer of 2026, everyone will "
        "have to compete and pay the right price.”</b> [1] On 8 February 2026 the Malta Tourism Authority (MTA) told the same "
        "outlet that no competitive tenders would be issued that summer: “this will have to wait until we have the "
        "permit” [2]. We checked whether the promise was kept.", lead)]
S.append(key_points([
    ("The promise had a date and a scope.",
     "“Starting in the summer of 2026”, “everyone” (the kiosk and beach-concession operators on Comino) would compete "
     "in a tender [1]. That is measurable."),
    ("The MTA itself said it would not happen.",
     "Four months before the season, an MTA spokesperson said no competitive tenders for kiosks or beach concessions "
     "would be issued in summer 2026, because the MTA’s planning application (PA00738/26) was not yet approved [2]."),
    ("Nothing we could find shows a change since.",
     "The Shift’s report of 24 June 2026 describes the same ad hoc extensions [3]; we found no tender notice for the "
     "kiosks (search log in the literature notes). Summer ended 42 days before this check."),
    ("The number of kiosks cannot be tested.",
     "The Minister gave “around 11” in March 2025 and the MTA still speaks of reducing them “radically” [4, 2]; "
     "we found no later count."),
    ("Pledge label: Missed (moderate confidence).",
     "The deadline passed and the MTA’s own statement and a later report show the tender did not take place. The "
     "evidence is outlets’ quotations of the MTA, not an MTA document."),
]))
S += [Spacer(1, 1 * mm), VerdictMeter(5, scale="pledge"), Spacer(1, 2 * mm),
      tiles([("300", GREEN, "days between the pledge (14 Apr 2025) and the MTA’s statement that no tender would come (8 Feb 2026)"),
             ("0", RED, "kiosk or beach-concession tender notices found for summer 2026"),
             ("11", ORANGE, "kiosks in the Minister’s March 2025 figure; no later count found"),
             ("42", GREEN, "days between the end of meteorological summer (31 Aug) and this check")]),
      Spacer(1, 3 * mm),
      up_down("A tender notice for the Comino kiosks or beach concessions issued, with an award, for the 2026 season "
              "(a date before 31 Aug 2026), or an MTA record showing competitive procedures we have not found. The label would move to Met if so.",
              "Nothing lower on the scale: Missed is the end of it. A document showing the pledge was changed in "
              "writing before the deadline would take it out of the check.",
              heads=("What would move the label up", "What would move it down")),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the record shows"),
          ("4", "Where the evidence points different ways"), ("5", "Testing the claim"),
          ("6", "Pledge label and requests for evidence"), ("7", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("Our record came from a Lovin Malta report of 3 March 2025 [4], which states, in its headline, that the Minister pledges a revamp "
           "of Comino’s kiosks, and from a record paraphrase: “from 2026 all Comino kiosks and encroached public spaces will "
           "be awarded through competitive tenders and their number reduced”. That sentence is the intake’s paraphrase, not the "
           "speaker’s wording. We therefore rate the Minister’s own words, quoted in The Shift on 14 April 2025 [1], and "
           "treat the rest as context."))
S.append(std_table([
    [C("What was said", cellh), C("Who, where, when", cellh), C("Form", cellh)],
    [C("“However, starting in the summer of 2026, everyone will have to compete and pay the right price.”"),
     C("Minister Ian Borg; The Shift, 14 Apr 2025 [1]"), C("Quotation")],
    [C("“When I took over this responsibility, it was already too late to conduct a proper tendering process”; “We did "
       "not have enough time to change the situation this year.”"), C("Ian Borg; The Shift, 14 Apr 2025 [1]"),
     C("Quotation")],
    [C("“A competitive process (tender) is in the process so that everyone would have the chance to compete”"),
     C("Spokesperson for the Minister; The Shift, 28 Feb 2025 [5]"), C("Quotation")],
    [C("“The Malta Tourism Authority has annual concessions with around 11 kiosks, but this might be too many”"),
     C("Ian Borg; Lovin Malta, 3 Mar 2025 [4]"), C("Quotation")],
    [C("The MTA is considering limiting the number of kiosks and a standard design"),
     C("The Shift, 14 Apr 2025 [1]"), C("Outlet’s paraphrase")],
    [C("The Minister’s statement in the Lovin Malta video that he would eventually redesign the kiosks"),
     C("Lovin Malta, 3 Mar 2025 [4]"), C("Outlet’s paraphrase")],
], [100 * mm, 44 * mm, 26 * mm]))
S.append(P("<b>What we rate.</b> One pledge: that from summer 2026 the Comino operators would compete for their concessions "
           "in a tender. “Everyone” and “the right price” point to the kiosks and beach concessions the article was about. "
           "Reducing the number of kiosks is not in the Minister’s quoted words as a commitment, so it is context and not "
           "rated."))
S += [Spacer(1, 2 * mm),
      callout([P("SCOPE AND FAIRNESS", tag),
               P("This check is about a statement on public concessions, not about any operator or about the island’s planning "
                 "status, which is before a tribunal (CC-002) and not discussed here. Earlier ministers made similar promises "
                 "(The Shift, 8 Feb 2026 [2]); we assess this Minister’s statement, not the people. The MTA’s own explanation "
                 "for the delay is reported in Section 3.", small)],
              bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Question.</b> Did Comino’s kiosks and beach concessions go to competitive tender from summer 2026, as the Minister "
           "said they would?"))
S.append(P("<b>Evidence.</b> Two outlets’ reports of the Minister’s words [1, 4]; the MTA’s own statement of 8 February 2026, "
           "quoted by The Shift [2]; The Shift’s reports of 28 February 2025 and 24 June 2026 [5, 3]; the MTA’s Blue Lagoon "
           "Strategic Plan page [6], which names summer 2026 as the date for completing the transformation. We looked for a tender "
           "notice in web searches and a tender aggregator’s listings of MTA procurement for Comino (search log in "
           "<i>literature/CC-086/notes.md</i>). The dates are transcribed in <i>data/cc-086/statements.csv</i> and the date "
           "arithmetic recomputed by <i>tools/cc-086-report/calc.py</i> into <i>checks.csv</i>."))
S.append(P("<b>Literature.</b> We searched Crossref and OpenAlex for peer-reviewed studies of kiosk or concession tendering on "
           "Mediterranean protected islands and found none to rely on. The general economics of franchise bidding "
           "(Williamson 1976 [7]) concerns whether competition for a concession can replace regulation; it does not bear on "
           "whether this tender took place, so we use it only as background. <b>Grades:</b> statements quoted in outlets are "
           "grade D (assertion) for what will happen and grade C for what an authority said it had decided; Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(70 * mm))
S.append(SectionHeading(3, "What the record shows"))
S.append(fig(str(FIG / "fig1_timeline.png")))
S.append(P("Figure 1. Statements about Comino’s kiosks, 2025–2026. Sources [1–5]; dates in data/cc-086/statements.csv.", small))
S.append(P("<b>2025.</b> The Minister said in March 2025 that the MTA gave about 11 annual kiosk concessions and that this “might "
           "be too many” [4]. In April 2025 he said it was too late for a tender that year and that “starting in the summer of "
           "2026, everyone will have to compete and pay the right price” [1]. The Shift reported that the MTA was considering "
           "limiting the number of kiosks (outlet’s paraphrase) [1]."))
S.append(P("<b>February 2026.</b> An MTA spokesperson told The Shift: “The intention remains to reduce kiosks radically and to "
           "issue beach concessions through a competitive tendering process. However, this will have to wait until we have the "
           "permit.” The outlet reports the MTA as confirming that no competitive tenders for kiosks or beach concessions would be "
           "issued that summer, and that the MTA’s planning application PA00738/26, filed in 2025, was at an early stage "
           "with no timeline (its paraphrase; we did not open the Planning Authority’s record, which is browser-only) [2]."))
S.append(P("<b>June 2026.</b> The Shift reported on 24 June that the kiosks have lacked valid Planning Authority permits since at "
           "least 2015 and that beach concessions continued through ad hoc arrangements extended annually [3]. It reported no "
           "tender. We found, in the places listed in the notes, no kiosk or beach-concession tender notice between February "
           "and 12 October 2026; this is a search result, not proof of absence (Section 7). MTA procurement for Comino that "
           "we did find concerned security, cleaning and visitor wristbands [8]."))

# ================================================================== 4
S.append(CondPageBreak(60 * mm))
S.append(SectionHeading(4, "Where the evidence points different ways"))
S.append(contested("Did the pledged tender happen?", "NO TENDER FOUND", RED,
    "The Minister’s words set summer 2026 as the date [1]. The MTA’s strategic plan page also says the transformation "
    "will be complete “by summer 2026” [6] (the page carries no publication date).",
    "The MTA said in February 2026 that tenders must wait for the planning permit and that the intention remains [2]. "
    "That is a stated reason for delay, and the intention may still be carried out. A tender after summer 2026 would not "
    "meet the promised date.",
    "The MTA’s own statement and a later report agree that the 2026 season ran without tenders; no document shows otherwise. "
    "The pledge was dated; the deadline passed.",
    label_a="WHAT THE MINISTER SAID", label_b="WHAT THE MTA SAID LATER"))

# ================================================================== 5
S.append(CondPageBreak(60 * mm))
S.append(SectionHeading(5, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> “starting in the summer of 2026, everyone will have to compete and pay the right price”"),
     C("MTA, 8 Feb 2026: no tenders for kiosks or beach concessions that summer; “this will have to wait until we have the "
       "permit”. The Shift, 24 Jun 2026: same ad hoc extensions; no tender found since [2, 3]."),
     verd("MISSED", MAROON)],
    [C("<b>B.</b> Context: the number of kiosks to be reduced (the record’s paraphrase)"),
     C("Minister: “around 11 kiosks, but this might be too many” (Mar 2025); the MTA “intention remains to reduce kiosks "
       "radically” (Feb 2026). No later count found; not a pledge in the Minister’s quoted words [4, 2]."),
     verd("NOT RATED", GREY)],
    [C("<b>C.</b> Reason given for the delay: the planning permit"),
     C("MTA: it “will have to wait until we have the permit” [2]. The application’s status is the outlet’s paraphrase; the "
       "Planning Authority record was not opened ◆."),
     verd("NOT RATED", GREY)],
], [56 * mm, 84 * mm, 30 * mm], valign="MIDDLE"))

# ================================================================== 6
S += [CondPageBreak(60 * mm), Spacer(1, 4 * mm), SectionHeading(6, "Pledge label and requests for evidence"),
      verdict_box("Missed", "The tender promised from summer 2026 did not take place, by the MTA’s own account. "
                  "As of 12 Oct 2026. Confidence: moderate."),
      Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) The pledge is measurable: a competitive tender for the kiosks and beach concessions, from summer 2026. "
           "(2) Its date has passed: summer ended on 31 August (42 days before this check), or on 30 September on the most "
           "generous reading (12 days). (3) The MTA said in February that no tender would be issued that summer and gave a "
           "reason; The Shift’s June report shows the same arrangements; we found no tender notice. Under the scale, <i>Missed</i> "
           "needs a passed deadline and documents or data that can be shown: these are the MTA’s statement and the reports "
           "listed in the evidence box, which we read in full. (4) Confidence is moderate because the evidence is outlets’ "
           "quotation of the MTA, not an MTA document, and our search of tender notices was not exhaustive."))
S.append(callout([P("PLEDGE LABEL: MISSED (AS OF 12 OCT 2026)", tag),
                  P("A pledge can still be met later (the MTA says the intention remains); the label then moves to Met only if a "
                    "tender is shown, and the report will say it was late. The label rates the date the Minister gave.", small)],
                 bg=BLUE_PALE, bar=BLUE))
S.append(P("<b>What this does not say.</b> It does not say the planning permit delay was avoidable, nor that the policy of "
           "tendering is right or wrong, nor anything about an operator."))
S.append(KeepTogether([P("Evidence we are asking for", h2), requests_list([
    "Malta Tourism Authority: whether any tender or call for the Comino kiosks and beach concessions was published for 2026, "
    "with its date and result.",
    "Malta Tourism Authority: the number of kiosk concessions in 2025 and 2026, and the status of application PA00738/26.",
    "Ministry for Tourism: the text of the press statement of February 2025 on competitive tenders from 2026, which we could "
    "not find in a readable outlet.",
])]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag),
               P("Pending right of reply. The maintainer will decide whether and how to invite a response from the Ministry for "
                 "Tourism and the MTA. A <i>Missed</i> label is not circulated beyond this site before the reply period has passed.",
                 small)], bg=AMBER_PALE, bar=AMBER)]

# ================================================================== 7
S += [Spacer(1, 5 * mm), SectionHeading(7, "Limitations")]
for l in ["gov.mt, mta.com.mt news pages and the Planning Authority’s site are browser-only for scripts, and the Wayback Machine "
          "reset connections; the Ministry’s press statement of February 2025 and the MTA’s tender page were not read. The "
          "MTA’s February 2026 words are as The Shift printed them.",
          "We found no tender notice, but searches of the web and of a tender aggregator are not a search of the government’s "
          "eTenders portal; an award we did not find would move the label.",
          "“The summer of 2026” is not defined by the Minister; we show the 31 August and 30 September readings.",
          "The Strategic Plan page [6] is undated; we use it only to show that the MTA itself named summer 2026."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Camilleri, I. (14 Apr 2025). Illegal kiosks on protected Comino to be allowed another year, despite promises. "
          "The Shift. Read in full 12 Oct 2026.",
     "https://theshiftnews.com/2025/04/14/illegal-kiosks-on-protected-comino-to-be-allowed-another-year-despite-promises"),
    ("2", "Camilleri, I. (8 Feb 2026). Broken promise as Comino illegal concessions to stay put for another summer. The Shift. "
          "Read in full 12 Oct 2026.",
     "https://theshiftnews.com/2026/02/08/broken-promise-as-comino-illegal-concessions-to-stay-put-for-another-summer/"),
    ("3", "The Shift (24 Jun 2026). Visit Malta officials filmed telling citizens to leave deckchair-occupied beach in Comino. "
          "Read 12 Oct 2026.",
     "https://theshiftnews.com/2026/06/24/visit-malta-officials-filmed-telling-citizens-to-leave-deckchair-occupied-beach-in-comino/"),
    ("4", "Lovin Malta (3 Mar 2025). Watch: No More Vans? Ian Borg Pledges Major Comino Kiosk Revamp. Read 12 Oct 2026.",
     "https://lovinmalta.com/news/watch-no-more-vans-ian-borg-pledges-major-comino-kiosk-revamp/"),
    ("5", "Camilleri, I. (28 Feb 2025). Yet another promise to address Comino concession problems. The Shift. Read 12 Oct 2026.",
     "https://theshiftnews.com/2025/02/28/yet-another-promise-to-address-comino-concession-problems/"),
    ("6", "Malta Tourism Authority (undated; © 2026). Blue Lagoon Strategic Plan. Read 12 Oct 2026.",
     "https://mta.com.mt/blue-lagoon-strategic-plan/"),
    ("7", "Williamson, O. E. (1976). Franchise Bidding for Natural Monopolies – in General and with Respect to CATV. "
          "<i>The Bell Journal of Economics</i> 7(1):73. doi:10.2307/3003191. Abstract read; background only.",
     "https://doi.org/10.2307/3003191"),
    ("8", "◆ Tender aggregator listings of MTA procurement for Comino (CT2029/2026 security; wristbands SPD2/2026/009 and /024), "
          "seen in a search summary 12 Oct 2026; not opened.", ""),
    ("9", "Miżien. Data and calculations: data/cc-086/; tools/cc-086-report/calc.py (checks.csv).", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or official "
                "statistics · D assertion or anecdote. ◆ marks a source known only second-hand (used for context only, "
                "never for a deciding figure).", pledges=True)
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "12 Oct 2026", "First issue. Pledge label Missed (moderate). Pending right of reply.")])

build_report(Report(
    number="086", out=str(FIG / "report.pdf"), kicker="Tourism and concessions",
    title_lines=["Comino kiosks:", "a tender from", "summer 2026?"],
    subtitle_lines=["Testing the Minister for Tourism’s 2025 promise against", "the Malta Tourism Authority’s own later statement"],
    quote_lines=["“However, starting in the summer of 2026,", "everyone will have to compete and pay", "the right price.”"],
    quote_size=14.5, title_size=34,
    attribution="Ian Borg, Minister for Tourism, as quoted by The Shift, 14 Apr 2025.",
    context="On Comino’s kiosks and beach concessions, which stayed unchanged in 2025.",
    verdict="Missed", verdict_note="No tender for summer 2026, by the MTA’s own account",
    footer_lines=["Version 1.0  ·  12 October 2026", "Status:",
                  "Prepared from public sources, quoted outlets and the MTA’s Blue Lagoon Strategic Plan page.",
                  "Pledge label: missed (as of 12 Oct 2026).  Repository: github.com/leandergrech/Mizien"],
    running_head="Comino kiosks and tenders", version="1.0", date="12 October 2026",
    pdf_title="Comino kiosks: a tender from summer 2026? Claim Check 086",
    pdf_subject="Tests the Minister for Tourism's April 2025 promise of competitive tenders for Comino kiosks from summer 2026",
    story=S))
