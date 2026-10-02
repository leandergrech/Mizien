"""Claim Check 004 report. Run calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []

# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("On 19 January 2026 the Ministry for the Environment said Malta was making <b>“strong progress” in "
        "waste separation</b>: mixed waste down by over 30% to 95.5 million kg, a record 30 million kg of organic "
        "waste, and about <b>412 million kg diverted from landfill over five years</b>. The Minister said the "
        "Long-Term Waste Management Plan “is working”. We tested these statements against the measure "
        "EU law uses: the share of municipal waste that is actually recycled.", lead)]
S.append(key_points([
    ("Separation really is rising.",
     "NSO and Eurostat confirm more organic, grey-bag, glass and deposit-scheme waste each year. Landfilled "
     "municipal waste fell 21% from 2019 to 2024."),
    ("But kilograms separated are not a recycling rate.",
     "EU law counts waste when it enters a recycling process after sorting. On that basis Malta recycled 16.7% of "
     "its municipal waste in 2024. The EU average is 48%; the 2025 target is 55%."),
    ("Four-fifths still goes to landfill.",
     "79% of treated municipal waste was landfilled in 2024. Malta missed the 2020 target by a wide margin and the "
     "Commission says it is on course to miss 2025."),
    ("The 412 million kg cannot be reconciled with published data.",
     "Eurostat records 271 thousand tonnes recycled or energy-recovered in 2020–2024. The release gives no "
     "scope, years or method; the 141 to 95.5 million kg comparison has no start year."),
    ("Verdict: not substantiated.",
     "Progress in separation is real, but “the plan is working” and the diversion figure are stated "
     "more strongly than the published evidence allows."),
]))
S += [Spacer(1, 4 * mm), VerdictMeter(2), Spacer(1, 3 * mm),
      tiles([("16.7%", RED, "Municipal waste recycled, 2024 (EU 48.1%)"),
             ("55%", GREEN, "EU target for 2025 (60% by 2030)"),
             ("79%", RED, "Share of treated municipal waste landfilled, 2024"),
             ("412 vs 271", ORANGE, "Thousand tonnes: ministry’s “diverted” vs Eurostat recycled or recovered")]),
      Spacer(1, 4 * mm),
      up_down("The scope, years and method behind 412 million kg, reconciled with NSO and Eurostat; sorting-plant "
              "reject rates showing most separated waste is recycled; an official projection showing Malta will reach "
              "55% by a stated date.",
              "Evidence that “diverted” counts collected weight including rejects later landfilled, or "
              "includes construction waste; a 2025 recycling rate no higher than 2024."),
      Spacer(1, 5 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "Separated, recycled, diverted"),
          ("4", "What the data show"), ("5", "Where the evidence points different ways"), ("6", "Testing the claim"),
          ("7", "Verdict and requests for evidence"), ("8", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The claim is the Department of Information press release PR260072en of 19 January 2026, read in full "
           "[1]. It reports a press conference by Minister Miriam Dalli and WasteServ CEO Richard Bilocca. A copy on "
           "publicservice.gov.mt (23 January) could not be opened [2]. Our candidate file also cited ERA’s "
           "“68% recycled” figure; reading ERA’s statement in full [9] shows it is explicitly about "
           "construction and demolition waste, so it is not part of this claim and our earlier note has been "
           "corrected."))
S.append(std_table([
    [C("Source", cellh), C("What it says", cellh), C("Our access", cellh), C("Status", cellh)],
    [C("<b>Ministry press release</b>, 19 Jan 2026 [1]"),
     C("Mixed waste down over 30%, now 95.5 million kg, “down from approximately 141 million kg”. Organic "
       "waste a record 30 million kg in 2025. Commercial mixed waste −1.1% (2024–25). Minister: “our "
       "Long-Term Waste Management Plan is working”; “we have diverted roughly 412 million kilogrammes of "
       "waste away from landfill over the past five years”."),
     C("Read in full in a browser (site blocks automated access)."), C("<b>The claim</b>")],
    [C("<b>NSO</b>, Municipal Waste 2024 [4]; Solid Waste Management 2024 [5]"),
     C("353,525 t municipal waste generated; 79.2% of treated municipal waste landfilled; 58,156 t recycled. "
       "Household separate collections up."), C("Salient points read."), C("<b>Primary data</b>")],
    [C("<b>Eurostat</b> [3]"), C("Recycling rates, treatment routes, packaging rates for Malta and EU-27."),
     C("Downloaded 2 Oct 2026."), C("<b>Primary data</b>")],
    [C("<b>European Commission</b>, EIR 2025 [6]"),
     C("Malta missed the 2020 target to recycle 50% of municipal waste by a large margin; on course to miss 2025 "
       "targets (55% municipal, 65% packaging)."), C("Waste passages read."), C("EU assessment")],
], [36 * mm, 76 * mm, 36 * mm, 22 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("FAIRNESS NOTE", tag),
               P("Mandatory separation (2023), a unified collection schedule and differentiated gate fees are the kinds "
                 "of measure the research associates with higher recycling: weekly food-waste collection and less "
                 "frequent residual collection were linked to higher recycling rates across 297 districts in England "
                 "and Wales [10]. Separation figures have improved. This check is about whether the release’s "
                 "conclusions follow from its figures.", small)], bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Question.</b> Do the figures in the release show “strong progress” and a plan that “is "
           "working”, when tested against the recycling and landfill measures that Malta’s EU obligations "
           "use?"))
S.append(P("<b>Evidence.</b> Eurostat municipal-waste tables (cei_wm011, env_wasmun, cei_wm020) and NSO releases, "
           "downloaded or read on 2 October 2026; the Waste Framework Directive as amended in 2018 [7]; the "
           "Commission’s 2025 Environmental Implementation Review [6]. All percentages are recomputed by script "
           "(<i>tools/cc-004-report/calc.py</i>; outputs in <i>data/cc-004/</i>). A Crossref search found no "
           "peer-reviewed study of Malta’s municipal waste system; one observational study on collection policy "
           "is used for context [10]."))
S.append(P("<b>Grades.</b> Official statistics and EU assessments: C. The collection-policy study: B. "
           "<b>Verdicts</b> follow Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(100 * mm))
S.append(SectionHeading(3, "Separated, recycled, diverted"))
S.append(P("The release uses three different measures, and they are easy to run together."))
S.append(P("<b>1. Separated (collected) weight.</b> Kilograms placed in organic, grey or green bags, glass banks or the "
           "deposit scheme. This is an <i>input</i>: it includes contamination and items that sorting plants later "
           "reject.", bul))
S.append(P("<b>2. Recycled weight.</b> Under Article 11a of the Waste Framework Directive, recycled municipal waste is "
           "the weight that, “having undergone all necessary checking, sorting and other preliminary "
           "operations”, enters the recycling operation [7]. This is the <i>outcome</i> the 55% target is "
           "measured on.", bul))
S.append(P("<b>3. Diverted from landfill.</b> Not defined in the release. It could mean weight collected separately, "
           "weight recycled, or weight sent anywhere but landfill (including energy recovery and exports).", bul))
S.append(callout([P("WHY IT MATTERS HERE", tag),
                  P("A rise in separated weight is a necessary step towards recycling, but the recycling rate is what "
                    "EU law and the Commission assess. The release reports measure 1, and an undefined measure 3. "
                    "It does not report measure 2. Our methodology calls this pattern <i>input-as-outcome</i>, and "
                    "using a favourable measure where the regulator uses a different one a <i>selective metric</i>.",
                    small)], bg=BLUE_PALE, bar=BLUE))

# ================================================================== 4
S.append(PageBreak())
S.append(SectionHeading(4, "What the data show"))
S.append(fig(FIG / "fig1_recycling_rate.png"))
S.append(P("Figure 1. Share of municipal waste recycled, Malta and EU-27, with the EU targets. Malta’s rate has "
           "risen from 9.1% (2019) to 16.7% (2024), roughly 1.5 points a year.", cap))
S.append(fig(FIG / "fig2_routes.png"))
S.append(P("Figure 2. Left: what happened to Malta’s treated municipal waste, with the landfilled share. Right: the "
           "ministry’s five-year “diverted” figure beside Eurostat’s recycled and energy-recovered "
           "municipal waste for 2020–2024. The windows may differ by a year: 2025 data are not yet published.", cap))
S.append(std_table([
    [C("Indicator", cellh), C("Malta", cellh), C("EU-27 / target", cellh), C("Source", cellh), C("Grade", cellh)],
    [C("Municipal recycling rate, 2024"), C("<b>16.7%</b>"), C("48.1% / 55% by 2025"), C("Eurostat cei_wm011 [3]"), grade_tag("C")],
    [C("Municipal recycling rate, 2019"), C("9.1%"), C("47.2%"), C("Eurostat [3]"), grade_tag("C")],
    [C("Landfilled share of treated municipal waste, 2024"), C("<b>79%</b>"), C("–"),
     C("Eurostat env_wasmun; NSO [3, 4]"), grade_tag("C")],
    [C("Landfilled municipal waste, 2019 to 2024"), C("321 to 255 kt (−21%)"), C("–"), C("Eurostat [3]"), grade_tag("C")],
    [C("Municipal waste generated, 2019 to 2024"), C("351 to 354 kt (+1%)"), C("–"), C("Eurostat [3]"), grade_tag("C")],
    [C("Recycled + energy-recovered, 2020–2024"), C("271 kt"), C("Ministry: 412 million kg “diverted”"),
     C("Eurostat [3]; [1]"), grade_tag("C")],
    [C("Composting and digestion counted as recycling, 2019–2024"), C("0 t each year"), C("–"),
     C("Eurostat env_wasmun (RCY_C_D) [3]"), grade_tag("C")],
    [C("Packaging recycling rate, 2023"), C("43.4%"), C("67.4% / 65% by 2025"), C("Eurostat cei_wm020 [3]"), grade_tag("C")],
    [C("2020 municipal target"), C("Missed by a large margin"), C("50%"), C("Commission EIR 2025 [6]"), grade_tag("C")],
], [60 * mm, 30 * mm, 38 * mm, 30 * mm, 12 * mm]))
S.append(P("Values in <i>data/cc-004/checks.csv</i>. kt = thousand tonnes = million kg.", cap))
S.append(P("Reading across the data", h2))
for t in ["• <b>The direction is right.</b> The recycling rate nearly doubled from 2019, and the landfilled tonnage "
          "fell by a fifth while generation stayed flat.",
          "• <b>The level is far from the target.</b> At the 2019–2024 pace of about 1.5 points a year, reaching "
          "55% would take roughly 25 years (an illustrative straight-line extrapolation, not a forecast).",
          "• <b>Separately collected organic waste does not show up as recycling.</b> Eurostat records zero tonnes of "
          "Maltese municipal waste recycled by composting or digestion in each year from 2019 to 2024, although the "
          "release reports 30 million kg of organic waste collected in 2025 and converted to electricity and compost. "
          "We do not know why; it may concern how digestate is used or reported. It is one of our questions.",
          "• <b>The 412 million kg is about 140 thousand tonnes more</b> than Eurostat’s recycled and "
          "energy-recovered municipal waste for 2020–2024. If the ministry’s five years are 2021–2025, "
          "the 2025 figure would have to exceed 170 thousand tonnes to close the gap, more than two and a half times the "
          "2024 level. The figure may include commercial or non-municipal streams; the release does not say."]:
    S.append(P(t, bul))

# ================================================================== 5
S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(5, "Where the evidence points different ways"))
S.append(contested(
    "Q1  Is separation the right thing to measure?", "USEFUL, NOT SUFFICIENT", AMBER,
    "Separation at source is a precondition for high-quality recycling, and the measures Malta introduced (mandatory "
    "separation, gate fees, weekly organics) match those associated with higher recycling elsewhere [10]. Household "
    "separate collections rose in 2024 [5].",
    "EU targets are set on recycled weight after sorting [7]. Malta’s recycling rate is about a third of the EU "
    "average and 38 points below the 2025 target [3]. Separated weight can rise while rejects are landfilled.",
    "<b>For this claim:</b> the figures support “progress in separation”. They do not by themselves support "
    "“the plan is working” if the plan is judged by recycling outcomes."))
S.append(contested(
    "Q2  Is the trend fast enough to call it strong progress?", "ON CURRENT DATA, NO", RED,
    "The recycling rate rose from 9.1% to 16.7% in five years. Separation "
    "measures began in 2023 and may take time to show. Mixed waste fell by over 30% on the ministry’s figures [1].",
    "The 2020 target was missed by a large margin and the Commission says Malta is on course to miss 2025 [6]; it was "
    "among the states flagged in the 2023 early-warning report [8 ◆]. The rate dipped from 17.4% (2023) to 16.7% "
    "(2024) [3].",
    "“Strong” is a judgement. Relative to Malta’s past it is defensible; relative to the legal target it "
    "is not. <b>For this claim:</b> the release gives only the first comparison."))
S.append(contested(
    "Q3  Do the release’s own numbers add up?", "CANNOT BE CHECKED", GREY,
    "The 141 to 95.5 million kg change is −32%, consistent with “over 30%”. Landfilled municipal "
    "waste fell 21% in 2019–2024 [3], the same direction.",
    "No start year is given for 141 million kg, and “mixed waste” is not a published NSO or Eurostat "
    "series. The 412 million kg exceeds Eurostat’s recycled and recovered tonnage by about 140 thousand tonnes.",
    "<b>For this claim:</b> the figures may come from WasteServ operational data. Until scope and method are "
    "published, they cannot be reproduced."))

# ================================================================== 6
S.append(PageBreak())
S.append(SectionHeading(6, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> Mixed waste down over 30%, to 95.5 million kg from about 141 million kg"), C("Ministry [1]"),
     C("Arithmetic correct (−32%). No start year; not a published statistic. Direction consistent with "
       "Eurostat landfill data."), verd("UNVERIFIABLE AS STATED", GREY)],
    [C("<b>B.</b> Organic waste a record 30 million kg in 2025"), C("Ministry [1]"),
     C("2025 data not yet published by NSO. 2024 NSO data show organic-bag collections rising."),
     verd("PLAUSIBLE", AMBER)],
    [C("<b>C.</b> About 412 million kg diverted from landfill over five years"), C("Minister Dalli [1]"),
     C("Not reconcilable with Eurostat (271 kt recycled or recovered, 2020–24). Scope, years and method not "
       "stated."), verd("NOT SUBSTANTIATED", ORANGE)],
    [C("<b>D.</b> Malta records strong progress in waste separation"), C("Ministry [1]"),
     C("Separated collections and the recycling rate have risen. “Strong” is relative to Malta’s "
       "past, not to its targets."), verd("PARTLY SUPPORTED", AMBER)],
    [C("<b>E.</b> The Long-Term Waste Management Plan is working; real and measurable outcomes"),
     C("Minister Dalli [1]"),
     C("Outcome measures: 16.7% recycled, 79% landfilled; 2020 target missed, 2025 on course to be missed [3, 6]. "
       "The release does not report them."), verd("NOT SUBSTANTIATED", ORANGE)],
], [44 * mm, 22 * mm, 70 * mm, 34 * mm], valign="MIDDLE"))
S += [Spacer(1, 4 * mm),
      callout([P("A CORRECTION TO OUR OWN CANDIDATE NOTE", tag),
               P("Our candidate list said ERA’s ‘68% recycled’ figure “covers mostly inert "
                 "construction material”, implying it might be read as a general recycling rate. ERA’s "
                 "statement says plainly that 68% of construction waste was recycled [9]. ERA did not present it as "
                 "municipal recycling, and we have removed that point from this check.", small)],
              bg=GREY_PALE, bar=SLATE)]

# ================================================================== 7
S += [Spacer(1, 6 * mm), SectionHeading(7, "Verdict and requests for evidence"),
      verdict_box("Not substantiated", "Real progress in separation; the wider conclusions are not shown. "
                  "Confidence: moderate. The ministry’s own figures could not be reproduced."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) Separate collection is rising and the recycling rate has improved from a very low base, so "
           "“progress in waste separation” is supported. (2) The release presents collected weight and an "
           "undefined “diverted” figure as evidence that the plan “is working”, but the outcome "
           "measures used by EU law show 16.7% recycled and 79% landfilled, far from the 55% target for 2025. "
           "(3) The 412 million kg figure cannot be reconciled with published statistics. We chose <i>Not "
           "substantiated</i> rather than <i>Misleading</i> because the release is framed around separation, where "
           "its direction is right, and because the ministry may hold data that explain the 412 figure."))
S.append(P("<b>What this verdict does not say.</b> It does not say the figures are invented, that separation measures "
           "were wrong, or that anyone acted in bad faith. A checkable statement would read: <i>“Separate "
           "collection rose to X t; after sorting, Y t entered recycling, raising the recycling rate to Z%. We expect "
           "to reach 55% by [year].”</i>"))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "The years, waste streams (household, commercial, deposit scheme, construction) and measurement point behind "
    "“412 million kg diverted from landfill”.",
    "The start year and definition of “mixed waste” in the 141 to 95.5 million kg comparison.",
    "Reject rates at sorting plants: how much separately collected grey- and green-bag waste is landfilled after "
    "sorting.",
    "How organic waste and digestate are reported to Eurostat, given that no composting or digestion is recorded as "
    "recycling for 2019–2024.",
    "Malta’s expected 2025 municipal recycling rate, and the year in which the plan expects to reach 55%.",
    "Whether Malta notified a postponement of the 2025 target under Article 11(3) of the Directive.",
]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag),
               P("Before wider circulation this draft should be sent to the Ministry for the Environment, Energy and "
                 "Public Cleanliness and to WasteServ with a fixed deadline (suggested 14 days). Responses will be "
                 "appended and the verdict revisited.", small)], bg=AMBER_PALE, bar=AMBER)]

# ================================================================== 8
S += [Spacer(1, 6 * mm), SectionHeading(8, "Limitations")]
for l in ["This is a statistical check. No peer-reviewed study of Malta’s municipal waste system was found; the one "
          "study used [10] is from England and Wales and is read as an abstract.",
          "2025 statistics are not yet published, so the ministry’s 2025 figures cannot be checked and the five-year "
          "windows may not match.",
          "We read NSO salient points, not the full NSO tables.",
          "The Commission’s 2023 early-warning report [8] is known to us only through summaries (◆).",
          "The publicservice.gov.mt version of the release could not be opened; we assume it matches the DOI text."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Ministry for the Environment, Energy and Public Cleanliness (19 Jan 2026). Malta records strong progress in "
          "waste separation. Press release PR260072en. (Read in full in a browser on 2 Oct 2026.)",
     "https://www.gov.mt/en/Government/DOI/Press%20Releases/Pages/2026/01/19/PR260072en.aspx"),
    ("2", "Malta records strong progress in waste separation (23 Jan 2026). publicservice.gov.mt. (Not read.)",
     "https://publicservice.gov.mt/en/news/malta-records-strong-progress-in-waste-separation"),
    ("3", "Eurostat. Recycling rate of municipal waste (cei_wm011); Municipal waste by waste management operations "
          "(env_wasmun); Recycling rate of packaging waste (cei_wm020). Retrieved 2 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/cei_wm011/default/table"),
    ("4", "National Statistics Office (2 Dec 2025). Municipal Waste: 2024. News Release 225/2025.",
     "https://nso.gov.mt/municipal-waste-2024/"),
    ("5", "National Statistics Office (17 Feb 2026). Solid Waste Management: 2024. News Release 023/2026.",
     "https://nso.gov.mt/solid-waste-management-2024/"),
    ("6", "European Commission (2025). Environmental Implementation Review 2025: Malta (country summary).",
     "https://op.europa.eu/webpub/env/eir-country-reports-summaries/en/malta.html"),
    ("7", "Directive (EU) 2018/851 of the European Parliament and of the Council of 30 May 2018 amending Directive "
          "2008/98/EC on waste. OJ L 150, 14.6.2018, p. 109. Articles 11(2) and 11a.",
     "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32018L0851"),
    ("8", "European Commission (2023). Early warning report, COM(2023) 304 final. ◆ Known through summaries; not "
          "read directly.", "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=COM%3A2023%3A304%3AFIN"),
    ("9", "Environment and Resources Authority (19 Feb 2025). NSO data reveals positive trends in sustainability and "
          "resource recovery.",
     "https://era.org.mt/press-releases/nso-data-reveals-positive-trends-in-sustainability-and-resource-recovery/"),
    ("10", "Wilansky J., Cao K. (2026). A comparison of municipal waste collection policies to optimize recycling "
           "rates: evidence from England and Wales. <i>Waste Management</i> 210:115258. "
           "doi:10.1016/j.wasman.2025.115258. (Abstract read.)", "https://doi.org/10.1016/j.wasman.2025.115258"),
    ("11", "MiŻien. Calculation script and outputs: tools/cc-004-report/calc.py; data/cc-004/checks.csv.", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "2 Oct 2026", "First issue. Draft pending right of reply from the Ministry for the "
                                         "Environment, Energy and Public Cleanliness and WasteServ.")])

build_report(Report(
    number="004", out=str(FIG / "report.pdf"), kicker="Statistics and EU law",
    title_lines=["More waste", "separated, but", "how much recycled?"],
    subtitle_lines=["Testing a public claim about waste in Malta", "against Eurostat, NSO and EU targets"],
    quote_lines=["“Malta continues to make strong progress", "in waste management.”"], quote_size=15,
    attribution="Ministry for the Environment, Energy and Public Cleanliness, press release PR260072en, 19 January 2026.",
    context="Minister Dalli: “our Long-Term Waste Management Plan is working”; 412 million kg diverted.",
    verdict="Not substantiated", verdict_note="Separation is up; the recycling outcome is not shown",
    footer_lines=["Version 1.0  ·  2 October 2026",
                  "Status: draft for right of reply (Environment Ministry; WasteServ)",
                  "Prepared from public sources, NSO and Eurostat data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Waste separation and recycling rates – Malta", version="1.0", date="2 October 2026",
    pdf_title="More waste separated, but how much recycled? Claim Check 004",
    pdf_subject="Tests the ministry's 'strong progress' waste claim against recycling and landfill rates",
    story=S))
