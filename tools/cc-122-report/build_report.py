"""Claim Check 122 report. Run fetch_eurostat.py, calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []

# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("On 29 August 2026 The Shift reported: <b>“The Shift is informed that Planning Authority applications validated "
        "by 15 June 2026 include proposals for approximately 30,000 additional hotel beds.”</b> It added that filling "
        "them all year at five to six nights a stay “would require between 1.8 million and 2.2 million additional "
        "tourist arrivals annually”, and that at 70% occupancy they would yield about 7.7 million extra guest nights "
        "[1][2]. We reproduced the arithmetic from The Shift’s own inputs and set it against Eurostat. We could not "
        "test the 30,000: no source, list or method is given, and the article says the Malta Tourism Authority declined "
        "to give figures and the Planning Authority did not reply.", lead)]
S.append(key_points([
    ("The sums are right, given the inputs.",
     "30,000 beds × 365 nights × 70% = 7.67 million nights; 30,000 × 365 ÷ 6 or ÷ 5 nights = 1.83 or 2.19 million "
     "arrivals. The two results rest on different occupancy: 1.8 to 2.2 million is 100% occupancy, 7.7 million is 70%."),
    ("The 30,000 beds cannot be tested.",
     "It comes from an unnamed source (“The Shift is informed”). We found no published count of beds in applications "
     "validated before 15 June; the Planning Authority’s register was not readable to us."),
    ("It is large against what exists.",
     "Eurostat counts 58,099 bed-places in Malta’s tourist accommodation in 2025: 30,000 would be 52% more. Other "
     "pipeline measures are of the same order (about 27,700 beds in the MTA’s list in April 2024) or far smaller "
     "(6,239 beds in pending compliance certificates to October 2025, second-hand ◆): they measure different things."),
    ("A stay of five to six nights is above recent data.",
     "Non-residents stayed 4.6 nights per arrival at establishments in 2025 (Eurostat); at that stay the same beds "
     "would need 2.4 million arrivals if full all year."),
    ("Verdict: not substantiated (moderate confidence).",
     "The conversions are sound, but the central figure has not been shown, and applications are not permits or built beds."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(2), Spacer(1, 3 * mm),
      tiles([("30,000", ORANGE, "Beds in applications, per The Shift: no source, list or method published"),
             ("7.67m", GREENC, "Guest nights at 70% occupancy: reproduces (The Shift: about 7.7 million)"),
             ("1.8–2.2m", GREENC, "Extra arrivals at 100% occupancy, 5–6 nights: reproduces"),
             ("+52%", ORANGE, "30,000 beds against Eurostat’s 58,099 bed-places in 2025")]),
      Spacer(1, 4 * mm),
      up_down("The Planning Authority’s count of hotel applications validated by 15 June 2026 (number, category, "
              "location and beds, as The Shift asked), showing about 30,000 beds of hotels and extensions.",
              "A count showing far fewer beds (for example, the 6,239 beds in pending compliance certificates), or "
              "showing that most of the 30,000 are withdrawn, refused or duplicate applications."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the data show"),
          ("4", "Where the evidence points different ways"), ("5", "Testing the claim"),
          ("6", "Verdict and requests for evidence"), ("7", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The claim is The Shift News’s own reporting. The first article (Ivan Camilleri, 29 August 2026) [1] gives the "
           "30,000 figure and the conversions; the second (8 September 2026, on an appeal against the Excelsior "
           "extension in Floriana) [2] repeats them in nearly the same words. We read both in full. The speaker is the "
           "outlet, so we rate its words, not those of the Planning Authority or the Malta Tourism Authority."))
S.append(std_table([
    [C("What was said (The Shift, 29 Aug 2026 [1])", cellh), C("Basis given", cellh), C("Access", cellh)],
    [C("“Planning Authority applications validated by 15 June 2026 include proposals for approximately 30,000 "
       "additional hotel beds. The figure covers both new hotels and extensions … but excludes short-let apartments.”"),
     C("“The Shift is informed”; no document named"), C("Article read; source not seen")],
    [C("“Based on an average stay of between five and six nights, filling all 30,000 new beds throughout the year would "
       "require between 1.8 million and 2.2 million additional tourist arrivals annually.”"),
     C("Calculation; inputs stated"), C("Reproduced")],
    [C("“At 70% occupancy, the proposed capacity would generate approximately 7.7 million additional tourist nights "
       "annually.”"), C("Calculation; input stated"), C("Reproduced")],
    [C("The MTA’s chief executive “declined to provide the figures”; the Planning Authority’s chief executive “did "
       "not reply despite repeated reminders” (the outlet’s account)."), C("The Shift"),
     C("Not checked with either body")],
], [98 * mm, 40 * mm, 32 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("SCOPE NOTE", tag),
               P("The claim is about applications validated before the new Tourism Accommodation Regulations took effect "
                 "on 15 June 2026. An application is not a permit and a permit is not a built bed; the article does not "
                 "say otherwise. We do not assess the regulations, the applicants or any individual project.", small)],
              bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Question.</b> Is the figure of about 30,000 additional hotel beds in applications supported by a source we "
           "can check, and do the stated conversions to guest nights and arrivals follow from the inputs?"))
S.append(P("<b>Evidence.</b> The two articles [1][2]; Eurostat bed-places, arrivals and nights in Malta’s tourist "
           "accommodation [3]; two Deloitte studies for the Malta Hotels and Restaurants Association, read in full for "
           "the earlier check CC-085, for other measures of the pipeline [4][5]. The Planning Authority’s application "
           "register and the Malta Tourism Authority’s lists are not readable from our network, so we could not count "
           "applications ourselves. Every calculation is in <i>tools/cc-122-report/calc.py</i>, from files in "
           "<i>data/cc-122/</i>; the search log for published counts is in <i>literature/CC-122/notes.md</i>."))
S.append(P("<b>Grades.</b> Official statistics are grade C; the article’s unnamed-source figure is grade D. "
           "<b>Verdicts</b> follow the five-point scale in Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(150 * mm))
S.append(SectionHeading(3, "What the data show"))
S.append(fig(FIG / "fig1_beds.png"))
S.append(P("Figure 1. Bed-places in Malta’s tourist accommodation, 2015–2025 (Eurostat), and the 30,000 beds in the "
           "claim. The stock grew 35% in 2015–2025, including 5,303 bed-places in 2025 alone. Eurostat’s count covers "
           "all collective accommodation (hotels, guesthouses and similar), a wider group than the “hotel beds” in the "
           "claim, so the +52% is an order of magnitude, not a like-for-like ratio.", cap))
S.append(fig(FIG / "fig2_arrivals.png"))
S.append(P("Figure 2. Additional arrivals needed a year to use 30,000 beds, under The Shift’s stay of five to six nights "
           "and under the 4.6 nights per arrival Eurostat records for non-residents in 2025. The dashed line is the "
           "number of non-resident arrivals at establishments in 2025. The article’s 1.8 to 2.2 million is the green "
           "bars at five and six nights; at its own 70% the figure would be 1.28 to 1.53 million.", cap))
S.append(std_table([
    [C("Check", cellh), C("Value", cellh), C("Source", cellh), C("Grade", cellh)],
    [C("30,000 beds × 365 nights × 70%"), C("<b>7.67 million</b> nights"), C("Calculated"), grade_tag("C")],
    [C("30,000 × 365 ÷ 6 nights; ÷ 5 nights (every bed full)"), C("<b>1.83 – 2.19 million</b> arrivals"),
     C("Calculated"), grade_tag("C")],
    [C("The same at 70% occupancy"), C("1.28 – 1.53 million arrivals"), C("Calculated"), grade_tag("C")],
    [C("Nights per arrival, non-residents at establishments, 2025"), C("4.6 (11.76 m nights / 2.56 m arrivals)"),
     C("Eurostat tour_occ_ninat, tour_occ_arnat"), grade_tag("C")],
    [C("Bed-places, 2025 (2019)"), C("58,099 (48,096)"), C("Eurostat tour_cap_nat"), grade_tag("C")],
    [C("MTA pipeline at end April 2024"), C("27,672 beds, 13,543 rooms"), C("Deloitte for MHRA 2024, p. 69 [4]"),
     grade_tag("C")],
    [C("Open permits implying more collective beds (2022)"), C("about 35,000 beds"), C("Deloitte for MHRA 2022, p. 25 [5]"),
     grade_tag("C")],
    [C("Pending compliance certificates to Oct 2025: 44 hotel projects"), C("2,998 rooms, 6,239 beds ◆"),
     C("Business Now via search summary; not opened"), grade_tag("D")],
], [64 * mm, 44 * mm, 50 * mm, 12 * mm]))
S.append(P("All values in <i>data/cc-122/checks.csv</i>. ◆ marks a source known only second-hand: it is not used for any "
           "rating. Eurostat data retrieved 14 Oct 2026; status flags were empty for every value used.", cap))

# ================================================================== 4
S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(4, "Where the evidence points different ways"))
S.append(contested(
    "Q1  Is there about 30,000 beds’ worth of applications?", "NOT SHOWN", GREY,
    "The scale is not out of line with other pipeline measures: the MTA’s own list stood at 27,672 beds in April 2024 [4] "
    "and open permits implied about 35,000 collective beds in 2022 [5]. Bed-places grew by 5,303 in 2025 alone [3], so "
    "a large pipeline is real.",
    "Those figures count different things, at other dates (permits and an MTA list, not applications validated before "
    "15 June 2026). The one smaller recent count we found, 6,239 beds in 44 pending compliance certificates to October "
    "2025, is second-hand and also measures another thing. The Shift names no document and the two bodies it asked did "
    "not give a number.",
    "<b>For this claim:</b> plausible in order of magnitude, but neither confirmed nor refuted. Only the Planning "
    "Authority’s validated-application register can settle it."))
S.append(contested(
    "Q2  Do the conversions hold?", "YES, WITH ONE MIXED ASSUMPTION", AMBER,
    "The arithmetic reproduces: 7.67 million nights at 70% and 1.83 to 2.19 million arrivals at five to six nights.",
    "The article does not say that 1.8 to 2.2 million assumes every bed full all year, while 7.7 million assumes 70%. "
    "At 70%, arrivals would be 1.28 to 1.53 million. The 5 to 6 nights is above the 4.6 nights Eurostat records for "
    "non-residents at establishments in 2025.",
    "<b>For this claim:</b> the headline “almost two million” is the upper bound under full occupancy; the conversion "
    "is sound but best read as a maximum, not an expected number."))

# ================================================================== 5
S.append(CondPageBreak(90 * mm))
S.append(SectionHeading(5, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> Applications validated by 15 June 2026 include about 30,000 additional hotel beds"),
     C("Unnamed source; no list or method; MTA gave no figure and PA did not reply (the outlet’s account). Same order "
       "as other pipeline measures, which differ in scope and date [4][5]."), verd("NOT SUBSTANTIATED", ORANGE)],
    [C("<b>B.</b> At 70% occupancy, about 7.7 million extra guest nights a year"),
     C("30,000 × 365 × 0.70 = 7.67 million. Follows from A; no more certain than A."), verd("REPRODUCES", GREENC)],
    [C("<b>C.</b> Filling the beds all year at 5–6 nights needs 1.8–2.2 million extra arrivals"),
     C("Reproduces at 100% occupancy (1.83–2.19 million). At 70%, 1.28–1.53 million; at the 4.6-night 2025 stay, "
       "2.38 million (100%)."), verd("REPRODUCES", GREENC)],
    [C("<b>D.</b> Context: 2022 Deloitte study, 4.7 million tourists a year by 2027 at under seven nights"),
     C("The outlet’s paraphrase of a study checked in CC-085, which found 4.7 million is a bed-filling scenario at "
       "2019 occupancy; not rated here."), verd("NOT RATED", GREY)],
], [52 * mm, 88 * mm, 30 * mm], valign="MIDDLE"))

# ================================================================== 6
S += [Spacer(1, 6 * mm), SectionHeading(6, "Verdict and requests for evidence"),
      verdict_box("Not substantiated", "The conversions are correct; the 30,000-bed figure they rest on has not been "
                  "shown. Confidence: moderate."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) The statement’s central number comes from an unnamed source, with no document, list or "
           "method published, and the bodies that hold the data gave none (as the outlet reports). Our scale defines "
           "<i>Not substantiated</i> as stated more strongly than the evidence offered or available allows; it may be "
           "true. (2) The scale of the pipeline is plausible against other measures. (3) The conversions follow "
           "from the stated inputs, with the occupancy caveat in Q2. Confidence is moderate, not high, because the "
           "Planning Authority’s register might confirm the figure at once."))
S.append(P("<b>What this verdict does not say.</b> It does not say the figure is wrong, that the outlet acted in bad "
           "faith, or that Malta’s hotel pipeline is small. It says the figure has not yet been shown to a standard we "
           "can check. The right of reply is pending."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "The Planning Authority’s count of hotel applications validated by 15 June 2026: number, category, location and beds, "
    "split between new hotels and extensions, and their status (pending, approved, refused, withdrawn).",
    "The Malta Tourism Authority’s Tourism Policy Compliance Certificate applications over the same period, with beds.",
    "The source and date of The Shift’s figure, or its method for 30,000.",
]))

# ================================================================== 7
S += [Spacer(1, 6 * mm), SectionHeading(7, "Limitations")]
for l in ["We did not see the document behind the 30,000, and could not open the Planning Authority’s register or the "
          "MTA’s lists (pa.org.mt and gov.mt return 403 to scripts).",
          "We did not contact the Planning Authority or the Malta Tourism Authority; their silence is The Shift’s account.",
          "Eurostat’s bed-places cover all collective accommodation and its arrivals and nights cover non-residents "
          "in establishments only; neither matches “hotel beds” or all tourists. The comparison is an order of magnitude.",
          "The searches for a published count of validated applications were limited (listed in notes.md); we state only that "
          "we did not find one.",
          "A bed is not a guest: sharing, seasonality and the mix of residents and non-residents are not modelled."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Camilleri I. (29 Aug 2026). 30,000 new hotel beds in the pipeline needing two million more tourists. <i>The Shift News</i>.",
     "https://theshiftnews.com/2026/08/29/30000-new-hotel-beds-in-the-pipeline-needing-two-million-more-tourists/"),
    ("2", "Camilleri I. (8 Sep 2026). Excelsior expansion appealed as Malta faces 30,000-bed hotel surge. <i>The Shift News</i>.",
     "https://theshiftnews.com/2026/09/08/excelsior-expansion-appealed-as-malta-faces-30000-bed-hotel-surge/"),
    ("3", "Eurostat. tour_cap_nat, tour_occ_arnat, tour_occ_ninat (Malta, NACE I551–I553; arrivals and nights of "
          "non-residents); retrieved 14 Oct 2026.", "https://ec.europa.eu/eurostat/databrowser/"),
    ("4", "Deloitte for MHRA (24 Sep 2024). Future proofing the Maltese tourism industry: Market update, p. 69.",
     "https://mhra.org.mt/wp-content/uploads/2024/11/20240924_Future-Proofing-the-Tourism-Industry_Final-report-1.pdf"),
    ("5", "Deloitte for MHRA (4 Jul 2022). Carrying Capacity Study for Tourism in the Maltese islands, p. 25.",
     "https://mhra.org.mt/wp-content/uploads/2022/09/TCC-Final-Report.pdf"),
    ("6", "Miżien. Data and calculations: data/cc-122/; tools/cc-122-report/calc.py; notes in literature/CC-122/notes.md.", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "14 Oct 2026", "First issue. Right of reply to The Shift pending.")])

build_report(Report(
    number="122", out=str(FIG / "report.pdf"), kicker="Tourism and population",
    title_lines=["30,000 more", "hotel beds in", "the pipeline?"],
    subtitle_lines=["Testing a news report on hotel applications before the 15 June 2026 rules",
                    "against Eurostat and the studies it cites"],
    quote_lines=["“Applications … include proposals for approximately", "30,000 additional hotel beds.”"], quote_size=16,
    attribution="The Shift News, 29 August 2026 (repeated 8 September 2026).",
    context="“The Shift is informed”; no document named.",
    verdict="Not substantiated", verdict_note="The sums hold; the 30,000 has not been shown",
    footer_lines=["Version 1.0  ·  14 October 2026", "Status: draft · pending right of reply",
                  "Prepared from public sources and Eurostat data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Hotel beds in applications – Malta", version="1.0", date="14 October 2026",
    pdf_title="30,000 more hotel beds in the pipeline? Claim Check 122",
    pdf_subject="Tests The Shift's report of about 30,000 hotel beds in applications validated before 15 June 2026",
    story=S))
