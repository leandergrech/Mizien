"""Build the CC-010 report using the shared Miżien report design."""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE.parent))
from mizien_report import *  # noqa: E402,F401

S = [SectionHeading(None, "TL;DR"), Spacer(1, mm),
     P("Project Green reported more than 8,000 trees and more than 25,000 shrubs planted by government entities in 2024. The 2022 Labour manifesto separately pledged 100,000 trees over five years. In February 2026, the Environment Minister told Parliament that relevant government entities had planted around 60,000 trees and over 100,000 shrubs through the end of 2025.", lead),
     P("The official figures support the stated planting totals, but they are not a surviving-tree count. The roughly 60,000 trees equal about 60% of the pledge at the end-2025 checkpoint; the five-year pledge period had not elapsed. The record does not establish that the target was ultimately met or that tree canopy increased.", body)]
S.append(key_points([
    ("The 2024 figures are distinct.", "Project Green reported over 8,000 trees and over 25,000 shrubs. Shrubs are not trees and are not added to the manifesto target."),
    ("The pledge is real and time-bound.", "Pledge 305 in the Labour manifesto committed to 100,000 trees in the next five years. From its March 2022 publication, the deadline falls in 2027."),
    ("The latest official progress figure is partial.", "A parliamentary answer reports around 60,000 trees and over 100,000 shrubs by end-2025 across environment and other ministries. It gives no project-level inventory."),
    ("Planting is not survival.", "Neither source provides a survival rate or a national cohort inventory. Mediterranean field studies show that survival depends on species, site and planting method; their rates cannot be transferred to Malta."),
]))
S += [Spacer(1, 2 * mm), VerdictMeter(1), Spacer(1, 2 * mm),
      tiles([(">8,000", GREEN, "trees reported in 2024"),
             ("~60,000", ORANGE, "trees reported by end-2025"),
             ("100,000", RED, "pledged over five years")]),
      Spacer(1, 3 * mm),
      up_down("A verified, tree-only planting register through the pledge deadline, with locations, planting dates and replacements.",
              "Evidence that the official planting totals mix shrubs or vouchers into the tree count, or that the published primary records misstate the quantities."),
      Spacer(1, 4 * mm),
      *toc([("1", "What was said"), ("2", "Checking the counts"),
            ("3", "What planting totals measure"), ("4", "Verdict and limits"), ("5", "Sources")]), PageBreak()]

S += [SectionHeading(1, "What was said"),
      P("On 31 December 2024, Project Green reported that more than 8,000 trees had been planted during the year through projects coordinated by entities under the Environment Ministry, and separately that more than 25,000 shrubs had been planted by government entities [1]. The release names Project Green, Ambjent Malta, ERA and GreenServ. These are government-reported totals; the release does not publish a site-by-site list."),
      callout([P("THE PLEDGE", tag),
               P("Pledge 305 of Partit Laburista's 2022 manifesto commits to an action plan for tree planting and afforestation and to 100,000 trees being planted “fil-ħames snin li ġejjin” — in the next five years [2]. The manifesto was published in March 2022, so the deadline falls in 2027.", lead)], bg=PALE, bar=GREEN),
      Spacer(1, 3 * mm),
      P("In a written answer to Parliamentary Question 34270, the Environment Minister said that, through the end of 2025, entities under her Ministry and entities under other ministries had together planted around 60,000 trees and more than 100,000 shrubs during the legislature [3]. The answer is broader than Project Green alone and does not break the counts down by agency or project."),
      P("The two annual/cumulative statements have different periods and scopes. Do not add the 2024 count to the cumulative 60,000, or add shrubs to either tree figure. The separate private-land voucher scheme announced in 2025–26 is also not counted here as planted trees [4].")]

S += [PageBreak(), SectionHeading(2, "Checking the counts"),
      P("The calculation in `data/cc-010/calc.py` divides the Minister's approximate end-2025 tree figure by the manifesto target. It does not assume a straight-line planting schedule or treat the arithmetic balance as a final shortfall."),
      std_table([
          [C("Record", cellh), C("Trees", cellh), C("Shrubs", cellh), C("Interpretation", cellh)],
          [C("Project Green, 2024"), C(">8,000"), C(">25,000"), C("Reported annual planting; government entities.")],
          [C("Parliamentary answer, through 2025"), C("about 60,000"), C(">100,000"), C("Collective figure across relevant ministries.")],
          [C("Labour manifesto, 2022"), C("100,000 target"), C("—"), C("Planting commitment over the next five years.")],
      ], [39 * mm, 34 * mm, 34 * mm, CW - 107 * mm]),
      Spacer(1, 3 * mm),
      tiles([("~60%", GREEN, "of the 100,000-tree target reported by end-2025"),
             ("~40,000", ORANGE, "arithmetic difference at that checkpoint"),
             ("2027", BLUE, "five-year pledge deadline")]),
      Spacer(1, 3 * mm),
      P("The figures are approximate and stop at the end of 2025. A rounded 60,000 is about 60% of the 100,000 pledge; subtracting it leaves about 40,000 trees. That arithmetic is a checkpoint, not proof of failure: the five-year period had not ended, and the parliamentary answer does not say the final count."),
      contested("Do the published planting totals show that the pledge has been delivered?", "INTERIM COUNT; DEADLINE STILL OPEN", AMBER,
        "The Minister reported around 60,000 trees planted collectively through the end of 2025, and Project Green separately reported more than 8,000 trees planted in 2024 [1, 3].",
        "The reported cumulative count is below 100,000, but it is approximate and precedes the manifesto's five-year deadline in 2027. The response contains no 2026 total or reconciliation to pledge 305 [2, 3].",
        "The count establishes interim reported progress, not final delivery or a final shortfall."), PageBreak()]

S += [SectionHeading(3, "What planting totals measure"),
      P("The government records describe numbers planted. They do not report how many trees were alive after establishment, how many were replaced, or how much canopy they produced. Ambjent Malta's 2024 report gives a more detailed but still partial example: it reports 7,380 trees and 13,970 shrubs planted in 2024, and separately 3,209 trees and shrubs in Natura 2000 sites [5]. The protected-site figure is a subset and combines trees with shrubs; it is not a national tree-only total."),
      P("Peer-reviewed Mediterranean research shows why a planting count cannot stand in for survival. A 20-year *Pinus halepensis* experiment in arid south-eastern Spain found survival differed substantially among shelter treatments; after 20 years, reported survival ranged from 29.5% to 57.5% [6]. A southern Spanish restoration study also found different three-year survival under nurse-based and traditional planting methods [7]. These are evidence that site and method matter, not survival estimates for Malta or for the Government's cohorts."),
      callout([P("WHAT A VERIFIABLE OUTCOME RECORD NEEDS", tag),
               P("For each planting cohort: project and location; species; number planted; planting date; maintenance and replacement; repeated survival checks; and, where the aim is greener public space, measured canopy or habitat change. The sources located for this check do not provide a national linked record of that kind.", lead)], bg=AMBER_PALE, bar=AMBER),
      Spacer(1, 3 * mm),
      P("The EU's MapMyTree register and satellite canopy data could provide separate context, but neither can by itself verify these national programme totals or survival without matched locations and definitions. No such reconciliation is attempted here.")]

S += [PageBreak(), SectionHeading(4, "Verdict and limits"),
      verdict_box("Largely supported", "The reported figures and pledge are confirmed; achievement and tree survival are not established."),
      Spacer(1, 3 * mm),
      P("Primary records confirm Project Green's 2024 statement of more than 8,000 trees and more than 25,000 shrubs, the 100,000-tree pledge in the 2022 Labour manifesto, and the Minister's approximate cumulative count of around 60,000 trees and more than 100,000 shrubs through end-2025. Confidence is moderate because totals are self-reported, rounded and lack a published project-level inventory."),
      P("This check does not call the pledge failed: its five-year period extends into 2027, after the latest cumulative count located. It also does not call it achieved. The records do not establish survival, net canopy gain or habitat recovery. The Project Green 2024 and parliamentary figures have different scopes and must not be added together."),
      P("Evidence needed to settle delivery and outcomes", h2),
      requests_list([
          "Publish a tree-only, project-level register through the pledge deadline, including dates, locations, species and responsible entity.",
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
      ]),
      Spacer(1, 4 * mm),
      P("Version 1.0 · 3 October 2026 · Draft pending right of reply · Calculations: data/cc-010/checks.csv", cap)]

build_report(Report(
    number="010", out=str(ROOT / "claims" / "CC-010" / "report.pdf"),
    kicker="Land & Trees, Malta", title_lines=["How many trees", "were planted?"],
    subtitle_lines=["Checking government counts against the", "100,000-tree pledge"],
    quote_lines=["“100,000 siġra fil-ħames snin li ġejjin”"],
    attribution="Partit Laburista, 2022 manifesto, pledge 305",
    context="2024 annual count · end-2025 parliamentary answer · pledge deadline 2027",
    verdict="Largely supported", verdict_note="Reported counts confirmed; delivery and survival remain separate questions.",
    footer_lines=["Miżien · independent, science-first fact-checking", "Draft for review · right of reply remains with the maintainer"],
    running_head="Tree-planting counts", version="1.0", date="3 October 2026",
    pdf_title="Miżien Claim Check 010 – How many trees were planted?",
    pdf_subject="Government-reported planting counts and the Labour 100,000-tree pledge", story=S))
