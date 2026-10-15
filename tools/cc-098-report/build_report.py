"""Claim Check 098 report. Run calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []

# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("On 24 June 2026 Moviment Graffitti released a video and a statement saying that Malta Tourism Authority (MTA) officials "
        "had ordered a group of friends off “a rocky part of the public Blue Lagoon beach”, where there were “no sunbeds or "
        "umbrellas”, and “even threatened to call the police”. We could not watch the video. We checked what the authorities "
        "said in response, and what the law says about the foreshore.", lead)]
S.append(key_points([
    ("The account is not disputed.",
     "Three outlets describe the video as the NGO does, and a fourth reports the PN’s reaction. We found no denial: the Ministry for Tourism and the MTA "
     "answered that the area is public land, and the Prime Minister called it an “isolated episode” (Newsbook’s quotation)."),
    ("The authorities’ own statement agrees the area is public.",
     "The ministry and the MTA said the Blue Lagoon and the surrounding bathing areas remain public land and are open "
     "to everyone (TVM News’s indirect speech, not a direct quotation). The Lands Authority Act lists foreshores and portbeaches as "
     "public domain."),
    ("The Prime Minister is reported as saying the opposite.",
     "Newsbook reports him as saying the area was “not public”. The two government positions, as reported, do not match; "
     "we could not read either in the original."),
    ("What we cannot tell.",
     "We did not see the video, the concession agreements, or any MTA instruction to its officers. Whether the concession "
     "gives operators any right over the rocky foreshore cannot be tested without those documents."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("14 Jun", BLUE, "Date of the incident, per the NGO (video released 24 Jun 2026)"),
             ("0", GREEN, "Denials of the incident found in four outlets read in full"),
             ("Public", GREEN, "Ministry/MTA: the Blue Lagoon and surrounding bathing areas remain public land"),
             ("Not read", GREY, "Concession agreements and the video itself")]),
      Spacer(1, 4 * mm),
      up_down("Nothing: Supported is the top of the scale, and it would need an independent viewing of the video and the "
              "MTA’s own account of the incident. Moving from Largely supported to Supported would require both.",
              "An MTA or ministry account showing the officials acted on a documented instruction or concession term "
              "that covers that rocky area, or footage that differs from the NGO’s description."),
      Spacer(1, 3 * mm)]
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The claim record paraphrased an outlet’s account. We restated it from the NGO’s own release, published on its website "
           "on 24 June 2026 in English and Maltese [1]. We quote only words inside quotation marks in that release. The record’s "
           "locator, The Shift [2], is the outlet’s account of the release, not a separate source for the incident."))
S.append(std_table([
    [C("Source", cellh), C("What it says", cellh), C("Our access", cellh), C("Status", cellh)],
    [C("<b>Moviment Graffitti</b>, release, 24 Jun 2026 [1]"),
     C("The incident “took place on Sunday, 14 June 2026”; officials were “forcing a group of friends, who were lying on a rocky part "
       "of the public Blue Lagoon beach, to move away”; “there were no sunbeds or umbrellas in the area where they were sitting”; "
       "officials “ordered them to leave and even threatened to call the police”; concessions “in no way grant sunbed operators a "
       "permanent right of occupation, let alone the authority to use public officials to remove beachgoers from a public beach”."),
     C("Full text read, 15 Oct 2026. The video it links was not viewed."), C("<b>The claim</b> (speaker’s own words)")],
    [C("<b>Ministry for Tourism and MTA</b>, as reported by TVM News, 24 Jun 2026 [3]"),
     C("The Blue Lagoon and the surrounding bathing areas remain public land and are accessible to everyone (TVM’s indirect speech, no "
       "quotation marks). Also that managing the site requires ongoing decisions and that any protocols must respect the "
       "public’s right of access (TVM’s paraphrase)."),
     C("Full text read."), C("Response (outlet’s paraphrase)")],
    [C("<b>Prime Minister Robert Abela</b>, as reported by Newsbook, 25 Jun 2026 [4]"),
     C("Newsbook says he dismissed the video as an “isolated episode”, said the area was “not public”, and praised the MTA for upholding "
       "“discipline” (the quoted words are Newsbook’s; no transcript read)."),
     C("Full text read."), C("Response (outlet’s report)")],
    [C("<b>Lands Authority Act</b> (Cap. 563), art. 7(2)(c) [5]"),
     C("The Authority administers “all land that form part of the public domain such as the coastal perimeter, foreshores, harbours, "
       "quays, wharfs, pontoons, portbeaches, landing places”."),
     C("Consolidated text read, 15 Oct 2026."), C("<b>Primary (law)</b>")],
    [C("<b>The Shift, Lovin Malta</b> [2, 6]; MaltaToday and PN statement [3, 7]"),
     C("Describe the video and the NGO’s account in their own words. PN asked who gave the instruction and on what basis the area was "
       "said not to be public [3]."),
     C("The Shift, Lovin Malta, TVM read in full; MaltaToday 403 (titles only) ◆."), C("Context")],
], [38 * mm, 78 * mm, 30 * mm, 24 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("WHAT WE COULD NOT READ", tag),
               P("The video itself; the concession agreements for sunbeds and umbrellas at the Blue Lagoon; any MTA protocol or "
                 "instruction for its officers; the ministry statement as issued; any transcript of the Prime Minister. Routes tried "
                 "are in <i>literature/CC-098/README.md</i>; the search log is in <i>notes.md</i>.", small)],
              bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Questions.</b> (A) Did the incident happen as the NGO describes? (B) Is the rocky area part of a public beach? "
           "(C) Do sunbed and umbrella concessions confer a right to remove people from public foreshore?"))
S.append(P("<b>Evidence.</b> For A we compared the NGO’s release with every readable report and with the authorities’ responses, "
           "looking for any denial or different account. For B we read the authorities’ response and the Lands Authority Act. For C we looked for "
           "the concession terms and found none published. Dates are in <i>data/cc-098/checks.csv</i>. A video is a record of events, but we "
           "did not watch it, so A rests on an NGO account that is consistent across outlets and uncontested by the authorities."))
S.append(P("<b>Grades.</b> Law and primary statements are grade C; reports are grade D; this is a case with no experiment or "
           "dataset to test. <b>Verdicts</b> follow Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(3, "What the evidence shows"))
S.append(P("<b>The incident.</b> The NGO says officials of the MTA told a group lying on rocks at the Blue Lagoon to leave, although they were "
           "not on sunbeds or umbrellas, and threatened to call the police [1]. The Shift, Lovin Malta and Newsbook give the same account "
           "as the NGO’s [2, 4, 6]. The PN asked the Government and the MTA to explain who gave the instruction and on what basis the area was said "
           "not to be public [3]. The ministry and the MTA did not deny the incident in the statement TVM carries [3]. Reports of the Prime "
           "Minister’s reply call it an “isolated episode” [4]. We found no account that the incident did not happen."))
S.append(fig(FIG / "fig1_timeline.png", width=CW * 0.98))
S.append(P("Figure 1. Public record, 14 to 25 June 2026. Sources: Graffitti [1], TVM News [3], Newsbook [4]. Quotation marks are the "
           "outlets’.", cap))
S.append(P("<b>The area.</b> Under the Lands Authority Act the Authority administers land forming part of the public domain, including foreshores and "
           "portbeaches [5]. The ministry and the MTA said the Blue Lagoon and the surrounding bathing areas remain public land and are "
           "accessible to everyone, and that any protocols must respect public access [3]. The Prime Minister is reported as saying the area was "
           "“not public” [4]. If he meant the area occupied by sunbeds, the two statements could be reconciled; Newsbook’s text does not say, and "
           "we did not hear the remarks."))
S.append(P("<b>The concessions.</b> The NGO says concessions permit sunbeds and umbrellas in “certain parts” of the beach but give no right "
           "of permanent occupation [1]. We found no published concession text or legal notice setting the boundaries of the "
           "concession areas at the Blue Lagoon (search log in <i>notes.md</i>). The Act we read does not itself set beach concession "
           "limits [5]. This part of the claim is an argument about legal rights; we can say the authorities’ own statement is consistent "
           "with it, but not test it against the concession terms."))
S.append(callout([P("WHAT THIS DOES AND DOES NOT SHOW", tag),
                  P("It shows that the account is consistent across outlets, uncontested in what we could read, and in line with the authorities’ "
                    "statement that the area is public. It does not show what the officials were told, where the concession boundary lies, or "
                    "what the video contains beyond the descriptions.", small)],
                 bg=BLUE_PALE, bar=BLUE))

# ================================================================== 4
S.append(CondPageBreak(70 * mm))
S.append(SectionHeading(4, "Where the evidence points different ways"))
S.append(contested("Was the rocky area public?", "GOVERNMENT STATEMENTS DIFFER", AMBER,
                   "The Ministry for Tourism and the MTA said the Blue Lagoon and the surrounding bathing areas remain public land, "
                   "accessible to everyone [3]. The Lands Authority Act lists foreshores and portbeaches as public domain [5]. Graffitti "
                   "says the area is public and that concessions confer no right of occupation [1].",
                   "The Prime Minister is reported as saying the area was “not public” and as praising the MTA for upholding “discipline” [4]. "
                   "Newsbook says the officials insisted the area was private property [4]; MaltaToday’s title has them saying “It’s not public” [7◆]. The NGO’s release does not report what the officials said about status [1].",
                   "The ministry/MTA statement and the law, as we read them, support Graffitti on public status. We did not see the "
                   "concession map or any rule that would put that rocky area outside the public foreshore.",
                   label_a="EVIDENCE THE AREA IS PUBLIC", label_b="EVIDENCE FOR ‘NOT PUBLIC’"))

# ================================================================== 5
S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(5, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> On 14 Jun 2026 MTA officials ordered a group on a rocky part of the Blue Lagoon beach, with no sunbeds or umbrellas, to leave, and threatened to call the police"),
     C("Moviment Graffitti [1]"),
     C("Same account in The Shift, Lovin Malta and Newsbook; PN asked for an explanation; no denial in the ministry/MTA statement or in the Prime Minister’s reported reply [2, 3, 4, 6]. Video not viewed by us."),
     verd("CONSISTENT", GREENC)],
    [C("<b>B.</b> The Blue Lagoon beach is public"),
     C("Moviment Graffitti [1]"),
     C("Ministry/MTA say the Blue Lagoon and surrounding bathing areas remain public land [3]; the Lands Authority Act treats foreshores as public domain [5]. The PM is reported as saying the area was “not public” [4]."),
     verd("ACCURATE", GREENC)],
    [C("<b>C.</b> Concessions grant no permanent right of occupation and no authority to use officials to remove beachgoers"),
     C("Moviment Graffitti [1]"),
     C("A legal argument. The ministry/MTA statement says protocols must respect the public’s right of access [3]. Concession texts not published or not found; not tested."),
     verd("NOT TESTED", GREY)],
    [C("<b>D.</b> “Government-sponsored web of commercial interests”"), C("Moviment Graffitti [1]"),
     C("Opinion; the carrying-capacity study and visitor caps are context, not rated."), verd("NOT RATED", GREY)],
], [46 * mm, 24 * mm, 66 * mm, 28 * mm], valign="MIDDLE"))

# ================================================================== 6
S += [Spacer(1, 6 * mm), SectionHeading(6, "Verdict and requests for evidence"),
      verdict_box("Largely supported", "The incident and the public status of the beach are consistent with the evidence we could "
                  "read; the legal argument on concessions is not testable here. Confidence: moderate."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) The account of the incident is the same in every outlet we read and the authorities’ responses do not dispute it. "
           "(2) The ministry/MTA statement and the Lands Authority Act agree with the NGO that the area is public. (3) We rate <i>Largely "
           "supported</i> rather than <i>Supported</i> because we did not see the video, the concession terms or the MTA’s own account, and the claim "
           "on concession rights is a legal argument we could not test. (4) Confidence is moderate because the support is the "
           "consistency of reports and an official statement we read second-hand. The rating applies to the statement, not to the "
           "officials involved; the NGO itself does not call for action against them."))
S.append(CondPageBreak(60 * mm))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "The video, or the MTA’s account of the 14 June 2026 incident, and any instruction given to its officers.",
    "The concession agreements for sunbeds and umbrellas at the Blue Lagoon, with a map of the permitted areas.",
    "The ministry’s and the MTA’s statement of 24 June 2026 as issued, and the Prime Minister’s remarks in full.",
]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag),
               P("No right of reply is needed for this verdict (maintainer rule of 5 October 2026). Corrections and further evidence are welcome "
                 "through the contest form.", small)], bg=PALE, bar=GREEN)]

# ================================================================== 7
S += [Spacer(1, 6 * mm), SectionHeading(7, "Limitations")]
for l in ["We did not watch the video. Sub-claim A rests on the NGO’s account as repeated by outlets, several of which may rely on the same release.",
          "The ministry/MTA response is read through TVM News’s indirect speech, and the Prime Minister’s remarks through Newsbook’s "
          "quotation marks. We did not read either in the original.",
          "MaltaToday’s pages returned 403 to scripts; we saw only their titles in search results ◆ and use none as evidence.",
          "Our statement that no denial and no concession text were found covers the four outlets read in full and the web searches listed "
          "in notes.md, on 15 October 2026. The MTA’s own site and the e-tenders portal were not searched.",
          "The Lands Authority Act is cited for the public-domain status of foreshores only. We did not read other laws, policies or "
          "concession terms that could apply to this site, and we offer no legal opinion."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Moviment Graffitti (24 Jun 2026). VIDEO: Public officials enforce illegitimate private interests at the Blue Lagoon. Press release (EN/MT).",
     "https://movimentgraffitti.org/2026/06/24/video-public-officials-enforce-illegitimate-private-interests-at-the-blue-lagoon/"),
    ("2", "The Shift Team (24 Jun 2026). Visit Malta officials filmed telling citizens to leave deckchair-occupied beach in Comino. The Shift News.",
     "https://theshiftnews.com/2026/06/24/visit-malta-officials-filmed-telling-citizens-to-leave-deckchair-occupied-beach-in-comino/"),
    ("3", "Spiteri M. (24 Jun 2026). PN demands answers over Blue Lagoon incident and calls for publication of Comino Capacity Study. TVM News.",
     "https://tvmnews.mt/en/news/pn-demands-answers-over-blue-lagoon-incident-and-calls-for-publication-of-comino-capacity-study/"),
    ("4", "Newsbook (25 Jun 2026). Graffitti warns PM over Comino abuse: ‘This is only the tip of the iceberg’.",
     "https://newsbook.com.mt/en/graffitti-warns-pm-over-comino-abuse-this-is-only-the-tip-of-the-iceberg/"),
    ("5", "Lands Authority Act, Cap. 563, Laws of Malta, art. 7(2)(c). Consolidated text, retrieved 15 Oct 2026.",
     "https://legislation.mt/eli/cap/563/eng"),
    ("6", "Lovin Malta (24 Jun 2026). Watch: Officials order people off public Blue Lagoon beach.",
     "https://lovinmalta.com/news/local/watch-officials-order-people-off-public-blue-lagoon-beach/"),
    ("7", "MaltaToday (June 2026). WATCH: ‘It’s not public’: MTA officials tell beachgoer to leave Comino area occupied by sunbeds ◆ (title only; page returns 403).",
     "https://www.maltatoday.com.mt/news/national/142752/watch__its_not_public_mta_officials_tell_beachgoer_to_leave_comino_area_occupied_by_sunbeds_"),
    ("8", "Miżien. Calculation script and outputs: tools/cc-098-report/calc.py; data/cc-098/checks.csv.", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "15 Oct 2026", "First issue. Verdict Largely supported (moderate confidence); no right of reply needed.")])

build_report(Report(
    number="098", out=str(FIG / "report.pdf"), kicker="Tourism and population",
    title_lines=["Blue Lagoon:", "told to leave", "a public beach?"],
    subtitle_lines=["Testing Moviment Graffitti’s account of", "14 June 2026 against the authorities’ response"],
    quote_lines=["“…ordered them to leave and even threatened", "to call the police.”"], quote_size=14,
    attribution="Moviment Graffitti, press release, 24 June 2026.",
    context="Speaker’s own words, English text of the release.",
    verdict="Largely supported", verdict_note="Incident and public status consistent with the evidence read",
    footer_lines=["Version 1.0  ·  15 October 2026", "Status: no right of reply needed",
                  "Prepared from public sources and the Laws of Malta.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Blue Lagoon: told to leave a public beach?", version="1.0", date="15 October 2026",
    pdf_title="Blue Lagoon: told to leave a public beach? Claim Check 098",
    pdf_subject="Tests Moviment Graffitti's account of MTA officials at the Blue Lagoon on 14 June 2026",
    story=S))
