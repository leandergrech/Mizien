"""Claim Check 125 report. Run calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
NYD = PLEDGE_COLS[1]          # "Not yet due" in the site's pledge palette
verd = lambda t, c: chip(t, c, w=29 * mm)
S = []
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("On 29 July 2026 the European Commission announced that it had endorsed Malta’s Social Climate Plan. Its news "
        "article says the plan “will mobilise EUR 60.6 million”, of which EUR 45.4 million comes from the Social Climate "
        "Fund, will “support renovations of social housing apartments to reduce primary energy use by 60%”, and is, in the "
        "Commission’s view, “a strong and lasting response” to the new carbon price on fuels in buildings and road "
        "transport (ETS2). We read the Commission’s decision, its annexes and Malta’s plan.", lead)]
S.append(key_points([
    ("The money is exactly as stated.",
     "The decision sets total costs at EUR 60,599,503, the Fund’s share at EUR 45,410,023 and Malta’s at EUR 15,189,480 "
     "(25.07%). The 16 milestone and target payouts in Annex II add up to the Fund share to the euro."),
    ("The 60% is a definition, not a monitored target.",
     "The plan says a 60% cut in primary energy use “can also be considered a deep renovation”. Annex II, which "
     "controls payment, asks for 236 social housing units improved to at least energy class B. No 60% indicator and no "
     "pre-renovation baseline is published."),
    ("The scale is modest and mostly in the future.",
     "236 units are about 4.7% of the 5,031 units the plan says the Housing Authority manages. The first milestone falls "
     "due in the first quarter of 2027; payments follow results, not spending."),
    ("‘Strong and lasting’ is the Commission’s assessment.",
     "The decision’s own legal finding is that the plan is “an adequate response”. We report it and do not rate it."),
    ("Verdict: largely supported (moderate confidence); pledge label: not yet due.",
     "The figures are confirmed; the 60% is real but is not what the plan will be paid against."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(1), Spacer(1, 3 * mm),
      tiles([("EUR 60.6m", GREEN, "Total cost of the plan, 2026–2032 (60,599,503), as stated"),
             ("25.07%", GREEN, "Malta’s share of the cost (claim: ‘at least 25%’)"),
             ("236", AMBER, "Social housing units to be retrofitted by 2032: 4.7% of 5,031"),
             ("Q1 2027", GREY, "First milestone due; no payout milestone has fallen due yet")]),
      Spacer(1, 4 * mm),
      up_down("None for the figures, which are confirmed. A ‘Supported’ verdict needs the Housing Authority’s project "
              "documents showing that the renovations are designed and certified to a 60% primary-energy cut against a stated "
              "starting point.",
              "Project documents or energy performance certificates showing the retrofits do not reach that level, or a "
              "revision of the plan that lowers the amounts (the plan itself shows EUR 50.9 million if the ETS2 price brake "
              "applies)."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "The money"),
          ("4", "The 60% and the retrofit target"), ("5", "‘Strong and lasting’, and what is not in the plan"),
          ("6", "Testing the claim"), ("7", "Verdict, pledge and requests for evidence"), ("8", "Limitations")])
S.append(PageBreak())

S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The claim is the Commission’s news article of 29 July 2026 [1], read in full on 20 October 2026. It says: "))
S.append(P("“Starting this year until 2032, the Maltese Social Climate Plan will mobilise EUR 60.6 million. EUR 45.4 million "
           "will be made available from the Social Climate Fund, while Malta will cover the remainder, representing at least "
           "25% of the total costs of the plan.” The plan “will … support renovations of social housing apartments to reduce "
           "primary energy use by 60%” and “equip social housing estates with renewable energy systems”. “The Commission "
           "considers that the Maltese plan gives a strong and lasting response to the new carbon pricing system for fuels in "
           "buildings and road transport sector in the EU (known as ETS2).”", bul))
S.append(P("The article links the legal act and the plan. We read both."))
S.append(std_table([
    [C("Source", cellh), C("What it says", cellh), C("Our access", cellh), C("Status", cellh)],
    [C("<b>European Commission</b>, DG EMPL news article, 29 Jul 2026 [1]"),
     C("The funding split, the 60% and the ‘strong and lasting’ assessment."),
     C("Read in full, 20 Oct 2026."), C("<b>The claim</b>")],
    [C("<b>Commission Implementing Decision</b> C(2026) 5266, 29 Jul 2026, Articles 1–2, recitals, Annexes I–IV [2]"),
     C("Total cost, Fund and national amounts; 16 milestones and targets with payout values; annual allocations."),
     C("Read in full; copy in the repository."), C("<b>Primary, binding</b>")],
    [C("<b>Malta’s Social Climate Plan</b>, adopted version, 156 pp. [3]"),
     C("Measures, costs, the 60% passage (p. 34), impact estimates (p. 127)."),
     C("Relevant sections read; not every page."), C("<b>Primary</b>")],
    [C("<b>Eurostat</b>, ilc_mdes01 [4]"),
     C("Share of people unable to keep their home warm, Malta and EU-27."), C("Retrieved, 20 Oct 2026."),
     C("<b>Context</b>")],
], [42 * mm, 66 * mm, 38 * mm, 24 * mm]))

S += [Spacer(1, 4 * mm), SectionHeading(2, "Method")]
S.append(P("<b>Question.</b> Are the amounts, the 60% and the assessment as the Commission’s own documents state them, and what "
           "will the plan be paid against? <b>Evidence.</b> We recomputed every figure from the decision and plan "
           "(<i>tools/cc-125-report/calc.py</i>; inputs in <i>data/cc-125/payouts.csv</i> and <i>plan_figures.csv</i>; results in "
           "<i>checks.csv</i>). We searched the plan’s text for the 60% and for any pre-renovation baseline "
           "(<i>literature/CC-125/notes.md</i>). <b>Grades.</b> The decision and plan are official documents (grade C); "
           "there is no peer-reviewed literature on a plan not yet implemented. Nothing here measures energy savings: "
           "none has yet been achieved. The Commission’s guidance on the Fund, which the plan cites for the 60%, was not read."))

S.append(CondPageBreak(70 * mm))
S.append(SectionHeading(3, "The money"))
S.append(P("The decision’s recitals state that “the estimated total costs of the Plan as indicated by Malta is EUR 60 599 503” "
           "and “the national contribution … is EUR 15 189 480”; Article 2 sets the Fund’s maximum allocation at "
           "EUR 45 410 023 [2]. The three numbers are consistent: 45,410,023 + 15,189,480 = 60,599,503, and Malta’s share "
           "is 25.07% of the total. The plan’s component costs (buildings EUR 31.73 million, road transport EUR 27.68 million, "
           "technical assistance EUR 1.19 million [3]) also sum to the total."))
S.append(P("<b>How the money is paid.</b> The Fund pays only when milestones or targets are met. Annex II lists 16, "
           "each with a payout value, and the values sum to EUR 45,410,023, the full Fund share. About 43% of the Fund money "
           "(EUR 19.5 million) is tied to results due by the end of 2029, and the rest to 2030–2032 (Figure 1). Annex III adds "
           "a condition: the designated audit body must give a positive opinion on the internal control system "
           "(milestone due in the fourth quarter of 2026), because the Commission found weaknesses there before the first payment."))
S.append(fig(FIG / "fig1_payouts.png", width=CW * 0.97))
S.append(P("Figure 1. The Fund’s EUR 45.4 million by the year in which each milestone or target is due (Annex II). The "
           "money is released as results are reached; the EUR 60.6 million is the cost of the whole programme.", cap))
S.append(P("<b>A caveat the article does not mention.</b> The plan’s financing table also shows a lower alternative “in case of "
           "application of Article 30k” of the ETS directive (a provision of the ETS directive that the plan does not explain in this table, and that we did not read): "
           "total cost EUR 50,878,285, Fund EUR 38,130,023, national EUR 12,748,262 [3, p. 117]. The EUR 60.6 million is the "
           "baseline case, and it is what the decision adopts."))

S.append(CondPageBreak(90 * mm))
S.append(SectionHeading(4, "The 60% and the retrofit target"))
S.append(P("The sentence about renovating social housing to cut primary energy use by 60% is in the article’s summary of the plan. "
           "In the plan, the measure is I2, retrofitting public social housing units. Its text says that units “shall undergo "
           "deep renovation works, in line with the definition in the Energy Performance of Buildings Directive”, which is a "
           "renovation to a zero-emission building level, adding that “a 60% reduction in primary energy use can therefore also "
           "be considered a deep renovation for the purpose of drafting and implementing the SCF Plans”, as the Commission’s "
           "guidance allows [3, p. 34]. The 60% is therefore the plan’s threshold for what counts as a deep renovation. "
           "We have the plan’s account of that guidance, not the guidance itself (second-hand ◆)."))
S.append(std_table([
    [C("What the plan will be paid against (Annex II [2])", cellh), C("Figure", cellh)],
    [C("Retrofit target, 2030 (cumulative)"), C("141 public social housing units")],
    [C("Retrofit target, 2032 (cumulative)"), C("236 units, 95 more")],
    [C("Quality required of each retrofit"), C("“an improvement reaching at least a B energy performance class”, with certificates")],
    [C("A 60% primary-energy indicator"), C("None in Annexes I–II")],
], [100 * mm, 70 * mm]))
S.append(Spacer(1, 2 * mm))
S.append(P("<b>What we could and could not test.</b> The plan states 236 units, about 4% of the 5,031 units the Housing Authority "
           "manages (236 / 5,031 = 4.7%), a retrofit cost of EUR 15.5 million (about EUR 65,700 a unit), and savings of "
           "1,563,195 kWh a year for the renovations (about 6,600 kWh per unit) [3, pp. 30, 33, 34]. It gives no pre-renovation "
           "consumption, so a percentage cannot be computed from its figures: we cannot say whether 6,600 kWh a unit is a 60% "
           "cut. The plan also states that savings will “exceed the average reference final energy consumption prior to "
           "renovation” (net zero energy or better, p. 126), a stronger claim than 60%, and it gives two totals for "
           "the same savings (5,212,620 and 5,220,644 kWh, a 0.15% gap that does not matter for the emissions figure) [3]."))
S.append(P("<b>Not the same quantity.</b> Press reports seen as search results (second-hand ◆) speak of a saving of about "
           "3,500 tonnes of CO2e. The plan’s figure is 3.54 ktCO2 <i>a year by 2032</i>, 0.65 from buildings and 2.89 from road "
           "transport [3, p. 127]. We do not rate the press figure."))

S.append(CondPageBreak(80 * mm))
S.append(SectionHeading(5, "‘Strong and lasting’, and what is not in the plan"))
S.append(P("The assessment is the Commission’s judgement. The legal finding in the decision reads: the plan “represents an "
           "adequate response to the social impact on and challenges faced by vulnerable households, vulnerable "
           "micro-enterprises and vulnerable transport users” [2, recital 15]. ‘Adequate’ and ‘strong and lasting’ are not the "
           "same words, and neither is a measurement; we do not rate either. Two facts bear on scale. First, the plan’s "
           "building measures cover 236 retrofitted units and 1,908 hot-water and solar-panel installations in estates, "
           "against 5,031 social housing units [3, p. 34; 2, Annex II]. Second, Eurostat reports that 7.6% of people in "
           "Malta could not keep their home warm in 2025 (EU-27: 8.8%), and 10.9% of those below the poverty line (EU-27: "
           "19.6%) [4]. Malta’s problem, on that measure, is smaller than the EU average, and heating is not the plan’s "
           "only target: the plan covers cooling and transport as well."))
S.append(P("<b>What the article leaves out.</b> It does not say the plan covers a small part of the housing stock; "
           "that payments depend on results; that the plan was revised after Commission observations (submitted 27 Nov 2025, "
           "revised 19 Jun 2026, final 15 Jul 2026 [2, recital 1]); or that the internal control system was not "
           "finalised at adoption [2, recital 26]. A news article of three minutes’ reading is not a plan summary, and "
           "none of these omissions changes the money."))

S.append(CondPageBreak(90 * mm))
S.append(SectionHeading(6, "Testing the claim"))
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> EUR 60.6 million over 2026–2032, EUR 45.4 million from the Fund, the rest (at least 25%) from Malta"),
     C("Commission [1]"), C("EUR 60,599,503; EUR 45,410,023; EUR 15,189,480 (25.07%) in the decision; Annex II payouts sum to the Fund share [2]."),
     verd("ACCURATE", GREENC)],
    [C("<b>B.</b> The plan will support social housing renovations “to reduce primary energy use by 60%”"),
     C("Commission [1]"),
     C("60% is the plan’s threshold for a deep renovation [3]; Annex II pays for 236 units reaching energy class B or better, with no 60% indicator or baseline [2]."),
     verd("PARTLY ACCURATE", AMBER)],
    [C("<b>C.</b> The plan is “a strong and lasting response” to ETS2"), C("Commission [1]"),
     C("An assessment. The decision’s own finding is “an adequate response” [2]; not measurable now."),
     verd("NOT RATED", GREY)],
    [C("<b>D.</b> Delivery of the plan’s targets by 2032"), C("Plan [2, 3]"),
     C("First milestone due Q1 2027; 16 milestones and targets to Q3 2032; no results yet."),
     verd("NOT YET DUE (PLEDGE)", NYD)],
], [44 * mm, 23 * mm, 69 * mm, 34 * mm], valign="MIDDLE"))

S += [CondPageBreak(95 * mm), Spacer(1, 6 * mm), SectionHeading(7, "Verdict, pledge and requests for evidence"),
      verdict_box("Largely supported", "The amounts and split are exact; the 60% is real but is a definition, not what is paid against. Confidence: moderate."),
      Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> The central figures, EUR 60.6 million, EUR 45.4 million and the 25% national share, are the decision’s own "
           "and recompute exactly. The 60% appears in the plan, but as a threshold for deep renovation. The monitored target is a count "
           "of units reaching energy class B, so the article’s sentence is a fair but looser summary. We call that a minor "
           "caveat, which is why the verdict is ‘largely supported’ rather than ‘supported’. Confidence is moderate because nothing has been "
           "delivered yet, no baseline is published, and we did not read the Commission’s guidance. <b>What this verdict does "
           "not say.</b> It does not say the plan is too small or too large, or that the renovations will reach 60%."))
S.append(callout([P("PLEDGE LABEL: NOT YET DUE (AS OF 20 OCT 2026)", tag),
                  P("The plan’s targets are measurable and dated: 141 retrofitted units by 2030 and 236 by 2032, 950 and then "
                    "1,908 hot-water and solar installations by 2029 and 2031, 80 and 109 electric vehicles for local councils "
                    "and 420 and 865 for micro-enterprises. Each is a government commitment tied to a payout. The first milestone "
                    "is due in the first quarter of 2027 and no results have been published. Revisit when Malta’s first payment "
                    "request (possible from the first quarter of 2027, per the article) or the 2029 targets are reported.", small)],
                 bg=BLUE_PALE, bar=BLUE))
S.append(P("Evidence we are asking for", h2))
S.append(requests_list([
    "Housing Authority / Ministry responsible for European Funds: the project documents for measure I2, with the "
    "pre-renovation consumption and the target saving per unit, so that the 60% can be checked.",
    "European Commission: the Social Climate Fund guidance (C(2025) 6732) passage on deep renovation and the 60% alternative.",
    "Ministry responsible for European Funds: the date of the audit body’s opinion on the internal control system (Annex III, Q4 2026)."]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag), P("Not needed for this verdict or this pledge label (maintainer rule of 5 October 2026).", small)],
              bg=AMBER_PALE, bar=AMBER)]
S += [Spacer(1, 6 * mm), SectionHeading(8, "Limitations")]
for l in ["The plan was read in the sections that bear on the claim, not in full. The Commission’s guidance on the Fund, "
          "which the plan cites for the 60% (◆), was not read.",
          "The statement that no 60% indicator exists is limited to Annexes I–II of the decision and to a text search of the "
          "plan (20 Oct 2026). The Housing Authority’s project documents were not available.",
          "Press figures on emissions are second-hand (◆) and not used.",
          "Nothing has been delivered, so no outcome (energy saved, emissions cut, households helped) is tested."]:
    S.append(P("• " + l, bul))
S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "European Commission, DG Employment, Social Affairs and Inclusion (29 Jul 2026). Commission paves the way for Malta to "
          "implement its EUR 60 million Social Climate Plan to support vulnerable households and transport users in the clean transition.",
     "https://employment-social-affairs.ec.europa.eu/news/commission-paves-way-malta-implement-its-eur60-million-social-climate-plan-support-vulnerable-2026-07-29_en"),
    ("2", "European Commission (29 Jul 2026). Implementing Decision C(2026) 5266 final on the Social Climate Plan of Malta, "
          "the financing of the Plan and the work programme for 2026–2032, with Annexes I–IV.",
     "https://employment-social-affairs.ec.europa.eu/document/download/af09c0fa-7763-4414-a404-bbda00262edd_en"),
    ("3", "Government of Malta (2026). Malta’s Social Climate Plan, adopted version (SFC2021 SCP-2026MT05SCFP001), 156 pp.",
     "https://employment-social-affairs.ec.europa.eu/document/download/b8ebd8ac-e077-4095-be50-fd0c10feee10_en"),
    ("4", "Eurostat. Inability to keep home adequately warm by income poverty status (ilc_mdes01), 2015–2025, retrieved 20 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/ilc_mdes01"),
    ("5", "Miżien. Data and calculations: data/cc-125/; tools/cc-125-report/calc.py (checks.csv).", ""),
])
S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or official "
                "statistics · D assertion or anecdote. ◆ marks a source known only second-hand.", pledges=True)
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "20 Oct 2026", "First issue. Verdict Largely supported (moderate confidence); pledge label Not yet due; "
                    "no right of reply needed.")])

build_report(Report(
    number="125", out=str(FIG / "report.pdf"), kicker="Climate policy and EU funds",
    title_lines=["Malta’s Social", "Climate Plan", "EUR 60.6 million"],
    subtitle_lines=["Testing the Commission’s July 2026 description of the", "plan against its own decision and annexes"],
    quote_lines=["“… the Maltese Social Climate Plan will mobilise", "EUR 60.6 million.”  “… reduce primary energy use by 60%.”"],
    quote_size=13.5,
    attribution="European Commission, DG EMPL news article, 29 July 2026.",
    context="Commission Implementing Decision C(2026) 5266 · Malta’s Social Climate Plan 2026–2032.",
    verdict="Largely supported", verdict_note="Amounts exact; the 60% is a definition, not the payout target",
    footer_lines=["Version 1.0  ·  20 October 2026", "Status:",
                  "Prepared from public sources.",
                  "Pledge label: not yet due (as of 20 Oct 2026).  Repository: github.com/leandergrech/Mizien"],
    running_head="Social Climate Plan – European Commission", version="1.0", date="20 October 2026",
    pdf_title="Malta's Social Climate Plan EUR 60.6 million. Claim Check 125",
    pdf_subject="Tests the Commission's 29 July 2026 description of Malta's Social Climate Plan",
    pledge_label="Not yet due", story=S))
