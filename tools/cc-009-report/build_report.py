"""Build the CC-009 reverse-osmosis and groundwater report."""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

S = [SectionHeading(None, "TL;DR"), Spacer(1, mm),
     P("WSC's latest annual report says reverse osmosis supplied 70.7% of its potable-water production in 2025. Its groundwater component fell to 11.5 million m³, the lowest annual total in a decade. But these are WSC production figures, not proof that Malta's aquifers have recovered.", lead)]
S.append(key_points([
    ("The source mix changed.", "RO rose from 64.3% of WSC production in 2022 to 70.7% in 2025; WSC groundwater production fell 8.95% over those years."),
    ("One percentage does not reconcile.", "WSC's 2025 prose says groundwater fell 11.4% from 2024; the annual-report chart values imply 11.86%. Both are reported transparently."),
    ("Aquifer status is a separate measure.", "The latest River Basin Management Plan identifies poor quantitative status in both main aquifer systems and poor chemical status in 14 groundwater bodies."),
    ("The nitrate claim needs precision.", "The plan says 12 of 15 bodies exceed the 50 mg/L nitrate standard; three named bodies are exceptions. Nitrate is not the only cause of poor groundwater status."),
    ("The plant is tendered, not operating.", "WSC issued a tender for Plant B at Għar Lapsi, planned for 30,000 m³/day. Bids are due 30 October 2026."),
]))
S += [Spacer(1, 2 * mm), VerdictMeter(1), Spacer(1, 2 * mm),
      tiles([("70.7%", GREEN, "WSC production from RO, 2025"),
             ("11.5m m³", ORANGE, "WSC groundwater production, 2025"),
             ("2", RED, "main aquifer systems poor quantitatively")]),
      Spacer(1, 3 * mm),
      up_down("A new, comparable groundwater-status assessment; full national abstraction and recharge data; and the new plant's commissioned output and its measured effects on WSC abstraction and aquifer levels.",
              "Evidence that WSC's 2025 mix, production series or procurement status is materially different from the official records."),
      Spacer(1, 4 * mm),
      *toc([("1", "What WSC reported"), ("2", "Rechecking the production series"),
            ("3", "Groundwater-body status"), ("4", "The Għar Lapsi tender"),
            ("5", "Verdict and limits"), ("6", "Sources")]), PageBreak()]

S += [SectionHeading(1, "What WSC reported"),
      P("WSC's Annual Report 2025 says 70.7% of its 39.5 million m³ of potable-water production came from four reverse-osmosis plants. It reports 11.5 million m³ of groundwater production, the lowest total in the previous decade, and says the volume was 11.4% lower than in 2024. WSC links the shift to blending for lower salinity in reservoirs [1]."),
      callout([P("KEEP THE MEASURES DISTINCT", tag),
               P("RO share and WSC groundwater production describe the utility's potable supply. Groundwater-body status compares aquifer quantity and quality against environmental criteria. Neither measure can substitute for the other.", lead)], bg=PALE, bar=GREEN),
      Spacer(1, 3 * mm),
      P("The 2025 report identifies taste and salinity as the immediate reason for increasing the RO proportion. Its statements therefore support reduced WSC reliance on groundwater in the production mix; they do not say that the aquifers had returned to good status."),
      P("The 2024 report provides useful context: it described groundwater production as fairly constant while abstraction sources were redistributed, and explained that WSC was reactivating sources to relieve localised pressure. A single year's decline should not be treated as evidence of a sustained aquifer trend [3].")]

S += [PageBreak(), SectionHeading(2, "Rechecking the production series"),
      P("We transcribed the annual RO and groundwater values shown in Figure 20 of WSC's 2025 report and recalculated totals, source shares and changes. The script is `data/cc-009/calc.py`; the inputs and outputs are in `data/cc-009/`."),
      std_table([
          [C("Year", cellh), C("RO (million m³)", cellh), C("Groundwater (million m³)", cellh), C("RO share", cellh)],
          [C("2022"), C("22.85"), C("12.68"), C("64.3%")],
          [C("2023"), C("23.70"), C("13.16"), C("64.3%")],
          [C("2024"), C("25.74"), C("13.09"), C("66.3%")],
          [C("2025"), C("27.92"), C("11.54"), C("70.7%")],
      ], [22 * mm, 38 * mm, 62 * mm, CW - 122 * mm]),
      Spacer(1, 3 * mm),
      P("From 2022 to 2025, WSC's groundwater component decreased by 8.95%, while its RO share rose by 6.43 percentage points. WSC's 2025 report narrative says the one-year groundwater decline was 11.4%. The 2024 and 2025 chart entries (13,094,325 m³ and 11,541,256 m³) imply 11.86%. The difference is small but unresolved, so this report does not silently substitute one figure for the other [1]."),
      P("These figures describe water produced for the WSC potable network. They do not include all groundwater abstraction for every use, and they do not measure aquifer recharge, groundwater levels, salinity or nitrate concentrations."),
      contested("Does the falling WSC groundwater share show that aquifers are recovering?", "SUPPLY MIX IS NOT AQUIFER STATUS", AMBER,
        "WSC's RO share increased and its reported groundwater production fell, with the 2025 total the lowest in a decade. Increasing desalinated production can reduce the groundwater portion of the WSC supply blend [1].",
        "The WSC series measures utility production, not water levels, recharge, chemical quality or total abstraction from each groundwater body. The latest official status assessment still identifies poor quantitative status in both principal aquifers [2].",
        "The production evidence supports lower WSC reliance in 2025. It does not establish aquifer recovery or improved groundwater quality."),
      PageBreak(), SectionHeading(3, "Groundwater-body status"),
      P("The 3rd River Basin Management Plan for 2021–2027 is the latest completed national plan identified on ERA's website. Its Chapter 6 status tables assess 15 groundwater bodies. It reports both the Malta and Gozo Mean Sea Level aquifer systems as poor quantitatively, meaning they are over-abstracted under the plan's water-balance assessment [2]."),
      std_table([
          [C("RBMP indicator", cellh), C("Result", cellh), C("Meaning", cellh)],
          [C("Overall groundwater status"), C("15 of 15 poor"), C("Overall good status requires both quantity and quality to pass.")],
          [C("Quantitative status"), C("2 poor"), C("Malta and Gozo Mean Sea Level aquifers.")],
          [C("Chemical status"), C("14 poor"), C("Nitrate is the main failing parameter, but not the only one.")],
          [C("Nitrate standard"), C("12 of 15 exceed 50 mg/L"), C("Gozo Mean Sea Level, Comino Mean Sea Level and Mellieħa Perched are named exceptions.")],
      ], [44 * mm, 37 * mm, CW - 81 * mm]),
      Spacer(1, 3 * mm),
      P("The queue note said all groundwater bodies fail on nitrates. The plan does not say that: it names three bodies that do not exceed the 50 mg/L nitrate standard. Fourteen bodies fail chemical status overall, a broader assessment that includes other factors such as saline intrusion [2]."),
      P("The RBMP assessment and WSC's 2025 production figures cover different measures and periods. A lower utility abstraction can help relieve pressure, but proving a change in aquifer status requires comparable monitoring of recharge, water levels, salinity and chemical quality. The plan itself notes that future quantitative assessments were expected to benefit from improved direct monitoring networks [2].")]

S += [PageBreak(), SectionHeading(4, "The Għar Lapsi tender"),
      P("On 25 August 2026, WSC said it had issued a €35 million tender for Plant B at the existing Għar Lapsi RO facility. The planned plant comprises six systems with a combined production capacity of 30,000 m³/day. The EU procurement notice records procedure WSC/T/064/2026, published on 28 August, with a 30 October 2026 submission deadline [4–5]."),
      callout([P("PLANNED CAPACITY IS NOT OUTPUT", tag),
               P("The tender is an official procurement step. It is not a signed contract, completed plant or measured increase in potable production. The plant's future effect on groundwater abstraction and aquifer status will require separate monitoring.", lead)], bg=AMBER_PALE, bar=AMBER),
      Spacer(1, 3 * mm),
      P("WSC describes the procurement as part of a wider capacity programme. This check records the plant's proposed design capacity, not a forecast of how much water it will supply or how it will change total groundwater use.")]

S += [PageBreak(), SectionHeading(5, "Verdict and limits"),
      verdict_box("Largely supported", "RO's share rose and WSC groundwater production fell; aquifer recovery is not established."),
      Spacer(1, 3 * mm),
      P("WSC's 2025 figures support a higher RO share and lower groundwater production in its potable supply system. The 2025 groundwater total was the lowest in a decade according to WSC. The new Għar Lapsi Plant B was tendered, with a stated capacity of 30,000 m³/day. Confidence is moderate because the one-year percentage differs slightly between the report's prose and chart, and the RBMP assessment is not contemporaneous with the 2025 production data."),
      P("This verdict does not say that RO production has restored groundwater bodies. The latest RBMP reports both main aquifers in poor quantitative status, 14 bodies in poor chemical status and 12 of 15 exceeding the nitrate standard. WSC production is not a national all-user abstraction dataset, and a tender is not an operating plant."),
      P("Evidence needed for an aquifer-recovery claim", h2),
      requests_list([
          "Publish annual abstraction and recharge by groundwater body and by user sector, with methods and uncertainty.",
          "Provide comparable water-level, salinity and nitrate series before and after changes in the public supply mix.",
          "Publish a reconciled 2024–2025 groundwater production figure and explain the 11.4% versus 11.86% difference.",
          "After Plant B is commissioned, report its actual output, energy use and any corresponding changes in WSC groundwater production.",
      ]),
      Spacer(1, 3 * mm),
      P("<b>Right of reply.</b> Not sought in this draft, at the maintainer's direction.", small),
      P("<b>Limitations.</b> The RBMP provides the latest completed national assessment located, but it is older than the 2025 production data. This report does not estimate private or agricultural abstraction or attribute aquifer status change to the proposed plant.", small),
      PageBreak(), SectionHeading(6, "Sources"),
      *references([
          (1, "Water Services Corporation, Annual Report 2025, pp. 40–43 (RO share and groundwater production).", "https://parlament.mt/media/139352/wsc-annual-report-2025.pdf"),
          (2, "ERA and Energy & Water Agency, 3rd River Basin Management Plan for Malta, Chapter 6: Assessment of Status.", "https://era.org.mt/wp-content/uploads/2023/09/3rd-River-Basin-Management-Plan-MALTA-Chapter-6-Assessment-of-Status-Final.pdf"),
          (3, "Water Services Corporation, Annual Report 2024, p. 42 (groundwater production and source redistribution).", "https://www.parlament.mt/media/134182/wsc-annual-report-2024.pdf"),
          (4, "Water Services Corporation, WSC issues €35 million tender for new Għar Lapsi reverse osmosis plant, 25 August 2026.", "https://www.wsc.com.mt/wsc-issues-e35-million-tender-for-new-ghar-lapsi-reverse-osmosis-plant/"),
          (5, "Publications Office of the European Union, WSC/T/064/2026 procurement notice, 28 August 2026.", "https://op.europa.eu/en/web/public-procurement/procurement-details/-/procurement/c70c57b4-61a5-4c26-a365-dc44067d6687"),
          (6, "Water Services Corporation, Annual Report 2022 (original 64% RO figure).", "https://www.wsc.com.mt/wp-content/uploads/2023/06/WSC-Annual-Report-2022.pdf"),
      ]),
      Spacer(1, 4 * mm),
      P("Version 1.0 · 3 October 2026 · Draft pending right of reply · Calculations: data/cc-009/checks.csv", cap)]

build_report(Report(
    number="009", out=str(ROOT / "claims" / "CC-009" / "report.pdf"),
    kicker="Water, Malta", title_lines=["Does more RO", "mean recovery?"],
    subtitle_lines=["Water supply, groundwater status and the", "new Għar Lapsi tender"],
    quote_lines=["“70.7% ... from the four Reverse Osmosis plants”"],
    attribution="Water Services Corporation, Annual Report 2025",
    context="Malta potable supply · 2025 production · August 2026 tender",
    verdict="Largely supported", verdict_note="WSC reliance fell; aquifer status remains a separate question.",
    footer_lines=["Miżien · independent, science-first fact-checking", "Draft for review · right of reply remains with the maintainer"],
    running_head="Reverse osmosis and groundwater", version="1.0", date="3 October 2026",
    pdf_title="Miżien Claim Check 009 – Does more RO mean recovery?",
    pdf_subject="WSC reverse-osmosis production, groundwater status and Għar Lapsi tender", story=S))
