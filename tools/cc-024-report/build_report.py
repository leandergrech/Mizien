"""Claim Check 024 report. Run calc.py and figures.py first. Output: out/report.pdf"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

FIG = HERE / "out"
S = []

# ================================================================== TL;DR
S += [SectionHeading(None, "TL;DR"), Spacer(1, 1 * mm),
      P("Malta’s final updated National Energy and Climate Plan (December 2024) puts Malta’s 2030 renewables share at "
        "<b>24.5%</b> of gross final energy consumption (summarised as “25%”), up from an earlier 11.5%. "
        "<b>The plan’s own calculation does not count offshore wind</b>, which it says will not be commissioned by 2030; "
        "the 2030 figure rests on solar PV on land, biogas, biofuel blending and heat-pump ambient heat. Malta is "
        "<b>ahead of the plan’s yearly path</b> (17.2% in 2024 against 15.5%), but the gain has come from heating and "
        "cooling, not from solar electricity, and the Commission found the 24.5% is below the 28% its formula gives "
        "and that the plan does not quantify what solar support will deliver.", lead)]
S.append(key_points([
    ("The target is 24.5% (25% in summaries), not 11.5%.",
     "The plan says it raises the contribution “from 11.5% to 25%” (p. 22) and projects 24.5% in 2030 (p. 83)."),
    ("Offshore wind is not in the sum.",
     "“Offshore wind does not contribute to Malta’s RES contribution … as it is not envisaged to be completed and "
     "commissioned by 2030” (p. 83). Yet the plan’s summary table lists offshore technologies among the means (p. 22)."),
    ("Solar PV is part of it, but not quantified in points.",
     "350 MWp by 2030 (p. 84) needs about 16 MWp a year against 11.5 added in 2024; the Commission notes PV support "
     "is not quantified."),
    ("Progress is ahead of the plan, but heat-driven.",
     "Eurostat: 17.2% in 2024 (plan 15.5%). The rise came from heating and cooling; the electricity share moved only "
     "9.5% to 10.7% since 2020. The Commission calls the 24.5% below its 28% formula."),
    ("Verdict: not substantiated (moderate confidence); pledge: on track.",
     "The target is on its path; the route named is not supported by the plan’s own sums."),
]))
S += [Spacer(1, 2.5 * mm), VerdictMeter(2), Spacer(1, 3 * mm),
      tiles([("24.5%", GREEN, "Malta’s projected 2030 renewables share in the plan (summary: 25%)"),
             ("0 MW", RED, "Offshore wind counted in that 24.5% (plan, p. 83)"),
             ("17.2%", GREEN, "Malta’s share in 2024 (Eurostat) against 15.5% on the plan’s path"),
             ("16 vs 11.5", ORANGE, "MWp of solar PV a year needed to 2030 vs net added in 2024")]),
      Spacer(1, 4 * mm),
      up_down("A dated, quantified breakdown showing how much each of solar PV, biogas, biofuels and heat pumps adds "
              "to the 24.5%; or a commissioning date and grid connection for offshore wind inside 2030.",
              "Eurostat data showing the share falling behind the plan’s path, or the plan being revised so that the "
              "2030 share depends on projects that are not built."),
      Spacer(1, 3 * mm)]
S += toc([("1", "The claim and what we could verify"), ("2", "Method"), ("3", "What the plan says"),
          ("4", "What the data show"), ("5", "Where the evidence points different ways"),
          ("6", "Testing the claim"), ("7", "Verdict, pledge and requests for evidence"), ("8", "Limitations")])
S.append(PageBreak())

# ================================================================== 1
S.append(SectionHeading(1, "The claim and what we could verify"))
S.append(P("The claim record paraphrases Malta’s updated National Energy and Climate Plan (NECP) 2021–2030: that Malta will "
           "reach its 2030 renewable-energy contribution (“11.5% … in the EU-reported target; 25% cited in summaries”) "
           "“through solar PV and offshore wind”. That wording was written by our intake from a locator source, so we "
           "assess the plan’s own words, read in the copy the European Commission publishes [1]."))
S.append(std_table([
    [C("Source", cellh), C("What it says", cellh), C("Our access", cellh), C("Status", cellh)],
    [C("<b>Government of Malta</b>, final updated NECP, summary table, pp. 21–22 [1]"),
     C("“Increase Malta’s ambition to a renewable energy share of 25% by 2030”; “Increase the Renewable Energy "
       "contribution from 11.5% to 25% through multiple initiatives to focus on more diversification in onshore and "
       "offshore technologies”."), C("Read in full (381 pages)."), C("<b>The claim</b>")],
    [C("<b>Same plan</b>, section 2.1.2, pp. 82–84 [1]"),
     C("“expected to amount to 24.5% in 2030”; 16.5% in 2025, 20.7% in 2027. Offshore wind “does not contribute … as it "
       "is not envisaged to be completed and commissioned by 2030”. “Solar PV is expected to reach 350 MWp by 2030”."),
     C("Read in full."), C("<b>The claim, detailed</b>")],
    [C("<b>European Commission</b>, assessment of the final NECP, SWD(2025) 140, Malta extract [2]"),
     C("24.5% “is below the 28%” from the Annex II formula; trajectories below reference points; support for solar "
       "PV not quantified."), C("Read."), C("<b>Primary evidence</b>")],
    [C("<b>Eurostat</b> nrg_ind_ren; <b>NSO</b> PV release NR 111/2025 [3, 4]"),
     C("Malta’s actual share to 2025 (provisional); PV capacity 252.3 MWp at end-2024."),
     C("Eurostat read by API; NSO page blocked (403), figures second-hand."), C("Data")],
    [C("<b>2019 NECP</b> (source of the “11.5%”)"), C("Not read: the agency’s host was refused to scripts."),
     C("The 11.5% is taken from the 2024 plan’s own wording."), C("Gap")],
], [40 * mm, 72 * mm, 36 * mm, 22 * mm]))
S += [Spacer(1, 4 * mm),
      callout([P("FAIRNESS NOTE", tag),
               P("A national plan is a forward-looking document, and the plan is open about its own limits: it states that "
                 "offshore wind is excluded from the 2030 share, and that Malta’s land area makes land-hungry renewables "
                 "hard (p. 74). This check is about how the target is summarised and whether the evidence supports it, "
                 "not about whether the ambition is worthwhile.", small)], bg=AMBER_PALE, bar=AMBER), Spacer(1, 4 * mm)]

# ================================================================== 2
S.append(SectionHeading(2, "Method"))
S.append(P("<b>Question.</b> Is the 2030 renewables contribution what the plan says, will it be reached the way the claim "
           "says, and is progress on the plan’s own path?"))
S.append(P("<b>Evidence.</b> We read the plan’s renewables sections and every passage that mentions offshore wind or PV "
           "capacity, then the Commission’s assessment of the plan. We downloaded Eurostat’s renewable-share series (nrg_ind_ren; "
           "Malta, Cyprus as an island comparator, EU-27) on 5 October 2026 and recomputed every comparison with a script "
           "(<i>tools/cc-024-report/calc.py</i>; outputs in <i>data/cc-024/</i>). Plan and Commission figures are typed "
           "with printed page numbers into <i>necp_commission_inputs.csv</i>. Peer-reviewed literature is context only: "
           "this is a check of a document against statistics, and we found no paper that tests the plan."))
S.append(P("<b>Grades.</b> Official statistics and EU assessments are grade C; the plan itself is grade D as evidence of "
           "what will happen (a statement of intent). <b>Verdicts</b> and <b>pledge labels</b> follow Appendix A."))

# ================================================================== 3
S.append(CondPageBreak(110 * mm))
S.append(SectionHeading(3, "What the plan says"))
S.append(P("Three figures circulate and the plan contains all of them. <b>11.5%</b> is the earlier contribution that the "
           "summary table says is being raised. <b>25%</b> is the ambition in the summary table. <b>24.5%</b> is the figure "
           "in the plan’s projection and indicative trajectory (Table 3), the one the Commission assessed. A reader quoting “25%” "
           "is quoting the plan’s summary; “11.5%” is out of date."))
S.append(P("The 24.5% is built, the plan says, from “additional effort to deploy solar PV systems on land”, biogas from "
           "waste facilities, higher biofuel blending in transport, and “ambient cooling captured by air-to-air heat pumps” "
           "(p. 83). It then adds: “offshore wind does not contribute to Malta’s RES contribution shown in the Table as it "
           "is not envisaged to be completed and commissioned by 2030.” Elsewhere the plan commits to “a minimum of 350MW of "
           "offshore renewable generation capacity … by 2030” (p. 25) and, in another section, to 350 MW “by 2050” (p. 78), "
           "as a non-binding TEN-E agreement. The plan therefore lists offshore energy among its means, while counting none "
           "of it towards 2030."))
S.append(fig(FIG / "fig_path.png", width=CW * 0.95))
S.append(P("Figure 1. Malta’s renewable share (Eurostat) against the plan’s indicative target, the Commission’s reference "
           "points and its 28% formula result. 2025 is provisional (Eurostat flag p).", cap))

# ================================================================== 4
S.append(CondPageBreak(95 * mm))
S.append(SectionHeading(4, "What the data show"))
S.append(std_table([
    [C("Indicator", cellh), C("Malta", cellh), C("Comparator", cellh), C("Source", cellh), C("Grade", cellh)],
    [C("Renewables share, 2024"), C("<b>17.2%</b>"), C("Plan path 15.5%; EU-27 25.2%; Cyprus 20.8%"), C("Eurostat [3]; plan p. 83"), grade_tag("C")],
    [C("Renewables share, 2025 (provisional)"), C("18.8%"), C("Plan path 16.5%; Commission reference point 18%"), C("Eurostat [3]; [2]"), grade_tag("C")],
    [C("Straight line from 2020 outturn (10.7%) to 24.5%, value in 2024"), C("16.2%"), C("Actual +1.0 point above"), C("calc.py"), grade_tag("C")],
    [C("Rise needed per year, 2024 to 2030"), C("1.2 points"), C("2020–2024 average 1.6 points"), C("calc.py"), grade_tag("C")],
    [C("Electricity share, 2020 to 2024"), C("<b>9.5% to 10.7%</b>"), C("EU-27 47.5% (2024)"), C("Eurostat [3]"), grade_tag("C")],
    [C("Heating and cooling share, 2020 to 2024"), C("<b>23.0% to 59.2%</b>"), C("EU-27 26.7% (2024)"), C("Eurostat [3]"), grade_tag("C")],
    [C("Transport share, 2020 to 2024"), C("10.6% to 11.4%"), C("EU-27 11.2% (2024)"), C("Eurostat [3]"), grade_tag("C")],
    [C("Solar PV capacity, end-2023 / end-2024"), C("241 / 252.3 MWp"), C("Plan: 350 MWp by 2030"), C("Plan p. 74; NSO [4] (second-hand)"), grade_tag("C")],
    [C("PV to add per year to reach 350 MWp / added in 2024 (net)"), C("<b>16.3 / 11.5 MWp</b>"), C("1.4 times the 2024 pace"), C("calc.py"), grade_tag("C")],
    [C("2030 contribution: plan / Commission formula"), C("24.5% / 28%"), C("3.5 points below"), C("Plan p. 83; [2]"), grade_tag("C")],
], [58 * mm, 28 * mm, 40 * mm, 30 * mm, 14 * mm]))
S.append(P("Values in <i>data/cc-024/checks.csv</i>. Eurostat now shows 14.04% for 2022, the plan 13.4%: the series is revised, so "
           "year-on-year comparisons use one vintage (retrieved 5 Oct 2026).", cap))
S.append(fig(FIG / "fig_sectors.png"))
S.append(P("Figure 2. Left: Malta’s renewable share by sector, 2013–2024. Right: the three sector shares in 2024 against the EU-27. "
           "Almost all of the recent rise is in heating and cooling.", cap))
S.append(P("Reading across the data", h2))
for t in ["• <b>Malta is ahead of the plan’s own path</b> in 2023, 2024 and (provisionally) 2025, and, if the 2025 figure holds, "
          "above the Commission’s 18% reference point for that year.",
          "• <b>The lead is built on heat, not on solar power.</b> The electricity share, where PV counts, rose about one point in "
          "four years. The heating and cooling share more than doubled from 2020 to 2024, which is consistent with the plan’s "
          "reliance on ambient heat from heat pumps; we could not split the effect by technology because the plan does not.",
          "• <b>PV needs to speed up by about 40%.</b> Reaching 350 MWp means adding about 16 MWp a year, against 11.5 MWp net in 2024. At "
          "2024’s output per kWp (about 1,290 kWh), 350 MWp would give about 450 GWh a year against 326 GWh in 2024. "
          "How many points of share that is cannot be said from sourced inputs, because the plan does not give it.",
          "• <b>Cyprus, another island, is 3.6 points ahead of Malta</b> (20.8% vs 17.2% in 2024) and the EU-27 average is 8 points ahead."]:
    S.append(P(t, bul))
S.append(KeepTogether([fig(FIG / "fig_pv.png"),
                       P("Figure 3. Installed solar PV: plan’s 350 MWp path against the 2024 pace. NSO figures are second-hand.", cap)]))

# ================================================================== 5
S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(5, "Where the evidence points different ways"))
S.append(contested(
    "Q1  Does the 2030 plan rely on offshore wind?", "NO, BY THE PLAN’S OWN SUM", RED,
    "The summary table lists “onshore and offshore technologies” as the means and the plan commits to 350 MW offshore under TEN-E "
    "(pp. 22, 25) [1].",
    "The projection excludes offshore wind in terms, because it is not expected to be commissioned by 2030, and the plan "
    "gives 350 MW “by 2050” in another section (pp. 83, 78) [1].",
    "<b>For this claim:</b> offshore wind is part of the plan’s ambition, not of its 2030 arithmetic.",
    label_a="WHAT THE SUMMARY SAYS", label_b="WHAT THE PROJECTION SAYS"))
S.append(contested(
    "Q2  Is Malta on track for 24.5%?", "ON THE PLAN’S PATH; HEAT-DRIVEN", AMBER,
    "Eurostat shows 17.2% in 2024 against 15.5% on the plan’s path, and 18.8% provisional in 2025 against 16.5% [3].",
    "The Commission rates the plan’s 2025 and 2027 points below its reference points and the 2030 share below its 28% formula "
    "result; the lead is in heating and cooling, with electricity share nearly flat [2, 3].",
    "<b>For this claim:</b> delivery of the plan’s own 2030 number looks on track; the Commission’s higher benchmark is a "
    "different standard, which the plan does not claim to meet.",
    label_a="EVIDENCE OF PROGRESS", label_b="EVIDENCE OF GAPS"))
S.append(contested(
    "Q3  Is solar PV enough?", "NOT SHOWN", AMBER,
    "PV is Malta’s main local source, 241 MWp by 2023, and support schemes are kept (pp. 74, 84) [1].",
    "The plan does not quantify what PV support delivers; the Commission says so [2]. PV additions in 2024 were below the pace "
    "needed [4].",
    "<b>For this claim:</b> PV is a plausible contributor but the plan shows no sum linking it to the target.",
    label_a="FOR", label_b="AGAINST"))

# ================================================================== 6
S.append(CondPageBreak(120 * mm))
S.append(SectionHeading(6, "Testing the claim"))
verd = lambda t, c: chip(t, c, w=29 * mm)
S.append(std_table([
    [C("Sub-claim", cellh), C("Said by", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
    [C("<b>A.</b> The 2030 contribution is 11.5%"), C("Claim record"),
     C("11.5% is the earlier contribution that the plan raises (p. 22). It is not the 2030 figure."), verd("OUTDATED", RED)],
    [C("<b>B.</b> It is 25% (or 24.5%)"), C("Plan [1]"),
     C("25% is the summary ambition; 24.5% is the projection and trajectory end-point (pp. 21, 83)."), verd("ACCURATE, ROUNDED", GREENC)],
    [C("<b>C.</b> Malta will reach it through solar PV"), C("Claim record"),
     C("PV is one of four named contributors; 350 MWp by 2030 needs a faster pace; its points of share are not quantified."),
     verd("PARTLY SUPPORTED", AMBER)],
    [C("<b>D.</b> …and through offshore wind"), C("Claim record; plan summary"),
     C("The plan counts no offshore wind in the 2030 share (p. 83)."), verd("NOT SUPPORTED", RED)],
    [C("<b>E.</b> Malta will reach the 2030 share"), C("Plan"),
     C("17.2% in 2024 against 15.5% on the plan’s path; Commission: below its formula and reference points. A target, rated as a pledge."),
     verd("ON TRACK (PLEDGE)", GREENC)],
], [42 * mm, 24 * mm, 70 * mm, 34 * mm], valign="MIDDLE"))

# ================================================================== 7
S += [Spacer(1, 6 * mm), SectionHeading(7, "Verdict, pledge and requests for evidence"),
      verdict_box("Not substantiated", "The 2030 share is plausible on current data; the stated route is not shown. Confidence: moderate."),
      Spacer(1, 4 * mm)]
S.append(P("<b>Why.</b> (1) The claim as worded names solar PV and offshore wind as the route. The plan’s own projection "
           "counts no offshore wind, and gives no sum for PV. (2) “11.5%” is a superseded figure. (3) The Commission found the "
           "plan’s ambition below its formula and its support measures unquantified. Under our scale, a statement made more "
           "strongly than the evidence offered allows is <i>Not substantiated</i>. We did not use <i>Misleading</i>: the plan "
           "itself discloses the exclusion of offshore wind in its body text."))
S.append(callout([P("PLEDGE LABEL: ON TRACK (AS OF 15 SEP 2026)", tag),
                  P("The plan’s target is a pledge-like commitment with a date (2030). Published progress is ahead of the "
                    "plan’s own path and of a straight line from the 2020 outturn: 17.2% against 16.2% in 2024; 18.8% "
                    "(provisional) against 17.6% in 2025. Reaching 24.5% needs 1.2 points a year from 2024, below the 1.6 "
                    "of 2020–2024. This is delivery against the plan’s figure, not against the Commission’s 28%, and the "
                    "label should be revisited when Eurostat finalises 2025.", small)], bg=BLUE_PALE, bar=BLUE))
S.append(P("<b>What this does not say.</b> It does not say the plan is wrong to include offshore wind as an ambition, that "
           "the 24.5% will be missed, or that anyone acted in bad faith. A fuller statement would read: <i>“Malta projects 24.5% "
           "renewables in 2030, mainly from solar PV on land, biogas, biofuels and heat pumps; offshore wind is planned but not "
           "counted.”</i>"))
S.append(KeepTogether([P("Evidence we are asking for", h2), requests_list([
    "A breakdown of the 24.5% by technology and sector (PV, biogas, biofuels, heat pumps), in points or ktoe.",
    "The date by which offshore wind is expected to be commissioned and what share it would add.",
    "The pace of PV additions planned for 2025–2030 and the support measures behind it.",
    "The 2019 NECP’s wording on the 11.5% contribution, to confirm the earlier figure.",
])]))
S += [Spacer(1, 4 * mm),
      callout([P("RIGHT OF REPLY", tag),
               P("This draft should go to the Energy and Water Agency and the Ministry responsible for energy with a fixed "
                 "deadline (suggested 14 days). A <i>Not substantiated</i> verdict is not circulated beyond this site before "
                 "the deadline passes. Responses will be appended and the verdict revisited.", small)],
              bg=AMBER_PALE, bar=AMBER)]

# ================================================================== 8
S += [Spacer(1, 6 * mm), SectionHeading(8, "Limitations")]
for l in ["The claim record’s wording is our intake’s paraphrase, not a quotation. We assessed the plan’s own sentences and "
          "say where they differ from it.",
          "The NSO PV figures (252.255 MWp, 11.792 MWp connected, 0.262 MW decommissioned, 326.5 GWh) were read from a web-search "
          "summary of release NR 111/2025; nso.gov.mt returns 403 to scripts. They agree with the plan’s 241 MWp at end-2023 "
          "(implied 240.7). Treat them as second-hand.",
          "The 2019 NECP could not be read, so “11.5% is the earlier contribution” rests on the 2024 plan’s wording.",
          "Eurostat’s 2025 value is provisional and the series is revised; the 2022 value differs from the plan’s.",
          "We could not convert PV, biofuels or heat pumps into points of share: the plan gives no such sums and we did not "
          "use assumed rates.",
          "Commission page numbers are the printed pages of SWD(2025) 140; the extract’s date is taken from the file (May 2025).",
          "The Commission’s reference points are for the EU’s 42.5% target and are a benchmark, not a legal limit on Malta."]:
    S.append(P("• " + l, bul))

S += [Spacer(1, 6 * mm), SectionHeading(None, "References")]
S += references([
    ("1", "Government of Malta (Dec 2024). Final updated National Energy and Climate Plan 2021–2030 (English), 381 pp., as "
          "published by the European Commission. Printed pages cited: 21–22, 25, 74, 78, 82–84, 279.",
     "https://commission.europa.eu/publications/malta-final-updated-necp-2021-2030-submitted-2025_en"),
    ("2", "European Commission (May 2025). Assessment of the final updated NECPs, Commission Staff Working Document "
          "SWD(2025) 140, Malta extract, Table 1 (p. 160) and section 2.2 (p. 163).",
     "https://commission.europa.eu/document/download/bf1c1e17-293c-4c50-92ca-1ae663ab6cae_en?filename=MT_Extract_SWD+2025_140.pdf"),
    ("3", "Eurostat. Share of energy from renewable sources (nrg_ind_ren), updated 15 Sep 2026, retrieved 5 Oct 2026.",
     "https://ec.europa.eu/eurostat/databrowser/view/nrg_ind_ren/default/table"),
    ("4", "National Statistics Office Malta (24 Jun 2025). Renewable Energy from Photovoltaic Panels (PVs): 2024, NR 111/2025. "
          "(Figures second-hand; page returned 403.) " + DIAM,
     "https://nso.gov.mt/energy/renewable-energy-from-photovoltaic-panels-pvs-2024/"),
    ("5", "European Commission (18 Dec 2023). Recommendation on the draft updated NECP of Malta, C(2023) 9610 final (read; "
          "context for the 28% formula).",
     "https://commission.europa.eu/system/files/2023-12/Recommendation_draft_updated_NECP_Malta_2023.pdf"),
    ("6", "Miżien. Calculation script and outputs: tools/cc-024-report/calc.py; data/cc-024/checks.csv.", ""),
])

S.append(PageBreak())
S += appendix_a("A experiment · B observational study with a control or gradient · C review, guidance or "
                "official statistics · D assertion or anecdote. ◆ marks a source known only second-hand.", pledges=True)
S += [Spacer(1, 5 * mm)]
S += revision_log([("1.0", "5 Oct 2026", "First issue. Draft pending right of reply from the Energy and Water Agency and the "
                                         "responsible Ministry.")])

build_report(Report(
    number="024", out=str(FIG / "report.pdf"), kicker="Climate and energy",
    title_lines=["Renewables by 2030:", "solar PV and", "offshore wind?"],
    subtitle_lines=["Testing Malta’s 2030 renewable-energy target", "against its own plan and Eurostat data"],
    quote_lines=["“Increase the Renewable Energy contribution from", "11.5% to 25% through multiple initiatives …”"], quote_size=15,
    attribution="Government of Malta, final updated National Energy and Climate Plan, p. 22 (December 2024).",
    context="Summarised in our record as reaching the 2030 share through solar PV and offshore wind.",
    verdict="Not substantiated", verdict_note="Target on track; route not shown (offshore wind not counted)",
    footer_lines=["Version 1.0  ·  5 October 2026", "Status: draft for right of reply (Energy and Water Agency; Ministry)",
                  "Prepared from public sources and Eurostat data.", "Repository: github.com/leandergrech/Mizien"],
    running_head="Malta’s 2030 renewables target", version="1.0", date="5 October 2026",
    pdf_title="Renewables by 2030: solar PV and offshore wind? Claim Check 024",
    pdf_subject="Tests Malta's 2030 renewables contribution in the updated NECP against Eurostat data",
    story=S))
