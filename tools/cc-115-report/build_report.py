"""Claim Check 115 report. Run fetch.py, calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("In its proposals for the 2026–2031 legislature (“LEAD”, 14 May 2026), the Malta Chamber of Commerce, "
        "Enterprise and Industry wrote: <b>“In 2025, traffic congestion imposed an estimated cost of €770 million on "
        "the Maltese economy, equivalent to 3.4% of GDP.”</b> We traced the figure to its source and recomputed the "
        "share of GDP.", lead)]
S.append(key_points([
    ("The €770 million is the government’s own figure, cited correctly.",
     "The Chamber’s footnote points to the National Transport Master Plan 2030 (January 2026), which says the cost of "
     "congestion is projected to reach €917 million a year by 2030, “up from €770 million in 2025”. The European "
     "Commission’s 2026 Country Report repeats the same figures from the same plan."),
    ("But no published method stands behind the 2025 figure.",
     "The plan gives no calculation for 2025. Its appraisal annex models 2030 and 2060 only, and two of its tables "
     "(lost time and idle fuel) carry identical numbers. We could not reproduce or test the €770 million."),
    ("“3.4% of GDP” does not reproduce.",
     "€770 million is 3.1% of Malta’s 2025 GDP at current prices (€24.7 billion, Eurostat), the like-for-like "
     "comparison. 3.4% would need GDP of €22.6 billion; 2024 nominal GDP gives 3.3%, and the Chamber’s own real GDP "
     "figure gives 3.8%."),
    ("Verdict: not substantiated (moderate confidence).",
     "A cost of this order may well be real, but the central figure has no published derivation, and the GDP share "
     "is stated higher than the data give. This is not a finding that the Chamber misreported its source: it "
     "reported it accurately."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(2), Spacer(1, 3 * mm),
      tiles([("€770m", AMBER, "Congestion cost for 2025 in the government’s transport plan: no method published"),
             ("3.1%", GREEN, "€770m as a share of 2025 GDP at current prices (claim: 3.4%)"),
             ("€917m", GREY, "The plan’s projection for 2030 if nothing changes (+19%)"),
             ("€195m", GREY, "Environmental costs a year, excluded from both figures")]),
      Spacer(1, 4 * mm),
      up_down("Publication of how the €770 million was estimated (lost hours, value of time, operating costs, base "
              "year) and of the GDP figure behind 3.4%.",
              "Evidence that the plan’s 2025 figure was not an estimate for 2025 at all, or a method showing it is "
              "much lower."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the data show"),
          ("4", "Where the evidence points different ways"), ("5", "Testing the claim"),
          ("6", "Verdict and requests for evidence"), ("7", "Limitations")])
S.append(PageBreak())

S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The sentence is on the third page of “LEAD – The Malta Chamber Proposals for the 2026–2031 Legislature” "
           "[1], published on the Chamber’s website with a press release on 14 May 2026 and read in full on 5 October "
           "2026. Its footnote 2 cites “Transport Master Plan 2030 (Page 124)”. Lovin Malta reported the proposals the "
           "same day in its own words [2]. The cited plan is the <i>National Transport Master Plan 2030</i> (document "
           "title “National Transport Strategy 2025 14 JAN26 (REV)”) [3]; the government site refuses automated "
           "access, so we read it from an Internet Archive copy of 21 March 2026."))
S.append(std_table([
    [C("Source", cellh), C("What it says", cellh), C("Our access", cellh), C("Status", cellh)],
    [C("<b>Malta Chamber</b>, LEAD proposals, 14 May 2026 [1]"),
     C("“In 2025, traffic congestion imposed an estimated cost of €770 million on the Maltese economy, equivalent to "
       "3.4% of GDP. This figure captures lost productivity, higher operating costs for firms, and the misallocation "
       "of time and resources.”"), C("Full PDF read, 5 Oct 2026."), C("<b>The claim</b>")],
    [C("<b>National Transport Master Plan 2030</b>, Jan 2026, p. 124 [3]"),
     C("“By 2030, the economic cost of traffic congestion … is projected to reach €917 million per year, up from €770 "
       "million in 2025, unless effective measures are put in place.” Footnote: excludes environmental costs "
       "(€195.4 million a year)."), C("Full PDF read (Internet Archive copy, 21 Mar 2026)."), C("<b>The source</b>")],
    [C("<b>European Commission</b>, 2026 Country Report, p. 16 [4]"), C("Same €770m and €917m, citing the plan."),
     C("Read."), C("Context")],
    [C("<b>Eurostat</b>, nama_10_gdp [5]"), C("Malta’s GDP, current prices and chain-linked volumes."),
     C("Downloaded 5 Oct 2026."), C("<b>Primary data</b>")],
], [38 * mm, 74 * mm, 36 * mm, 22 * mm]))

S += [Spacer(1, 4 * mm), SectionHeading(2, "Method")]
S.append(P("<b>Question.</b> Where does the €770 million come from, can it be tested, and is it 3.4% of GDP?"))
S.append(P("<b>Evidence.</b> We read the Chamber’s document and the plan it cites, searched the plan for the derivation "
           "of the 2025 figure, and recorded the plan’s figures in <i>data/cc-115/congestion_estimates.csv</i>. We "
           "downloaded Malta’s GDP from Eurostat (nama_10_gdp, updated 2 October 2026) and computed the share on "
           "each basis (<i>tools/cc-115-report/calc.py</i>; outputs in <i>data/cc-115/checks.csv</i>). A cost in euros of "
           "2025 is compared with GDP in euros of 2025, i.e. at current prices; the other ratios are shown because the "
           "Chamber’s document uses real GDP elsewhere (its €11.34 billion for 2015 matches Eurostat’s chain-linked "
           "series at 2020 prices)."))
S.append(P("<b>Grades.</b> Official statistics and the government plan are grade C; the plan’s 2025 figure is an "
           "assertion without a published method (D) until its derivation is published. <b>Verdicts</b> follow the "
           "five-point scale in Appendix A."))

S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(3, "What the data show"))
S.append(fig(FIG / "fig1_share.png", width=CW * 0.98))
S.append(P("Figure 1. Left: €770 million as a share of Malta’s GDP on four bases. Right: the plan’s figures for 2025 "
           "and 2030, with the environmental costs it excludes.", cap))
S.append(P("Malta’s GDP in 2025 was €24,664 million at current prices; €770 million is 3.12% of it. Against 2024 GDP "
           "(€23,079 million) it is 3.34%, which would round to 3.3%. Against real GDP in 2020 prices it is 3.85%, and "
           "against the Chamber’s own real GDP figure (€20.40 billion) 3.77%. None of the published series gives 3.4%; "
           "that would need GDP of about €22.6 billion."))
S.append(P("In the plan, the only derivation we found is in the appraisal annex (pp. 218–221), which values lost "
           "time with HEATCO unit values for 2030 (11.04 million hours a year, €248 million) and 2060. It does not "
           "cover 2025, and the plan does not show how the €770 million or the €917 million is assembled."))

S.append(CondPageBreak(80 * mm))
S.append(SectionHeading(4, "Where the evidence points different ways"))
S.append(contested("Is a congestion cost of this size plausible?", "UNTESTED", AMBER,
                   "The government’s plan and the European Commission both use the figure. Engineer Marco Cremona "
                   "estimated a higher cost, €1.13 billion a year, in a presentation reported by the Malta News Agency "
                   "on 3 June 2026 ◆.",
                   "No published calculation stands behind €770 million for 2025. The plan’s own appraisal models "
                   "other years and has two tables with identical numbers. Cremona’s estimate uses its own assumptions "
                   "(60.8 million hours at €10 an hour plus fuel ◆), which we have not read first-hand.",
                   "Estimates of this order exist from more than one source, which makes a large cost plausible. "
                   "Plausible is not tested: without the method the figure cannot be checked.",
                   label_a="FOR", label_b="AGAINST"))

S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(5, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> Traffic congestion cost the economy an estimated €770 million in 2025"), C("Malta Chamber [1]"),
     C("Accurately cited from the National Transport Master Plan 2030, p. 124. The plan publishes no derivation for "
       "2025, so the figure cannot be tested."), verd("NOT TESTABLE", ORANGE)],
    [C("<b>B.</b> …equivalent to 3.4% of GDP"), C("Malta Chamber [1]"),
     C("3.12% of 2025 GDP at current prices; 3.34% of 2024 GDP; 3.8–3.9% of real GDP. No published series gives 3.4%."),
     verd("OVERSTATED", AMBER)],
], [42 * mm, 18 * mm, 76 * mm, 34 * mm], valign="MIDDLE"))

S += [Spacer(1, 6 * mm), SectionHeading(6, "Verdict and requests for evidence"),
      verdict_box("Not substantiated", "The figure is the government’s, cited correctly, but has no published method; "
                  "the GDP share does not reproduce. Confidence: moderate."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> Our scale rates a claim <i>Not substantiated</i> when its central figure has no evidence that "
           "can be checked. The €770 million comes from an official plan but without a published calculation, and the "
           "3.4% does not match Malta’s GDP on the like-for-like basis (3.1%). Confidence is moderate because the "
           "plan’s authors may hold a calculation we have not seen."))
S.append(P("<b>What this verdict does not say.</b> It does not say congestion is cheap, that the figure is wrong, or "
           "that the Chamber misreported its source: the Chamber quoted the government’s plan and gave the page. The "
           "missing piece is the plan’s method. A fuller sentence would read: <i>“The government’s transport plan puts "
           "the cost of congestion at about €770 million in 2025, roughly 3% of GDP, without publishing how it was "
           "estimated.”</i>"))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "From the Ministry for Transport and Transport Malta: the calculation behind €770 million (2025) and €917 million "
    "(2030): hours lost, values of time, operating costs and base year.",
    "From the Malta Chamber: the GDP figure used for “3.4% of GDP”.",
]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag),
               P("Pending. Under the maintainer’s rule of 5 October 2026 a reply is sought for <i>Not substantiated</i> "
                 "verdicts. The maintainer will contact the Malta Chamber; this report will be updated with any "
                 "response.", small)], bg=AMBER_PALE, bar=AMBER)]
S += [Spacer(1, 6 * mm), SectionHeading(7, "Limitations")]
for l in ["We read the government’s plan from an Internet Archive copy; the live file refuses automated access.",
          "We searched the plan’s text for the derivation; a calculation could exist in an annex or model report not "
          "published with it.",
          "The Cremona estimate is known to us only from the claim record’s summary of a news report (second-hand, ◆).",
          "GDP figures are revised; the share would differ slightly with an earlier vintage."]:
    S.append(P("• " + l, bul))
S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "The Malta Chamber of Commerce, Enterprise and Industry (14 May 2026). LEAD – The Malta Chamber Proposals for "
          "the 2026–2031 Legislature. Page 3 and footnote 2.",
     "https://maltachamber.org.mt/wp-content/uploads/2026/05/LEAD-The-Malta-Chamber-Proposals-for-2026-2031-Legislature.pdf"),
    ("2", "Lovin Malta (14 May 2026). Chamber tells political parties: Malta must address productivity crisis or face "
          "structural decline.",
     "https://lovinmalta.com/news/general-election-2026/chamber-tells-political-parties-malta-must-address-productivity-crisis-or-face-structural-decline/"),
    ("3", "Ministry for Transport / Transport Malta (January 2026). National Transport Master Plan 2030 (“National "
          "Transport Strategy 2025 14 JAN26 (REV)”). P. 124 and appraisal annex pp. 218–221. Internet Archive copy of "
          "21 Mar 2026.", "https://infrastructure.gov.mt/wp-content/uploads/2026/01/NATIONAL-TRANSPORT-MASTERPLAN-2030.pdf"),
    ("4", "European Commission (3 June 2026). 2026 Country Report – Malta. SWD(2026) 218 final, footnotes 9–10.",
     "https://data.consilium.europa.eu/doc/document/ST-10135-2026-ADD-1/en/pdf"),
    ("5", "Eurostat. GDP and main components (nama_10_gdp), updated 2 Oct 2026, retrieved 5 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/nama_10_gdp/default/table"),
    ("6", "Malta News Agency (3 June 2026), report of Marco Cremona’s presentation to Momentum (via the CC-115 claim "
          "record; not read first-hand ◆).", ""),
    ("7", "MiŻien. Calculation script and outputs: tools/cc-115-report/calc.py; data/cc-115/.", ""),
])
S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "5 Oct 2026", "First issue. Verdict Not substantiated (moderate confidence); pending right of reply.")])

build_report(Report(
    number="115", out=str(FIG / "report.pdf"), kicker="Economics and transport",
    title_lines=["Congestion cost", "€770 million,", "3.4% of GDP?"],
    subtitle_lines=["Tracing the Malta Chamber’s figure to the government’s", "transport plan, and recomputing the share of GDP"],
    quote_lines=["“In 2025, traffic congestion imposed an estimated cost of", "€770 million on the Maltese economy, equivalent to",
                 "3.4% of GDP.”"], quote_size=14,
    attribution="The Malta Chamber of Commerce, Enterprise and Industry, LEAD proposals, 14 May 2026.",
    context="Proposals for the 2026–2031 legislature; footnote: Transport Master Plan 2030, p. 124.",
    verdict="Not substantiated", verdict_note="Cited correctly, but no published method; 3.4% is 3.1%",
    footer_lines=["Version 1.0  ·  5 October 2026", "Status: draft, pending right of reply",
                  "Prepared from public sources and Eurostat data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Congestion cost – Malta Chamber LEAD proposals 2026", version="1.0", date="5 October 2026",
    status_note="pending right of reply",
    pdf_title="Congestion cost €770 million, 3.4% of GDP? Claim Check 115",
    pdf_subject="Tests the Malta Chamber's figure for the cost of traffic congestion in 2025",
    story=S))
