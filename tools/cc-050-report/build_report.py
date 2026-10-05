"""Claim Check 050 report. Run calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
LG = colors.HexColor("#8DB36B")
S = []
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("On 27 May 2026, three days before the general election, BirdLife Malta headlined a press release "
        "<b>“BirdLife Malta condemns dangerous political race to weaken environmental enforcement”</b>, naming both the "
        "Labour Party and the Nationalist Party (PN). We read the release, both parties’ programmes and the later "
        "record to see whether each party made commitments that weaken hunting and trapping enforcement.", lead)]
S.append(key_points([
    ("The Labour side is documented, but not in the manifesto.",
     "Labour’s manifesto (items 63–64) promises to defend EU-permitted derogations and “safeguard” hunting and trapping; "
     "it has nothing on fines or licences. The cuts came from a minister’s campaign statement and, after the election, "
     "an ORNIS Committee proposal to cut fines for shooting protected birds by 40%."),
    ("The PN side rests on one sentence and an inference.",
     "Alex Borg said hunting and trapping “will be safeguarded”. We found no PN proposal to cut fines or restore "
     "licences, and the 16 chapters of its programme contain no hunting or trapping item. That the pledge would "
     "override the Birds Directive is BirdLife Malta’s reading, not Mr Borg’s words."),
    ("No law has changed yet.",
     "The consolidated Conservation of Wild Birds Regulations still carry fines of EUR 5,000 and EUR 10,000 for "
     "shooting a protected bird. The reduced figures are reported second-hand from a presentation we cannot see."),
    ("Verdict: not substantiated (moderate confidence).",
     "Shown for Labour; not shown for the PN. A “race” between both parties to weaken enforcement is stated more "
     "strongly than the documents allow."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(2), Spacer(1, 3 * mm),
      tiles([("2 of 2", AMBER, "Parties named; documents show weakening for one (Labour)"),
             ("0", GREY, "Hunting or trapping hits in the 16 PN programme chapters"),
             ("-40%", AMBER, "Reported cut to fines for shooting protected birds (ORNIS, 23 Sep 2026)"),
             ("0", GREEN, "Legal notices amending the penalties in 2026 (consolidated text to L.N. 251/2025)")]),
      Spacer(1, 4 * mm),
      up_down("A PN document or on-the-record statement committing to lower fines, to restore revoked licences, or to "
              "keep a practice the EU Birds Directive does not allow.",
              "A PN statement ruling out any change to penalties and licences, or the ORNIS proposal being withdrawn and "
              "BirdLife Malta’s reading of Mr Borg’s words being shown to be wrong."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the evidence shows"),
          ("4", "Where the evidence points different ways"), ("5", "Testing the claim"),
          ("6", "Verdict and requests for evidence"), ("7", "Limitations")])
S.append(PageBreak())

S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The intake locator was a Newsbook article of 27 May 2026 headlined “BirdLife Malta accuses Labour, PN of "
           "‘dangerous race’ to weaken hunting laws ahead of election” [1]. The wording is BirdLife Malta’s own, in its "
           "press release of the same day [2]. Two differences matter. The release says <i>environmental enforcement</i>, "
           "not “hunting laws”, and its body text is more careful than its headline: a “worrying race between political "
           "parties to outbid each other with commitments that risk weakening enforcement and accountability”; the PN "
           "“appears to have fallen into the same trap”; and statements “indicating that hunting and trapping would be "
           "safeguarded even in situations where practices may conflict with obligations arising from the EU Birds "
           "Directive”."))
S.append(P("The release points to three things: calls to lower fines for shooting protected birds and for hunting or "
           "trapping in closed seasons; statements “reportedly made by candidates” that lifetime licence bans should be "
           "revisited; and the PN’s position on safeguarding hunting. It names no speaker or document. Newsbook "
           "attributes the first two to Economy Minister Silvio Schembri and the third to PN leader Alex Borg."))
S.append(std_table([
    [C("Source", cellh), C("What it says", cellh), C("Our access", cellh), C("Status", cellh)],
    [C("<b>BirdLife Malta</b>, press release, 27 May 2026 [2]"),
     C("“…a worrying race between political parties to outbid each other with commitments that risk weakening "
       "enforcement and accountability.”"), C("Read in full, 5 Oct 2026."), C("<b>The claim</b>")],
    [C("<b>Labour</b>, <i>Int Malta</i> manifesto 2026, items 63–64 [3]"),
     C("Defend the derogations EU directives permit and safeguard hunting and trapping practices; no item on fines or "
       "licences."), C("PDF read; section extracted to data/cc-050/."), C("<b>Primary</b>")],
    [C("<b>Alex Borg</b>, PN, Rabat mass meeting, 26 May 2026 [4]"),
     C("Hunting and trapping “will be safeguarded” (quoted by Lovin Malta)."), C("Outlet’s transcription ◆; video not "
       "viewed."), C("Primary words, second-hand")],
    [C("<b>PN</b> programme <i>Nifs Ġdid</i>, 16 chapters [5]"), C("No hunting or trapping item found."),
     C("All 16 chapter pages searched."), C("<b>Primary</b>")],
    [C("<b>Newsbook</b> 24 Sep and 2 Oct 2026 [6]; <b>BirdLife Malta</b> 24 Sep and 2 Oct [7]"),
     C("ORNIS proposal: fines for shooting protected birds from EUR 5,000 to 3,000 (first) and 10,000 to 6,000 (repeat); "
       "revoked licences could be reapplied for."), C("Read. Presentation not public ◆."), C("NGO and news")],
], [38 * mm, 74 * mm, 36 * mm, 22 * mm]))

S += [Spacer(1, 4 * mm), SectionHeading(2, "Method")]
S.append(P("<b>Question.</b> Did each party make commitments that weaken hunting and trapping enforcement, as the "
           "release says? We tested each party on its own, using the same steps."))
S.append(P("<b>Evidence.</b> (1) The Labour manifesto PDF and the 16 chapter pages of the PN programme were searched for "
           "hunting, trapping, the hunters’ federation, fines and licences (data/cc-050/). (2) Campaign statements were "
           "traced to the outlet that quoted them. (3) The current penalties were read from the consolidated "
           "Conservation of Wild Birds Regulations (S.L. 549.42) on legislation.mt, and the size of the reported "
           "reduction computed in <i>tools/cc-050-report/calc.py</i>. We did not interview anyone and could not see the "
           "ORNIS presentation. BirdLife Malta’s views of the Birds Directive are not tested here; this is a check of "
           "what the parties committed to."))
S.append(P("<b>Grades.</b> Legislation and party manifestos: C (primary documents; official text). BirdLife Malta "
           "release: D for facts about others, since it is an advocacy statement. News reports: D. <b>Verdicts</b> follow "
           "the five-point scale in Appendix A."))

S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(3, "What the evidence shows"))
S.append(P("<b>Labour.</b> Items 63 and 64 of the manifesto, under “Hunting and trapping”, say that only a Labour "
           "government guarantees that the country keeps defending the derogations the EU directives permit and that "
           "hunting and trapping practices are safeguarded [3]. The text is bounded by EU law and says nothing about fines, "
           "revocations or reapplication. The weakening comes elsewhere. Newsbook reports that in the final week the Economy "
           "Minister told a campaign event a Labour government would amend fines and licence revocations, including for "
           "those already revoked, and that the government had agreed this with the hunters’ federation [6]. We could "
           "not find the minister’s own words; the account is Newsbook’s. After the election, on 23 September, a "
           "presentation to the ORNIS Committee by a lawyer commissioned for the purpose proposed lower fines and a "
           "ministerial route for reapplying; BirdLife Malta was the only dissenting voice [7]."))
S.append(P("<b>Nationalist Party.</b> Lovin Malta quotes Mr Borg telling the Rabat meeting that hunting and trapping "
           "“will be safeguarded” [4]. The 16 chapters of the PN programme contain no hunting or trapping proposal "
           "[5]. We found no PN statement proposing lower fines or restoring revoked licences. BirdLife Malta’s release "
           "reads the pledge as one that would hold “even in situations where practices may conflict” with the Birds "
           "Directive; the words quoted do not say that."))
S.append(KeepTogether([fig(FIG / "fig1_fines.png", width=CW * 0.98),
    P("Figure 1. Fines for hunting or taking a bird in Schedule I or IX of the regulations, in force and as reported "
      "for the ORNIS proposal (-40% in both cases).", cap)]))
S.append(P("<b>The law has not changed.</b> The consolidated regulations on legislation.mt, amended up to L.N. 251 of "
           "2025, set EUR 5,000 or a year’s imprisonment and permanent licence revocation for a first conviction, and "
           "EUR 10,000 or two years for a repeat conviction [8]. We found no 2026 amending notice, so what exists is a "
           "proposal, not a weakened law."))

S.append(CondPageBreak(80 * mm))
S.append(SectionHeading(4, "Where the evidence points different ways"))
S.append(contested("Are both parties “racing” to weaken enforcement?", "ONE PARTY SHOWN", AMBER,
                   "Labour’s minister announced cuts in the campaign; the government confirmed an agreement with the "
                   "hunters’ federation; an ORNIS proposal followed. The PN’s leader pledged to “safeguard” hunting and "
                   "trapping to loud cheers at the final Gozo rally.",
                   "The Labour manifesto itself is limited to EU-permitted derogations. For the PN there is no document "
                   "proposing weaker penalties or licences, and “safeguarded” is not defined. The reading that it "
                   "overrides the Birds Directive is an inference.",
                   "BirdLife Malta’s concern is documented for Labour. For the PN it is an interpretation of one unqualified "
                   "sentence, which the release itself words as “appears” and “indicating”.",
                   label_a="FOR", label_b="AGAINST"))

S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(5, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> Labour made commitments to lower penalties and revisit licence bans"), C("BirdLife Malta [2]"),
     C("Minister’s campaign statement (Newsbook ◆), government–federation agreement (Newsbook ◆), ORNIS proposal "
       "(-40% fines; BirdLife screenshot ◆). Not in the manifesto."), verd("LARGELY SUPPORTED", LG)],
    [C("<b>B.</b> The PN would safeguard hunting and trapping even where it conflicts with the Birds Directive"),
     C("BirdLife Malta [2]"),
     C("Mr Borg: “will be safeguarded” (quoted by Lovin Malta ◆). No Directive reference, no fine or licence "
       "proposal, no hunting item in the programme."), verd("NOT SUBSTANTIATED", AMBER)],
    [C("<b>C.</b> The two parties are in a race to outbid each other in weakening enforcement"),
     C("BirdLife Malta [2]"),
     C("Documented for one party; the other’s side is an inference. Opposite sides making similar pledges to the "
       "same voters is plausible, but a “race to weaken” needs both."), verd("NOT SUBSTANTIATED", AMBER)],
], [44 * mm, 18 * mm, 72 * mm, 36 * mm], valign="MIDDLE"))

S += [Spacer(1, 6 * mm), SectionHeading(6, "Verdict and requests for evidence"),
      verdict_box("Not substantiated", "Shown for Labour, not for the PN. Confidence: moderate."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> The Labour half is backed by a minister’s reported statement, a confirmed government–federation "
           "agreement and a proposal before the advisory committee. The PN half rests on one unqualified pledge and an "
           "inference about EU law. The headline puts both parties in one race; the evidence we could show supports "
           "one. Confidence is moderate because the key Labour evidence is second-hand. <b>What this verdict does "
           "not say.</b> It does not say either party acted in bad faith, and it does not test whether the proposed "
           "penalties are proportionate or what the Birds Directive requires; a lawyer would need to answer that."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "From BirdLife Malta: the sources for “statements reportedly made by candidates”, and which PN statement it relies on.",
    "From the Government: the ORNIS presentation and minutes of 23 September 2026.",
    "From the PN: whether “safeguarded” includes any change to penalties, licences or derogations.",
]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag), P("Draft, pending right of reply (BirdLife Malta); the maintainer sends it.", small)],
              bg=AMBER_PALE, bar=AMBER)]
S += [Spacer(1, 6 * mm), SectionHeading(7, "Limitations")]
for l in ["Mr Schembri’s and Mr Borg’s words come from news outlets (◆); we did not view the recordings.",
          "The ORNIS presentation is not public; its figures are BirdLife Malta’s and Newsbook’s account (◆).",
          "The PN programme was read as 16 web chapters; a separate PDF or later policy paper could contain a hunting item.",
          "The consolidated regulations may lag newly published notices; we found no 2026 amendment."]:
    S.append(P("• " + l, bul))
S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Balzan J. (27 May 2026). BirdLife Malta accuses Labour, PN of ‘dangerous race’ to weaken hunting laws ahead of "
          "election. Newsbook.", "https://newsbook.com.mt/en/birdlife-malta-accuses-labour-pn-of-dangerous-race-to-weaken-hunting-laws-ahead-of-election/"),
    ("2", "BirdLife Malta (27 May 2026). BirdLife Malta condemns dangerous political race to weaken environmental enforcement.",
     "https://birdlifemalta.org/2026/05/birdlife-malta-condemns-dangerous-political-race-to-weaken-environmental-enforcement/"),
    ("3", "Partit Laburista (2026). Int Malta: Manifest Elettorali 2026, items 63–64, p. 171.",
     "https://partitlaburista.org/wp-content/uploads/2026/08/Manifest_Elettorali_INT_MALTA_2026.pdf"),
    ("4", "Falzon G. (26 May 2026). Borg pledges hunting and trapping ‘will be safeguarded’ during Gozo mass meeting. Lovin Malta. ◆",
     "https://lovinmalta.com/news/general-election-2026/watch-borg-pledges-hunting-and-trapping-will-be-safeguarded-during-gozo-mass-meeting/"),
    ("5", "Partit Nazzjonalista (2026). Nifs Ġdid: Programm Elettorali (16 chapters).", "https://pn.org.mt/en/nifsgdid/"),
    ("6", "Balzan J. (28 May 2026). Government should fight wildlife crime, not reward it, 10 NGOs warn; (24 Sep 2026) BirdLife "
          "warns reduced hunting fines would reward those who break the law; (2 Oct 2026) BirdLife accuses FKNK chief of lying. "
          "Newsbook. ◆", "https://newsbook.com.mt/en/government-should-fight-wildlife-crime-not-reward-it-10-ngos-warn/"),
    ("7", "BirdLife Malta (24 Sep and 2 Oct 2026). Calls on Government not to weaken penalties; rejects FKNK President’s statement as false. ◆",
     "https://birdlifemalta.org/2026/10/birdlife-malta-rejects-fknk-presidents-statement-as-false/"),
    ("8", "Conservation of Wild Birds Regulations, S.L. 549.42 (consolidated, to L.N. 251 of 2025). Retrieved 5 Oct 2026.",
     "https://legislation.mt/eli/sl/549.42/eng"),
    ("9", "MiŻien. Searches and calculation: data/cc-050/; tools/cc-050-report/calc.py.", ""),
])
S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "5 Oct 2026", "First issue. Verdict Not substantiated (moderate confidence); draft, pending right of reply.")])

build_report(Report(
    number="050", out=str(FIG / "report.pdf"), kicker="Nature and wildlife",
    title_lines=["A “race to weaken", "hunting laws”?"],
    subtitle_lines=["Testing BirdLife Malta’s claim about Labour and the PN", "against their programmes and the record"],
    quote_lines=["“BirdLife Malta condemns dangerous political race to", "weaken environmental enforcement”"], quote_size=14,
    attribution="BirdLife Malta, press release headline, 27 May 2026.",
    context="Three days before the 30 May 2026 general election; names both Labour and the PN.",
    verdict="Not substantiated", verdict_note="Shown for Labour, not for the PN",
    footer_lines=["Version 1.0  ·  5 October 2026", "Status: Draft, pending right of reply",
                  "Prepared from public sources and published literature.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Hunting laws – BirdLife Malta", version="1.0", date="5 October 2026",
    status_note="pending right of reply",
    pdf_title="A race to weaken hunting laws? Claim Check 050",
    pdf_subject="Tests BirdLife Malta's claim that Labour and the PN are racing to weaken hunting enforcement",
    story=S))
