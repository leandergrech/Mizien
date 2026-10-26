"""Claim Check 131 report. Run fetch.py, calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
verd = lambda t, c: chip(t, c, w=29 * mm)
LG = colors.HexColor("#8DB36B")
S = []
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("In its 2026 Country Report for Malta, published on 3 June 2026, the European Commission wrote that Malta ranks "
        "low on recycling, and then: <b>“By contrast, the rate of recovery of construction and demolition waste is 100, "
        "above the EU average of 89%.”</b> The sentence cites a 2024 assessment by the Commission’s Joint Research Centre "
        "(JRC). We traced the figures to that report and to Eurostat’s waste treatment statistics, recomputed them, and "
        "looked at what the “100” is made of.", lead)]
S.append(key_points([
    ("The 100 is a percentage, and it is right.",
     "The report prints “100” without a unit, but its own table and the JRC report it cites give the rate in per cent. "
     "Eurostat’s data give 99.9996% for 2020 (12 tonnes of 2.95 million landfilled) and 99.9998% for 2022."),
    ("The EU figure is from an older release.",
     "The JRC’s 89% is the EU-27 rate for 2020 as published at the time. After revisions (mainly France), Eurostat now "
     "gives 90.9% for 2020 and 91.4% for 2022. Malta is still above the EU, by 9 points rather than 11."),
    ("Recovery is not recycling.",
     "EU law counts backfilling, the use of waste to fill excavations such as spent quarries, as recovery towards its 70% "
     "target. In 2020, the year the figures describe, 58% of Malta’s treated mineral construction waste was backfilled and "
     "42% recycled; the EU shares were 12% and 79%. On recycling alone Malta ranked 21st of 27."),
    ("The 100 began with a change of classification.",
     "Malta reported 84% of this waste as landfilled in 2010. A Commission study (2015) records that deposits in spent "
     "quarries were then reclassified from landfill to backfilling; from 2012 the recovery rate has been 100 or nearly so."),
    ("Verdict: largely supported (high confidence).",
     "The figures are accurate and use the measure EU law sets. The caveats are the missing unit, the older EU value, and "
     "that most of Malta’s ‘recovery’ in the year cited was backfilling, which the sentence does not say."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("100%", GREEN, "Malta’s C&D waste recovery rate, 2020 and 2022 (Eurostat; Commission: “100”)"),
             ("90.9%", GREEN, "EU-27, 2020, current Eurostat data (Commission: 89%, an earlier release)"),
             ("58%", AMBER, "Share of Malta’s 2020 total that was backfilling, not recycling (EU-27: 12%)"),
             ("21st", AMBER, "Malta’s rank of 27 on recycling alone, 2020 (18th of 26 in 2022)")]),
      Spacer(1, 4 * mm),
      up_down("A ‘Supported’ verdict would need the sentence to state the unit and the current EU value, and to say "
              "that the rate counts backfilling, or evidence that Malta’s backfilled waste is used as recycling-grade "
              "material.",
              "A regulator’s or auditor’s finding, that can be shown, that Malta’s quarry deposits do not meet the legal "
              "definition of backfilling (substituting non-waste material, limited to the amount strictly necessary), "
              "so that they should count as disposal."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "The two figures"),
          ("4", "What the 100 is made of"), ("5", "Where the evidence points different ways"),
          ("6", "Testing the claim"), ("7", "Verdict and requests for evidence"), ("8", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The claim is in the Commission’s 2026 Country Report for Malta (staff working document SWD(2026) 218 final), in "
           "Annex 8 on industry decarbonisation, circularity and climate, under ‘Circular economy’ [1]. We read the document "
           "in full from the Council’s register copy (the same file archived on 5 October 2026). On PDF page 76 (printed "
           "page 74) the passage reads:"))
S.append(P("“However, in 2024 the country continues to rank low on recycling rates, with only 16.7% of municipal waste "
           "recycled against the EU average of 48.1%, and 35.6% of plastic packaging in 2023 below the EU average of 42%. By "
           "contrast, the rate of recovery of construction and demolition waste is 100 (152), above the EU average of 89%.”", bul))
S.append(P("Footnote 152 reads “Techno-economic and environmental assessment of CDW management, JRC, 2024”, and its link "
           "goes to the JRC report [2]. The paragraph opens with the words “Some of Malta’s circular economy indicators show "
           "strong results.” Table A8.1 of the same annex (PDF page 79) lists “Construction and demolition waste (CDW) "
           "recovery” for Malta as 100 in 2018, no value in 2019 and 100 in 2020, with the EU at 88 (2018) and 89 (latest); "
           "the 2021–2024 columns are blank, and the notes give Eurostat as the source [1]."))
S.append(std_table([
    [C("What was said", cellh), C("Who", cellh), C("Access", cellh)],
    [C("The rate of recovery of construction and demolition waste is 100"), C("Commission [1]"), C("Read in full; page image checked")],
    [C("… above the EU average of 89%"), C("Commission [1]"), C("Read in full")],
    [C("Placed “by contrast” with low recycling rates, in a paragraph on indicators that “show strong results”"),
     C("Commission [1]"), C("Read in full")],
], [104 * mm, 34 * mm, 32 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("SCOPE NOTE", tag),
               P("The speaker is the Commission’s staff, writing a country assessment. This check tests the two figures, "
                 "their unit and source, and what the measure counts. It does not assess Malta’s quarry permits or "
                 "enforcement, the dispute over disposal fees, or claims of dumping at sea; related checks cover the "
                 "35 quarries (CC-082) and the 2021 ‘standstill’ warning (CC-063). We criticise statements, not people.", small)],
              bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Question.</b> Is Malta’s recovery rate 100% and the EU’s 89%, and what does the rate count? <b>Unit.</b> We "
           "rendered the page at 300 dpi to read the printed figure, and compared it with Table A8.1 and with the JRC "
           "report’s Table 10, headed “Overall recovery rate for CDW across the EU Member States (in %)” [2]. "
           "<b>Evidence.</b> Eurostat’s treatment of waste by category and operation (env_wastrt) and waste generation "
           "(env_wasgen), for mineral waste from construction and demolition (category W121) and soils (W126), all 27 states and "
           "the EU-27, 2010–2022, downloaded on 26 October 2026 with status flags [3, 4]. The recovery rate is recycling plus "
           "backfilling (operations R2–R11) of non-hazardous W121 divided by the amount treated; on the current data this "
           "reproduces 25 of the 27 values in the JRC’s 2020 column to within one point (calculations in "
           "<i>tools/cc-131-report/calc.py</i>; results in <i>data/cc-131/checks.csv</i>). Eurostat’s own indicator for this "
           "rate (cei_wm040) is no longer in its database: the catalogue does not list it and the data service answers that it "
           "is not available. <b>Law.</b> Directive 2008/98/EC, Article 11(2)(b); Commission Decision 2011/753/EU; Directive "
           "(EU) 2018/851 [5–7]. <b>History.</b> The Commission’s 2015 factsheet on construction waste in Malta [8]. "
           "<b>Grades.</b> Official statistics, the JRC technical report and the Commission study are grade C; two "
           "peer-reviewed studies of Eurostat’s construction-waste data are cited as context, read as abstracts (grade B) "
           "[9, 10]. Figures marked ◆ are second-hand. Verdicts follow the scale in Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(3, "The two figures"))
S.append(P("<b>Malta: 100.</b> The page shows “100” with no percent sign, although the next figure, “89%”, has one. The "
           "source makes the unit clear: the JRC writes that the rate “varies from 63% for Finland to 100% for Malta, Greece "
           "and the Netherlands, and equals on average 89% for the EU in 2020” [2, p. 41]. On Eurostat’s current data, Malta "
           "treated 2,947,811 tonnes of mineral construction and demolition waste in 2020 and recovered all but 12 tonnes: "
           "99.9996%. In 2022 it treated 2,062,368 tonnes and recovered all but 4: 99.9998% (Eurostat marks Malta’s 2022 "
           "values as estimates) [3]. The rate rounds to 100 in every reported year since 2012."))
S.append(fig(FIG / "fig2_eu_2020.png"))
S.append(P("Figure 1. Recovery rate of mineral construction and demolition waste, 2020, by Member State, split into "
           "recycling and other recovery (mostly backfilling). Malta (strong colours) is at 100 with Greece and the "
           "Netherlands; the dashed line is the EU-27 aggregate on current data.", cap))
S.append(P("<b>EU: 89%.</b> This is the JRC’s value for 2020, from the Eurostat release available when the report was "
           "written (it was published in 2024) [2]. Eurostat has since revised some countries; France’s 2020 rate moved from 74% "
           "in the JRC table to 81.7% now, and the EU-27 rate for 2020 is now 90.9%. For 2022 it is 91.4% [3]. The "
           "simple average of the Member States is 90.7% (2020) and 92.5% (2022). On any of these, Malta is above the EU, "
           "by about 9 points rather than the 11 the sentence implies. In 2020, 26 of 27 states were at or above the 70% "
           "target; three (Greece, Malta, the Netherlands) round to 100 [3]."))
S.append(P("<b>Tense.</b> The sentence says the rate “is” 100, but the figures it cites are for 2020. Eurostat’s 2022 "
           "data, released before the report was written (the dataset was last updated in September 2025), also give 100 for Malta, so the "
           "present tense does not change the number. The NSO’s 2024 figures were not in a form we could test (see Section 4)."))

# ================================================================== 4
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(4, "What the 100 is made of"))
S.append(P("<b>What the law counts.</b> The Waste Framework Directive set a target for 2020: “the preparing for re-use, "
           "recycling and other material recovery, including backfilling operations using waste to substitute other materials” "
           "of non-hazardous construction and demolition waste was to reach at least 70% by weight [5]. The Commission’s "
           "calculation rules require backfilling to be reported separately [6]. Since 2018 the Directive defines "
           "backfilling as a recovery operation where suitable non-hazardous waste is used to reclaim excavated areas or for "
           "engineering in landscaping; the waste must substitute non-waste materials and be limited to the amount strictly "
           "necessary [7]. Recycling, by definition, excludes reprocessing into materials for backfilling [5]. So a "
           "recovery rate of 100% means that no waste was reported as landfilled; it does not mean that all of it was "
           "recycled."))
S.append(fig(FIG / "fig1_malta_series.png"))
S.append(P("Figure 2. Malta’s treated mineral construction and demolition waste by operation, 2010–2022 (Eurostat collects "
           "these data every two years). The recovery rate (top) is recycling plus backfilling.", cap))
S.append(P("<b>Malta’s split.</b> In 2020, 41.8% of the waste was recycled and 58.2% backfilled; in 2022, 67.3% and 32.7% [3]. "
           "For the EU-27 the shares were 78.7% recycled and 12.2% backfilled in 2020, and 80.3% and 11.1% in 2022; the rest "
           "was mainly landfilled. On recycling alone Malta ranked 21st of 27 in 2020 and 18th of 26 in 2022; on backfilling "
           "it ranked 4th of 26 in 2020, after Hungary, Denmark and Portugal [3]. Malta is not alone in relying on "
           "backfilling, but in the year the Commission’s figures describe, most of its “recovery” was backfilling."))
S.append(P("<b>A change of classification.</b> Malta’s data for 2010 show 84.1% of this waste landfilled (636,638 tonnes) and "
           "a recovery rate of 16% (the JRC table gives 16 too). From 2012, landfill falls to 0.3% and backfilling rises to 77% [3]. "
           "The Commission’s 2015 factsheet on construction waste in Malta explains why: until the 2012 reporting, waste deposited "
           "in spent quarries was reported as landfill; in early 2015 the Malta Environment and Planning Authority told the NSO "
           "it should be classified as backfilling, so “a large amount previously reported as landfilling, now is reported as "
           "recovery and contributes to the fulfilment of the WFD targets” [8, pp. 4–5]. The factsheet called backfilling "
           "“the principal CDW management practice in Malta” and said the waste plan of the time recognised “the need to move "
           "away from backfilling” to options higher in the waste hierarchy [8, p. 3]. The jump in Figure 2 is therefore "
           "largely a change in how quarry deposits are counted, documented by the Commission’s own study, rather than a "
           "measured change in practice."))
S.append(P("<b>Since 2022.</b> Malta’s recycling share rose from 22% (2018) to 67% (2022) [3]. The NSO’s release on 2024 "
           "reports that backfilling of mineral construction and demolition waste “surged by 58.0 per cent (381,727 tonnes)” "
           "and recycling “declined by 13.6 per cent (197,255 tonnes)” ◆ [11]. We read the release text only through a "
           "web-reading tool and could not open its tables; taken at face value, these figures put backfilling at about 45% "
           "of the total again in 2024 ◆. The NSO also says the inert waste taken to quarries “also includes clean "
           "geological material from excavation works” [11] ◆."))

# ================================================================== 5
S.append(CondPageBreak(95 * mm))
S.append(SectionHeading(5, "Where the evidence points different ways"))
S.append(contested("Is a recovery rate of 100 a ‘strong result’?", "BOTH, ON DIFFERENT MEASURES", AMBER,
                   "It is the measure EU law sets for construction waste, and Malta met its 70% target with almost no waste "
                   "landfilled. Eurostat and the JRC give 100 for 2020 and 2022 [2, 3]. Several states with high rates also "
                   "rely on backfilling (Hungary 88%, Denmark 73%, Portugal 63% in 2020) [3].",
                   "In 2020, 58% of Malta’s total was backfilling, mostly into spent quarries; recycling was 42% against "
                   "79% for the EU. Before 2012 the same deposits were reported as landfill [3, 8]. Peer-reviewed work warns "
                   "that differing readings of ‘backfilling’ impede comparisons between countries [9].",
                   "The sentence uses the legal term correctly, but it sits “by contrast” with recycling rates and in a "
                   "paragraph on “strong results”. A reader who takes recovery as recycling would overrate Malta’s "
                   "performance; a reader of EU waste law would not. That is a caveat about context, not about the figure.",
                   label_a="FOR THE ‘STRONG RESULT’ READING", label_b="AGAINST"))
S.append(contested("Is the EU average 89%?", "OLDER RELEASE", LG,
                   "The JRC report, dated 2024 and cited by the Commission, gives 89% for the EU in 2020 [2].",
                   "Current Eurostat data give 90.9% for 2020 and 91.4% for 2022, after revisions (France 74% to 81.7% for "
                   "2020) [3].",
                   "The Commission used its source correctly; the source was out of date by June 2026. The comparison’s "
                   "direction does not change.",
                   label_a="THE CITED SOURCE", label_b="CURRENT DATA"))

# ================================================================== 6
S.append(CondPageBreak(80 * mm))
S.append(SectionHeading(6, "Testing the claim"))
S.append(std_table([
    [C("Sub-claim", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> The rate of recovery of construction and demolition waste is 100"),
     C("A percentage (unit not printed): 99.9996% in 2020 and 99.9998% in 2022 in Eurostat; 100 in the JRC table [2, 3]."),
     verd("ACCURATE", GREENC)],
    [C("<b>B.</b> Above the EU average of 89%"),
     C("89% is the JRC’s 2020 value from an earlier release; current data give 90.9% (2020) and 91.4% (2022). Malta is still "
       "above [2, 3]."), verd("OLDER FIGURE", LG)],
    [C("<b>C.</b> Presented “by contrast” with low recycling rates, as a strong result"),
     C("The rate counts backfilling: 58% of Malta’s 2020 total (EU 12%); recycling alone 42%, 21st of 27. Quarry deposits "
       "counted as landfill until the 2012 data [3, 8]."), verd("NEEDS CONTEXT", AMBER)],
], [58 * mm, 82 * mm, 30 * mm], valign="MIDDLE"))
S.append(P("The rest of the paragraph (municipal and plastic packaging recycling) is covered by CC-117 and CC-111 and is not "
           "rated here.", cap))

# ================================================================== 7
S += [Spacer(1, 6 * mm), SectionHeading(7, "Verdict and requests for evidence"),
      verdict_box("Largely supported", "The figures are right on the legal measure; the sentence leaves out that most of "
                  "the ‘recovery’ was backfilling. Confidence: high."),
      Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) Malta’s recovery rate is 100% in 2020 and 2022 on Eurostat’s data and in the JRC report the "
           "Commission cites; the missing percent sign is a slip. (2) Malta is above the EU, although the EU value cited "
           "(89%) is from an earlier release and is now about 91%. (3) The measure is the one EU law uses for the 70% target, "
           "and the Commission names it correctly as “recovery”. The caveats are that the sentence, placed against recycling "
           "rates, does not say that the rate counts backfilling, which made up 58% of Malta’s total in 2020, or that Malta’s "
           "rate rose to 100 when quarry deposits were reclassified. These caveats concern how the figure should be read, not "
           "whether it is correct, which is why the verdict is ‘largely supported’ rather than ‘misleading’. Confidence is "
           "high because the Commission’s figures, the JRC table and Eurostat agree. <b>What this verdict does not say.</b> "
           "It does not say whether Malta’s quarry deposits meet the legal definition of backfilling; we found no "
           "regulator’s finding either way."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "European Commission: whether the Country Report should give the rate as a percentage and use the current EU value, and "
    "whether it will report recycling and backfilling separately for construction waste.",
    "Environment and Resources Authority: how deposits in quarries are assessed against the 2018 definition of backfilling "
    "(substitution of non-waste materials, amount strictly necessary), and the tonnage by quarry.",
    "National Statistics Office: the 2024 tables for mineral construction and demolition waste by operation, and how "
    "excavated rock is coded (W121 or soils).",
]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag), P("Not needed for this verdict (maintainer rule of 5 October 2026).", small)],
              bg=AMBER_PALE, bar=AMBER)]

# ================================================================== 8
S += [Spacer(1, 6 * mm), SectionHeading(8, "Limitations")]
for l in ["Eurostat revises its series; the values here are those of the 23 September 2025 release (treatment) and 14 October "
          "2026 (generation). Malta’s 2022 values are estimates (flag e). Eurostat’s former indicator cei_wm040 is no longer "
          "published, so we recomputed the rate; we did not find why it was withdrawn.",
          "Malta’s treated tonnage exceeded the amount generated in 2022 (102.9%), as the 2015 factsheet also found for 2012; "
          "the rate is computed on waste treated, not generated.",
          "Malta reports almost no soil waste (W126: 80 tonnes generated in 2022), which the indicator excludes. We could "
          "not tell from the published data whether excavated rock is reported within W121, which would raise both the "
          "numerator and the denominator.",
          "The NSO’s 2024 figures (◆) were read through a web-reading tool from the release text; the tables could not be opened.",
          "The peer-reviewed studies were read as abstracts only and do not analyse Malta specifically.",
          "We found no finding by a regulator or auditor on whether Malta’s quarry deposits meet the definition of backfilling; "
          "our search (web search, the ERA site, the 2015 factsheet) is listed in literature/CC-131/notes.md and was not exhaustive."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "European Commission (3 Jun 2026; transmitted to the Council 8 Jun 2026). 2026 Country Report – Malta, "
          "SWD(2026) 218 final, Annexes (Council document 10135/26 ADD 1), Annex 8, PDF pp. 76 (claim, footnote 152) and 79 "
          "(Table A8.1).", "https://data.consilium.europa.eu/doc/document/ST-10135-2026-ADD-1/en/pdf"),
    ("2", "Cristóbal García J., Caro D., Foster G., Pristerà G., Gallo F., Tonini D. (2024). Techno-economic and "
          "environmental assessment of construction and demolition waste management in the European Union. JRC Technical "
          "Report JRC135470, EUR 31784 EN. Publications Office of the EU. doi:10.2760/721895. Section 4.5 and Table 10, "
          "pp. 41–43. (Read in full; CC BY 4.0.)", "https://doi.org/10.2760/721895"),
    ("3", "Eurostat. Treatment of waste by waste category, hazardousness and waste management operations (env_wastrt), "
          "W121 and W126, 2010–2022, dataset updated 23 Sep 2025; downloaded 26 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/env_wastrt"),
    ("4", "Eurostat. Generation of waste by waste category, hazardousness and NACE Rev. 2 activity (env_wasgen), updated "
          "14 Oct 2026; downloaded 26 Oct 2026.", "https://ec.europa.eu/eurostat/databrowser/view/env_wasgen"),
    ("5", "Directive 2008/98/EC on waste, Articles 3(17) and 11(2)(b). OJ L 312, 22.11.2008.",
     "http://publications.europa.eu/resource/celex/32008L0098"),
    ("6", "Commission Decision 2011/753/EU establishing rules and calculation methods for verifying compliance with the "
          "targets set in Article 11(2) of Directive 2008/98/EC, Article 4 and Annex III. OJ L 310, 25.11.2011.",
     "http://publications.europa.eu/resource/celex/32011D0753"),
    ("7", "Directive (EU) 2018/851 amending Directive 2008/98/EC, Article 1 (new Article 3(17a), backfilling). OJ L 150, "
          "14.6.2018.", "http://publications.europa.eu/resource/celex/32018L0851"),
    ("8", "Deloitte and BIO by Deloitte for the European Commission (Sept 2015). Construction and Demolition Waste "
          "management in Malta, V2 (screening factsheet, ‘Resource Efficient Use of Mixed Wastes’), pp. 3–5.",
     "https://ec.europa.eu/environment/pdf/waste/studies/deliverables/CDW_Malta_Factsheet_Final.pdf"),
    ("9", "Moschen-Schimek J., Kasper T., Huber-Humer M. (2023). Critical review of the recovery rates of construction and "
          "demolition waste in the European Union – An analysis of influencing factors in selected EU countries. "
          "<i>Waste Management</i> 167:150–164. doi:10.1016/j.wasman.2023.05.020. (Abstract read.)",
     "https://doi.org/10.1016/j.wasman.2023.05.020"),
    ("10", "Villoria Sáez P., Osmani M. (2019). A diagnosis of construction and demolition waste generation and recovery "
           "practice in the European Union. <i>Journal of Cleaner Production</i> 241:118400. doi:10.1016/j.jclepro.2019.118400. "
           "(Abstract read.)", "https://doi.org/10.1016/j.jclepro.2019.118400"),
    ("11", "◆ National Statistics Office Malta (17 Feb 2026). Solid Waste Management: 2024, NR 023/2026. Release text read "
           "through a web-reading tool on 26 Oct 2026; tables not read (403).", "https://nso.gov.mt/solid-waste-management-2024/"),
    ("12", "Miżien. Data and calculations: data/cc-131/; tools/cc-131-report/calc.py (checks.csv).", ""),
])
S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or official "
                "statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "26 Oct 2026", "First issue. Verdict Largely supported (high confidence); no right of reply needed.")])

build_report(Report(
    number="131", out=str(FIG / "report.pdf"), kicker="Waste and the circular economy",
    title_lines=["Malta recovers", "100% of its", "construction waste?"],
    subtitle_lines=["Testing the Commission’s 2026 Country Report", "against the JRC and Eurostat’s waste statistics"],
    quote_lines=["“By contrast, the rate of recovery of construction", "and demolition waste is 100, above the EU average of 89%.”"],
    quote_size=14,
    attribution="European Commission, 2026 Country Report – Malta, 3 June 2026.",
    context="Annex 8, circular economy, citing a 2024 JRC assessment.",
    verdict="Largely supported", verdict_note="Right on the legal measure; most of it was backfilling",
    footer_lines=["Version 1.0  ·  26 October 2026", "Status:",
                  "Prepared from public sources and Eurostat data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Construction waste recovery – European Commission", version="1.0", date="26 October 2026",
    pdf_title="Malta recovers 100% of its construction waste? Claim Check 131",
    pdf_subject="Tests the Commission's 2026 Country Report statement on Malta's construction and demolition waste recovery rate",
    story=S))
