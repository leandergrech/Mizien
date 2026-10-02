"""Claim Check 006 report. Run data/cc-006/calc.py first."""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

OUT = HERE / "out"
S = []

S += [SectionHeading(None, "TL;DR"), Spacer(1, mm),
      P("Malta’s 2026 spring-hunting regulations define “small numbers” as a sample in the order of 1% of a "
        "population’s total annual mortality. Their own calculations put the Quail benchmark at 2,416 birds and "
        "the Turtle-dove benchmark at 2,510. The national quotas were 2,400 and 1,500 respectively.", lead)]
S.append(key_points([
    ("The legal numbers are reproducible.", "The Quail quota is 99.3% of its stated 1% benchmark; the Turtle-dove quota is 59.8%."),
    ("That is a statutory comparison, not a population survey.", "The legislation defines the reference population as EU regions whose birds mainly pass through Malta. The benchmark is derived from model inputs, not a direct count of birds at Malta."),
    ("Turtle-dove numbers are declining.", "WBRU’s March 2026 status report describes a continuing central-eastern flyway decline and says the latest Article 12 data were still provisional."),
    ("Rules exist; 2026 supervision is not yet independently assessable.", "The law incorporates licence controls. WBRU’s 2025 report documents inspections, spot-checks and offences, but no 2026 outcome report was listed by the review cut-off."),
    ("Verdict: not substantiated for the broader impression.", "The quota sizes sit within the regulation’s mortality benchmark. That alone does not establish ecological sustainability or prove strict supervision in practice."),
]))
S += [Spacer(1, 4 * mm), VerdictMeter(2), Spacer(1, 2 * mm),
      std_table([
          [C("Species", cellh), C("Quota", cellh), C("1% mortality benchmark", cellh), C("Quota / benchmark", cellh)],
          [C("Common Quail"), C("2,400"), C("2,416"), C("99.3%")],
          [C("European Turtle-dove"), C("1,500"), C("2,510"), C("59.8%")],
      ], [43 * mm, 25 * mm, 52 * mm, 50 * mm]),
      Spacer(1, 3 * mm),
      up_down("The 2026 season outcome report, official bag totals, full enforcement records, and final population data for 2019–2024.",
              "Evidence that the legal calculation uses incorrect inputs, quotas exceed the applicable benchmark, or the stated licensing and enforcement controls were not applied."),
      Spacer(1, 5 * mm)]
S += toc([("1", "The wording and laws"), ("2", "How we checked the calculation"), ("3", "What the benchmark does and does not say"),
          ("4", "Supervision: rules and implementation"), ("5", "Verdict, limits and evidence needed"), ("6", "Sources")])
S.append(PageBreak())

S += [SectionHeading(1, "The wording and laws"),
      P("This check assesses whether Malta’s 2026 derogation met both Article 9(1)(c) conditions behind the "
        "“small” and “strictly supervised” description. The Directive permits derogations only under strictly "
        "supervised conditions, on a selective basis, and for birds in small numbers [11]. The exact official "
        "English PDFs for Legal Notices 80 and 81 were opened through Legislation Malta and inspected on "
        "2 October 2026 [1–2]."),
      callout([P("THE LEGAL WORDING", tag),
               P("The “small numbers” requirement “shall be understood as a sample in the order of one percent (1%) "
                 "of the total annual mortality of the population in question”.", lead),
               P("The notices define the population in question by reference to EU regions from which the main "
                 "migratory contingents passing through Malta originate. This is not Malta’s resident population.", small)],
              bg=PALE, bar=GREEN),
      Spacer(1, 3 * mm),
      P("The regulations also set the operative season and national quota. Quail could be hunted from 13 April to "
        "3 May 2026; Turtle-dove from 20 April to 3 May. Both periods ran from two hours before sunrise to noon. "
        "The Minister could terminate a season by notice [1–2]. The separate 17 April Gazette notice authorising "
        "research capture and tagging of four Turtle-doves is not the recreational hunting derogation [3]."),
      P("A contemporaneous MaltaToday report states that Ornis voted for these dates and quotas on 30 March [4]. "
        "The WBRU page lists Ornis minutes only through 2024, so the committee’s original 2026 wording and vote "
        "could not be checked directly. We therefore attribute the tested wording to the enacted regulations, "
        "not to an unpublished committee minute.")]

S += [Spacer(1, 3 * mm), SectionHeading(2, "How we checked the calculation"),
      P("We transcribed the mortality estimates and quotas printed in each regulation, then recalculated the quota "
        "as a share of total annual mortality and as a share of the regulation’s rounded 1% benchmark. Inputs and "
        "formulas are in <i>data/cc-006/checks.csv</i>; the calculation is reproducible with "
        "<i>data/cc-006/calc.py</i>. Values are rounded to one decimal place in this report."),
      std_table([
          [C("Species", cellh), C("Modelled annual mortality", cellh), C("1% printed in law", cellh), C("Quota", cellh), C("Quota / mortality", cellh), C("Quota / 1%", cellh)],
          [C("Common Quail"), C("241,638"), C("2,416"), C("2,400"), C("0.993%"), C("99.3%")],
          [C("European Turtle-dove"), C("251,032"), C("2,510"), C("1,500"), C("0.598%"), C("59.8%")],
      ], [35 * mm, 31 * mm, 25 * mm, 20 * mm, 29 * mm, 30 * mm]),
      Spacer(1, 3 * mm),
      P("<b>Evidence grades.</b> Legal Notices and WBRU technical reports: C (official regulatory or monitoring "
        "records). The 2016 peer-reviewed harvest analysis: B, but its estimates are historical and have wide "
        "uncertainty. FKNK and BirdLife Malta monitoring statements: D for independent inference; they are used "
        "to identify each organisation’s position and observations, not as population estimates.")]

S += [PageBreak(), SectionHeading(3, "What the benchmark does and does not say"),
      P("On the statutory calculation, both quotas are at or below the legal order-of-1% mortality benchmark. "
        "The Quail limit is close to the full benchmark; the Turtle-dove limit is about three-fifths of it. "
        "That comparison supports the limited statement that the quotas were set within the benchmark written "
        "into the regulations [1–2]."),
      P("It does not establish how many birds actually crossed Malta, how many were killed, or what fraction of a "
        "population can withstand the added mortality. The reference population is defined across EU source regions. "
        "A calculated cap is not a field count and is not a direct test of population response."),
      P("The March 2026 WBRU assessment reports an 11% Pan-European decline in Turtle-doves over 2015–2024 and "
        "an 88% decline since 1980. It says the central-eastern flyway continued to decline and that the latest "
        "Article 12 submissions were provisional at the time of assessment [5]. This is material context for "
        "conservation risk; it does not by itself show that the specific 2026 quota exceeded the statutory formula."),
      P("Caruana-Galizia and Fenech’s peer-reviewed study compared spring and autumn harvest and estimated historic "
        "effects from hunter records and independent harvest figures [6]. The independent series covers 1980–1992; "
        "its population denominators are older and its estimates have wide error margins. We do not apply its "
        "historic percentages to the 2026 quotas."),
      callout([P("KEEP THESE QUESTIONS SEPARATE", tag),
               P("<b>Legal benchmark:</b> do quotas fit the 1% mortality formula printed in the notices? Yes, on "
                 "the Government’s own inputs. <b>Ecological sustainability:</b> do current population data show "
                 "that this additional mortality is sustainable? The quota calculation alone cannot answer that.", small)],
              bg=AMBER_PALE, bar=AMBER)]

S += [Spacer(1, 2 * mm), SectionHeading(4, "Supervision: rules and implementation"),
      contested("What can the public record establish?", "IMPLEMENTATION DATA INCOMPLETE", AMBER,
        "The 2026 regulations make the season subject to the established framework and Special Hunting Licence "
        "conditions. The latest WBRU outcome report available at review records 1,336 patrols/field inspections, "
        "909 spot-checks and 19 detected offences during the 2025 spring season [7]. This is evidence of an "
        "enforcement operation in 2025.",
        "The 2025 counts do not establish 2026 supervision. BirdLife Malta’s April/May 2026 reports describe "
        "field observations and suspected illegal targeting; they are stakeholder monitoring accounts, not an "
        "official or independently audited enforcement total [8–9]. The WBRU archive did not list a 2026 outcome "
        "report at the 2 October 2026 cut-off.",
        "Rules and patrol counts describe controls and activity, not whether all hunting was compliant. The 2026 "
        "implementation question remains open until WBRU publishes season data and incident outcomes."),
      Spacer(1, 3 * mm),
      P("FKNK’s 7 April statement says it would conduct surveys to estimate a “sustainability index” and invite "
        "members to submit voluntary forms recording the sex of harvested birds [10]. This is useful evidence of "
        "a stakeholder monitoring initiative, but voluntary member records are not a substitute for official "
        "bag-reporting and enforcement data. The existence of a survey does not demonstrate strict supervision."),
      P("The original candidate summary bundled the statutory mortality benchmark with a broad claim about strict "
        "supervision. The evidence supports the benchmark arithmetic; the public record available for this check "
        "does not establish the 2026 enforcement outcome. The two conclusions should not be collapsed.")]

S += [PageBreak(), SectionHeading(5, "Verdict, limits and evidence needed"),
      verdict_box("Not substantiated", "The statutory quota comparison checks out; 2026 supervision and ecological effect remain unproven."),
      Spacer(1, 3 * mm),
      P("<b>Why.</b> The regulations set quotas below the 1% mortality benchmark they define as “small numbers”. "
        "The Quail quota is 99.3% of the stated benchmark; the Turtle-dove quota is 59.8%. But those ratios only "
        "confirm consistency with the regulations’ own mortality model. They do not show current harvest impact "
        "or prove that the season was strictly supervised in practice. The latest official season-outcome data "
        "available at review are for 2025. For the broader characterization “very small and strictly supervised”, "
        "the evidence available is incomplete, so the verdict is Not substantiated (moderate confidence)."),
      P("<b>What this verdict does not say.</b> It does not say the legal notices’ arithmetic is wrong, that the "
        "quotas were exceeded, or that the derogation was unlawful. The 2026 outcome and final population data "
        "could change the assessment."),
      P("Evidence that would settle the open parts", h2),
      requests_list([
          "The 30 March 2026 Ornis minutes or another primary record of the vote and recommendations.",
          "WBRU’s 2026 outcome report, with actual bag totals, licence-holder reporting, inspections, detected offences and outcomes.",
          "The final 2019–2024 Article 12 population data and transparent derivation of each mortality input.",
          "The FKNK survey protocol, raw anonymised results and independent validation of its “sustainability index”.",
      ]),
      Spacer(1, 3 * mm),
      P("<b>Right of reply.</b> Not sought in this draft, at the maintainer’s direction. Handle before wider circulation.", small),
      Spacer(1, 3 * mm), SectionHeading(6, "Sources"),
      *references([
          (1, "Government of Malta, L.N. 80/2026, Quail, regulations 3–7.", "https://legislation.mt/eli/ln/2026/80/eng"),
          (2, "Government of Malta, L.N. 81/2026, Turtle-dove, regulations 3–7.", "https://legislation.mt/eli/ln/2026/81/eng"),
          (3, "Government Gazette No. 21,626, Notice 622, 17 April 2026 (separate research-capture derogation).", "https://www.gov.mt/en/Government/DOI/Government%20Gazette/Government%20Notices/Pages/2026/04/GovNotices1704extra.aspx"),
          (4, "MaltaToday, “Ornis Committee votes in favour of opening spring hunting season”, 30 March 2026 (secondary account).", "https://www.maltatoday.com.mt/news/national/140671/ornis_committee_votes_in_favour_of_opening_spring_hunting_season_"),
          (5, "WBRU, Conservation Status of Common Quail and European Turtle-dove, March 2026.", "https://wbru.gov.mt/wp-content/uploads/2026/04/Conservation-Status-of-Common-Quail-and-Turtle-Dove-Mar-2026.pdf"),
          (6, "Caruana-Galizia & Fenech, Bird Conservation International 26(1), 29–38 (2016), DOI 10.1017/S0959270915000325.", "https://doi.org/10.1017/S0959270915000325"),
          (7, "WBRU, Report on the Outcome of the 2025 Spring Hunting Season in Malta, June 2025.", "https://wbru.gov.mt/wp-content/uploads/2026/04/2025-SH-Derogation-Report.pdf"),
          (8, "BirdLife Malta, “Majority of hunters illegally target Turtle-doves during first week of spring season”, 20 April 2026.", "https://birdlifemalta.org/2026/04/majority-of-hunters-illegally-target-turtle-doves-during-first-week-of-spring-season/"),
          (9, "BirdLife Malta, “On the Frontlines: May 2026 Newsletter”, 13 May 2026.", "https://birdlifemalta.org/2026/05/on-the-frontlines-may-2026-newsletter/"),
          (10, "FKNK, “Spring hunting season in the Maltese Islands 2026: The FKNK will again carry out scientific studies”, 7 April 2026.", "https://www.huntinginmalta.org.mt/post/spring-hunting-season-in-the-maltese-islands-2026the-fknk-will-again-carry-out-scientific-studies"),
          (11, "Directive 2009/147/EC on the conservation of wild birds, Article 9(1)(c).", "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32009L0147"),
      ]),
      Spacer(1, 4 * mm),
      P("Version 1.0 · 2 October 2026 · Draft pending right of reply · Calculations: data/cc-006/checks.csv · "
        "Report generator: tools/cc-006-report/build_report.py", cap)]

build_report(Report(
    number="006", out=str(OUT / "report.pdf"), kicker="Nature and wildlife, Malta",
    title_lines=["What does ‘small", "numbers’ mean?"],
    subtitle_lines=["Malta’s 2026 spring-hunting quotas, checked against", "their statutory mortality benchmark"],
    quote_lines=["“Under strictly supervised conditions ... in small numbers”"],
    attribution="Directive 2009/147/EC, Article 9(1)(c)",
    context="Malta’s 2026 quotas: 2,400 Quail · 1,500 Turtle-doves",
    verdict="Not substantiated",
    verdict_note="The arithmetic checks out; wider claims do not.",
    footer_lines=["Miżien · independent, science-first fact-checking", "Draft for review · right of reply remains with the maintainer"],
    running_head="2026 spring-hunting derogation",
    version="1.0", date="2 October 2026",
    pdf_title="Miżien Claim Check 006 – What does small numbers mean?",
    pdf_subject="The 2026 Malta spring hunting derogation's mortality benchmark, quotas and supervision",
    story=S,
))
