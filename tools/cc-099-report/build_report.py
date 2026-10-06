"""Claim Check 099 report. Run fetch.py, calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []
STATUS = "right of reply on hold until PwC’s report is read"

# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("PwC Malta’s press release on its <i>Summer 2026 Economic Update</i> (Finance Malta, 17 July 2026) says: "
        "<b>“The latest figures show that foreign residents now make up 31% of Malta’s population”</b>, with "
        "<b>“the mix of foreign to local residents potentially reaching around 38% by 2030.”</b>", lead)]
S.append(key_points([(a, b.replace("◆", DIAM)) for a, b in [
    ("The 31% is right.",
     "Our calculation from Eurostat data gives 30.9–31.1% non-Maltese citizens at the end of 2025 (if 2025’s change "
     "was within the 2010–24 range); the NSO reports 31.1% ◆."),
    ("The definition matters.",
     "32.0% of residents were born abroad already on 1 January 2025, and foreign nationals were 39.8% of registered "
     "employment in December 2025 (Jobsplus)."),
    ("The 38% is PwC’s own projection.",
     "We found no Eurostat or NSO projection by citizenship, and PwC’s report, which sets out its model, could not "
     "be read."),
    ("Whether about 38% is reachable turns on naturalisations.",
     "On citizenship, 37.5–38.5% of PwC’s 636,000 needs Maltese citizens to fall by at least 1,610 a year in "
     "2026–30. They rose every year 2010–2024; only a projection without future naturalisations, like the Central "
     "Bank’s ◆, gives such a fall. The release does not say what PwC assumed."),
    ("Verdict: not substantiated (low confidence).",
     "The 31% is right. The 38% has not been shown: PwC states neither its definition nor its naturalisation "
     "assumption, and its report could not be read."),
]]))
S += [Spacer(1, 4 * mm), VerdictMeter(2), Spacer(1, 3 * mm),
      tiles([("31%", GREEN, "Non-Maltese citizens at end-2025: right (our calculation from Eurostat data: "
                            "30.9–31.1%)"),
             ("32.0%", GREY, "Residents born abroad, 1 January 2025 (Eurostat)"),
             ("39.8%", GREY, "Foreign nationals in registered employment, December 2025 (Jobsplus)"),
             ("≥1,610", RED, "Fewer Maltese citizens a year in 2026–30 for 37.5–38.5% of 636,000; the count rose "
                             "every year 2010–2024")]),
      Spacer(1, 4 * mm),
      up_down("PwC’s report, or PwC, showing the definition and the naturalisation assumption behind the 38%, "
              "reproducible from published inputs: the verdict would move to Largely supported.",
              "Evidence that the 38% is counted on a different basis from the 31% (for example country of birth) "
              "without saying so; or a correction to the NSO’s end-2025 figure that moved the 31%."),
      Spacer(1, 5 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What “foreign residents” can mean"),
          ("4", "Testing the 31%"), ("5", "Testing the 38% by 2030"), ("6", "Where the evidence points different ways"),
          ("7", "Testing the claim"), ("8", "Verdict and requests for evidence"), ("9", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The words are PwC Malta’s. Finance Malta posted them on 17 July 2026 as an “Industry Update” from PwC, with "
           "PwC’s own boilerplate [1]. The Malta Business Weekly reprinted the same text on 19 July [2], and the Malta "
           "Chamber (22 July) and Mondaq, under PwC’s name (23 July), carry it too [3]. The release speaks of “our "
           "projections” and quotes PwC Malta’s Territory Senior Partner, so we assess it as PwC’s statement. The two "
           "figures are in different paragraphs (2 and 6) of the same release."))
S.append(std_table([
    [C("What PwC says", cellh), C("Where", cellh), C("Access", cellh)],
    [C("“…Malta’s population reached 588,254 by year-end 2025. This marks an increase of approximately 14,000 "
       "residents (2.4%) from the previous year.”"), C("Para. 1 [1]"), C("Read in full, 6 Oct 2026")],
    [C("“The latest figures show that foreign residents now make up 31% of Malta’s population, with net migration "
       "patterns continuing to drive growth.”"), C("Para. 2 [1]"), C("Read in full; no source or definition given")],
    [C("“Based on PwC’s demographic modelling, Malta’s population is projected to reach a base case of 636,000 by "
       "2030.”"), C("Para. 2 [1]"), C("Read in full")],
    [C("“Our projections are based on varying levels of slowdown in current net migration flows. Nonetheless, "
       "population is still expected to increase significantly, with the mix of foreign to local residents "
       "potentially reaching around 38% by 2030.”"), C("Para. 6 [1] (para. 7 in [2])"),
     C("Read in full; method in the report")],
    [C("The <i>Summer 2026 Economic Update</i> itself, which “sets out demographic projections”"), C("pwc.com [4]"),
     C("Not readable: 403 to scripts; no Internet Archive capture")],
    [C("◆ Quoted by two outlets as the report’s words: “… the results suggest that population would still increase "
       "significantly, with the mix of foreign to local reaching around 38% in the base case.” Range 624,000–660,000."),
     C("Business Now [5], Newsbook [6]"), C("Second-hand")],
], [96 * mm, 38 * mm, 36 * mm]))
S.append(P("<b>The record’s link.</b> Our intake record pointed to a different Malta Business Weekly article (2 June "
           "2025, by Silvan Mifsud, on a Central Bank of Malta policy note) [21]. That article does not contain the "
           "claim: it gives 28.1% of the population as foreign nationals in 2023 and “just over 31%” of the "
           "working-age population. The claim’s wording matches the July 2026 release, which we rate here."))
S += [Spacer(1, 2 * mm),
      callout([P("SCOPE NOTE", tag),
               P("This check tests two statistics and how they were produced. It does not assess migration policy, the "
                 "economic effects of population growth, or the hospital-bed and electricity figures in the same "
                 "release. The words “foreign” and “local” are PwC’s; we use the statistical terms (non-Maltese "
                 "citizens, born abroad) when we test them.", small)],
              bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(CondPageBreak(60 * mm))
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Questions.</b> (1) Were foreign residents 31% of Malta’s population at the time of the release, and on what "
           "definition? (2) Does “around 38% by 2030” come from a published projection, and can it be shown from "
           "published figures?"))
S.append(P("<b>Evidence.</b> We downloaded from Eurostat’s dissemination API on 6 October 2026, with Eurostat’s flags: "
           "the population on 1 January by citizenship and by country of birth [10, 11], the demographic balance "
           "[12], Census 2021 [13], immigration, emigration and acquisitions of citizenship by citizenship [14], births "
           "by the mother’s citizenship and deaths by citizenship [15], and the EUROPOP2025 projections [16]. We "
           "downloaded Jobsplus’s workbooks on foreign nationals in employment and total employment [18, 19]. The NSO’s "
           "release of 9 July 2026 [7] and PwC’s report [4] refused automated access; their figures are used only as "
           "reported by news outlets, marked ◆. The Central Bank of Malta’s policy note was read as its abstract (Crossref) "
           "[20]. Every figure is recomputed by <i>tools/cc-099-report/calc.py</i> from <i>data/cc-099/</i>. A Crossref "
           "search (three queries, logged in <i>literature/CC-099/notes.md</i>) found no peer-reviewed study of "
           "Malta’s foreign-population share or its projection."))
S.append(P("<b>Definitions.</b> Eurostat counts usual residents (a stay of at least 12 months, or intended to last "
           "that long); citizenship is the legal bond with a state, and a non-national is a citizen of another country "
           "or stateless [17]. The population on 1 January of a year is the population at the end of the year before: "
           "Eurostat’s 1 January 2026 total is 588,254, the figure PwC gives for the end of 2025 [1, 12]. We read "
           "“around 38%” as 37.5–38.5%, the values that round to 38, and apply the same tolerance to every reading."))
S.append(P("<b>Grades.</b> Official statistics and administrative data are grade C under our scale. <b>Verdicts</b> "
           "follow the five-point scale in Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(3, "What “foreign residents” can mean"))
S.append(P("The release does not define “foreign residents”. Three published measures fit the phrase, and they differ "
           "by several points (Figure 1, Table 1). Counted by <b>citizenship</b>, a person born in Malta to foreign "
           "parents is foreign, and a foreigner who becomes a Maltese citizen is not. Counted by <b>country of birth</b>, "
           "Maltese citizens born abroad are included. Jobsplus reports <b>foreign nationals in registered "
           "employment</b>, a share of employment, not of residents."))
S.append(KeepTogether([fig(FIG / "fig1_shares.png"), P(
    "Figure 1. Share of Malta’s residents who are non-Maltese citizens and who were born abroad (Eurostat, 1 January), "
    "and foreign nationals’ share of registered employment (Jobsplus, December). Census 2021 (reference date 21 "
    "November 2021 [22]) is shown as diamonds. The green bar at 1 January 2026 is our calculation from Eurostat data "
    "(section 4); the hollow circle is the NSO’s end-2025 figure as reported ◆. PwC’s 31% is plotted at the end of "
    "2025 and its 38% at the end of 2030; PwC published no path between them.", cap)]))
S.append(KeepTogether([
    std_table([
        [C("Measure", cellh), C("Value", cellh), C("Date", cellh), C("Source", cellh), C("Grade", cellh)],
        [C("Non-Maltese citizens (other EU 8.0%, non-EU 21.4%)"), C("<b>29.4%</b> (168,938)"), C("1 Jan 2025"),
         C("Eurostat [10]"), grade_tag("C")],
        [C("Non-Maltese citizens: our calculation from Eurostat data, if 2025’s change was within the 2010–24 range"),
         C("<b>30.9–31.1%</b>"), C("1 Jan 2026"), C("calculated [10, 12]"), grade_tag("C")],
        [C("◆ Non-Maltese citizens, NSO"), C("31.1% (182,693)"), C("end-2025"), C("NSO via news [8, 9]"),
         grade_tag("C")],
        [C("Born abroad"), C("<b>32.0%</b> (183,765)"), C("1 Jan 2025"), C("Eurostat [11]"), grade_tag("C")],
        [C("Census: non-Maltese citizens / born abroad"), C("22.2% / 25.7%"), C("21 Nov 2021"), C("Eurostat [13]"),
         grade_tag("C")],
        [C("Foreign nationals in registered employment (full- and part-time)"), C("39.8% (135,417)"), C("Dec 2025"),
         C("Jobsplus [18, 19]"), grade_tag("C")],
        [C("Foreign nationals in full-time registered employment"), C("42.2%"), C("Dec 2025"), C("Jobsplus [18, 19]"),
         grade_tag("C")],
    ], [62 * mm, 32 * mm, 22 * mm, 38 * mm, 16 * mm]),
    P("Table 1. All values in <i>data/cc-099/checks.csv</i>. Eurostat’s 2010–2025 citizenship and birth series carry no "
      "flags (earlier years carry a break in 2001 and 2009 and an estimate in 2006). Unflagged, the born-abroad series "
      "shifts between 2022 and 2023 (Malta-born 397,432 to 388,690), and its 1 January 2022 share (23.6%) is below "
      "Census 2021 (25.7%); we use only its 2025 level. Employment shares are not comparable with shares of residents.",
      cap)]))

# ================================================================== 4
S.append(CondPageBreak(90 * mm))
S.append(SectionHeading(4, "Testing the 31%"))
S.append(P("The latest year for which Eurostat publishes Malta’s population by citizenship is 1 January 2025: 29.4% "
           "non-Maltese citizens, up from 28.1% a year earlier and 4.6% in 2010 [10]. PwC’s “latest figures” refer to "
           "the end of 2025, a year later. Eurostat already gives that total, 588,254 on 1 January 2026, matching "
           "PwC’s figure and its 14,004 rise (2.44%) in 2025 [12]."))
S.append(P("Eurostat has not yet published the 2026 split, so we bound it ourselves. The number of Maltese citizens "
           "rose in every year from 2010 to 2024, by between 237 (2024) and 1,394 (2011) a year [10]. If 2025’s change "
           "lay within that range, Maltese citizens numbered 405,549–406,706 on 1 January 2026, and non-Maltese "
           "citizens were <b>30.9–31.1%</b> of 588,254 (our calculation). Both ends round to 31%."))
S.append(P("The NSO’s own figure agrees. Its World Population Day release (NR 120/2026, 9 July 2026) is not readable "
           "from our network, but four outlets report it: 68.9% Maltese citizens and 31.1% non-Maltese citizens at the "
           "end of 2025, or 182,693 people [8, 9] ◆. That implies 405,561 Maltese citizens, 249 more than a year "
           "earlier, inside our range. PwC does not name its source; the 31% matches the NSO’s citizenship figure, "
           "rounded (our identification). By country of birth the share would be higher: 32.0% were born abroad a "
           "year earlier [11]."))

# ================================================================== 5
S.append(CondPageBreak(70 * mm))
S.append(SectionHeading(5, "Testing the 38% by 2030"))
S.append(P("Is it an official projection?", h2))
S.append(P("No. Eurostat’s EUROPOP2025 projections (June 2026) give Malta’s population by age and sex only, with no "
           "split by citizenship or country of birth [16]. The Central Bank of Malta wrote in 2025 that it projected "
           "the native Maltese population itself “in the absence of demographic projections specifically covering the "
           "native Maltese population” [20]. The NSO’s website refuses automated access, and a web search found no NSO "
           "projection by citizenship; Newsbook reports that a parliamentary reply confirmed the government holds no "
           "formal population projections for the next four years ◆ [6]. The 38% is PwC’s own model result: the "
           "release attributes it to “our projections”, based on “varying levels of slowdown in current net migration "
           "flows” [1]."))
S.append(P("What “38%” means", h2))
S.append(P("“The mix of foreign to local residents” could be read as a ratio of foreign to local. On 1 January 2025 "
           "there were already 41.7 non-Maltese citizens for every 100 Maltese citizens [10], so a ratio of 38 would be "
           "a fall, which the release does not describe. We read the 38% as a share of all residents, as the 31% is."))
S.append(P("What it requires", h2))
S.append(P("At PwC’s base case of 636,000 residents, “around 38%” (37.5–38.5%) leaves 391,140–397,500 local "
           "residents. On the citizenship basis of the 31%, local residents are Maltese citizens, 405,549–406,706 at "
           "the end of 2025 by our calculation (section 4). Reaching 397,500 by the end of 2030 needs a fall of at "
           "least <b>1,610 a year</b> over 2026–2030; exactly 38% needs 2,246–2,477 a year, and 38.5% up to 3,113. "
           "(Counted from 1 January 2025, the figures would be 1,302–2,362 a year, but that spreads the fall over 2025, "
           "when the count rose.) Figure 2 sets this against what has happened."))
S.append(KeepTogether([fig(FIG / "fig2_locals.png"), P(
    "Figure 2. A: Maltese citizens on 1 January, 2010–2025, our 1 January 2026 range, and the number left for local "
    "residents by 37.5–38.5% of 636,000. B: the parts of each year’s change, 2021–2024: acquisitions of Maltese "
    "citizenship, net migration of Maltese citizens, and the remainder, against the yearly fall needed in 2026–2030 "
    "[10, 14, 15].", cap)]))
S.append(KeepTogether([
    std_table([
        [C("Year", cellh), C("Total change", cellh), C("Net migration of Maltese", cellh),
         C("Acquisitions of citizenship", cellh), C("Remainder", cellh), C("Births to Maltese mothers minus deaths of "
                                                                         "Maltese", cellh)],
        [C("2021"), C("+331"), C("+306"), C("+1,156"), C("−1,131"), C("−900")],
        [C("2022"), C("+881"), C("+1,039"), C("+842"), C("−1,000"), C("−921")],
        [C("2023"), C("+400"), C("+489"), C("+825"), C("−914"), C("−857")],
        [C("2024"), C("+237"), C("+533"), C("+1,145"), C("−1,441"), C("−1,119")],
        [C("<b>Needed a year, 2026–30, for 37.5–38.5% of 636,000</b>"), C("<b>−1,610 to −2,882</b>"),
         C("from 405,549 (−1,841 to −3,113 from 406,706)"), C(""), C(""), C("")],
    ], [36 * mm, 24 * mm, 27 * mm, 27 * mm, 22 * mm, 34 * mm]),
    P("Table 2. Maltese citizens, components of change (persons). Remainder = total change minus net migration and "
      "acquisitions; it also includes losses of citizenship and statistical adjustment. Births are counted by the "
      "mother’s citizenship, which can differ from the child’s (general context), so the last column is approximate. "
      "Eurostat [10, 14, 15]; acquisitions for 2010 carry a break flag (not used).", cap)]))
S.append(P("Even if no foreigner became a Maltese citizen and no Maltese citizen moved in or out, the remainder fell by "
           "914–1,441 a year in 2021–2024, a slower fall than the 1,610 needed. For comparison only, not as forecasts: "
           "if 2024’s remainder (−1,441), the largest, repeated every year from our end-2025 range, the non-Maltese "
           "share at 636,000 would be 37.2–37.4% (37.6% if 2025 is included), at the edge of “around 38%”; had the "
           "count stayed at its 1 January 2025 level, it would be 36.3%. The release gives no local-population path. "
           "In Business Now’s paraphrase of the report, the local population “has remained at just over 400,000” ◆ [5]."))
S.append(P("Other readings come close to 38%. A projection without future naturalisations, like the Central Bank’s ◆, "
           "gives about 38% (section 6). On <b>country of birth</b>, 390,485 residents were born in Malta on 1 January "
           "2025 [11]; at that count, 38.6% of 636,000 would be born abroad, just above the band, and 37.5–38.5% would "
           "need 655–7,015 more Malta-born residents by 2030. At the top of PwC’s reported range, 660,000 ◆ [5, 6], the "
           "1 January 2025 count of Maltese citizens would leave 38.6% non-Maltese. The release states none of these."))
S.append(KeepTogether([P("Context: total population", h2), P(
    "PwC’s base case sits between Eurostat’s projections. EUROPOP2025 gives 621,470 on 1 January 2030 and 628,876 on "
    "1 January 2031 in its baseline, and 650,230 and 663,463 with higher migration [16]. Its baseline for 1 January "
    "2026 (585,012) was already 3,242 below the outcome [12, 16]. We do not rate the 636,000; it is the denominator "
    "PwC chose.")]))

# ================================================================== 6
S.append(CondPageBreak(90 * mm))
S.append(SectionHeading(6, "Where the evidence points different ways"))
S.append(contested(
    "Q1  Could the local population fall fast enough for about 38%?", "ONLY IF NATURALISATIONS ARE LEFT OUT", ORANGE,
    "The Central Bank of Malta projects “a persistent decline and ageing of the native Maltese population” [20]. Its "
    "baseline, as reported ◆, falls from 405,075 (2023) to about 350,000 [21] or 347,000 [23] by 2050: about 2,040–2,230 "
    "a year on average, faster than the 1,610 needed. Its start equals Eurostat’s Maltese citizens on 1 January 2024 "
    "[10], the basis of the 31%, but it leaves out people who acquire citizenship ◆ [23]. Applied to 2026–2030 that "
    "average gives 37.8–38.0% at 636,000. Its path to 2030 is not known to us, so this decides nothing.",
    "The number of Maltese citizens rose in every year 2010–2024 [10]. In 2021–2024, 825–1,156 people a year "
    "became Maltese citizens and net migration of Maltese citizens was positive [14]. Even with both set to zero, the "
    "remainder fell by at most 1,441 a year, short of the 1,610 needed (Table 2). Births to Maltese mothers were "
    "below deaths of Maltese citizens by only 857–1,119 a year [15].",
    "<b>For this claim:</b> the answer turns on naturalisations. With them, as recorded, the count rises; without "
    "them, a CBM-style projection gives about 38%. The release does not say which PwC assumed, and only its report "
    "could show it.",
    label_a="EVIDENCE THAT THE LOCAL POPULATION COULD FALL"))
S.append(contested(
    "Q2  Is the 38% on the same definition as the 31%?", "UNKNOWN", GREY,
    "The release uses one phrase for both (“foreign residents”; “the mix of foreign to local residents”) and gives "
    "no change of definition. The 31% matches the NSO’s citizenship figure (section 4). In Business Now’s paraphrase, "
    "the report puts the local population “at just over 400,000” ◆ [5], which fits Maltese citizens (405,312 on 1 "
    "January 2025) rather than Malta-born residents (390,485) [10, 11].",
    "On country of birth, 38.6% would be born abroad at 636,000 with the 1 January 2025 count of Malta-born residents "
    "[11]. Business Now’s “In 2019, it was 20 per cent” ◆ [5] matches the born-abroad share on 1 January 2019 "
    "(20.2%), not citizenship (18.4%) [10, 11]; and 31% also matches born abroad on 1 January 2024 (30.8%).",
    "<b>For this claim:</b> the clues point both ways and are second-hand. Either the 38% is on the citizenship "
    "basis and needs a fall in Maltese citizens that only a no-naturalisation projection gives, or it is on another "
    "basis and cannot be set beside the 31%. Either way the figure has not been shown.",
    label_a="EVIDENCE OF THE CITIZENSHIP BASIS", label_b="EVIDENCE OF A BIRTHPLACE BASIS"))

# ================================================================== 7
S.append(CondPageBreak(90 * mm))
S.append(SectionHeading(7, "Testing the claim"))
S.append(P("The verdict rests on A and B, the two figures in the claim. C is the release’s own context and is rated "
           "for completeness."))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> “foreign residents now make up 31% of Malta’s population”"),
     C("Our calculation from Eurostat data: 30.9–31.1% non-Maltese citizens on 1 January 2026 (if 2025’s change was "
       "within the 2010–24 range); 29.4% a year earlier [10, 12]. The NSO’s 31.1% agrees ◆ [8]. By country of birth "
       "the share is higher (32.0% in 2025) [11]."),
     verd("ACCURATE", GREENC)],
    [C("<b>B.</b> “the mix of foreign to local residents potentially reaching around 38% by 2030”"),
     C("PwC’s own model; no Eurostat or NSO projection by citizenship found [16, 20]. On citizenship, 37.5–38.5% of "
       "636,000 needs Maltese citizens to fall by at least 1,610 a year in 2026–30; recorded data show a rise every "
       "year 2010–2024 [10, 14]. Only a projection without future naturalisations, like the CBM’s ◆, gives such a fall. "
       "PwC states neither its definition nor this assumption; report not readable [4]."),
     verd("NOT SUBSTANTIATED", ORANGE)],
    [C("<b>C.</b> “…Malta’s population reached 588,254 by year-end 2025 … approximately 14,000 residents (2.4%)” "
       "(context)"),
     C("Eurostat: 588,254 on 1 January 2026; +14,004 (2.44%) in 2025 [12]."), verd("ACCURATE", GREENC)],
], [56 * mm, 84 * mm, 30 * mm], valign="MIDDLE"))

# ================================================================== 8
S += [CondPageBreak(80 * mm), Spacer(1, 4 * mm), SectionHeading(8, "Verdict and requests for evidence"),
      verdict_box("Not substantiated", "The 31% is right. The 38% by 2030 has not been shown: PwC does not state its "
                  "definition of foreign and local residents or its assumption about naturalisations, and its report "
                  "could not be read. Confidence: low."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) The current figure reproduces from our calculation on Eurostat data and agrees with the "
           "NSO’s ◆. (2) The 2030 figure is PwC’s own model result, not an official projection, and the release gives "
           "one sentence on how it was made. (3) On citizenship, “around 38%” of PwC’s 636,000 needs Maltese citizens "
           "to fall by at least 1,610 a year over 2026–2030 (about 2,250 for exactly 38%). Recorded data show them "
           "rising every year 2010–2024, because naturalisations and returning citizens outweigh the natural decrease; "
           "only a projection that leaves out future naturalisations, as the Central Bank’s does ◆, gives a fall of "
           "that size. On country of birth the figure is closer, but the 31% matches citizenship. (4) The release "
           "states neither its definition nor its naturalisation assumption, so the figure cannot be checked from what "
           "PwC published. (5) Confidence is low: the evidence on the 38% points both ways, the deciding document "
           "(PwC’s report) could not be read, and the NSO’s end-2025 figure is second-hand."))
S.append(P("<b>What this verdict does not say.</b> It does not say that the share of foreign residents will not rise, "
           "that PwC’s population total is wrong, or anything about migration policy. It addresses only whether the "
           "two figures are supported by the evidence offered and available."))
S.append(P("<b>Right of reply.</b> A reply from PwC Malta is on hold until its <i>Summer 2026 Economic Update</i> is "
           "read, because the explanation of the 38% may be in it. If the report shows the method, the verdict will be "
           "revisited before any reply is sought."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "The definition of “foreign” and “local” behind the 38%: citizenship, as in the 31%, or country of birth.",
    "The base-case number of local residents for 2030, and whether the model counts future naturalisations, with its "
    "assumptions for births, deaths and migration.",
    "The share of foreign residents at the low (624,000) and high (660,000) ends of PwC’s range (range known "
    "second-hand ◆).",
    "From the NSO: the end-2025 population by citizenship as a published table (Eurostat’s 1 January 2026 split was "
    "not yet available on 6 October 2026).",
]))

# ================================================================== 9
S += [Spacer(1, 5 * mm), SectionHeading(9, "Limitations")]
for l in ["PwC’s report could not be read (pwc.com refuses automated access and the Internet Archive has no copy); it "
          "may explain the 38%.",
          "The NSO’s end-2025 figures are second-hand (nso.gov.mt refuses automated access; an Internet Archive copy "
          "exists but could not be opened from our network). Four outlets agree.",
          "The 30.9–31.1% for 1 January 2026 is our calculation from Eurostat data, valid if 2025’s change in Maltese "
          "citizens lay within the 2010–24 range; Eurostat has not yet published the 2026 split.",
          "The Central Bank of Malta’s note was read as its abstract; its baseline figures are second-hand (◆), and its "
          "path to 2030 is unknown.",
          "Births are recorded by the mother’s citizenship, so the last column of Table 2 is approximate.",
          "Jobsplus’s own label is “Foreign Nationals Employed in Malta & Gozo”; “registered employment” is our "
          "short name for the series. It counts employment, not residents, so it is not comparable with population "
          "shares.",
          "Figures quoted from the report by Business Now and Newsbook are second-hand (◆) and decide no rating."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
EU = "https://ec.europa.eu/eurostat/databrowser/product/page/"
S += references([
    ("1", "Finance Malta (17 Jul 2026). Malta’s rapid population growth creates urgent need to focus on the country’s "
          "infrastructure demands… Industry Update / PwC. Read in full, 6 Oct 2026.",
     "https://financemalta.org/industry-updates/malta-s-rapid-population-growth-creates-urgent-need-to-focus-on-the-country-s-infrastructure-demands-for-the-future"),
    ("2", "The Malta Business Weekly (19 Jul 2026). Same release text. Read in full, 6 Oct 2026.",
     "https://maltabusinessweekly.com/population-growth-drives-urgent-infrastructure-needs-pwc-malta-summer-2026-economic-update/30680/"),
    ("3", "The Malta Chamber (22 Jul 2026); Mondaq (23 Jul 2026, author PwC). Same text. Read 6 Oct 2026.",
     "https://maltachamber.org.mt/maltas-rapid-population-growth-creates-urgent-need-to-focus-on-the-countrys-infrastructure-demands-for-the-future/"),
    ("4", "PwC Malta. Economic update summer edition 2026. Not readable (403; no Internet Archive capture).",
     "https://www.pwc.com/mt/en/publications/economic-outlook/economic-outlook-summer-2026.html"),
    ("5", "◆ Schembri Orland K. (15 Jul 2026). Malta’s population could reach 636,000 by 2030, PwC projects. Business "
          "Now.",
     "https://businessnow.mt/maltas-population-could-reach-636000-by-2030-pwc-projects/"),
    ("6", "◆ Balzan J. (17 Jul 2026). PwC: Malta’s population could climb to 660,000 within five years. Newsbook.",
     "https://newsbook.com.mt/en/pwc-maltas-population-could-climb-to-660000-within-five-years/"),
    ("7", "National Statistics Office (9 Jul 2026). World Population Day: 11 July 2026 (NR 120/2026). Not readable "
          "(403), 6 Oct 2026.", "https://nso.gov.mt/world-population-day-11-july-2026/"),
    ("8", "◆ Newsbook (9 Jul 2026). Malta’s population grows 2.4%, driven entirely by migration. MEETinc and "
          "International Adviser agree.",
     "https://newsbook.com.mt/en/maltas-population-grows-2-4-driven-entirely-by-migration/"),
    ("9", "◆ Lovin Malta (11 Jul 2026). World Population Day: Malta’s population reaches record 588,254 "
          "(NSO: 68.9% / 31.1%).",
     "https://lovinmalta.com/news/local/world-population-day-maltas-population-reaches-record-588254/"),
    ("10", "Eurostat. migr_pop1ctz Population on 1 January by age group, sex and citizenship; updated 25 Sep 2026, "
           "retrieved 6 Oct 2026, with flags. doi:10.2908/migr_pop1ctz.", EU + "MIGR_POP1CTZ"),
    ("11", "Eurostat. migr_pop3ctb Population on 1 January by age group, sex and country of birth; updated 25 Sep 2026, "
           "retrieved 6 Oct 2026. doi:10.2908/migr_pop3ctb.", EU + "MIGR_POP3CTB"),
    ("12", "Eurostat. demo_gind Population change – demographic balance and crude rates; updated 30 Sep 2026, "
           "retrieved 6 Oct 2026. doi:10.2908/demo_gind.", EU + "DEMO_GIND"),
    ("13", "Eurostat. Census 2021: cens_21ctz_r3, cens_21cob_r3; retrieved 6 Oct 2026. doi:10.2908/cens_21ctz_r3.",
     EU + "CENS_21CTZ_R3"),
    ("14", "Eurostat. migr_imm1ctz, migr_emi1ctz, migr_acq (migration and acquisitions by citizenship); retrieved "
           "6 Oct 2026. doi:10.2908/migr_acq.", EU + "MIGR_ACQ"),
    ("15", "Eurostat. demo_faczc, demo_maczc (births by mother’s citizenship; deaths by citizenship); retrieved 6 Oct "
           "2026.", EU + "DEMO_MACZC"),
    ("16", "Eurostat. proj_25np Population on 1st January by age, sex and type of projection (EUROPOP2025); updated "
           "11 Jun 2026, retrieved 6 Oct 2026. doi:10.2908/proj_25np.", EU + "PROJ_25NP"),
    ("17", "Eurostat. International migration statistics, reference metadata (definitions). Read 6 Oct 2026.",
     "https://ec.europa.eu/eurostat/cache/metadata/en/migr_immi_esms.htm"),
    ("18", "Jobsplus. Foreign nationals employment trends; workbook “Trend of employed foreign nationals 2015–2025”. "
           "Retrieved 6 Oct 2026.", "https://jobsplus.gov.mt/labour-market-trends/foreign-nationals-employment-trends"),
    ("19", "Jobsplus. Employment trends: total and full-time employment workbooks, 2015–2025. Retrieved 6 Oct 2026.",
     "https://jobsplus.gov.mt/labour-market-trends/employment-trends"),
    ("20", "Cumbo L. (2025). The native Maltese population: projections and implications on the labour supply. Central "
           "Bank of Malta Policy Note 1/2025. doi:10.2139/ssrn.5356748. Abstract read (Crossref).", "https://doi.org/10.2139/ssrn.5356748"),
    ("21", "Mifsud S. (2 Jun 2025). Malta’s demographic shift: a growing foreign workforce. The Malta Business Weekly. "
           "Intake link; not the claim; ◆ for CBM figures.",
     "https://maltabusinessweekly.com/maltas-demographic-shift-a-growing-foreign-workforce/29055/"),
    ("22", "Eurostat. 2021 censuses, reference metadata: reference dates (Malta, 21 Nov 2021). Read 6 Oct 2026.",
     "https://ec.europa.eu/eurostat/cache/metadata/en/cens_21_esms.htm"),
    ("23", "◆ Amphora Media (6 Nov 2025). FATTI: Is Malta’s native population at risk of collapse…?",
     "https://www.amphora.media/2025/11/fatti-malta-native-population-numbers-budget-tax-cut-child-parent"),
    ("24", "Miżien. Data and calculations: data/cc-099/; tools/cc-099-report/calc.py.", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "6 Oct 2026", "First issue. Right of reply to PwC Malta on hold until its Summer 2026 "
                                         "Economic Update is read.")])

build_report(Report(
    number="099", out=str(FIG / "report.pdf"), kicker="Population statistics",
    title_lines=["31% foreign now,", "38% by 2030?"],
    subtitle_lines=["Testing PwC Malta’s figures for foreign residents", "against Eurostat, NSO and Jobsplus data"],
    quote_lines=["“…foreign residents now make up 31% of Malta’s population”",
                 "“…the mix of foreign to local residents potentially",
                 "reaching around 38% by 2030.”"],
    quote_size=14,
    attribution="PwC Malta, Summer 2026 Economic Update press release, as posted by Finance Malta, 17 July 2026.",
    context="Two fragments, from paragraphs 2 and 6; the 2030 figure comes from PwC’s own model.",
    verdict="Not substantiated", verdict_note="31% right; 38% by 2030 not shown",
    footer_lines=["Version 1.0  ·  6 October 2026", "Status:",
                  "Prepared from public sources and official statistics.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Foreign residents in Malta", version="1.0", date="6 October 2026",
    status_note=STATUS,
    pdf_title="31% foreign now, 38% by 2030? Claim Check 099",
    pdf_subject="Tests PwC Malta's statement that foreign residents make up 31% of Malta's population, potentially "
                "reaching around 38% by 2030",
    story=S))
