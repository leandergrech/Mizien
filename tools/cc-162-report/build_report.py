"""Claim Check 162 report. Run fetch.py, calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []

# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("In its EU Climate Action Progress Report 2026 (adopted 9 November 2026) the European Commission wrote, under a "
        "chart of every Member State’s 2030 outlook: <b>“Malta’s gap to target is 49 and 61 percentage points, exceeding its "
        "19% reduction target. This means Malta is projected to emit more in 2030 than in 2005.”</b> [1] It also named "
        "Malta among nine Member States that it will ask for a corrective action plan. The sentence repeats the 2025 report "
        "(see Claim Check 094), so we tested it again against the 2026 data and asked what changed.", lead)]
S.append(key_points([
    ("The numbers reproduce to the nearest point, again.",
     "Malta’s projections give 1,324 kt (planned measures) and 1,450 kt (existing measures) in 2030: +29.7% and +42.1% "
     "on the legal 2005 level of 1,021 kt, a gap of 48.7 and 61.1 points to the −19% target [3, 4, 6]."),
    ("Nothing in Malta’s projections changed.",
     "The EEA’s 2026 dataset still holds Malta’s March 2025 submission only; Germany and Ireland, among others, "
     "updated in 2026, Malta did not. Malta’s 2027 totals are identical to the 2025 dataset [4]."),
    ("Measured emissions are 37% above 2005, not below.",
     "Approximated 2025 emissions are 1,400 kt, down from 1,430 kt in 2024 but 315 kt over the 2025 limit [2, 5]."),
    ("What did change is the Commission’s conclusion.",
     "In 2025 it named six Member States with excess emissions in 2026–2030 and said it could not conclude they were "
     "not making sufficient progress; in 2026 it names eight (nine with Croatia) and concludes that nine are not [1, 7]."),
    ("Verdict: supported (high confidence).",
     "The Commission’s words match the data and the law. Whether Malta will actually need to buy allocations, and at what cost, is not public."),
]))
S += [Spacer(1, 4 * mm), VerdictMeter(0), Spacer(1, 3 * mm),
      tiles([("+30–42%", RED, "Malta’s effort-sharing emissions in 2030 vs 2005 (planned / existing measures)"),
             ("49 / 61", GREEN, "points of gap to the −19% target (planned / existing): the Commission’s figures, reproduced"),
             ("+37%", ORANGE, "2025 emissions vs 2005 (approximated)"),
             ("1.4 Mt", ORANGE, "still to buy or cut over 2021–2030 after Malta’s own flexibilities (planned measures)")]),
      Spacer(1, 4 * mm),
      up_down("None: Supported is the top of the scale.",
              "A new Malta submission (due 2027) or a revision of the 2005 level or reviewed emissions large enough to bring "
              "the 2030 projection down to the 2005 level (it is 303 kt above it with planned measures)."),
      Spacer(1, 5 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the data show"),
          ("4", "What changed since the 2025 report"), ("5", "Where the evidence points different ways"),
          ("6", "Testing the claim"), ("7", "Verdict and requests for evidence"), ("8", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The speaker is the European Commission, in its annual report to the European Parliament and the Council under the "
           "Governance Regulation, COM(2026) 601 final. We read the text as transmitted to the Council (doc. 15659/26) [1]. "
           "We rate the words printed below; the intake’s headline (“more in 2030 than in 2005”) is a quotation of the "
           "second sentence, not a paraphrase."))
S.append(std_table([
    [C("What the Commission says", cellh), C("Where", cellh)],
    [C("“Malta’s gap to target is 49 and 61 percentage points, exceeding its 19% reduction target. This means Malta is "
       "projected to emit more in 2030 than in 2005.”"), C("Note to Figure 13, printed p. 46 [1]")],
    [C("“Before any use of ESR flexibilities by Member States to meet their targets, Germany, Ireland and Malta show the "
       "largest projected gaps to the 2030 target.”"), C("Chapter 3, printed p. 45 [1]")],
    [C("“…Austria, Cyprus, Germany, Italy, Malta, Ireland, Lithuania and Sweden are projected to have excess emissions in "
       "the second compliance period (2026-2030).” … “the Commission will request Austria, Croatia, Cyprus, Germany, Italy, "
       "Ireland, Lithuania, Malta and Sweden to submit a corrective action plan in line with article 8 of ESR.”"),
     C("Chapter 3, printed pp. 46–47 [1]")],
], [118 * mm, 52 * mm]))
S.append(Spacer(1, 2 * mm))
S.append(P("The note does not say which of 49 and 61 belongs to which projection; Figure 13’s legend separates “with "
           "additional measures” from “with existing measures”, and the 2025 report’s staff working document showed 49 for "
           "additional (planned) and 61 for existing measures [7, 8]. The third passage rests on stated assumptions: the "
           "Commission assumes planned measures are implemented, that allocations are banked and borrowed between years, and "
           "that Member States that notified the ETS flexibility use it when needed [1]. The 2026 staff working document "
           "(SWD(2026) 331) was not obtained; the page numbers are the printed pages of the main report."))
S += [Spacer(1, 1 * mm),
      callout([P("FAIRNESS NOTE", tag),
               P("This check holds an EU institution to the same standard as Maltese speakers. It tests what the Commission "
                 "said, not whether Malta’s target is fair. Related checks: CC-094 (the same sentence in the 2025 report), "
                 "CC-003 (the Climate Action Authority’s per-person figures) and CC-146 (the Central Bank on effort sharing).", small)],
              bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Question.</b> Do Malta’s reported projections, the official emissions data and the law still give a 2030 gap of "
           "49 and 61 points against a −19% target, so that Malta is projected to emit more in 2030 than in 2005? Did anything "
           "behind the sentence change since the 2025 report?"))
S.append(P("<b>Evidence.</b> We downloaded from the European Environment Agency (EEA) its 2026 effort-sharing emissions "
           "(2005–2025) [2] and its 2026 projections dataset [3], and recomputed every figure with "
           "<i>tools/cc-162-report/calc.py</i> from <i>data/cc-162/</i>. The inputs that cannot have changed (the 2005 level, "
           "targets, yearly limits and flexibilities from EU law [9–12]) and Malta’s projections as held in the 2025 dataset [4] "
           "are reused from Claim Check 094 (<i>data/cc-094/</i>, read 6 October 2026) [5, 6]. We did not repeat the literature "
           "search of CC-094, which found no peer-reviewed study of Malta’s effort-sharing gap."))
S.append(P("<b>Grades.</b> Official statistics, projections reported under EU law and legal texts are grade C under our scale. "
           "<b>Verdicts</b> follow the five-point scale in Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(60 * mm))
S.append(SectionHeading(3, "What the data show"))
S.append(P("Projections and the 2005 level", h2))
S.append(std_table([
    [C("Measure", cellh), C("Existing measures (WEM)", cellh), C("Planned measures (WAM)", cellh), C("Source", cellh), C("Grade", cellh)],
    [C("Malta’s 2030 effort-sharing emissions, March 2025 projection"), C("1,450.1 kt"), C("1,323.8 kt"), C("EEA [3, 4]"), grade_tag("C")],
    [C("Change vs the legal 2005 level (1,020.6 kt)"), C("<b>+42.1%</b>"), C("<b>+29.7%</b>"), C("calculated"), grade_tag("C")],
    [C("Gap to the −19% target"), C("<b>61.1 points</b> (Commission: 61)"), C("<b>48.7 points</b> (Commission: 49)"),
     C("calculated; [1]"), grade_tag("C")],
    [C("Excess over the 2030 limit of 826.7 kt"), C("623 kt"), C("497 kt"), C("calculated"), grade_tag("C")],
], [62 * mm, 34 * mm, 34 * mm, 24 * mm, 16 * mm]))
S.append(Spacer(1, 2 * mm))
S.append(P("Measured emissions point the same way. In the EEA’s 2026 edition, Malta’s effort-sharing emissions were 29.7%, 43.0% "
           "and 38.1% above the 2005 level in 2021–2023, 40.1% above in 2024 (1,430 kt) and 37.1% above in 2025 (1,400 kt, "
           "approximated) [2]. Malta was over its yearly limit by 220, 222, 293 and 315 kt in 2022–2025. The 2025 value is 5.7% "
           "below what the March 2025 projection expected for that year. The 2023 value (1,410 kt) is 35 kt lower than in the "
           "2025 edition of the dataset (1,445 kt); we did not find the reason, and it does not change the conclusion. Reaching 827 kt "
           "by 2030 would need a 40.9% cut from the 2025 value, about 10% a year; the planned-measures projection has 5.4% "
           "in all over five years, and the existing-measures one has emissions rising 3.6%."))
S.append(KeepTogether([fig(FIG / "fig1_path.png"), P(
    "Figure 1. Malta’s effort-sharing emissions against its yearly limits, 2021–2030. Emissions have been above the limits "
    "since 2022 and, on both projections, stay well above the 2030 limit of 827 kt. Sources [2–4, 9, 11].", cap)]))
S.append(P("Is Malta’s gap among the largest?", h2))
S.append(P("On the 2025 submissions that the EEA dataset holds for most Member States, with planned measures the largest gaps in "
           "points are Malta (48.7), Ireland (20.3) and Germany (13.2), then Austria (8.0), and the largest overachievement is "
           "Bulgaria (25.6), Greece (20.6) and Portugal (11.4): the countries the Commission names [4]. The 2026 dataset holds "
           "updated submissions for Belgium, Germany, Denmark, Estonia, Ireland, Italy, Lithuania and Romania [3]; its sheets do "
           "not give their effort-sharing totals, so we could not recompute the ranking with those updates. "
           "In tonnes, Malta’s gap is small (0.5 Mt with planned measures; CC-094)."))

# ================================================================== 4
S.append(CondPageBreak(95 * mm))
S.append(SectionHeading(4, "What changed since the 2025 report"))
S.append(P("The Commission’s sentence about Malta is word for word the same as in 2025 and so are the numbers; only the "
           "surrounding assessment moved."))
S.append(std_table([
    [C("", cellh), C("2025 report, COM(2025) 668 [7]", cellh), C("2026 report, COM(2026) 601 [1]", cellh)],
    [C("Malta’s gap, with planned / existing measures"), C("49 and 61 points"), C("49 and 61 points")],
    [C("Basis"), C("Projections of March 2025"), C("Projections of March 2025, “updated in 2026” for some Member States")],
    [C("Largest gaps"), C("Germany, Ireland, Malta"), C("Germany, Ireland, Malta")],
    [C("Excess in 2026–2030 after flexibilities"), C("Austria, Estonia, Germany, Malta, Ireland, Sweden (6)"),
     C("Austria, Cyprus, Germany, Italy, Malta, Ireland, Lithuania, Sweden (8)")],
    [C("Excess already in 2021–2025"), C("Cyprus, Croatia, Italy, Romania"), C("Cyprus, Croatia, Italy")],
    [C("Expected EU-wide surplus of allocations"), C("125–175 Mt"), C("about 140 Mt, after covering the nine")],
    [C("Commission’s conclusion"), C("“cannot, at this stage, conclude” insufficient progress"),
     C("“concludes that those nine Member States are not making sufficient progress”; corrective action plans requested")],
], [48 * mm, 60 * mm, 62 * mm]))
S.append(Spacer(1, 2 * mm))
S.append(P("The wording of the 2025 conclusion is from CC-094’s reading of COM(2025) 668 (p. 31). In 2026 the Commission rests "
           "its conclusion on the fact that “no transfers of emission allocations between Member States have been reported” "
           "[1]. Malta’s own position is unchanged in the data: no new submission, and a shortfall that depends on buying "
           "allocations that the Commission says exist in surplus."))
S.append(P("Malta’s balance, 2021–2030, with the 2026 data", h2))
S.append(std_table([
    [C("Step, total", cellh), C("Planned measures (WAM)", cellh), C("Existing measures (WEM)", cellh), C("Source", cellh)],
    [C("Yearly limits minus emissions, 2021–2025 (2025 approximated)"), C("−0.31 Mt"), C("−0.31 Mt"), C("[2, 11]")],
    [C("…after the ETS flexibility (510.3 kt)"), C("+0.20 Mt: covered"), C("+0.20 Mt: covered"), C("[12]")],
    [C("Yearly limits minus emissions, 2026–2030 (projected)"), C("−1.65 Mt"), C("−2.27 Mt"), C("[4, 11]")],
    [C("Yearly limits minus emissions, 2021–2030"), C("−1.96 Mt"), C("−2.58 Mt"), C("[2, 4, 11]")],
    [C("…after the ETS flexibility and the maximum land-use credit (0.03 Mt)"), C("<b>−1.42 Mt</b>"), C("<b>−2.04 Mt</b>"), C("[9, 12]")],
    [C("As a share of the EU surplus of about 140 Mt"), C("1.0%"), C("1.5%"), C("[1]")],
], [76 * mm, 34 * mm, 34 * mm, 26 * mm]))
S.append(Spacer(1, 2 * mm))
S.append(P("This reproduces the Commission’s pattern: Malta is covered for 2021–2025 (it is not on the first-period list) and "
           "has excess emissions in 2026–2030. With the 2026 emissions data the net excess is 1.96 Mt, smaller than the 2.09 Mt "
           "of CC-094, because the reviewed 2023 and 2024 values and the approximated 2025 value are lower than the 2025 projections assumed."))
S.append(KeepTogether([fig(FIG / "fig2_ledger.png", width=CW * 0.9), P(
    "Figure 2. Malta’s effort-sharing balance over 2021–2030 and what its own flexibilities cover. The rest would have to be "
    "bought from other Member States or cut further. Sources [1, 2, 4, 9, 11, 12].", cap)]))

# ================================================================== 5
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(5, "Where the evidence points different ways"))
S.append(contested(
    "Q1  Is a projection a fair basis for saying Malta “is projected to emit more”?", "YES, AS WORDED", GREEN,
    "The Commission says Malta “is projected to” emit more, which is what Malta’s own March 2025 projections show [4]. Measured "
    "emissions agree: 37% above 2005 in 2025 (approximated), over the yearly limit every year since 2022 [2, 11].",
    "Projections can be wrong. Malta’s 2025 value came in 5.7% below the projection’s, and the projections are a year and a "
    "half old; Malta has not updated them [3].",
    "<b>For this claim:</b> closing the gap by 2030 would take a cut of 40.9% from the 2025 level, far beyond any projection "
    "Malta has reported."))
S.append(contested(
    "Q2  Does the corrective action plan mean Malta has failed?", "NOT WHAT THE COMMISSION SAYS", GREY,
    "The Commission concludes the nine Member States “are not making sufficient progress towards their ESR obligations” [1].",
    "The same page says the EU as a whole keeps a surplus of about 140 Mt after covering the nine, so the gap can be closed by "
    "transfers between Member States, none of which had been reported [1].",
    "<b>For this claim:</b> the sentence we rate is about projected emissions, not compliance. A corrective action plan under "
    "Article 8 is a request, not a finding of non-compliance, and we do not rate it beyond reporting the Commission’s words."))

# ================================================================== 6
S.append(CondPageBreak(40 * mm))
S.append(SectionHeading(6, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> “Malta’s gap to target is 49 and 61 percentage points”"),
     C("48.7 (planned measures) and 61.1 (existing) from Malta’s projections, the legal 2005 level and the −19% target [3, 4, 9, 10]."),
     verd("ACCURATE", GREENC)],
    [C("<b>B.</b> “…Malta is projected to emit more in 2030 than in 2005”"),
     C("+29.7% and +42.1% on 2005; 2025 emissions are +37.1% already [2, 4]."), verd("ACCURATE", GREENC)],
    [C("<b>C.</b> Germany, Ireland and Malta show the largest projected 2030 gaps before flexibilities"),
     C("Reproduced on the 2025 submissions (Malta 48.7, Ireland 20.3, Germany 13.2 points). Updates from Germany and Ireland "
       "in 2026 not recomputed [3, 4]."), verd("ACCURATE (2025 DATA)", GREENC)],
    [C("<b>D.</b> Malta among Member States with excess emissions in 2026–2030, and asked for a corrective action plan"),
     C("Covered to 2025 after the ETS flexibility; −1.42 Mt over 2021–2030 after Malta’s own flexibilities (planned measures). "
       "That the Commission will request a plan is its statement of intent; no transfers reported is its statement [1, 2, 4, 11, 12]."),
     verd("ACCURATE", GREENC)],
], [62 * mm, 78 * mm, 30 * mm], valign="MIDDLE"))

# ================================================================== 7
S += [CondPageBreak(75 * mm), Spacer(1, 4 * mm), SectionHeading(7, "Verdict and requests for evidence"),
      verdict_box("Supported", "The Commission’s figures and its inference reproduce from Malta’s own reported projections, "
                  "the EEA’s data and the legal 2005 level. Confidence: high."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) The 49 and 61 points reproduce from the projections the EEA holds for Malta, the 2005 level and the "
           "target in EU law. (2) “More in 2030 than in 2005” holds under both projections; 2025 emissions (approximated) are already "
           "37% above 2005. (3) The EEA’s 2026 dataset shows Malta did not update its projections, so the 2026 sentence tests the "
           "same data as the 2025 one. Confidence is high; the one part not recomputed is the cross-country ranking with the 2026 updates."))
S.append(P("<b>What this verdict does not say.</b> That Malta will fail its legal obligations (it can buy allocations), whether "
           "the −19% target is fair to Malta, or anything about anyone’s intentions."))
S.append(KeepTogether([P("Evidence we are asking for", h2), requests_list([
    "From the Ministry for the Environment and the Climate Action Authority: how Malta intends to cover its 2026–2030 excess "
    "(purchases of allocations, from whom, at what cost), and whether it will submit updated projections.",
    "The Commission’s staff working document SWD(2026) 331 final, for Malta’s table of emissions, allocations and the flexibilities assumed.",
])]))

# ================================================================== 8
S += [Spacer(1, 2 * mm), SectionHeading(8, "Limitations")]
for l in ["Malta’s projections are the March 2025 submission as quality-checked by the EEA; the next are due in 2027. 2025 emissions are "
          "approximated, and the 2023 value was revised by 35 kt between editions of the EEA dataset (reason not found).",
          "We read the main report, not the staff working document, and could not recompute the 2026 cross-country ranking with the "
          "updated submissions of Germany, Ireland and others.",
          "Our balance treats the ETS flexibility as usable when needed, as the Commission does. Whether and at what price Malta "
          "will buy allocations is not public, so we do not estimate a cost.",
          "The 2025-report statements in section 4 are from CC-094’s reading of COM(2025) 668; we did not re-open that report."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 2 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "European Commission (9 Nov 2026). EU Climate Action Progress Report 2026, COM(2026) 601 final, as transmitted to the "
          "Council (doc. 15659/26, 11 Nov 2026): chapter 3, printed pp. 44–47 (Figure 13 note, p. 46). Read in full 16 Nov 2026.",
     "https://data.consilium.europa.eu/doc/document/ST-15659-2026-INIT/en/pdf"),
    ("2", "European Environment Agency. Greenhouse gas emissions under the Effort Sharing Legislation, 2005–2025 "
          "(GHG_ESD-ESR_2026_updated01102026.xlsx). Retrieved 16 Nov 2026.",
     "https://sdi.eea.europa.eu/catalogue/srv/api/records/be4056d8-9d3e-4cca-b995-3c684637f29e"),
    ("3", "European Environment Agency. Anthropogenic greenhouse gas emission projections, reporting year 2026 "
          "(GHG_Projections_2026 datahub_dataset.xlsx). Retrieved 16 Nov 2026.",
     "https://sdi.eea.europa.eu/catalogue/srv/api/records/4619479e-dc9f-46e5-bce2-292a952f6721"),
    ("4", "European Environment Agency. Member States’ greenhouse gas (GHG) emission projections 2025. "
          "doi:10.2909/d6938865-05e5-4016-a15c-a09bb898421d. Retrieved 6 Oct 2026 (Claim Check 094).",
     "https://doi.org/10.2909/d6938865-05e5-4016-a15c-a09bb898421d"),
    ("5", "Miżien. Claim Check 094 (the same sentence in the 2025 report), data/cc-094/.",
     "https://github.com/leandergrech/Mizien/tree/main/claims/CC-094"),
    ("6", "Miżien. Inputs reused from Claim Check 094: data/cc-094/ (legal inputs, EEA 2025 projections; read 6 Oct 2026).",
     "https://github.com/leandergrech/Mizien/tree/main/data/cc-094"),
    ("7", "European Commission (6 Nov 2025). EU Climate Action Progress Report 2025, COM(2025) 668 final, pp. 30–31, as read for "
          "Claim Check 094.", "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX%3A52025DC0668"),
    ("8", "European Commission (Nov 2025). Climate Action Progress Report 2025, staff working document SWD(2025) 347, Table 25.",
     "https://climate.ec.europa.eu/document/download/35f83a2d-f77d-4895-b616-d579069b23d3_en?filename=capr2025_swd_en.pdf"),
    ("9", "Regulation (EU) 2018/842 (Effort Sharing Regulation), Articles 4–11 and Annexes. OJ L 156, 19.6.2018.",
     "https://data.europa.eu/eli/reg/2018/842/oj"),
    ("10", "Regulation (EU) 2023/857 amending Regulation (EU) 2018/842, Annex I. OJ L 111, 26.4.2023.",
     "https://data.europa.eu/eli/reg/2023/857/oj"),
    ("11", "Commission Implementing Decisions (EU) 2020/2126 (2005 values) and 2026/895 (annual emission allocations 2021–2030).",
     "https://data.europa.eu/eli/dec_impl/2026/895/oj"),
    ("12", "Commission Implementing Decision (EU) 2024/1884 (ETS flexibility: Malta 510,300 t).",
     "https://data.europa.eu/eli/dec_impl/2024/1884/oj"),
    ("13", "Miżien. Data and calculations: data/cc-162/; tools/cc-162-report/calc.py.", ""),
])
S.append(CondPageBreak(150 * mm))
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance, "
                "official statistics or legal text · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += revision_log([("1.0", "16 Nov 2026", "First issue. No right of reply needed for a Supported verdict.")])

build_report(Report(
    number="162", out=str(FIG / "report.pdf"), kicker="EU assessments and effort-sharing data",
    title_lines=["Still more in 2030", "than in 2005?"],
    subtitle_lines=["Testing the Commission’s 2026 sentence on Malta", "and what changed since the 2025 report"],
    quote_lines=["“Malta’s gap to target is 49 and 61 percentage points,", "exceeding its 19% reduction target. "
                 "This means Malta", "is projected to emit more in 2030 than in 2005.”"],
    quote_size=13.2,
    attribution="European Commission, EU Climate Action Progress Report 2026, COM(2026) 601, p. 46, 9 Nov 2026.",
    context="Effort-sharing sectors: transport, buildings, waste, agriculture, small industry, refrigerant gases.",
    verdict="Supported", verdict_note="Reproduced from Malta’s own projections and EU law",
    footer_lines=["Version 1.0  ·  16 November 2026", "Status:",
                  "Prepared from public sources, EEA data and EU legal texts.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Malta’s 2030 effort-sharing gap, 2026", version="1.0", date="16 November 2026",
    pdf_title="Still more in 2030 than in 2005? Claim Check 162",
    pdf_subject="Tests the European Commission's 2026 statement that Malta is projected to emit more in 2030 than in 2005 "
                "in effort-sharing sectors",
    story=S))
