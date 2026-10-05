"""Claim Check 091 report. Run fetch.py, calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

LG = colors.HexColor("#8DB36B")
FIG = HERE / "out"
S = []

# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("The Occupational Health and Safety Authority (OHSA) tabled its 2025 annual report in parliament on 1 July 2026. "
        "MaltaToday reported that inspections “more than doubled”, that about 74% of construction sites met safety "
        "standards and that nine workers died. The report itself says that <b>“inspection numbers rising by a further "
        "152.8% in 2025”</b>, that <b>“Approximately 74% of sites were found to be adequately compliant with "
        "occupational health and safety requirements”</b> and that <b>“During 2025, nine fatal workplace accidents were "
        "recorded”</b>. We checked each against the report and public data.", lead)]
S.append(key_points([
    ("Inspections more than doubled: yes.",
     "OHSA's Table 14 gives 23,711 inspections in 2025 against 9,381 in 2024: 2.53 times as many, and 9.2 times the "
     "2,585 of 2023. The divisional figures add up to the total in both years."),
    ("The 74% is OHSA's own rating, accurately reported, but its base is unstated.",
     "Table 6 rates 74% of construction inspections “adequate”, 21% as ending in orders and 5% in stop-work orders. "
     "Applied to all 19,296 construction inspections, 5% would be about 965 stop-work orders; OHSA issued 526 in all "
     "sectors. So the percentages must rest on a subset the report does not define."),
    ("The nine deaths are confirmed.",
     "Table 1 and Table 5 agree: nine fatal accidents (three in construction, four in transport and storage, two in "
     "agriculture); four Maltese and five third-country nationals. OHSA's reports give five deaths in 2023 and five in "
     "2024, so 2025 is the highest of the three years."),
    ("Doubling the inspections did not coincide with fewer deaths.",
     "The claim does not say it would. Context: deaths rose from five to nine while inspections rose 2.5 times; with "
     "numbers this small, one year says little about cause."),
    ("Verdict: largely supported (moderate confidence).",
     "All three figures are in the report. “Met safety standards” is a plain-language reading of OHSA's “adequately "
     "compliant”, and the base of the 74% cannot be checked from the published tables."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("2.5x", GREEN, "Inspections in 2025 against 2024 (23,711 and 9,381)"),
             ("74%", AMBER, "Construction inspections rated adequate; base not stated"),
             ("9", RED, "Workplace deaths investigated in 2025 (five in 2024)"),
             ("26%", GREY, "Construction inspections ending in an order or stop-work order")]),
      Spacer(1, 4 * mm),
      up_down("Full support if OHSA published the base of Table 6 (inspections or distinct sites) and it reconciles with "
              "the 526 stop orders.",
              "A base showing that the 74% covers far fewer sites than the headline suggests, or a revision of the "
              "inspection counts."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the data show"),
          ("4", "Where the evidence points different ways"), ("5", "Testing the claim"),
          ("6", "Verdict and requests for evidence"), ("7", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The claim record locates the statement in a MaltaToday report of 1 July 2026 [1]. That article is the "
           "outlet's account of the Minister for Infrastructure, Planning and Works, Jonathan Attard, tabling OHSA's "
           "Annual Report 2025 in parliament. The wording “more than doubled” is the article's paraphrase of the "
           "minister's speech; the 74% and the nine deaths come from the report. We therefore read the primary text, "
           "the Annual Report 2025 on OHSA's website [2], in full for the relevant chapters (4 and 8) on 5 October "
           "2026, and quote it below. We also read the 2024 and 2023 reports [3] for earlier figures."))
S.append(std_table([
    [C("Source", cellh), C("What it says", cellh), C("Our access", cellh), C("Status", cellh)],
    [C("<b>OHSA</b>, Annual Report 2025, section 8.3, p. 67 [2]"),
     C("“…inspections declined by 41.1% in 2023. This was followed by a substantial 262.8% increase in 2024, with "
       "inspection numbers rising by a further 152.8% in 2025…”; Table 14: 23,711 inspections in 2025, 9,381 in 2024."),
     C("Full text read, 5 Oct 2026."), C("<b>The claim (inspections)</b>")],
    [C("<b>OHSA</b>, section 4.3.1, p. 42 [2]"),
     C("“Approximately 74% of sites were found to be adequately compliant with occupational health and safety "
       "requirements.” Table 6: adequate 74%, orders 21%, stop-work orders 5%."), C("Read."),
     C("<b>The claim (74%)</b>")],
    [C("<b>OHSA</b>, section 4.2.6, p. 41 [2]"),
     C("“During 2025, nine fatal workplace accidents were recorded, resulting in the loss of nine workers’ lives.” "
       "Four Maltese and five third-country nationals."), C("Read."), C("<b>The claim (deaths)</b>")],
    [C("<b>MaltaToday</b>, 1 Jul 2026 [1]"),
     C("Reports the minister's speech and the report; “more than doubled” is its paraphrase."),
     C("Read via Internet Archive copy (site 403)."), C("Locator")],
    [C("<b>OHSA</b>, Annual Reports 2023 and 2024 [3]"), C("Five fatal accidents in 2023; five in 2024; 9,381 inspections "
       "in 2024; a fatality rate of 1.22 per 100,000 workers in 2024."), C("Read."), C("Context")],
    [C("<b>Eurostat</b>, hsw_n2_02 and nama_10_pe [4]"), C("Fatal accidents at work and employment, Malta."),
     C("Downloaded 5 Oct 2026 (data/cc-091/)."), C("<b>Independent data</b>")],
], [38 * mm, 74 * mm, 36 * mm, 22 * mm]))
S.append(Spacer(1, 2 * mm))
S.append(P("<b>Who said what.</b> The statement belongs to OHSA's report; the minister presented it. The press report "
           "does not give the minister's own words for “more than doubled”, so we rate the report's figures, not the "
           "outlet's wording."))

# ================================================================== 2
S += [Spacer(1, 4 * mm), SectionHeading(2, "Method")]
S.append(P("<b>Question.</b> Do the three figures match the report, can they be reproduced from its tables, and "
           "what do independent data say about the deaths?"))
S.append(P("<b>Evidence.</b> We transcribed the report's tables into <i>data/cc-091/ohsa_annual_reports.csv</i> and "
           "recomputed each change and total with <i>calc.py</i> (output in <i>data/cc-091/checks.csv</i>). For deaths we "
           "downloaded Eurostat's fatal accidents at work (hsw_n2_02) and employment (nama_10_pe) for Malta. "
           "Regulator reports and official statistics are grade C in our scale. We found no independent count of "
           "inspections: OHSA is the only source for inspection volumes and compliance outcomes, so those figures are "
           "self-reported. <b>Verdicts</b> follow the five-point scale in Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(3, "What the data show"))
S.append(KeepTogether([fig(FIG / "fig1_inspections_deaths.png", width=CW * 0.98),
                       P("Figure 1. OHSA inspections 2021 to 2025 (left) and workplace deaths investigated, 2023 to 2025 (right).", cap)]))
S.append(P("Inspections fell from 4,387 in 2022 to 2,585 in 2023, then rose to 9,381 in 2024 and 23,711 in 2025. The "
           "report links this to a larger enforcement team, campaign-based inspections and the new Act 33 of 2024. "
           "Construction accounts for 19,296 of the 23,711 (81%, the report's “approximately 80%”) and rose 2.66 times "
           "from 7,263. The press report adds that the technical enforcement team grew 58% to 38 staff; we did not test "
           "that figure. Because 2023 was a low year, “more than doubled” is true on either comparison, but the "
           "comparison with 2024 is the fairer one."))
S.append(KeepTogether([fig(FIG / "fig2_construction.png", width=CW * 0.98),
                       P("Figure 2. Outcome of construction inspections in 2025 (left) and the share of applicable sites adequate "
                         "on selected safety features (right).", cap)]))
S.append(P("OHSA rated 74% of construction inspections adequately compliant, 21% as needing orders and 5% as needing "
           "stop-work orders. The weakest feature was the safe use of lifting machinery (65% adequate); falls "
           "protection and scaffolds were at 77% and 76%. The finishing stage of construction had the lowest overall "
           "compliance (60%). Nine people died: four in transport and storage, three in construction and two in "
           "agriculture. Eurostat's count for 2024 is four (OHSA: five; the two use different definitions) and "
           "its 2025 figure is not yet published. Dividing OHSA's counts by Eurostat's employment gives a crude rate "
           "of 1.6 per 100,000 in 2023, 1.5 in 2024 and 2.7 in 2025; OHSA's own 2024 rate is 1.22 (denominator not stated)."))

# ================================================================== 4
S.append(CondPageBreak(80 * mm))
S.append(SectionHeading(4, "Where the evidence points different ways"))
S.append(contested("Does “74% of sites met safety standards” describe what OHSA measured?", "BROADLY", AMBER,
                   "OHSA's wording is “adequately compliant”, and Table 6 reports 74% of construction inspections "
                   "in that class. The press summary compresses this to sites meeting standards.",
                   "The report does not say what “adequate” requires, and its base is unstated: the 5% stop-work share "
                   "would imply about 965 stop-work orders if applied to all 19,296 construction inspections, "
                   "against 526 stop orders issued in all sectors. One inspection is also not one site.",
                   "The 74% is faithfully reported. It is a regulator's own rating of an unspecified set of inspections, "
                   "and 26% needed orders or a stop. Falls protection (77%) and lifting machinery (65%) were weaker.",
                   label_a="THE REPORT", label_b="CAVEATS"))
S.append(Spacer(1, 3 * mm))
S.append(contested("Does a doubling of inspections mean safer workplaces?", "NOT CLAIMED, NOT SHOWN", AMBER,
                   "Inspections rose 2.5 times and OHSA reports its 2024 fatality rate as the lowest in recent years.",
                   "Deaths rose from five in 2024 to nine in 2025, and construction rated adequate in only 74% of "
                   "inspections. Counts this small, and a change in inspection mix, do not allow a causal reading either way.",
                   "The claim is about activity, not outcomes. We rate it as such and make no claim about whether "
                   "the inspections reduced harm.", label_a="ACTIVITY", label_b="OUTCOMES"))

# ================================================================== 5
S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(5, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> Inspections more than doubled in 2025"), C("OHSA [2]"),
     C("23,711 in 2025 against 9,381 in 2024: 2.53 times (+152.8%). Totals match the divisional tables."),
     verd("SUPPORTED", GREENC)],
    [C("<b>B.</b> Around 74% of construction sites met safety standards"), C("OHSA [2]"),
     C("Report: about 74% of sites “adequately compliant” (Table 6). Accurately reported, but “adequate” is "
       "undefined and the base is unstated; 26% needed orders or a stop."), verd("LARGELY SUPPORTED", LG)],
    [C("<b>C.</b> Nine workers died in 2025"), C("OHSA [2]"),
     C("Nine fatal accidents (Tables 1 and 5). Eurostat's 2025 figure not yet published; 2023 and 2024 agree "
       "closely with OHSA's counts."), verd("SUPPORTED", GREENC)],
], [42 * mm, 18 * mm, 76 * mm, 34 * mm], valign="MIDDLE"))

# ================================================================== 6
S += [Spacer(1, 6 * mm), SectionHeading(6, "Verdict and requests for evidence"),
      verdict_box("Largely supported", "The three figures are in OHSA's report and reproduce from its tables; the 74% is a "
                  "regulator's own rating with an unstated base. Confidence: moderate."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> Inspections rose 2.53-fold and the report's own arithmetic holds. The nine deaths agree across "
           "two tables and with the sector and nationality splits. The 74% is quoted accurately, but the report "
           "does not define the base or the standard, and a plain reading of Table 6 against Table 17 does not "
           "reconcile. That keeps the claim just short of Supported. Confidence is moderate because inspection and "
           "compliance data come only from OHSA."))
S.append(P("<b>What this verdict does not say.</b> It does not rate OHSA's enforcement or the safety of Maltese "
           "building sites. Counter-evidence in the claim record (a construction injury rate of 94 per 100,000 and "
           "more than half of deaths among migrant workers) concerns outcomes: the report confirms five of nine "
           "victims were third-country nationals, and we did not test the 94 figure."))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "From OHSA: the base of Table 6 (inspections or distinct sites; active sites only) and the definition of “adequate compliance”.",
    "From OHSA: a reconciliation of Table 6's 5% stop-work share with the 526 stop orders in Table 17.",
    "From OHSA or the NSO: 2025 fatality and injury rates by sector, with their denominators.",
]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag),
               P("Not needed for this verdict (maintainer rule of 5 October 2026: a reply is sought only for "
                 "<i>Not substantiated</i>, <i>Misleading</i> or <i>Contradicted</i>).", small)], bg=AMBER_PALE, bar=AMBER)]

# ================================================================== 7
S += [Spacer(1, 6 * mm), SectionHeading(7, "Limitations")]
for l in ["Inspection counts, compliance outcomes and orders are OHSA's own; we found no independent source for them.",
          "We did not read the minister's speech in the parliamentary record; the press report is the only account of it.",
          "Eurostat's 2025 fatal accident count was not available, and its definition differs from OHSA's.",
          "The crude fatality rates divide OHSA's counts by Eurostat's national-accounts employment; they are not OHSA's rates.",
          "We did not test the claim record's figure of 94 injuries per 100,000 in construction, or the press report's "
          "figures on staffing and helpline calls."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Zammit, J. (1 July 2026). Nine workers die on the job in 2025 as OHSA inspections more than double. "
          "MaltaToday. (Read via Internet Archive copy.) ◆ second-hand locator.",
     "https://www.maltatoday.com.mt/news/national/142928/nine_workers_die_on_the_job_in_2025_as_ohsa_inspections_more_than_double"),
    ("2", "Occupational Health and Safety Authority (2026). Annual Report 2025. Sections 4.2, 4.3, 8.3; Tables 1, 5, 6, 9, "
          "14, 16, 17, 18.", "https://ohsa.mt/sites/default/files/2026-05/AR-OHSA-2025.pdf"),
    ("3", "Occupational Health and Safety Authority. Annual Reports 2024 and 2023.",
     "https://www.ohsa.mt/sites/default/files/2025-05/AR-OHSA-2024.pdf"),
    ("4", "Eurostat. Fatal accidents at work by NACE Rev. 2 activity (hsw_n2_02), updated 25 Sep 2026; Population and "
          "employment, national accounts (nama_10_pe), updated 2 Oct 2026; retrieved 5 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/hsw_n2_02/default/table"),
    ("5", "MiŻien. Calculation script and outputs: tools/cc-091-report/calc.py; data/cc-091/checks.csv.", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "5 Oct 2026", "First issue. Verdict Largely supported (moderate confidence); no right of reply needed.")])

build_report(Report(
    number="091", out=str(FIG / "report.pdf"), kicker="Workplace safety",
    title_lines=["OHSA inspections", "doubled, 74% of", "sites compliant?"],
    subtitle_lines=["Testing the Occupational Health and Safety", "Authority's 2025 annual report"],
    quote_lines=["“Approximately 74% of sites were found to be adequately", "compliant with occupational health and safety",
                 "requirements.”"], quote_size=14,
    attribution="OHSA, Annual Report 2025, section 4.3.1, tabled 1 July 2026.",
    context="The same report: inspections rose 152.8% in 2025 and “nine fatal workplace accidents were recorded”.",
    verdict="Largely supported", verdict_note="Figures match the report; the 74% has no stated base",
    footer_lines=["Version 1.0  ·  5 October 2026", "Status: no right of reply needed",
                  "Prepared from public sources and Eurostat data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="OHSA Annual Report 2025 – inspections, compliance, deaths", version="1.0", date="5 October 2026",
    status_note="no right of reply needed",
    pdf_title="OHSA inspections doubled, 74% of sites compliant? Claim Check 091",
    pdf_subject="Tests the OHSA Annual Report 2025 figures on inspections, construction compliance and workplace deaths",
    story=S))
