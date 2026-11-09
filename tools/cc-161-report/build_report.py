"""Claim Check 161 report. Run calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []

# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("On 3 March 2026 the Parliamentary Ombudsman published Part 2 of a two-part note on nightlife noise. Its "
        "conclusion reads: <b>“Residents complain without effective remedy.”</b> It also says that “regular (not "
        "exceptional) nightlife establishments are licenced to operate close to residential areas” and that "
        "“public authorities know and acknowledge excessive noise.” We tested whether public data can show the "
        "outcome statement.", lead)]
S.append(key_points([
    ("The wording is the Ombudsman’s own.",
     "We read Part 2 [1] and Part 1 [2] in full. Part 2 is a summary of two European Court of Human Rights "
     "judgments against Spain; its three-sentence conclusion contains the claim and no figures."),
    ("Part 1 gives a structural reason a remedy could be weak.",
     "It lists five laws and four enforcing bodies and calls the framework “fragmented and weak”, with "
     "enforcement that is reactive: for the police, “action frequently occurs following complaints” [2]."),
    ("No outcome data are published that would test “without effective remedy”.",
     "We found no count of noise complaints, fines, closures or time to resolution for nightlife venues (search "
     "log in <i>literature/CC-161/notes.md</i>). The one count we found, 98 police reports in four localities "
     "over 18 months in 2021–22 ◆, measures reports received, not what happened to them."),
    ("A remedy was obtained in one related case.",
     "After residents complained about boat parties, Transport Malta issued Notice to Mariners 115 of 2025 on "
     "11 July 2025 following Ombudsman action [3]. That is not a licensed venue on land, and shows only that "
     "some complaints lead to rules."),
    ("Verdict: not substantiated (low confidence).",
     "The statement may well be true, and the Ombudsman’s casework may hold the evidence, but neither Part 2 nor "
     "any public dataset we could reach shows it."),
]))
S += [Spacer(1, 2 * mm), VerdictMeter(2), Spacer(1, 2 * mm),
      tiles([("5", GREEN, "Laws with a noise role listed in Part 1 [2]"),
             ("0", GREY, "Outcome figures in Part 2 [1]"),
             ("98", ORANGE, "Police reports of excessive noise, four localities, Jan 2021–Jun 2022 (second-hand)"),
             ("1", GREEN, "Remedy documented: boat-party noise rules, July 2025 [3]")]),
      Spacer(1, 2 * mm),
      up_down("Published outcome data (police, Planning Authority, ERA, Malta Tourism Authority, local councils) showing "
              "that nightlife-noise complaints rarely end in fines, closures or abatement, or the case file summaries "
              "behind the Ombudsman’s finding.",
              "Outcome data showing that most such complaints are resolved within a stated time (for example by "
              "abatement, fines or licence action)."),
      Spacer(1, 2 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What would count as a remedy"),
          ("4", "What the evidence shows"), ("5", "Where the evidence points different ways"),
          ("6", "Testing the claim"), ("7", "Verdict and requests for evidence"), ("8", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The statement is the last section of the Office of the Ombudsman’s note of 3 March 2026 [1], which we "
           "read in full on 9 November 2026. Part 1, published on 2 March 2026 [2], sets out the legal framework. We "
           "assess the Ombudsman’s own words."))
S.append(std_table([
    [C("What was said [1]", cellh), C("Form", cellh), C("Our access", cellh)],
    [C("“In Malta regular (not exceptional) nightlife establishments are licenced to operate close to residential "
       "areas.”"), C("Direct quote"), C("Read in full")],
    [C("“Public authorities know and acknowledge excessive noise.”"), C("Direct quote"), C("Read in full")],
    [C("“Residents complain without effective remedy.”"), C("Direct quote (the claim)"), C("Read in full")],
], [104 * mm, 36 * mm, 30 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("FAIRNESS NOTE", tag),
               P("Part 2 is a legal summary of two Spanish cases, <i>Moreno Gómez v Spain</i> (2005) and <i>Cuenca "
                 "Zarzoso v Spain</i> (2018), both as described by the Ombudsman and not read by us. Its "
                 "conclusion is a finding of the Ombudsman’s office, which receives complaints and may hold "
                 "casework we cannot see. The note gives no figures and does not claim to be a statistical study. "
                 "This check asks whether the outcome statement can be tested with public data, not whether the "
                 "Ombudsman is right to raise the issue.", small)],
              bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Question.</b> Is there public evidence on what happens to residents’ complaints about nightlife noise, "
           "and does it show that they have no effective remedy?"))
S.append(P("<b>Evidence.</b> We read both parts of the Ombudsman’s note [1, 2], the Ombudsman’s case note on boat-party "
           "noise [3] and a news report of a parliamentary answer on police noise reports [4]. We searched for "
           "complaint and enforcement counts on 9 November 2026 (log in <i>literature/CC-161/notes.md</i>). "
           "The parliamentary text and Planning Authority, ERA and Malta Tourism Authority records were not "
           "reachable or did not contain such counts. All counts are in <i>data/cc-161/</i> and derived values are "
           "recomputed by <i>tools/cc-161-report/calc.py</i>. Second-hand figures are marked ◆ and are not used to "
           "decide any rating."))
S.append(P("<b>Grades.</b> The Ombudsman’s legal analysis and case note are official documents (grade C). The news "
           "report of a parliamentary answer is grade C but second-hand. <b>Verdicts</b> follow the five-point scale "
           "in Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(60 * mm))
S.append(SectionHeading(3, "What would count as a remedy"))
S.append(P("“Effective remedy” is a legal phrase, and Part 2 does not define it for this purpose. For a check, it "
           "has to be turned into something observable. We use four measures, each of which a public body could "
           "report: (1) the share of noise complaints about licensed venues that lead to a recorded action (warning, "
           "fine, licence condition, closure order); (2) the time from complaint to action; (3) whether the noise "
           "stops or falls, for example in a repeat measurement; (4) repeat complaints about the same venue. None of "
           "these is published for Malta in the sources we could reach. This is a choice of ours, not the "
           "Ombudsman’s; a court might apply a different test."))
S.append(P("Part 1 describes why the first measure could be low. Five laws touch noise (Criminal Code, Malta Tourism "
           "and Travel Services Act, Trading Licences Act, Environment Protection Act, Development Planning Act) with "
           "the police, Malta Tourism Authority, the Environment and Resources Authority and the Planning "
           "Authority as enforcers. It says the Environment Protection Act “does not set entertainment decibel "
           "thresholds”, that planning enforcement “tends to be reactive”, and that residents cannot be sure which "
           "authority to approach [2]. That is a documented mechanism, not a measured outcome."))

# ================================================================== 4
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(4, "What the evidence shows"))
S.append(fig(FIG / "fig1_police_reports.png"))
S.append(P("Figure 1. Reports of excessive noise to the police, January 2021 to June 2022, as reported by Lovin Malta [4] "
           "from a parliamentary answer we could not read ◆. Second-hand. These are reports received, not outcomes.", cap))
S.append(std_table([
    [C("Indicator", cellh), C("Value", cellh), C("Source", cellh), C("Use here", cellh)],
    [C("Laws and enforcing bodies for entertainment noise"), C("5 laws; police, MTA, ERA, PA"), C("[2]"),
     C("Mechanism")],
    [C("Outcome figures in the Ombudsman’s Part 2"), C("None"), C("[1]"), C("Limits what can be tested")],
    [C("Police reports of excessive noise, 4 localities, 18 months"), C("98 (34 after 23:00) ◆"), C("[4], calculated"),
     C("Context only")],
    [C("Police reports a month, four localities together"), C("about 5 ◆"), C("calculated"), C("Context only")],
    [C("Remedy after Ombudsman action: boat-party noise"), C("Notice to Mariners 115/2025, 11 Jul 2025"), C("[3]"),
     C("Counter-example")],
    [C("Fines, closures, time to resolve for nightlife venues"), C("Not found"), C("search log"), C("Gap")],
], [58 * mm, 46 * mm, 30 * mm, 36 * mm]))
S.append(P("All values in <i>data/cc-161/checks.csv</i>. The 2022 counts pre-date the Ombudsman’s note by more than "
           "three years and cover four localities only.", cap))
S.append(P("Reading across the evidence", h2))
for t in ["• <b>The statement is plausible and partly explained.</b> Part 1 documents fragmented, complaint-driven "
          "enforcement, which is the kind of setting in which a remedy can be slow or unclear [2].",
          "• <b>It has not been measured.</b> We found no public count of complaints or outcomes, so we cannot say how "
          "many residents obtain relief and how many do not.",
          "• <b>Low police-report counts do not show a failure.</b> A small number of reports can mean few problems, "
          "residents using other channels, or reports not being made; the figure cannot tell these apart ◆ [4].",
          "• <b>One remedy exists in a neighbouring area.</b> The boat-party case shows that complaints to the "
          "Ombudsman can lead to a rule change [3]; it says nothing about land-based venues."]:
    S.append(P(t, bul))

# ================================================================== 5
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(5, "Where the evidence points different ways"))
S.append(contested(
    "Q1  Do residents lack an effective remedy?", "NOT SHOWN EITHER WAY", AMBER,
    "Part 1 describes five overlapping laws, no decibel limits for entertainment, reactive enforcement and unclear "
    "jurisdiction; it says residents have no one authority to approach with confidence [2].",
    "A remedy was obtained for boat-party noise after complaints [3], and the Ombudsman’s role itself is a "
    "complaints route. No data on the share of nightlife complaints that lead to action are published in the "
    "sources we could reach.",
    "<b>For this claim:</b> the mechanism is credible; the outcome is not measured."))
S.append(contested(
    "Q2  Are nightlife venues licensed near homes as a rule?", "PLAUSIBLE, NOT COUNTED", AMBER,
    "The Ombudsman states it as a general fact [1], and Part 1 refers to noise spilling into residential areas "
    "[2].",
    "We did not find a register or map of licensed venues and nearby dwellings, so the “regular, not exceptional” "
    "part is untested.",
    "<b>For this claim:</b> not rated beyond ‘untested’."))

# ================================================================== 6
S.append(CondPageBreak(80 * mm))
S.append(SectionHeading(6, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> “regular (not exceptional) nightlife establishments are licenced to operate close to residential "
       "areas”"),
     C("Stated without data in [1]; Part 1 describes noise spilling into residential areas [2]. No register of "
       "venues and dwellings found."), verd("UNTESTED", GREY)],
    [C("<b>B.</b> “Public authorities know and acknowledge excessive noise”"),
     C("The Ombudsman’s office and Transport Malta (for boats) have acknowledged noise problems [2, 3]. We did "
       "not read statements from the police, Planning Authority or ERA on nightlife noise."),
     verd("PARTLY SHOWN", AMBER)],
    [C("<b>C.</b> “Residents complain without effective remedy”"),
     C("Mechanism documented [2]; no outcome data published; one remedy in a related case [3]; police-report "
       "counts ◆ are inputs, not outcomes [4]."), verd("NOT SUBSTANTIATED", colors.HexColor("#C85A3A"))],
], [52 * mm, 88 * mm, 30 * mm], valign="MIDDLE"))

# ================================================================== 7
S += [Spacer(1, 6 * mm), SectionHeading(7, "Verdict and requests for evidence"),
      verdict_box("Not substantiated", "Credible mechanism, no outcome data. Confidence: low. This is not a finding "
                  "that the statement is false."),
      Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) The note is explicit about the legal framework but gives no figure on what happens to "
           "complaints. (2) We found no public series that could show it, and the one count we found measures "
           "reports, not results. (3) Where a remedy can be traced, in the boat-party case, one was obtained. Our "
           "scale defines <i>Not substantiated</i> as a claim stated more strongly than the evidence offered or "
           "available allows, which “may be true in some conditions but has not been shown”."))
S.append(P("<b>What this verdict does not say.</b> It does not say that residents are well served, that the Ombudsman "
           "is wrong, or that anyone acted in bad faith. Complaints files that the Ombudsman and public bodies hold, "
           "but we cannot see, could change this."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "From the Ombudsman: the number and outcome of nightlife-noise complaints that support the finding, in "
    "anonymised form.",
    "From the police, Planning Authority, ERA, Malta Tourism Authority and local councils: noise complaints about "
    "licensed venues per year, and how many ended in a fine, closure, licence condition or abatement, with "
    "time to resolution.",
    "The text and date of the parliamentary answer behind the 2021–22 police figures, and updates since.",
    "A register of licensed entertainment venues with distance to the nearest dwelling.",
]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag),
               P("Before wider circulation this draft should be offered to the Office of the Ombudsman with a fixed "
                 "deadline (suggested 14 days). Under our standards a <i>Not substantiated</i> verdict is not "
                 "circulated before that deadline passes. Responses will be appended and the verdict revisited.", small)],
              bg=AMBER_PALE, bar=AMBER)]

# ================================================================== 8
S += [Spacer(1, 6 * mm), SectionHeading(8, "Limitations")]
for l in ["Our definition of ‘effective remedy’ is operational and ours (Section 3). A legal test could differ.",
          "The police counts are second-hand (a news report of a parliamentary answer we could not read), cover four "
          "localities and 18 months of 2021–22, and count reports rather than outcomes.",
          "We did not read the Spanish judgments; they are described as in the Ombudsman’s note. They do not bear on "
          "the Maltese outcome data.",
          "Absence of evidence: we searched the places listed in the notes file on 9 November 2026 and could not "
          "reach parlament.mt, era.org.mt, the Planning Authority and Malta Tourism Authority records beyond "
          "web search. The statement that no outcome series is published holds only for what we could reach.",
          "No peer-reviewed study of enforcement outcomes for Maltese nightlife noise was found; the WHO "
          "Environmental Noise Guidelines (2018), named in the note, are context and were not used for any figure."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Office of the Ombudsman, Malta (3 Mar 2026). Curbing uncontrolled and abusive noise in entertainment and "
          "other places: Part 2 – A human rights issue.",
     "https://ombudsman.org.mt/news-and-events/curbing-uncontrolled-and-abusive-noise-in-entertainment-and-other-places-part-2-a-human-rights-issue/"),
    ("2", "Office of the Ombudsman, Malta (2 Mar 2026). Curbing uncontrolled and abusive noise in entertainment and "
          "other places – Part 1 – Structural regulatory weaknesses (copy on the European Network of Ombudsmen site).",
     "https://eno.ombudsman.europa.eu/home/news/maincontent/curbing-uncontrolled-and-abusive.html"),
    ("3", "Office of the Ombudsman, Malta (15 Jul 2025). Ombudsman’s intervention leads to stricter noise controls on "
          "boat parties.",
     "https://ombudsman.org.mt/case-work/ombudsman-s-intervention-leads-to-stricter-noise-controls-on-boat-parties"),
    ("4", "Lovin Malta (6 Oct 2022). Think reports to Malta’s police over noisy late-night neighbours are ignored? "
          "(Reports a parliamentary answer by the Minister for Home Affairs; second-hand ◆.)",
     "https://lovinmalta.com/news/think-reports-to-maltas-police-over-noisy-late-night-neighbours-are-ignored-these-figures-seem-to-prove-it"),
    ("5", "MiŻien. Data and calculations: data/cc-161/ (police_noise_reports.csv, checks.csv); "
          "tools/cc-161-report/calc.py.", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "9 Nov 2026", "First issue. Draft pending right of reply from the Office of the Ombudsman.")])

build_report(Report(
    number="161", out=str(FIG / "report.pdf"), kicker="Nightlife noise",
    title_lines=["“Without", "effective", "remedy”?"],
    subtitle_lines=["Testing the Ombudsman’s finding on nightlife noise", "for the evidence behind it"],
    quote_lines=["“Residents complain without", "effective remedy.”"], quote_size=16,
    attribution="Parliamentary Ombudsman, Part 2 of ‘Curbing uncontrolled and abusive noise’, 3 March 2026.",
    context="Said of regular nightlife establishments licensed near homes.",
    verdict="Not substantiated", verdict_note="A credible mechanism, but no published outcome data",
    footer_lines=["Version 1.0  ·  9 November 2026", f"Status: {reply_status('Not substantiated')}",
                  "Prepared from public sources.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Nightlife noise – Malta", version="1.0", date="9 November 2026",
    pdf_title="Without effective remedy? Claim Check 161",
    pdf_subject="Tests the Ombudsman's statement that residents complain without effective remedy about nightlife noise",
    story=S))
