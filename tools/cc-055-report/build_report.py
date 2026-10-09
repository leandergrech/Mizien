"""Claim Check 055 report. Run calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []

# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("On 13 May 2026, the day the Government of Malta and MIDI plc signed the deed that ended the Manoel Island and Fort "
        "Tigné concession, Prime Minister Robert Abela said: <b>“We are transforming this area into a national park designed "
        "according to the wishes of the Maltese and Gozitan people”</b> (as Newsbook reported him). The claim record "
        "summarises this as: Manoel Island has been returned to public ownership from MIDI and will become a national park. "
        "We checked the return against MIDI’s own stock-exchange announcements and the news reports, and the park against "
        "what the law, the Planning Authority and the Government have published since.", lead)]
S.append(key_points([
    ("The return happened, and MIDI says so.",
     "MIDI’s announcement of 13 May 2026 says a public deed “was today entered into” by the Government, Transport Malta and "
     "the company “for the rescission and termination” of the concession over Manoel Island and Fort Tigné, “resulting in the "
     "return thereof to Government”. Parliament had approved the agreement and MIDI’s shareholders did so on 28 April [3, 7]."),
    ("The return is of the concession area, not every use on it.",
     "MIDI keeps the Tigné Point development [4]. A sports ground on the island is being sanctioned for padel courts, and the "
     "Prime Minister said the yacht yard was never part of the MIDI concession [12, 13 ◆]. None of this contradicts the "
     "return; it shapes what “public” means in practice."),
    ("“National park” is not defined in any law we searched.",
     "The word does not appear in the six Maltese Acts we searched, including the Environment Protection Act and the "
     "Development Planning Act [14]. We found no instrument, plan or local plan change for a Manoel Island national park, and "
     "no date. Newsbook and TVM News report that the local plan will be changed and that Heritage Malta is expected to draw up a management plan [1, 2]."),
    ("What we cannot tell.",
     "We did not read the deed or the shareholder circular, and our searches of the Planning Authority and Heritage Malta "
     "were by web search only. A plan may exist that we did not find."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(0), Spacer(1, 3 * mm),
      tiles([("13 May", GREEN, "2026: public deed ends the concession over Manoel Island and Fort Tigné (MIDI)"),
             ("€43m", GREY, "Net cost (MIDI: €47.3m gross, “circa” €43m net). Not part of the claim"),
             ("0 of 6", ORANGE, "Maltese Acts searched that use the term “national park”"),
             ("Not measurable", ORANGE, "Pledge label for “will become a national park”, as of 9 Oct 2026")]),
      Spacer(1, 4 * mm),
      up_down("None for the facts: Supported is the top of the scale. The pledge label could move to On track if a "
              "definition, plan or designation with a date is published.",
              "A deed or circular showing the Government kept no real control of the island, or reserved rights that "
              "limit public use, would lower the factual rating. A published plan with a deadline would let the "
              "pledge be rated against it (On track, Off track or Missed)."),
      Spacer(1, 3 * mm)]
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The claim record came from a MaltaToday headline, “Manoel Island officially returned as public land” [locator, "
           "page refused to scripts]. Following our rule to quote the speaker, not the headline, we read the readable reports of "
           "the signing day (13 May 2026) and the company’s own announcements. The Prime Minister’s words inside quotation marks "
           "are quoted below; everything else is the outlet’s text or the company’s announcement."))
S.append(std_table([
    [C("Source", cellh), C("What it says", cellh), C("Our access", cellh), C("Status", cellh)],
    [C("<b>Prime Minister Robert Abela</b>, as reported by Newsbook, 13 May 2026 [1]"),
     C("“We are transforming this area into a national park designed according to the wishes of the Maltese and Gozitan "
       "people.” Also: “We have placed the health and time of our citizens before money.” Newsbook says the Government will amend "
       "local plans so no development can take place on the island, and that Heritage Malta takes responsibility (outlet’s text)."),
     C("Read in full, 9 Oct 2026."), C("<b>The claim</b> (quoted words)")],
    [C("<b>TVM News</b>, 13 May 2026 [2]"),
     C("Abela called the signing a “historic moment”. TVM reports that the sites “have been returned to the Maltese public” and "
       "will fall under Heritage Malta (TVM’s text, not in quotation marks)."),
     C("Read in full."), C("Outlet report")],
    [C("<b>MIDI p.l.c.</b> company announcements, 17 Mar, 20 Mar and 13 May 2026 [3, 4, 5]"),
     C("In-principle agreement for partial rescission of the 2000 emphyteutical deed; reimbursement of €47,321,000, about €43 "
       "million net of VAT; the concession over Tigné Point (excluding Fort Tigné) stays in force. On 13 May a public deed was "
       "entered into, “resulting in the return thereof to Government”."),
     C("Read in full (PDFs; hashes in data/cc-055/documents.csv)."), C("<b>Primary (company disclosure)</b>")],
    [C("<b>TVM News</b>, 17 Mar and 28 Apr 2026 [6, 7]"),
     C("Lands Minister Owen Bonnici’s figures (€78m asked, €43m agreed) and next steps; Parliament approved the agreement "
       "unanimously “last March”; shareholders approved on 28 April. Abela called it another “dream come true”."),
     C("Read in full."), C("Outlet report")],
    [C("<b>Partit Nazzjonalista</b> statement, 17 Jul 2026 [11]"),
     C("Says no legal guarantee defines what a national park is or what is permitted in it."),
     C("Read in full."), C("Opposition view; tested in section 3")],
], [40 * mm, 72 * mm, 32 * mm, 26 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("WHAT WE COULD NOT READ", tag),
               P("The public deed itself, MIDI’s circular to shareholders of 6 April 2026, the parliamentary resolution, the "
                 "Office of the Prime Minister’s release and the Planning Authority’s decision on the padel courts were not "
                 "available to us (gov.mt and parlament.mt refuse scripts; the deed and circular are not linked from the "
                 "announcements we read). MaltaToday pages return 403; the 21 July remarks are known only through Lovin Malta’s "
                 "summary of MaltaToday ◆. Routes tried are in <i>literature/CC-055/README.md</i>.", small)],
              bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Questions.</b> (A) Was the MIDI concession over Manoel Island ended and the island returned to the Government? "
           "(B) Is the return complete as far as the public is concerned? (C) Is there anything published that makes “will "
           "become a national park” checkable?"))
S.append(P("<b>Evidence.</b> For A and B we read MIDI’s three announcements and the reports of the signing; the dates and the "
           "amounts are checked in <i>calc.py</i> (<i>data/cc-055/checks.csv</i>). For C we searched the consolidated texts of "
           "six Acts on legislation.mt for “national park” and “nature reserve” (Cap. 549, 552, 445, 504, 573 and 623; 9 October "
           "2026) and searched the web, TVM News’s and Lovin Malta’s Manoel Island pages and MIDI’s announcements for a plan, a "
           "designation or a local plan change; the search log is in <i>literature/CC-055/notes.md</i>."))
S.append(P("<b>The limit of C.</b> Not finding a document is weaker than reading one. Subsidiary legislation, the Planning "
           "Authority’s consultation pages, Heritage Malta’s website and the e-tenders portal were not searched directly."))
S.append(P("<b>Grades.</b> A company’s regulatory disclosure and statute text are grade C (primary, but not independently "
           "audited); news reports are grade D and are used to locate what was said. <b>Verdicts</b> and <b>pledge labels</b> "
           "follow Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(3, "What the evidence shows"))
S.append(P("<b>The return.</b> On 17 March 2026 MIDI announced an in-principle agreement for the partial rescission of the "
           "emphyteutical deed of 15 June 2000, so that the concession over Manoel Island and Fort Tigné is rescinded while the "
           "concession over Tigné Point (excluding Fort Tigné) stays in force [4]. On 20 March it said the terms had been agreed "
           "subject to Parliament and its shareholders [5]. TVM News reports that Parliament approved the agreement unanimously and "
           "that shareholders approved it on 28 April [7]. On 13 May MIDI announced that the public deed had been entered into, "
           "“resulting in the return thereof to Government” [3]. That is 57 days from the first announcement to the deed."))
S.append(fig(FIG / "fig1_timeline.png", width=CW * 0.98))
S.append(P("Figure 1. Steps from the in-principle agreement to the deed (green), and later events that bear on the park (grey). "
           "Sources: MIDI announcements [3, 4, 5]; TVM News [2, 7]; Lovin Malta [12, 13 ◆].", cap))
S.append(P("<b>The cost, for context.</b> The claim does not state a price, but reports differ. MIDI’s €47,321,000 is the gross "
           "reimbursement and “circa €43 million” the net figure after VAT [4]; Lands Minister Bonnici’s €43 million is “just over "
           "half” of the €78 million MIDI asked for (our check: 55.1%) [6]."))
S.append(P("<b>What the public now has.</b> TVM News reports the Prime Minister saying that the sites pass to the responsibility "
           "of Heritage Malta [2]. Not everything on the island is covered by a park. The Planning Authority approved the "
           "sanctioning of 20 padel courts and 10 more on the former Nicholl football ground on 16 July 2026 [12], and the "
           "Prime Minister said that area had always been a sports facility and that the yacht yard, on the Sliema side, was "
           "outside the MIDI concession [13 ◆]. These are uses within or beside the returned land, not a reversal of the return."))
S.append(P("<b>The park.</b> The words “national park” were used by the Prime Minister on 13 May [1] and by the Labour Party "
           "that day, which pledged that Manoel Island, White Rocks and Fort Campbell would be priorities in the next legislature "
           "[9]. We found no Maltese Act that defines the term: the six consolidated texts contain no occurrence of “national "
           "park” [14]. The opposition makes the same point [11]. We also found no published designation, management plan or "
           "local plan amendment for Manoel Island, and no deadline. Without a definition or a date, the statement cannot be "
           "shown to be met or missed."))
S.append(callout([P("WHAT THIS DOES AND DOES NOT SHOW", tag),
                  P("It shows that the concession was ended and the island returned to the Government. It does not show that no "
                    "park is coming: the outlets report steps (a local plan change, a Heritage Malta management plan) "
                    "that may be taken later. It shows only that on 9 October 2026, 149 days after the deed, we could not find "
                    "them.", small)],
                 bg=BLUE_PALE, bar=BLUE))

# ================================================================== 4
S.append(Spacer(1, 4 * mm))
S.append(SectionHeading(4, "Where the evidence points different ways"))
S.append(contested("Is Manoel Island on course to be a protected national park?", "NO PUBLIC TEST YET", AMBER,
                   "The Government ended the concession and took the island back; the Prime Minister has announced a local "
                   "plan change, and a Heritage Malta management plan is expected [1, 2], after a public consultation that drew thousands of "
                   "submissions.",
                   "No law defines a national park [14]; the opposition says so too [11]. Two months after the deed the Planning "
                   "Authority sanctioned padel courts on the island [12], and the Prime Minister said a marina concession would be "
                   "issued by public call [13 ◆].",
                   "Both can be true. The Government’s commitments are real but undated, and “national park” has no legal "
                   "meaning against which they can be tested. We rate what was said as Not measurable, not as broken.",
                   label_a="WHAT WAS COMMITTED", label_b="WHAT WE FOUND SINCE"))

# ================================================================== 5
S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(5, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> The MIDI concession over Manoel Island ended and the island returned to Government"),
     C("Prime Minister [2]; MIDI [3]"),
     C("MIDI’s own announcement of 13 May 2026: public deed, “return thereof to Government”; Parliament and shareholders "
       "approved [3, 7]."),
     verd("ACCURATE", GREENC)],
    [C("<b>B.</b> The return is to the public"),
     C("Prime Minister [2]"),
     C("Heritage Malta takes responsibility [2]. MIDI keeps Tigné Point [4]; padel courts and a yacht yard sit on or beside "
       "the island [12, 13 ◆]. Deed not read."),
     verd("ACCURATE, WITH CAVEATS", GREENC)],
    [C("<b>C.</b> It will become a national park"),
     C("Prime Minister [1]"),
     C("No definition in six Acts searched; no designation, plan or local plan change found; no date stated."),
     verd("NOT MEASURABLE (PLEDGE)", GREY)],
], [42 * mm, 24 * mm, 70 * mm, 34 * mm], valign="MIDDLE"))

# ================================================================== 6
S += [Spacer(1, 6 * mm), SectionHeading(6, "Verdict, pledge and requests for evidence"),
      verdict_box("Supported", "The concession ended and the island was returned to the Government, as MIDI’s own "
                  "announcement states; “national park” is rated as a pledge: Not measurable. Confidence: moderate."),
      Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) The factual statement, that Manoel Island went back from MIDI to the Government, is confirmed by the "
           "counterparty’s regulatory disclosure and by unanimous parliamentary approval as reported. (2) The caveats on "
           "public use (MIDI’s Tigné Point, sports uses, the yacht yard) concern what stands on or beside the island, not "
           "whether it was returned. (3) “Will become a national park” is a promise, so it is rated under the pledge scale. "
           "Confidence is moderate because we did not read the deed or the shareholder circular."))
S.append(callout([P("PLEDGE LABEL: NOT MEASURABLE (AS OF 9 OCT 2026)", tag),
                  P("The pledge as worded has no definition (no Maltese Act we searched defines “national park”) and no date. "
                    "The label judges delivery against the pledge as worded, not anyone’s intent, and is revisited when a "
                    "definition, designation or timetable is published.", small)],
                 bg=AMBER_PALE, bar=AMBER))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "From the Lands Ministry and Heritage Malta: the public deed and MIDI’s circular of 6 April 2026, and any terms that limit public use.",
    "From the Office of the Prime Minister: what “national park” means for Manoel Island in law, and the date by which it is to be designated.",
    "From the Planning Authority: the local plan amendment ruling out development on Manoel Island, if made.",
    "From Heritage Malta: the management plan, and the consultation report behind “thousands of submissions”.",
]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag),
               P("A reply is sought for the pledge label <i>Not measurable</i> (maintainer rule of 5 October 2026). The maintainer "
                 "handles it; nothing has been sent. Until the deadline has passed this is a draft label on this site only and "
                 "is not to be circulated elsewhere.", small)], bg=AMBER_PALE, bar=AMBER)]

# ================================================================== 7
S += [Spacer(1, 6 * mm), SectionHeading(7, "Limitations")]
for l in ["The Prime Minister’s words are read through Newsbook and TVM News; the Office of the Prime Minister’s release was not "
          "readable. Only words inside quotation marks are quoted.",
          "We read MIDI’s announcements, not the deed or the circular. MIDI is a party to the agreement and its announcement is a "
          "company disclosure, not an independent record.",
          "Whether “public ownership” in law is exactly “return to Government” was not tested against the deed. We did not check "
          "the land registry or the Lands Authority.",
          "“No national park instrument or plan found” rests on six consolidated Acts (legislation.mt), web searches and two "
          "outlets’ Manoel Island pages (first page of results). Subsidiary legislation, Hansard, the Planning Authority and "
          "Heritage Malta websites, and the Government Gazette were not searched directly.",
          "The padel-court decision is read as Lovin Malta reports it; the Planning Authority’s decision was not read. The 21 July "
          "remarks are second-hand (◆).",
          "The pledge was made on 13 May 2026, 17 days before the 30 May 2026 general election; the claim is rated on what was "
          "said, not on the party’s motive."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Xuereb M. (13 May 2026). Watch: Agreement over Manoel Island and Fort Tigné signed. Newsbook.",
     "https://newsbook.com.mt/en/agreement-over-manoel-island-and-fort-tigne-signed/"),
    ("2", "Rossitto A. (13 May 2026). Manoel Island and Fort Tigné agreement finalised to return sites to the public. TVM News.",
     "https://tvmnews.mt/en/news/manoel-island-and-fort-tigne-agreement-finalised-to-return-sites-to-the-public/"),
    ("3", "MIDI p.l.c. (13 May 2026). Company announcement MDI222: Manoel Island and Fort Tigné (public deed). Malta Stock Exchange.",
     "https://cdn.borzamalta.com.mt/download/announcements/MDI222.pdf"),
    ("4", "MIDI p.l.c. (17 Mar 2026). Company announcement MDI214: Manoel Island and Fort Tigné (in-principle agreement).",
     "https://cdn.borzamalta.com.mt/download/announcements/MDI214.pdf"),
    ("5", "MIDI p.l.c. (20 Mar 2026). Company announcement MDI215: Manoel Island and Fort Tigné (terms agreed).",
     "https://cdn.borzamalta.com.mt/download/announcements/MDI215.pdf"),
    ("6", "Spulber M. (17 Mar 2026). Government reaches €43M agreement to end concession – MIDI requested €78M. TVM News.",
     "https://tvmnews.mt/en/news/government-reaches-e43m-agreement-to-end-concession-midi-requested-e78m"),
    ("7", "TVM Newsroom (28 Apr 2026). MIDI shareholders approve agreement to return Manoel Island and Fort Tigné to the public. TVM News.",
     "https://tvmnews.mt/en/news/midi-shareholders-approve-agreement-to-return-manoel-island-and-fort-tigne-to-the-public"),
    ("8", "Falzon G. (17 Mar 2026). Manoel Island and Fort Tigné to be returned to public, Robert Abela announces. Lovin Malta.",
     "https://lovinmalta.com/malta/manoel-island-and-fort-tigne-to-be-returned-to-public-robert-abela-announces/"),
    ("9", "Scalvini Spiteri R. (13 May 2026). Manoel Island and Fort Tigné return agreement signed as PL unveils national park plan. Lovin Malta.",
     "https://lovinmalta.com/news/news-politics/manoel-island-and-fort-tigne-return-agreement-signed-as-pl-unveils-national-park-plan/"),
    ("10", "Italpress/MNA (1 Jan 2026). Malta, PM rings in New Year with pledge to reclaim key sites for public.",
     "https://www.italpress.com/?p=623920"),
    ("11", "Partit Nazzjonalista (17 Jul 2026). Manoel Island: A “national park” only for the election.",
     "https://pn.org.mt/en/?p=29629"),
    ("12", "Falzon G. (16 Jul 2026). Planning Authority sanctions 20 illegal Manoel Island padel courts and approves 10 more. Lovin Malta.",
     "https://lovinmalta.com/news/local/planning-authority-sanctions-20-illegal-manoel-island-padel-courts-and-approves-10-more/"),
    ("13", "Demirci A. (21 Jul 2026). Robert Abela says Transport Malta will issue concession for Manoel Island yacht marina. Lovin Malta, "
           "reporting MaltaToday (page refused to scripts) ◆.",
     "https://lovinmalta.com/news/robert-abela-says-transport-malta-will-issue-concession-for-manoel-island-yacht-marina/"),
    ("14", "legislation.mt. Consolidated texts of Cap. 549, 552, 445, 504, 573, 623, searched 9 Oct 2026 for “national park” and "
           "“nature reserve”.", "https://legislation.mt/"),
    ("15", "Miżien. Calculation script and outputs: tools/cc-055-report/calc.py; data/cc-055/checks.csv, documents.csv.", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance, statute text or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.", pledges=True)
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "9 Oct 2026", "First issue. Verdict Supported (moderate confidence); pledge label Not measurable; pending right of reply.")])

build_report(Report(
    number="055", out=str(FIG / "report.pdf"), kicker="Land and trees",
    title_lines=["Manoel Island:", "back to the public,", "a national park?"],
    subtitle_lines=["Testing the Prime Minister’s statement on the", "return of Manoel Island from MIDI"],
    quote_lines=["“We are transforming this area into a national park", "designed according to the wishes of the Maltese",
                 "and Gozitan people.”"], quote_size=14,
    attribution="Prime Minister Robert Abela, 13 May 2026 (as reported by Newsbook).",
    context="Said on the day the deed ending MIDI’s concession was signed.",
    verdict="Supported", verdict_note="The return is confirmed; “national park” is a pledge: Not measurable",
    footer_lines=["Version 1.0  ·  9 October 2026", "Status: draft, pending right of reply (pledge label)",
                  "Prepared from public sources.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Manoel Island – return and national park", version="1.0", date="9 October 2026", pledge_label="Not measurable",
    pdf_title="Manoel Island: back to the public, a national park? Claim Check 055",
    pdf_subject="Tests the statement that Manoel Island has been returned from MIDI and will become a national park",
    story=S))
