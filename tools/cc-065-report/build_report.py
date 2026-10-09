"""Claim Check 065 report. Run calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []

# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("In a statement published on 2 May 2026, ADPD – The Green Party (chairperson Sandra Gauci and Luke Caruana) said, in "
        "Maltese, that the Planning Authority had approved “the construction of apartments and garages in the buffer zone around "
        "the Ġgantija” (our translation), calling that decision and another one on the same day “sacrilege against our heritage”. "
        "The claim record summarised this as: recent planning decisions endanger Malta’s heritage, including a permit for apartments "
        "within the buffer zone of the Ġgantija Temples. We checked the facts in that sentence. This report covers the Ġgantija "
        "permit only; the Fort Chambray decision named in the same statement is Claim Check 066.", lead)]
S.append(key_points([(a, b.replace("◆", DIAM)) for a, b in [
    ("The permit was approved.",
     "The Planning Board approved application PA/00570/21 on 30 April 2026, by 10 votes to 1: 22 apartments over 20 garages in "
     "Xagħra. Newsbook reported the vote the same morning [3], and TVM News reported the reaction that day [6]. We could not read "
     "the Authority’s own record."),
    ("The site is in the buffer zone, and the Authority has said so itself.",
     "In March 2024 the Authority revoked the 2023 permit after acknowledging that incorrect information had been given on "
     "whether the site lay in the buffer zone [8 ◆]. The 2026 approval followed a heritage impact assessment, which is required "
     "for development in the zone [9]. We could not place the plot on the plan’s map ourselves."),
    ("“Sacrilege” and “endangers” are judgements, and they are contested.",
     "The Superintendence of Cultural Heritage withdrew its objections to revised designs and the assessment concluded the "
     "development would not harm the integrity of the site [3, 4, 9]. NGOs and Momentum call the assessment internally "
     "contradictory [3, 9]. We did not rate the opinion."),
    ("What we cannot tell.",
     "We did not read the permit, the assessment, the Superintendence’s reply or any UNESCO comment on the final design."),
]]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("30 Apr", GREEN, "2026: Planning Board approves 22 apartments and 20 garages, 10 votes to 1 (Newsbook)"),
             ("7 Mar 2024", GREEN, "Permit revoked: the Authority said wrong buffer-zone information had been given (Newsbook, TVM)"),
             ("150–157 m", GREY, "Reported distance of the site from the temples; the buffer zone extends 127–477 m from the temple edge on our map reading"),
             ("0", ORANGE, "UNESCO comments on the final design found (whc.unesco.org refused our access)")]),
      Spacer(1, 4 * mm),
      up_down("A move up to Supported would need the Authority’s own decision record, with the vote date and the plot’s position on "
              "the official buffer-zone plan, and a reading of the ‘yesterday’ wording as a one-day slip.",
              "A decision record showing that the permitted plot, or part of it, lies outside the official buffer zone would lower the "
              "location sub-claim. An error in the vote date or the permit’s content would lower the first."),
      Spacer(1, 3 * mm)]
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The claim record came from a MaltaToday headline, “ADPD slams planning decisions that endanger Malta’s heritage” [locator, "
           "page refused to scripts]. Following our rule to quote the speaker, not the headline, we read ADPD’s own statement on its "
           "website. It is in Maltese; the English below is our translation. The statement closes by asking what culture and heritage are "
           "worth “when the profits of the few are at stake” and answering “Apparently, nothing” (Newsbook’s English [2]); that is an opinion and not rated."))
S.append(std_table([
    [C("Source", cellh), C("What it says", cellh), C("Our access", cellh), C("Status", cellh)],
    [C("<b>ADPD – The Green Party</b>, statement signed by Sandra Gauci and Luke Caruana, adpd.mt, 2 May 2026 [1]"),
     C("“Ma kienx biżżejjed tapprova l-kostruzzjoni ta’ appartamenti u garaxxijiet fil-buffer zone ta’ madwar il-Ġgantija – sit "
       "uniku u meqjus bħala wirt kulturali dinji mill-UNESCO.” (It was not enough to approve the construction of apartments and "
       "garages in the buffer zone around the Ġgantija – a unique site considered world cultural heritage by UNESCO.) The text "
       "says the Authority did this “yesterday” and calls it, with the Fort Chambray decision, “żewġ sagrileġġi” (two sacrileges)."),
     C("Read in full, 9 Oct 2026."), C("<b>The claim</b> (quoted words)")],
    [C("<b>Newsbook</b>, 2 May 2026 [2]"),
     C("Reports the same statement in English. Its paraphrase says ADPD pointed to “a permit to build an apartment block in the buffer zone of the "
       "Ġgantija Temples” made “the same day” as the Fort Chambray decision (outlet’s text)."),
     C("Read in full."), C("Outlet report")],
    [C("<b>Newsbook</b>, 30 Apr 2026 [3]; <b>TVM News</b>, 30 Apr 2026 [6]"),
     C("The Authority approved a 22-apartment block with 20 garages (PA/00570/21); “the board voted 10 to 1 in favour this "
       "morning” (Newsbook’s text); Momentum condemned the approval (TVM)."),
     C("Read in full."), C("Outlet reports")],
    [C("<b>Planning Authority</b> statements, as reported, 9 Nov 2023 and 7 Mar 2024 [7, 8, 12]"),
     C("2023: approved “outside the buffer zone” (TVM’s text of the statement). 2024: revoked because incorrect information had been given on "
       "the buffer zone (Newsbook’s text of the statement)."),
     C("Read via TVM News and Newsbook; the statements themselves were not."), C("Outlet reports of a primary statement ◆")],
    [C("<b>Heritage Malta</b>, Megalithic Temples of Malta Management Plan 2012–2017 (Nov 2011) [11]"),
     C("Describes the buffer zone of each property, a minimum 100 m radius for a Grade A scheduled site, and plots the Ġgantija buffer "
       "zone on Figure 2 (MEPA map, GN 357/98)."),
     C("Read in full (PDF; hash in data/cc-065/documents.csv)."), C("<b>Primary</b> (official plan)")],
], [40 * mm, 72 * mm, 32 * mm, 26 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("WHAT WE COULD NOT READ", tag),
               P("The Authority’s case file for PA/00570/21, the heritage impact assessment, the Superintendence of Cultural "
                 "Heritage’s reply and the permit conditions were not available to us (pa.org.mt and gov.mt refuse scripts). UNESCO’s "
                 "World Heritage Centre pages return 403. MaltaToday pages return 403: its reports reached us only as search summaries, "
                 "which we do not use ◆. Routes tried are in <i>literature/CC-065/README.md</i>.", small)],
              bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Questions.</b> (A) Did the Planning Authority approve apartments and garages on this site when ADPD said it did? "
           "(B) Is the site in the buffer zone of the Ġgantija Temples? (C) Is the harm to heritage that ADPD alleges something "
           "the records can show?"))
S.append(P("<b>Evidence.</b> For A we read the same-day reports of the vote and its reporting through to the demolition footage of 13 June [3, 5, 6]. "
           "For B we read the Authority’s two statements as reported [7, 8, 12], the Shift’s account of the 2026 hearing [9], the Gozo "
           "Regional Council’s letter [10] and the management plan [11]. We also measured Figure 2 of the plan: its scale bar gave "
           "0.4 km, and its printed bounding co-ordinates gave a frame 926 m wide; we measured 929 m, a difference of 0.4% (<i>calc.py</i>; "
           "<i>data/cc-065/checks.csv</i>). We then measured, in eight directions, how far the plotted buffer zone extends from the edge of "
           "the temple site, to compare with the 150–157 m at which the outlets place the plot."))
S.append(P("<b>The limit of B.</b> The permit’s plot is not drawn on the plan, and we could not obtain its co-ordinates (the Overpass map "
           "service refused our connection, and the Authority’s file is browser-only). The plan is dated November 2011 and the Shift refers to "
           "the 2015 management plan: we did not read a later plan or the current official zone."))
S.append(P("<b>Grades.</b> A management plan is grade C (an official document, not an audited dataset); news reports are grade D and are used to "
           "locate what was said. <b>Verdicts</b> follow Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(3, "What the evidence shows"))
S.append(P("<b>The approval.</b> Application PA/00570/21 covers a three-storey block of about 22 apartments and 20 garages in Xagħra, roughly "
           "150 metres from the temples according to the Shift [9] and “approximately 157 meters” according to TVM News [7]. The board first approved it "
           "on 9 November 2023 [10, 12]. In that decision the Authority’s statement said the development was “outside the buffer zone” and "
           "that Heritage Malta considered the drawings compatible with the management plan [12]. On 7 March 2024 the board revoked the permit and "
           "reprocessed the application so that a heritage impact assessment could be presented [7, 8]. After a six-week adjournment in March 2026 [9], "
           "the board approved the project again on 30 April 2026, voting 10 to 1; the only dissent was the NGO representative, Romano Cassar [3]. "
           "The vote is 90.9% in favour (<i>calc.py</i>). Newsbook reports that the farmhouse on the plot was being demolished by 13 June, 44 days "
           "after the vote [5]."))
S.append(fig(FIG / "fig1_timeline.png", width=CW * 0.98))
S.append(P("Figure 1. Steps in application PA/00570/21. Sources: Newsbook [3, 8]; The Shift [9]; Gozo Regional Council [10]; ADPD [1]. "
           "“Feb 2026” is Newsbook’s statement that the assessment was completed in February [3].", cap))
S.append(P("<b>The buffer zone.</b> The Authority’s own words, as the outlets relay them, changed between the two decisions: in November 2023 it "
           "approved the project as outside the buffer zone, relying on an architect’s argument that the site lay in an area of archaeological "
           "importance instead [9, 12]; in March 2024 it acknowledged that incorrect information had been provided on that question [8 ◆]. The 2026 "
           "approval followed a heritage impact assessment that the Shift says the Authority required because the site is in the zone defined in "
           "the management plan [9]. The Gozo Regional Council’s letter of December 2023 names Government Notice 853/10 of 17 August 2010 as including this "
           "buffer zone [10]; the plan’s appendix lists two sites in the Ġgantija zone scheduled on that same date, 17 August 2010 [11]."))
S.append(fig(FIG / "fig2_margins.png", width=CW * 0.98))
S.append(P("Figure 2. How far the plotted Ġgantija buffer zone extends from the edge of the temple site, by compass direction, measured by us on Figure 2 "
           "of the management plan [11]. Amber: less than 157 m. The orange band is the 150–157 m at which the outlets place the plot [7, 9]; the plot’s "
           "direction from the temples is not given in any source we read. Sources: <i>data/cc-065/margins.csv</i>.", cap))
S.append(P("<b>What the measurement does and does not show.</b> The plan states a minimum radius of 100 m for the buffer zone of a Grade A site [11]. On "
           "the map, the zone reaches 127 m from the temple edge at its narrowest of the eight directions (south-east) and 477 m at its widest (west); the "
           "shortest distance in any direction is 94 m. A plot 150–157 m from the temples is therefore inside the zone in five of the eight directions and "
           "near or past the boundary in three. Distance alone does not settle it; the Authority’s 2024 statement and the 2026 assessment process do."))
S.append(callout([P("WHAT THIS DOES AND DOES NOT SHOW", tag),
                  P("It shows that the Planning Board approved the project on 30 April 2026 and that, on the Authority’s own account, the site is in the buffer "
                    "zone. It does not show whether the building will harm the temples: that is the question the assessment, the Superintendence and "
                    "the objectors disagree on (section 4).", small)],
                 bg=BLUE_PALE, bar=BLUE))

# ================================================================== 4
S.append(Spacer(1, 4 * mm))
S.append(SectionHeading(4, "Where the evidence points different ways"))
S.append(contested("Does the approved building endanger the Ġgantija Temples’ setting?", "CONTESTED", AMBER,
                   "The heritage impact assessment concluded that the development would not negatively affect the integrity of the site, because "
                   "the building would be seen largely from within the buffer zone and would sit within the existing skyline of Xagħra [9]. The "
                   "Superintendence of Cultural Heritage withdrew its objections after revised designs [3, 4], and the Prime Minister said the "
                   "development “will not prejudice this historic site” [4].",
                   "Din l-Art Ħelwa Għawdex, Għawdix and Wirt Għawdex called the assessment’s methodology partial and its conclusions "
                   "internally contradictory [3, 5, 9]. Newsbook and Momentum report that the assessment itself calls the building “visually dominant "
                   "in the landscape” while rating the impact “not significant” [3, 5]. UNESCO’s World Heritage Centre told Malta in 2022 that "
                   "an assessment is a pre-requisite for development around a property [13 ◆].",
                   "Both can be true. Whether an impact is “significant” is a judgement against a standard we did not have. We did not find a UNESCO "
                   "comment on the final design. ADPD’s “sacrilege” is an opinion on that judgement and we did not rate it.",
                   label_a="FOR THE PERMIT: HERITAGE ASSESSMENT AND AUTHORITIES", label_b="AGAINST: NGOs AND THE PARTY STATEMENTS"))

# ================================================================== 5
S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(5, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> The Planning Authority approved apartments and garages on the site (“yesterday”)"),
     C("ADPD [1]"),
     C("Board vote 10 to 1 on 30 April 2026 for 22 apartments and 20 garages [3, 6]. ADPD’s text, stamped 2 May, says “yesterday”: a two-day gap at most (calc.py). Authority’s record not read."),
     verd("ACCURATE", GREENC)],
    [C("<b>B.</b> The apartments are in the buffer zone around the Ġgantija"),
     C("ADPD [1]"),
     C("Authority acknowledged wrong buffer-zone information in 2024 [8 ◆]; 2026 approval followed the required assessment [9]; Regional Council cites GN 853/10 [10]. Plot not placed on the plan by us."),
     verd("ACCURATE", GREENC)],
    [C("<b>C.</b> The decision is a “sacrilege” against heritage (endangers it)"),
     C("ADPD [1]"),
     C("A judgement. The assessment and the Superintendence find no negative effect; NGOs and Momentum dispute it [3, 5, 9]. No UNESCO comment on the final design found."),
     verd("NOT RATED (OPINION)", GREY)],
], [42 * mm, 24 * mm, 70 * mm, 34 * mm], valign="MIDDLE"))

# ================================================================== 6
S += [Spacer(1, 6 * mm), SectionHeading(6, "Verdict and requests for evidence"),
      verdict_box("Largely supported", "The permit was approved and the site is in the buffer zone, as ADPD said; “sacrilege” is an opinion we did not rate. "
                  "Confidence: moderate."),
      Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) The approval on 30 April 2026 is reported on the day by two outlets and matches the application’s history. (2) The "
           "location in the buffer zone rests on the Authority’s own change of position and the assessment it then required; we could not "
           "check it against the plot’s co-ordinates. (3) The caveats are minor: the word “yesterday” in a statement stamped 2 May, and a "
           "judgement of harm that the sources dispute and that we did not rate. Confidence is moderate because the Authority’s record, the "
           "assessment and the permit were not read."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "From the Planning Authority: the decision notice and permit conditions for PA/00570/21, with the date of the board’s decision.",
    "From the Planning Authority: the plot’s position on the official Ġgantija buffer-zone plan and the current zone boundary.",
    "From the Superintendence of Cultural Heritage: the heritage impact assessment and its reply on the revised designs.",
    "From UNESCO’s World Heritage Centre: any comment on the heritage impact assessment for this application.",
]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag),
               P("No reply is needed: the verdict is Largely supported (maintainer rule of 5 October 2026). Nothing has been sent to anyone.", small)],
              bg=BLUE_PALE, bar=BLUE)]

# ================================================================== 7
S += [Spacer(1, 6 * mm), SectionHeading(7, "Limitations")]
for l in ["ADPD’s statement is in Maltese; the English is our translation, and the quoted Maltese is as printed on adpd.mt.",
          "The vote and its date come from Newsbook and TVM News, not from the Authority’s record. The Authority’s statements of 2023 and 2024 are read "
          "through TVM News and Newsbook ◆.",
          "We did not place the plot on the plan. The 150–157 m figures are the outlets’; they do not say from which part of the temple site they are measured.",
          "The management plan we read is for 2012–2017. The Shift refers to a 2015 plan; we did not find it, and the current official buffer zone may differ.",
          "Our map measurement is a pixel measurement of a scanned map (calibrated to 0.4%); it is approximate and not a survey.",
          "UNESCO’s World Heritage Centre pages were refused. The 2022 letter is known through Newsbook’s report of the Coalition for Gozo’s "
          "quotation of it, so it is second-hand ◆.",
          "Our claim concerns the Ġgantija permit only. ADPD’s sentence on Fort Chambray, and its general claim that planning decisions endanger heritage, "
          "are not tested here."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "ADPD – The Green Party (2 May 2026). Forti Chambray: eżempju wieħed biss tas-saltna tar-regħba f’pajjiżna [statement signed by Sandra Gauci and Luke Caruana]. adpd.mt.",
     "https://adpd.mt/forti-chambray-ezempju-wiehed-biss-tas-saltna-tar-reghba-fpajjizna/"),
    ("2", "Cordina J. P. (2 May 2026). Fort Chambray debacle just one example of Malta’s ‘reign of greed’ – ADPD. Newsbook.",
     "https://newsbook.com.mt/en/fort-chambray-debacle-just-one-example-of-maltas-reign-of-greed-adpd/"),
    ("3", "Balzan J. (30 Apr 2026). Ġgantija development approved despite heritage fears. Newsbook.",
     "https://newsbook.com.mt/en/ggantija-development-approved-despite-heritage-fears/"),
    ("4", "Balzan J. (4 May 2026). Abela claims Ġgantija apartments ‘will not prejudice’ UNESCO site. Newsbook.",
     "https://newsbook.com.mt/en/abela-claims-ggantija-apartments-will-not-prejudice-unesco-site/"),
    ("5", "Balzan J. (13 Jun 2026). Watch: Farmhouse beside Ġgantija Temples demolished following planning approval. Newsbook.",
     "https://newsbook.com.mt/en/watch-farmhouse-beside-ggantija-temples-demolished-following-planning-approval/"),
    ("6", "Spiteri M. (30 Apr 2026). Momentum condemns permit approval for 22 block apartment near Ggantija Temples. TVM News.",
     "https://tvmnews.mt/en/news/momentum-condemns-permit-approval-for-22-block-apartment-near-ggantija-temples/"),
    ("7", "TVM Newsroom (7 Mar 2024). Planning Authority revokes permit for apartments in Ġgantija area. TVM News.",
     "https://tvmnews.mt/en/news/planning-authority-revokes-permit-for-apartments-in-ggantija-area/"),
    ("8", "Newsbook (7 Mar 2024). PA revokes approval of apartment block overlooking Ġgantija temples ◆ (outlet’s report of the Authority’s statement).",
     "https://newsbook.com.mt/en/pa-revokes-approval-of-apartment-block-overlooking-ggantija-temples/"),
    ("9", "The Shift Team (12 Mar 2026). Planning Authority delays decision on Ġgantija buffer zone flats after NGOs challenge heritage assessment. The Shift News.",
     "https://theshiftnews.com/2026/03/12/planning-authority-delays-decision-on-ggantija-buffer-zone-flats-after-ngos-challenge-heritage-assessment/"),
    ("10", "Gozo Regional Council (15 Dec 2023). Gozo Regional Council objects to development within Ġgantija Temples buffer zone [letter to the Planning Authority]. Reġjun Għawdex.",
     "https://regjunghawdex.com/?p=1812"),
    ("11", "Parliamentary Secretariat for Culture and Local Government (Nov 2011). The Megalithic Temples of Malta World Heritage Site: Management Plan 2012–2017, "
            "section 2.1.3, Figure 2, Appendix 1. Heritage Malta.",
     "https://heritagemalta.mt/app/uploads/2024/02/Megalithic-Temples-Management-Plan-2012-17.pdf"),
    ("12", "TVM Newsroom (9 Nov 2023). Residential development downsized outside buffer zone will not impact Ġgantija temples – PA. TVM News.",
     "https://tvmnews.mt/en/news/residential-development-downsized-outside-buffer-zone-will-not-impact-ggantija-temples-pa/"),
    ("13", "Cordina J. P. (2025). Coalition for Gozo: UNESCO confirms need for heritage impact assessment near Ġgantija. Newsbook, quoting a letter of Oct 2022 ◆.",
     "https://newsbook.com.mt/en/coalition-for-gozo-unesco-confirms-need-for-heritage-impact-assessment-near-ggantija/"),
    ("14", "Miżien. Calculation script and outputs: tools/cc-065-report/calc.py; data/cc-065/checks.csv, margins.csv, documents.csv.", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance, statute text or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "9 Oct 2026", "First issue. Verdict Largely supported (moderate confidence); no right of reply needed.")])

build_report(Report(
    number="065", out=str(FIG / "report.pdf"), kicker="Planning and housing",
    title_lines=["Ġgantija:", "apartments in the", "buffer zone?"],
    subtitle_lines=["Testing ADPD’s statement on the permit for 22", "apartments beside the Ġgantija Temples"],
    quote_lines=["“Ma kienx biżżejjed tapprova l-kostruzzjoni ta’ appartamenti", "u garaxxijiet fil-buffer zone ta’ madwar il-Ġgantija.”"],
    quote_size=13,
    attribution="ADPD – The Green Party (Sandra Gauci and Luke Caruana), 2 May 2026, in Maltese.",
    context="Our translation: “It was not enough to approve apartments and garages in the buffer zone around Ġgantija.”",
    verdict="Largely supported", verdict_note="Approved and in the buffer zone; “sacrilege” is an opinion, not rated",
    footer_lines=["Version 1.0  ·  9 October 2026", "Status: no right of reply needed",
                  "Prepared from public sources.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Ġgantija – apartments in the buffer zone", version="1.0", date="9 October 2026",
    pdf_title="Ġgantija: apartments in the buffer zone? Claim Check 065",
    pdf_subject="Tests ADPD's statement that the Planning Authority approved apartments in the buffer zone of the Ġgantija Temples",
    story=S))
