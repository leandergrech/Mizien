"""Build the CC-009 reverse-osmosis and groundwater report.

Run fetch_data.py, data/cc-009/calc.py and figures.py first (or `python tools/restore_figures.py CC-009` to restore
the published figures). Output: claims/CC-009/report.pdf
"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FIG = HERE / "out"
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

S = [SectionHeading(None, "TL;DR"), Spacer(1, mm),
     P("WSC's latest annual report says reverse osmosis supplied 70.7% of its potable-water production in 2025, and "
       "that its groundwater production fell to 11.5 million m³, the lowest annual total in a decade. The figures "
       "check out against WSC's own series. We set them beside national data and the research on Malta's aquifers: "
       "the cut is real but small, and it is not evidence that the aquifers have recovered.", lead)]
S.append(key_points([
    ("The source mix changed.", "Reverse osmosis rose from 64.3% of WSC production in 2022 to 70.7% in 2025 "
     "(Figure 1). WSC says its groundwater production fell 11.4% in 2025; its chart values give 11.9%."),
    ("The cut is about 4% of national abstraction.", "WSC produced 1.55 million m³ less groundwater in 2025. Malta "
     "abstracted an estimated 38.5 million m³ in 2024, 57% of it for agriculture, whose estimated use rose by "
     "3.1 million m³ that year (Figure 2)."),
    ("Abstraction is close to what the aquifers can give.", "Estimated recharge was 41.5 million m³ in 2024. A "
     "published water balance puts the groundwater available for abstraction at about 37 million m³ a year."),
    ("No groundwater body is in good status.", "The River Basin Management Plan names both main aquifers as poor "
     "quantitatively; Malta's EU reporting lists four of 15, and all 15 as poor chemically (Figure 3)."),
    ("Recovery would be slow to show.", "A tracer study puts travel times through the main aquifer at 15–40 years on "
     "Malta and up to 60 or more on Gozo; nitrate held in the rock keeps reaching the groundwater for years."),
    ("The new plant is tendered, not built.", "Għar Lapsi Plant B (30,000 m³/day) was tendered in August 2026; bids "
     "are due on 30 October 2026."),
]))
S += [Spacer(1, 2 * mm), VerdictMeter(1), Spacer(1, 2 * mm),
      tiles([("70.7%", GREEN, "WSC production from reverse osmosis, 2025"),
             ("4%", ORANGE, "WSC’s 2025 groundwater cut as a share of national abstraction (2024)"),
             ("57%", ORANGE, "of groundwater abstracted in 2024 went to agriculture (estimate)"),
             ("0 of 15", RED, "groundwater bodies in good overall status (latest assessment)")]),
      Spacer(1, 3 * mm),
      up_down("WSC's reconciled 2024–25 figure and the ten-year series behind “lowest in a decade”; for any claim of "
              "recovery, a new status assessment with metered abstraction, recharge, water levels, salinity and nitrate "
              "by groundwater body.",
              "Evidence that WSC's 2025 mix, production series or procurement status is materially different from the "
              "official records."),
      Spacer(1, 4 * mm),
      *toc([("1", "What WSC reported"), ("2", "Rechecking the production series"),
            ("3", "National abstraction and recharge"), ("4", "Groundwater-body status"),
            ("5", "What the research says"), ("6", "The Għar Lapsi tender"),
            ("7", "Verdict and limits"), ("8", "Sources")]), PageBreak()]

S += [SectionHeading(1, "What WSC reported"),
      P("WSC's Annual Report 2025 says 70.7% of its 39.5 million m³ of potable-water production came from four "
        "reverse-osmosis plants. It reports 11.5 million m³ of groundwater production, the lowest total in the previous "
        "decade, and says the volume was 11.4% lower than in 2024. WSC links the shift to blending for lower salinity "
        "in reservoirs [1]. WSC does not say that the aquifers have recovered; this check asks what its figures can "
        "and cannot show."),
      callout([P("KEEP THE MEASURES DISTINCT", tag),
               P("RO share and WSC groundwater production describe the utility's potable supply. National abstraction "
                 "counts every user, including farms. Groundwater-body status compares aquifer quantity and quality "
                 "against environmental criteria. None of these measures can substitute for another.", lead)],
              bg=PALE, bar=GREEN),
      Spacer(1, 3 * mm),
      P("The 2025 report identifies taste and salinity as the immediate reason for increasing the RO proportion. Its "
        "statements therefore support reduced WSC reliance on groundwater in the production mix; they do not say that "
        "the aquifers had returned to good status."),
      P("The 2024 report provides useful context: it described groundwater production as fairly constant while "
        "abstraction sources were redistributed, and explained that WSC was reactivating sources to relieve localised "
        "pressure. A single year's decline should not be treated as evidence of a sustained aquifer trend [3].")]

S += [CondPageBreak(120 * mm), SectionHeading(2, "Rechecking the production series"),
      P("We transcribed the annual RO and groundwater values shown in Figure 20 of WSC's 2025 report and recalculated "
        "totals, source shares and changes. The script is <i>data/cc-009/calc.py</i>; the inputs and outputs are in "
        "<i>data/cc-009/</i>."),
      fig(FIG / "fig1_wsc_sources.png", width=CW * 0.9),
      P("Figure 1. WSC potable-water production by source, million m³, with the RO share. WSC production only; "
        "national abstraction is in Figure 2.", cap),
      P("From 2022 to 2025, WSC's groundwater component decreased by 8.95%, while its RO share rose by 6.43 percentage "
        "points. WSC's 2025 report narrative says the one-year groundwater decline was 11.4%. The 2024 and 2025 chart "
        "entries (13,094,325 m³ and 11,541,256 m³) imply 11.86%. The difference is small but unresolved, so this report "
        "does not silently substitute one figure for the other [1]. WSC's own 2022 report gives that year's "
        "groundwater production as 486 m³ less than the 2025 chart; the difference does not change any share or "
        "percentage shown here [6]."),
      P("Our series covers 2022–2025 only, so “lowest in a decade” is WSC's statement. Eurostat's separate series of "
        "groundwater abstracted for public water supply (a different measure, about 1 million m³ a year higher than "
        "WSC's production in 2022–2024) never fell below 13.5 million m³ in 2015–2024 [8]. That is consistent with "
        "WSC's statement, but cannot confirm it.")]

S += [CondPageBreak(130 * mm), SectionHeading(3, "National abstraction and recharge"),
      P("WSC is one groundwater user among several. Eurostat's figures for Malta, all flagged as estimates, show "
        "38.5 million m³ of fresh groundwater abstracted in 2024 [8]. Agriculture took 21.8 million m³ (57%), up from "
        "18.7 million m³ in 2023; public water supply took 14.3 million m³ (37%)."),
      fig(FIG / "fig2_abstraction.png", width=CW * 0.92),
      P("Figure 2. Malta's fresh groundwater abstraction by user, 2015–2024, with estimated recharge into the aquifers "
        "(Eurostat estimates) and the long-term available groundwater in a published water balance [9]. For 2021 "
        "Eurostat gives no public-supply value; the hatched segment is the total minus the other users.", cap),
      std_table([
          [C("Measure (million m³)", cellh), C("Value", cellh), C("Year", cellh), C("Source", cellh), C("Grade", cellh)],
          [C("Fresh groundwater abstraction, all users"), C("<b>38.46</b>"), C("2024"), C("Eurostat env_wat_abs [8]"),
           grade_tag("C")],
          [C("of which agriculture (2023: 18.67)"), C("21.77"), C("2024"), C("Eurostat [8]"), grade_tag("C")],
          [C("of which public water supply"), C("14.28"), C("2024"), C("Eurostat [8]"), grade_tag("C")],
          [C("WSC groundwater production cut, 2024 to 2025"), C("1.55 (4.0% of 38.46)"), C("2025"),
           C("WSC [1]; our calculation"), grade_tag("C")],
          [C("Estimated recharge into the aquifers"), C("41.52"), C("2024"), C("Eurostat env_wat_res [8]"),
           grade_tag("C")],
          [C("Groundwater available for abstraction, long-term average"), C("37"), C("long term"),
           C("Sapiano 2020, Table 1 [9]"), grade_tag("C")],
      ], [64 * mm, 34 * mm, 20 * mm, 40 * mm, 12 * mm]),
      P("Eurostat values are flagged as estimates; no 2025 national figures are yet published, so the 4% compares "
        "different years. Values and query URLs in <i>data/cc-009/eurostat_water.csv</i> and <i>checks.csv</i>.", cap),
      P("Three points follow. <b>First</b>, WSC's 2025 cut is small beside national use: about 4% of the 2024 total, "
        "and about half the estimated rise in agricultural abstraction in 2024 alone. <b>Second</b>, recharge depends "
        "on rainfall and varies widely; the 2023 and 2024 estimates (41.2 and 41.5 million m³) are the lowest in the "
        "2010–2024 series [8]. <b>Third</b>, abstraction equal to 93% of recharge does not leave 7% to spare. The "
        "published water balance for Malta sets aside about half of the recharge to the sea-level aquifers as natural "
        "discharge to the sea and puts the groundwater available for abstraction at about 37 million m³ a year, "
        "against abstraction of 38–41 million m³; it gives a water exploitation index of 78% over the long term and "
        "89% in 2019, where the EU treats 40% as high water stress [9].")]

S += [CondPageBreak(140 * mm), SectionHeading(4, "Groundwater-body status"),
      P("The 3rd River Basin Management Plan for 2021–2027 is the latest completed national plan identified on ERA's "
        "website. Its Chapter 6 status tables assess 15 groundwater bodies. It reports both the Malta and Gozo Mean Sea "
        "Level aquifer systems as poor quantitatively, meaning they are over-abstracted under the plan's water-balance "
        "assessment [2]. Malta's reporting of the same plan cycle to the EEA, with status assessed in 2021, does not "
        "match the plan on every count [7]. The table shows both."),
      std_table([
          [C("Indicator (15 bodies)", cellh), C("Plan, Chapter 6, as recorded in our notes [2]", cellh),
           C("Malta's EU reporting, 3rd cycle [7]", cellh)],
          [C("Overall status"), C("15 of 15 poor; good overall status requires both quantity and quality to pass."),
           C("15 of 15 poor (all fail chemical status).")],
          [C("Quantitative status"), C("Poor: Malta and Gozo Mean Sea Level aquifers."),
           C("4 poor: Malta and Gozo Mean Sea Level, Pwales Coastal and Marfa Coastal.")],
          [C("Chemical status"), C("14 poor; nitrate is the main failing parameter, but not the only one."),
           C("15 poor.")],
          [C("Nitrate standard"), C("12 of 15 exceed 50 mg/L; Gozo Mean Sea Level, Comino Mean Sea Level and Mellieħa "
                                    "Perched are named exceptions."), C("Not given by body in the layer queried.")],
      ], [34 * mm, (CW - 34 * mm) / 2, (CW - 34 * mm) / 2]),
      Spacer(1, 3 * mm),
      fig(FIG / "fig3_gwb_map.png", width=CW * 0.95),
      P("Figure 3. Groundwater bodies by quantitative status in Malta's 3rd-cycle EU reporting [7]. The perched bodies "
        "sit above parts of the sea-level aquifers, so they are drawn separately.", cap),
      P("The two sources agree that both main aquifers are poor quantitatively and that none of the 15 bodies reaches "
        "good overall status. They differ on two counts: Malta's EU reporting also lists Pwales Coastal and Marfa "
        "Coastal as poor quantitatively, and it lists all 15 bodies, not 14, as poor chemically. Its previous cycle "
        "(2016 reporting, status assessed 2010–2014) listed 2 and 12. We could not re-open the plan to explain the "
        "difference, because ERA's website blocks automated access, so both are shown [2, 7]."),
      P("The queue note said all groundwater bodies fail on nitrates. The plan does not say that: it names three bodies "
        "that do not exceed the 50 mg/L nitrate standard. Chemical status is a broader assessment that includes other "
        "factors such as saline intrusion; the plan records 14 bodies failing it, and Malta's EU reporting 15 [2, 7]."),
      P("The RBMP assessment and WSC's 2025 production figures cover different measures and periods. A lower utility "
        "abstraction can help relieve pressure, but proving a change in aquifer status requires comparable monitoring "
        "of recharge, water levels, salinity and chemical quality. The plan itself notes that future quantitative "
        "assessments were expected to benefit from improved direct monitoring networks [2].")]

S += [CondPageBreak(120 * mm), SectionHeading(5, "What the research says"),
      P("Peer-reviewed research on Malta's aquifers is limited. We checked three studies on Crossref and read the two "
        "that are legally accessible; the third [11] is closed access and is not used."),
      P("<b>Groundwater moves slowly.</b> A British Geological Survey and Malta Resources Authority study dated "
        "groundwater with chemical and isotope tracers. Water in the saturated zone of the Malta Mean Sea Level aquifer "
        "had travel times of 15–40 years, and on Gozo from 25 to possibly more than 60 years. Nitrate held in the rock "
        "matrix moves slowly downwards, “providing a long-term source and sustained concentrations of nitrate”, so the "
        "time it takes measures to work depends on these residence times. The study also describes the water table of "
        "the sea-level aquifer as controlled by abstraction, only up to about 3 m above sea level in places, with "
        "abstraction drawing up saline water [10]. Grade B (observational)."),
      P("<b>The water balance is tight.</b> An overview by an Energy and Water Agency author describes the sea-level "
        "aquifers as freshwater lenses floating on seawater, “highly vulnerable to sea-water intrusion in response to "
        "abstraction activities”. It gives the water balance used in Section 3 and reports that groundwater abstracted "
        "for municipal supply fell from about 21 million m³ in the early 1990s to about 13 million m³ in 2019, which it "
        "links to leakage control [9]. It is a policy overview published in a workshop issue, not an independent "
        "evaluation. Grade C."),
      contested("Does the falling WSC groundwater share show that aquifers are recovering?",
                "SUPPLY MIX IS NOT AQUIFER STATUS", AMBER,
                "WSC's RO share increased and its groundwater production fell, to its lowest in a decade on WSC's "
                "account [1]. Municipal-supply abstraction has fallen by about 8 million m³ since the early 1990s [9]. "
                "Less abstraction is a precondition for recovery.",
                "The 2025 cut is about 4% of national abstraction, which is near or above the estimated available "
                "resource [8, 9]. Agricultural abstraction rose in 2024. All 15 bodies were last assessed as poor, and "
                "water-quality changes take years to decades to show [2, 7, 10].",
                "The production evidence supports lower WSC reliance in 2025. It does not establish aquifer recovery "
                "or improved groundwater quality, and the research says one year of data could not.")]

S += [CondPageBreak(50 * mm), SectionHeading(6, "The Għar Lapsi tender"),
      P("On 25 August 2026, WSC said it had issued a €35 million tender for Plant B at the existing Għar Lapsi RO "
        "facility. The planned plant comprises six systems with a combined production capacity of 30,000 m³/day. The "
        "EU procurement notice records procedure WSC/T/064/2026, published on 28 August, with a 30 October 2026 "
        "submission deadline [4–5]."),
      callout([P("PLANNED CAPACITY IS NOT OUTPUT", tag),
               P("The tender is an official procurement step. It is not a signed contract, completed plant or measured "
                 "increase in potable production. The plant's future effect on groundwater abstraction and aquifer "
                 "status will require separate monitoring.", lead)], bg=AMBER_PALE, bar=AMBER),
      Spacer(1, 3 * mm),
      P("WSC describes the procurement as part of a wider capacity programme. This check records the plant's proposed "
        "design capacity, not a forecast of how much water it will supply or how it will change total groundwater "
        "use.")]

S += [CondPageBreak(120 * mm), SectionHeading(7, "Verdict and limits"),
      verdict_box("Largely supported", "RO's share rose and WSC groundwater production fell; aquifer recovery is not "
                                       "established."),
      Spacer(1, 3 * mm),
      P("WSC's 2025 figures support a higher RO share and lower groundwater production in its potable supply system. "
        "The 2025 groundwater total was the lowest in a decade according to WSC. The new Għar Lapsi Plant B was "
        "tendered, with a stated capacity of 30,000 m³/day. Confidence is moderate because the one-year percentage "
        "differs slightly between the report's prose and chart, the decade comparison rests on WSC's own series, and "
        "the RBMP assessment is not contemporaneous with the 2025 production data."),
      P("This verdict does not say that RO production has restored groundwater bodies. WSC's 2025 cut is about 4% of "
        "national abstraction, which a published water balance puts near or above the available resource; the latest "
        "status assessments report both main aquifers poor quantitatively (four bodies in Malta's EU reporting) and "
        "none of the 15 bodies in good status; and the research shows that changes in the sea-level aquifers take "
        "years to decades to appear. The national data and the research do not change the verdict on WSC's own "
        "figures; they strengthen the caution against reading them as recovery."),
      KeepTogether([P("Evidence needed for an aquifer-recovery claim", h2),
                    requests_list([
                        "Publish annual abstraction and recharge by groundwater body and by user sector, metered where "
                        "possible, with methods and uncertainty.",
                        "Provide comparable water-level, salinity and nitrate series before and after changes in the "
                        "public supply mix.",
                        "Publish a reconciled 2024–2025 groundwater production figure, explain the 11.4% versus 11.86% "
                        "difference, and publish the ten-year series behind “lowest in a decade”.",
                        "After Plant B is commissioned, report its actual output, energy use and any corresponding "
                        "changes in WSC groundwater production.",
                    ])]),
      Spacer(1, 3 * mm),
      callout([P("RIGHT OF REPLY", tag),
               P("Before wider circulation this draft should be sent to the Water Services Corporation and the Energy "
                 "and Water Agency with a fixed deadline (suggested 14 days). Responses will be appended and the "
                 "verdict revisited.", small)], bg=AMBER_PALE, bar=AMBER),
      Spacer(1, 3 * mm)]
LIM = [P("Limitations", h2)]
for l in ["The RBMP is the latest completed national assessment located, but it is older than the 2025 production "
          "data, and its Chapter 6 tables could not be re-opened (ERA blocks automated access).",
          "National abstraction and recharge are Eurostat estimates; agricultural abstraction in particular is "
          "estimated, not fully metered. No 2025 national figures are yet published.",
          "The available-resource figure (37 million m³) is a long-term estimate from a different method and period "
          "than Eurostat's recharge series; it is shown as a reference, not a threshold.",
          "Stuart et al. was read as the authors' accepted manuscript, not the publisher's version. A third study "
          "[11] could not be read.",
          "This report does not attribute any change in aquifer status to the proposed plant."]:
    LIM.append(P("• " + l, bul))
S.append(KeepTogether(LIM))

S += [CondPageBreak(60 * mm), SectionHeading(8, "Sources"),
      *references([
          (1, "Water Services Corporation, Annual Report 2025, pp. 40–43 (RO share and groundwater production).",
           "https://parlament.mt/media/139352/wsc-annual-report-2025.pdf"),
          (2, "ERA and Energy & Water Agency, 3rd River Basin Management Plan for Malta, Chapter 6: Assessment of "
              "Status.", "https://era.org.mt/wp-content/uploads/2023/09/3rd-River-Basin-Management-Plan-MALTA-Chapter-6-Assessment-of-Status-Final.pdf"),
          (3, "Water Services Corporation, Annual Report 2024, p. 42 (groundwater production and source redistribution).",
           "https://www.parlament.mt/media/134182/wsc-annual-report-2024.pdf"),
          (4, "Water Services Corporation, WSC issues €35 million tender for new Għar Lapsi reverse osmosis plant, "
              "25 August 2026.", "https://www.wsc.com.mt/wsc-issues-e35-million-tender-for-new-ghar-lapsi-reverse-osmosis-plant/"),
          (5, "Publications Office of the European Union, WSC/T/064/2026 procurement notice, 28 August 2026.",
           "https://op.europa.eu/en/web/public-procurement/procurement-details/-/procurement/c70c57b4-61a5-4c26-a365-dc44067d6687"),
          (6, "Water Services Corporation, Annual Report 2022 (2022 production figures; original 64% RO figure).",
           "https://www.wsc.com.mt/wp-content/uploads/2023/06/WSC-Annual-Report-2022.pdf"),
          (7, "European Environment Agency, WISE Water Framework Directive reporting, groundwater bodies, 3rd RBMP "
              "(WFD2022_GroundWaterBody_WM, layer 0, Malta), with the 2nd-cycle layer (WFD2016) for comparison. "
              "Retrieved 5 October 2026; extracts in data/cc-009/wise_gwb_status.csv and wise_gwb_2022.geojson.",
           "https://water.discomap.eea.europa.eu/arcgis/rest/services/WISE_WFD/WFD2022_GroundWaterBody_WM/MapServer/0"),
          (8, "Eurostat, Annual freshwater abstraction by source and sector (env_wat_abs, updated 16 September 2026) and "
              "Renewable freshwater resources (env_wat_res, updated 3 July 2026), Malta. Retrieved 5 October 2026; "
              "extract with flags in data/cc-009/eurostat_water.csv.",
           "https://ec.europa.eu/eurostat/databrowser/view/env_wat_abs/default/table"),
          (9, "Sapiano M. (2020). Integrated Water Resources Management in the Maltese Islands. <i>Acque Sotterranee – "
              "Italian Journal of Groundwater</i> 9(3):25–32. doi:10.7343/as-2020-477. (Read in full; open access.)",
           "https://doi.org/10.7343/as-2020-477"),
          (10, "Stuart M.E., Maurice L., Heaton T.H.E., Sapiano M., Micallef Sultana M., Gooddy D.C., Chilton P.J. "
               "(2010). Groundwater residence time and movement in the Maltese islands – a geochemical approach. "
               "<i>Applied Geochemistry</i> 25(5):609–620. doi:10.1016/j.apgeochem.2009.12.010. (Read in full as the "
               "authors' accepted manuscript: nora.nerc.ac.uk/id/eprint/9619.)",
           "https://doi.org/10.1016/j.apgeochem.2009.12.010"),
          (11, "Mangion J., Sapiano M. (2008). The Mean Sea Level Aquifer, Malta and Gozo. In <i>Natural Groundwater "
               "Quality</i>, pp. 404–420. Blackwell. doi:10.1002/9781444300345.ch19. (Not read; closed access; not "
               "used for any finding.)", "https://doi.org/10.1002/9781444300345.ch19"),
          (12, "Miżien. Scripts and outputs: tools/cc-009-report/fetch_data.py, figures.py; data/cc-009/calc.py, "
               "checks.csv.", ""),
      ]),
      Spacer(1, 4 * mm),
      P("Version 1.2 · 5 October 2026 · Draft pending right of reply · Calculations: data/cc-009/checks.csv", cap),
      Spacer(1, 4 * mm),
      *revision_log([
          ("1.0", "3 Oct 2026", "First issue."),
          ("1.1", "5 Oct 2026", "Corrections: (1) Groundwater-body status: the table gave the plan's counts alone "
                                "(quantitative ‘2 poor’, chemical ‘14 poor’). It now shows the plan alongside Malta's "
                                "3rd-cycle EU reporting to the EEA (4 poor quantitatively, 15 poor chemically) and "
                                "states the difference; TL;DR, verdict text and flyer card updated to match. (2) Cover "
                                "verdict line ‘aquifer status remains a separate question’ and flyer ‘aquifer status "
                                "remains poor’ → both ‘aquifers last assessed as poor’. (3) ‘Lowest in a decade’ in the "
                                "TL;DR and section 2 is now attributed to WSC. (4) Reference [6] is now cited in "
                                "section 2; reference [7] added for the EU reporting. Verdict and confidence "
                                "unchanged."),
          ("1.2", "5 Oct 2026", "Upgrade: national abstraction by user and estimated recharge (Eurostat [8]): WSC's "
                                "2025 cut is about 4% of national abstraction; new section 3. Peer-reviewed literature "
                                "verified on Crossref and read [9, 10]; new section 5. Figures 1–3 added (WSC "
                                "production by source; abstraction and recharge; groundwater-body map). Right-of-reply "
                                "status corrected to pending (maintainer, 5 Oct 2026). Verdict and confidence "
                                "unchanged."),
      ])]

build_report(Report(
    number="009", out=str(ROOT / "claims" / "CC-009" / "report.pdf"),
    kicker="Water, Malta", title_lines=["Does more RO", "mean recovery?"],
    subtitle_lines=["Water supply, groundwater status and the", "new Għar Lapsi tender"],
    quote_lines=["“70.7% ... from the four Reverse Osmosis plants”"],
    attribution="Water Services Corporation, Annual Report 2025",
    context="Malta potable supply · 2025 production · August 2026 tender",
    verdict="Largely supported", verdict_note="WSC reliance fell; aquifers last assessed as poor.",
    footer_lines=["Version 1.2  ·  5 October 2026",
                  "Status: draft for right of reply (WSC; Energy and Water Agency)",
                  "Prepared from WSC, Eurostat, EEA and ERA sources and peer-reviewed studies.",
                  "Repository: github.com/leandergrech/Mizien"],
    running_head="Reverse osmosis and groundwater", version="1.2", date="5 October 2026",
    pdf_title="Miżien Claim Check 009 – Does more RO mean recovery?",
    pdf_subject="WSC reverse-osmosis production, groundwater status and Għar Lapsi tender", story=S))
