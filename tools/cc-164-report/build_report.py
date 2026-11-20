"""Claim Check 164 report. Run calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("In his Budget 2027 speech on 26 October 2026, the Minister for Finance, Clyde Caruana, announced that from 1 "
        "January the eco-contribution would be €8 a night (up to €64 a person) in collective accommodation and €10 a night "
        "(up to €80) in short lets. He added, in Maltese: <b>“Id-dħul minn dawn ir-reviżjonijiet mistenni jkun madwar €182 "
        "miljun”</b> (“The revenue from these revisions is expected to be around €182 million”). Outlets reported "
        "different totals. We read the speech and estimated the yield from official guest-night data.", lead)]
S.append(key_points([
    ("The rates and the €182 million are in the speech.",
     "Printed page 27 gives €8 and €10 a night, caps of €64 and €80, and “madwar €182 miljun”. Adults under 18 pay "
     "nothing, and English-language schools will be exempt."),
    ("€182 million is a plausible order of magnitude.",
     "Applying the new rates to the NSO’s 2025 guest nights, adults only, gives about €176 million before the 8-night "
     "caps. Scaled to the 28 million nights the speech expects in 2026, it is about €193 million."),
    ("It probably means extra revenue.",
     "As reported from the Budget Estimates, eco-contribution revenue is €213 million in 2027 against €21 million in "
     "2026. The difference, €192 million, includes the new cruise and Comino fees. We could not read the Estimates "
     "ourselves."),
    ("The “€80 million” figure is not the eco-contribution.",
     "In the speech, about €80 million is the expected yield of the higher work-permit fees."),
    ("Verdict: largely supported (moderate confidence).",
     "The wording and rates are exact, and the projection is consistent with the data. It remains a forecast, and the "
     "speech does not say whether €182 million is total or additional revenue."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("€182m", GREEN, "projected revenue from the revisions (speech, p. 27)"),
             ("€176–193m", GREEN, "our rough estimate before caps, from NSO nights"),
             ("22.5m", AMBER, "nights in collective and other rented accommodation, 2025"),
             ("€80m", GREY, "work-permit fees, not the eco-contribution")]),
      Spacer(1, 4 * mm),
      up_down("The Estimates 2027 revenue line and the Ministry’s method, confirming the €182 million as additional "
              "accommodation revenue.",
              "Estimates or outturn showing the accommodation contribution yielding well below €182 million."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "Estimating the yield"),
          ("4", "Testing the claim"), ("5", "Verdict"), ("6", "Limitations")])
S.append(PageBreak())

S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The Budget speech is in Maltese. We read it from the maintainer’s copy of the Ministry for Finance PDF "
           "(80 pages; finance.gov.mt refuses scripts) [1]. The eco-contribution passage is on printed pages 26–27. Newsbook, "
           "TVMnews, Lovin Malta and The Malta Independent reported the rates and €182 million in their own words [2, 3]. "
           "A search summary of MaltaToday’s live blog gave about €80 million. The live blog itself says the higher ecotax "
           "is “expected to generate €214 million in 2027”, and the speech gives €80 million for work-permit fees [1, 4]. "
           "Amphora Media reports €213 million from the Budget Estimates (CC-165) [5]."))
S.append(std_table([
    [C("Source", cellh), C("What it says", cellh), C("Our access", cellh), C("Status", cellh)],
    [C("<b>Clyde Caruana</b>, Budget Speech 2027, pp. 26–27 [1]"),
     C("€8 / €10 a night, caps €64 / €80; “Id-dħul minn dawn ir-reviżjonijiet mistenni jkun madwar €182 miljun.”"),
     C("Maintainer’s copy; read in full."), C("<b>The claim</b>")],
    [C("<b>Newsbook, TVMnews, Lovin Malta, Independent</b> [2, 3]"), C("Same rates; €182 million."),
     C("Read."), C("<b>Reports</b>")],
    [C("<b>MaltaToday</b> live blog [4]"), C("“€214 million in 2027” (editorial summary)."),
     C("Maintainer’s copy."), C("<b>Report</b>")],
    [C("<b>NSO</b>, Inbound Tourism: December 2025 [6]"), C("Guest nights by accommodation type and tourists by age."),
     C("xlsx read in a browser."), C("<b>Primary data</b>")],
], [38 * mm, 66 * mm, 40 * mm, 26 * mm]))

S += [Spacer(1, 4 * mm), SectionHeading(2, "Method")]
S.append(P("A revenue projection cannot be checked before the year is over, but it can be tested for plausibility. In "
           "<i>tools/cc-164-report/calc.py</i> we multiplied the NSO’s 2025 nights in collective accommodation by €8 and "
           "in “other rented” accommodation (private rentals, the nearest category to short lets) by €10. We removed an "
           "assumed under-18 share of 11% (half of the NSO’s 0–24 age group) and scaled to the 28 million nights the speech "
           "expects in 2026. The 8-night caps and the school exemption are not modelled, because the NSO does not publish "
           "stays longer than 7 nights separately. Outputs are in <i>data/cc-164/checks.csv</i>. NSO data are grade C; the "
           "Estimates figures are second-hand (◆)."))

S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(3, "Estimating the yield"))
S.append(fig(FIG / "fig1_yield.png", width=CW * 0.98))
S.append(P("Figure 1. The speech’s projection beside our rough estimates and the Estimates figures as reported.", cap))
S.append(P("In 2025 tourists spent 13.5 million nights in collective accommodation and 9.0 million in other rented "
           "accommodation [6]. At the new rates, before caps and for all ages, that is €198 million. For adults only it is "
           "about €176 million, and scaled to 2026 night volumes about €193 million. The caps bite only on stays longer "
           "than eight nights. In 2025, 38% of tourists stayed seven nights or more, and the average stay was 6.3 nights, "
           "so the caps lower the figure without changing its order of magnitude."))
S.append(P("The speech does not say whether €182 million is the total or the increase. The Estimates, as Amphora Media "
           "reports them, put eco-contribution revenue at €213 million in 2027 against €21 million in 2026 [5]. The "
           "€192 million difference also includes a new €10 fee for cruise passengers and €5 for Comino visitors. Both "
           "readings fit our estimate, but the reported Estimates point to €182 million being extra revenue."))

S.append(CondPageBreak(70 * mm))
S.append(SectionHeading(4, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> €8 a night (cap €64) in collective accommodation and €10 (cap €80) in short lets from 1 Jan 2027"),
     C("Caruana [1]"), C("In the speech, p. 27, exactly."), verd("ACCURATE", GREENC)],
    [C("<b>B.</b> Revenue from the revisions “around €182 million”"), C("Caruana [1]"),
     C("Our estimate from NSO nights is €176–193 million before caps. The reported Estimates fit it as extra revenue."),
     verd("PLAUSIBLE", GREENC)],
    [C("<b>C.</b> About €80 million (as summarised for MaltaToday)"), C("Search summary"),
     C("In the speech €80 million is the work-permit fee yield; MaltaToday’s own blog says €214 million."),
     verd("MIX-UP", AMBER)],
], [42 * mm, 26 * mm, 68 * mm, 34 * mm], valign="MIDDLE"))

S += [Spacer(1, 6 * mm), SectionHeading(5, "Verdict"),
      verdict_box("Largely supported", "The rates and the €182 million are the Minister’s words, and the figure is "
                  "consistent with guest-night data. It is a forecast, and the speech does not say if it is total or "
                  "additional. Confidence: moderate."), Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> Everything checkable is right, and a simple estimate lands near €182 million. The caveats are "
           "that the figure is a projection, and the speech leaves its basis unstated. <b>What this verdict does not "
           "say.</b> It does not judge whether the rise is good policy, or how the money will be spent (CC-165, CC-166)."))
S.append(P("<b>Pledge label: not yet due (as of 17 November 2026).</b> The new rates are a budget measure due from 1 "
           "January 2027. We will revisit them when they are in force and when 2027 receipts are published.", small))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list(["From the Ministry for Finance: whether €182 million is total or additional revenue, the guest "
                        "nights assumed, and the Estimates line for the accommodation eco-contribution."]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag),
               P("Not needed for this verdict (maintainer rule of 5 October 2026).", small)], bg=AMBER_PALE, bar=AMBER)]
S += [Spacer(1, 6 * mm), SectionHeading(6, "Limitations")]
for l in ["Our estimate ignores the 8-night caps, the English-language school exemption, compliance gaps and 2027 growth.",
          "The under-18 share is an assumption (half of the NSO’s 0–24 group).",
          "The Budget Estimates were not read; their figures are second-hand via Amphora Media.",
          "The previous rate (€1.50 a night, as outlets report) is not stated in the speech and was not checked."]:
    S.append(P("• " + l, bul))
S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Ministry for Finance. Diskors tal-Baġit 2027 (Budget Speech 2027), 26 October 2026, pp. 26–27 (maintainer copy).",
     "https://finance.gov.mt/"),
    ("2", "Newsbook. Budget 2027: Eco-tax rises to €8 a night for hotel guests and €10 for short-lets, 26 October 2026.",
     "https://newsbook.com.mt/en/budget-2027-eco-tax-rises-to-e8-a-night-for-hotel-guests-and-e10-for-short-lets/"),
    ("3", "The Malta Independent. Budget 2027: Higher eco-contributions for tourists staying in Malta, visiting Comino, "
          "26 October 2026 (maintainer copy).",
     "https://www.independent.com.mt/articles/2026-10-26/local-news/Budget-2027-Higher-eco-contributions-for-tourists-staying-in-Malta-visiting-Comino-6736294107"),
    ("4", "MaltaToday. Budget 2027 live coverage, 26 October 2026 (maintainer copy).",
     "https://www.maltatoday.com.mt/news/budget-2027/145265/live__budget_2027_follow_the_announcements_analysis_and_measures_as_they_unfold"),
    ("5", "Amphora Media. Malta Will Charge Tourists €213 Million; Most Will Be Spent On Marketing Malta To More Tourists, "
          "13 November 2026 (second-hand for the Estimates).",
     "https://www.amphora.media/2026/11/malta-will-charge-tourists-e213-million-most-will-be-spent-on-marketing-malta-to-more-tourists"),
    ("6", "NSO. Inbound Tourism: December 2025, NR 020/2026, Tables 1–2 (read in a browser 17 Nov 2026).",
     "https://nso.gov.mt/inbound-tourism-december-2025/"),
    ("7", "MiŻien. Data and script: data/cc-164/; tools/cc-164-report/calc.py. Related: CC-165, CC-166.", ""),
])
S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.")
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "17 Nov 2026", "First issue. Verdict Largely supported (moderate confidence); no right of "
                    "reply needed.")])

build_report(Report(
    number="164", out=str(FIG / "report.pdf"), kicker="Tourism",
    title_lines=["€182 million", "from tourists?"],
    subtitle_lines=["Testing the Budget 2027 eco-contribution", "rates and revenue projection"],
    quote_lines=["“Id-dħul minn dawn ir-reviżjonijiet", "mistenni jkun madwar €182 miljun.”"], quote_size=15,
    attribution="Clyde Caruana, Minister for Finance, Budget Speech 2027, 26 October 2026.",
    context="“The revenue from these revisions is expected to be around €182 million.”",
    verdict="Largely supported", verdict_note="Rates exact; projection plausible from guest nights",
    footer_lines=["Version 1.0  ·  17 November 2026", "Status: no right of reply needed",
                  "Prepared from public sources and open data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Eco-contribution – Budget 2027", version="1.0", date="17 November 2026",
    pdf_title="€182 million from tourists? Claim Check 164",
    pdf_subject="Tests the Budget 2027 eco-contribution rates and the EUR 182 million revenue projection",
    pledge_label="Not yet due", story=S))
