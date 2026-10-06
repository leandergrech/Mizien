"""Claim Check 029 report. Run fetch.py, calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []

# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("On 22 July 2025 the Energy Ministry said Malta’s first floating wind farm, of “approximately 300MW”, would be built "
        "“beyond Malta’s territorial waters”, that three submissions had been received for the first stage, and that the "
        "plan was to inform qualifying candidates of the next phase “by the first part of next year”. We checked the facts "
        "against the project’s own documents and Eurostat data, and the timetable against what has been published since.", lead)]
S.append(key_points([
    ("The facts hold.",
     "InterConnect Malta (ICM), the government company running the process, describes a floating wind farm of around "
     "300 MW beyond the 12-nautical-mile limit, in an area to be declared as Malta’s Exclusive Economic Zone. Three "
     "submissions were announced on 22 July 2025, from named applicants."),
    ("The output claim is consistent with national data.",
     "ICM says the farm would give up to 0.8 TWh a year, about 25% of Malta’s electricity demand as it stood in 2025. "
     "That implies a 30% capacity factor and matches 25% of the 3,252 GWh Eurostat shows Malta supplied in 2025 "
     "(production plus imports); it is 27% of final consumption."),
    ("The timetable has slipped, as far as the public record shows.",
     "The “first part of 2026” step, telling qualifying candidates they may continue, has no public notice. ICM’s news "
     "list to 3 October 2026 and its tenders page record none. It did issue a EUR 3.6 million metocean survey tender in "
     "April 2026, to gather two years of site data for developers."),
    ("What we cannot tell.",
     "The notice to candidates may have been sent privately, and the government may have revised the plan without "
     "publishing it. A press report we could only see in a search summary says the next stage was expected around April 2026 "
     "and a contractor by the end of 2027; we mark it second-hand."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("≈300 MW", GREEN, "Capacity, beyond 12 nautical miles (ICM, Energy Ministry)"),
             ("3", GREEN, "Submissions to the first stage, announced 22 Jul 2025"),
             ("≈25%", GREEN, "Of 2025 electricity supplied would come from the farm (ICM figure; our check 24.6%)"),
             ("Off track", ORANGE, "Pledge label for the “first part of 2026” step, as of 6 Oct 2026")]),
      Spacer(1, 4 * mm),
      up_down("None for the facts. They rest on the project’s own documents and one national dataset; Supported would need "
              "an independent record of the final site and capacity, which will exist only after a concession is awarded.",
              "A published notice, or a PQQ document, showing that qualifying candidates were informed in the first part of "
              "2026 would move the label to On track or Met. A published revised timetable would reset the baseline. "
              "A final contract at a different capacity would change the factual rating."),
      Spacer(1, 3 * mm)]
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The Energy Ministry announced the result of the first stage on 22 July 2025. TVM News published the ministry’s "
           "statement and a quotation from the Minister, Miriam Dalli [1]; Newsbook published the same announcement [2]. "
           "The maintainer supplied the passages (<i>literature/CC-029/primary-source.md</i>) and we re-read both pages in full. "
           "The ministry’s own page and ICM’s site carry the project description [3, 4]. Only the minister’s words inside "
           "quotation marks are quoted; the rest is the ministry statement as the outlet reports it."))
S.append(std_table([
    [C("Source", cellh), C("What it says", cellh), C("Our access", cellh), C("Status", cellh)],
    [C("<b>Energy Ministry statement</b>, as reported by TVM News, 22 Jul 2025 [1]"),
     C("The wind farm “will be located beyond Malta’s territorial waters”, in an area to be declared part of the EEZ, with “an installed "
       "capacity of approximately 300MW”; three submissions; the “current plan is to inform candidates who qualify for the next phase "
       "by the first part of next year” (TVM’s rendering of the statement)."),
     C("Read in full, 6 Oct 2026."), C("<b>The claim</b> (statement as reported)")],
    [C("<b>Minister Miriam Dalli</b> [1, 2]"),
     C("“What was once an exploratory initiative has now entered a structured phase”; “an important step forward for the project and a "
       "clear signal that the process has truly kicked off.”"),
     C("Read in full."), C("Quoted")],
    [C("<b>InterConnect Malta</b>, project page and news, 5 Dec 2024 to 22 Apr 2026 [3, 4, 5, 6]"),
     C("Around 300 MW; 12 nautical miles or more offshore; up to 0.8 TWh a year; a three-step competitive dialogue (qualification "
       "questionnaire, invitation to dialogue, best and final offer); two sites; submissions deadline extended to 21 Jul 2025; a "
       "metocean tender of 22 Apr 2026."),
     C("Read in full, 6 Oct 2026."), C("<b>Primary (government company)</b>")],
    [C("<b>Eurostat</b>, nrg_cb_e [7]"), C("Malta electricity production, imports, exports and final consumption, 2019 to 2025."),
     C("Downloaded 6 Oct 2026 (data/cc-029/)."), C("<b>Primary data</b>")],
    [C("<b>Trade and press reports</b> [8, 9, 10]"),
     C("Repeat the timetable; one (MaltaToday, 403 to us, seen in a search summary only ◆) says the dialogue stage was planned "
       "around April 2026 and the contractor’s selection for the end of 2027."),
     C("Trade pages read; MaltaToday not read."), C("Context; second-hand ◆")],
], [40 * mm, 72 * mm, 32 * mm, 26 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("WHAT WE COULD NOT READ", tag),
               P("The qualification questionnaire documents, the e-tenders notices and any letters to candidates were not available "
                 "to us (the ministry and ICM’s e-tender portal are browser-only or refused scripted access). The National Energy and "
                 "Climate Plan’s offshore wind assumption was not read and is not used. Routes tried are in "
                 "<i>literature/CC-029/README.md</i>.", small)],
              bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Questions.</b> (A) Is the project as described: a floating farm of about 300 MW beyond territorial waters? "
           "(B) Were there three first-stage submissions? (C) Is the stated output plausible against national demand? "
           "(D) Did the next stage happen when the plan said?"))
S.append(P("<b>Evidence.</b> For A and B we read the ministry statement and ICM’s own pages. For C we downloaded Malta’s electricity "
           "balance from Eurostat (nrg_cb_e, siec E7000, GWh) with <i>fetch.py</i> and computed the shares with <i>calc.py</i> "
           "(<i>data/cc-029/checks.csv</i>). The 2025 values carry the Eurostat provisional flag. For D we looked for a published notice "
           "in ICM’s news list, ICM’s tenders page, trade media and a search of the project’s name, between July 2025 and 6 October 2026."))
S.append(P("<b>The limit of D.</b> Absence of a public notice is not proof that nothing happened: candidates can be told privately. "
           "It does show that no progress after the qualification stage has been published, which is what a pledge label judges."))
S.append(P("<b>Grades.</b> Official statistics and government project documents are grade C; news and trade reports are grade D and are "
           "used to locate what was announced. <b>Verdicts</b> and <b>pledge labels</b> follow Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(3, "What the evidence shows"))
S.append(P("<b>The description.</b> ICM’s project page says the concession covers design, construction, operation, maintenance and "
           "decommissioning of an offshore floating wind farm beyond Malta’s 12-nautical-mile territorial waters, with the substation and "
           "export cable owned by the government, “around 300MW” delivered to the 132 kV network, “up to 0.8 TWh” a year, under a 35-year "
           "agreement with a two-way contract for difference [4]. Two sites are on offer, one of which will be developed [4, 6]."))
S.append(P("<b>The submissions.</b> The first-stage questionnaire was issued on 5 December 2024 [5]. Its deadline, originally 28 March "
           "2025 ◆, was extended by 115 days to 21 July 2025 after clarification requests [5a]. Three submissions followed: the Code Zero "
           "Consortium (led by SEP (Malta) Holding Ltd), Atlas Med Wind (managed by GreenIT SpA, Italy) and MCKEDRIK Sole Member Ltd "
           "(Greece) [1, 2]. ICM’s December 2024 notice said only the top five candidates would be invited to the next stage [5]; with "
           "three submissions, that limit is not a constraint."))
S.append(fig(FIG / "fig1_timeline.png", width=CW * 0.98))
S.append(P("Figure 1. Public milestones of the first offshore wind concession against the timetable stated on 22 July 2025. "
           "Sources: ICM news, TVM News, offshoreWIND.biz [1, 5, 6, 9].", cap))
S.append(P("<b>The output.</b> 0.8 TWh from 300 MW is a capacity factor of 30.4%, a plausible value for offshore wind. Eurostat gives Malta’s "
           "2025 final electricity consumption as 2,970 GWh and electricity supplied (production plus imports minus exports) as 3,252 GWh, "
           "31.7% of it imported by cable [7]. 0.8 TWh is 26.9% of consumption and 24.6% of supply, so ICM’s “25% of overall demand as it "
           "stood in 2025” [6] matches the supply measure."))
S.append(fig(FIG / "fig2_share.png", width=CW * 0.95))
S.append(P("Figure 2. The farm’s stated output against Malta’s 2025 electricity supply and consumption (Eurostat, 2025 provisional).", cap))
S.append(P("<b>The timetable.</b> The 22 July 2025 statement set the plan: tell qualifying candidates “by the first part of next year”, "
           "while ICM prepared technical and financial criteria for them [1]. By 6 October 2026, 98 days after the end of June, the end of "
           "what we read as “the first part” of 2026, ICM’s news list and tenders page record no notice of qualification or of the "
           "invitation to dialogue. What ICM did publish, on 22 April 2026, was a EUR 3.6 million tender for two years of metocean "
           "measurements at both sites (deadline 21 May 2026), said to let “prospective developers” prepare proposals [6, 9]. That is "
           "progress on the project, but it is not the step the plan named."))
S.append(callout([P("WHAT THIS DOES AND DOES NOT SHOW", tag),
                  P("It shows that the project exists as described and that the one public milestone after the questionnaire is a "
                    "data-collection tender. It does not show the project has failed or that the candidates were not told: the "
                    "statement concerned an internal evaluation, and a due-diligence step could take longer than planned.", small)],
                 bg=BLUE_PALE, bar=BLUE))

# ================================================================== 4
S.append(Spacer(1, 4 * mm))
S.append(SectionHeading(4, "Where the evidence points different ways"))
S.append(contested("Has the next stage kept to the stated timetable?", "NO PUBLIC SIGN", AMBER,
                   "The project is active: ICM issued the metocean tender in April 2026 and still describes the competitive "
                   "dialogue structure; the ministry’s plan was a statement of intent, and evaluation of three bulky submissions "
                   "was said to be thorough [1, 6].",
                   "No public notice of qualification or of the dialogue stage by 6 October 2026, three months after the end of the "
                   "“first part” of the year. The metocean tender, which comes with two years of data collection, looks like a "
                   "longer path. A search summary of a press report puts the dialogue stage around April 2026 ◆ [10].",
                   "Both can be true: the work continues, and the stated date was missed in public terms. Only the candidates and "
                   "ICM know whether the notice was sent. We rate what has been published.",
                   label_a="EVIDENCE OF PROGRESS", label_b="EVIDENCE OF DELAY"))

# ================================================================== 5
S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(5, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> A first floating wind farm of about 300 MW, beyond territorial waters"), C("Energy Ministry [1]"),
     C("ICM’s project page gives the same capacity, floating technology and position beyond 12 nautical miles [4]."),
     verd("ACCURATE", GREENC)],
    [C("<b>B.</b> Three submissions to the first stage"), C("Energy Ministry [1]"),
     C("Three named applicants; announced 22 Jul 2025 by the ministry; same in Newsbook and trade media [1, 2, 9]."),
     verd("ACCURATE", GREENC)],
    [C("<b>C.</b> Output: around a quarter of 2025 demand (ICM)"), C("ICM [6]"),
     C("0.8 TWh is 24.6% of 2025 electricity supplied and 26.9% of final consumption (Eurostat) [7]."),
     verd("CONSISTENT", GREENC)],
    [C("<b>D.</b> Qualifying candidates informed “by the first part” of 2026"), C("Energy Ministry [1]"),
     C("No public notice by 6 Oct 2026; a metocean tender was issued in April 2026 instead; a private notice cannot be excluded."),
     verd("OFF TRACK (PLEDGE)", ORANGE)],
], [42 * mm, 24 * mm, 70 * mm, 34 * mm], valign="MIDDLE"))

# ================================================================== 6
S += [Spacer(1, 6 * mm), SectionHeading(6, "Verdict, pledge and requests for evidence"),
      verdict_box("Largely supported", "The project, its size and the three submissions are as stated; the timetable is rated "
                  "as a pledge: Off track. Confidence: moderate."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) The factual statements, capacity, position and number of submissions, are confirmed by the government’s own "
           "project documents and the announcement. (2) The output figure agrees with Eurostat data. (3) We rate <i>Largely supported</i> "
           "rather than <i>Supported</i> because the project is a plan, no concession has been awarded, and the capacity and site may "
           "change in the dialogue. (4) The timetable is a plan, not a fact, so it is rated under the pledge scale. Confidence is "
           "moderate because the sources are the project’s own documents and the timetable rating depends on absence of a notice."))
S.append(callout([P("PLEDGE LABEL: OFF TRACK (AS OF 6 OCT 2026)", tag),
                  P("The step “inform qualifying candidates by the first part of 2026” has no published sign by 6 October 2026, while "
                    "ICM has published a later data-collection tender. The label is Off track, not Missed, because the evidence that "
                    "would show it missed (a statement that the step has not happened, or a revised date) was not found, and the "
                    "notice may have been private. It judges delivery against the pledge as worded, not anyone’s intent.", small)],
                 bg=AMBER_PALE, bar=AMBER))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "The date candidates were informed of the result of the qualification stage, and how many qualified.",
    "A current timetable for the invitation to participate in dialogue and the best and final offer.",
    "The e-tenders notice and documents for the metocean survey, and the award, if made.",
    "The offshore wind assumption (capacity and year) in Malta’s National Energy and Climate Plan, for comparison with 300 MW.",
]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag),
               P("A reply is sought for the pledge label <i>Off track</i> (maintainer rule of 5 October 2026). The maintainer handles "
                 "it; nothing has been sent. Until the deadline has passed this is a draft label on this site only and is not "
                 "to be circulated elsewhere.", small)], bg=AMBER_PALE, bar=AMBER)]

# ================================================================== 7
S += [Spacer(1, 6 * mm), SectionHeading(7, "Limitations")]
for l in ["The ministry’s statement is read through TVM News and Newsbook; the ministry’s own release was refused to scripts. Only the "
          "minister’s words are in quotation marks.",
          "We read no tender documents. Capacity, position and output come from ICM’s web pages; the e-tenders portal was not read.",
          "The Off track label rests on the absence of a public notice, which is weaker evidence than a dated statement.",
          "“The first part of 2026” is not defined in the statement; we read it as ending on 30 June 2026. Reading it more "
          "loosely would shorten the gap but not remove it.",
          "Eurostat 2025 values are provisional. ICM’s 25% is compared with supply and consumption as defined by Eurostat; "
          "ICM does not say which measure it used.",
          "The MaltaToday report of the April 2026 dialogue date and 2027 contractor selection was seen only in a search summary."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "TVM News (22 Jul 2025). Three submissions presented for the first offshore wind farm concession in Malta.",
     "https://tvmnews.mt/en/news/three-submissions-presented-for-the-first-offshore-wind-farm-concession-in-malta/"),
    ("2", "Balzan J. (22 Jul 2025). Three firms bid for Malta’s first offshore wind farm concession. Newsbook.",
     "https://newsbook.com.mt/en/three-firms-bid-for-maltas-first-offshore-wind-farm-concession/"),
    ("3", "InterConnect Malta. News and events list (read 6 Oct 2026).", "https://icm.mt/news-events/"),
    ("4", "InterConnect Malta. Offshore Renewable Energy Project (read 6 Oct 2026).",
     "https://icm.mt/projects/offshore-renewable-energy-project/"),
    ("5", "InterConnect Malta (5 Dec 2024). Malta launches preliminary qualification questionnaire for offshore floating wind farm "
          "project; and (27 Mar 2025) submission deadline extended [5a].",
     "https://icm.mt/malta-launches-preliminary-qualification-questionnaire-for-offshore-floating-wind-farm-project/"),
    ("6", "InterConnect Malta (22 Apr 2026). Offshore floating wind farm: ICM issues tender to collect data on wind, wave conditions.",
     "https://icm.mt/offshore-floating-wind-farm-icm-issues-tender-to-collect-data-on-wind-wave-conditions/"),
    ("7", "Eurostat. Supply, transformation and consumption of electricity (nrg_cb_e), Malta, retrieved 6 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/nrg_cb_e/default/table"),
    ("8", "offshoreWIND.biz (23 Jul 2025). Three applications submitted in Malta’s first offshore wind tender.",
     "https://www.offshorewind.biz/2025/07/23/three-applications-submitted-in-maltas-first-offshore-wind-tender"),
    ("9", "offshoreWIND.biz (21 Apr 2026). Malta opens EUR 3.6 million offshore wind metocean survey tender.",
     "https://www.offshorewind.biz/2026/04/21/malta-opens-eur-3-6-million-offshore-wind-metocean-survey-tender"),
    ("10", "MaltaToday. Miriam Dalli: offshore wind farm contractor to be selected by start of 2028. ◆ Seen only as a search result; "
           "page returns 403. Second-hand.",
     "https://www.maltatoday.com.mt/news/national/136333/miriam_dalli_offshore_wind_farm_contractor_to_be_selected_by_end_2027"),
    ("11", "Miżien. Calculation script and outputs: tools/cc-029-report/calc.py; data/cc-029/checks.csv.", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.", pledges=True)
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "6 Oct 2026", "First issue. Verdict Largely supported (moderate confidence); pledge label Off track; "
                                         "pending right of reply.")])

build_report(Report(
    number="029", out=str(FIG / "report.pdf"), kicker="Climate and energy",
    title_lines=["Malta’s first", "offshore wind farm:", "on schedule?"],
    subtitle_lines=["Testing the Energy Ministry’s capacity, bids", "and timetable against public records"],
    quote_lines=["“…located beyond Malta’s territorial waters… an installed", "capacity of approximately 300MW…”",
                 "“…inform candidates who qualify… by the first part of next year.”"], quote_size=13,
    attribution="Energy Ministry statement, 22 July 2025 (as reported by TVM News).",
    context="Statement as reported; only Minister Dalli’s words are in quotation marks in the source.",
    verdict="Largely supported", verdict_note="Facts hold; the timetable is Off track (pledge)",
    footer_lines=["Version 1.0  ·  6 October 2026", "Status: draft, pending right of reply (pledge label)",
                  "Prepared from public sources and Eurostat data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Malta’s first offshore wind farm", version="1.0", date="6 October 2026",
    status_note="pending right of reply",
    pdf_title="Malta's first offshore wind farm: on schedule? Claim Check 029",
    pdf_subject="Tests the Energy Ministry's statement on Malta's first floating offshore wind concession",
    story=S))
