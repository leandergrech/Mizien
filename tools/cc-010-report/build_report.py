"""Build the CC-010 report using the shared Miżien report design. Run data/cc-010/calc.py and figures.py first."""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

S = [SectionHeading(None, "TL;DR"), Spacer(1, mm),
     P("Project Green reported more than 8,000 trees and more than 25,000 shrubs planted by government entities in 2024. The 2022 Labour manifesto separately pledged 100,000 trees over five years. In February 2026, the Environment Minister told Parliament that relevant government entities had planted around 60,000 trees and over 100,000 shrubs through the end of 2025.", lead),
     P("<b>Counts confirmed; the 100,000 trees were not reached by the end of 2025, and no later count shows them "
       "reached before the legislature ended.</b> The official figures support the stated planting totals, but they "
       "are not a surviving-tree count. The roughly 60,000 trees equal about 60% of the pledge at the end-2025 "
       "checkpoint, when about three-quarters of the five-year period had passed; Labour's own 2026 manifesto gives a "
       "lower figure, more than 57,000. The legislature ended with a snap general election on 30 May 2026. The record "
       "does not show that tree canopy increased.", body)]
S.append(key_points([
    ("The 2024 figures are distinct.", "Project Green reported over 8,000 trees and over 25,000 shrubs. Shrubs are not trees and are not added to the manifesto target."),
    ("The pledge is real and time-bound.", "Pledge 305 in the Labour manifesto committed to 100,000 trees in the next five years, from March 2022. The legislature ended early, with a snap general election on 30 May 2026."),
    ("The latest official progress figure is partial.", "A parliamentary answer reports around 60,000 trees and over 100,000 shrubs by end-2025. It gives no project-level inventory. Labour's 2026 manifesto reports more than 57,000 trees for 2022–2025."),
    ("Delivery of the pledge is not substantiated.", "It is rated separately: about 60% of the trees by end-2025, with 75% of the time gone, and no later count. The verdict on the counts is unchanged."),
    ("Planting is not survival.", "Neither source provides a survival rate or a national cohort inventory; Mediterranean field studies show survival depends on species, site and method."),
]))
S += [Spacer(1, 2 * mm), VerdictMeter(1), Spacer(1, 2 * mm),
      tiles([(">8,000", GREEN, "trees reported in 2024"),
             ("~60,000", ORANGE, "trees reported by end-2025"),
             ("60% / 75%", RED, "of the 100,000 trees, against the share of the five years gone (end-2025)")]),
      Spacer(1, 3 * mm),
      up_down("A verified, tree-only planting register for the 2022–2026 legislature, with locations, planting dates and replacements.",
              "Evidence that the official planting totals mix shrubs or vouchers into the tree count, or that the published primary records misstate the quantities."),
      Spacer(1, 4 * mm),
      *toc([("1", "What was said"), ("2", "Checking the counts"),
            ("3", "What planting totals measure"), ("4", "Testing the claim, verdict and limits"),
            ("5", "Sources")]), PageBreak()]

S += [SectionHeading(1, "What was said"),
      P("On 31 December 2024, Project Green reported that more than 8,000 trees had been planted during the year through projects coordinated by entities under the Environment Ministry, and separately that more than 25,000 shrubs had been planted by government entities [1]. The release names Project Green, Ambjent Malta, ERA and GreenServ. These are government-reported totals; the release does not publish a site-by-site list."),
      callout([P("THE PLEDGE", tag),
               P("Pledge 305 of Partit Laburista's 2022 manifesto commits to an action plan for tree planting and afforestation and to 100,000 trees being planted “fil-ħames snin li ġejjin” — in the next five years [2]. The manifesto was published in March 2022, ahead of the general election of 26 March 2022, so five years would run to March 2027. The legislature ended earlier: a snap general election was held on 30 May 2026 [8].", lead)], bg=PALE, bar=GREEN),
      Spacer(1, 3 * mm),
      P("In a written answer to Parliamentary Question 34270, the Environment Minister said that, through the end of 2025, entities under her Ministry and entities under other ministries had together planted around 60,000 trees and more than 100,000 shrubs during the legislature [3]. The answer is broader than Project Green alone and does not break the counts down by agency or project."),
      P("Labour's 2026 election manifesto gives the party's own count: “Bejn l-2022 u l-2025 tħawlu aktar minn 57,000 siġra” — between 2022 and 2025, more than 57,000 trees were planted [9]. That is lower than the Minister's figure of around 60,000 for a similar period. Both figures are approximate, and neither document reconciles them."),
      P("The two annual/cumulative statements have different periods and scopes. Do not add the 2024 count to the cumulative 60,000, or add shrubs to either tree figure. The separate private-land voucher scheme announced in 2025–26 is also not counted here: by 13 May 2026, Project Green reported vouchers issued for 23,000 trees to more than 250 beneficiaries, some of them already redeemed [4, 10]. Vouchers issued are not trees planted.")]

S += [PageBreak(), SectionHeading(2, "Checking the counts"),
      P("The calculation in <i>data/cc-010/calc.py</i> divides the Minister's approximate end-2025 tree figure by the manifesto target, and computes the share of the five-year period elapsed from the dates in <i>data/cc-010/dates.csv</i>. It does not assume a straight-line planting schedule or treat the arithmetic balance as a final shortfall."),
      std_table([
          [C("Record", cellh), C("Trees", cellh), C("Shrubs", cellh), C("Interpretation", cellh)],
          [C("Project Green, 2024"), C(">8,000"), C(">25,000"), C("Reported annual planting; government entities.")],
          [C("Parliamentary answer, through 2025"), C("about 60,000"), C(">100,000"), C("Collective figure across relevant ministries.")],
          [C("Labour manifesto, 2026"), C("more than 57,000"), C("—"), C("Party's own count for 2022–2025; lower than the Minister's.")],
          [C("Labour manifesto, 2022"), C("100,000 target"), C("—"), C("Planting commitment over the next five years.")],
      ], [39 * mm, 34 * mm, 34 * mm, CW - 107 * mm]),
      Spacer(1, 3 * mm),
      fig(HERE / "out" / "fig1_pledge.png"),
      P("Figure 1. Left: trees reported against the five years of pledge 305, counted from the 26 March 2022 election; "
        "the dashed line is an even pace to 100,000, for reference only. Right: at the end of 2025, 75% of the window had "
        "passed and about 60% of the trees had been reported (more than 57% on Labour's count). Shrubs and vouchers "
        "are not trees planted and are kept out [1–4, 8–10].", cap),
      P("The figures are approximate and stop at the end of 2025. A rounded 60,000 is about 60% of the 100,000 pledge; subtracting it leaves about 40,000 trees. Counted from the general election of 26 March 2022, about 75% of the five-year period had passed by the end of 2025, and about 84% by the snap election of 30 May 2026, which ended the legislature [8]. No later count was found: Project Green's news from the election to 5 October 2026 reports gardens and open spaces but no tree total, and Parliament's website could not be searched by script. The arithmetic is therefore a checkpoint. It does not show delivery, which is rated not substantiated in Section 4, and it does not prove a final shortfall either."),
      contested("Do the published planting totals show that the pledge has been delivered?", "NOT SUBSTANTIATED", ORANGE,
        "The Minister reported around 60,000 trees planted collectively through the end of 2025, and Project Green separately reported more than 8,000 trees planted in 2024 [1, 3].",
        "The reported cumulative count is below 100,000 and approximate. It stops at the end of 2025, five months before the 30 May 2026 election ended the legislature; no 2026 total or reconciliation to pledge 305 was located [2, 3, 8].",
        "The count establishes interim reported progress, not delivery of 100,000 trees within the legislature; nor does it prove a final shortfall."), CondPageBreak(110 * mm)]

S += [SectionHeading(3, "What planting totals measure"),
      P("The government records describe numbers planted. They do not report how many trees were alive after establishment, how many were replaced, or how much canopy they produced. Ambjent Malta's 2024 report gives a more detailed but still partial example: it reports 7,380 trees and 13,970 shrubs planted in 2024, and separately 3,209 trees and shrubs in Natura 2000 sites [5]. The protected-site figure is a subset and combines trees with shrubs; it is not a national tree-only total."),
      P("Peer-reviewed Mediterranean research shows why a planting count cannot stand in for survival. A 20-year <i>Pinus halepensis</i> experiment in arid south-eastern Spain found survival differed substantially among shelter treatments; after 20 years, reported survival ranged from 29.5% to 57.5% [6]. A southern Spanish restoration study also found different three-year survival under nurse-based and traditional planting methods [7]. These are evidence that site and method matter, not survival estimates for Malta or for the Government's cohorts."),
      callout([P("WHAT A VERIFIABLE OUTCOME RECORD NEEDS", tag),
               P("For each planting cohort: project and location; species; number planted; planting date; maintenance and replacement; repeated survival checks; and, where the aim is greener public space, measured canopy or habitat change. The sources located for this check do not provide a national linked record of that kind.", lead)], bg=AMBER_PALE, bar=AMBER),
      Spacer(1, 3 * mm),
      P("The EU's MapMyTree register and satellite canopy data could provide separate context, but neither can by itself verify these national programme totals or survival without matched locations and definitions. No such reconciliation is attempted here.")]

verd = lambda t, c: chip(t, c, w=29 * mm)
S += [PageBreak(), SectionHeading(4, "Testing the claim, verdict and limits"),
      std_table([
          [C("Sub-claim", cellh), C("What the evidence shows", cellh), C("Rating", cellh)],
          [C("<b>A.</b> More than 8,000 trees and more than 25,000 shrubs planted by government entities in 2024"),
           C("Stated in Project Green's release [1]; self-reported, with no site list."), verd("SUPPORTED", GREENC)],
          [C("<b>B.</b> Pledge 305: 100,000 trees in the next five years"),
           C("Wording confirmed in the 2022 manifesto, PDF p. 91 [2]."), verd("SUPPORTED", GREENC)],
          [C("<b>C.</b> About 60,000 trees and more than 100,000 shrubs planted through end-2025"),
           C("Stated by the Minister in Parliament [3]; rounded, no project list; Labour's own count is lower, more "
             "than 57,000 [9]."), verd("LARGELY SUPPORTED", colors.HexColor("#8DB36B"))],
          [C("<b>D.</b> Delivery of 100,000 trees within the pledge period"),
           C("About 60,000 (Labour: more than 57,000) by end-2025, when about 75% of the window had elapsed; the "
             "legislature then ended with the 30 May 2026 election, and no later count was found [3, 8, 9]."),
           verd("NOT SUBSTANTIATED", ORANGE)],
      ], [52 * mm, 88 * mm, 30 * mm], valign="MIDDLE"),
      P("The verdict applies to the reported counts, sub-claims A to C, which is the claim as stated. The pledge's "
        "delivery, sub-claim D, is rated separately and does not change it.", cap),
      Spacer(1, 2 * mm),
      verdict_box("Largely supported", "Counts confirmed; the 100,000 trees were not reached by end-2025 (about 60,000), and no later count was found before the legislature ended. Confidence: moderate."),
      Spacer(1, 3 * mm),
      P("Primary records confirm Project Green's 2024 statement of more than 8,000 trees and more than 25,000 shrubs, the 100,000-tree pledge in the 2022 Labour manifesto, and the Minister's approximate cumulative count of around 60,000 trees and more than 100,000 shrubs through end-2025 (Labour's 2026 manifesto gives more than 57,000 trees for 2022–2025). Confidence is moderate because totals are self-reported, rounded and lack a published project-level inventory."),
      P("The pledge is rated separately: delivery of 100,000 trees within the pledge period is not substantiated. The latest cumulative count stops at the end of 2025, when about three-quarters of the five-year period had passed and about 60% of the trees had been reported; the legislature then ended with the snap election of 30 May 2026, and no later count was found. Without a final count this is not proof of a shortfall either. The records do not establish survival, net canopy gain or habitat recovery. The Project Green 2024 and parliamentary figures have different scopes and must not be added together."),
      P("Evidence needed to settle delivery and outcomes", h2),
      requests_list([
          "Publish a tree-only, project-level register for the 2022–2026 legislature, including dates, locations, species and responsible entity.",
          "State whether the 100,000 commitment includes trees planted by other ministries, contractors, private landowners or replacement planting.",
          "Report cohort survival and replacements at comparable intervals; distinguish shrubs and vouchers from planted trees.",
          "Where increased tree cover is the aim, publish comparable canopy measurements rather than using planting totals as a proxy.",
      ]),
      Spacer(1, 3 * mm),
      P("<b>Right of reply.</b> Not sought in this draft, at the maintainer's direction.", small),
      PageBreak(), SectionHeading(5, "Sources"),
      *references([
          (1, "Project Green, ‘Over 8,000 new trees in 2024’, 31 December 2024.", "https://projectgreen.mt/over-8000-new-trees-in-2024/"),
          (2, "Partit Laburista, Malta Flimkien: Manifest Elettorali 2022, pledge 305, printed p. 89 (PDF p. 91).", "https://talk.mt/wp-content/uploads/2022/03/MALTA-FLIMKIEN-MANIFEST-ELETTORALI-2022.pdf"),
          (3, "House of Representatives of Malta, Parliamentary Question 34270, sitting 435, 18 February 2026, p. 25.", "https://www.parlament.mt/media/137706/20260218_435o_par.pdf"),
          (4, "Ministry for the Environment, ‘Distribution of trees begins to the first beneficiaries of the tree-planting initiative’, 15 April 2026. Separate private-land scheme.", "https://www.gov.mt/en/Government/DOI/Press%20Releases/Pages/2026/04/15/PR260616en.aspx"),
          (5, "Ambjent Malta, Annual Report 2024, pp. 49–51.", "https://parlament.mt/media/136607/06228.pdf"),
          (6, "Oliet et al., Frontiers in Forests and Global Change 5 (2023), doi:10.3389/ffgc.2022.1092703.", "https://doi.org/10.3389/ffgc.2022.1092703"),
          (7, "Rey et al., Journal of Applied Ecology 46(4) (2009): 937–945, doi:10.1111/j.1365-2664.2009.01680.x.", "https://doi.org/10.1111/j.1365-2664.2009.01680.x"),
          (8, "IFES ElectionGuide, Malta: Maltese House of Representatives 2026 General (held 30 May 2026; previous election 26 March 2022; results source: Electoral Commission of Malta). Accessed 5 October 2026.", "https://electionguide.org/elections/id/5161/"),
          (9, "Partit Laburista, Int Malta: Manifest Elettorali 2026, item 43, printed p. 168 (PDF p. 170).", "https://partitlaburista.org/wp-content/uploads/2026/08/Manifest_Elettorali_INT_MALTA_2026.pdf"),
          (10, "Project Green, ‘Vouchers continue to be issued to beneficiaries of the Tree Planting Initiative’, 13 May 2026.", "https://projectgreen.mt/vouchers-continue-to-be-issued-to-beneficiaries-of-the-tree-planting-initiative/"),
      ]),
      Spacer(1, 4 * mm),
      P("Version 1.2 · 5 October 2026 · Draft pending right of reply · Calculations: data/cc-010/checks.csv", cap),
      Spacer(1, 4 * mm),
      *revision_log([
          ("1.0", "3 Oct 2026", "First issue. Right of reply not sought, at the maintainer's direction."),
          ("1.1", "5 Oct 2026", "Corrections: the pledge was framed as open until 2027; it now records that the legislature "
           "ended with the snap general election of 30 May 2026 [8] and that about 75% of the five-year period had "
           "passed by end-2025, against about 60% of the trees reported (the “2027 deadline” tile is replaced). Added "
           "Labour's own 2026 manifesto count, more than 57,000 trees for 2022–2025 [9], alongside the Minister's "
           "~60,000. Updated the voucher scheme to 23,000 trees in vouchers issued by 13 May 2026 [10]; vouchers are "
           "not trees planted. Cover note shortened to fit; italics fixed. Verdict and confidence unchanged."),
          ("1.2", "5 Oct 2026", "Upgrade: (1) New Figure 1, trees reported (more than 8,000 in 2024; about 60,000 "
           "and more than 57,000 by end-2025) against the five-year window of pledge 305 (75% elapsed by end-2025; "
           "the 30 May 2026 election at 84%), with shrubs and vouchers kept out; it replaces the Section 2 tiles. (2) "
           "Searched for a count after the 30 May 2026 election (Project Green’s news to 5 October 2026; web "
           "searches): none found. (3) New sub-claim table in Section 4 (A–D); TL;DR, a tile, verdict box, "
           "cover note, flyer and claim.yml updated. Version and date added to the cover."),
          ("1.2", "5 Oct 2026", "Maintainer decision (5 Oct 2026): pledge delivery rated separately as Not "
           "substantiated; overall verdict unchanged."),
      ])]

build_report(Report(
    number="010", out=str(ROOT / "claims" / "CC-010" / "report.pdf"),
    kicker="Land & Trees, Malta", title_lines=["How many trees", "were planted?"],
    subtitle_lines=["Checking government counts against the", "100,000-tree pledge"],
    quote_lines=["“100,000 siġra fil-ħames snin li ġejjin”"],
    attribution="Partit Laburista, 2022 manifesto, pledge 305",
    context="2024 annual count · end-2025 parliamentary answer · snap election 30 May 2026",
    verdict="Largely supported", verdict_note="Counts confirmed; about 60,000 of the 100,000 by end-2025",
    footer_lines=["Version 1.2  ·  5 October 2026", "Miżien · independent, science-first fact-checking",
                  "Draft for review · right of reply remains with the maintainer"],
    running_head="Tree-planting counts", version="1.2", date="5 October 2026",
    pdf_title="Miżien Claim Check 010 – How many trees were planted?",
    pdf_subject="Government-reported planting counts and the Labour 100,000-tree pledge", story=S))
