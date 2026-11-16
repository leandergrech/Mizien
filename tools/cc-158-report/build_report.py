"""Claim Check 158 report. Run calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("On 7 October 2025 the National Audit Office (NAO) published its review of Malta’s climate action using "
        "ClimateScanner, an international rapid-assessment tool for audit offices. Its press release said: <b>“This "
        "Review, which presents the overall situation as at September 2025, shows that Malta has made significant "
        "strides in climate action.”</b> The report scores Malta 6.92 out of 10, which it says “is considered as "
        "representing strong progress vis-à-vis climate action”. We recomputed every score, read the tool’s handbook, "
        "and set the result beside Malta’s emissions record.", lead)]
S.append(key_points([
    ("The numbers are right.",
     "All 18 rated component scores follow from the item ratings in the report’s appendix. The three axis scores "
     "(Governance 6.55, Public Policies 8.00, Finance 6.20) are the averages of their components, and 6.92 is the "
     "average of the three axes."),
    ("“Strong progress” is the NAO’s reading of the method, and a fair one.",
     "The ClimateScanner Handbook calls a <i>component</i> scoring 6.66 or more a “strength”. It defines no overall "
     "score and no “strong progress” label. 6.66 is also the score of an item at the “intermediate” stage: “many "
     "aspects … present, but there is still room for improvement”. Malta’s overall score is 0.26 above that."),
    ("The score measures whether policies exist, not what they achieve.",
     "The Handbook says so, and the NAO’s report says so twice. The press release, where “significant strides” "
     "appears, does not repeat it."),
    ("Outcomes point the other way, and the review does not cover them.",
     "Malta’s emissions under the EU effort-sharing rules were 41% above 2005 in 2024. They were over the yearly limit "
     "by 220–301 kt in 2022–2024 and are projected 30% above 2005 in 2030, against a target of −19%. The report does "
     "not mention this. The Climate Action Authority’s summary, “progress in tackling climate change”, goes further "
     "than the review."),
    ("Verdict: largely supported (high confidence).",
     "As a summary of what the review measured, the NAO’s statement holds. The caveat is that “climate action” here "
     "means policies and institutions, not results."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("6.92", GREEN, "overall ClimateScanner score, reproduced from the report’s own item ratings"),
             ("12 of 18", GREEN, "rated components at or above 6.66, the tool’s mark of a “strength”"),
             ("6.66", AMBER, "score of an item at the “intermediate” stage, and the strength threshold"),
             ("+41%", RED, "Malta’s effort-sharing emissions in 2024 against 2005 (not scored by the tool)")]),
      Spacer(1, 4 * mm),
      up_down("A public summary from the NAO stating, as its report does, that ClimateScanner records whether "
              "policies and systems exist and does not measure their results.",
              "Evidence that items were rated against the Handbook’s criteria wrongly, or that the NAO presented the "
              "score as evidence that emissions are falling."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the review measured"),
          ("4", "What the review does not measure"), ("5", "Where the evidence points different ways"),
          ("6", "Testing the claim"), ("7", "Verdict and requests for evidence"), ("8", "Limitations")])
S.append(PageBreak())

S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The sentence is in the NAO’s own press release on its website, dated 7 October 2025 [1]. The report itself "
           "(73 pages, October 2025) gives the scores and the “strong progress” wording on PDF page 14 and repeats "
           "the score in its conclusions (page 33: “considerable progress, with an overall score of 6.92 out of 10”) "
           "[2]. The same day the Climate Action Authority (CAA) welcomed the report, quoting the “strong progress” "
           "sentence correctly and adding its own summary [3]. nao.gov.mt and climateaction.gov.mt refuse scripts. "
           "We read all three from browser copies supplied by the maintainer on 16 November 2026, recorded with their "
           "sha256 hashes in the project’s archive manifest."))
S.append(std_table([
    [C("Source", cellh), C("What it says", cellh), C("Our access", cellh), C("Status", cellh)],
    [C("<b>NAO</b>, press release, 7 Oct 2025 [1]"),
     C("“This Review … shows that Malta has made significant strides in climate action.” It also notes challenges in "
       "data use and performance metrics."),
     C("Browser copy, read in full."), C("<b>The claim</b>")],
    [C("<b>NAO</b>, report, Oct 2025 [2]"),
     C("Overall 6.92; axes 6.55, 8.00, 6.20; “strong progress”; the method “mainly focuses on identifying the "
       "existence of policies … rather than evaluating their effectiveness”."),
     C("Browser copy of the PDF; text extracted; scores and appendix read in full."), C("<b>Primary</b>")],
    [C("<b>CAA</b>, 7 Oct 2025 [3]"),
     C("Notes feedback that “highlights Malta’s notable and significant progress in tackling climate change”."),
     C("Browser copy, read in full."), C("<b>Restatement</b>")],
    [C("<b>INTOSAI / TCU</b>, ClimateScanner Handbook, May 2024 [4]"),
     C("Scale, scoring and thresholds; the tool assesses whether mechanisms exist, not their effectiveness."),
     C("PDF downloaded 16 Nov 2026; p. 11 read."), C("<b>Method</b>")],
    [C("<b>EEA; EU law</b> [5, 6]; <b>Eurostat</b> [7]"),
     C("Malta’s effort-sharing emissions, yearly limits and 2030 target; total emissions."),
     C("Files saved for CC-094 and CC-025 (Oct 2026)."), C("<b>Primary data</b>")],
], [38 * mm, 66 * mm, 40 * mm, 26 * mm]))
S.append(Spacer(1, 2 * mm))
S.append(P("<b>Fairness note.</b> The NAO is an independent audit office describing its own review, and the report is "
           "open about the tool’s limits. This check asks whether the one-line summary matches what was measured. It "
           "does not question the NAO’s independence or its ratings.", small))

S += [Spacer(1, 4 * mm), SectionHeading(2, "Method")]
S.append(P("<b>Questions.</b> (A) Are the published scores correct? (B) Does the ClimateScanner method support calling "
           "6.92 “strong progress”? (C) Does the review show “significant strides in climate action”, and in what sense? "
           "(D) Does the CAA’s summary match the review?"))
S.append(P("<b>Evidence.</b> We typed the number of items at each tier for every component from the report’s appendix "
           "into <i>data/cc-158/components.csv</i>. We then recomputed each component, axis and the overall score with the "
           "Handbook’s tier values (0, 3.33, 6.66, 10) in <i>tools/cc-158-report/calc.py</i>. We read the Handbook’s "
           "scoring rules (p. 11). For outcomes, which the tool does not measure, we used the European Environment Agency "
           "(EEA) and EU legal figures saved for CC-094, and the Eurostat inventory saved for CC-025. Outputs are in "
           "<i>data/cc-158/checks.csv</i>."))
S.append(P("<b>Grades.</b> The NAO report and the Handbook are official documents (grade C). EEA and Eurostat inventories "
           "are official statistics (grade C). <b>Verdicts</b> follow the five-point scale in Appendix A."))

S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(3, "What the review measured"))
S.append(fig(FIG / "fig1_components.png", width=CW * 0.98))
S.append(P("Figure 1. The NAO’s 18 rated component scores. Shaded bands mark the Handbook’s “challenge” (3.33 or "
           "less) and “strength” (6.66 or more) ranges.", cap))
S.append(P("ClimateScanner has three axes (Governance, Public Policies, Finance), 19 components and 62 items [2]. "
           "Each item is rated at one of four tiers worth 0, 3.33, 6.66 or 10 points. A component’s score is the "
           "average of its items, and an axis score is the average of its components [4]. Every published component "
           "score follows from the appendix ratings. Malta has 18 items at the advanced tier, 26 at the intermediate "
           "tier, 14 at the early tier and none at “no progress”. One finance component (support received as a "
           "recipient country) was marked not applicable [2]."))
S.append(P("Twelve of the 18 rated components reach 6.66, the Handbook’s mark of a strength, and none falls to 3.33. "
           "This matches the NAO’s “strong performance in approximately two-thirds of the components”. The overall "
           "6.92 is the average of the three axis scores. The Handbook defines component and axis scores but no "
           "overall score, and uses the word “strengths” only for components. Applying the 6.66 mark to the overall "
           "average is the NAO’s step. It is a reasonable one, and averaging the 18 components instead gives 6.89, "
           "which is still above 6.66."))
S.append(P("Two points set the label in context. First, 6.66 is exactly the score of an item rated “intermediate”: "
           "“many aspects of item are present, but there is still room for improvement” [4]. A country rated "
           "intermediate on every item would therefore count as showing “strong progress”. Second, the Handbook says "
           "“implementation” in the tool means “the presence or not of certain features”. The NAO’s report repeats "
           "this: the tool “mainly focuses on identifying the existence of policies, mechanisms, or systems, rather "
           "than evaluating their effectiveness or efficiency” (PDF p. 14; also §1.4.1) [2]."))

S.append(CondPageBreak(95 * mm))
S.append(SectionHeading(4, "What the review does not measure"))
S.append(fig(FIG / "fig2_outcomes.png", width=CW * 0.98))
S.append(P("Figure 2. Malta’s emissions in the sectors covered by the EU Effort Sharing Regulation (transport, "
           "buildings, agriculture, waste, small industry) [6], and the yearly limits set for 2022–2030.", cap))
S.append(P("The tool does not score results, so we set them beside it, using figures from earlier checks. Under the "
           "Effort Sharing Regulation Malta must cut these emissions 19% below 2005 by 2030 [6]. In 2024 they were "
           "1,437 kt, 41% above the 2005 base of 1,021 kt. They exceeded Malta’s yearly limit by 220 kt in 2022, "
           "257 kt in 2023 and 301 kt in 2024 [5, 6]. Malta’s own projections, as compiled by the EEA, put them 30% "
           "above 2005 in 2030 even with planned measures (CC-094). Total emissions, including power generation, "
           "fell 27% between 2005 and 2024 against 33.5% for the EU-27, and have risen 18% since their low in "
           "2016 [7]."))
S.append(P("We searched the full text of the report for “effort-sharing”, “ESR”, “target”, “2030” and the 19% "
           "figure. It does not mention Malta’s effort-sharing gap or its overshoot of the yearly limits. Its "
           "mitigation-sector component (P4, energy) is rated intermediate on all four items, for plans that exist "
           "but lack clear priorities, timeframes and measurable indicators [2]. This is consistent with the tool’s "
           "scope: it was not designed to judge whether emissions are falling."))

S.append(CondPageBreak(80 * mm))
S.append(SectionHeading(5, "Where the evidence points different ways"))
S.append(contested("Does 6.92 show “significant strides in climate action”?", "YES FOR POLICIES; NOT FOR RESULTS", AMBER,
                   "Malta’s climate framework is largely in place. It rests on the Climate Action Act of 2024 and the "
                   "recently established CAA, with a National Climate Action Council and a climate coordinator in "
                   "every ministry [1, 3]. The Nationally Determined Contribution and international finance score 10, and "
                   "no component is a challenge [2].",
                   "The score records that policies exist, not what they achieve, and 6.66 is the “intermediate” "
                   "tier. Effort-sharing emissions are 41% above 2005, over the yearly limit three years running and "
                   "projected far from the 2030 target [5, 6]. The press release does not say which of these senses "
                   "“climate action” has.",
                   "Both are true at once. Read as a statement about institutions and plans, the NAO’s sentence is "
                   "supported by its review. Read as a statement about emissions, it would not be, and the review "
                   "does not claim to measure them.",
                   label_a="FOR THE CLAIM", label_b="AGAINST"))

S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(6, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> Malta’s overall ClimateScanner score is 6.92 out of 10 (axes 6.55, 8.00, 6.20)"), C("NAO [2]"),
     C("All 18 component scores follow from the appendix item ratings; the axes are their averages, and 6.92 is the "
       "average of the axes."), verd("ACCURATE", GREENC)],
    [C("<b>B.</b> 6.92 “is considered as representing strong progress” under the methodology"), C("NAO [2]"),
     C("The Handbook marks components at 6.66 or more as strengths, but defines no overall score or label. The NAO "
       "applies the same mark to the average. 6.66 is the “intermediate” tier."), verd("FAIR READING", GREENC)],
    [C("<b>C.</b> The review “shows that Malta has made significant strides in climate action”"), C("NAO [1]"),
     C("True of policies, institutions and plans, which is what the tool records. The report says it does not measure "
       "results, but the press release does not. Effort-sharing emissions are 41% above 2005."),
     verd("TRUE OF POLICIES", AMBER)],
    [C("<b>D.</b> The feedback “highlights Malta’s notable and significant progress in tackling climate change”"),
     C("CAA [3]"),
     C("The review rated whether policies exist. “Tackling climate change” suggests results it did not assess. The "
       "CAA quotes the NAO’s “strong progress” sentence correctly."), verd("GOES FURTHER", ORANGE)],
], [42 * mm, 18 * mm, 76 * mm, 34 * mm], valign="MIDDLE"))

S += [Spacer(1, 6 * mm), SectionHeading(7, "Verdict and requests for evidence"),
      verdict_box("Largely supported", "The scores and the label are correct; “climate action” here means policies and "
                  "institutions, not emissions results. Confidence: high."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> The NAO’s statement is a summary of its own review, and the review’s figures check out exactly. "
           "Calling 6.92 “strong progress” is a fair extension of the tool’s rule for components. The caveat is one "
           "of scope. The tool records whether policies, systems and institutions exist, not whether emissions fall. "
           "The NAO’s report says this plainly, but its press release does not. Malta’s effort-sharing emissions are "
           "rising and above their limits. That does not make the NAO’s sentence wrong, because the review measured "
           "something else, but a reader of the press release alone could take “significant strides” to mean results. "
           "The CAA’s restatement, “progress in tackling climate change”, moves further in that direction. "
           "<b>What this verdict does not say.</b> It does not grade Malta’s climate policy, and it does not question "
           "the NAO’s ratings of individual items."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list(["From the NAO: whether its public summaries will state that ClimateScanner records the existence "
                        "of policies and does not measure their results, as its report does.",
                        "From the NAO: the basis for applying the Handbook’s 6.66 component threshold to the overall "
                        "average.",
                        "From the Climate Action Authority: the evidence for “significant progress in tackling climate "
                        "change” beyond the ClimateScanner scores."]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag),
               P("Not needed for this verdict (maintainer rule of 5 October 2026).", small)], bg=AMBER_PALE, bar=AMBER)]
S += [Spacer(1, 6 * mm), SectionHeading(8, "Limitations")]
for l in ["nao.gov.mt and climateaction.gov.mt refuse scripts. The press release, the CAA note and the report were "
          "read from browser copies supplied by the maintainer (hashes in archive/manifest.csv). The URL of the "
          "report PDF itself was not recorded, but the press-release page links to it.",
          "Item counts were taken from the text extracted from the appendix tables. As a check, every component "
          "score is reproduced exactly from them.",
          "The Handbook read is the May 2024 English edition, the one the NAO cites (footnote 11). A later edition "
          "may word the thresholds differently.",
          "The emissions figures are reused from CC-094 and CC-025 (retrieved 5–6 October 2026). The 2024 "
          "effort-sharing value is the EEA’s approximated inventory, not the final review.",
          "The report’s situation is as at September 2025; outcomes after 2024 are not yet published."]:
    S.append(P("• " + l, bul))
S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "National Audit Office, Malta. A review of Malta’s climate action using the ClimateScanner framework – "
          "press release, 7 October 2025 (browser copy read 16 Nov 2026).",
     "https://nao.gov.mt/2025/10/07/a-review-of-maltas-climate-action-using-the-climatescanner-framework/"),
    ("2", "National Audit Office, Malta. A review of Malta’s climate action using the ClimateScanner framework. October "
          "2025, 73 pp. (PDF linked from [1]; browser copy read 16 Nov 2026; scores PDF pp. 14, 33 and Appendix pp. 38–73).", ""),
    ("3", "Climate Action Authority. Climate Action Authority welcomes the NAO report highlighting “strong progress” in "
          "climate action, 7 October 2025 (browser copy read 16 Nov 2026).", "https://climateaction.gov.mt/?p=4273"),
    ("4", "INTOSAI / Federal Court of Accounts – Brazil (TCU). ClimateScanner Handbook, May 2024, p. 11 (downloaded "
          "16 Nov 2026).", "https://sites.tcu.gov.br/recursos/climatescanner/materiais/Handbook_ENG_May24.pdf"),
    ("5", "European Environment Agency. GHG_ESD-ESR_2025.xlsx, effort-sharing emissions 2005–2024 (retrieved 6 Oct 2026 "
          "for CC-094; data/cc-094/eea_esr_emissions.csv).",
     "https://sdi.eea.europa.eu/datashare/public.php/webdav/eea_t_esd-2022_p_2005-2024_v01_r00/GHG_ESD-ESR_2025.xlsx"),
    ("6", "Implementing Decisions (EU) 2020/2126 and 2026/895 (2005 base and yearly allocations); Regulation (EU) "
          "2023/857 (2030 target −19% for Malta). Data/cc-094/esr_legal_inputs.csv.",
     "https://data.europa.eu/eli/dec_impl/2026/895/oj"),
    ("7", "Eurostat. Greenhouse gas emissions by source sector (env_air_gge), retrieved 5 Oct 2026 for CC-025.",
     "https://ec.europa.eu/eurostat/databrowser/view/env_air_gge/default/table"),
    ("8", "MiŻien. Calculation script and outputs: tools/cc-158-report/calc.py; data/cc-158/checks.csv. Related checks: "
          "CC-094 (Commission: Malta to emit more in 2030 than in 2005), CC-025 (per-capita emissions).", ""),
])
S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "16 Nov 2026", "First issue. Verdict Largely supported (high confidence); no right of reply needed.")])

build_report(Report(
    number="158", out=str(FIG / "report.pdf"), kicker="Governance and accountability",
    title_lines=["Significant", "strides?"],
    subtitle_lines=["Testing the National Audit Office’s summary of its", "ClimateScanner review of Malta’s climate action"],
    quote_lines=["“This Review … shows that Malta has made", "significant strides in climate action.”"], quote_size=15,
    attribution="National Audit Office, press release, 7 October 2025.",
    context="On its review of Malta’s climate action using the ClimateScanner framework.",
    verdict="Largely supported", verdict_note="Scores correct; they measure policies, not emissions results",
    footer_lines=["Version 1.0  ·  16 November 2026", "Status: no right of reply needed",
                  "Prepared from public sources and open data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="ClimateScanner review – NAO, October 2025", version="1.0", date="16 November 2026",
    pdf_title="Significant strides? Claim Check 158",
    pdf_subject="Tests the National Audit Office's summary of its ClimateScanner review of Malta's climate action",
    story=S))
