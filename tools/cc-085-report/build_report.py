"""Claim Check 085 report. Run fetch.py (optional), calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []
LGREEN = colors.HexColor("#8DB36B")

# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("Tony Zahra, president of the Malta Hotels and Restaurants Association (MHRA), wrote in <i>Horeca Malta</i> (23 December "
        "2022) that the association’s Deloitte study “concluded that Malta will need to attract 4.7 million tourists each spending an "
        "average of 7 nights in Malta” to “reach 80 percent occupancy throughout the year” [1], and said much the same in November "
        "2024 [2]. We read the study, recomputed its tables and compared them with Eurostat’s hotel data.", lead)]
S.append(key_points([(a, b.replace("◆", DIAM)) for a, b in [
    ("The 4.7 million is in the study.",
     "Its airport table (p. 66) gives 4,680,509 tourists a year, at 7 nights each, if guest nights rise 70% on 2019. The same table "
     "gives 4.41 and 4.96 million for rises of 60% and 80%; its bed-stock table and launch slides give 4.1 to 4.5 million [3, 4]. "
     "We reproduce every one of these figures."),
    ("The 80% is not the study’s condition.",
     "The scenarios keep 2019 occupancy: 76.7% in hotels and other collective beds, 59.3% in private rented beds [3]. Eurostat puts "
     "2019 hotel room occupancy at 75.4% (bed-places 66.2%), and no year since 2012 reached 80% [6]. Only 4-star hotels in the MHRA’s "
     "own survey were at 80% or more (81.2%) [5]."),
    ("At 80% the answer barely moves.",
     "Applying 80% to the study’s own beds gives 4.6 to 5.0 million tourists (4.79 million in the middle case). The MHRA’s 2024 "
     "update, using the Malta Tourism Authority’s list of 27,672 approved beds, gives 4.4 to 4.8 million at 2023 occupancy [5]."),
    ("The planned stock is an estimate, and only partly built.",
     "The 2022 scenarios added 80% to 100% to collective beds within about five years, a figure agreed with stakeholders [3]. "
     "Eurostat counts 20.9% more hotel bed-places in 2025 than in 2019, and occupancy back above 2019 levels, with about "
     "4.0 million tourists ◆ [6, 9]."),
]]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("4.68m", GREEN, "tourists a year in the study’s middle scenario (p. 66), at 2019 occupancy and 7-night stays"),
             ("75.4%", ORANGE, "hotel room occupancy in 2019 (Eurostat), not 80%; bed-places 66.2%"),
             ("4.6–5.0m", GREEN, "the study’s own planned beds filled to 80% (our calculation)"),
             ("+20.9%", GREY, "hotel bed-places, 2019 to 2025 (Eurostat); the study assumed +80% to +100%")]),
      Spacer(1, 4 * mm),
      up_down("A statement of the study’s own condition (2019 occupancy) and range (4.1 to 5.0 million), or Planning Authority "
              "figures confirming the size of the pipeline the study assumed, would move it to Supported.",
              "Evidence that the approved pipeline is far smaller than the study assumed, or that the 80% was meant as a forecast of "
              "occupancy rather than a condition, would move it down."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "How the number is built"),
          ("4", "What the studies found"), ("5", "What has happened since 2022"), ("6", "Where the evidence points different ways"),
          ("7", "Testing the claim"), ("8", "Verdict and requests for evidence"), ("9", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The claim record summarised news reports of the study’s launch on 22 September 2022: “if all planned hotels are built, Malta "
           "would need about 4.7 million tourists a year to keep occupancy at 80%”. Those reports (<i>Newsbook</i>, <i>The Malta Business "
           "Weekly</i>, <i>Business Now</i>) give the figure in their own words, with no MHRA words in quotation marks [10–12]. We rate the "
           "MHRA’s own words: its president’s signed column of December 2022 and his interview of November 2024. Words in quotation marks "
           "below are as printed; the column prints “oi” where “to” is meant."))
S.append(std_table([
    [C("Source", cellh), C("What it says", cellh), C("Our access", cellh), C("Status", cellh)],
    [C("<b>Tony Zahra</b>, President, MHRA; <i>Horeca Malta</i>, 23 Dec 2022 [1]"),
     C("The report started from the beds operating and new beds “approved or are in the course of being approved”; it “concluded that "
       "Malta will need to attract 4.7 million tourists each spending an average of 7 nights in Malta” to “reach 80 percent occupancy "
       "throughout the year”."),
     C("Read in full (signed column)."), C("<b>The claim</b>")],
    [C("<b>Tony Zahra</b>, interview, <i>Malta Independent on Sunday</i>, reprinted 28 Nov 2024 [2]"),
     C("“If we want the 80% occupancy rate of hotels we had in 2019, with the number of beds we have, we need 4.7 million tourists.”"),
     C("Reprint read in full; the original page refused us (403)."), C("<b>The claim</b>, restated")],
    [C("<b>Deloitte for the MHRA</b>, Carrying Capacity Study, report of 4 Jul 2022 [3] and launch slides, Sep 2022 [4]"),
     C("Arrivals needed to keep 2019 occupancy if the expected beds are built: 4.1, 4.3 and 4.5 million (bed-stock table, slides); "
       "4.41, 4.68 and 4.96 million (airport table, p. 66)."),
     C("Both read in full (from mhra.org.mt and the outlet’s link)."), C("<b>The study cited</b>")],
    [C("<b>Deloitte for the MHRA</b>, Market update, 24 Sep 2024 [5]"),
     C("Pipeline of 13,543 rooms (27,672 beds) approved by the Malta Tourism Authority; 4.4 to 4.8 million arrivals needed at 2023 "
       "occupancy; hotel survey occupancy for 2019."), C("Read (pp. 4, 9–10, 17, 27, 69, 72–74)."), C("Follow-up study")],
    [C("<b>Eurostat</b>, tourism accommodation data [6]"),
     C("Hotel bed-places, room and bed-place occupancy, arrivals and nights at establishments, 2010–2025."),
     C("Downloaded 10 Oct 2026 (data/cc-085/)."), C("<b>Primary data</b>")],
    [C("<b>NSO</b> inbound tourism, via the studies and outlets [9]"),
     C(f"Tourists and nights, 2019, 2023, 2024 and 2025 {DIAM}."), C("nso.gov.mt refused us (403)."),
     C(f"Second-hand {DIAM}")],
], [40 * mm, 72 * mm, 32 * mm, 26 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("A NOTE ON FAIRNESS", tag),
               P("The MHRA represents hotels and restaurants, and its study argues that Malta has too many hotel beds in the pipeline. A "
                 "warning about oversupply is a legitimate concern, and others have raised it too, ADPD among them [8]. We check the figure the MHRA gives "
                 "and the conditions attached to it, not the case for or against more hotels, and nothing here is about motive.", small)],
              bg=PALE, bar=GREEN), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Questions.</b> (A) Is 4.7 million what the study found? (B) Does the study assume stays of 7 nights? (C) Is 80% "
           "occupancy the study’s condition, and did hotels have 80% occupancy in 2019? (D) Is the planned bed stock documented? "
           "(E) What do the study’s own beds need at 80%, and what has happened since 2022?"))
S.append(P("<b>Evidence.</b> We read the 2022 report, its launch slides and the 2024 update, transcribed every table used "
           "(<i>data/cc-085/mhra_studies.csv</i>, with page numbers) and recomputed them (<i>tools/cc-085-report/calc.py</i>; results in "
           "<i>data/cc-085/checks.csv</i>). We downloaded Eurostat’s data on hotel capacity, occupancy, arrivals and nights for Malta "
           "(<i>fetch.py</i>). We searched Crossref and OpenAlex for peer-reviewed work on tourism carrying capacity and hotel supply, "
           "and verified each DOI in Crossref. Every source we tried is listed in <i>literature/CC-085/README.md</i>."))
S.append(P("<b>Grades.</b> The MHRA’s studies are consultancy analyses commissioned by the speaker (grade C, not independent). "
           "Eurostat data are official statistics (C). The papers are graded in Section 4. Outlet reports are used to locate statements and, "
           f"marked {DIAM}, for NSO figures we could not read. <b>Verdicts</b> follow the five-point scale in Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(100 * mm))
S.append(SectionHeading(3, "How the number is built"))
S.append(P("The arithmetic is simple. The tourists needed in a year are the beds, times 365 nights, times the share of bed-nights "
           "filled (occupancy), divided by the nights each tourist stays, plus tourists who stay in homes nobody rents out. More beds, "
           "higher occupancy or shorter stays all raise the number. The 2022 study does this twice [3]:"))
for t in ["<b>Bed-stock table (p. 27).</b> Collective beds (hotels, guesthouses and the like) rise from 38,000 by 80%, 90% or 100%, "
          "and private rented beds from 23,502 by 25%, 30% or 35%, at the 2019 occupancy of 76.7% and 59.3%. Divided by the 2019 stay "
          "(labelled 7 nights; the arithmetic uses 7.024), this needs 3.63, 3.82 or 4.01 million tourists in rented beds. With the 2019 "
          "count of 513,921 tourists in non-rented homes added, these are the launch slides’ 4.1, 4.3 and 4.5 million [4].",
          "<b>Airport table (p. 66).</b> To size the flights needed, 2019’s 19,338,860 guest nights are grown by 60%, 70% or 80%, the "
          "growth the bed scenarios imply. At 7 nights that is 4,405,184, <b>4,680,509</b> or 4,955,833 tourists: 2019’s 2,753,240 "
          "arrivals times 1.6, 1.7 or 1.8. The middle case is the 4.7 million."]:
    S.append(P("• " + t, bul))
S.append(P("The two tables differ because the airport table grows all guest nights, including those in non-rented homes, while the "
           "bed-stock table grows only rented beds. Neither uses 80% occupancy. Figure 1 sets out every estimate the MHRA’s two studies "
           "give, with the same beds filled to 80%."))
S.append(KeepTogether([fig(FIG / "fig1_estimates.png", width=CW * 0.98), P(f"Figure 1. Tourist arrivals a year needed to fill existing and planned beds, as estimated in the MHRA’s studies [3–5] and "
           f"with the study’s beds at 80% occupancy (our calculation). Orange point: the 4.7 million. Dotted lines: arrivals in 2019 "
           f"(2,753,240, the study’s base year) and 2025 (4,022,310 {DIAM}, NSO via an outlet [9]). Sources: <i>data/cc-085/checks.csv</i>.",
           cap)]))

# ================================================================== 4
S.append(CondPageBreak(70 * mm))
S.append(SectionHeading(4, "What the studies found"))
S.append(P("No peer-reviewed study of Malta’s hotel pipeline, or of the tourists needed to fill it, turned up in our searches. "
           "The research on tourism carrying capacity bears on how to read the 4.7 million, and one panel study bears on the "
           "mechanism the MHRA worries about: added hotel supply lowering occupancy."))
S.append(std_table([
    [C("Study", cellh), C("Design", cellh), C("Finding (from the abstract)", cellh), C("Grade", cellh)],
    [C("McCool &amp; Lime (2001) [13]"), C("Conceptual review"),
     C("A single number of visitors a place can take rests on assumptions rarely met; the useful question is what conditions are "
       "acceptable, not how many is too many."), grade_tag("C")],
    [C("Saveriades (2000) [14]"), C("Case study, Cyprus east-coast resorts"),
     C("Island resorts have thresholds of social carrying capacity beyond which residents’ acceptance and visitors’ satisfaction fall."),
     grade_tag("C")],
    [C("Dogru et al. (2020) [15]"), C("Panel of US hotel markets"),
     C("More hotel supply lowers hotel occupancy and revenue per room; more Airbnb supply lowers prices but not occupancy."),
     grade_tag("B")],
    [C("Hung &amp; Tsou (2025) [16]"), C("Review and expert survey, Taiwanese island"),
     C("Static capacity numbers are limited for small islands; proposes indicators of environmental, economic, social and governance "
       "pressure."), grade_tag("C")],
    [C("Deloitte for the MHRA (2022, 2024) [3, 5]"), C("Consultancy analysis, stakeholder workshops"),
     C("Beds in the pipeline need far more tourists than 2019’s; already at 2019 volumes beaches, heritage sites and the sewage network "
       "were under strain."), grade_tag("C")],
], [38 * mm, 34 * mm, 86 * mm, 12 * mm]))
S.append(Spacer(1, 3 * mm))
S.append(P("Read together, they make a distinction the claim depends on. The 4.7 million is a <i>requirement</i>: the tourists the "
           "planned beds would need at a given occupancy. It is not a <i>capacity</i>: how many tourists Malta can take, which the "
           "literature treats as a question of acceptable conditions rather than a single number [13, 16]. The MHRA’s study draws the "
           "same line: it presents the figure as a level it does not think achievable or desirable [3]. The US evidence that new hotel "
           "supply lowers occupancy [15] supports the study’s worry, though Malta’s market was not studied."))

# ================================================================== 5
S.append(CondPageBreak(100 * mm))
S.append(SectionHeading(5, "What has happened since 2022"))
S.append(P("Eurostat’s data, compiled from the NSO’s survey of accommodation establishments, show hotel bed-places rising from 46,350 "
           "in 2019 to 56,034 in 2025 (+20.9%), with 10.7% of that in 2025 alone; hotels and similar establishments went from 224 to 360 "
           "[6]. That is well short of the 2022 scenarios, which assumed collective beds up 80% to 100% within about five years, but "
           "the MTA’s list of approved projects (27,672 beds at the end of April 2024, 62.9% of the 2023 stock) shows more is planned "
           f"[5]. A parliamentary answer reported 21 new hotels with 2,256 beds approved in 2022–23 {DIAM} [7]. The study’s "
           "counts and Eurostat’s are not on the same basis (38,000 licensed collective beds in 2019 against 46,350 hotel bed-places), "
           "so we compare growth rates, not levels."))
S.append(P(f"Occupancy recovered with the beds. Hotel room occupancy was 75.4% in 2019 and 75.8% in 2025; bed-place occupancy 66.2% and "
           f"67.3% [6]. Tourist arrivals rose from 2,753,240 in 2019 to 4,022,310 in 2025 {DIAM} (+46.1%), 85.6% of 4.7 million, "
           f"while nights at establishments rose 25.8% [6, 9]. Arrivals grew faster than nights because stays shortened: nights per "
           f"arrival at establishments fell from 4.90 to 4.41 (−10.0%) [6], and the NSO’s average stay from 7.02 to 6.31 nights {DIAM} "
           f"[9]. Shorter stays raise the tourists needed for the same beds: had stays in the study’s middle scenario been 10.0% shorter, "
           f"it would have needed 5.2 million rather than 4.7 million (<i>calc.py</i>)."))
S.append(KeepTogether([fig(FIG / "fig2_hotels.png", width=CW * 0.98), P("Figure 2. Hotel bed-places (left) and net occupancy of hotel rooms and bed-places (right) in Malta. Dashed line: the "
           "claim’s 80%. Source: Eurostat tour_cap_nat and tour_occ_anor, retrieved 10 Oct 2026 [6]; <i>data/cc-085/eurostat_tourism.csv</i>.",
           cap)]))

# ================================================================== 6
S.append(CondPageBreak(80 * mm))
S.append(SectionHeading(6, "Where the evidence points different ways"))
S.append(contested("Did the study “conclude” 4.7 million?", "ONE OF SEVERAL", AMBER,
                   "The airport table (p. 66) prints 4,680,509 for the middle scenario, at 7 nights a stay [3]. The three launch-day reports we "
                   "read gave 4.7 million [10–12], and the MHRA president repeated it in 2022 and 2024 [1, 2].",
                   "The bed-stock table and the launch slides give 4.1, 4.3 and 4.5 million [3, 4], and the MHRA’s 2024 update "
                   "describes the original estimate as 4.5 million [5]. The report states no single conclusion of 4.7 million.",
                   "The two tables answer slightly different questions (Section 3). 4.7 million is a fair reading of one scenario; "
                   "“the Deloitte report concluded” makes it sound like the study’s only answer. The range is 4.1 to 5.0 million.",
                   label_a="FOR 4.7 MILLION", label_b="AGAINST"))
S.append(contested("Did hotels have 80% occupancy in 2019?", "FOR 4-STAR HOTELS ONLY", AMBER,
                   "The MHRA and Deloitte’s survey of hotels put 2019 occupancy at 81.2% for 4-star hotels [5]. The MHRA president’s "
                   "2024 wording, “the 80% occupancy rate of hotels we had in 2019” [2], matches that group.",
                   "The same survey gives 72.7% for 5-star hotels [5]. Eurostat puts all hotels at 75.4% of rooms and 66.2% of "
                   "bed-places in 2019, with no year at 80% since 2012 [6]. The study itself assumed 76.7% for collective beds and "
                   "59.3% for private rented beds [3].",
                   "Rooms fill more often than beds, and the survey covers participating hotels while Eurostat covers all. 80% is a fair "
                   "round number for 4-star rooms and high for hotels as a whole. For the claim it matters little: at 80% the study’s "
                   "beds need 4.6 to 5.0 million tourists.", label_a="FOR 80%", label_b="AGAINST"))

# ================================================================== 7
S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(7, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> “the Deloitte report concluded that Malta will need to attract 4.7 million tourists”"), C("MHRA president, 2022 [1]"),
     C("4,680,509 in the airport table’s middle scenario (p. 66), reproduced exactly; the report’s tables range from 4.1 to 5.0 million and "
       "its slides headline 4.5 million [3, 4].", cell), verd("IN THE STUDY", GREENC)],
    [C("<b>B.</b> “each spending an average of 7 nights”"), C("MHRA president, 2022 [1]"),
     C("The study’s stay: 7 nights as labelled, 7.024 in its arithmetic (2019 nights over arrivals) [3]. Stays have shortened since (Section 5).",
       cell), verd("AS IN THE STUDY", GREENC)],
    [C("<b>C.</b> to “reach 80 percent occupancy throughout the year”"), C("MHRA president, 2022 [1]"),
     C("The study keeps 2019 occupancy (76.7% collective, 59.3% private rented); no 80% occupancy condition in its text [3, 4]. At 80% its "
       "beds need 4.6 to 5.0 million.", cell), verd("NOT THE STUDY’S CONDITION", AMBER)],
    [C("<b>D.</b> Beds operating plus new beds “approved or are in the course of being approved”"), C("MHRA president, 2022 [1]"),
     C("The study’s pipeline: about 35,000 collective beds in open permits and a stakeholder consensus of +80% to +100%; the Planning "
       "Authority’s own count was not shared with it [3]. MTA list in 2024: 27,672 beds [5].", cell), verd("ESTIMATE", AMBER)],
    [C("<b>E.</b> “the 80% occupancy rate of hotels we had in 2019”"), C("MHRA president, 2024 [2]"),
     C("4-star hotels 81.2%, 5-star 72.7% in the MHRA survey [5]; all hotels 75.4% of rooms and 66.2% of bed-places (Eurostat) [6].",
       cell), verd("PARTLY SUPPORTED", AMBER)],
    [C("<b>F.</b> “with the number of beds we have, we need 4.7 million tourists”"), C("MHRA president, 2024 [2]"),
     C("With the planned beds, as the interview’s context suggests, the 2024 update gives 4.4 to 4.8 million [5]. With the beds operating "
       "alone it is not shown: hotel rooms were 75.8% full in 2025 [6] with about 4.0 million tourists "
       '<font name="DejaVu" size="6.5">◆</font> [9].', cell),
     verd("DEPENDS ON READING", AMBER)],
], [42 * mm, 22 * mm, 72 * mm, 34 * mm], valign="MIDDLE"))

# ================================================================== 8
S += [Spacer(1, 6 * mm), SectionHeading(8, "Verdict and requests for evidence"),
      verdict_box("Largely supported", "The 4.7 million is one of the study’s scenarios and its arithmetic holds; the 80% occupancy is "
                  "not the study’s condition, and the planned stock is an estimate. Confidence: moderate."),
      Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> The substance of the statement is that the beds Malta already had, plus those approved or in the planning "
           "system, would need about 4.7 million tourists a year to stay as full as hotels were before the pandemic, far above the 2.75 "
           "million of 2019. The MHRA’s study shows that, and we reproduce its numbers exactly: 4.1 to 5.0 million depending on the "
           "scenario, 4.68 million in the one quoted. Two details are wrong or overstated. The study’s condition is 2019 occupancy "
           "(76.7% for hotels and similar, 59.3% for private rentals), not 80%, a level Eurostat’s hotel data do not reach in any year from 2012 to 2025; and “the report "
           "concluded” presents one scenario as the study’s single answer. Neither changes the substance: at 80% the study’s beds need "
           "4.6 to 5.0 million. <b>Confidence</b> is moderate, not high, because the size of the pipeline rests on stakeholder "
           "estimates and a tourism authority list rather than published planning data, and the arrivals series we compare with is "
           "second-hand. <b>What this verdict does not say.</b> It does not say whether more hotels should be built, whether 4.7 million "
           "tourists is achievable or desirable, or anything about the MHRA’s reasons; it tests a figure and its stated conditions."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "From the MHRA: the source of the “80 percent” occupancy in the 2022 column and the 2024 interview (the 4-star survey rate, or another figure).",
    "From the MHRA: whether “the number of beds we have” (2024) included the beds in the pipeline.",
    "From the Planning Authority: the count of approved but unbuilt hotel beds that the 2022 study (p. 25) says was compiled for the MTA.",
    "From the Malta Tourism Authority: the pipeline list by year of expected opening, updated from April 2024.",
]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag),
               P("Not needed for this verdict (maintainer rule of 5 October 2026). The requests above are open to the MHRA and the "
                 "authorities at any time; nothing has been sent to anyone.", small)], bg=AMBER_PALE, bar=AMBER)]

# ================================================================== 9
S += [Spacer(1, 6 * mm), SectionHeading(9, "Limitations")]
for l in [f"Tourist arrivals and nights for 2019–2025 come from the NSO’s inbound tourism survey, which we could not read (nso.gov.mt "
          f"refused automated access); we use the figures as given in the MHRA’s studies and in outlet reports {DIAM}.",
          "The 2022 study counts 38,000 licensed collective beds in 2019; Eurostat counts 46,350 hotel bed-places. The bases differ, so "
          "we compare growth rates and occupancy, not bed numbers.",
          "Hotel survey occupancy for 2019 and 2023 is read from chart labels in the 2024 update; the survey itself is not public.",
          "We searched the text of the 2022 report and slides for an 80% occupancy condition and inspected the charts on the pages "
          "cited; charts drawn as images on other pages were not all inspected.",
          "We do not know how the launch-day reports arrived at 4.7 million and 80%; we found no MHRA press release of the launch, and "
          "MaltaToday’s report (headlined 5 million) refused us.",
          "The papers were read as abstracts only, and none studies Malta’s accommodation market.",
          "The 4.7 million is a conditional scenario. It can be tested only once the pipeline is built, and occupancy and stays will "
          "have changed by then."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Zahra T. (23 Dec 2022). Will Winter 2022–2023 build further on the Results achieved in Summer of ’22? Horeca Malta.",
     "https://horecamalta.com.mt/2022/12/23/will-winter-2022-2023-build-further-on-the-results-achieved-in-summer-of-22/"),
    ("2", "The Malta Business Weekly (28 Nov 2024). ‘Only divine intervention can solve some bottlenecks created by tourist "
          "over-capacity’ – Tony Zahra (reprint of a Malta Independent on Sunday interview).",
     "https://maltabusinessweekly.com/only-divine-intervention-can-solve-some-bottlenecks-created-by-tourist-over-capacity-tony-zahra/27747/"),
    ("3", "Deloitte for the MHRA (4 Jul 2022). Carrying Capacity Study for Tourism in the Maltese islands. Final report, pp. 25, 27, "
          "37–38, 40, 66.", "https://mhra.org.mt/wp-content/uploads/2022/09/TCC-Final-Report.pdf"),
    ("4", "Deloitte for the MHRA (Sep 2022). Carrying Capacity Study for Tourism in the Maltese islands: executive presentation, slide 11.",
     "https://maltabusinessweekly.com/wp-content/uploads/2022/09/TCC-executive-presentation-final-original.pdf"),
    ("5", "Deloitte for the MHRA (24 Sep 2024). Future proofing the Maltese tourism industry: Market update. Final report, pp. 4, 9–10, "
          "17, 27, 69, 72–74.",
     "https://mhra.org.mt/wp-content/uploads/2024/11/20240924_Future-Proofing-the-Tourism-Industry_Final-report-1.pdf"),
    ("6", "Eurostat. tour_cap_nat, tour_occ_anor, tour_occ_arnat and tour_occ_ninat, Malta. Retrieved 10 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/tour_occ_anor/"),
    ("7", "The Shift News (5 Oct 2023). 21 new hotels approved in two years despite oversupply (reports a parliamentary answer: "
          f"2,256 beds approved in 2022–23) {DIAM}.", "https://theshiftnews.com/2023/10/05/21-new-hotels-approved-in-two-years-despite-oversupply/"),
    ("8", "ADPD, Cacopardo C. (2 Oct 2022). Tourism: reflections on the Deloitte report (also in The Malta Independent on Sunday).",
     "https://adpd.mt/tourism-reflections-on-the-deloitte-report/"),
    ("9", f"The Malta Business Weekly (12 Feb 2026). More than 4 million tourists visit Malta in 2025 – NSO {DIAM}. Also Business Now "
          f"(17 Feb 2025) for 3.56 million in 2024 {DIAM}.",
     "https://maltabusinessweekly.com/more-than-4-million-tourists-visit-malta-in-2025-nso/30156/"),
    ("10", "Cordina J. P. (22 Sep 2022). Malta would need 4.7m tourists a year if planned hotels are built. Newsbook.",
     "https://newsbook.com.mt/en/malta-would-need-4-7m-tourists-a-year-if-planned-hotels-are-built/"),
    ("11", "Galdes M. (22 Sep 2022). 4.7 million tourists needed to cater for expected increase of hotel beds. The Malta Business Weekly.",
     "https://maltabusinessweekly.com/4-7-million-tourists-needed-to-cater-for-expected-increase-of-hotel-beds/20336/"),
    ("12", "Fenech R. (22 Sep 2022). If all hotels in pipeline get built, sector can wave goodbye to profitability – study. Business Now.",
     "https://businessnow.mt/if-all-hotels-in-pipeline-get-built-sector-can-wave-goodbye-to-profitability-study/"),
    ("13", "McCool S. F., Lime D. W. (2001). Tourism carrying capacity: tempting fantasy or useful reality? Journal of Sustainable "
           "Tourism 9(5), 372–388 (abstract read).", "https://doi.org/10.1080/09669580108667409"),
    ("14", "Saveriades A. (2000). Establishing the social tourism carrying capacity for the tourist resorts of the east coast of the "
           "Republic of Cyprus. Tourism Management 21(2), 147–156 (abstract read).", "https://doi.org/10.1016/S0261-5177(99)00044-8"),
    ("15", "Dogru T., Mody M., Line N., Suess C., Hanks L., Bonn M. (2020). Investigating the whole picture: comparing the effects of "
           "Airbnb supply and hotel supply on hotel performance across the United States. Tourism Management 79, 104094 (abstract read).",
     "https://doi.org/10.1016/j.tourman.2020.104094"),
    ("16", "Hung Y.-T., Tsou C. (2025). From carrying capacity to destination resilience: an indicator framework for island tourism. "
           "Tourism Geographies 28(2), 141–162 (abstract read).", "https://doi.org/10.1080/14616688.2025.2588628"),
    ("17", "Miżien. Calculation script and outputs: tools/cc-085-report/calc.py; data/cc-085/checks.csv, mhra_studies.csv, "
           "eurostat_tourism.csv, inbound_tourists_secondhand.csv.", ""),
])
S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance, consultancy analysis or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "10 Oct 2026", "First issue. Verdict Largely supported (moderate confidence); no right of reply needed.")])

build_report(Report(
    number="085", out=str(FIG / "report.pdf"), kicker="Tourism and population",
    title_lines=["4.7 million", "tourists to fill", "the hotels?"],
    subtitle_lines=["Testing the MHRA’s figure for the tourists Malta’s", "existing and planned hotel beds would need"],
    quote_lines=["“Malta will need to attract 4.7 million tourists each", "spending an average of 7 nights in Malta [to] reach",
                 "80 percent occupancy throughout the year.”"],
    quote_size=13,
    attribution="Tony Zahra, President of the MHRA, Horeca Malta, 23 December 2022, on the MHRA’s Deloitte study.",
    context="Counting beds operating and new beds approved or being approved. Repeated in an interview, November 2024.",
    verdict="Largely supported", verdict_note="The figure is in the study; its 80% condition is not",
    footer_lines=["Version 1.0  ·  10 October 2026", "Status:",
                  "Prepared from public sources and Eurostat data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="4.7 million tourists – MHRA carrying capacity study", version="1.0", date="10 October 2026",
    pdf_title="4.7 million tourists to fill the hotels? Claim Check 085",
    pdf_subject="Tests the MHRA's statement that Malta would need 4.7 million tourists a year to fill existing and planned hotel beds",
    story=S))
